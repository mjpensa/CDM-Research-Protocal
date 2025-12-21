#!/usr/bin/env python3
"""
CDM Research Protocol - State Integrity Validation Suite

Comprehensive validation of state files to ensure:
- Schema version compatibility
- Idempotency key uniqueness
- Probability value constraints (0-1 scale)
- History entry integrity
- Version backup integrity
- Log rotation metadata
- Lock file cleanup

Usage:
    # Validate all state files
    python tools/validate_state_integrity.py outputs/

    # Check specific bank
    python tools/validate_state_integrity.py outputs/ --bank deutsche-bank

    # Validate with strict mode (fail on any error)
    python tools/validate_state_integrity.py outputs/ --strict

    # Generate JSON report
    python tools/validate_state_integrity.py outputs/ --output-json validation-report.json
"""

import argparse
import gzip
import hashlib
import json
import logging
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple

# Add tools directory to path for imports
TOOLS_DIR = Path(__file__).parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Validation constants
VALID_SCHEMA_VERSIONS = ["1.0", "1.1", "1.2", "2.0"]
VALID_STAGES = [
    "initialize", "pre_mortem", "tier1_evidence", "bayesian_1", "gate_1",
    "tier2_evidence", "bayesian_2", "gate_2", "tier3_evidence", "bayesian_3",
    "gate_3", "adversarial_challenge", "final_classification", "synthesis", "complete"
]
VALID_CLASSIFICATIONS = ["ARCHITECT", "PRAGMATIST", "OBSERVER", "UNKNOWN"]


class ValidationSeverity:
    """Severity levels for validation issues."""
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


@dataclass
class ValidationIssue:
    """A single validation issue found."""
    file_path: str
    check_name: str
    severity: str
    message: str
    field: Optional[str] = None
    expected: Optional[str] = None
    actual: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class FileValidationResult:
    """Validation result for a single file."""
    file_path: str
    file_type: str  # status, log, workflow, lock
    valid: bool
    issues: List[ValidationIssue] = field(default_factory=list)
    checks_passed: int = 0
    checks_failed: int = 0

    def to_dict(self) -> dict:
        data = asdict(self)
        data['issues'] = [i.to_dict() if hasattr(i, 'to_dict') else i for i in self.issues]
        return data


@dataclass
class ValidationReport:
    """Complete validation report."""
    outputs_dir: str
    validated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    total_files: int = 0
    files_valid: int = 0
    files_invalid: int = 0
    total_errors: int = 0
    total_warnings: int = 0
    total_info: int = 0
    results: List[FileValidationResult] = field(default_factory=list)
    bank_filter: Optional[str] = None
    is_valid: bool = True

    def to_dict(self) -> dict:
        data = asdict(self)
        data['results'] = [r.to_dict() if hasattr(r, 'to_dict') else r for r in self.results]
        return data


