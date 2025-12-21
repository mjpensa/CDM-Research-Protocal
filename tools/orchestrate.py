"""
CDM Research Protocol - Workflow Orchestrator v1.0

Automated workflow orchestrator for CDM research protocol.
Sequences agents, enforces checkpoints, manages state.

This tool:
- Reads workflow-state.json to determine current position
- Checks gate conditions (P > 80% -> skip to adversarial)
- Enforces BLOCK checkpoints requiring human approval
- Updates state files after each stage

Usage:
    python orchestrate.py <bank_directory>
    python orchestrate.py outputs/phase-1/barclays
    python orchestrate.py outputs/phase-1/barclays --advance
    python orchestrate.py outputs/phase-1/barclays --status
"""

import json
import sys
import logging
import hashlib
from pathlib import Path
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field, asdict
from typing import Optional

# Import centralized configuration
try:
    from config_loader import (
        get_skip_threshold,
        get_low_confidence_block_threshold,
        get_confidence_caps
    )
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False
    # Fallback defaults
    def get_skip_threshold(): return 80
    def get_low_confidence_block_threshold(): return 50
    def get_confidence_caps(): return {1: 95, 2: 75, 3: 50, 4: 35, None: 35}

# Import unified state management (Phase 5 consolidation)
try:
    from state_manager import UnifiedStateManager
    from state_adapter import convert_orchestrate_state_to_bank_state
    from state_schema import BankState, normalize_stage
    STATE_MANAGER_AVAILABLE = True
except ImportError:
    STATE_MANAGER_AVAILABLE = False

# --- LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Stage(Enum):
    """Workflow stages in execution order."""
    INIT = "init"
    PRE_MORTEM = "pre_mortem"
    TIER1_EVIDENCE = "tier1_evidence"
    BAYESIAN_1 = "bayesian_1"
    GATE_1 = "gate_1"
    TIER2_EVIDENCE = "tier2_evidence"
    BAYESIAN_2 = "bayesian_2"
    GATE_2 = "gate_2"
    TIER3_EVIDENCE = "tier3_evidence"
    BAYESIAN_3 = "bayesian_3"
    GATE_3 = "gate_3"
    ADVERSARIAL = "adversarial"
    SYNTHESIS = "synthesis"
    VERIFICATION = "verification"
    COMPLETE = "complete"


class CheckpointType(Enum):
    """Types of checkpoints."""
    AUTO_PROCEED = "auto_proceed"
    BLOCK = "block"


# Stage files for provenance hashing
STAGE_FILES = {
    'tier1_evidence': ['1-evidence/tier1-evidence.md'],
    'bayesian_1': ['2-bayesian/post-tier1-update.md'],
    'gate_1': ['3-gates/gate-1.md'],
    'tier2_evidence': ['1-evidence/tier2-evidence.md'],
    'bayesian_2': ['2-bayesian/post-tier2-update.md'],
    'gate_2': ['3-gates/gate-2.md'],
    'adversarial': ['4-adversarial/verdict.md', '4-adversarial/steelman.md'],
    'synthesis': ['5-synthesis/assessment.md'],
}


def compute_stage_hash(bank_dir: Path, stage: str) -> str:
    """
    Compute SHA256 hash of stage output files for provenance tracking.

    Args:
        bank_dir: Path to bank directory
        stage: Stage name

    Returns:
        First 16 chars of SHA256 hex digest
    """
    hasher = hashlib.sha256()
    files = STAGE_FILES.get(stage, [])

    for rel_path in files:
        file_path = bank_dir / rel_path
        if file_path.exists():
            hasher.update(file_path.read_bytes())

    return hasher.hexdigest()[:16]


