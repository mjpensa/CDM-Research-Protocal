"""
CDM Research Protocol - New Outputs Validator v1.0

Validates the three new outputs added to the research protocol:
1. evidence.json - Structured Evidence Ledger (PRIMARY output)
2. confidence-calibration.md - Per-Bank Confidence Calculation
3. contradiction-resolution.md - Contradiction Resolution Log (if needed)

Usage:
    python validate_new_outputs.py outputs/phase-1/deutsche-bank/
    python validate_new_outputs.py --batch outputs/phase-1-european-tier1/
    python validate_new_outputs.py --all outputs/
"""

import json
import sys
import re
import logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

# --- LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of a validation check."""
    valid: bool
    file_path: Optional[str] = None
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    info: list = field(default_factory=list)


def validate_evidence_json(bank_dir: Path) -> ValidationResult:
    """
    Validate evidence.json exists and is schema-compliant.

    Per CLAUDE.md Ledger-First mandate:
    - evidence.json is the PRIMARY output
    - Must contain evidence_items array
    - Each item must have required fields

    Args:
        bank_dir: Path to bank directory

    Returns:
        ValidationResult with status and issues
    """
    result = ValidationResult(valid=True)
    json_path = bank_dir / 'evidence.json'
    result.file_path = str(json_path)

    # Check file exists
    if not json_path.exists():
        result.valid = False
        result.errors.append("evidence.json not found (CRITICAL: Ledger-First mandate violation)")
        return result

    # Load and validate JSON structure
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        result.valid = False
        result.errors.append(f"Invalid JSON: {e}")
        return result

    # Check required top-level fields
    required_fields = ['bank_id', 'bank_name', 'evidence_items']
    for field in required_fields:
        if field not in data:
            result.valid = False
            result.errors.append(f"Missing required field: {field}")

    # Check evidence_items array
    items = data.get('evidence_items', [])
    if not isinstance(items, list):
        result.valid = False
        result.errors.append("evidence_items must be an array")
        return result

    if len(items) == 0:
        result.warnings.append("evidence_items array is empty")

    # Validate each evidence item
    required_item_fields = ['id', 'claim', 'tier', 'claim_type']
    valid_tiers = [1, 2, 3]
    valid_claim_types = [
        'production_usage', 'pilot_or_poc', 'membership_or_participation',
        'open_source_contribution', 'vendor_proxy_signal', 'hiring_signal'
    ]

    for i, item in enumerate(items):
        item_id = item.get('id', f'item_{i}')

        # Check required fields
        for field in required_item_fields:
            if field not in item:
                result.errors.append(f"{item_id}: Missing required field '{field}'")
                result.valid = False

        # Validate tier
        tier = item.get('tier')
        if tier and tier not in valid_tiers:
            result.errors.append(f"{item_id}: Invalid tier '{tier}' (must be 1, 2, or 3)")
            result.valid = False

        # Validate claim_type
        claim_type = item.get('claim_type')
        if claim_type and claim_type not in valid_claim_types:
            result.warnings.append(f"{item_id}: Non-standard claim_type '{claim_type}'")

        # Check for lr_mapping (new field)
        if 'lr_mapping' in item:
            lr_mapping = item['lr_mapping']
            if not isinstance(lr_mapping, dict):
                result.warnings.append(f"{item_id}: lr_mapping should be an object")
            elif 'likelihood_ratio' not in lr_mapping:
                result.warnings.append(f"{item_id}: lr_mapping missing likelihood_ratio")
            else:
                result.info.append(f"{item_id}: Has lr_mapping (LR = {lr_mapping.get('likelihood_ratio')})")

    # Check for null_results array
    if 'null_results' in data:
        null_results = data['null_results']
        if not isinstance(null_results, list):
            result.warnings.append("null_results should be an array")
        else:
            result.info.append(f"null_results: {len(null_results)} entries")

    # Check for meta section
    if 'meta' in data:
        meta = data['meta']
        if 'tier_completed' in meta:
            result.info.append(f"Highest tier completed: {meta['tier_completed']}")
    else:
        result.warnings.append("Missing 'meta' section")

    # Check for trust_metrics (from trust_audit)
    if 'trust_metrics' in data:
        result.info.append("trust_metrics present (trust_audit has run)")
    else:
        result.warnings.append("No trust_metrics - run trust_audit.py")

    return result


