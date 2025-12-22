"""
CDM Research Protocol - Bank Completeness Audit v1.0

Audits bank research outputs to ensure all required files are present
and have non-trivial content. Designed to catch incomplete research
before banks are marked as complete.

Usage:
    python tools/audit_completeness.py --phase 1                    # Audit entire phase
    python tools/audit_completeness.py --bank hsbc --phase 1        # Audit single bank
    python tools/audit_completeness.py --all                        # Audit all phases

Exit codes:
    0 = All audited banks are COMPLETE
    1 = One or more banks are INCOMPLETE
    2 = Error (invalid arguments, missing directories)
"""

import argparse
import json
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional

# Project paths
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
CONFIG_DIR = PROJECT_ROOT / "config"

# Required files for a complete bank research output (17 files)
REQUIRED_FILES = [
    '1-evidence/tier1-evidence.md',
    '1-evidence/tier2-evidence.md',
    '1-evidence/tier3-evidence.md',
    '2-bayesian/post-tier1-update.md',
    '2-bayesian/post-tier2-update.md',
    '2-bayesian/post-tier3-update.md',
    '3-gates/pre-mortem.md',
    '3-gates/gate-1.md',
    '3-gates/gate-2.md',
    '3-gates/gate-3.md',
    '4-adversarial/counter-case.md',
    '4-adversarial/disconfirming-searches.md',
    '4-adversarial/steelman.md',
    '4-adversarial/verdict.md',
    '5-synthesis/assessment.md',
    'status.json',
    'evidence.json',
]

# Minimum file sizes to prevent empty/truncated files from passing
MIN_FILE_SIZES = {
    'status.json': 300,
    'evidence.json': 400,
    '.md': 100,
}

# Phase folder mapping
PHASE_FOLDERS = {
    1: 'phase-1-european-tier1',
    2: 'phase-2-uk-regional',
    3: 'phase-3-japanese',
    4: 'phase-4-other-european',
    5: 'phase-5-spanish',
    6: 'phase-6-deep-dives',
    7: 'phase-7-emerging-markets',
    8: 'phase-8-us-investment-banks',
    9: 'phase-9-us-custody-banks',
}


@dataclass
class FileAuditResult:
    """Result for a single file check."""
    path: str
    exists: bool
    size: int = 0
    min_size: int = 0
    valid: bool = False
    issue: str = ""


@dataclass
class BankAuditResult:
    """Result for a single bank audit."""
    bank_id: str
    phase: int
    files_present: int = 0
    files_required: int = len(REQUIRED_FILES)
    status: str = "UNKNOWN"
    missing_files: List[str] = field(default_factory=list)
    truncated_files: List[str] = field(default_factory=list)
    file_results: List[FileAuditResult] = field(default_factory=list)

    @property
    def is_complete(self) -> bool:
        return self.status == "COMPLETE"


def get_min_size(filename: str) -> int:
    """Get minimum size threshold for a file."""
    if filename in MIN_FILE_SIZES:
        return MIN_FILE_SIZES[filename]
    ext = Path(filename).suffix
    return MIN_FILE_SIZES.get(ext, 50)


def audit_file(bank_dir: Path, rel_path: str) -> FileAuditResult:
    """Audit a single file for existence and minimum size."""
    full_path = bank_dir / rel_path
    filename = Path(rel_path).name
    min_size = get_min_size(filename)

    result = FileAuditResult(
        path=rel_path,
        exists=full_path.exists(),
        min_size=min_size
    )

    if not result.exists:
        result.issue = "MISSING"
        return result

    result.size = full_path.stat().st_size

    if result.size < min_size:
        result.issue = f"TRUNCATED ({result.size} < {min_size} bytes)"
        return result

    result.valid = True
    return result


def audit_bank(bank_id: str, phase: int) -> BankAuditResult:
    """Audit a single bank's research outputs."""
    phase_folder = PHASE_FOLDERS.get(phase)
    if not phase_folder:
        result = BankAuditResult(bank_id=bank_id, phase=phase)
        result.status = "ERROR"
        return result

    bank_dir = OUTPUTS_DIR / phase_folder / bank_id
    result = BankAuditResult(bank_id=bank_id, phase=phase)

    if not bank_dir.exists():
        result.status = "NOT_STARTED"
        result.missing_files = REQUIRED_FILES.copy()
        return result

    # Audit each required file
    for rel_path in REQUIRED_FILES:
        file_result = audit_file(bank_dir, rel_path)
        result.file_results.append(file_result)

        if not file_result.exists:
            result.missing_files.append(rel_path)
        elif not file_result.valid:
            result.truncated_files.append(f"{rel_path} ({file_result.issue})")
        else:
            result.files_present += 1

    # Determine overall status
    if result.files_present == result.files_required:
        result.status = "COMPLETE"
    elif result.files_present == 0:
        result.status = "NOT_STARTED"
    else:
        result.status = "INCOMPLETE"

    return result