@dataclass
class WorkflowState:
    """
    State of the research workflow for a bank.

    DEPRECATED: This class is being migrated to state_schema.BankState.
    New code should use UnifiedStateManager for state operations.
    This class is retained for backward compatibility.

    NOTE: As of v1.1, probabilities use 0-1 scale (not 0-100).
    """
    bank_id: str
    current_stage: str = "init"
    probability_architect: float = 0.30  # Default prior (30%) - 0-1 scale
    classification: Optional[str] = None
    sub_classification: Optional[str] = None
    confidence: float = 0.0
    stages_completed: list = field(default_factory=list)
    checkpoints_pending: list = field(default_factory=list)
    checkpoints_approved: list = field(default_factory=list)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    errors: list = field(default_factory=list)
    provenance: dict = field(default_factory=dict)  # Stage -> hash+timestamp

    @classmethod
    def load(cls, state_path: Path) -> 'WorkflowState':
        """Load state from JSON file."""
        if not state_path.exists():
            raise FileNotFoundError(f"No state file at {state_path}")
        data = json.loads(state_path.read_text(encoding='utf-8'))

        # Handle legacy 0-100 scale (convert to 0-1)
        prob = data.get('probability_architect', 0.30)
        if prob > 1.0:
            prob = prob / 100.0

        return cls(
            bank_id=data.get('bank_id', state_path.parent.name),
            current_stage=data.get('current_stage', 'init'),
            probability_architect=prob,
            classification=data.get('classification'),
            sub_classification=data.get('sub_classification'),
            confidence=data.get('confidence', 0.0),
            stages_completed=data.get('stages_completed', []),
            checkpoints_pending=data.get('checkpoints_pending', []),
            checkpoints_approved=data.get('checkpoints_approved', []),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
            errors=data.get('errors', []),
            provenance=data.get('provenance', {})
        )

    def add_provenance(self, bank_dir: Path, stage: str):
        """
        Record provenance hash for a completed stage.

        Args:
            bank_dir: Path to bank directory
            stage: Stage name that was completed
        """
        stage_hash = compute_stage_hash(bank_dir, stage)
        self.provenance[stage] = {
            'hash': stage_hash,
            'at': datetime.utcnow().isoformat()
        }

    def verify_provenance(self, bank_dir: Path) -> list[str]:
        """
        Verify all recorded stage hashes match current files.

        Args:
            bank_dir: Path to bank directory

        Returns:
            List of stages with drift detected (empty if all OK)
        """
        drift = []
        for stage, record in self.provenance.items():
            expected_hash = record.get('hash')
            if not expected_hash:
                continue

            current_hash = compute_stage_hash(bank_dir, stage)
            if current_hash != expected_hash:
                drift.append(
                    f"{stage}: expected {expected_hash[:8]}..., "
                    f"got {current_hash[:8]}... (file modified since {record.get('at', 'unknown')})"
                )

        return drift

    def save(self, state_path: Path, phase: int = 1):
        """
        Save state to JSON file and sync to UnifiedStateManager.

        Args:
            state_path: Path to status.json file
            phase: Phase number for state manager sync (default 1)
        """
        self.updated_at = datetime.utcnow().isoformat()
        if not self.created_at:
            self.created_at = self.updated_at

        data = asdict(self)
        state_path.write_text(json.dumps(data, indent=2), encoding='utf-8')
        logger.info(f"Saved state to {state_path}")

        # Sync to unified state manager (Phase 5 consolidation)
        if STATE_MANAGER_AVAILABLE:
            try:
                outputs_dir = state_path.parent.parent.parent
                sm = UnifiedStateManager(outputs_dir)

                # Get bank name from path
                bank_name = self.bank_id.replace('-', ' ').title()

                # Convert and save
                bank_state = convert_orchestrate_state_to_bank_state(
                    self, bank_name=bank_name, phase=phase
                )
                sm.save_bank_state(bank_state, validate=True)
                logger.debug(f"Synced state to UnifiedStateManager")
            except Exception as e:
                logger.warning(f"Could not sync to state manager: {e}")


