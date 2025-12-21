#!/usr/bin/env python3
"""
LR Calibration Backtesting Tool

Compares predictions against ground truth and calculates empirical LR values.
Identifies miscalibrated evidence types for recalibration.

Usage:
    python backtest_lr_calibration.py --bank deutsche-bank --phase 1
    python backtest_lr_calibration.py --phase 1 --batch
    python backtest_lr_calibration.py --all --output-report outputs/state/lr-backtest-report.json
"""

import argparse
import json
import logging
import math
import sys
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple

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
STATE_DIR = OUTPUTS_DIR / "state"

GROUND_TRUTH_FILE = CONFIG_DIR / "ground-truth.json"
LR_TABLES_FILE = CONFIG_DIR / "bayesian-lr-tables.json"
REGULATORY_CALENDAR_FILE = CONFIG_DIR / "regulatory-calendar.json"

# Calibration thresholds
MIN_SAMPLE_SIZE = 3  # Minimum outcomes before computing observed LR
DIVERGENCE_THRESHOLD = 0.30  # Flag if observed differs from assumed by >30%
MAX_LR_CAP = 200.0  # Maximum LR to prevent numerical instability


@dataclass
class BankPrediction:
    """Represents a bank's prediction for comparison."""
    bank_id: str
    predicted_probability: float  # P(ARCHITECT)
    prediction_date: str
    evidence_summary: Dict[str, int]  # evidence_type -> count
    evidence_items: List[dict]
    source_file: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class CalibrationResult:
    """Results for a single evidence type calibration."""
    evidence_type: str
    assumed_lr: float
    sample_size: int
    architect_with_evidence: int
    pragmatist_with_evidence: int
    observed_lr: Optional[float]
    divergence: Optional[float]
    needs_recalibration: bool
    recommendation: Optional[str]

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class BacktestReport:
    """Complete backtesting report."""
    report_date: str
    analysis_scope: dict
    summary_metrics: dict
    evidence_type_analysis: List[dict]
    bank_level_analysis: List[dict]
    adjustment_proposals: List[dict]

    def to_dict(self) -> dict:
        return asdict(self)