class StateValidator:
    """
    Validates state file integrity across the system.

    Checks performed:
    1. Schema version validity
    2. Probability values in range [0, 1]
    3. Idempotency key uniqueness
    4. Stage sequence validity
    5. Timestamp format validity
    6. History entry consistency
    7. Version backup integrity
    8. Lock file cleanup
    9. Required field presence
    """

    def __init__(self, outputs_dir: Path, bank_filter: Optional[str] = None,
                 strict: bool = False):
        self.outputs_dir = Path(outputs_dir)
        self.bank_filter = bank_filter
        self.strict = strict
        self.report = ValidationReport(outputs_dir=str(outputs_dir), bank_filter=bank_filter)

        # Global tracking for cross-file validation
        self.all_idempotency_keys: Dict[str, Set[str]] = {}  # bank_id -> set of keys

    def validate_all(self) -> ValidationReport:
        """Run all validations."""
        logger.info(f"Validating state files in: {self.outputs_dir}")
        if self.bank_filter:
            logger.info(f"Filtering to bank: {self.bank_filter}")

        # Validate status.json files
        for status_file in self.outputs_dir.glob("**/status.json"):
            if self.bank_filter and self.bank_filter not in str(status_file):
                continue
            result = self._validate_status_file(status_file)
            self._add_result(result)

        # Validate log files
        log_patterns = [
            "**/checkpoint-log.json",
            "**/error-log.json",
            "**/deferred-review-queue.json",
            "**/violation-queue.json"
        ]
        for pattern in log_patterns:
            for log_file in self.outputs_dir.glob(pattern):
                if self.bank_filter and self.bank_filter not in str(log_file):
                    continue
                result = self._validate_log_file(log_file)
                self._add_result(result)

        # Validate workflow-state.json
        for wf_file in self.outputs_dir.glob("**/workflow-state.json"):
            result = self._validate_workflow_file(wf_file)
            self._add_result(result)

        # Check for stale lock files
        lock_results = self._check_stale_locks()
        for result in lock_results:
            self._add_result(result)

        # Cross-file validations
        self._validate_cross_file_consistency()

        # Final validity determination
        self.report.is_valid = self.report.total_errors == 0
        if self.strict:
            self.report.is_valid = self.report.total_errors == 0 and self.report.total_warnings == 0

        return self.report

    def _validate_status_file(self, file_path: Path) -> FileValidationResult:
        """Validate a status.json file."""
        result = FileValidationResult(
            file_path=str(file_path),
            file_type="status",
            valid=True
        )

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            result.valid = False
            result.issues.append(ValidationIssue(
                file_path=str(file_path),
                check_name="json_parse",
                severity=ValidationSeverity.ERROR,
                message=f"Failed to parse JSON: {e}"
            ))
            return result

        # Check schema version
        self._check_schema_version(data, file_path, result)

        # Check required fields
        self._check_required_fields(data, file_path, result, [
            'bank_id', 'bank_name', 'phase'
        ])

        # Check probability values
        self._check_probability_values(data, file_path, result)

        # Check stage validity
        self._check_stage_validity(data, file_path, result)

        # Check timestamps
        self._check_timestamps(data, file_path, result)

        # Check probability history
        self._check_probability_history(data, file_path, result)

        # Check classification validity
        self._check_classification(data, file_path, result)

        # Check version backups
        self._check_version_backups(file_path, result)

        # Determine overall validity
        result.valid = all(
            issue.severity != ValidationSeverity.ERROR
            for issue in result.issues
        )

        return result

    def _validate_log_file(self, file_path: Path) -> FileValidationResult:
        """Validate a log file."""
        result = FileValidationResult(
            file_path=str(file_path),
            file_type="log",
            valid=True
        )

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            result.valid = False
            result.issues.append(ValidationIssue(
                file_path=str(file_path),
                check_name="json_parse",
                severity=ValidationSeverity.ERROR,
                message=f"Failed to parse JSON: {e}"
            ))
            return result

        # Check for rotation metadata if migrated
        if 'schema_version' in data and data['schema_version'] == '2.0':
            if 'rotation_metadata' not in data:
                result.issues.append(ValidationIssue(
                    file_path=str(file_path),
                    check_name="rotation_metadata",
                    severity=ValidationSeverity.WARNING,
                    message="Missing rotation_metadata for v2.0 log file"
                ))
                result.checks_failed += 1
            else:
                result.checks_passed += 1

        # Check entry count (should be bounded)
        entry_field = None
        for field_name in ['entries', 'events', 'queue', 'items']:
            if field_name in data and isinstance(data[field_name], list):
                entry_field = field_name
                break

        if entry_field:
            entry_count = len(data[entry_field])
            if entry_count > 1000:
                result.issues.append(ValidationIssue(
                    file_path=str(file_path),
                    check_name="entry_count",
                    severity=ValidationSeverity.WARNING,
                    message=f"Log file has {entry_count} entries, exceeds recommended max of 1000",
                    field=entry_field,
                    actual=str(entry_count),
                    expected="<= 1000"
                ))
                result.checks_failed += 1
            else:
                result.checks_passed += 1

        result.valid = all(
            issue.severity != ValidationSeverity.ERROR
            for issue in result.issues
        )

        return result

    def _validate_workflow_file(self, file_path: Path) -> FileValidationResult:
        """Validate a workflow-state.json file."""
        result = FileValidationResult(
            file_path=str(file_path),
            file_type="workflow",
            valid=True
        )

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            result.valid = False
            result.issues.append(ValidationIssue(
                file_path=str(file_path),
                check_name="json_parse",
                severity=ValidationSeverity.ERROR,
                message=f"Failed to parse JSON: {e}"
            ))
            return result

        # Check bank list consistency
        all_banks = set()
        for list_name in ['banks_completed', 'banks_in_progress', 'banks_pending', 'banks_blocked']:
            if list_name in data:
                banks = set(data[list_name])
                overlap = all_banks & banks
                if overlap:
                    result.issues.append(ValidationIssue(
                        file_path=str(file_path),
                        check_name="bank_list_overlap",
                        severity=ValidationSeverity.ERROR,
                        message=f"Banks appear in multiple lists: {overlap}",
                        field=list_name
                    ))
                    result.checks_failed += 1
                all_banks.update(banks)

        if not result.issues:
            result.checks_passed += 1

        result.valid = all(
            issue.severity != ValidationSeverity.ERROR
            for issue in result.issues
        )

        return result

    def _check_stale_locks(self) -> List[FileValidationResult]:
        """Check for stale lock files."""
        results = []
        stale_threshold_seconds = 300  # 5 minutes

        for lock_file in self.outputs_dir.glob("**/*.lock"):
            result = FileValidationResult(
                file_path=str(lock_file),
                file_type="lock",
                valid=True
            )

            try:
                # Check lock file age
                mtime = lock_file.stat().st_mtime
                age_seconds = (datetime.now().timestamp() - mtime)

                if age_seconds > stale_threshold_seconds:
                    # Check if process is still alive
                    try:
                        with open(lock_file, 'r') as f:
                            lock_data = json.load(f)
                            pid = lock_data.get('pid')

                            # Simple check - if lock is old, report it
                            result.issues.append(ValidationIssue(
                                file_path=str(lock_file),
                                check_name="stale_lock",
                                severity=ValidationSeverity.WARNING,
                                message=f"Lock file is {age_seconds:.0f} seconds old (PID: {pid})",
                                actual=f"{age_seconds:.0f}s",
                                expected=f"<= {stale_threshold_seconds}s"
                            ))
                            result.checks_failed += 1
                    except (json.JSONDecodeError, KeyError):
                        result.issues.append(ValidationIssue(
                            file_path=str(lock_file),
                            check_name="lock_format",
                            severity=ValidationSeverity.WARNING,
                            message="Lock file has invalid format"
                        ))
                        result.checks_failed += 1
                else:
                    result.checks_passed += 1

            except Exception as e:
                result.issues.append(ValidationIssue(
                    file_path=str(lock_file),
                    check_name="lock_check",
                    severity=ValidationSeverity.WARNING,
                    message=f"Could not check lock file: {e}"
                ))

            if result.issues:
                results.append(result)

        return results

    def _check_schema_version(self, data: dict, file_path: Path,
                              result: FileValidationResult) -> None:
        """Check schema version validity."""
        version = data.get('schema_version')

        if version is None:
            result.issues.append(ValidationIssue(
                file_path=str(file_path),
                check_name="schema_version",
                severity=ValidationSeverity.INFO,
                message="Missing schema_version field (pre-migration file)",
                field="schema_version"
            ))
            result.checks_failed += 1
        elif version not in VALID_SCHEMA_VERSIONS:
            result.issues.append(ValidationIssue(
                file_path=str(file_path),
                check_name="schema_version",
                severity=ValidationSeverity.ERROR,
                message=f"Invalid schema version: {version}",
                field="schema_version",
                expected=str(VALID_SCHEMA_VERSIONS),
                actual=version
            ))
            result.checks_failed += 1
        else:
            result.checks_passed += 1

    def _check_required_fields(self, data: dict, file_path: Path,
                               result: FileValidationResult,
                               required: List[str]) -> None:
        """Check that required fields are present."""
        for field_name in required:
            if field_name not in data:
                result.issues.append(ValidationIssue(
                    file_path=str(file_path),
                    check_name="required_field",
                    severity=ValidationSeverity.ERROR,
                    message=f"Missing required field: {field_name}",
                    field=field_name
                ))
                result.checks_failed += 1
            else:
                result.checks_passed += 1

    def _check_probability_values(self, data: dict, file_path: Path,
                                  result: FileValidationResult) -> None:
        """Check probability values are in valid range [0, 1]."""
        prob_fields = [
            'prior_probability', 'current_probability',
            'probability_architect', 'probability_pragmatist', 'confidence'
        ]

        for field_name in prob_fields:
            if field_name in data and data[field_name] is not None:
                value = data[field_name]

                # Check if in percentage scale (0-100)
                if value > 1.0 and value <= 100.0:
                    result.issues.append(ValidationIssue(
                        file_path=str(file_path),
                        check_name="probability_scale",
                        severity=ValidationSeverity.WARNING,
                        message=f"{field_name} appears to be in percentage scale (0-100)",
                        field=field_name,
                        expected="0-1 scale",
                        actual=str(value)
                    ))
                    result.checks_failed += 1
                elif value < 0 or value > 100:
                    result.issues.append(ValidationIssue(
                        file_path=str(file_path),
                        check_name="probability_range",
                        severity=ValidationSeverity.ERROR,
                        message=f"{field_name} is out of valid range",
                        field=field_name,
                        expected="0-1 or 0-100",
                        actual=str(value)
                    ))
                    result.checks_failed += 1
                else:
                    result.checks_passed += 1

    def _check_stage_validity(self, data: dict, file_path: Path,
                              result: FileValidationResult) -> None:
        """Check stage names are valid."""
        if 'current_stage' in data:
            stage = data['current_stage']
            if stage not in VALID_STAGES:
                result.issues.append(ValidationIssue(
                    file_path=str(file_path),
                    check_name="stage_validity",
                    severity=ValidationSeverity.WARNING,
                    message=f"Unknown stage: {stage}",
                    field="current_stage",
                    expected=str(VALID_STAGES),
                    actual=stage
                ))
                result.checks_failed += 1
            else:
                result.checks_passed += 1

        if 'stages_completed' in data:
            for stage in data['stages_completed']:
                if stage not in VALID_STAGES:
                    result.issues.append(ValidationIssue(
                        file_path=str(file_path),
                        check_name="stage_validity",
                        severity=ValidationSeverity.WARNING,
                        message=f"Unknown completed stage: {stage}",
                        field="stages_completed"
                    ))
                    result.checks_failed += 1

    def _check_timestamps(self, data: dict, file_path: Path,
                          result: FileValidationResult) -> None:
        """Check timestamp formats are valid ISO format."""
        timestamp_fields = ['started_at', 'last_updated', 'completed_at', 'blocked_at']

        for field_name in timestamp_fields:
            if field_name in data and data[field_name] is not None:
                try:
                    # Try to parse as ISO format
                    ts_str = data[field_name]
                    datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
                    result.checks_passed += 1
                except (ValueError, AttributeError):
                    result.issues.append(ValidationIssue(
                        file_path=str(file_path),
                        check_name="timestamp_format",
                        severity=ValidationSeverity.WARNING,
                        message=f"Invalid timestamp format in {field_name}",
                        field=field_name,
                        actual=str(data[field_name]),
                        expected="ISO 8601 format"
                    ))
                    result.checks_failed += 1

    def _check_probability_history(self, data: dict, file_path: Path,
                                   result: FileValidationResult) -> None:
        """Check probability history integrity."""
        if 'probability_history' not in data:
            return

        history = data['probability_history']
        if not isinstance(history, list):
            result.issues.append(ValidationIssue(
                file_path=str(file_path),
                check_name="history_type",
                severity=ValidationSeverity.ERROR,
                message="probability_history is not a list",
                field="probability_history"
            ))
            result.checks_failed += 1
            return

        bank_id = data.get('bank_id', 'unknown')
        if bank_id not in self.all_idempotency_keys:
            self.all_idempotency_keys[bank_id] = set()

        seen_keys = set()
        for i, entry in enumerate(history):
            if not isinstance(entry, dict):
                continue

            # Check idempotency key
            idem_key = entry.get('idempotency_key')
            if idem_key:
                if idem_key in seen_keys:
                    result.issues.append(ValidationIssue(
                        file_path=str(file_path),
                        check_name="idempotency_uniqueness",
                        severity=ValidationSeverity.ERROR,
                        message=f"Duplicate idempotency key at entry {i}: {idem_key}",
                        field="probability_history"
                    ))
                    result.checks_failed += 1
                else:
                    seen_keys.add(idem_key)
                    self.all_idempotency_keys[bank_id].add(idem_key)
                    result.checks_passed += 1

            # Check prior/posterior consistency
            prior = entry.get('prior')
            posterior = entry.get('posterior')
            if prior is not None and posterior is not None:
                if prior > 1.0 or posterior > 1.0:
                    result.issues.append(ValidationIssue(
                        file_path=str(file_path),
                        check_name="history_probability_scale",
                        severity=ValidationSeverity.WARNING,
                        message=f"History entry {i} uses percentage scale",
                        field="probability_history"
                    ))
                    result.checks_failed += 1

    def _check_classification(self, data: dict, file_path: Path,
                              result: FileValidationResult) -> None:
        """Check classification validity."""
        if 'classification' in data and data['classification'] is not None:
            classification = data['classification'].upper() if isinstance(data['classification'], str) else str(data['classification'])
            if classification not in VALID_CLASSIFICATIONS:
                result.issues.append(ValidationIssue(
                    file_path=str(file_path),
                    check_name="classification_validity",
                    severity=ValidationSeverity.WARNING,
                    message=f"Unknown classification: {data['classification']}",
                    field="classification",
                    expected=str(VALID_CLASSIFICATIONS),
                    actual=data['classification']
                ))
                result.checks_failed += 1
            else:
                result.checks_passed += 1

    def _check_version_backups(self, file_path: Path,
                               result: FileValidationResult) -> None:
        """Check version backup integrity."""
        versions_dir = file_path.parent / "versions"

        if not versions_dir.exists():
            # Not an error - versioning might not be enabled
            return

        version_files = list(versions_dir.glob("status.*.json.gz"))
        if not version_files:
            return

        # Check version sequence
        version_numbers = []
        for vf in version_files:
            try:
                # Extract version number from filename like "status.1.json.gz"
                parts = vf.name.split('.')
                if len(parts) >= 3:
                    version_numbers.append(int(parts[1]))
            except ValueError:
                result.issues.append(ValidationIssue(
                    file_path=str(vf),
                    check_name="version_naming",
                    severity=ValidationSeverity.WARNING,
                    message=f"Invalid version file naming: {vf.name}"
                ))
                result.checks_failed += 1

        # Check for gaps in version sequence
        if version_numbers:
            version_numbers.sort()
            expected_seq = list(range(1, max(version_numbers) + 1))
            if version_numbers != expected_seq:
                result.issues.append(ValidationIssue(
                    file_path=str(versions_dir),
                    check_name="version_sequence",
                    severity=ValidationSeverity.INFO,
                    message=f"Gap in version sequence: have {version_numbers}, expected {expected_seq}"
                ))

        # Verify each version file can be decompressed
        for vf in version_files:
            try:
                with gzip.open(vf, 'rt') as f:
                    json.load(f)
                result.checks_passed += 1
            except Exception as e:
                result.issues.append(ValidationIssue(
                    file_path=str(vf),
                    check_name="version_integrity",
                    severity=ValidationSeverity.ERROR,
                    message=f"Version backup corrupted: {e}"
                ))
                result.checks_failed += 1

    def _validate_cross_file_consistency(self) -> None:
        """Perform cross-file consistency checks."""
        # Check for duplicate idempotency keys across banks (should never happen)
        all_keys = set()
        for bank_id, keys in self.all_idempotency_keys.items():
            overlap = all_keys & keys
            if overlap:
                logger.warning(f"Idempotency key collision detected: {overlap}")
            all_keys.update(keys)

    def _add_result(self, result: FileValidationResult) -> None:
        """Add a validation result to the report."""
        self.report.results.append(result)
        self.report.total_files += 1

        if result.valid:
            self.report.files_valid += 1
        else:
            self.report.files_invalid += 1

        for issue in result.issues:
            if issue.severity == ValidationSeverity.ERROR:
                self.report.total_errors += 1
            elif issue.severity == ValidationSeverity.WARNING:
                self.report.total_warnings += 1
            elif issue.severity == ValidationSeverity.INFO:
                self.report.total_info += 1


