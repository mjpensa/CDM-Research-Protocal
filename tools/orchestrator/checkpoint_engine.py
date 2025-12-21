"""
CDM Research Protocol - Checkpoint Engine

Evaluates checkpoints and queues edge cases for deferred human review.
Designed for fully automated overnight runs with batch review at end.

Usage:
    engine = CheckpointEngine()
    decision = engine.evaluate(stage, state, outputs)
    if decision.needs_review:
        engine.queue_for_review(bank_id, decision)
"""

import json
import logging
from pathlib import Path
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)


@dataclass
class CheckpointDecision:
    """Result of checkpoint evaluation."""
    checkpoint_id: str
    checkpoint_name: str
    action: str  # AUTO_PROCEED, DEFERRED_REVIEW, CRITICAL_STOP
    needs_review: bool = False
    review_reason: Optional[str] = None
    review_options: List[str] = field(default_factory=list)
    confidence_adjustment: Optional[float] = None
    skip_to_stage: Optional[str] = None
    validation_warnings: List[str] = field(default_factory=list)
    rationale: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class DeferredReviewItem:
    """Item queued for human review at end of run."""
    bank_id: str
    bank_name: str
    phase: int
    checkpoint_id: str
    checkpoint_name: str
    stage: str
    review_reason: str
    current_classification: Optional[str]
    current_confidence: Optional[float]
    current_probability: float
    options: List[str]
    context: Dict[str, Any]
    severity: str  # INFO, WARNING, CRITICAL
    auto_resolution: Optional[str] = None  # What the system did automatically
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        return asdict(self)


