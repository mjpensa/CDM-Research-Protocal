#!/usr/bin/env python3
"""
Timeline Analyzer Tool

Detects stalled initiatives by analyzing adoption timeline progression.
If announcement in 2022 but no production by 2025, that's a PRAGMATIST signal.

Usage:
    python timeline_analyzer.py --bank deutsche-bank --analyze-progression
    python timeline_analyzer.py --phase 1 --detect-stalls
    python timeline_analyzer.py --bank hsbc --output timeline-report.json
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


def load_timeline_patterns() -> dict:
    """Load adoption timeline patterns configuration."""
    path = CONFIG_DIR / "adoption-timeline-patterns.json"
    if not path.exists():
        return {"stage_progression": {}, "stall_indicators": {}}
    return json.loads(path.read_text(encoding='utf-8'))


@dataclass
class EvidenceStage:
    """Represents evidence at a specific adoption stage."""
    stage: str  # 'announcement', 'pilot', 'production'
    claim_type: str
    date: Optional[str]
    date_parsed: Optional[datetime]
    source_tier: int
    source_url: str
    claim: str

    def to_dict(self) -> dict:
        result = asdict(self)
        result['date_parsed'] = self.date_parsed.isoformat() if self.date_parsed else None
        return result


@dataclass
class StallIndicator:
    """Represents a detected stall in adoption timeline."""
    indicator_type: str
    description: str
    months_stalled: float
    threshold_months: float
    lr_penalty: float
    classification_impact: str
    last_stage: str
    last_evidence_date: Optional[str]

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class TimelineAnalysis:
    """Complete timeline analysis for a bank."""
    bank_id: str
    bank_name: str
    evidence_stages: List[EvidenceStage]
    earliest_evidence: Optional[str]
    latest_evidence: Optional[str]
    current_stage: str
    months_since_last: float
    progression_status: str  # 'progressing', 'stalled', 'completed', 'unknown'
    stall_indicators: List[StallIndicator]
    recommended_lr_adjustment: float
    classification_impact: str

    def to_dict(self) -> dict:
        result = asdict(self)
        result['evidence_stages'] = [e.to_dict() for e in self.evidence_stages]
        result['stall_indicators'] = [s.to_dict() for s in self.stall_indicators]
        return result


class TimelineAnalyzer:
    """Analyzes adoption timeline progression to detect stalls."""

    # Map claim types to stages
    STAGE_MAPPING = {
        'strategic_intent': 'announcement',
        'membership_or_participation': 'announcement',
        'hiring_signal': 'announcement',
        'pilot_or_poc': 'pilot',
        'vendor_proxy_signal': 'pilot',
        'open_source_contribution': 'production',
        'production_usage': 'production'
    }

    def __init__(self):
        self.patterns = load_timeline_patterns()
        self.bank_manifest = load_bank_manifest()
        self.stage_progression = self.patterns.get('stage_progression', {})
        self.stall_indicators = self.patterns.get('stall_indicators', {})

    def load_bank_evidence(
        self,
        bank_id: str,
        phase: Optional[int] = None
    ) -> List[dict]:
        """Load evidence items for a bank."""
        if phase:
            phase_patterns = [f"phase-{phase}-*"]
        else:
            phase_patterns = ["phase-*"]

        for pattern in phase_patterns:
            for phase_dir in OUTPUTS_DIR.glob(pattern):
                bank_dir = phase_dir / bank_id
                evidence_file = bank_dir / "evidence.json"
                if evidence_file.exists():
                    try:
                        data = json.loads(evidence_file.read_text(encoding='utf-8'))
                        return data.get('evidence', data.get('evidence_items', []))
                    except (json.JSONDecodeError, KeyError):
                        pass

        return []

    def parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse a date string to datetime."""
        if not date_str:
            return None

        formats = [
            '%Y-%m-%d',
            '%Y-%m',
            '%Y',
            '%d/%m/%Y',
            '%m/%d/%Y',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%dT%H:%M:%SZ'
        ]

        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue

        return None

    def categorize_evidence(self, evidence: List[dict]) -> List[EvidenceStage]:
        """Categorize evidence by adoption stage."""
        stages = []

        for item in evidence:
            claim_type = item.get('claim_type', '')
            stage = self.STAGE_MAPPING.get(claim_type)

            if not stage:
                continue

            date_str = item.get('date', item.get('evidence_date'))
            date_parsed = self.parse_date(date_str)

            stages.append(EvidenceStage(
                stage=stage,
                claim_type=claim_type,
                date=date_str,
                date_parsed=date_parsed,
                source_tier=item.get('tier', 3),
                source_url=item.get('source_url', ''),
                claim=item.get('claim', '')[:100]  # Truncate
            ))

        # Sort by date
        stages.sort(key=lambda x: x.date_parsed or datetime.min)
        return stages

    def detect_stalls(
        self,
        stages: List[EvidenceStage],
        current_date: Optional[datetime] = None
    ) -> List[StallIndicator]:
        """Detect stalled initiatives based on stage progression."""
        stalls = []
        current_date = current_date or datetime.now(timezone.utc).replace(tzinfo=None)

        if not stages:
            return stalls

        # Find latest evidence for each stage
        stage_latest = {}
        for stage in stages:
            if stage.date_parsed:
                if stage.stage not in stage_latest or stage.date_parsed > stage_latest[stage.stage]:
                    stage_latest[stage.stage] = stage.date_parsed

        # Check for stalls
        has_announcement = 'announcement' in stage_latest
        has_pilot = 'pilot' in stage_latest
        has_production = 'production' in stage_latest

        # Check announcement → pilot stall
        if has_announcement and not has_pilot and not has_production:
            announcement_date = stage_latest['announcement']
            months_since = (current_date - announcement_date).days / 30.44
            threshold = self.stage_progression.get(
                'announcement_to_pilot', {}
            ).get('stall_threshold_months', 24)

            if months_since > threshold:
                stall_config = self.stall_indicators.get('no_progression', {})
                stalls.append(StallIndicator(
                    indicator_type='no_progression',
                    description=f"Announcement without pilot for {months_since:.0f} months",
                    months_stalled=months_since,
                    threshold_months=threshold,
                    lr_penalty=stall_config.get('lr_penalty', 0.6),
                    classification_impact=stall_config.get('classification_impact', 'PRAGMATIST'),
                    last_stage='announcement',
                    last_evidence_date=announcement_date.strftime('%Y-%m-%d')
                ))

        # Check pilot → production stall
        if has_pilot and not has_production:
            pilot_date = stage_latest['pilot']
            months_since = (current_date - pilot_date).days / 30.44
            threshold = self.stage_progression.get(
                'pilot_to_production', {}
            ).get('stall_threshold_months', 48)

            if months_since > threshold:
                stall_config = self.stall_indicators.get('pilot_stall', {})
                stalls.append(StallIndicator(
                    indicator_type='pilot_stall',
                    description=f"Pilot without production for {months_since:.0f} months",
                    months_stalled=months_since,
                    threshold_months=threshold,
                    lr_penalty=stall_config.get('lr_penalty', 0.7),
                    classification_impact=stall_config.get('classification_impact', 'PRAGMATIST'),
                    last_stage='pilot',
                    last_evidence_date=pilot_date.strftime('%Y-%m-%d')
                ))

        return stalls

    def analyze_bank(
        self,
        bank_id: str,
        phase: Optional[int] = None
    ) -> TimelineAnalysis:
        """Analyze timeline progression for a bank."""
        bank_config = get_bank_config(bank_id)
        bank_name = bank_config.get('bank_name', bank_id) if bank_config else bank_id

        # Load and categorize evidence
        evidence = self.load_bank_evidence(bank_id, phase)
        stages = self.categorize_evidence(evidence)

        # Find earliest and latest
        dated_stages = [s for s in stages if s.date_parsed]
        earliest = min(dated_stages, key=lambda x: x.date_parsed).date if dated_stages else None
        latest = max(dated_stages, key=lambda x: x.date_parsed).date if dated_stages else None

        # Determine current stage
        stage_order = {'announcement': 1, 'pilot': 2, 'production': 3}
        current_stage = 'unknown'
        if stages:
            current_stage = max(
                set(s.stage for s in stages),
                key=lambda x: stage_order.get(x, 0)
            )

        # Calculate months since last evidence
        if dated_stages:
            latest_date = max(s.date_parsed for s in dated_stages)
            months_since = (datetime.now() - latest_date).days / 30.44
        else:
            months_since = 0

        # Detect stalls
        stalls = self.detect_stalls(stages)

        # Determine progression status
        if current_stage == 'production':
            progression_status = 'completed'
        elif stalls:
            progression_status = 'stalled'
        elif stages:
            progression_status = 'progressing'
        else:
            progression_status = 'unknown'

        # Calculate LR adjustment
        if stalls:
            # Use worst penalty
            lr_adjustment = min(s.lr_penalty for s in stalls)
            classification_impact = stalls[0].classification_impact
        elif current_stage == 'production':
            lr_adjustment = 1.0
            classification_impact = 'ARCHITECT'
        elif current_stage == 'pilot':
            lr_adjustment = 1.0
            classification_impact = 'Potential ARCHITECT'
        else:
            lr_adjustment = 1.0
            classification_impact = 'Neutral'

        return TimelineAnalysis(
            bank_id=bank_id,
            bank_name=bank_name,
            evidence_stages=stages,
            earliest_evidence=earliest,
            latest_evidence=latest,
            current_stage=current_stage,
            months_since_last=round(months_since, 1),
            progression_status=progression_status,
            stall_indicators=stalls,
            recommended_lr_adjustment=lr_adjustment,
            classification_impact=classification_impact
        )

    def detect_stalls_batch(
        self,
        phase: Optional[int] = None
    ) -> List[TimelineAnalysis]:
        """Detect stalls across all banks in a phase."""
        stalled_banks = []
        banks = self.bank_manifest.get('banks', [])

        if phase:
            banks = [b for b in banks if b.get('phase') == phase]

        for bank_data in banks:
            bank_id = bank_data.get('bank_id', bank_data.get('id'))
            if not bank_id:
                continue

            analysis = self.analyze_bank(bank_id, phase)
            if analysis.stall_indicators:
                stalled_banks.append(analysis)

        return stalled_banks