class Orchestrator:
    """
    Orchestrates the CDM research workflow.

    Manages stage progression, gate decisions, and checkpoint enforcement.
    """

    # Stage execution order
    STAGE_SEQUENCE = [
        Stage.INIT,
        Stage.PRE_MORTEM,
        Stage.TIER1_EVIDENCE,
        Stage.BAYESIAN_1,
        Stage.GATE_1,
        Stage.TIER2_EVIDENCE,
        Stage.BAYESIAN_2,
        Stage.GATE_2,
        Stage.TIER3_EVIDENCE,
        Stage.BAYESIAN_3,
        Stage.GATE_3,
        Stage.ADVERSARIAL,
        Stage.SYNTHESIS,
        Stage.VERIFICATION,
        Stage.COMPLETE
    ]

    # Stages that can be skipped when probability exceeds threshold
    SKIPPABLE_FROM_GATES = {
        Stage.GATE_1: [Stage.TIER2_EVIDENCE, Stage.BAYESIAN_2, Stage.GATE_2,
                       Stage.TIER3_EVIDENCE, Stage.BAYESIAN_3, Stage.GATE_3],
        Stage.GATE_2: [Stage.TIER3_EVIDENCE, Stage.BAYESIAN_3, Stage.GATE_3],
    }

    # Checkpoint configuration
    CHECKPOINT_CONFIG = {
        Stage.PRE_MORTEM: CheckpointType.AUTO_PROCEED,
        Stage.GATE_1: CheckpointType.AUTO_PROCEED,
        Stage.GATE_2: CheckpointType.AUTO_PROCEED,
        Stage.GATE_3: CheckpointType.AUTO_PROCEED,
        Stage.ADVERSARIAL: CheckpointType.AUTO_PROCEED,  # Unless verdict is REVISED
        Stage.SYNTHESIS: CheckpointType.BLOCK,  # Final classification always requires approval
    }

    def __init__(self, bank_dir: Path):
        """
        Initialize orchestrator for a bank.

        Args:
            bank_dir: Path to bank output directory
        """
        self.bank_dir = Path(bank_dir)
        self.state_path = self.bank_dir / "status.json"
        self.state = self._load_or_init_state()
        # Convert thresholds from percentage (0-100) to decimal (0-1)
        self.skip_threshold = get_skip_threshold() / 100.0
        self.low_confidence_threshold = get_low_confidence_block_threshold()

    def _load_or_init_state(self) -> WorkflowState:
        """Load existing state or initialize new state."""
        if self.state_path.exists():
            try:
                state = WorkflowState.load(self.state_path)

                # Verify provenance integrity
                drift = state.verify_provenance(self.bank_dir)
                if drift:
                    logger.warning("PROVENANCE DRIFT DETECTED - output files modified:")
                    for d in drift:
                        logger.warning(f"  {d}")
                    # Add to checkpoints_pending for review
                    if 'provenance_drift' not in state.checkpoints_pending:
                        state.checkpoints_pending.append('provenance_drift')

                return state
            except Exception as e:
                logger.warning(f"Failed to load state: {e}. Creating new state.")

        # Initialize new state
        state = WorkflowState(
            bank_id=self.bank_dir.name,
            current_stage=Stage.INIT.value,
            probability_architect=0.30,  # Default prior (0-1 scale)
            created_at=datetime.utcnow().isoformat()
        )
        return state

    def get_current_stage(self) -> Stage:
        """Get current stage as Stage enum."""
        try:
            return Stage(self.state.current_stage)
        except ValueError:
            logger.warning(f"Unknown stage: {self.state.current_stage}")
            return Stage.INIT

    def get_next_stage(self) -> Optional[Stage]:
        """
        Determine next stage based on current state and probabilities.

        Returns:
            Next Stage, or None if workflow is complete
        """
        current = self.get_current_stage()
        current_idx = self.STAGE_SEQUENCE.index(current)

        if current == Stage.COMPLETE:
            return None

        # Check skip conditions at gates
        if current in self.SKIPPABLE_FROM_GATES:
            p = self.state.probability_architect
            # Skip if probability is decisive (> 80% or < 20%) - using 0-1 scale
            if p > self.skip_threshold or p < (1.0 - self.skip_threshold):
                logger.info(f"P(Architect) = {p * 100:.1f}% exceeds threshold. Skipping to ADVERSARIAL.")
                return Stage.ADVERSARIAL

        # Normal progression
        if current_idx + 1 < len(self.STAGE_SEQUENCE):
            return self.STAGE_SEQUENCE[current_idx + 1]

        return None

    def _load_anchor_points(self) -> dict:
        """Load anchor points from config."""
        anchor_path = Path(__file__).parent.parent / "config" / "anchor-points.json"
        if anchor_path.exists():
            try:
                return json.loads(anchor_path.read_text(encoding='utf-8'))
            except Exception as e:
                logger.warning(f"Could not load anchor points: {e}")
                return {}
        return {}

    def check_anchor_violation(self) -> tuple[bool, str]:
        """
        Check if current classification violates anchor points.

        Returns:
            (violation_found, violation_message)
        """
        anchors = self._load_anchor_points()
        if not anchors:
            return False, ""

        # Normalize bank_id for comparison
        bank_id = self.state.bank_id.lower().replace('_', '-')
        classification = self.state.classification
        sub_class = self.state.sub_classification

        if not classification:
            return False, ""

        # Check production banks - must be ARCHITECT-Native
        for prod_bank in anchors.get('production_banks', {}).get('banks', []):
            if prod_bank.get('id', '').lower() == bank_id:
                if classification != 'ARCHITECT' or sub_class != 'Native':
                    return True, (
                        f"ANCHOR VIOLATION: {self.state.bank_id} is confirmed in production "
                        f"(since {prod_bank.get('date', 'unknown')}) but classified as "
                        f"{classification}/{sub_class}. Must be ARCHITECT/Native."
                    )

        # Check confirmed contributors - must be ARCHITECT (any variant)
        for contrib in anchors.get('confirmed_contributors', {}).get('banks', []):
            if contrib.get('id', '').lower() == bank_id:
                if classification != 'ARCHITECT':
                    return True, (
                        f"ANCHOR WARNING: {self.state.bank_id} is confirmed contributor "
                        f"({contrib.get('evidence', 'see anchor-points.json')}) but classified as "
                        f"{classification}. Expected ARCHITECT unless explicit contrary evidence."
                    )

        return False, ""

    def should_block(self) -> tuple[bool, str, str]:
        """
        Check if current checkpoint requires human approval.

        Returns:
            (should_block, reason, checkpoint_id)
        """
        current = self.get_current_stage()
        p = self.state.probability_architect

        # Final classification always requires approval
        if current == Stage.SYNTHESIS:
            return True, "Final classification requires human approval", "final_classification"

        # Check anchor point violations
        if self.state.classification:
            violation, msg = self.check_anchor_violation()
            if violation:
                return True, msg, "anchor_point_violation"

        # Low confidence requires review
        if self.state.confidence > 0 and self.state.confidence < self.low_confidence_threshold:
            return True, f"Low confidence ({self.state.confidence}%) requires review", "low_confidence"

        # Adversarial verdict of REVISED requires review
        if current == Stage.ADVERSARIAL:
            if "adversarial_revised" in self.state.checkpoints_pending:
                return True, "Adversarial challenge revised classification", "adversarial_revised"

        # Check for pending contradictions
        if "contradiction_detected" in self.state.checkpoints_pending:
            return True, "Contradiction detected in evidence", "contradiction"

        # Check for provenance drift (files modified after stage completion)
        if "provenance_drift" in self.state.checkpoints_pending:
            return True, "Provenance drift detected - output files modified after completion", "provenance_drift"

        # Check for single-source triangulation requirement
        if "single_source" in self.state.checkpoints_pending:
            return True, "Single-source claim requires corroboration (triangulation)", "triangulation"

        return False, "", ""

    def is_blocked(self) -> bool:
        """
        Check if workflow is currently blocked awaiting approval.

        Returns:
            True if blocked, False if can proceed
        """
        blocked, _, _ = self.should_block()
        return blocked

    def advance(self) -> bool:
        """
        Advance to next stage and update state.

        Returns:
            True if advanced successfully, False if blocked
        """
        # Check if blocked
        should_block, reason, checkpoint_id = self.should_block()
        if should_block:
            if checkpoint_id not in self.state.checkpoints_pending:
                self.state.checkpoints_pending.append(checkpoint_id)
            # Log the block decision
            self.log_checkpoint(checkpoint_id, "BLOCK", reason)
            logger.warning(f"BLOCKED: {reason}")
            logger.warning("Run with --approve to approve checkpoint")
            self.state.save(self.state_path)
            return False

        # Get current and next stage
        current = self.get_current_stage()
        next_stage = self.get_next_stage()

        if next_stage is None:
            logger.info("Workflow complete!")
            return True

        # Record completion
        if current.value not in self.state.stages_completed:
            self.state.stages_completed.append(current.value)

        # Advance
        self.state.current_stage = next_stage.value
        self.state.save(self.state_path)

        logger.info(f"Advanced from {current.value} to {next_stage.value}")
        return True

    def log_checkpoint(self, checkpoint_id: str, action: str, reason: str = None):
        """
        Log checkpoint decision to central checkpoint-log.json.

        Args:
            checkpoint_id: ID of the checkpoint
            action: Action taken (BLOCK, AUTO_PROCEED, APPROVED)
            reason: Reason for the action
        """
        log_path = self.bank_dir.parent.parent / "state" / "checkpoint-log.json"
        log_path.parent.mkdir(parents=True, exist_ok=True)

        existing = []
        if log_path.exists():
            try:
                existing = json.loads(log_path.read_text(encoding='utf-8'))
            except Exception:
                existing = []

        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "bank_id": self.state.bank_id,
            "checkpoint_id": checkpoint_id,
            "action": action,
            "reason": reason,
            "stage": self.state.current_stage,
            "probability": self.state.probability_architect
        }
        existing.append(entry)

        log_path.write_text(json.dumps(existing, indent=2), encoding='utf-8')
        logger.debug(f"Logged checkpoint: {checkpoint_id} -> {action}")

    def approve_checkpoint(self, checkpoint_id: str, approver: str = "human") -> bool:
        """
        Approve a pending checkpoint.

        Args:
            checkpoint_id: ID of checkpoint to approve
            approver: Who approved (for audit)

        Returns:
            True if approved, False if checkpoint not found
        """
        if checkpoint_id not in self.state.checkpoints_pending:
            logger.warning(f"Checkpoint {checkpoint_id} not pending")
            return False

        self.state.checkpoints_pending.remove(checkpoint_id)
        self.state.checkpoints_approved.append({
            "checkpoint_id": checkpoint_id,
            "approved_by": approver,
            "approved_at": datetime.utcnow().isoformat()
        })

        # Log the approval
        self.log_checkpoint(checkpoint_id, "APPROVED", f"Approved by {approver}")
        self.state.save(self.state_path)
        logger.info(f"Approved checkpoint: {checkpoint_id}")
        return True

    def update_probability(self, probability: float, source: str = "bayesian"):
        """
        Update the P(Architect) probability.

        Args:
            probability: New probability (0-1 scale)
            source: What triggered the update
        """
        old_p = self.state.probability_architect
        self.state.probability_architect = probability

        logger.info(f"P(Architect) updated: {old_p * 100:.1f}% -> {probability * 100:.1f}% (source: {source})")
        self.state.save(self.state_path)

    def set_classification(self, classification: str, sub_classification: str,
                          confidence: float):
        """
        Set the classification result.

        Args:
            classification: Main classification (ARCHITECT, PRAGMATIST, etc.)
            sub_classification: Variant (Native, Follower, Vendor-Dependent, etc.)
            confidence: Confidence percentage (0-100)
        """
        self.state.classification = classification
        self.state.sub_classification = sub_classification
        self.state.confidence = confidence

        logger.info(f"Classification set: {classification} ({sub_classification}) at {confidence}%")
        self.state.save(self.state_path)

    def get_status(self) -> dict:
        """Get current workflow status as dict."""
        current = self.get_current_stage()
        next_stage = self.get_next_stage()
        should_block, reason, checkpoint_id = self.should_block()

        return {
            "bank_id": self.state.bank_id,
            "current_stage": current.value,
            "next_stage": next_stage.value if next_stage else None,
            "probability_architect": self.state.probability_architect,
            "classification": self.state.classification,
            "sub_classification": self.state.sub_classification,
            "confidence": self.state.confidence,
            "stages_completed": self.state.stages_completed,
            "checkpoints_pending": self.state.checkpoints_pending,
            "is_blocked": should_block,
            "block_reason": reason if should_block else None,
            "is_complete": current == Stage.COMPLETE
        }