def print_report(report: ValidationReport, verbose: bool = False) -> None:
    """Print validation report to console."""
    print("\n" + "=" * 60)
    print("STATE INTEGRITY VALIDATION REPORT")
    print("=" * 60)
    print(f"Directory:      {report.outputs_dir}")
    if report.bank_filter:
        print(f"Bank filter:    {report.bank_filter}")
    print(f"Validated at:   {report.validated_at}")
    print("-" * 60)
    print(f"Total files:    {report.total_files}")
    print(f"  Valid:        {report.files_valid}")
    print(f"  Invalid:      {report.files_invalid}")
    print(f"Total errors:   {report.total_errors}")
    print(f"Total warnings: {report.total_warnings}")
    print(f"Total info:     {report.total_info}")
    print("-" * 60)

    status = "PASSED" if report.is_valid else "FAILED"
    status_color = "\033[92m" if report.is_valid else "\033[91m"
    print(f"Overall status: {status_color}{status}\033[0m")
    print("=" * 60)

    # Print issues if any, or if verbose
    if report.total_errors > 0 or report.total_warnings > 0 or verbose:
        print("\nDETAILED ISSUES:")

        for result in report.results:
            if result.issues or verbose:
                status_icon = '✓' if result.valid else '✗'
                print(f"\n{status_icon} [{result.file_type}] {result.file_path}")
                print(f"   Checks: {result.checks_passed} passed, {result.checks_failed} failed")

                for issue in result.issues:
                    severity_color = {
                        ValidationSeverity.ERROR: "\033[91m",
                        ValidationSeverity.WARNING: "\033[93m",
                        ValidationSeverity.INFO: "\033[94m"
                    }.get(issue.severity, "")

                    print(f"   {severity_color}[{issue.severity}]\033[0m {issue.check_name}: {issue.message}")
                    if issue.field:
                        print(f"      Field: {issue.field}")
                    if issue.expected and issue.actual:
                        print(f"      Expected: {issue.expected}")
                        print(f"      Actual: {issue.actual}")