def format_timeline_analysis(analysis: TimelineAnalysis) -> str:
    """Format timeline analysis as human-readable text."""
    lines = []
    lines.append(f"\n{'='*60}")
    lines.append(f"Timeline Analysis: {analysis.bank_name}")
    lines.append(f"{'='*60}")
    lines.append(f"Current Stage: {analysis.current_stage.upper()}")
    lines.append(f"Progression Status: {analysis.progression_status.upper()}")
    lines.append(f"Months Since Last Evidence: {analysis.months_since_last:.1f}")

    if analysis.earliest_evidence:
        lines.append(f"Evidence Range: {analysis.earliest_evidence} to {analysis.latest_evidence}")

    lines.append(f"\nLR Adjustment: {analysis.recommended_lr_adjustment:.2f}x")
    lines.append(f"Classification Impact: {analysis.classification_impact}")

    if analysis.stall_indicators:
        lines.append("\nSTALL INDICATORS:")
        for stall in analysis.stall_indicators:
            lines.append(f"  [STALL] {stall.indicator_type}")
            lines.append(f"    {stall.description}")
            lines.append(f"    LR Penalty: {stall.lr_penalty:.2f}x")
            lines.append(f"    Impact: {stall.classification_impact}")

    if analysis.evidence_stages:
        lines.append("\nEvidence Timeline:")
        for stage in analysis.evidence_stages:
            stage_icon = {
                'announcement': '[A]',
                'pilot': '[P]',
                'production': '[*]'
            }.get(stage.stage, '[?]')
            date_str = stage.date or 'Unknown'
            lines.append(f"  {stage_icon} {date_str}: {stage.claim_type}")
            lines.append(f"      {stage.claim}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Analyze adoption timeline progression and detect stalls',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --bank deutsche-bank --analyze-progression
  %(prog)s --phase 1 --detect-stalls
  %(prog)s --bank hsbc --output timeline.json
        """
    )

    # Scope options
    parser.add_argument('--bank', metavar='BANK_ID',
                       help='Analyze specific bank')
    parser.add_argument('--phase', type=int, metavar='N',
                       help='Phase number for batch analysis')

    # Analysis options
    parser.add_argument('--analyze-progression', action='store_true',
                       help='Show detailed progression analysis')
    parser.add_argument('--detect-stalls', action='store_true',
                       help='Detect stalled initiatives')

    # Output options
    parser.add_argument('--output', metavar='FILE',
                       help='Output file path')
    parser.add_argument('--json', action='store_true',
                       help='Output in JSON format')

    args = parser.parse_args()

    # Validate arguments
    if not any([args.bank, args.phase, args.detect_stalls]):
        parser.print_help()
        sys.exit(1)

    analyzer = TimelineAnalyzer()

    # Analyze specific bank
    if args.bank:
        analysis = analyzer.analyze_bank(args.bank, args.phase)

        if args.output:
            output_path = Path(args.output)
            output_path.write_text(
                json.dumps(analysis.to_dict(), indent=2),
                encoding='utf-8'
            )
            print(f"Report saved to: {args.output}")
        elif args.json:
            print(json.dumps(analysis.to_dict(), indent=2))
        else:
            print(format_timeline_analysis(analysis))
        return

    # Detect stalls batch
    if args.detect_stalls:
        stalled = analyzer.detect_stalls_batch(args.phase)

        if args.json:
            print(json.dumps([a.to_dict() for a in stalled], indent=2))
        else:
            print(f"\nStalled Initiatives")
            print(f"Phase: {args.phase or 'All'}")
            print(f"Total Stalled: {len(stalled)}")
            print("=" * 60)

            if not stalled:
                print("No stalled initiatives detected.")
            for analysis in stalled:
                print(format_timeline_analysis(analysis))


if __name__ == '__main__':
    main()
