"""
CDM Research Protocol - Workflow Orchestrator

Main orchestrator for fully automated bank research.
Manages the research lifecycle, coordinates components, and tracks progress.

Usage:
    orch = WorkflowOrchestrator()
    result = orch.run_bank("deutsche-bank", phase=1)
"""

import json
import logging
import sys
from pathlib import Path
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from state_manager import UnifiedStateManager
from state_schema import BankState, STAGE_SEQUENCE

from .prompt_assembler import PromptAssembler, StageContext
from .output_validator import OutputValidator, ValidationResult
from .checkpoint_engine import CheckpointEngine, CheckpointDecision

logger = logging.getLogger(__name__)


@dataclass
class StageResult:
    """Result of executing a single stage."""
    stage: str
    success: bool
    validation: Optional[ValidationResult] = None
    checkpoint: Optional[CheckpointDecision] = None
    skipped_to: Optional[str] = None
    error: Optional[str] = None
    duration_seconds: float = 0.0


@dataclass
class BankResearchResult:
    """Complete result of researching a bank."""
    bank_id: str
    bank_name: str
    phase: int
    success: bool
    classification: Optional[str] = None
    classification_variant: Optional[str] = None
    confidence: Optional[float] = None
    final_probability: float = 0.30
    stages_completed: List[str] = field(default_factory=list)
    stages_skipped: List[str] = field(default_factory=list)
    stage_results: List[StageResult] = field(default_factory=list)
    review_items: List[Dict] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    started_at: str = ""
    completed_at: str = ""
    total_duration_seconds: float = 0.0

    def to_dict(self) -> dict:
        data = asdict(self)
        data["stage_results"] = [asdict(r) for r in self.stage_results]
        return data


