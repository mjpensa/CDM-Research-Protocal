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
from collections import defaultdict, Counter

# Import config loader for manifest and priors
SCRIPT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR))

from config_loader import load_bank_manifest, get_default_priors


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
            except (ValueError, AttributeError):
                architect = 0
        if isinstance(pragmatist, str):
            try:
                pragmatist = float(pragmatist.rstrip('%')) / 100
            except (ValueError, AttributeError):
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
            except (ValueError, AttributeError):
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
            except (ValueError, AttributeError):
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


def load_anchor_points() -> dict:
    """Load anchor points configuration."""
    path = Path(__file__).parent.parent / "config" / "anchor-points.json"
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    return {}


def check_ordinal_ranking(statuses: dict) -> list:
    """
    Test 1: Ordinal Ranking Consistency

    If Bank A has stronger evidence than Bank B on every dimension,
    then A must rank >= B in classification hierarchy.

    Hierarchy: ARCHITECT-Native > Leader > Follower > PRAGMATIST
    """
    issues = []

    HIERARCHY = {
        'ARCHITECT': {'Native': 4, 'Leader': 3, 'Follower': 2},
        'PRAGMATIST': {'*': 1},
        'OBSERVER': {'*': 0},
        'UNKNOWN': {'*': -1}
    }

    def get_rank(status: dict) -> int:
        classification = status.get('classification', 'UNKNOWN').upper()
        sub = status.get('sub_classification', '*')

        if classification in HIERARCHY:
            variants = HIERARCHY[classification]
            return variants.get(sub, variants.get('*', 0))
        return -1

    # Compare banks with confidence data
    banks_with_data = [
        (bank, s) for bank, s in statuses.items()
        if not s.get('_error') and s.get('confidence', 0) > 0
    ]

    for i, (bank_a, status_a) in enumerate(banks_with_data):
        for bank_b, status_b in banks_with_data[i+1:]:
            rank_a = get_rank(status_a)
            rank_b = get_rank(status_b)
            conf_a = status_a.get('confidence', 0)
            conf_b = status_b.get('confidence', 0)

            # If A has higher confidence but lower rank, flag it
            if conf_a > conf_b + 10 and rank_a < rank_b:
                issues.append({
                    'bank': f"{bank_a} vs {bank_b}",
                    'check': 'ordinal_ranking',
                    'issue': f"{bank_a} has higher confidence ({conf_a}%) but lower rank than {bank_b} ({conf_b}%)"
                })

    return issues


def check_similar_profiles(statuses: dict) -> list:
    """
    Test 2: Similar Profile Cohorts

    Banks with similar business models, regions, and derivatives exposure
    should have similar classifications unless exceptional circumstances.
    """
    issues = []

    try:
        manifest = load_bank_manifest()
        banks_config = {b['id']: b for b in manifest.get('banks', [])}
    except Exception:
        return issues  # Can't run without manifest

    # Group by region
    by_region = {}
    for bank, status in statuses.items():
        if bank in banks_config:
            region = banks_config[bank].get('region', 'Unknown')
            if region not in by_region:
                by_region[region] = []
            by_region[region].append((bank, status))

    # Check for outliers within regions
    for region, banks in by_region.items():
        if len(banks) < 2:
            continue

        classifications = [s.get('classification', 'UNKNOWN') for _, s in banks]
        class_counts = Counter(classifications)

        # If one bank is very different from peers
        majority_class = class_counts.most_common(1)[0][0]
        majority_count = class_counts.most_common(1)[0][1]

        if majority_count >= len(banks) - 1 and len(banks) >= 3:
            # One outlier
            for bank, status in banks:
                if status.get('classification') != majority_class:
                    issues.append({
                        'bank': bank,
                        'check': 'similar_profiles',
                        'issue': f"Outlier in {region}: {bank} is {status.get('classification')} while {majority_count} peers are {majority_class}"
                    })

    return issues


def check_evidence_confidence_correlation(statuses: dict) -> list:
    """
    Test 3: Evidence-Confidence Correlation

    More/higher-tier evidence should correlate with higher confidence.
    Banks with only Tier 3 evidence shouldn't have >50% confidence.
    """
    issues = []

    for bank, status in statuses.items():
        if status.get('_error'):
            continue

        confidence = status.get('confidence', 0)
        classification = status.get('classification', '').upper()

        # ARCHITECT classifications should have higher confidence
        if classification == 'ARCHITECT' and confidence < 60:
            issues.append({
                'bank': bank,
                'check': 'evidence_confidence',
                'issue': f"ARCHITECT classification with only {confidence}% confidence - needs stronger evidence"
            })

        # UNKNOWN shouldn't have high confidence
        if classification == 'UNKNOWN' and confidence > 50:
            issues.append({
                'bank': bank,
                'check': 'evidence_confidence',
                'issue': f"UNKNOWN classification with {confidence}% confidence - contradictory"
            })

    return issues


