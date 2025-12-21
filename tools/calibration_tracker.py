"""
CDM Research Protocol - Calibration Tracker v1.0

Tracks predictions, records outcomes, calculates Brier scores, and detects calibration drift.
This module enables the platform to learn from its predictions and improve over time.

Usage:
    from calibration_tracker import CalibrationTracker

    tracker = CalibrationTracker()

    # Capture a prediction at assessment completion
    pred_id = tracker.capture_prediction(
        bank_id="deutsche-bank",
        phase=1,
        classification="PRAGMATIST",
        variant="Regulatory-Driven",
        probability_architect=0.17,
        confidence=55,
        prior=0.30,
        combined_lr=0.12,
        evidence_summary={...},
        key_evidence_ids=["DB-001", "DB-002"]
    )

    # Record an outcome when ground truth becomes available
    tracker.record_outcome(
        prediction_id=pred_id,
        outcome=0,  # 0=PRAGMATIST confirmed, 1=ARCHITECT confirmed
        outcome_type="vendor_only_confirmation",
        source_url="https://example.com/announcement",
        source_date="2026-06-14",
        excerpt="..."
    )

    # Calculate Brier scores
    metrics = tracker.calculate_brier_scores()

    # Detect calibration drift
    drift = tracker.detect_calibration_drift()
"""

import json
import hashlib
import statistics
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
from functools import lru_cache

# Project imports
try:
    from config_loader import (
        load_calibration_config,
        get_brier_thresholds,
        get_drift_detection_params,
        get_minimum_validations,
        get_lr_adjustment_rules
    )
except ImportError:
    # Allow running standalone
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from config_loader import (
        load_calibration_config,
        get_brier_thresholds,
        get_drift_detection_params,
        get_minimum_validations,
        get_lr_adjustment_rules
    )

# --- PATHS ---
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
STATE_DIR = PROJECT_ROOT / "outputs" / "state"
PREDICTION_LOG_PATH = STATE_DIR / "prediction-log.json"
VALIDATION_LOG_PATH = STATE_DIR / "validation-log.json"
CALIBRATION_METRICS_PATH = STATE_DIR / "calibration-metrics.json"
LR_PERFORMANCE_PATH = STATE_DIR / "lr-performance.json"


# --- DATA CLASSES ---

@dataclass
class EvidenceSummary:
    """Summary of evidence for a prediction."""
    tier1_count: int = 0
    tier2_count: int = 0
    tier3_count: int = 0
    null_results_count: int = 0
    highest_tier: int = 0
    highest_claim_type: Optional[str] = None
    evidence_direction_ratio: float = 0.0
    source_diversity: float = 0.0

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'EvidenceSummary':
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class Prediction:
    """Record of a prediction at assessment time."""
    prediction_id: str
    bank_id: str
    phase: int
    timestamp: str
    predicted_classification: str
    predicted_variant: Optional[str]
    predicted_probability_architect: float  # 0-1 scale
    confidence: int  # 0-100 scale
    prior_probability: float
    combined_lr: float
    evidence_summary: Dict[str, Any]
    key_evidence_ids: List[str]
    validation_status: str = "pending"  # pending | validated | stale
    validation_id: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'Prediction':
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class Validation:
    """Record of a validation (outcome) event."""
    validation_id: str
    prediction_id: str
    bank_id: str
    validation_date: str
    outcome: int  # 1=ARCHITECT confirmed, 0=PRAGMATIST confirmed
    outcome_type: str
    outcome_source: Dict[str, str]  # url, date, excerpt
    predicted_probability: float
    squared_error: float
    error_direction: str  # correct, overconfident, underconfident
    notes: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'Validation':
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class CalibrationMetrics:
    """Rolling calibration metrics."""
    total_predictions: int = 0
    total_validations: int = 0
    current_brier_score: Optional[float] = None
    brier_score_trend: str = "unknown"  # improving, stable, declining
    calibration_status: str = "insufficient_data"  # excellent, good, acceptable, marginal, poor

    tier_breakdown: Dict[str, Dict] = field(default_factory=dict)
    confidence_bucket_analysis: Dict[str, Dict] = field(default_factory=dict)
    drift_analysis: Dict[str, Any] = field(default_factory=dict)
    adjustment_recommendations: List[Dict] = field(default_factory=list)
    quarterly_history: List[Dict] = field(default_factory=list)
    last_updated: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'CalibrationMetrics':
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


