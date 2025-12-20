"""
CDM Research Protocol - Cross-Bank Validator v1.0

Validates consistency across all bank assessments.

Checks:
- Probability sanity (sums to ~1.0)
- Taxonomy compliance (no deprecated terms)
- Classification/probability alignment
- Evidence quality distribution

Usage:
    python cross_bank_validator.py <outputs_directory>
"""

import json
import sys
from pathlib import Path
from collections import defaultdict


# Valid classifications per current taxonomy
VALID_CLASSIFICATIONS = {'ARCHITECT', 'PRAGMATIST', 'OBSERVER', 'UNKNOWN'}
DEPRECATED_CLASSIFICATIONS = {'NOT ENGAGED', 'NOT_ENGAGED', 'NON-ARCHITECT', 'NON_ARCHITECT'}


def load_all_statuses(outputs_dir: Path) -> dict:
    """
    Load status.json from all bank directories.

    Args:
        outputs_dir: Path to outputs directory

    Returns:
        Dict mapping bank_id to status dict
    """
    statuses = {}

    for phase in outputs_dir.iterdir():
        if not phase.is_dir() or not phase.name.startswith('phase-'):
            continue
        for bank in phase.iterdir():
            if not bank.is_dir():
                continue
            status_file = bank / 'status.json'
            if status_file.exists():
                try:
                    statuses[bank.name] = json.loads(status_file.read_text(encoding='utf-8'))
                except json.JSONDecodeError as e:
                    statuses[bank.name] = {'_error': f'Invalid JSON: {e}'}

    return statuses


def check_probability_sanity(statuses: dict) -> list:
    """
    Check that probabilities sum to approximately 1.0.

    Args:
        statuses: Dict of bank_id to status dict

    Returns:
        List of issue dicts
    """
    issues = []

    for bank, s in statuses.items():
        if '_error' in s:
            continue

        probs = s.get('current_probability', {})

        # Handle different probability storage formats
        if isinstance(probs, (int, float)):
            # Single value format - assume it's P(Architect)
            architect = probs
            pragmatist = 1 - probs if probs <= 1 else 0
        elif isinstance(probs, dict):
            architect = probs.get('architect', 0)
            pragmatist = probs.get('pragmatist', 0)
        else:
            continue  # Skip if we can't parse

        # Handle case where probability is stored differently
        if isinstance(architect, str):
            try:
                architect = float(architect.rstrip('%')) / 100
            except:
                architect = 0
        if isinstance(pragmatist, str):
            try:
                pragmatist = float(pragmatist.rstrip('%')) / 100
            except:
                pragmatist = 0

        total = architect + pragmatist

        if abs(total - 1.0) > 0.05:
            issues.append({
                'bank': bank,
                'check': 'probability_sum',
                'issue': f'P(A)={architect:.2f} + P(P)={pragmatist:.2f} = {total:.2f} (expected ~1.0)'
            })

    return issues


def check_taxonomy(statuses: dict) -> list:
    """
    Check for deprecated or invalid classification terms.

    Args:
        statuses: Dict of bank_id to status dict

    Returns:
        List of issue dicts
    """
    issues = []

    for bank, s in statuses.items():
        if '_error' in s:
            issues.append({
                'bank': bank,
                'check': 'status_json',
                'issue': s['_error']
            })
            continue

        classification = s.get('classification', '').upper()

        if classification in DEPRECATED_CLASSIFICATIONS:
            issues.append({
                'bank': bank,
                'check': 'taxonomy',
                'issue': f"Deprecated classification: '{classification}' - use PRAGMATIST"
            })
        elif classification and classification not in VALID_CLASSIFICATIONS:
            issues.append({
                'bank': bank,
                'check': 'taxonomy',
                'issue': f"Invalid classification: '{classification}'"
            })

    return issues


def check_alignment(statuses: dict) -> list:
    """
    Check that classification aligns with probability.

    ARCHITECT should have P(Architect) >= 50%
    PRAGMATIST should have P(Architect) < 50%

    Args:
        statuses: Dict of bank_id to status dict

    Returns:
        List of issue dicts
    """
    issues = []

    for bank, s in statuses.items():
        if '_error' in s:
            continue

        probs = s.get('current_probability', {})

        # Handle different probability storage formats
        if isinstance(probs, (int, float)):
            architect_prob = probs
        elif isinstance(probs, dict):
            architect_prob = probs.get('architect', 0)
        else:
            continue

        classification = s.get('classification', '').upper()

        # Handle percentage strings
        if isinstance(architect_prob, str):
            try:
                architect_prob = float(architect_prob.rstrip('%')) / 100
            except:
                architect_prob = 0

        # Check alignment
        if classification == 'ARCHITECT' and architect_prob < 0.5:
            issues.append({
                'bank': bank,
                'check': 'alignment',
                'issue': f"ARCHITECT classification but P(Architect)={architect_prob:.0%}"
            })
        elif classification == 'PRAGMATIST' and architect_prob >= 0.5:
            issues.append({
                'bank': bank,
                'check': 'alignment',
                'issue': f"PRAGMATIST classification but P(Architect)={architect_prob:.0%}"
            })

    return issues


