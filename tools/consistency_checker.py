"""
CDM Research Protocol - Consistency Checker v1.0

Cross-bank consistency analysis using evidence fingerprinting and peer calibration.
Detects when similar evidence profiles yield inconsistent outcomes.

Usage:
    from consistency_checker import ConsistencyChecker

    checker = ConsistencyChecker()

    # Check single bank against patterns
    issues = checker.check_bank_consistency("deutsche-bank", outputs_dir)

    # Check entire phase for consistency
    phase_issues = checker.check_phase_consistency(phase_dir)

    # Generate evidence fingerprint
    fingerprint = checker.generate_fingerprint(evidence_json)
"""

import json
import math
import hashlib
from pathlib import Path
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any, Tuple
from urllib.parse import urlparse
from collections import Counter

# Project imports
import sys
sys.path.insert(0, str(Path(__file__).parent))

try:
    from config_loader import load_calibration_config
except ImportError:
    def load_calibration_config():
        return {}


# --- PATHS ---
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
CONFIG_DIR = PROJECT_ROOT / "config"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"


# --- DATA CLASSES ---

@dataclass
class EvidenceFingerprint:
    """Fingerprint of a bank's evidence profile for comparison."""
    tier1_count: int = 0
    tier2_count: int = 0
    tier3_count: int = 0
    null_results_count: int = 0
    highest_tier: int = 0
    highest_claim_type: Optional[str] = None
    evidence_direction_ratio: float = 0.0
    average_freshness: float = 0.5
    source_diversity: float = 0.0
    vendor_signals_present: bool = False
    production_signals_present: bool = False
    contribution_signals_present: bool = False
    claim_type_vector: List[int] = field(default_factory=lambda: [0, 0, 0, 0, 0, 0])

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'EvidenceFingerprint':
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

    def fingerprint_hash(self) -> str:
        """Generate a hash for quick comparison."""
        content = f"{self.tier1_count}-{self.tier2_count}-{self.tier3_count}-{self.highest_claim_type}"
        return hashlib.md5(content.encode()).hexdigest()[:8]


@dataclass
class ConsistencyIssue:
    """Record of a consistency issue between banks."""
    issue_type: str  # SIMILAR_PROFILE_DIVERGENCE, PEER_OUTLIER, LR_CALIBRATION_DRIFT
    severity: str  # critical, warning, info
    banks_involved: List[str]
    description: str
    fingerprint_similarity: Optional[float] = None
    confidence_gap: Optional[float] = None
    classification_difference: Optional[str] = None
    suggested_action: str = ""
    auto_resolvable: bool = False
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'ConsistencyIssue':
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


# --- MAIN CLASS ---