def validate_confidence_calibration(bank_dir: Path) -> ValidationResult:
    """
    Validate confidence-calibration.md exists and matches assessment.md.

    Per Phase 2 implementation:
    - confidence-calibration.md must exist if assessment.md exists
    - Final confidence value must match between files

    Args:
        bank_dir: Path to bank directory

    Returns:
        ValidationResult with status and issues
    """
    result = ValidationResult(valid=True)
    synthesis_dir = bank_dir / '5-synthesis'
    calibration_path = synthesis_dir / 'confidence-calibration.md'
    assessment_path = synthesis_dir / 'assessment.md'

    result.file_path = str(calibration_path)

    # If assessment.md doesn't exist, calibration is not required yet
    if not assessment_path.exists():
        result.info.append("assessment.md not found - confidence-calibration.md not yet required")
        return result

    # If assessment.md exists, calibration MUST exist
    if not calibration_path.exists():
        result.valid = False
        result.errors.append("confidence-calibration.md not found but assessment.md exists (REQUIRED)")
        return result

    # Both files exist - check confidence values match
    try:
        calibration_content = calibration_path.read_text(encoding='utf-8')
        assessment_content = assessment_path.read_text(encoding='utf-8')
    except Exception as e:
        result.valid = False
        result.errors.append(f"Could not read files: {e}")
        return result

    # Extract confidence from calibration file
    # Look for "FINAL CONFIDENCE:" pattern
    calibration_confidence = None
    final_match = re.search(r'FINAL CONFIDENCE:\s*(\d+)%', calibration_content)
    if final_match:
        calibration_confidence = int(final_match.group(1))
    else:
        # Alternative pattern
        final_match = re.search(r'Final Confidence:\s*(\d+)%', calibration_content)
        if final_match:
            calibration_confidence = int(final_match.group(1))

    # Extract confidence from assessment file
    # Look for "Confidence:" or "Confidence Level:" pattern
    assessment_confidence = None
    conf_match = re.search(r'Confidence(?:\s+Level)?:\s*(\d+)%', assessment_content)
    if conf_match:
        assessment_confidence = int(conf_match.group(1))

    if calibration_confidence is None:
        result.warnings.append("Could not extract final confidence from confidence-calibration.md")
    else:
        result.info.append(f"Calibration confidence: {calibration_confidence}%")

    if assessment_confidence is None:
        result.warnings.append("Could not extract confidence from assessment.md")
    else:
        result.info.append(f"Assessment confidence: {assessment_confidence}%")

    # Check match
    if calibration_confidence is not None and assessment_confidence is not None:
        if calibration_confidence != assessment_confidence:
            result.valid = False
            result.errors.append(
                f"Confidence mismatch: calibration={calibration_confidence}% vs assessment={assessment_confidence}%"
            )
        else:
            result.info.append("Confidence values match between files")

    # Check for required sections in calibration file
    required_sections = [
        'Evidence Tier Assessment',
        'Calibration Calculation',
        'Betting Test',
        'Confidence Rationale'
    ]

    for section in required_sections:
        if section.lower() not in calibration_content.lower():
            result.warnings.append(f"Missing section in calibration: {section}")

    return result


