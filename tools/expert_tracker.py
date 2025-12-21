#!/usr/bin/env python3
"""
Expert Tracker Tool

Tracks CDM experts and their movements between organizations.
An architect-level expert joining a bank is a strong ARCHITECT signal.

Usage:
    python expert_tracker.py --bank jpmorgan --show-experts
    python expert_tracker.py --expert EXPERT-001 --show-history
    python expert_tracker.py --track-movement
    python expert_tracker.py --all-experts --output experts-report.json
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
KB_DIR = PROJECT_ROOT / "knowledge_base"

# Import config loader
sys.path.insert(0, str(SCRIPT_DIR))
from config_loader import get_bank_config


def load_expert_registry() -> dict:
    """Load CDM experts registry."""
    path = KB_DIR / "cdm_experts.json"
    if not path.exists():
        return {"experts": [], "expertise_levels": {}, "movement_signals": {}}
    return json.loads(path.read_text(encoding='utf-8'))


@dataclass
class ExpertPresence:
    """Represents expert presence at an organization."""
    expert_id: str
    expert_name: str
    expertise_level: str
    organization_id: str
    organization_name: str
    role: str
    status: str
    lr_impact: float

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class BankExpertMetrics:
    """Metrics for experts at a bank."""
    bank_id: str
    bank_name: str
    total_experts: int
    architect_count: int
    contributor_count: int
    practitioner_count: int
    expertise_score: float
    experts: List[ExpertPresence] = field(default_factory=list)
    recommended_lr_adjustment: float = 1.0

    def to_dict(self) -> dict:
        result = asdict(self)
        result['experts'] = [e.to_dict() for e in self.experts]
        return result


@dataclass
class ExpertMovement:
    """Represents an expert movement event."""
    expert_id: str
    expert_name: str
    expertise_level: str
    from_org: Optional[str]
    to_org: Optional[str]
    movement_type: str  # 'join', 'leave', 'transfer'
    signal_type: str
    lr_multiplier: float
    detected_date: str

    def to_dict(self) -> dict:
        return asdict(self)


class ExpertTracker:
    """Tracks CDM experts and their organizational movements."""

    def __init__(self):
        self.registry = load_expert_registry()
        self.experts = self.registry.get('experts', [])
        self.expertise_levels = self.registry.get('expertise_levels', {})
        self.movement_signals = self.registry.get('movement_signals', {})

    def get_expert_by_id(self, expert_id: str) -> Optional[dict]:
        """Get expert by ID."""
        for expert in self.experts:
            if expert.get('id') == expert_id:
                return expert
        return None

    def get_expert_by_name(self, name: str) -> Optional[dict]:
        """Get expert by name (case-insensitive partial match)."""
        name_lower = name.lower()
        for expert in self.experts:
            if name_lower in expert.get('name', '').lower():
                return expert
        return None

    def get_bank_experts(self, bank_id: str) -> BankExpertMetrics:
        """Get all experts currently at a bank."""
        bank_config = get_bank_config(bank_id)
        bank_name = bank_config.get('bank_name', bank_id) if bank_config else bank_id

        current_experts = []
        architect_count = 0
        contributor_count = 0
        practitioner_count = 0

        for expert in self.experts:
            for affiliation in expert.get('known_affiliations', []):
                if (affiliation.get('organization_id') == bank_id and
                    affiliation.get('status') == 'current'):

                    expertise_level = expert.get('expertise_level', 'practitioner')
                    level_config = self.expertise_levels.get(expertise_level, {})
                    lr_impact = level_config.get('lr_multiplier_joining', 1.0)

                    presence = ExpertPresence(
                        expert_id=expert.get('id'),
                        expert_name=expert.get('name'),
                        expertise_level=expertise_level,
                        organization_id=bank_id,
                        organization_name=affiliation.get('organization_name', bank_name),
                        role=affiliation.get('role', 'Unknown'),
                        status='current',
                        lr_impact=lr_impact
                    )
                    current_experts.append(presence)

                    if expertise_level == 'architect':
                        architect_count += 1
                    elif expertise_level == 'contributor':
                        contributor_count += 1
                    elif expertise_level == 'practitioner':
                        practitioner_count += 1

        # Calculate expertise score
        expertise_score = (
            architect_count * 3.0 +
            contributor_count * 2.0 +
            practitioner_count * 1.0
        )

        # Calculate recommended LR adjustment
        if len(current_experts) >= 3:
            # Multiple experts = strong signal
            recommended_adjustment = self.movement_signals.get(
                'multiple_experts_same_bank', {}
            ).get('lr_multiplier', 2.5)
        elif architect_count >= 1:
            recommended_adjustment = self.expertise_levels.get(
                'architect', {}
            ).get('lr_multiplier_joining', 2.0)
        elif contributor_count >= 1:
            recommended_adjustment = self.expertise_levels.get(
                'contributor', {}
            ).get('lr_multiplier_joining', 1.5)
        elif practitioner_count >= 1:
            recommended_adjustment = self.expertise_levels.get(
                'practitioner', {}
            ).get('lr_multiplier_joining', 1.3)
        else:
            recommended_adjustment = 1.0

        return BankExpertMetrics(
            bank_id=bank_id,
            bank_name=bank_name,
            total_experts=len(current_experts),
            architect_count=architect_count,
            contributor_count=contributor_count,
            practitioner_count=practitioner_count,
            expertise_score=expertise_score,
            experts=current_experts,
            recommended_lr_adjustment=recommended_adjustment
        )

    def get_expert_history(self, expert_id: str) -> Optional[dict]:
        """Get complete history for an expert."""
        expert = self.get_expert_by_id(expert_id)
        if not expert:
            return None

        affiliations = expert.get('known_affiliations', [])
        level_config = self.expertise_levels.get(
            expert.get('expertise_level', 'practitioner'), {}
        )

        return {
            'expert_id': expert.get('id'),
            'name': expert.get('name'),
            'expertise_level': expert.get('expertise_level'),
            'expertise_areas': expert.get('expertise_areas', []),
            'lr_multiplier_joining': level_config.get('lr_multiplier_joining', 1.0),
            'lr_multiplier_leaving': level_config.get('lr_multiplier_leaving', 1.0),
            'affiliations': affiliations,
            'public_contributions': expert.get('public_contributions', []),
            'notes': expert.get('notes')
        }

    def detect_recent_movements(self, months: int = 12) -> List[ExpertMovement]:
        """Detect expert movements in the past N months."""
        movements = []
        cutoff_date = datetime.now(timezone.utc)

        for expert in self.experts:
            affiliations = expert.get('known_affiliations', [])
            expertise_level = expert.get('expertise_level', 'practitioner')

            for i, aff in enumerate(affiliations):
                start_date_str = aff.get('start_date')
                if start_date_str:
                    try:
                        start_date = datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
                        months_ago = (cutoff_date - start_date).days / 30.44

                        if months_ago <= months:
                            # This is a recent join
                            from_org = None
                            if i > 0:
                                from_org = affiliations[i-1].get('organization_name')

                            signal_key = f"{expertise_level}_joins_bank"
                            signal = self.movement_signals.get(
                                signal_key,
                                {'signal_type': 'moderate_architect', 'lr_multiplier': 1.3}
                            )

                            movement = ExpertMovement(
                                expert_id=expert.get('id'),
                                expert_name=expert.get('name'),
                                expertise_level=expertise_level,
                                from_org=from_org,
                                to_org=aff.get('organization_name'),
                                movement_type='join',
                                signal_type=signal.get('signal_type', 'unknown'),
                                lr_multiplier=signal.get('lr_multiplier', 1.0),
                                detected_date=start_date_str
                            )
                            movements.append(movement)
                    except (ValueError, TypeError):
                        pass

        return sorted(movements, key=lambda m: m.detected_date or '', reverse=True)

    def generate_report(self) -> dict:
        """Generate comprehensive expert report."""
        # Group experts by current organization
        org_experts = {}
        for expert in self.experts:
            for aff in expert.get('known_affiliations', []):
                if aff.get('status') == 'current':
                    org_id = aff.get('organization_id', 'unknown')
                    if org_id not in org_experts:
                        org_experts[org_id] = []
                    org_experts[org_id].append({
                        'name': expert.get('name'),
                        'level': expert.get('expertise_level'),
                        'role': aff.get('role')
                    })

        # Count by expertise level
        level_counts = {}
        for expert in self.experts:
            level = expert.get('expertise_level', 'unknown')
            level_counts[level] = level_counts.get(level, 0) + 1

        return {
            'generated_at': datetime.now(timezone.utc).isoformat(),
            'total_experts': len(self.experts),
            'expertise_distribution': level_counts,
            'experts_by_organization': org_experts,
            'expertise_levels': self.expertise_levels
        }


def format_bank_experts(metrics: BankExpertMetrics) -> str:
    """Format bank expert metrics as human-readable text."""
    lines = []
    lines.append(f"\n{'='*60}")
    lines.append(f"CDM Experts at: {metrics.bank_name}")
    lines.append(f"{'='*60}")
    lines.append(f"Total Experts: {metrics.total_experts}")
    lines.append(f"  - Architects: {metrics.architect_count}")
    lines.append(f"  - Contributors: {metrics.contributor_count}")
    lines.append(f"  - Practitioners: {metrics.practitioner_count}")
    lines.append(f"\nExpertise Score: {metrics.expertise_score:.1f}")
    lines.append(f"Recommended LR Adjustment: {metrics.recommended_lr_adjustment:.2f}x")

    if metrics.experts:
        lines.append("\nExperts:")
        for expert in metrics.experts:
            level_icon = {
                'architect': '[A]',
                'contributor': '[C]',
                'practitioner': '[P]',
                'advocate': '[V]'
            }.get(expert.expertise_level, '[?]')
            lines.append(f"  {level_icon} {expert.expert_name}")
            lines.append(f"      Role: {expert.role}")
            lines.append(f"      LR Impact: {expert.lr_impact:.2f}x")
    else:
        lines.append("\nNo known CDM experts at this organization.")

    return "\n".join(lines)


def format_expert_history(history: dict) -> str:
    """Format expert history as human-readable text."""
    lines = []
    lines.append(f"\n{'='*60}")
    lines.append(f"Expert Profile: {history.get('name')}")
    lines.append(f"{'='*60}")
    lines.append(f"ID: {history.get('expert_id')}")
    lines.append(f"Level: {history.get('expertise_level')}")
    lines.append(f"Expertise Areas: {', '.join(history.get('expertise_areas', []))}")
    lines.append(f"LR Multiplier (Joining): {history.get('lr_multiplier_joining'):.2f}x")
    lines.append(f"LR Multiplier (Leaving): {history.get('lr_multiplier_leaving'):.2f}x")

    lines.append("\nAffiliation History:")
    for aff in history.get('affiliations', []):
        status = "[CURRENT]" if aff.get('status') == 'current' else "[PAST]"
        lines.append(f"  {status} {aff.get('organization_name')}")
        lines.append(f"      Role: {aff.get('role')}")
        lines.append(f"      Period: {aff.get('start_date')} - {aff.get('end_date') or 'Present'}")

    if history.get('public_contributions'):
        lines.append("\nPublic Contributions:")
        for contrib in history.get('public_contributions', []):
            lines.append(f"  - {contrib}")

    if history.get('notes'):
        lines.append(f"\nNotes: {history.get('notes')}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Track CDM experts and their movements',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --bank jpmorgan --show-experts
  %(prog)s --expert EXPERT-001 --show-history
  %(prog)s --track-movement --months 12
  %(prog)s --all-experts --output report.json
        """
    )

    # Scope options
    parser.add_argument('--bank', metavar='BANK_ID',
                       help='Show experts at specific bank')
    parser.add_argument('--expert', metavar='EXPERT_ID',
                       help='Show specific expert history')
    parser.add_argument('--all-experts', action='store_true',
                       help='Generate full expert report')

    # Analysis options
    parser.add_argument('--show-experts', action='store_true',
                       help='Show expert details (requires --bank)')
    parser.add_argument('--show-history', action='store_true',
                       help='Show expert history (requires --expert)')
    parser.add_argument('--track-movement', action='store_true',
                       help='Detect recent expert movements')
    parser.add_argument('--months', type=int, default=12,
                       help='Months to look back for movements (default: 12)')

    # Output options
    parser.add_argument('--output', metavar='FILE',
                       help='Output file path')
    parser.add_argument('--json', action='store_true',
                       help='Output in JSON format')

    args = parser.parse_args()

    # Validate arguments
    if not any([args.bank, args.expert, args.all_experts, args.track_movement]):
        parser.print_help()
        sys.exit(1)

    tracker = ExpertTracker()

    # Show experts at bank
    if args.bank and args.show_experts:
        metrics = tracker.get_bank_experts(args.bank)

        if args.json:
            print(json.dumps(metrics.to_dict(), indent=2))
        else:
            print(format_bank_experts(metrics))
        return

    # Show bank expert count without details
    if args.bank:
        metrics = tracker.get_bank_experts(args.bank)

        if args.json:
            print(json.dumps(metrics.to_dict(), indent=2))
        else:
            print(f"\nBank: {metrics.bank_name}")
            print(f"Known CDM Experts: {metrics.total_experts}")
            print(f"Recommended LR Adjustment: {metrics.recommended_lr_adjustment:.2f}x")
        return

    # Show expert history
    if args.expert:
        history = tracker.get_expert_history(args.expert)

        if not history:
            print(f"Error: Expert '{args.expert}' not found")
            sys.exit(1)

        if args.json:
            print(json.dumps(history, indent=2))
        else:
            print(format_expert_history(history))
        return

    # Track movements
    if args.track_movement:
        movements = tracker.detect_recent_movements(args.months)

        if args.json:
            print(json.dumps([m.to_dict() for m in movements], indent=2))
        else:
            print(f"\nRecent Expert Movements (past {args.months} months)")
            print("=" * 60)
            if not movements:
                print("No recent movements detected.")
            for mov in movements:
                print(f"\n{mov.expert_name} ({mov.expertise_level})")
                print(f"  Movement: {mov.from_org or 'Unknown'} -> {mov.to_org}")
                print(f"  Signal: {mov.signal_type}")
                print(f"  LR Multiplier: {mov.lr_multiplier:.2f}x")
                print(f"  Date: {mov.detected_date}")
        return

    # Generate full report
    if args.all_experts:
        report = tracker.generate_report()

        if args.output:
            output_path = Path(args.output)
            output_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
            print(f"Report saved to: {args.output}")
        elif args.json:
            print(json.dumps(report, indent=2))
        else:
            print(f"\nCDM Expert Report")
            print(f"Generated: {report['generated_at']}")
            print(f"Total Experts: {report['total_experts']}")
            print("\nExpertise Distribution:")
            for level, count in report['expertise_distribution'].items():
                print(f"  - {level}: {count}")
            print("\nExperts by Organization:")
            for org_id, experts in report['experts_by_organization'].items():
                print(f"\n  {org_id}:")
                for expert in experts:
                    print(f"    - {expert['name']} ({expert['level']})")


if __name__ == '__main__':
    main()