class ConsistencyChecker:
    """
    Cross-bank consistency analysis.

    Compares evidence profiles across banks to detect inconsistent classifications.
    """

    def __init__(self, config_dir: Path = None, outputs_dir: Path = None):
        """
        Initialize the consistency checker.

        Args:
            config_dir: Path to config directory
            outputs_dir: Path to outputs directory
        """
        self.config_dir = config_dir or CONFIG_DIR
        self.outputs_dir = outputs_dir or OUTPUTS_DIR

        # Load peer cohorts if available
        self.peer_cohorts = self._load_peer_cohorts()
        self.evidence_patterns = self._load_evidence_patterns()

    def _load_peer_cohorts(self) -> Dict:
        """Load peer cohort configuration."""
        path = self.config_dir / "peer-cohorts.json"
        if path.exists():
            return json.loads(path.read_text(encoding='utf-8'))
        return {"cohorts": []}

    def _load_evidence_patterns(self) -> Dict:
        """Load known evidence patterns."""
        path = self.config_dir / "evidence-patterns.json"
        if path.exists():
            return json.loads(path.read_text(encoding='utf-8'))
        return {"patterns": [], "match_threshold": 0.75}

    # --- FINGERPRINT GENERATION ---

    def generate_fingerprint(self, evidence_json: Dict) -> EvidenceFingerprint:
        """
        Generate fingerprint from evidence.json data.

        Args:
            evidence_json: Parsed evidence.json content

        Returns:
            EvidenceFingerprint for the bank
        """
        items = evidence_json.get('evidence_items', [])
        null_results = evidence_json.get('null_results', [])

        # Count by tier
        tier_counts = Counter(item.get('tier', 3) for item in items)

        # Claim type ordering
        claim_type_order = [
            'production_usage', 'pilot_or_poc', 'membership_or_participation',
            'open_source_contribution', 'vendor_proxy_signal', 'hiring_signal'
        ]

        claim_vector = [
            sum(1 for item in items if item.get('claim_type') == ct)
            for ct in claim_type_order
        ]

        # Highest claim type
        highest_claim = None
        for ct in claim_type_order:
            if claim_vector[claim_type_order.index(ct)] > 0:
                highest_claim = ct
                break

        # Direction ratio (what fraction supports ARCHITECT)
        directions = []
        for item in items:
            direction = item.get('direction', 'NEUTRAL')
            if direction == 'SUPPORTS_ARCHITECT':
                directions.append(1)
            elif direction == 'SUPPORTS_PRAGMATIST':
                directions.append(0)
            else:
                directions.append(0.5)

        direction_ratio = sum(directions) / len(directions) if directions else 0.5

        # Freshness analysis
        freshness_scores = []
        for item in items:
            qa = item.get('quality_assessment', {})
            recency = qa.get('recency', 'unknown')
            score = {
                'current': 1.0,
                'recent': 0.8,
                'dated': 0.5,
                'historical': 0.25
            }.get(recency, 0.5)
            freshness_scores.append(score)

        avg_freshness = sum(freshness_scores) / len(freshness_scores) if freshness_scores else 0.5

        # Source diversity
        domains = set()
        for item in items:
            url = item.get('source_url', '')
            if url:
                try:
                    domain = urlparse(url).netloc
                    domains.add(domain)
                except:
                    pass

        source_diversity = len(domains) / max(len(items), 1) if items else 0

        # Signal flags
        vendor_present = claim_vector[4] > 0  # vendor_proxy_signal
        production_present = claim_vector[0] > 0  # production_usage
        contribution_present = claim_vector[3] > 0  # open_source_contribution

        return EvidenceFingerprint(
            tier1_count=tier_counts.get(1, 0),
            tier2_count=tier_counts.get(2, 0),
            tier3_count=tier_counts.get(3, 0),
            null_results_count=len(null_results),
            highest_tier=min(tier_counts.keys()) if tier_counts else 0,
            highest_claim_type=highest_claim,
            evidence_direction_ratio=round(direction_ratio, 2),
            average_freshness=round(avg_freshness, 2),
            source_diversity=round(source_diversity, 2),
            vendor_signals_present=vendor_present,
            production_signals_present=production_present,
            contribution_signals_present=contribution_present,
            claim_type_vector=claim_vector
        )

    # --- FINGERPRINT COMPARISON ---

    def calculate_fingerprint_similarity(
        self,
        fp1: EvidenceFingerprint,
        fp2: EvidenceFingerprint
    ) -> float:
        """
        Calculate similarity between two evidence fingerprints.

        Uses weighted comparison across dimensions:
        - claim_type_vector: 0.25 (cosine similarity)
        - tier_distribution: 0.20 (normalized difference)
        - boolean_flags: 0.20 (exact match)
        - direction_ratio: 0.15 (absolute difference)
        - freshness/diversity: 0.20 (absolute difference)

        Args:
            fp1: First fingerprint
            fp2: Second fingerprint

        Returns:
            Similarity score 0.0 to 1.0
        """
        weights = {
            'claim_type_vector': 0.25,
            'tier_distribution': 0.20,
            'boolean_flags': 0.20,
            'direction_ratio': 0.15,
            'freshness_diversity': 0.20
        }

        # Claim type vector cosine similarity
        v1 = fp1.claim_type_vector
        v2 = fp2.claim_type_vector
        dot_product = sum(a * b for a, b in zip(v1, v2))
        mag1 = math.sqrt(sum(a**2 for a in v1))
        mag2 = math.sqrt(sum(a**2 for a in v2))
        if mag1 > 0 and mag2 > 0:
            claim_sim = dot_product / (mag1 * mag2)
        else:
            claim_sim = 1.0 if mag1 == mag2 == 0 else 0.0

        # Tier distribution similarity
        tier_diff = (
            abs(fp1.tier1_count - fp2.tier1_count) +
            abs(fp1.tier2_count - fp2.tier2_count) +
            abs(fp1.tier3_count - fp2.tier3_count)
        )
        max_tier = max(
            fp1.tier1_count + fp1.tier2_count + fp1.tier3_count,
            fp2.tier1_count + fp2.tier2_count + fp2.tier3_count,
            1
        )
        tier_sim = 1 - (tier_diff / (2 * max_tier))

        # Boolean flags
        bool_matches = [
            fp1.vendor_signals_present == fp2.vendor_signals_present,
            fp1.production_signals_present == fp2.production_signals_present,
            fp1.contribution_signals_present == fp2.contribution_signals_present
        ]
        bool_sim = sum(bool_matches) / len(bool_matches)

        # Direction ratio similarity
        direction_sim = 1 - abs(fp1.evidence_direction_ratio - fp2.evidence_direction_ratio)

        # Freshness and diversity similarity
        freshness_sim = 1 - abs(fp1.average_freshness - fp2.average_freshness)
        diversity_sim = 1 - abs(fp1.source_diversity - fp2.source_diversity)
        fresh_div_sim = (freshness_sim + diversity_sim) / 2

        # Weighted sum
        total_sim = (
            weights['claim_type_vector'] * claim_sim +
            weights['tier_distribution'] * tier_sim +
            weights['boolean_flags'] * bool_sim +
            weights['direction_ratio'] * direction_sim +
            weights['freshness_diversity'] * fresh_div_sim
        )

        return round(total_sim, 3)

    # --- CONSISTENCY CHECKING ---

    def check_bank_consistency(
        self,
        bank_id: str,
        phase_dir: Path
    ) -> List[ConsistencyIssue]:
        """
        Check a bank's consistency against other banks in the phase.

        Args:
            bank_id: Bank identifier
            phase_dir: Path to phase directory

        Returns:
            List of consistency issues found
        """
        issues = []

        # Load target bank's data
        bank_dir = phase_dir / bank_id
        if not bank_dir.exists():
            return issues

        target_data = self._load_bank_data(bank_dir)
        if not target_data:
            return issues

        target_fp = target_data.get('fingerprint')
        target_conf = target_data.get('confidence', 0)
        target_class = target_data.get('classification', 'UNKNOWN')

        # Compare with other banks
        for other_dir in phase_dir.iterdir():
            if not other_dir.is_dir() or other_dir.name == bank_id:
                continue

            other_data = self._load_bank_data(other_dir)
            if not other_data:
                continue

            other_fp = other_data.get('fingerprint')
            other_conf = other_data.get('confidence', 0)
            other_class = other_data.get('classification', 'UNKNOWN')

            # Calculate similarity
            similarity = self.calculate_fingerprint_similarity(target_fp, other_fp)
            threshold = self.evidence_patterns.get('match_threshold', 0.75)

            # Check for divergence
            if similarity >= threshold:
                conf_gap = abs(target_conf - other_conf)
                class_diff = target_class != other_class

                if class_diff:
                    issues.append(ConsistencyIssue(
                        issue_type="SIMILAR_PROFILE_CLASSIFICATION_DIVERGENCE",
                        severity="critical",
                        banks_involved=[bank_id, other_dir.name],
                        description=f"Similar evidence profiles ({similarity:.0%}) but different classifications: {target_class} vs {other_class}",
                        fingerprint_similarity=similarity,
                        classification_difference=f"{target_class} vs {other_class}",
                        suggested_action="Review classification criteria for consistency"
                    ))
                elif conf_gap > 15:
                    issues.append(ConsistencyIssue(
                        issue_type="SIMILAR_PROFILE_CONFIDENCE_DIVERGENCE",
                        severity="warning",
                        banks_involved=[bank_id, other_dir.name],
                        description=f"Similar evidence profiles ({similarity:.0%}) but confidence gap of {conf_gap:.0f}%",
                        fingerprint_similarity=similarity,
                        confidence_gap=conf_gap,
                        suggested_action="Review confidence calibration for consistency"
                    ))

        # Check peer cohort consistency
        issues.extend(self._check_peer_cohort(bank_id, target_data, phase_dir))

        return issues

    def _check_peer_cohort(
        self,
        bank_id: str,
        bank_data: Dict,
        phase_dir: Path
    ) -> List[ConsistencyIssue]:
        """Check if bank is consistent with its peer cohort."""
        issues = []

        # Find cohort for this bank
        cohort = None
        for c in self.peer_cohorts.get('cohorts', []):
            if bank_id in c.get('members', []):
                cohort = c
                break

        if not cohort:
            return issues

        # Get data for all cohort members
        cohort_data = []
        for member_id in cohort.get('members', []):
            if member_id == bank_id:
                continue
            member_dir = phase_dir / member_id
            if member_dir.exists():
                data = self._load_bank_data(member_dir)
                if data:
                    cohort_data.append(data)

        if len(cohort_data) < 2:
            return issues

        # Calculate cohort statistics
        cohort_confidences = [d.get('confidence', 50) for d in cohort_data]
        cohort_classifications = Counter(d.get('classification', 'UNKNOWN') for d in cohort_data)

        bank_conf = bank_data.get('confidence', 50)
        bank_class = bank_data.get('classification', 'UNKNOWN')

        # Check for outlier
        import statistics
        if len(cohort_confidences) >= 2:
            mean_conf = statistics.mean(cohort_confidences)
            std_conf = statistics.stdev(cohort_confidences) if len(cohort_confidences) > 1 else 0

            if std_conf > 0 and abs(bank_conf - mean_conf) > 2 * std_conf:
                issues.append(ConsistencyIssue(
                    issue_type="PEER_OUTLIER_CONFIDENCE",
                    severity="warning",
                    banks_involved=[bank_id] + cohort.get('members', []),
                    description=f"Bank confidence ({bank_conf}%) is outlier in {cohort.get('name', 'peer cohort')} (mean: {mean_conf:.0f}%, std: {std_conf:.0f}%)",
                    confidence_gap=abs(bank_conf - mean_conf),
                    suggested_action="Verify if different confidence is justified"
                ))

        # Check classification against cohort majority
        most_common = cohort_classifications.most_common(1)
        if most_common:
            common_class, common_count = most_common[0]
            if bank_class != common_class and common_count >= len(cohort_data) * 0.6:
                issues.append(ConsistencyIssue(
                    issue_type="PEER_OUTLIER_CLASSIFICATION",
                    severity="warning",
                    banks_involved=[bank_id] + cohort.get('members', []),
                    description=f"Bank classified as {bank_class} while {common_count}/{len(cohort_data)} peers are {common_class}",
                    classification_difference=f"{bank_class} vs cohort {common_class}",
                    suggested_action="Verify if different classification is justified by evidence"
                ))

        return issues

    def _load_bank_data(self, bank_dir: Path) -> Optional[Dict]:
        """Load bank's evidence and status data."""
        evidence_path = bank_dir / "evidence.json"
        status_path = bank_dir / "status.json"

        if not evidence_path.exists():
            return None

        try:
            evidence_json = json.loads(evidence_path.read_text(encoding='utf-8'))
            fingerprint = self.generate_fingerprint(evidence_json)

            status = {}
            if status_path.exists():
                status = json.loads(status_path.read_text(encoding='utf-8'))

            return {
                'bank_id': bank_dir.name,
                'fingerprint': fingerprint,
                'confidence': status.get('confidence', 0),
                'classification': status.get('classification', 'UNKNOWN'),
                'probability': status.get('current_probability', 0.5)
            }
        except Exception as e:
            return None

    def check_phase_consistency(self, phase_dir: Path) -> List[ConsistencyIssue]:
        """
        Check consistency across all banks in a phase.

        Args:
            phase_dir: Path to phase directory

        Returns:
            All consistency issues found
        """
        all_issues = []

        for bank_dir in phase_dir.iterdir():
            if bank_dir.is_dir():
                issues = self.check_bank_consistency(bank_dir.name, phase_dir)
                all_issues.extend(issues)

        # Deduplicate issues involving same bank pairs
        seen = set()
        unique_issues = []
        for issue in all_issues:
            key = tuple(sorted(issue.banks_involved)) + (issue.issue_type,)
            if key not in seen:
                seen.add(key)
                unique_issues.append(issue)

        return unique_issues

    def generate_consistency_report(self, phase_dir: Path) -> str:
        """
        Generate markdown consistency report for a phase.

        Args:
            phase_dir: Path to phase directory

        Returns:
            Markdown report
        """
        issues = self.check_phase_consistency(phase_dir)

        lines = [
            f"# Cross-Bank Consistency Report",
            f"",
            f"**Phase**: {phase_dir.name}",
            f"**Generated**: {datetime.now(timezone.utc).isoformat()}",
            f"",
            f"## Summary",
            f"",
            f"- Total issues: {len(issues)}",
            f"- Critical: {sum(1 for i in issues if i.severity == 'critical')}",
            f"- Warning: {sum(1 for i in issues if i.severity == 'warning')}",
            f"- Info: {sum(1 for i in issues if i.severity == 'info')}",
            f""
        ]

        if issues:
            lines.append("## Issues")
            lines.append("")

            for issue in issues:
                severity_icon = {"critical": "🔴", "warning": "🟡", "info": "🔵"}.get(issue.severity, "⚪")
                lines.append(f"### {severity_icon} {issue.issue_type}")
                lines.append(f"")
                lines.append(f"**Banks**: {', '.join(issue.banks_involved)}")
                lines.append(f"")
                lines.append(f"{issue.description}")
                lines.append(f"")
                if issue.fingerprint_similarity:
                    lines.append(f"- Similarity: {issue.fingerprint_similarity:.0%}")
                if issue.confidence_gap:
                    lines.append(f"- Confidence gap: {issue.confidence_gap:.0f}%")
                if issue.classification_difference:
                    lines.append(f"- Classification: {issue.classification_difference}")
                lines.append(f"- Suggested action: {issue.suggested_action}")
                lines.append(f"")
        else:
            lines.append("## No Issues Found")
            lines.append("")
            lines.append("All banks in this phase have consistent evidence profiles and classifications.")

        return "\n".join(lines)