# --- MAIN CLASS ---

class CalibrationTracker:
    """
    Main class for prediction tracking and calibration analysis.
    """

    def __init__(self, state_dir: Optional[Path] = None):
        """
        Initialize the calibration tracker.

        Args:
            state_dir: Custom state directory (defaults to outputs/state/)
        """
        self.state_dir = Path(state_dir) if state_dir else STATE_DIR
        self.state_dir.mkdir(parents=True, exist_ok=True)

        self.prediction_log_path = self.state_dir / "prediction-log.json"
        self.validation_log_path = self.state_dir / "validation-log.json"
        self.metrics_path = self.state_dir / "calibration-metrics.json"
        self.lr_performance_path = self.state_dir / "lr-performance.json"

    # --- PREDICTION CAPTURE ---

    def capture_prediction(
        self,
        bank_id: str,
        phase: int,
        classification: str,
        variant: Optional[str],
        probability_architect: float,
        confidence: int,
        prior: float,
        combined_lr: float,
        evidence_summary: Dict[str, Any],
        key_evidence_ids: List[str]
    ) -> str:
        """
        Capture a prediction at assessment completion.

        Args:
            bank_id: Bank identifier
            phase: Research phase number
            classification: Final classification (ARCHITECT, PRAGMATIST, etc.)
            variant: Classification variant (Native, Vendor-Dependent, etc.)
            probability_architect: P(ARCHITECT) as 0-1 scale
            confidence: Confidence percentage (0-100)
            prior: Prior probability P(ARCHITECT) before evidence
            combined_lr: Combined likelihood ratio from all evidence
            evidence_summary: Summary of evidence (tier counts, claim types)
            key_evidence_ids: IDs of key evidence items

        Returns:
            prediction_id: Unique identifier for this prediction
        """
        timestamp = datetime.now(timezone.utc)
        prediction_id = self._generate_prediction_id(bank_id, timestamp)

        prediction = Prediction(
            prediction_id=prediction_id,
            bank_id=bank_id,
            phase=phase,
            timestamp=timestamp.isoformat(),
            predicted_classification=classification,
            predicted_variant=variant,
            predicted_probability_architect=probability_architect,
            confidence=confidence,
            prior_probability=prior,
            combined_lr=combined_lr,
            evidence_summary=evidence_summary,
            key_evidence_ids=key_evidence_ids,
            validation_status="pending"
        )

        # Load existing log and append
        log = self._load_prediction_log()
        log["predictions"].append(prediction.to_dict())
        log["last_updated"] = timestamp.isoformat()
        log["summary"]["total_predictions"] = len(log["predictions"])
        log["summary"]["pending_validations"] = sum(
            1 for p in log["predictions"] if p.get("validation_status") == "pending"
        )

        self._save_prediction_log(log)

        return prediction_id

    # --- OUTCOME RECORDING ---

    def record_outcome(
        self,
        prediction_id: str,
        outcome: int,
        outcome_type: str,
        source_url: str,
        source_date: str,
        excerpt: str,
        notes: str = ""
    ) -> Dict[str, Any]:
        """
        Record an outcome when ground truth becomes available.

        Args:
            prediction_id: ID of the prediction to validate
            outcome: 1 if ARCHITECT confirmed, 0 if PRAGMATIST confirmed
            outcome_type: Type of outcome (production_announcement, rejection_statement, etc.)
            source_url: URL of the source confirming the outcome
            source_date: Date of the source
            excerpt: Relevant excerpt from the source
            notes: Additional notes

        Returns:
            Validation summary with error metrics
        """
        timestamp = datetime.now(timezone.utc)

        # Load prediction
        pred_log = self._load_prediction_log()
        prediction = None
        pred_idx = None

        for idx, p in enumerate(pred_log["predictions"]):
            if p["prediction_id"] == prediction_id:
                prediction = p
                pred_idx = idx
                break

        if prediction is None:
            raise ValueError(f"Prediction {prediction_id} not found")

        # Calculate squared error
        predicted_prob = prediction["predicted_probability_architect"]
        squared_error = (predicted_prob - outcome) ** 2

        # Determine error direction
        if outcome == 1 and predicted_prob >= 0.5:
            error_direction = "correct"
        elif outcome == 0 and predicted_prob < 0.5:
            error_direction = "correct"
        elif outcome == 1 and predicted_prob < 0.5:
            error_direction = "underconfident"  # Missed ARCHITECT
        else:
            error_direction = "overconfident"  # False ARCHITECT prediction

        # Create validation record
        validation_id = self._generate_validation_id(prediction_id, timestamp)

        validation = Validation(
            validation_id=validation_id,
            prediction_id=prediction_id,
            bank_id=prediction["bank_id"],
            validation_date=timestamp.isoformat(),
            outcome=outcome,
            outcome_type=outcome_type,
            outcome_source={
                "url": source_url,
                "date": source_date,
                "excerpt": excerpt
            },
            predicted_probability=predicted_prob,
            squared_error=squared_error,
            error_direction=error_direction,
            notes=notes if notes else None
        )

        # Update prediction status
        pred_log["predictions"][pred_idx]["validation_status"] = "validated"
        pred_log["predictions"][pred_idx]["validation_id"] = validation_id
        pred_log["summary"]["pending_validations"] = sum(
            1 for p in pred_log["predictions"] if p.get("validation_status") == "pending"
        )
        pred_log["last_updated"] = timestamp.isoformat()
        self._save_prediction_log(pred_log)

        # Save validation
        val_log = self._load_validation_log()
        val_log["validations"].append(validation.to_dict())
        val_log["last_updated"] = timestamp.isoformat()
        val_log["summary"]["total_validations"] = len(val_log["validations"])
        self._save_validation_log(val_log)

        # Recalculate metrics
        self._update_calibration_metrics()

        return {
            "validation_id": validation_id,
            "prediction_id": prediction_id,
            "squared_error": squared_error,
            "error_direction": error_direction,
            "outcome_type": outcome_type
        }

    # --- BRIER SCORE CALCULATION ---

    def calculate_brier_scores(self) -> Dict[str, Any]:
        """
        Calculate Brier scores across all validated predictions.

        Returns:
            Comprehensive metrics dict
        """
        val_log = self._load_validation_log()
        validations = val_log.get("validations", [])

        if not validations:
            return {
                "overall_brier_score": None,
                "calibration_status": "insufficient_data",
                "validation_count": 0
            }

        # Overall Brier score
        squared_errors = [v["squared_error"] for v in validations]
        overall_brier = statistics.mean(squared_errors)

        # Determine calibration status
        thresholds = get_brier_thresholds()
        if overall_brier <= thresholds.get("excellent", 0.10):
            status = "excellent"
        elif overall_brier <= thresholds.get("good", 0.15):
            status = "good"
        elif overall_brier <= thresholds.get("acceptable", 0.20):
            status = "acceptable"
        elif overall_brier <= thresholds.get("marginal", 0.25):
            status = "marginal"
        else:
            status = "poor"

        # Tier breakdown
        pred_log = self._load_prediction_log()
        predictions_by_id = {p["prediction_id"]: p for p in pred_log.get("predictions", [])}

        tier_scores = {}
        for tier in [1, 2, 3]:
            tier_validations = [
                v for v in validations
                if predictions_by_id.get(v["prediction_id"], {}).get("evidence_summary", {}).get("highest_tier") == tier
            ]
            if tier_validations:
                tier_scores[f"tier{tier}"] = {
                    "count": len(tier_validations),
                    "brier_score": statistics.mean([v["squared_error"] for v in tier_validations])
                }

        # Confidence bucket analysis
        buckets = self._analyze_confidence_buckets(validations, predictions_by_id)

        return {
            "overall_brier_score": round(overall_brier, 4),
            "calibration_status": status,
            "validation_count": len(validations),
            "tier_breakdown": tier_scores,
            "confidence_buckets": buckets,
            "last_calculated": datetime.now(timezone.utc).isoformat()
        }

    def _analyze_confidence_buckets(
        self,
        validations: List[Dict],
        predictions_by_id: Dict[str, Dict]
    ) -> Dict[str, Dict]:
        """Analyze calibration by confidence level."""
        buckets = {
            "90_100": {"predicted": [], "outcomes": []},
            "70_89": {"predicted": [], "outcomes": []},
            "50_69": {"predicted": [], "outcomes": []},
            "30_49": {"predicted": [], "outcomes": []},
            "under_30": {"predicted": [], "outcomes": []}
        }

        for v in validations:
            pred = predictions_by_id.get(v["prediction_id"], {})
            conf = pred.get("confidence", 50)
            prob = v["predicted_probability"]
            outcome = v["outcome"]

            if conf >= 90:
                bucket = "90_100"
            elif conf >= 70:
                bucket = "70_89"
            elif conf >= 50:
                bucket = "50_69"
            elif conf >= 30:
                bucket = "30_49"
            else:
                bucket = "under_30"

            buckets[bucket]["predicted"].append(prob)
            buckets[bucket]["outcomes"].append(outcome)

        results = {}
        for bucket_name, data in buckets.items():
            if data["predicted"]:
                avg_predicted = statistics.mean(data["predicted"])
                actual_rate = statistics.mean(data["outcomes"])
                results[bucket_name] = {
                    "count": len(data["predicted"]),
                    "avg_predicted_prob": round(avg_predicted, 3),
                    "actual_rate": round(actual_rate, 3),
                    "calibration_error": round(abs(avg_predicted - actual_rate), 3)
                }

        return results

    # --- DRIFT DETECTION ---

    def detect_calibration_drift(self) -> Dict[str, Any]:
        """
        Detect systematic over/under-confidence patterns.

        Returns:
            Drift analysis results
        """
        val_log = self._load_validation_log()
        validations = val_log.get("validations", [])

        params = get_drift_detection_params()
        window_size = params.get("window_size", 10)
        direction_threshold = params.get("direction_threshold", 0.60)

        if len(validations) < window_size:
            return {
                "detected": False,
                "direction": None,
                "severity": None,
                "message": f"Insufficient validations ({len(validations)}/{window_size}) for drift detection"
            }

        # Analyze recent window
        recent = validations[-window_size:]

        overconfident_count = sum(1 for v in recent if v["error_direction"] == "overconfident")
        underconfident_count = sum(1 for v in recent if v["error_direction"] == "underconfident")
        correct_count = sum(1 for v in recent if v["error_direction"] == "correct")

        error_count = overconfident_count + underconfident_count

        if error_count == 0:
            return {
                "detected": False,
                "direction": None,
                "severity": None,
                "message": "No calibration drift detected - all predictions correct"
            }

        overconfident_ratio = overconfident_count / error_count if error_count > 0 else 0
        underconfident_ratio = underconfident_count / error_count if error_count > 0 else 0

        # Check for systematic drift
        drift_detected = False
        direction = None
        severity = None

        severity_thresholds = params.get("severity_thresholds", {"low": 0.05, "medium": 0.10, "high": 0.15})

        if overconfident_ratio > direction_threshold:
            drift_detected = True
            direction = "overconfident"
            # Calculate severity based on average squared error
            avg_error = statistics.mean([v["squared_error"] for v in recent])
            if avg_error > severity_thresholds.get("high", 0.15):
                severity = "high"
            elif avg_error > severity_thresholds.get("medium", 0.10):
                severity = "medium"
            else:
                severity = "low"
        elif underconfident_ratio > direction_threshold:
            drift_detected = True
            direction = "underconfident"
            avg_error = statistics.mean([v["squared_error"] for v in recent])
            if avg_error > severity_thresholds.get("high", 0.15):
                severity = "high"
            elif avg_error > severity_thresholds.get("medium", 0.10):
                severity = "medium"
            else:
                severity = "low"

        return {
            "detected": drift_detected,
            "direction": direction,
            "severity": severity,
            "window_size": window_size,
            "overconfident_count": overconfident_count,
            "underconfident_count": underconfident_count,
            "correct_count": correct_count,
            "overconfident_ratio": round(overconfident_ratio, 3),
            "underconfident_ratio": round(underconfident_ratio, 3),
            "recommended_action": self._get_drift_recommendation(direction, severity) if drift_detected else None
        }

    def _get_drift_recommendation(self, direction: str, severity: str) -> str:
        """Get recommendation based on drift direction and severity."""
        if direction == "overconfident":
            if severity == "high":
                return "Consider reducing confidence caps by 10-15% or reviewing LR values for key evidence types"
            elif severity == "medium":
                return "Monitor closely; consider minor confidence adjustments"
            else:
                return "Minor overconfidence detected; no immediate action required"
        else:  # underconfident
            if severity == "high":
                return "Consider increasing confidence caps or reviewing if evidence quality is being undervalued"
            elif severity == "medium":
                return "Monitor closely; may be underweighting strong evidence"
            else:
                return "Minor underconfidence detected; no immediate action required"

    # --- ADJUSTMENT RECOMMENDATIONS ---

    def generate_adjustment_recommendations(self) -> List[Dict[str, Any]]:
        """
        Generate LR and threshold adjustment recommendations based on observed outcomes.

        Returns:
            List of adjustment recommendations
        """
        recommendations = []

        val_log = self._load_validation_log()
        validations = val_log.get("validations", [])

        rules = get_lr_adjustment_rules()
        min_sample = rules.get("minimum_sample_for_empirical_lr", 5)
        divergence_threshold = rules.get("divergence_threshold_for_recommendation", 0.30)

        if len(validations) < min_sample:
            return [{
                "type": "insufficient_data",
                "message": f"Need at least {min_sample} validations for recommendations",
                "current_count": len(validations)
            }]

        # Analyze drift
        drift = self.detect_calibration_drift()
        if drift.get("detected"):
            recommendations.append({
                "type": "calibration_drift",
                "direction": drift["direction"],
                "severity": drift["severity"],
                "recommendation": drift["recommended_action"]
            })

        # Analyze tier-level performance
        brier_scores = self.calculate_brier_scores()
        tier_breakdown = brier_scores.get("tier_breakdown", {})

        for tier_name, tier_data in tier_breakdown.items():
            if tier_data.get("brier_score", 0) > 0.25:
                recommendations.append({
                    "type": "tier_performance",
                    "tier": tier_name,
                    "brier_score": tier_data["brier_score"],
                    "recommendation": f"Review LR values for {tier_name} evidence types"
                })

        return recommendations

    # --- INTERNAL HELPERS ---

    def _generate_prediction_id(self, bank_id: str, timestamp: datetime) -> str:
        """Generate unique prediction ID."""
        hash_input = f"{bank_id}-{timestamp.isoformat()}"
        hash_suffix = hashlib.sha256(hash_input.encode()).hexdigest()[:8]
        return f"PRED-{timestamp.strftime('%Y%m%d')}-{bank_id}-{hash_suffix}"

    def _generate_validation_id(self, prediction_id: str, timestamp: datetime) -> str:
        """Generate unique validation ID."""
        hash_input = f"{prediction_id}-{timestamp.isoformat()}"
        hash_suffix = hashlib.sha256(hash_input.encode()).hexdigest()[:8]
        return f"VAL-{timestamp.strftime('%Y%m%d')}-{hash_suffix}"

    def _load_prediction_log(self) -> Dict:
        """Load prediction log from disk."""
        if self.prediction_log_path.exists():
            return json.loads(self.prediction_log_path.read_text(encoding='utf-8'))
        return {
            "schema_version": "1.0",
            "predictions": [],
            "summary": {"total_predictions": 0, "pending_validations": 0},
            "last_updated": datetime.now(timezone.utc).isoformat()
        }

    def _save_prediction_log(self, data: Dict) -> None:
        """Save prediction log to disk."""
        self.prediction_log_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )

    def _load_validation_log(self) -> Dict:
        """Load validation log from disk."""
        if self.validation_log_path.exists():
            return json.loads(self.validation_log_path.read_text(encoding='utf-8'))
        return {
            "schema_version": "1.0",
            "validations": [],
            "summary": {"total_validations": 0},
            "last_updated": datetime.now(timezone.utc).isoformat()
        }

    def _save_validation_log(self, data: Dict) -> None:
        """Save validation log to disk."""
        self.validation_log_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )

    def _load_calibration_metrics(self) -> Dict:
        """Load calibration metrics from disk."""
        if self.metrics_path.exists():
            return json.loads(self.metrics_path.read_text(encoding='utf-8'))
        return CalibrationMetrics().to_dict()

    def _save_calibration_metrics(self, data: Dict) -> None:
        """Save calibration metrics to disk."""
        self.metrics_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )

    def _update_calibration_metrics(self) -> None:
        """Recalculate and save calibration metrics."""
        brier_scores = self.calculate_brier_scores()
        drift = self.detect_calibration_drift()
        recommendations = self.generate_adjustment_recommendations()

        pred_log = self._load_prediction_log()
        val_log = self._load_validation_log()

        metrics = CalibrationMetrics(
            total_predictions=len(pred_log.get("predictions", [])),
            total_validations=len(val_log.get("validations", [])),
            current_brier_score=brier_scores.get("overall_brier_score"),
            calibration_status=brier_scores.get("calibration_status", "insufficient_data"),
            tier_breakdown=brier_scores.get("tier_breakdown", {}),
            confidence_bucket_analysis=brier_scores.get("confidence_buckets", {}),
            drift_analysis=drift,
            adjustment_recommendations=recommendations,
            last_updated=datetime.now(timezone.utc).isoformat()
        )

        self._save_calibration_metrics(metrics.to_dict())

    # --- STATUS & REPORTING ---

    def get_status(self) -> Dict[str, Any]:
        """Get current calibration status."""
        pred_log = self._load_prediction_log()
        val_log = self._load_validation_log()

        predictions = pred_log.get("predictions", [])
        validations = val_log.get("validations", [])

        pending = sum(1 for p in predictions if p.get("validation_status") == "pending")
        validated = sum(1 for p in predictions if p.get("validation_status") == "validated")
        stale = sum(1 for p in predictions if p.get("validation_status") == "stale")

        brier_scores = self.calculate_brier_scores()

        return {
            "predictions": {
                "total": len(predictions),
                "pending": pending,
                "validated": validated,
                "stale": stale
            },
            "validations": {
                "total": len(validations)
            },
            "calibration": {
                "brier_score": brier_scores.get("overall_brier_score"),
                "status": brier_scores.get("calibration_status"),
                "min_validations_for_assessment": get_minimum_validations().get("overall_assessment", 10)
            }
        }


