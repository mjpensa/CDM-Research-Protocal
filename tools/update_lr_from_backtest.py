#!/usr/bin/env python3
"""
LR Update Tool

Applies calibration adjustments to bayesian-lr-tables.json with safety controls.
Creates backups and maintains audit trail.

Usage:
    python update_lr_from_backtest.py --backtest-report outputs/state/lr-backtest-report.json --dry-run
    python update_lr_from_backtest.py --backtest-report outputs/state/lr-backtest-report.json --apply
    python update_lr_from_backtest.py --backtest-report outputs/state/lr-backtest-report.json --apply --annotate
"""

import argparse
import json
import logging
import shutil
import sys
from dataclasses import dataclass, asdict
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
BACKUPS_DIR = CONFIG_DIR / "backups"
STATE_DIR = PROJECT_ROOT / "outputs" / "state"

LR_TABLES_FILE = CONFIG_DIR / "bayesian-lr-tables.json"
UPDATE_HISTORY_FILE = STATE_DIR / "lr-update-history.json"

# Safety thresholds
MAX_CHANGE_FACTOR = 2.0  # Max 2x change per update
MIN_SAMPLE_SIZE = 5  # Minimum samples for high-confidence update
MIN_SAMPLE_SIZE_OVERRIDE = 3  # Minimum for any update
MAX_LR_VALUE = 200.0  # Cap maximum LR
MIN_LR_VALUE = 0.01  # Floor minimum LR


@dataclass
class UpdateProposal:
    """A proposed LR update."""
    evidence_type: str
    current_lr: float
    proposed_lr: float
    final_lr: float
    was_capped: bool
    sample_size: int
    confidence: str
    recommendation: str
    status: str  # 'approved', 'rejected', 'applied'
    rejection_reason: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