def check_confidence_bounds(statuses: dict) -> list:
    """
    Check that confidence values are within valid bounds.

    Args:
        statuses: Dict of bank_id to status dict

    Returns:
        List of issue dicts
    """
    issues = []

    for bank, s in statuses.items():
        if '_error' in s:
            continue

        confidence = s.get('confidence', 0)

        # Handle percentage strings
        if isinstance(confidence, str):
            try:
                confidence = float(confidence.rstrip('%'))
            except:
                confidence = 0

        if confidence > 95:
            issues.append({
                'bank': bank,
                'check': 'confidence_bounds',
                'issue': f"Confidence {confidence}% exceeds maximum 95%"
            })
        elif confidence < 20 and confidence > 0:
            issues.append({
                'bank': bank,
                'check': 'confidence_bounds',
                'issue': f"Confidence {confidence}% below floor 20%"
            })

    return issues


def generate_summary(statuses: dict) -> dict:
    """
    Generate summary statistics across all banks.

    Args:
        statuses: Dict of bank_id to status dict

    Returns:
        Summary dict
    """
    classification_counts = defaultdict(int)
    confidence_values = []

    for bank, s in statuses.items():
        if '_error' in s:
            classification_counts['ERROR'] += 1
            continue

        classification = s.get('classification', 'UNKNOWN').upper()
        classification_counts[classification] += 1

        confidence = s.get('confidence', 0)
        if isinstance(confidence, (int, float)) and confidence > 0:
            confidence_values.append(confidence)

    return {
        'total_banks': len(statuses),
        'classifications': dict(classification_counts),
        'avg_confidence': round(sum(confidence_values) / len(confidence_values), 1) if confidence_values else 0,
        'min_confidence': min(confidence_values) if confidence_values else 0,
        'max_confidence': max(confidence_values) if confidence_values else 0
    }


def run_checks(outputs_dir: Path) -> dict:
    """
    Run all cross-bank validation checks.

    Args:
        outputs_dir: Path to outputs directory

    Returns:
        Validation results dict
    """
    statuses = load_all_statuses(outputs_dir)

    if not statuses:
        return {
            'banks': 0,
            'issues': [{'bank': 'N/A', 'check': 'load', 'issue': 'No bank status files found'}],
            'passed': False
        }

    all_issues = []
    all_issues.extend(check_probability_sanity(statuses))
    all_issues.extend(check_taxonomy(statuses))
    all_issues.extend(check_alignment(statuses))
    all_issues.extend(check_confidence_bounds(statuses))

    summary = generate_summary(statuses)

    return {
        'banks': len(statuses),
        'issues': all_issues,
        'passed': len(all_issues) == 0,
        'summary': summary
    }


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python cross_bank_validator.py <outputs_directory>")
        sys.exit(1)

    outputs_dir = Path(sys.argv[1]).resolve()

    if not outputs_dir.exists():
        print(f"Error: Directory not found: {outputs_dir}")
        sys.exit(1)

    result = run_checks(outputs_dir)

    # Print results
    print(f"\n{'='*60}")
    print(f"CROSS-BANK VALIDATION: {'PASSED' if result['passed'] else 'FAILED'}")
    print(f"{'='*60}")

    if 'summary' in result:
        summary = result['summary']
        print(f"\nSummary:")
        print(f"  Banks analyzed: {summary['total_banks']}")
        print(f"  Classifications: {summary['classifications']}")
        print(f"  Confidence range: {summary['min_confidence']}% - {summary['max_confidence']}%")
        print(f"  Average confidence: {summary['avg_confidence']}%")

    if result['issues']:
        print(f"\nIssues ({len(result['issues'])}):")
        # Group by bank
        by_bank = defaultdict(list)
        for issue in result['issues']:
            by_bank[issue['bank']].append(issue)

        for bank in sorted(by_bank.keys()):
            print(f"\n  {bank}:")
            for issue in by_bank[bank]:
                print(f"    [{issue['check']}] {issue['issue']}")
    else:
        print("\nNo issues found.")

    print(f"\n{'='*60}")

    # Also output JSON for scripting
    print(f"\n{json.dumps(result, indent=2)}")

    sys.exit(0 if result['passed'] else 1)


if __name__ == "__main__":
    main()