def print_status(status: dict):
    """Print status in human-readable format."""
    print(f"\n{'='*60}")
    print(f"Bank: {status['bank_id']}")
    print(f"{'='*60}")
    print(f"Current Stage:     {status['current_stage']}")
    print(f"Next Stage:        {status['next_stage'] or 'N/A'}")
    # Display probability as percentage (values are 0-1 internally)
    prob = status['probability_architect']
    print(f"P(Architect):      {prob * 100:.1f}%")

    if status['classification']:
        print(f"\nClassification:    {status['classification']}")
        print(f"Sub-classification:{status['sub_classification']}")
        print(f"Confidence:        {status['confidence']}%")

    print(f"\nStages Completed:  {len(status['stages_completed'])}")
    for stage in status['stages_completed']:
        print(f"  [OK] {stage}")

    if status['is_blocked']:
        print(f"\n[BLOCKED] {status['block_reason']}")
        print("Pending checkpoints:", status['checkpoints_pending'])
    elif status['is_complete']:
        print("\n[COMPLETE] Workflow finished")
    else:
        print("\n[READY] Ready to advance")

    print(f"{'='*60}\n")


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python orchestrate.py <bank_directory> [options]")
        print("       python orchestrate.py outputs/phase-1/barclays")
        print("       python orchestrate.py outputs/phase-1/barclays --status")
        print("       python orchestrate.py outputs/phase-1/barclays --advance")
        print("       python orchestrate.py outputs/phase-1/barclays --approve <checkpoint_id>")
        print("       python orchestrate.py outputs/phase-1/barclays --set-probability 75")
        sys.exit(1)

    bank_dir = Path(sys.argv[1])

    # Ensure directory exists
    if not bank_dir.exists():
        logger.info(f"Creating bank directory: {bank_dir}")
        bank_dir.mkdir(parents=True, exist_ok=True)

    orchestrator = Orchestrator(bank_dir)

    # Handle commands
    if len(sys.argv) == 2 or '--status' in sys.argv:
        # Show status
        status = orchestrator.get_status()
        print_status(status)

    elif '--advance' in sys.argv:
        # Advance to next stage
        success = orchestrator.advance()
        status = orchestrator.get_status()
        print_status(status)
        sys.exit(0 if success else 1)

    elif '--approve' in sys.argv:
        # Approve checkpoint
        idx = sys.argv.index('--approve')
        if idx + 1 >= len(sys.argv):
            print("Error: --approve requires checkpoint_id")
            sys.exit(1)
        checkpoint_id = sys.argv[idx + 1]
        success = orchestrator.approve_checkpoint(checkpoint_id)
        status = orchestrator.get_status()
        print_status(status)
        sys.exit(0 if success else 1)

    elif '--set-probability' in sys.argv:
        # Set probability
        idx = sys.argv.index('--set-probability')
        if idx + 1 >= len(sys.argv):
            print("Error: --set-probability requires a value")
            sys.exit(1)
        try:
            prob = float(sys.argv[idx + 1])
            orchestrator.update_probability(prob)
            status = orchestrator.get_status()
            print_status(status)
        except ValueError:
            print("Error: probability must be a number")
            sys.exit(1)

    else:
        print(f"Unknown command. Run with --help for usage.")
        sys.exit(1)


if __name__ == "__main__":
    main()