class WorkflowOrchestrator:
    """
    Main orchestrator for CDM/DRR bank research.

    Coordinates:
    - State management (via UnifiedStateManager)
    - Prompt assembly (via PromptAssembler)
    - Output validation (via OutputValidator)
    - Checkpoint evaluation (via CheckpointEngine)

    Designed for fully automated overnight runs with deferred human review.
    """

    def __init__(self, outputs_dir: Path = None, config_dir: Path = None):
        self.outputs_dir = outputs_dir or Path(__file__).parent.parent.parent / "outputs"
        self.config_dir = config_dir or Path(__file__).parent.parent.parent / "config"

        # Initialize components
        self.state_manager = UnifiedStateManager(self.outputs_dir)
        self.prompt_assembler = PromptAssembler(self.config_dir, self.outputs_dir)
        self.output_validator = OutputValidator(self.outputs_dir)
        self.checkpoint_engine = CheckpointEngine(self.config_dir, self.outputs_dir)

        # Load bank manifest
        self.bank_manifest = self._load_bank_manifest()

    def _load_bank_manifest(self) -> Dict[str, Any]:
        """Load the bank manifest configuration."""
        manifest_path = self.config_dir / "bank-manifest.json"
        if not manifest_path.exists():
            logger.warning(f"Bank manifest not found: {manifest_path}")
            return {"banks": []}

        with open(manifest_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _get_bank_config(self, bank_id: str) -> Optional[Dict]:
        """Get configuration for a specific bank."""
        for bank in self.bank_manifest.get("banks", []):
            if bank.get("bank_id") == bank_id:
                return bank
        return None

    def _get_bank_dir(self, bank_id: str, phase: int) -> Path:
        """Get the output directory for a bank."""
        # Look for existing phase directory
        phase_dirs = sorted(self.outputs_dir.glob(f"phase-{phase}-*"))
        if phase_dirs:
            bank_dir = phase_dirs[0] / bank_id
        else:
            # Create default
            bank_dir = self.outputs_dir / f"phase-{phase}" / bank_id

        # Ensure directory structure exists
        bank_dir.mkdir(parents=True, exist_ok=True)
        for subdir in ["1-evidence", "2-bayesian", "3-gates", "4-adversarial", "5-synthesis", "snapshots"]:
            (bank_dir / subdir).mkdir(exist_ok=True)

        return bank_dir

    def get_status(self, bank_id: str, phase: int) -> Optional[BankState]:
        """Get current status for a bank."""
        return self.state_manager.load_bank_state(bank_id, phase)

    def initialize_bank(self, bank_id: str, phase: int, prior_probability: float = 0.30) -> BankState:
        """
        Initialize research state for a bank.

        Args:
            bank_id: Bank identifier
            phase: Phase number
            prior_probability: Starting P(Architect) - default 30%

        Returns:
            New BankState
        """
        bank_config = self._get_bank_config(bank_id)
        if not bank_config:
            raise ValueError(f"Bank not found in manifest: {bank_id}")

        bank_name = bank_config.get("bank_name", bank_id)

        # Get execution tier from config
        execution_tier = "B"  # Default to B
        if bank_config.get("derivatives_relevance") == "High":
            execution_tier = "A"
        elif bank_config.get("derivatives_relevance") == "Low":
            execution_tier = "C"

        state = self.state_manager.create_bank_state(
            bank_id=bank_id,
            bank_name=bank_name,
            phase=phase,
            prior_probability=prior_probability,
            execution_tier=execution_tier
        )

        logger.info(f"Initialized bank state: {bank_id} (Phase {phase}, Tier {execution_tier})")
        return state

    def get_next_stage(self, state: BankState) -> Optional[str]:
        """
        Determine the next stage to execute.

        Handles skip logic and stage progression.
        """
        if state.is_complete():
            return None

        if state.is_blocked():
            logger.warning(f"Bank {state.bank_id} is blocked: {state.blocked_reason}")
            return None

        current_idx = STAGE_SEQUENCE.index(state.current_stage)

        # Check for skip condition at gates
        if "gate" in state.current_stage:
            skip_to = self.checkpoint_engine.check_skip_condition(state)
            if skip_to:
                # Mark intermediate stages as skipped
                skip_start = current_idx + 1
                skip_end = STAGE_SEQUENCE.index(skip_to)
                for i in range(skip_start, skip_end):
                    state.mark_stage_skipped(STAGE_SEQUENCE[i])
                return skip_to

        # Normal progression
        return state.get_next_stage()

    def build_stage_context(self, state: BankState, bank_config: Dict) -> StageContext:
        """Build context for prompt assembly."""
        bank_dir = self._get_bank_dir(state.bank_id, state.phase)

        # Get evidence counts
        evidence_counts = self.output_validator.count_evidence_by_tier(bank_dir)

        # Get prior evidence
        prior_evidence = []
        evidence_path = bank_dir / "evidence.json"
        if evidence_path.exists():
            try:
                with open(evidence_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    prior_evidence = data.get("evidence_items", [])
            except Exception:
                pass

        return StageContext(
            bank_id=state.bank_id,
            bank_name=state.bank_name,
            bank_config=bank_config,
            current_probability=state.current_probability,
            evidence_counts=evidence_counts,
            highest_tier=self.output_validator.get_highest_tier(bank_dir),
            bank_dir=bank_dir,
            prior_evidence=prior_evidence,
            thresholds=self.prompt_assembler.thresholds
        )

    def validate_stage(self, state: BankState, stage: str) -> ValidationResult:
        """Validate outputs for a stage."""
        bank_dir = self._get_bank_dir(state.bank_id, state.phase)
        return self.output_validator.validate(state.bank_id, state.phase, stage, bank_dir)

    def evaluate_checkpoint(self, state: BankState, stage: str, outputs: Dict = None) -> CheckpointDecision:
        """Evaluate checkpoint for a stage."""
        return self.checkpoint_engine.evaluate(stage, state, outputs)

    def advance_stage(self, state: BankState, stage: str, validation: ValidationResult, checkpoint: CheckpointDecision) -> str:
        """
        Advance to the next stage after completing current.

        Returns:
            Next stage name
        """
        # Mark current stage complete
        state.mark_stage_complete(stage)

        # Update evidence counts from validation
        if "evidence" in stage:
            bank_dir = self._get_bank_dir(state.bank_id, state.phase)
            state.evidence_counts = self.output_validator.count_evidence_by_tier(bank_dir)
            state.highest_tier = self.output_validator.get_highest_tier(bank_dir)

        # Extract probability from parsed outputs
        if validation.parsed_outputs:
            for filename, data in validation.parsed_outputs.items():
                if isinstance(data, dict):
                    prob = data.get("probability")
                    if prob is not None:
                        # Update state probability
                        if prob > 1:
                            prob = prob / 100  # Convert from percentage
                        state.current_probability = prob

        # Handle skip condition
        if checkpoint.skip_to_stage:
            # Mark intermediate stages as skipped
            current_idx = STAGE_SEQUENCE.index(stage)
            skip_idx = STAGE_SEQUENCE.index(checkpoint.skip_to_stage)
            for i in range(current_idx + 1, skip_idx):
                state.mark_stage_skipped(STAGE_SEQUENCE[i])
            state.current_stage = checkpoint.skip_to_stage
            next_stage = checkpoint.skip_to_stage
        else:
            # Normal progression
            next_stage = state.get_next_stage()
            if next_stage:
                state.current_stage = next_stage

        # Queue for review if needed
        if checkpoint.needs_review:
            bank_config = self._get_bank_config(state.bank_id)
            self.checkpoint_engine.queue_for_review(
                bank_id=state.bank_id,
                bank_name=state.bank_name,
                phase=state.phase,
                stage=stage,
                decision=checkpoint,
                state=state,
                context={"bank_config": bank_config}
            )

        # Apply confidence adjustment from checkpoint
        if checkpoint.confidence_adjustment and state.confidence:
            state.confidence = max(20, min(95, state.confidence + checkpoint.confidence_adjustment))

        # Save state
        self.state_manager.save_bank_state(state)

        return next_stage

    def get_prompt_for_stage(self, state: BankState, stage: str) -> str:
        """Get the prompt for a specific stage."""
        bank_config = self._get_bank_config(state.bank_id)
        if not bank_config:
            raise ValueError(f"Bank not found: {state.bank_id}")

        ctx = self.build_stage_context(state, bank_config)
        return self.prompt_assembler.assemble(stage, ctx)

    def get_full_research_prompt(self, bank_id: str, phase: int) -> str:
        """
        Generate a complete research prompt for a bank.

        This is the main entry point for fully automated runs.
        The prompt guides Claude Code through all stages in sequence.
        """
        bank_config = self._get_bank_config(bank_id)
        if not bank_config:
            raise ValueError(f"Bank not found: {bank_id}")

        return self.prompt_assembler.get_full_research_prompt(bank_config, phase)

    def finalize_bank(self, state: BankState) -> BankResearchResult:
        """
        Finalize research for a bank and generate result.

        Called after all stages complete.
        """
        bank_dir = self._get_bank_dir(state.bank_id, state.phase)

        # Extract classification from synthesis outputs
        assessment_path = bank_dir / "5-synthesis" / "assessment.md"
        if assessment_path.exists():
            content = assessment_path.read_text(encoding='utf-8')
            # Parse classification from content
            import re
            match = re.search(r'Classification[:\s]+(ARCHITECT|PRAGMATIST|UNKNOWN)', content, re.IGNORECASE)
            if match:
                state.classification = match.group(1).upper()

            # Parse variant
            match = re.search(r'(Native|Leader|Follower|Vendor|Integration|Regulatory)', content, re.IGNORECASE)
            if match:
                state.classification_variant = match.group(1)

            # Parse confidence
            match = re.search(r'Confidence[:\s]+(\d+(?:\.\d+)?)\s*%', content, re.IGNORECASE)
            if match:
                state.confidence = float(match.group(1))

        # Extract adversarial verdict
        verdict_path = bank_dir / "4-adversarial" / "verdict.md"
        if verdict_path.exists():
            verdict_content = verdict_path.read_text(encoding='utf-8')
            import re
            match = re.search(r'[Vv]erdict[:\s]+(STRENGTHENED|WEAKENED|UNCHANGED|REVISED)', verdict_content)
            if match:
                state.adversarial_verdict = match.group(1).upper()

        # Mark complete
        state.completed_at = datetime.now(timezone.utc).isoformat()
        state.mark_stage_complete("complete")
        self.state_manager.save_bank_state(state)

        # Build result
        review_items = self.checkpoint_engine.get_review_queue(state.phase)
        bank_reviews = [r.to_dict() for r in review_items if r.bank_id == state.bank_id]

        return BankResearchResult(
            bank_id=state.bank_id,
            bank_name=state.bank_name,
            phase=state.phase,
            success=True,
            classification=state.classification,
            classification_variant=state.classification_variant,
            confidence=state.confidence,
            final_probability=state.current_probability,
            stages_completed=state.stages_completed,
            stages_skipped=state.skipped_stages,
            review_items=bank_reviews,
            errors=state.errors,
            started_at=state.started_at,
            completed_at=state.completed_at
        )

    def get_phase_summary(self, phase: int) -> Dict[str, Any]:
        """Get summary of research for a phase."""
        # Find all banks in this phase
        banks_in_phase = [
            b for b in self.bank_manifest.get("banks", [])
            if b.get("phase") == phase
        ]

        completed = []
        in_progress = []
        pending = []
        blocked = []

        for bank in banks_in_phase:
            bank_id = bank["bank_id"]
            state = self.state_manager.load_bank_state(bank_id, phase)

            if state is None:
                pending.append(bank_id)
            elif state.is_complete():
                completed.append({
                    "bank_id": bank_id,
                    "classification": state.classification,
                    "confidence": state.confidence
                })
            elif state.is_blocked():
                blocked.append({
                    "bank_id": bank_id,
                    "reason": state.blocked_reason
                })
            else:
                in_progress.append({
                    "bank_id": bank_id,
                    "stage": state.current_stage,
                    "probability": state.current_probability
                })

        # Get review queue summary
        review_summary = self.checkpoint_engine.get_review_summary()

        return {
            "phase": phase,
            "total_banks": len(banks_in_phase),
            "completed": len(completed),
            "in_progress": len(in_progress),
            "pending": len(pending),
            "blocked": len(blocked),
            "banks_completed": completed,
            "banks_in_progress": in_progress,
            "banks_pending": pending,
            "banks_blocked": blocked,
            "review_queue": review_summary
        }

    def get_banks_for_phase(self, phase: int) -> List[Dict]:
        """Get all bank configurations for a phase."""
        return [
            b for b in self.bank_manifest.get("banks", [])
            if b.get("phase") == phase
        ]

    def clear_bank_state(self, bank_id: str, phase: int) -> None:
        """Clear all state for a bank (for re-running)."""
        bank_dir = self._get_bank_dir(bank_id, phase)

        # Clear review queue items for this bank
        self.checkpoint_engine.clear_review_queue(bank_id)

        # Clear errors
        self.state_manager.clear_errors(bank_id, phase)

        # Note: We don't delete the output files - user can do that manually if needed
        logger.info(f"Cleared state for {bank_id} (Phase {phase})")