class CheckpointEngine:
    """
    Evaluates checkpoints and manages deferred review queue.

    Philosophy:
    - During automated runs, never block - always proceed
    - Queue edge cases for batch human review at end
    - Apply conservative defaults when human judgment would be needed
    """

    def __init__(self, config_dir: Path = None, outputs_dir: Path = None):
        self.config_dir = config_dir or Path(__file__).parent.parent.parent / "config"
        self.outputs_dir = outputs_dir or Path(__file__).parent.parent.parent / "outputs"

        # Load configuration
        self.checkpoint_rules = self._load_json(self.config_dir / "checkpoint-rules.json")
        self.thresholds = self._load_json(self.config_dir / "decision-thresholds.json")

        # Review queue file
        self.review_queue_path = self.outputs_dir / "state" / "deferred-review-queue.json"

    def _load_json(self, path: Path) -> dict:
        """Load JSON file."""
        if not path.exists():
            logger.warning(f"Config file not found: {path}")
            return {}
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_json(self, path: Path, data: dict) -> None:
        """Save JSON file atomically."""
        path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = path.with_suffix('.tmp')
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        temp_path.replace(path)

    def evaluate(self, stage: str, state: Any, outputs: Dict[str, Any] = None) -> CheckpointDecision:
        """
        Evaluate checkpoint for a stage.

        Args:
            stage: Current stage name
            state: BankState object
            outputs: Parsed outputs from the stage

        Returns:
            CheckpointDecision with action and any review needs
        """
        outputs = outputs or {}

        # Map stage to checkpoint type
        if stage == "pre_mortem":
            return self._evaluate_pre_mortem(state, outputs)
        elif stage.startswith("gate_"):
            return self._evaluate_reasoning_gate(stage, state, outputs)
        elif stage.startswith("bayesian_"):
            return self._evaluate_bayesian(stage, state, outputs)
        elif stage == "adversarial_challenge":
            return self._evaluate_adversarial(state, outputs)
        elif stage == "synthesis":
            return self._evaluate_synthesis(state, outputs)
        else:
            # Default: auto-proceed
            return CheckpointDecision(
                checkpoint_id=f"{stage}_default",
                checkpoint_name=f"{stage} Default",
                action="AUTO_PROCEED",
                rationale="No specific checkpoint rules for this stage"
            )

    def _evaluate_pre_mortem(self, state: Any, outputs: Dict) -> CheckpointDecision:
        """Evaluate pre-mortem gate - always auto-proceed."""
        warnings = []

        # Check for required sections in output
        if "pre-mortem.md" in outputs:
            content = outputs.get("pre-mortem.md", "")
            required = ["Failure Mode 1", "Failure Mode 2", "Failure Mode 3", "Failure Mode 4"]
            for section in required:
                if section.lower() not in content.lower():
                    warnings.append(f"Missing section: {section}")

        return CheckpointDecision(
            checkpoint_id="pre_mortem_gate",
            checkpoint_name="Pre-Mortem Gate",
            action="AUTO_PROCEED",
            validation_warnings=warnings,
            rationale="Pre-mortem analysis is preparatory and low-risk"
        )

    def _evaluate_reasoning_gate(self, stage: str, state: Any, outputs: Dict) -> CheckpointDecision:
        """Evaluate reasoning gates with skip logic."""
        gate_num = int(stage.replace("gate_", ""))
        prob = state.current_probability
        skip_threshold = self.thresholds.get("workflow_decisions", {}).get(
            "skip_to_adversarial", {}
        ).get("threshold", 80) / 100.0

        warnings = []
        skip_to = None
        needs_review = False
        review_reason = None

        # Check for skip condition
        if prob > skip_threshold or prob < (1 - skip_threshold):
            skip_to = "adversarial_challenge"
            logger.info(f"Gate {gate_num}: P(A)={prob:.1%} exceeds threshold, skipping to adversarial")

        # Check for high uncertainty
        uncertainty_range = self.thresholds.get("workflow_decisions", {}).get("uncertainty_range", {})
        lower = uncertainty_range.get("lower", 40) / 100.0
        upper = uncertainty_range.get("upper", 60) / 100.0

        if lower < prob < upper:
            warnings.append(f"High uncertainty: P(Architect)={prob:.1%} in {lower:.0%}-{upper:.0%} range")
            needs_review = True
            review_reason = f"Probability {prob:.1%} indicates genuine uncertainty"

        return CheckpointDecision(
            checkpoint_id=f"reasoning_gate_{gate_num}",
            checkpoint_name=f"Reasoning Gate {gate_num}",
            action="AUTO_PROCEED",
            skip_to_stage=skip_to,
            validation_warnings=warnings,
            needs_review=needs_review,
            review_reason=review_reason,
            review_options=["Accept current trajectory", "Request additional evidence"],
            rationale=f"Gate {gate_num} evaluated. P(A)={prob:.1%}"
        )

    def _evaluate_bayesian(self, stage: str, state: Any, outputs: Dict) -> CheckpointDecision:
        """Evaluate Bayesian update with extreme LR check."""
        tier = int(stage.replace("bayesian_", ""))

        needs_review = False
        review_reason = None
        warnings = []

        # Check for extreme likelihood ratio
        if state.probability_history:
            last_update = state.probability_history[-1]
            combined_lr = getattr(last_update, 'combined_lr', 1.0)

            extreme_lr = self.thresholds.get("workflow_decisions", {}).get("extreme_lr_flag", {})
            upper = extreme_lr.get("upper", 100)
            lower = extreme_lr.get("lower", 0.01)

            if combined_lr > upper or combined_lr < lower:
                needs_review = True
                review_reason = f"Extreme combined LR: {combined_lr:.4f}"
                warnings.append(f"Combined LR {combined_lr:.4f} outside normal range [{lower}, {upper}]")
                logger.warning(f"Extreme LR detected for {state.bank_id}: {combined_lr}")

        return CheckpointDecision(
            checkpoint_id=f"bayesian_tier_{tier}",
            checkpoint_name=f"Bayesian Update Tier {tier}",
            action="AUTO_PROCEED",
            needs_review=needs_review,
            review_reason=review_reason,
            review_options=[
                "Accept extreme LR (evidence is genuinely strong)",
                "Review for independence violations",
                "Adjust LR mappings"
            ],
            validation_warnings=warnings,
            rationale=f"Bayesian update for Tier {tier}"
        )

    def _evaluate_adversarial(self, state: Any, outputs: Dict) -> CheckpointDecision:
        """Evaluate adversarial challenge verdict."""
        verdict = outputs.get("verdict", "UNCHANGED")
        needs_review = False
        review_reason = None
        confidence_adj = 0

        # Parse verdict from outputs
        if isinstance(verdict, dict):
            verdict_str = verdict.get("verdict", "UNCHANGED")
        else:
            verdict_str = str(verdict).upper()

        if "REVISED" in verdict_str or "REVERSE" in verdict_str:
            needs_review = True
            review_reason = "Adversarial challenge resulted in classification change"
            confidence_adj = -10
            logger.warning(f"Adversarial challenge REVISED classification for {state.bank_id}")
        elif "STRENGTHENED" in verdict_str:
            confidence_adj = 5
        elif "WEAKENED" in verdict_str:
            confidence_adj = -5
            needs_review = True
            review_reason = "Adversarial challenge weakened classification"

        return CheckpointDecision(
            checkpoint_id="adversarial_verdict",
            checkpoint_name="Adversarial Challenge Verdict",
            action="AUTO_PROCEED",  # Always proceed, queue for review if needed
            needs_review=needs_review,
            review_reason=review_reason,
            review_options=[
                "Approve revised classification",
                "Retain original classification",
                "Request additional evidence gathering"
            ],
            confidence_adjustment=confidence_adj,
            rationale=f"Adversarial verdict: {verdict_str}"
        )

    def _evaluate_synthesis(self, state: Any, outputs: Dict) -> CheckpointDecision:
        """Evaluate final synthesis with confidence check."""
        needs_review = False
        review_reason = None
        warnings = []

        confidence = state.confidence or 0
        low_conf_threshold = self.thresholds.get("workflow_decisions", {}).get(
            "low_confidence_block", {}
        ).get("threshold", 50)

        # Low confidence check
        if confidence < low_conf_threshold:
            needs_review = True
            review_reason = f"Low confidence: {confidence:.0f}% (below {low_conf_threshold}% threshold)"
            warnings.append(f"Confidence {confidence:.0f}% below threshold")

        # Check for UNKNOWN classification
        if state.classification == "UNKNOWN":
            needs_review = True
            review_reason = f"Classification is UNKNOWN - insufficient evidence"

        return CheckpointDecision(
            checkpoint_id="final_classification",
            checkpoint_name="Final Classification",
            action="AUTO_PROCEED",
            needs_review=needs_review,
            review_reason=review_reason,
            review_options=[
                "Approve classification and confidence",
                "Adjust confidence level",
                "Change classification",
                "Mark for additional research"
            ],
            validation_warnings=warnings,
            rationale=f"Final: {state.classification} ({state.classification_variant}) @ {confidence:.0f}%"
        )

    def queue_for_review(
        self,
        bank_id: str,
        bank_name: str,
        phase: int,
        stage: str,
        decision: CheckpointDecision,
        state: Any,
        context: Dict[str, Any] = None
    ) -> None:
        """
        Add item to deferred review queue.

        Called when a checkpoint flags something for human review.
        The run continues, but the item is logged for batch review later.
        """
        # Determine severity
        if "REVISED" in decision.rationale or "UNKNOWN" in (state.classification or ""):
            severity = "CRITICAL"
        elif decision.confidence_adjustment and decision.confidence_adjustment < -5:
            severity = "WARNING"
        else:
            severity = "INFO"

        item = DeferredReviewItem(
            bank_id=bank_id,
            bank_name=bank_name,
            phase=phase,
            checkpoint_id=decision.checkpoint_id,
            checkpoint_name=decision.checkpoint_name,
            stage=stage,
            review_reason=decision.review_reason or "Flagged for review",
            current_classification=state.classification,
            current_confidence=state.confidence,
            current_probability=state.current_probability,
            options=decision.review_options,
            context=context or {},
            severity=severity,
            auto_resolution=f"Proceeded automatically with {decision.action}"
        )

        # Load existing queue
        if self.review_queue_path.exists():
            data = self._load_json(self.review_queue_path)
        else:
            data = {
                "description": "Deferred review queue for overnight research runs",
                "items": [],
                "summary": {}
            }

        # Add item
        data["items"].append(item.to_dict())

        # Update summary
        data["summary"] = {
            "total_items": len(data["items"]),
            "critical_count": sum(1 for i in data["items"] if i.get("severity") == "CRITICAL"),
            "warning_count": sum(1 for i in data["items"] if i.get("severity") == "WARNING"),
            "info_count": sum(1 for i in data["items"] if i.get("severity") == "INFO"),
            "last_updated": datetime.now(timezone.utc).isoformat()
        }

        self._save_json(self.review_queue_path, data)
        logger.info(f"Queued for review: {bank_id} - {decision.checkpoint_name} ({severity})")

    def get_review_queue(self, phase: int = None) -> List[DeferredReviewItem]:
        """Get pending review items, optionally filtered by phase."""
        if not self.review_queue_path.exists():
            return []

        data = self._load_json(self.review_queue_path)
        items = [DeferredReviewItem(**i) for i in data.get("items", [])]

        if phase is not None:
            items = [i for i in items if i.phase == phase]

        return items

    def get_review_summary(self) -> Dict[str, Any]:
        """Get summary of items needing review."""
        if not self.review_queue_path.exists():
            return {"total_items": 0}

        data = self._load_json(self.review_queue_path)
        return data.get("summary", {"total_items": 0})

    def clear_review_queue(self, bank_id: str = None) -> int:
        """
        Clear review queue items.

        Args:
            bank_id: If provided, only clear items for this bank

        Returns:
            Number of items cleared
        """
        if not self.review_queue_path.exists():
            return 0

        data = self._load_json(self.review_queue_path)
        original_count = len(data.get("items", []))

        if bank_id:
            data["items"] = [i for i in data["items"] if i.get("bank_id") != bank_id]
        else:
            data["items"] = []

        cleared = original_count - len(data["items"])

        # Update summary
        data["summary"] = {
            "total_items": len(data["items"]),
            "critical_count": sum(1 for i in data["items"] if i.get("severity") == "CRITICAL"),
            "warning_count": sum(1 for i in data["items"] if i.get("severity") == "WARNING"),
            "info_count": sum(1 for i in data["items"] if i.get("severity") == "INFO"),
            "last_updated": datetime.now(timezone.utc).isoformat()
        }

        self._save_json(self.review_queue_path, data)
        return cleared

    def check_skip_condition(self, state: Any) -> Optional[str]:
        """
        Check if current probability triggers a skip.

        Returns:
            Stage to skip to, or None to continue normally
        """
        prob = state.current_probability
        skip_threshold = self.thresholds.get("workflow_decisions", {}).get(
            "skip_to_adversarial", {}
        ).get("threshold", 80) / 100.0

        if prob > skip_threshold or prob < (1 - skip_threshold):
            return "adversarial_challenge"

        return None

    def get_confidence_cap(self, highest_tier: int) -> float:
        """
        Get confidence cap based on highest evidence tier.

        Args:
            highest_tier: Highest tier of evidence found (1, 2, 3, or 4)

        Returns:
            Maximum confidence percentage (0-100)
        """
        caps = self.thresholds.get("confidence_caps", {})

        tier_keys = {
            1: "tier1_only",
            2: "tier2_only",
            3: "tier3_only",
            4: "tier4_inference_only"
        }

        key = tier_keys.get(highest_tier, "tier4_inference_only")
        return caps.get(key, 35)