def main():
    parser = argparse.ArgumentParser(
        description="Validate CDM state file integrity",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate all state files
  python validate_state_integrity.py outputs/

  # Check specific bank
  python validate_state_integrity.py outputs/ --bank deutsche-bank

  # Validate with strict mode (fail on warnings too)
  python validate_state_integrity.py outputs/ --strict

  # Generate JSON report
  python validate_state_integrity.py outputs/ --output-json report.json
        """
    )

    parser.add_argument(
        'outputs_dir',
        type=Path,
        help='Path to outputs directory'
    )
    parser.add_argument(
        '--bank',
        type=str,
        help='Filter to specific bank ID'
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Fail on warnings in addition to errors'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show all files, not just those with issues'
    )
    parser.add_argument(
        '--output-json',
        type=Path,
        help='Write validation report to JSON file'
    )
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Only output if there are issues'
    )

    args = parser.parse_args()

    if not args.outputs_dir.exists():
        print(f"Error: Directory not found: {args.outputs_dir}")
        sys.exit(1)

    # Run validation
    validator = StateValidator(
        outputs_dir=args.outputs_dir,
        bank_filter=args.bank,
        strict=args.strict
    )

    report = validator.validate_all()

    # Print report
    if not args.quiet or not report.is_valid:
        print_report(report, verbose=args.verbose)

    # Write JSON report if requested
    if args.output_json:
        with open(args.output_json, 'w') as f:
            json.dump(report.to_dict(), f, indent=2)
        print(f"\nValidation report written to: {args.output_json}")

    # Exit with appropriate code
    sys.exit(0 if report.is_valid else 1)


if __name__ == "__main__":
    main()
