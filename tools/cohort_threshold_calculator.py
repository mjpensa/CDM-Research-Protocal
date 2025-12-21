#!/usr/bin/env python3
"""
Cohort Threshold Calculator

Calculates network adoption thresholds and peer pressure metrics.
When ~40% of a peer cohort adopts CDM (tipping point), remaining banks
face intense pressure to follow.

Usage:
    python cohort_threshold_calculator.py --cohort eu-tier1 --phase 1
    python cohort_threshold_calculator.py --bank deutsche-bank --peer-pressure
    python cohort_threshold_calculator.py --all-cohorts --output adoption-report.json
"""

import argparse
import json
import logging
import sys
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
CONFIG_DIR = PROJECT_ROOT / "config"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

# Import config loader
sys.path.insert(0, str(SCRIPT_DIR))
from config_loader import load_bank_manifest, get_bank_config


def load_peer_cohorts() -> dict:
    """Load peer cohorts configuration."""
    path = CONFIG_DIR / "peer-cohorts.json"
    if not path.exists():
        return {"cohorts": [], "network_adoption_thresholds": {}}
    return json.loads(path.read_text(encoding='utf-8'))


@dataclass
class CohortAdoptionMetrics:
    """Adoption metrics for a cohort."""
    cohort_id: str
    cohort_name: str
    total_members: int
    architect_count: int
    pragmatist_count: int
    unknown_count: int
    adoption_rate: float
    threshold_distance: float  # Distance from tipping point
    pressure_intensity: str  # LOW, MEDIUM, HIGH, CRITICAL
    pressure_adjustment: float
    members: List[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class PeerPressureMetrics:
    """Peer pressure metrics for a specific bank."""
    bank_id: str
    bank_name: str
    cohorts: List[str]
    peer_architects: List[str]
    peer_pragmatists: List[str]
    total_peers: int
    architect_peer_rate: float
    estimated_pressure: float
    pressure_intensity: str
    recommended_classification_adjustment: float
    contributing_factors: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


class CohortThresholdCalculator:
    """Calculator for network adoption thresholds and peer pressure."""

    def __init__(self):
        self.cohorts_config = load_peer_cohorts()
        self.bank_manifest = load_bank_manifest()
        self.thresholds = self.cohorts_config.get('network_adoption_thresholds', {})

    def get_bank_classification(self, bank_id: str, phase: Optional[int] = None) -> Optional[str]:
        """
        Get the current classification for a bank from its evidence.json.

        Returns: 'ARCHITECT', 'PRAGMATIST', 'OBSERVER', 'UNKNOWN', or None
        """
        # Try to find the bank's output directory
        if phase:
            phase_dirs = [f"phase-{phase}-*"]
        else:
            phase_dirs = ["phase-*"]

        for phase_pattern in phase_dirs:
            for phase_dir in OUTPUTS_DIR.glob(phase_pattern):
                bank_dir = phase_dir / bank_id
                evidence_file = bank_dir / "evidence.json"
                if evidence_file.exists():
                    try:
                        evidence = json.loads(evidence_file.read_text(encoding='utf-8'))
                        # Check for synthesis_result
                        synthesis = evidence.get('synthesis_result', {})
                        classification = synthesis.get('classification')
                        if classification:
                            return classification

                        # Fallback: infer from evidence
                        items = evidence.get('evidence', [])
                        has_production = any(
                            item.get('claim_type') == 'production_usage'
                            for item in items
                        )
                        has_pilot = any(
                            item.get('claim_type') == 'pilot_or_poc'
                            for item in items
                        )
                        has_contribution = any(
                            item.get('claim_type') == 'open_source_contribution'
                            for item in items
                        )

                        if has_production:
                            return 'ARCHITECT'
                        elif has_pilot or has_contribution:
                            return 'PRAGMATIST'
                        elif items:
                            return 'OBSERVER'
                        else:
                            return 'UNKNOWN'
                    except (json.JSONDecodeError, KeyError):
                        pass

        # Check bank manifest for known classification
        bank_config = get_bank_config(bank_id)
        if bank_config:
            return bank_config.get('expected_classification', 'UNKNOWN')

        return 'UNKNOWN'

    def get_pressure_intensity(self, adoption_rate: float) -> tuple[str, float]:
        """
        Determine pressure intensity level based on adoption rate.

        Returns: (intensity_level, pressure_adjustment)
        """
        levels = self.thresholds.get('pressure_intensity_levels', {})

        for level_name, level_config in levels.items():
            range_vals = level_config.get('range', [0, 1])
            if range_vals[0] <= adoption_rate < range_vals[1]:
                return level_name, level_config.get('pressure_adjustment', 0.0)

        return 'LOW', 0.0

    def calculate_cohort_adoption(
        self,
        cohort_id: str,
        phase: Optional[int] = None
    ) -> Optional[CohortAdoptionMetrics]:
        """Calculate adoption metrics for a specific cohort."""
        # Find cohort
        cohort = None
        for c in self.cohorts_config.get('cohorts', []):
            if c.get('cohort_id') == cohort_id:
                cohort = c
                break

        if not cohort:
            logger.warning(f"Cohort not found: {cohort_id}")
            return None

        members = cohort.get('members', [])
        total_members = len(members)

        if total_members == 0:
            return None

        # Get classifications for all members
        architect_count = 0
        pragmatist_count = 0
        unknown_count = 0
        member_details = []

        for member_id in members:
            classification = self.get_bank_classification(member_id, phase)
            bank_config = get_bank_config(member_id)
            bank_name = bank_config.get('bank_name', member_id) if bank_config else member_id

            member_details.append({
                'bank_id': member_id,
                'bank_name': bank_name,
                'classification': classification
            })

            if classification == 'ARCHITECT':
                architect_count += 1
            elif classification in ['PRAGMATIST', 'OBSERVER']:
                pragmatist_count += 1
            else:
                unknown_count += 1

        # Calculate adoption rate (ARCHITECT / total)
        adoption_rate = architect_count / total_members

        # Calculate distance from tipping point
        tipping_point = self.thresholds.get('tipping_point', {}).get('threshold', 0.40)
        threshold_distance = tipping_point - adoption_rate

        # Determine pressure intensity
        pressure_intensity, pressure_adjustment = self.get_pressure_intensity(adoption_rate)

        return CohortAdoptionMetrics(
            cohort_id=cohort_id,
            cohort_name=cohort.get('name', cohort_id),
            total_members=total_members,
            architect_count=architect_count,
            pragmatist_count=pragmatist_count,
            unknown_count=unknown_count,
            adoption_rate=adoption_rate,
            threshold_distance=threshold_distance,
            pressure_intensity=pressure_intensity,
            pressure_adjustment=pressure_adjustment,
            members=member_details
        )

    def calculate_peer_pressure(
        self,
        bank_id: str,
        phase: Optional[int] = None
    ) -> PeerPressureMetrics:
        """Calculate peer pressure metrics for a specific bank."""
        # Find all cohorts this bank belongs to
        bank_cohorts = []
        all_peers = set()
        peer_architects = set()
        peer_pragmatists = set()

        for cohort in self.cohorts_config.get('cohorts', []):
            members = cohort.get('members', [])
            if bank_id in members:
                bank_cohorts.append(cohort.get('cohort_id'))
                # Add peers (excluding the bank itself)
                for member in members:
                    if member != bank_id:
                        all_peers.add(member)
                        classification = self.get_bank_classification(member, phase)
                        if classification == 'ARCHITECT':
                            peer_architects.add(member)
                        elif classification in ['PRAGMATIST', 'OBSERVER']:
                            peer_pragmatists.add(member)

        total_peers = len(all_peers)
        architect_peer_rate = len(peer_architects) / total_peers if total_peers > 0 else 0.0

        # Calculate pressure based on architect peer rate
        pressure_intensity, base_adjustment = self.get_pressure_intensity(architect_peer_rate)

        # Calculate contributing factors
        contributing_factors = []
        estimated_pressure = 0.0

        if architect_peer_rate > 0:
            contributing_factors.append(
                f"{len(peer_architects)} peer(s) classified as ARCHITECT"
            )
            estimated_pressure += base_adjustment

        # Check if above tipping point
        tipping_point = self.thresholds.get('tipping_point', {}).get('threshold', 0.40)
        if architect_peer_rate >= tipping_point:
            tipping_multiplier = self.thresholds.get('tipping_point', {}).get('pressure_multiplier', 1.5)
            contributing_factors.append(
                f"Peer adoption rate ({architect_peer_rate:.0%}) above tipping point ({tipping_point:.0%})"
            )
            estimated_pressure *= tipping_multiplier

        # Check if above critical mass
        critical_mass = self.thresholds.get('critical_mass', {}).get('threshold', 0.60)
        if architect_peer_rate >= critical_mass:
            critical_multiplier = self.thresholds.get('critical_mass', {}).get('pressure_multiplier', 2.0)
            contributing_factors.append(
                f"Peer adoption rate ({architect_peer_rate:.0%}) above critical mass ({critical_mass:.0%})"
            )
            estimated_pressure *= critical_multiplier / 1.5  # Avoid double-counting

        # Classification adjustment recommendation
        if estimated_pressure >= 0.3:
            recommended_adjustment = 0.15  # Strong upward adjustment
        elif estimated_pressure >= 0.15:
            recommended_adjustment = 0.10  # Moderate adjustment
        elif estimated_pressure >= 0.05:
            recommended_adjustment = 0.05  # Slight adjustment
        else:
            recommended_adjustment = 0.0

        bank_config = get_bank_config(bank_id)
        bank_name = bank_config.get('bank_name', bank_id) if bank_config else bank_id

        return PeerPressureMetrics(
            bank_id=bank_id,
            bank_name=bank_name,
            cohorts=bank_cohorts,
            peer_architects=list(peer_architects),
            peer_pragmatists=list(peer_pragmatists),
            total_peers=total_peers,
            architect_peer_rate=architect_peer_rate,
            estimated_pressure=min(estimated_pressure, 1.0),
            pressure_intensity=pressure_intensity,
            recommended_classification_adjustment=recommended_adjustment,
            contributing_factors=contributing_factors
        )

    def generate_adoption_report(
        self,
        phase: Optional[int] = None
    ) -> dict:
        """Generate comprehensive adoption report for all cohorts."""
        cohort_reports = []

        for cohort in self.cohorts_config.get('cohorts', []):
            cohort_id = cohort.get('cohort_id')
            metrics = self.calculate_cohort_adoption(cohort_id, phase)
            if metrics:
                cohort_reports.append(metrics.to_dict())

        return {
            'generated_at': datetime.now(timezone.utc).isoformat(),
            'phase': phase,
            'cohort_count': len(cohort_reports),
            'thresholds': {
                'tipping_point': self.thresholds.get('tipping_point', {}).get('threshold', 0.40),
                'critical_mass': self.thresholds.get('critical_mass', {}).get('threshold', 0.60)
            },
            'cohorts': cohort_reports
        }


def format_cohort_report(metrics: CohortAdoptionMetrics) -> str:
    """Format cohort metrics as human-readable text."""
    lines = []
    lines.append(f"\n{'='*60}")
    lines.append(f"Cohort: {metrics.cohort_name}")
    lines.append(f"{'='*60}")
    lines.append(f"Total Members: {metrics.total_members}")
    lines.append(f"  - ARCHITECT: {metrics.architect_count}")
    lines.append(f"  - PRAGMATIST/OBSERVER: {metrics.pragmatist_count}")
    lines.append(f"  - UNKNOWN: {metrics.unknown_count}")
    lines.append(f"\nAdoption Rate: {metrics.adoption_rate:.1%}")
    lines.append(f"Pressure Intensity: {metrics.pressure_intensity}")
    lines.append(f"Pressure Adjustment: {metrics.pressure_adjustment:+.2f}")

    if metrics.threshold_distance > 0:
        lines.append(f"\nDistance to Tipping Point: {metrics.threshold_distance:.1%}")
    else:
        lines.append(f"\nABOVE Tipping Point by: {abs(metrics.threshold_distance):.1%}")

    lines.append("\nMembers:")
    for member in metrics.members:
        status = "✓" if member['classification'] == 'ARCHITECT' else "○"
        lines.append(f"  {status} {member['bank_name']}: {member['classification']}")

    return "\n".join(lines)


def format_pressure_report(metrics: PeerPressureMetrics) -> str:
    """Format peer pressure metrics as human-readable text."""
    lines = []
    lines.append(f"\n{'='*60}")
    lines.append(f"Peer Pressure Analysis: {metrics.bank_name}")
    lines.append(f"{'='*60}")
    lines.append(f"Cohorts: {', '.join(metrics.cohorts) or 'None'}")
    lines.append(f"Total Peers: {metrics.total_peers}")
    lines.append(f"  - ARCHITECT peers: {len(metrics.peer_architects)}")
    lines.append(f"  - PRAGMATIST peers: {len(metrics.peer_pragmatists)}")
    lines.append(f"\nPeer Adoption Rate: {metrics.architect_peer_rate:.1%}")
    lines.append(f"Pressure Intensity: {metrics.pressure_intensity}")
    lines.append(f"Estimated Pressure: {metrics.estimated_pressure:.2f}")
    lines.append(f"Recommended Adjustment: {metrics.recommended_classification_adjustment:+.2f}")

    if metrics.contributing_factors:
        lines.append("\nContributing Factors:")
        for factor in metrics.contributing_factors:
            lines.append(f"  • {factor}")

    if metrics.peer_architects:
        lines.append("\nARCHITECT Peers:")
        for peer in metrics.peer_architects:
            lines.append(f"  ✓ {peer}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Calculate network adoption thresholds and peer pressure',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --cohort eu-tier1
  %(prog)s --cohort eu-tier1 --phase 1
  %(prog)s --bank deutsche-bank --peer-pressure
  %(prog)s --all-cohorts --output adoption-report.json
        """
    )

    # Scope options
    parser.add_argument('--cohort', metavar='COHORT_ID',
                       help='Analyze specific cohort')
    parser.add_argument('--bank', metavar='BANK_ID',
                       help='Calculate peer pressure for specific bank')
    parser.add_argument('--all-cohorts', action='store_true',
                       help='Generate report for all cohorts')
    parser.add_argument('--phase', type=int, metavar='N',
                       help='Phase number for evidence lookup')

    # Analysis options
    parser.add_argument('--peer-pressure', action='store_true',
                       help='Calculate peer pressure (requires --bank)')

    # Output options
    parser.add_argument('--output', metavar='FILE',
                       help='Output file path')
    parser.add_argument('--json', action='store_true',
                       help='Output in JSON format')

    args = parser.parse_args()

    # Validate arguments
    if not any([args.cohort, args.bank, args.all_cohorts]):
        parser.print_help()
        sys.exit(1)

    if args.peer_pressure and not args.bank:
        print("Error: --peer-pressure requires --bank")
        sys.exit(1)

    calculator = CohortThresholdCalculator()

    # Calculate peer pressure for specific bank
    if args.bank and args.peer_pressure:
        metrics = calculator.calculate_peer_pressure(args.bank, args.phase)

        if args.json:
            print(json.dumps(metrics.to_dict(), indent=2))
        else:
            print(format_pressure_report(metrics))
        return

    # Analyze specific cohort
    if args.cohort:
        metrics = calculator.calculate_cohort_adoption(args.cohort, args.phase)

        if not metrics:
            print(f"Error: Cohort '{args.cohort}' not found")
            sys.exit(1)

        if args.json:
            print(json.dumps(metrics.to_dict(), indent=2))
        else:
            print(format_cohort_report(metrics))
        return

    # Generate full report for all cohorts
    if args.all_cohorts:
        report = calculator.generate_adoption_report(args.phase)

        if args.output:
            output_path = Path(args.output)
            output_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
            print(f"Report saved to: {args.output}")
        elif args.json:
            print(json.dumps(report, indent=2))
        else:
            print(f"\nNetwork Adoption Report")
            print(f"Generated: {report['generated_at']}")
            print(f"Phase: {report['phase'] or 'All'}")
            print(f"Cohorts analyzed: {report['cohort_count']}")
            print(f"\nThresholds:")
            print(f"  Tipping Point: {report['thresholds']['tipping_point']:.0%}")
            print(f"  Critical Mass: {report['thresholds']['critical_mass']:.0%}")

            for cohort_data in report['cohorts']:
                metrics = CohortAdoptionMetrics(**cohort_data)
                print(format_cohort_report(metrics))


if __name__ == '__main__':
    main()