# --- CLI INTERFACE ---

def main():
    """CLI interface for calibration tracker."""
    import argparse

    parser = argparse.ArgumentParser(description="CDM Research Protocol - Calibration Tracker")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Status command
    status_parser = subparsers.add_parser("status", help="Show calibration status")

    # Record outcome command
    record_parser = subparsers.add_parser("record-outcome", help="Record a validation outcome")
    record_parser.add_argument("--prediction-id", required=True, help="Prediction ID to validate")
    record_parser.add_argument("--outcome", type=int, choices=[0, 1], required=True,
                               help="1=ARCHITECT confirmed, 0=PRAGMATIST confirmed")
    record_parser.add_argument("--outcome-type", required=True, help="Type of outcome")
    record_parser.add_argument("--source-url", required=True, help="Source URL")
    record_parser.add_argument("--source-date", required=True, help="Source date (YYYY-MM-DD)")
    record_parser.add_argument("--excerpt", required=True, help="Relevant excerpt")
    record_parser.add_argument("--notes", default="", help="Additional notes")

    # Brier scores command
    brier_parser = subparsers.add_parser("brier-scores", help="Calculate Brier scores")

    # Drift detection command
    drift_parser = subparsers.add_parser("detect-drift", help="Detect calibration drift")

    # Recommendations command
    rec_parser = subparsers.add_parser("recommendations", help="Generate adjustment recommendations")

    args = parser.parse_args()

    tracker = CalibrationTracker()

    if args.command == "status":
        status = tracker.get_status()
        print(json.dumps(status, indent=2))

    elif args.command == "record-outcome":
        result = tracker.record_outcome(
            prediction_id=args.prediction_id,
            outcome=args.outcome,
            outcome_type=args.outcome_type,
            source_url=args.source_url,
            source_date=args.source_date,
            excerpt=args.excerpt,
            notes=args.notes
        )
        print(f"Validation recorded: {result['validation_id']}")
        print(f"Squared error: {result['squared_error']:.4f}")
        print(f"Error direction: {result['error_direction']}")

    elif args.command == "brier-scores":
        scores = tracker.calculate_brier_scores()
        print(json.dumps(scores, indent=2))

    elif args.command == "detect-drift":
        drift = tracker.detect_calibration_drift()
        print(json.dumps(drift, indent=2))

    elif args.command == "recommendations":
        recs = tracker.generate_adjustment_recommendations()
        print(json.dumps(recs, indent=2))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