def get_banks_in_phase(phase: int) -> List[str]:
    """Get list of bank IDs for a phase from bank-manifest.json."""
    manifest_path = CONFIG_DIR / "bank-manifest.json"

    if not manifest_path.exists():
        return []

    try:
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        return [
            bank['bank_id']
            for bank in manifest.get('banks', [])
            if bank.get('phase') == phase
        ]
    except (json.JSONDecodeError, KeyError):
        return []


def audit_phase(phase: int) -> List[BankAuditResult]:
    """Audit all banks in a phase."""
    banks = get_banks_in_phase(phase)
    return [audit_bank(bank_id, phase) for bank_id in banks]


def audit_all_phases() -> Dict[int, List[BankAuditResult]]:
    """Audit all banks in all phases."""
    results = {}
    for phase in PHASE_FOLDERS.keys():
        results[phase] = audit_phase(phase)
    return results


def print_bank_result(result: BankAuditResult, verbose: bool = False):
    """Print audit result for a single bank."""
    # Use ASCII-safe characters for Windows compatibility
    status_icon = "[OK]" if result.is_complete else "[X]"

    # Format: bank-id:     17/17 files [OK] COMPLETE
    print(f"{result.bank_id:20s} {result.files_present:2d}/{result.files_required} files {status_icon} {result.status}")

    if verbose and result.missing_files:
        print(f"  Missing ({len(result.missing_files)}):")
        for f in result.missing_files[:5]:
            print(f"    - {f}")
        if len(result.missing_files) > 5:
            print(f"    ... and {len(result.missing_files) - 5} more")

    if verbose and result.truncated_files:
        print(f"  Truncated ({len(result.truncated_files)}):")
        for f in result.truncated_files[:3]:
            print(f"    - {f}")


def print_phase_results(phase: int, results: List[BankAuditResult], verbose: bool = False):
    """Print audit results for a phase."""
    phase_name = PHASE_FOLDERS.get(phase, f"Phase {phase}")

    print(f"\n{phase_name} Completeness Audit")
    print("=" * 50)

    for result in results:
        print_bank_result(result, verbose)

    # Summary
    complete = sum(1 for r in results if r.is_complete)
    total = len(results)
    print("-" * 50)
    print(f"Summary: {complete}/{total} banks complete")


def main():
    parser = argparse.ArgumentParser(
        description="Audit CDM Research Protocol bank outputs for completeness",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Audit entire phase
    python tools/audit_completeness.py --phase 1

    # Audit single bank
    python tools/audit_completeness.py --bank hsbc --phase 1

    # Audit all phases
    python tools/audit_completeness.py --all

    # Verbose output with missing file details
    python tools/audit_completeness.py --phase 1 --verbose
        """
    )

    parser.add_argument("--phase", type=int, help="Phase number (1-9)")
    parser.add_argument("--bank", help="Bank ID (requires --phase)")
    parser.add_argument("--all", action="store_true", help="Audit all phases")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed file lists")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    # Validate arguments
    if not args.all and not args.phase:
        parser.error("Either --phase or --all must be specified")

    if args.bank and not args.phase:
        parser.error("--bank requires --phase")

    all_complete = True

    try:
        if args.bank:
            # Single bank audit
            result = audit_bank(args.bank, args.phase)

            if args.json:
                output = {
                    'bank_id': result.bank_id,
                    'phase': result.phase,
                    'files_present': result.files_present,
                    'files_required': result.files_required,
                    'status': result.status,
                    'is_complete': result.is_complete,
                    'missing_files': result.missing_files,
                    'truncated_files': result.truncated_files
                }
                print(json.dumps(output, indent=2))
            else:
                print(f"\nBank Audit: {args.bank} (Phase {args.phase})")
                print("=" * 50)
                print_bank_result(result, args.verbose)

            all_complete = result.is_complete

        elif args.all:
            # All phases audit
            all_results = audit_all_phases()

            if args.json:
                output = {}
                for phase, results in all_results.items():
                    output[f"phase_{phase}"] = [
                        {
                            'bank_id': r.bank_id,
                            'status': r.status,
                            'files_present': r.files_present,
                            'files_required': r.files_required
                        }
                        for r in results
                    ]
                print(json.dumps(output, indent=2))
            else:
                for phase, results in all_results.items():
                    if results:
                        print_phase_results(phase, results, args.verbose)
                        if any(not r.is_complete for r in results):
                            all_complete = False

        else:
            # Single phase audit
            results = audit_phase(args.phase)

            if not results:
                print(f"Error: No banks found for phase {args.phase}")
                return 2

            if args.json:
                output = {
                    'phase': args.phase,
                    'banks': [
                        {
                            'bank_id': r.bank_id,
                            'status': r.status,
                            'files_present': r.files_present,
                            'files_required': r.files_required,
                            'missing_files': r.missing_files
                        }
                        for r in results
                    ]
                }
                print(json.dumps(output, indent=2))
            else:
                print_phase_results(args.phase, results, args.verbose)

            all_complete = all(r.is_complete for r in results)

        return 0 if all_complete else 1

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