class BacktestEngine:
    """Engine for backtesting LR calibration against ground truth."""

    def __init__(self):
        self.ground_truth = self._load_ground_truth()
        self.lr_tables = self._load_lr_tables()
        self.regulatory_calendar = self._load_regulatory_calendar()
        self.evidence_tracker = defaultdict(lambda: {'architect': 0, 'pragmatist': 0})

    def _load_ground_truth(self) -> dict:
        """Load ground truth file."""
        if not GROUND_TRUTH_FILE.exists():
            logger.warning(f"Ground truth not found: {GROUND_TRUTH_FILE}")
            return {"validated_outcomes": [], "pending_validations": []}

        with open(GROUND_TRUTH_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _load_lr_tables(self) -> dict:
        """Load LR tables."""
        if not LR_TABLES_FILE.exists():
            logger.error(f"LR tables not found: {LR_TABLES_FILE}")
            return {}

        with open(LR_TABLES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _load_regulatory_calendar(self) -> dict:
        """Load regulatory calendar for temporal context."""
        if not REGULATORY_CALENDAR_FILE.exists():
            logger.warning(f"Regulatory calendar not found: {REGULATORY_CALENDAR_FILE}")
            return {}

        with open(REGULATORY_CALENDAR_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _get_assumed_lr(self, evidence_type: str) -> Optional[float]:
        """Get assumed LR for an evidence type from tables."""
        # Check each tier
        for tier_key in ['tier1_evidence', 'tier2_evidence', 'tier3_evidence']:
            tier_data = self.lr_tables.get(tier_key, {})
            evidence_types = tier_data.get('evidence_types', {})
            if evidence_type in evidence_types:
                return evidence_types[evidence_type].get('lr')

        return None

    def _get_validated_outcome(self, bank_id: str) -> Optional[dict]:
        """Get validated outcome for a bank if available."""
        for outcome in self.ground_truth.get('validated_outcomes', []):
            if outcome.get('bank_id') == bank_id:
                return outcome
        return None

    def load_completed_banks(
        self,
        phase: Optional[int] = None,
        bank_id: Optional[str] = None
    ) -> List[BankPrediction]:
        """Load completed bank predictions from outputs."""
        predictions = []

        # Find phase directories
        if phase:
            phase_dirs = list(OUTPUTS_DIR.glob(f"phase-{phase}-*"))
        else:
            phase_dirs = list(OUTPUTS_DIR.glob("phase-*"))

        for phase_dir in phase_dirs:
            if not phase_dir.is_dir():
                continue

            # Find bank directories
            if bank_id:
                bank_dirs = [phase_dir / bank_id] if (phase_dir / bank_id).exists() else []
            else:
                bank_dirs = [d for d in phase_dir.iterdir() if d.is_dir()]

            for bank_dir in bank_dirs:
                evidence_file = bank_dir / "evidence.json"
                if not evidence_file.exists():
                    continue

                try:
                    prediction = self._load_bank_prediction(evidence_file)
                    if prediction:
                        predictions.append(prediction)
                except Exception as e:
                    logger.warning(f"Error loading {evidence_file}: {e}")

        return predictions

    def _load_bank_prediction(self, evidence_file: Path) -> Optional[BankPrediction]:
        """Load a bank prediction from evidence file."""
        with open(evidence_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        bank_id = data.get('bank_id')
        if not bank_id:
            return None

        # Extract evidence items
        evidence_items = data.get('evidence_items', [])

        # Count by evidence type
        evidence_summary = defaultdict(int)
        for item in evidence_items:
            lr_mapping = item.get('lr_mapping', {})
            evidence_type = lr_mapping.get('evidence_type', 'unknown')
            evidence_summary[evidence_type] += 1

        # Get prediction probability if available
        # Look in various places it might be stored
        probability = data.get('bayesian_analysis', {}).get('final_probability')
        if probability is None:
            probability = data.get('final_probability')
        if probability is None:
            # Try to find in synthesis output
            synthesis_dir = evidence_file.parent / "5-synthesis"
            assessment_file = synthesis_dir / "assessment.md"
            if assessment_file.exists():
                try:
                    content = assessment_file.read_text(encoding='utf-8')
                    # Look for probability in markdown
                    import re
                    match = re.search(r'P\(ARCHITECT\)[:\s]+([0-9.]+)', content)
                    if match:
                        probability = float(match.group(1))
                except Exception:
                    pass

        if probability is None:
            probability = 0.5  # Default if not found

        return BankPrediction(
            bank_id=bank_id,
            predicted_probability=probability,
            prediction_date=data.get('last_updated', datetime.now().strftime('%Y-%m-%d')),
            evidence_summary=dict(evidence_summary),
            evidence_items=evidence_items,
            source_file=str(evidence_file)
        )

    def match_to_ground_truth(self, prediction: BankPrediction) -> Optional[Tuple[str, float]]:
        """Match prediction to ground truth outcome. Returns (actual_class, brier_score)."""
        outcome = self._get_validated_outcome(prediction.bank_id)

        if not outcome:
            return None

        actual_class = outcome.get('actual_classification', '')

        # Calculate Brier score
        # Brier = (p - actual)^2 where actual = 1 for ARCHITECT, 0 for PRAGMATIST
        actual_value = 1.0 if 'ARCHITECT' in actual_class else 0.0
        brier_score = (prediction.predicted_probability - actual_value) ** 2

        return (actual_class, brier_score)

    def track_evidence_outcomes(self, predictions: List[BankPrediction]):
        """Track which evidence types appear with which outcomes."""
        for prediction in predictions:
            outcome = self._get_validated_outcome(prediction.bank_id)
            if not outcome:
                continue

            is_architect = 'ARCHITECT' in outcome.get('actual_classification', '')
            outcome_key = 'architect' if is_architect else 'pragmatist'

            for item in prediction.evidence_items:
                lr_mapping = item.get('lr_mapping', {})
                evidence_type = lr_mapping.get('evidence_type', 'unknown')

                if evidence_type != 'unknown':
                    self.evidence_tracker[evidence_type][outcome_key] += 1

    def calculate_observed_lr(self, evidence_type: str) -> Optional[float]:
        """Calculate observed LR from tracked outcomes."""
        counts = self.evidence_tracker.get(evidence_type, {})
        architect_count = counts.get('architect', 0)
        pragmatist_count = counts.get('pragmatist', 0)

        total = architect_count + pragmatist_count
        if total < MIN_SAMPLE_SIZE:
            return None

        # Avoid division by zero with Laplace smoothing
        # P(E|A) approximated by (architect_count + 0.5) / (architect_total + 1)
        # P(E|P) approximated by (pragmatist_count + 0.5) / (pragmatist_total + 1)
        # For simplicity, use direct ratio with small constant
        p_e_given_a = (architect_count + 0.5) / (total + 1)
        p_e_given_p = (pragmatist_count + 0.5) / (total + 1)

        if p_e_given_p < 0.001:
            return MAX_LR_CAP

        observed_lr = p_e_given_a / p_e_given_p
        return min(observed_lr, MAX_LR_CAP)

    def detect_miscalibration(self) -> List[CalibrationResult]:
        """Detect evidence types with miscalibrated LRs."""
        results = []

        for evidence_type, counts in self.evidence_tracker.items():
            architect_count = counts.get('architect', 0)
            pragmatist_count = counts.get('pragmatist', 0)
            total = architect_count + pragmatist_count

            assumed_lr = self._get_assumed_lr(evidence_type)
            observed_lr = self.calculate_observed_lr(evidence_type)

            # Calculate divergence
            divergence = None
            needs_recalibration = False
            recommendation = None

            if assumed_lr and observed_lr and total >= MIN_SAMPLE_SIZE:
                # Log scale divergence
                log_assumed = math.log(assumed_lr + 0.01)
                log_observed = math.log(observed_lr + 0.01)
                divergence = abs(log_observed - log_assumed) / abs(log_assumed) if log_assumed != 0 else 0

                if divergence > DIVERGENCE_THRESHOLD:
                    needs_recalibration = True
                    if observed_lr > assumed_lr:
                        recommendation = f"Increase LR from {assumed_lr:.2f} to ~{observed_lr:.2f} (evidence stronger than assumed)"
                    else:
                        recommendation = f"Decrease LR from {assumed_lr:.2f} to ~{observed_lr:.2f} (evidence weaker than assumed)"

            results.append(CalibrationResult(
                evidence_type=evidence_type,
                assumed_lr=assumed_lr or 0,
                sample_size=total,
                architect_with_evidence=architect_count,
                pragmatist_with_evidence=pragmatist_count,
                observed_lr=observed_lr,
                divergence=divergence,
                needs_recalibration=needs_recalibration,
                recommendation=recommendation
            ))

        return results

    def generate_calibration_report(
        self,
        predictions: List[BankPrediction],
        phase: Optional[int] = None,
        bank_id: Optional[str] = None
    ) -> BacktestReport:
        """Generate comprehensive calibration report."""
        # Track evidence outcomes
        self.track_evidence_outcomes(predictions)

        # Calculate summary metrics
        brier_scores = []
        bank_analyses = []

        for prediction in predictions:
            result = self.match_to_ground_truth(prediction)

            bank_analysis = {
                'bank_id': prediction.bank_id,
                'predicted_probability': prediction.predicted_probability,
                'has_ground_truth': result is not None,
                'actual_classification': result[0] if result else None,
                'brier_score': result[1] if result else None,
                'evidence_count': len(prediction.evidence_items),
                'evidence_types': prediction.evidence_summary
            }
            bank_analyses.append(bank_analysis)

            if result:
                brier_scores.append(result[1])

        # Summary metrics
        avg_brier = sum(brier_scores) / len(brier_scores) if brier_scores else None
        overconfident = sum(1 for b in brier_scores if b > 0.25)
        underconfident = sum(1 for b in brier_scores if b < 0.1 and b > 0)

        summary_metrics = {
            'total_predictions': len(predictions),
            'matched_to_ground_truth': len(brier_scores),
            'average_brier_score': avg_brier,
            'overconfident_predictions': overconfident,
            'underconfident_predictions': underconfident,
            'perfectly_calibrated': len([b for b in brier_scores if 0.1 <= b <= 0.25])
        }

        # Evidence type analysis
        calibration_results = self.detect_miscalibration()
        evidence_analysis = [r.to_dict() for r in calibration_results]

        # Adjustment proposals
        proposals = []
        for result in calibration_results:
            if result.needs_recalibration:
                proposals.append({
                    'evidence_type': result.evidence_type,
                    'current_lr': result.assumed_lr,
                    'proposed_lr': result.observed_lr,
                    'sample_size': result.sample_size,
                    'divergence': result.divergence,
                    'recommendation': result.recommendation,
                    'confidence': 'high' if result.sample_size >= 10 else 'medium'
                })

        return BacktestReport(
            report_date=datetime.now(timezone.utc).isoformat(),
            analysis_scope={
                'phase': phase,
                'bank_id': bank_id,
                'total_banks_analyzed': len(predictions),
                'ground_truth_available': len(brier_scores)
            },
            summary_metrics=summary_metrics,
            evidence_type_analysis=evidence_analysis,
            bank_level_analysis=bank_analyses,
            adjustment_proposals=proposals
        )

    def propose_adjustments(self) -> List[dict]:
        """Generate LR adjustment proposals."""
        calibration_results = self.detect_miscalibration()

        proposals = []
        for result in calibration_results:
            if result.needs_recalibration and result.observed_lr:
                # Safety: max 2x change
                current = result.assumed_lr
                proposed = result.observed_lr

                if proposed > current * 2:
                    proposed = current * 2
                    capped = True
                elif proposed < current / 2:
                    proposed = current / 2
                    capped = True
                else:
                    capped = False

                proposals.append({
                    'evidence_type': result.evidence_type,
                    'current_lr': current,
                    'proposed_lr': proposed,
                    'was_capped': capped,
                    'sample_size': result.sample_size,
                    'divergence': result.divergence,
                    'recommendation': result.recommendation
                })

        return proposals


def print_report(report: BacktestReport, json_output: bool = False):
    """Print the backtest report."""
    if json_output:
        print(json.dumps(report.to_dict(), indent=2))
        return

    print("\n" + "=" * 70)
    print("LR CALIBRATION BACKTEST REPORT")
    print("=" * 70)
    print(f"Report Date: {report.report_date}")
    print(f"Analysis Scope: Phase {report.analysis_scope.get('phase', 'all')}")
    print(f"               Bank: {report.analysis_scope.get('bank_id', 'all')}")

    print("\n--- SUMMARY METRICS ---")
    metrics = report.summary_metrics
    print(f"Total predictions analyzed: {metrics.get('total_predictions', 0)}")
    print(f"Matched to ground truth: {metrics.get('matched_to_ground_truth', 0)}")

    if metrics.get('average_brier_score') is not None:
        print(f"Average Brier score: {metrics['average_brier_score']:.4f}")
        print(f"  (0 = perfect, 0.25 = random)")
        print(f"Overconfident predictions (Brier > 0.25): {metrics.get('overconfident_predictions', 0)}")
        print(f"Underconfident predictions: {metrics.get('underconfident_predictions', 0)}")

    print("\n--- EVIDENCE TYPE CALIBRATION ---")
    for analysis in report.evidence_type_analysis:
        if analysis['sample_size'] == 0:
            continue

        status = "[NEEDS RECALIBRATION]" if analysis['needs_recalibration'] else "[OK]"
        print(f"\n{analysis['evidence_type']} {status}")
        print(f"  Assumed LR: {analysis['assumed_lr']:.2f}")
        print(f"  Observed LR: {analysis['observed_lr']:.2f}" if analysis['observed_lr'] else "  Observed LR: insufficient data")
        print(f"  Sample size: {analysis['sample_size']} (A:{analysis['architect_with_evidence']}, P:{analysis['pragmatist_with_evidence']})")
        if analysis['divergence'] is not None:
            print(f"  Divergence: {analysis['divergence']:.1%}")
        if analysis['recommendation']:
            print(f"  Recommendation: {analysis['recommendation']}")

    if report.adjustment_proposals:
        print("\n--- ADJUSTMENT PROPOSALS ---")
        for proposal in report.adjustment_proposals:
            print(f"\n{proposal['evidence_type']}:")
            print(f"  Current LR: {proposal['current_lr']:.2f} -> Proposed: {proposal['proposed_lr']:.2f}")
            print(f"  Confidence: {proposal.get('confidence', 'medium')}")
            print(f"  {proposal['recommendation']}")

    print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description='LR Calibration Backtesting Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --bank deutsche-bank --phase 1
  %(prog)s --phase 1 --batch
  %(prog)s --all --output-report outputs/state/lr-backtest-report.json
        """
    )

    # Scope options
    parser.add_argument('--bank', metavar='BANK_ID',
                       help='Analyze specific bank')
    parser.add_argument('--phase', type=int, metavar='N',
                       help='Analyze specific phase')
    parser.add_argument('--batch', action='store_true',
                       help='Batch process all banks in scope')
    parser.add_argument('--all', action='store_true',
                       help='Analyze all phases')

    # Output options
    parser.add_argument('--output-report', metavar='FILE',
                       help='Save report to file')
    parser.add_argument('--json', action='store_true',
                       help='Output in JSON format')
    parser.add_argument('--proposals-only', action='store_true',
                       help='Only show adjustment proposals')

    args = parser.parse_args()

    # Need at least one scope option
    if not any([args.bank, args.phase, args.batch, args.all]):
        parser.print_help()
        sys.exit(1)

    engine = BacktestEngine()

    # Load predictions
    phase = args.phase if args.phase else None
    bank_id = args.bank if args.bank else None

    if args.all:
        phase = None
        bank_id = None

    predictions = engine.load_completed_banks(phase=phase, bank_id=bank_id)

    if not predictions:
        print("No completed predictions found for the specified scope")
        sys.exit(1)

    logger.info(f"Loaded {len(predictions)} bank prediction(s)")

    # Generate report
    report = engine.generate_calibration_report(
        predictions=predictions,
        phase=phase,
        bank_id=bank_id
    )

    # Output
    if args.proposals_only:
        if args.json:
            print(json.dumps(report.adjustment_proposals, indent=2))
        else:
            if report.adjustment_proposals:
                print("Adjustment Proposals:")
                for p in report.adjustment_proposals:
                    print(f"  {p['evidence_type']}: {p['current_lr']:.2f} -> {p['proposed_lr']:.2f}")
            else:
                print("No adjustment proposals (all LRs well-calibrated or insufficient data)")
    else:
        print_report(report, json_output=args.json)

    # Save report if requested
    if args.output_report:
        output_path = Path(args.output_report)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report.to_dict(), f, indent=2)

        logger.info(f"Report saved to {output_path}")


if __name__ == '__main__':
    main()
