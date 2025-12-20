"""
CDM Research Protocol - Output Validator v1.0

Validates that research outputs match claimed workflow state.
Checks for:
- Required files per execution tier
- Probability sum validity (should sum to ~1.0)
- Deprecated classification terms
- Status.json consistency

Usage:
    python validate_outputs.py <bank_directory>
    python validate_outputs.py <outputs_directory>  # Validates workflow-state.json
"""

import json
import sys
from pathlib import Path
from dataclasses import dataclass, asdict


@dataclass
class ValidationResult:
    """Validation result for a single bank."""
    bank_id: str
    valid: bool
    missing: list
    issues: list


# Required files by execution tier
REQUIRED_BY_TIER = {
    'A': [
        '1-evidence/tier1-evidence.md',
        '2-bayesian/post-tier1-update.md',
        '3-gates/pre-mortem.md',
        '3-gates/gate-1.md',
        '4-adversarial/verdict.md',
        '4-adversarial/steelman.md',
        '5-synthesis/assessment.md',
        'status.json',
    ],
    'B': [
        '1-evidence/tier1-evidence.md',
        '2-bayesian/post-tier1-update.md',
        '3-gates/pre-mortem.md',
        '3-gates/gate-1.md',
        '4-adversarial/verdict.md',
        '5-synthesis/assessment.md',
        'status.json',
    ],
    'C': [
        '1-evidence/tier1-evidence.md',
        '2-bayesian/post-tier1-update.md',
        '3-gates/gate-1.md',
        '4-adversarial/verdict.md',
        '5-synthesis/assessment.md',
        'status.json',
    ]
}

# Deprecated terms that should not appear
DEPRECATED_TERMS = ['NOT ENGAGED', 'NOT_ENGAGED', 'NON-ARCHITECT', 'NON_ARCHITECT']


def get_execution_tier(bank_dir: Path) -> str:
    """Get execution tier from status.json or default to 'B'."""
    status_path = bank_dir / 'status.json'
    if status_path.exists():
        try:
            status = json.loads(status_path.read_text(encoding='utf-8'))
            return status.get('execution_tier', 'B')
        except (json.JSONDecodeError, KeyError):
            pass
    return 'B'


def validate_bank(bank_dir: Path) -> ValidationResult:
    """
    Validate a single bank's outputs.

    Args:
        bank_dir: Path to bank directory

    Returns:
        ValidationResult with any issues found
    """
    tier = get_execution_tier(bank_dir)
    required = REQUIRED_BY_TIER.get(tier, REQUIRED_BY_TIER['B'])

    # Check for missing files
    missing = []
    for rel_path in required:
        full_path = bank_dir / rel_path
        if not full_path.exists():
            missing.append(rel_path)

    issues = []

    # Check status.json consistency
    status_path = bank_dir / 'status.json'
    if status_path.exists():
        try:
            status = json.loads(status_path.read_text(encoding='utf-8'))

            # Check probability sanity
            probs = status.get('current_probability', {})
            architect = probs.get('architect', 0)
            pragmatist = probs.get('pragmatist', 0)
            total = architect + pragmatist

            if abs(total - 1.0) > 0.05:
                issues.append(f"Probability sum {total:.2f} != 1.0 (expected ~1.0)")

            # Check for deprecated classification terms
            classification = status.get('classification', '').upper()
            for term in DEPRECATED_TERMS:
                if term.upper() in classification:
                    issues.append(f"Deprecated classification: '{classification}' - use PRAGMATIST")

            # Check classification/probability alignment
            if classification == 'ARCHITECT' and architect < 0.5:
                issues.append(f"ARCHITECT classification but P(Architect)={architect:.0%}")
            elif classification == 'PRAGMATIST' and architect > 0.5:
                issues.append(f"PRAGMATIST classification but P(Architect)={architect:.0%}")

            # Check confidence bounds
            confidence = status.get('confidence', 0)
            if confidence > 95:
                issues.append(f"Confidence {confidence}% exceeds max 95%")
            elif confidence < 20:
                issues.append(f"Confidence {confidence}% below floor 20%")

        except json.JSONDecodeError as e:
            issues.append(f"Invalid JSON in status.json: {e}")
        except Exception as e:
            issues.append(f"Error reading status.json: {e}")

    return ValidationResult(
        bank_id=bank_dir.name,
        valid=len(missing) == 0 and len(issues) == 0,
        missing=missing,
        issues=issues
    )