def validate_contradiction_resolution(bank_dir: Path) -> ValidationResult:
    """
    Validate contradiction-resolution.md exists if CONTRADICTIONS_DETECTED flag is set.

    Per Phase 3 implementation:
    - If trust_metrics has CONTRADICTIONS_DETECTED flag, resolution file must exist
    - File must contain resolution for each contradiction

    Args:
        bank_dir: Path to bank directory

    Returns:
        ValidationResult with status and issues
    """
    result = ValidationResult(valid=True)
    gates_dir = bank_dir / '3-gates'
    resolution_path = gates_dir / 'contradiction-resolution.md'
    json_path = bank_dir / 'evidence.json'

    result.file_path = str(resolution_path)

    # Check if evidence.json exists and has contradictions flag
    if not json_path.exists():
        result.info.append("evidence.json not found - cannot check for contradictions")
        return result

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        result.warnings.append(f"Could not read evidence.json: {e}")
        return result

    trust_metrics = data.get('trust_metrics', {})
    flags = trust_metrics.get('flags', [])
    contradictions = data.get('contradictions', [])
    contradiction_details = data.get('contradiction_details', [])

    has_contradictions_flag = 'CONTRADICTIONS_DETECTED' in flags
    contradiction_count = len(contradictions)

    if has_contradictions_flag or contradiction_count > 0:
        result.info.append(f"CONTRADICTIONS_DETECTED: {contradiction_count} contradiction(s)")

        # Resolution file is required
        if not resolution_path.exists():
            result.valid = False
            result.errors.append(
                f"contradiction-resolution.md not found but {contradiction_count} contradiction(s) detected (REQUIRED)"
            )
            return result

        # File exists - validate content
        try:
            content = resolution_path.read_text(encoding='utf-8')
        except Exception as e:
            result.valid = False
            result.errors.append(f"Could not read contradiction-resolution.md: {e}")
            return result

        # Check for summary section
        if 'summary' not in content.lower():
            result.warnings.append("Missing Summary section")

        # Count documented contradictions in resolution file
        documented = content.lower().count('contradiction')
        if documented < contradiction_count:
            result.warnings.append(
                f"Resolution file may not address all contradictions "
                f"(found {documented} mentions, expected {contradiction_count})"
            )

        # Check for resolution status
        resolved_count = content.lower().count('resolved')
        unresolved_count = content.lower().count('unresolved')

        result.info.append(f"Resolution mentions: resolved={resolved_count}, unresolved={unresolved_count}")

        # Check for confidence impact
        if 'confidence impact' not in content.lower():
            result.warnings.append("Missing 'Confidence Impact' documentation")

    else:
        # No contradictions - file should not exist or is optional
        if resolution_path.exists():
            result.info.append("contradiction-resolution.md exists but no contradictions detected (OK)")
        else:
            result.info.append("No contradictions detected, resolution file not required")

    return result


def validate_cross_references(bank_dir: Path) -> ValidationResult:
    """
    Validate cross-references between new output files.

    Checks:
    - evidence.json is referenced by other files
    - Confidence values are consistent across files
    - Contradiction resolutions are referenced in Bayesian updates

    Args:
        bank_dir: Path to bank directory

    Returns:
        ValidationResult with status and issues
    """
    result = ValidationResult(valid=True)
    result.file_path = str(bank_dir)

    json_path = bank_dir / 'evidence.json'
    calibration_path = bank_dir / '5-synthesis' / 'confidence-calibration.md'
    resolution_path = bank_dir / '3-gates' / 'contradiction-resolution.md'
    bayesian_dir = bank_dir / '2-bayesian'

    # Check if Bayesian updates reference evidence.json
    if bayesian_dir.exists():
        for bayesian_file in bayesian_dir.glob('post-tier*.md'):
            try:
                content = bayesian_file.read_text(encoding='utf-8')
                if 'evidence.json' not in content.lower() and 'lr_mapping' not in content.lower():
                    result.info.append(f"{bayesian_file.name}: No explicit evidence.json reference (OK for legacy)")
            except Exception:
                pass

    # Check if contradiction resolution is referenced in calibration
    if calibration_path.exists() and resolution_path.exists():
        try:
            calibration_content = calibration_path.read_text(encoding='utf-8')
            if 'contradiction' not in calibration_content.lower():
                result.warnings.append(
                    "confidence-calibration.md does not reference contradictions "
                    "(contradiction-resolution.md exists)"
                )
        except Exception:
            pass

    result.info.append("Cross-reference validation complete")
    return result


def run_all_validations(bank_dir: Path) -> dict:
    """
    Run all validations for a bank directory.

    Args:
        bank_dir: Path to bank directory

    Returns:
        dict with all validation results
    """
    bank_dir = Path(bank_dir)

    if not bank_dir.is_dir():
        return {
            'bank_id': str(bank_dir),
            'valid': False,
            'error': f'Not a directory: {bank_dir}'
        }

    results = {
        'bank_id': bank_dir.name,
        'valid': True,
        'validations': {}
    }

    # Run each validation
    validations = [
        ('evidence_json', validate_evidence_json),
        ('confidence_calibration', validate_confidence_calibration),
        ('contradiction_resolution', validate_contradiction_resolution),
        ('cross_references', validate_cross_references),
    ]

    for name, validator in validations:
        try:
            result = validator(bank_dir)
            results['validations'][name] = {
                'valid': result.valid,
                'file_path': result.file_path,
                'errors': result.errors,
                'warnings': result.warnings,
                'info': result.info
            }
            if not result.valid:
                results['valid'] = False
        except Exception as e:
            results['validations'][name] = {
                'valid': False,
                'error': str(e)
            }
            results['valid'] = False

    return results