class LRUpdater:
    """Safely updates LR tables with calibration adjustments."""

    def __init__(self):
        self.lr_tables = self._load_lr_tables()
        self.update_history = self._load_update_history()

    def _load_lr_tables(self) -> dict:
        """Load current LR tables."""
        if not LR_TABLES_FILE.exists():
            logger.error(f"LR tables not found: {LR_TABLES_FILE}")
            return {}

        with open(LR_TABLES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _load_update_history(self) -> dict:
        """Load update history."""
        if not UPDATE_HISTORY_FILE.exists():
            return {"updates": []}

        with open(UPDATE_HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _find_evidence_type_location(self, evidence_type: str) -> Optional[tuple]:
        """Find where an evidence type is defined in LR tables. Returns (tier_key, evidence_type)."""
        for tier_key in ['tier1_evidence', 'tier2_evidence', 'tier3_evidence']:
            tier_data = self.lr_tables.get(tier_key, {})
            evidence_types = tier_data.get('evidence_types', {})
            if evidence_type in evidence_types:
                return (tier_key, evidence_type)
        return None

    def load_backtest_report(self, report_path: Path) -> dict:
        """Load a backtest report."""
        if not report_path.exists():
            raise FileNotFoundError(f"Report not found: {report_path}")

        with open(report_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def validate_proposals(self, proposals: List[dict]) -> List[UpdateProposal]:
        """Validate and process update proposals."""
        validated = []

        for proposal in proposals:
            evidence_type = proposal.get('evidence_type', '')
            current_lr = proposal.get('current_lr', 0)
            proposed_lr = proposal.get('proposed_lr', 0)
            sample_size = proposal.get('sample_size', 0)
            recommendation = proposal.get('recommendation', '')

            # Check if evidence type exists
            location = self._find_evidence_type_location(evidence_type)
            if not location:
                validated.append(UpdateProposal(
                    evidence_type=evidence_type,
                    current_lr=current_lr,
                    proposed_lr=proposed_lr,
                    final_lr=current_lr,
                    was_capped=False,
                    sample_size=sample_size,
                    confidence='none',
                    recommendation=recommendation,
                    status='rejected',
                    rejection_reason=f"Evidence type '{evidence_type}' not found in LR tables"
                ))
                continue

            # Check sample size
            if sample_size < MIN_SAMPLE_SIZE_OVERRIDE:
                validated.append(UpdateProposal(
                    evidence_type=evidence_type,
                    current_lr=current_lr,
                    proposed_lr=proposed_lr,
                    final_lr=current_lr,
                    was_capped=False,
                    sample_size=sample_size,
                    confidence='insufficient',
                    recommendation=recommendation,
                    status='rejected',
                    rejection_reason=f"Sample size {sample_size} below minimum {MIN_SAMPLE_SIZE_OVERRIDE}"
                ))
                continue

            # Determine confidence
            confidence = 'high' if sample_size >= MIN_SAMPLE_SIZE else 'medium'

            # Apply safety caps
            final_lr = proposed_lr
            was_capped = False

            # Max change factor
            if final_lr > current_lr * MAX_CHANGE_FACTOR:
                final_lr = current_lr * MAX_CHANGE_FACTOR
                was_capped = True
            elif final_lr < current_lr / MAX_CHANGE_FACTOR:
                final_lr = current_lr / MAX_CHANGE_FACTOR
                was_capped = True

            # Absolute limits
            if final_lr > MAX_LR_VALUE:
                final_lr = MAX_LR_VALUE
                was_capped = True
            elif final_lr < MIN_LR_VALUE:
                final_lr = MIN_LR_VALUE
                was_capped = True

            validated.append(UpdateProposal(
                evidence_type=evidence_type,
                current_lr=current_lr,
                proposed_lr=proposed_lr,
                final_lr=final_lr,
                was_capped=was_capped,
                sample_size=sample_size,
                confidence=confidence,
                recommendation=recommendation,
                status='approved'
            ))

        return validated

    def preview_changes(self, proposals: List[UpdateProposal]) -> str:
        """Generate preview of changes."""
        lines = []
        lines.append("=" * 70)
        lines.append("LR UPDATE PREVIEW")
        lines.append("=" * 70)

        approved = [p for p in proposals if p.status == 'approved']
        rejected = [p for p in proposals if p.status == 'rejected']

        if approved:
            lines.append("\nAPPROVED CHANGES:")
            for p in approved:
                cap_note = " (capped)" if p.was_capped else ""
                lines.append(f"\n  {p.evidence_type}:")
                lines.append(f"    Current LR: {p.current_lr:.2f}")
                lines.append(f"    Proposed:   {p.proposed_lr:.2f}")
                lines.append(f"    Final:      {p.final_lr:.2f}{cap_note}")
                lines.append(f"    Confidence: {p.confidence} (n={p.sample_size})")
        else:
            lines.append("\nNo changes approved")

        if rejected:
            lines.append("\nREJECTED PROPOSALS:")
            for p in rejected:
                lines.append(f"\n  {p.evidence_type}:")
                lines.append(f"    Reason: {p.rejection_reason}")

        lines.append("\n" + "=" * 70)
        return "\n".join(lines)

    def create_backup(self) -> Path:
        """Create timestamped backup of LR tables."""
        BACKUPS_DIR.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = BACKUPS_DIR / f"bayesian-lr-tables-{timestamp}.json"

        shutil.copy2(LR_TABLES_FILE, backup_path)
        logger.info(f"Backup created: {backup_path}")

        return backup_path

    def apply_changes(
        self,
        proposals: List[UpdateProposal],
        annotate: bool = False
    ) -> List[UpdateProposal]:
        """Apply approved changes to LR tables."""
        applied = []

        for proposal in proposals:
            if proposal.status != 'approved':
                continue

            location = self._find_evidence_type_location(proposal.evidence_type)
            if not location:
                continue

            tier_key, evidence_type = location

            # Update the LR value
            self.lr_tables[tier_key]['evidence_types'][evidence_type]['lr'] = proposal.final_lr

            # Optionally add annotation
            if annotate:
                self.lr_tables[tier_key]['evidence_types'][evidence_type]['calibration_note'] = {
                    'last_updated': datetime.now(timezone.utc).isoformat(),
                    'previous_lr': proposal.current_lr,
                    'sample_size': proposal.sample_size,
                    'confidence': proposal.confidence
                }

            proposal.status = 'applied'
            applied.append(proposal)

        # Save updated tables
        if applied:
            with open(LR_TABLES_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.lr_tables, f, indent=2)

            logger.info(f"Applied {len(applied)} LR update(s)")

        return applied

    def log_update(self, proposals: List[UpdateProposal], backup_path: Path):
        """Log the update to history file."""
        STATE_DIR.mkdir(parents=True, exist_ok=True)

        update_record = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'backup_file': str(backup_path),
            'changes': [p.to_dict() for p in proposals if p.status == 'applied'],
            'rejected': [p.to_dict() for p in proposals if p.status == 'rejected']
        }

        self.update_history['updates'].append(update_record)

        with open(UPDATE_HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.update_history, f, indent=2)

        logger.info(f"Update logged to {UPDATE_HISTORY_FILE}")

    def get_update_history(self) -> List[dict]:
        """Get update history."""
        return self.update_history.get('updates', [])


def main():
    parser = argparse.ArgumentParser(
        description='Apply LR calibration updates with safety controls',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --backtest-report outputs/state/lr-backtest-report.json --dry-run
  %(prog)s --backtest-report outputs/state/lr-backtest-report.json --apply
  %(prog)s --backtest-report outputs/state/lr-backtest-report.json --apply --annotate
  %(prog)s --history
        """
    )

    parser.add_argument('--backtest-report', metavar='FILE',
                       help='Path to backtest report JSON')
    parser.add_argument('--dry-run', action='store_true',
                       help='Preview changes without applying')
    parser.add_argument('--apply', action='store_true',
                       help='Apply the changes')
    parser.add_argument('--annotate', action='store_true',
                       help='Add calibration notes to updated LRs')
    parser.add_argument('--history', action='store_true',
                       help='Show update history')
    parser.add_argument('--json', action='store_true',
                       help='Output in JSON format')

    args = parser.parse_args()

    updater = LRUpdater()

    # Show history
    if args.history:
        history = updater.get_update_history()
        if args.json:
            print(json.dumps(history, indent=2))
        else:
            if not history:
                print("No update history")
            else:
                print(f"LR Update History ({len(history)} updates):")
                for i, update in enumerate(history, 1):
                    print(f"\n{i}. {update['timestamp']}")
                    print(f"   Backup: {update['backup_file']}")
                    print(f"   Changes applied: {len(update.get('changes', []))}")
                    print(f"   Rejected: {len(update.get('rejected', []))}")
        return

    # Need backtest report for other operations
    if not args.backtest_report:
        parser.print_help()
        sys.exit(1)

    # Load report
    try:
        report = updater.load_backtest_report(Path(args.backtest_report))
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    proposals = report.get('adjustment_proposals', [])
    if not proposals:
        print("No adjustment proposals in report")
        sys.exit(0)

    # Validate proposals
    validated = updater.validate_proposals(proposals)

    # Dry run or preview
    if args.dry_run or not args.apply:
        preview = updater.preview_changes(validated)
        print(preview)

        if args.json:
            print("\nJSON output:")
            print(json.dumps([p.to_dict() for p in validated], indent=2))

        if not args.apply:
            print("\nUse --apply to apply these changes")
        return

    # Apply changes
    approved = [p for p in validated if p.status == 'approved']
    if not approved:
        print("No changes to apply (all proposals rejected)")
        sys.exit(0)

    # Create backup
    backup_path = updater.create_backup()

    # Apply
    applied = updater.apply_changes(validated, annotate=args.annotate)

    # Log update
    updater.log_update(validated, backup_path)

    # Report results
    print(f"\nApplied {len(applied)} LR update(s)")
    print(f"Backup saved to: {backup_path}")
    print(f"History logged to: {UPDATE_HISTORY_FILE}")

    if args.json:
        print("\nApplied changes:")
        print(json.dumps([p.to_dict() for p in applied], indent=2))
    else:
        print("\nApplied changes:")
        for p in applied:
            print(f"  {p.evidence_type}: {p.current_lr:.2f} -> {p.final_lr:.2f}")


if __name__ == '__main__':
    main()