def validate_workflow(outputs_dir: Path) -> dict:
    """
    Validate workflow-state.json against actual outputs.

    Args:
        outputs_dir: Path to outputs directory

    Returns:
        dict with validation results
    """
    state_path = outputs_dir / 'state' / 'workflow-state.json'
    if not state_path.exists():
        return {'error': 'workflow-state.json not found', 'valid': False}

    try:
        state = json.loads(state_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e:
        return {'error': f'Invalid JSON: {e}', 'valid': False}

    problems = []
    banks_checked = 0

    # Check each claimed completed bank
    for bank_id in state.get('banks_completed', []):
        # Find bank directory across phases
        bank_found = False
        for phase_dir in outputs_dir.iterdir():
            if not phase_dir.is_dir() or not phase_dir.name.startswith('phase-'):
                continue
            bank_dir = phase_dir / bank_id
            if bank_dir.exists():
                bank_found = True
                banks_checked += 1
                result = validate_bank(bank_dir)
                if not result.valid:
                    problems.append({
                        'bank': bank_id,
                        'missing': result.missing,
                        'issues': result.issues
                    })
                break

        if not bank_found:
            problems.append({
                'bank': bank_id,
                'error': f'Directory not found for claimed completed bank'
            })

    return {
        'checked': banks_checked,
        'problems': problems,
        'valid': len(problems) == 0
    }


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python validate_outputs.py <path>")
        print("       path: bank directory or outputs directory")
        sys.exit(1)

    path = Path(sys.argv[1]).resolve()

    if not path.exists():
        print(f"Error: Path not found: {path}")
        sys.exit(1)

    # Determine mode: single bank or workflow validation
    if (path / 'state').exists():
        # Workflow validation mode
        result = validate_workflow(path)
        print(f"\nWorkflow Validation: {'PASSED' if result['valid'] else 'FAILED'}")
        print(f"Banks checked: {result.get('checked', 0)}")

        if result.get('error'):
            print(f"Error: {result['error']}")

        if result.get('problems'):
            print(f"\nProblems ({len(result['problems'])}):")
            for p in result['problems']:
                print(f"\n  {p['bank']}:")
                if p.get('error'):
                    print(f"    ERROR: {p['error']}")
                if p.get('missing'):
                    print(f"    Missing files: {len(p['missing'])}")
                    for m in p['missing'][:5]:
                        print(f"      - {m}")
                    if len(p['missing']) > 5:
                        print(f"      ... and {len(p['missing'])-5} more")
                if p.get('issues'):
                    print(f"    Issues: {len(p['issues'])}")
                    for i in p['issues']:
                        print(f"      - {i}")

        sys.exit(0 if result['valid'] else 1)

    elif (path / 'status.json').exists() or (path / '1-evidence').exists():
        # Single bank validation mode
        result = validate_bank(path)

        print(f"\nBank Validation: {result.bank_id}")
        print(f"Status: {'PASSED' if result.valid else 'FAILED'}")

        if result.missing:
            print(f"\nMissing files ({len(result.missing)}):")
            for m in result.missing:
                print(f"  - {m}")

        if result.issues:
            print(f"\nIssues ({len(result.issues)}):")
            for i in result.issues:
                print(f"  - {i}")

        # Output JSON for scripting
        print(f"\n{json.dumps(asdict(result), indent=2)}")

        sys.exit(0 if result.valid else 1)

    else:
        print(f"Error: Cannot determine validation mode for: {path}")
        print("Expected either:")
        print("  - Bank directory with status.json or 1-evidence/")
        print("  - Outputs directory with state/ subdirectory")
        sys.exit(1)


if __name__ == "__main__":
    main()