def print_validation_report(results: dict):
    """Print formatted validation report."""
    bank_id = results.get('bank_id', 'Unknown')
    overall_valid = results.get('valid', False)

    print("\n" + "=" * 70)
    print(f"VALIDATION REPORT: {bank_id}")
    print("=" * 70)

    status = "PASS" if overall_valid else "FAIL"
    print(f"\nOverall Status: {status}")

    validations = results.get('validations', {})

    for name, validation in validations.items():
        print(f"\n--- {name.replace('_', ' ').title()} ---")
        valid = validation.get('valid', False)
        print(f"Status: {'PASS' if valid else 'FAIL'}")

        if validation.get('file_path'):
            print(f"File: {validation['file_path']}")

        for error in validation.get('errors', []):
            print(f"  ERROR: {error}")

        for warning in validation.get('warnings', []):
            print(f"  WARNING: {warning}")

        for info in validation.get('info', []):
            print(f"  INFO: {info}")

    print("\n" + "=" * 70)


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    if sys.argv[1] == '--batch':
        if len(sys.argv) < 3:
            print("Error: --batch requires a directory path")
            sys.exit(1)

        directory = Path(sys.argv[2])

        # Find all bank directories (those with evidence.json or 1-evidence/)
        bank_dirs = []
        for path in directory.rglob('evidence.json'):
            bank_dirs.append(path.parent)
        for path in directory.rglob('1-evidence'):
            if path.is_dir() and path.parent not in bank_dirs:
                bank_dirs.append(path.parent)

        bank_dirs = sorted(set(bank_dirs))
        print(f"Found {len(bank_dirs)} bank directories")

        all_results = []
        for bank_dir in bank_dirs:
            results = run_all_validations(bank_dir)
            all_results.append(results)
            print_validation_report(results)

        # Summary
        print("\n" + "=" * 70)
        print("BATCH SUMMARY")
        print("=" * 70)
        passed = sum(1 for r in all_results if r.get('valid', False))
        failed = len(all_results) - passed
        print(f"Passed: {passed} | Failed: {failed} | Total: {len(all_results)}")

        if failed > 0:
            print("\nFailed banks:")
            for r in all_results:
                if not r.get('valid', False):
                    print(f"  - {r.get('bank_id')}")

        sys.exit(0 if failed == 0 else 1)

    elif sys.argv[1] == '--all':
        if len(sys.argv) < 3:
            print("Error: --all requires a directory path")
            sys.exit(1)

        # Same as batch but more comprehensive
        directory = Path(sys.argv[2])
        bank_dirs = set()

        for path in directory.rglob('evidence.json'):
            bank_dirs.add(path.parent)
        for path in directory.rglob('1-evidence'):
            if path.is_dir():
                bank_dirs.add(path.parent)

        bank_dirs = sorted(bank_dirs)
        print(f"Found {len(bank_dirs)} bank directories")

        all_results = []
        for bank_dir in bank_dirs:
            results = run_all_validations(bank_dir)
            all_results.append(results)

        # Print only failures for brevity
        failed = [r for r in all_results if not r.get('valid', False)]

        if failed:
            print(f"\n{len(failed)} bank(s) with validation failures:")
            for r in failed:
                print_validation_report(r)
        else:
            print(f"\nAll {len(all_results)} banks passed validation")

        sys.exit(0 if len(failed) == 0 else 1)

    else:
        # Single bank validation
        bank_dir = Path(sys.argv[1])
        results = run_all_validations(bank_dir)
        print_validation_report(results)
        sys.exit(0 if results.get('valid', False) else 1)


if __name__ == '__main__':
    main()