# --- CLI INTERFACE ---

def main():
    """CLI interface for consistency checker."""
    import argparse

    parser = argparse.ArgumentParser(description="CDM Research Protocol - Consistency Checker")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Check bank command
    bank_parser = subparsers.add_parser("check-bank", help="Check single bank consistency")
    bank_parser.add_argument("bank_id", help="Bank identifier")
    bank_parser.add_argument("phase_dir", type=Path, help="Path to phase directory")

    # Check phase command
    phase_parser = subparsers.add_parser("check-phase", help="Check entire phase consistency")
    phase_parser.add_argument("phase_dir", type=Path, help="Path to phase directory")

    # Report command
    report_parser = subparsers.add_parser("report", help="Generate consistency report")
    report_parser.add_argument("phase_dir", type=Path, help="Path to phase directory")
    report_parser.add_argument("--output", help="Output file path")

    # Fingerprint command
    fp_parser = subparsers.add_parser("fingerprint", help="Generate evidence fingerprint")
    fp_parser.add_argument("evidence_json", type=Path, help="Path to evidence.json")

    args = parser.parse_args()

    checker = ConsistencyChecker()

    if args.command == "check-bank":
        issues = checker.check_bank_consistency(args.bank_id, args.phase_dir)
        if issues:
            print(f"Found {len(issues)} issue(s):")
            for issue in issues:
                print(f"  [{issue.severity.upper()}] {issue.issue_type}")
                print(f"         {issue.description}")
        else:
            print("No consistency issues found.")

    elif args.command == "check-phase":
        issues = checker.check_phase_consistency(args.phase_dir)
        if issues:
            print(f"Found {len(issues)} issue(s) across phase:")
            for issue in issues:
                print(f"  [{issue.severity.upper()}] {issue.issue_type}")
                print(f"         Banks: {', '.join(issue.banks_involved)}")
                print(f"         {issue.description}")
        else:
            print("No consistency issues found in phase.")

    elif args.command == "report":
        report = checker.generate_consistency_report(args.phase_dir)
        if args.output:
            Path(args.output).write_text(report)
            print(f"Report saved to {args.output}")
        else:
            print(report)

    elif args.command == "fingerprint":
        evidence = json.loads(args.evidence_json.read_text(encoding='utf-8'))
        fp = checker.generate_fingerprint(evidence)
        print(json.dumps(fp.to_dict(), indent=2))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