def check_classification_distribution(statuses: dict) -> list:
    """
    Test 4: Classification Distribution Sanity

    Global distribution should roughly match priors (~30% Architect, ~70% Pragmatist).
    Flag if Architects > 40% or if all banks have same classification.
    """
    issues = []

    valid_statuses = [s for s in statuses.values() if not s.get('_error')]
    if not valid_statuses:
        return issues

    classifications = [s.get('classification', 'UNKNOWN').upper() for s in valid_statuses]
    counts = Counter(classifications)
    total = len(classifications)

    architect_count = counts.get('ARCHITECT', 0)
    architect_pct = architect_count / total

    # Expected: ~30% Architects based on default priors
    if architect_pct > 0.45:
        issues.append({
            'bank': 'GLOBAL',
            'check': 'distribution',
            'issue': f"High ARCHITECT rate: {architect_pct:.0%} ({architect_count}/{total}) - expected ~30%"
        })
    elif architect_pct < 0.10 and total >= 10:
        issues.append({
            'bank': 'GLOBAL',
            'check': 'distribution',
            'issue': f"Low ARCHITECT rate: {architect_pct:.0%} ({architect_count}/{total}) - verify not under-classifying"
        })

    # All same classification is suspicious
    if len(counts) == 1 and total >= 5:
        issues.append({
            'bank': 'GLOBAL',
            'check': 'distribution',
            'issue': f"All {total} banks have same classification: {list(counts.keys())[0]}"
        })

    return issues


def check_anchor_points(statuses: dict) -> list:
    """
    Test 5: Anchor Point Coherence

    No classification can violate immutable facts (e.g., known production banks).
    """
    issues = []

    anchors = load_anchor_points()
    if not anchors:
        return issues

    # Check production banks
    for prod_bank in anchors.get('production_banks', {}).get('banks', []):
        bank_id = prod_bank['id']

        if bank_id in statuses:
            status = statuses[bank_id]
            classification = status.get('classification', '').upper()
            sub = status.get('sub_classification', '')

            if classification != 'ARCHITECT' or sub != 'Native':
                issues.append({
                    'bank': bank_id,
                    'check': 'anchor_point',
                    'issue': f"ANCHOR VIOLATION: {bank_id} is in production (since {prod_bank['date']}) but classified as {classification} {sub}"
                })

    # Check confirmed contributors
    for contrib_bank in anchors.get('confirmed_contributors', {}).get('banks', []):
        bank_id = contrib_bank['id']

        if bank_id in statuses:
            status = statuses[bank_id]
            classification = status.get('classification', '').upper()

            if classification not in ['ARCHITECT']:
                issues.append({
                    'bank': bank_id,
                    'check': 'anchor_point',
                    'issue': f"ANCHOR WARNING: {bank_id} is confirmed contributor but classified as {classification}"
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
            'passed': False,
            'critical': []
        }

    all_issues = []

    # Original checks
    all_issues.extend(check_probability_sanity(statuses))
    all_issues.extend(check_taxonomy(statuses))
    all_issues.extend(check_alignment(statuses))
    all_issues.extend(check_confidence_bounds(statuses))

    # NEW: QA validator checks
    all_issues.extend(check_ordinal_ranking(statuses))
    all_issues.extend(check_similar_profiles(statuses))
    all_issues.extend(check_evidence_confidence_correlation(statuses))
    all_issues.extend(check_classification_distribution(statuses))
    all_issues.extend(check_anchor_points(statuses))

    summary = generate_summary(statuses)

    # Separate critical (anchor violations) from warnings
    critical_issues = [i for i in all_issues if 'ANCHOR VIOLATION' in i.get('issue', '')]

    return {
        'banks': len(statuses),
        'issues': all_issues,
        'critical': critical_issues,
        'passed': len(critical_issues) == 0,  # Fail only on critical issues
        'summary': summary
    }


def main():
    """CLI entry point."""
    # Fix encoding for Windows console
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

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

    # Show critical issues first
    critical = result.get('critical', [])
    if critical:
        print(f"\n[CRITICAL] Anchor Point Violations ({len(critical)}):")
        for issue in critical:
            print(f"  - {issue['bank']}: {issue['issue']}")

    # Show all issues grouped by bank
    if result['issues']:
        non_critical = [i for i in result['issues'] if i not in critical]
        print(f"\nAll Issues ({len(result['issues'])} total, {len(critical)} critical):")

        # Group by bank
        by_bank = defaultdict(list)
        for issue in result['issues']:
            by_bank[issue['bank']].append(issue)

        for bank in sorted(by_bank.keys()):
            print(f"\n  {bank}:")
            for issue in by_bank[bank]:
                prefix = "[CRITICAL] " if issue in critical else ""
                print(f"    {prefix}[{issue['check']}] {issue['issue']}")
    else:
        print("\nNo issues found.")

    print(f"\n{'='*60}")

    # Also output JSON for scripting
    print(f"\n{json.dumps(result, indent=2)}")

    sys.exit(0 if result['passed'] else 1)


if __name__ == "__main__":
    main()
