"""
CDM Research Protocol - Unified State Manager v1.0

Single source of truth for all workflow state.
Replaces disparate state management across orchestration tools.

Features:
- Atomic writes (write to temp, rename)
- Lock file for concurrent access
- State validation on load/save
- Provenance tracking

Usage:
    from state_manager import UnifiedStateManager

    manager = UnifiedStateManager(Path("outputs"))
    state = manager.load_bank_state("deutsche-bank", phase=1)
    state.update_probability(0.65, combined_lr=2.5, evidence_count=5, stage="bayesian_t1")
    manager.save_bank_state(state)
"""

import json
import os
import sys
import time
import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from contextlib import contextmanager

# Cross-platform file locking
if sys.platform == 'win32':
    import msvcrt
    WINDOWS = True
else:
    import fcntl
    WINDOWS = False

from state_schema import (
    BankState, WorkflowState, ProbabilityUpdate, CheckpointEvent,
    ErrorEvent, ReviewItem, STAGE_SEQUENCE
)

logger = logging.getLogger(__name__)


class StateLockError(Exception):
    """Raised when state file is locked by another process."""
    pass


class StateValidationError(Exception):
    """Raised when state validation fails."""
    pass


class UnifiedStateManager:
    """
    Single source of truth for all workflow state.

    Manages:
    - Per-bank state (outputs/phase-N/bank-id/status.json)
    - Workflow state (outputs/state/workflow-state.json)
    - Checkpoint log (outputs/state/checkpoint-log.json)
    - Error log (outputs/state/error-log.json)
    - Review queue (outputs/state/review-queue.json)
    """

    def __init__(self, outputs_dir: Path):
        """
        Initialize the state manager.

        Args:
            outputs_dir: Path to the outputs directory
        """
        self.outputs_dir = Path(outputs_dir)
        self.state_dir = self.outputs_dir / "state"

        # Ensure state directory exists
        self.state_dir.mkdir(parents=True, exist_ok=True)

        # State file paths
        self.workflow_state_path = self.state_dir / "workflow-state.json"
        self.checkpoint_log_path = self.state_dir / "checkpoint-log.json"
        self.error_log_path = self.state_dir / "error-log.json"
        self.review_queue_path = self.state_dir / "review-queue.json"

        # Lock timeout
        self.lock_timeout = 30  # seconds

    def _get_bank_dir(self, bank_id: str, phase: int) -> Path:
        """Get the directory for a bank's outputs."""
        return self.outputs_dir / f"phase-{phase}-*" / bank_id

    def _get_bank_status_path(self, bank_id: str, phase: int) -> Path:
        """Get the path to a bank's status.json file."""
        # Find the phase directory (could have suffix like "european-tier1")
        phase_dirs = list(self.outputs_dir.glob(f"phase-{phase}-*"))
        if phase_dirs:
            bank_dir = phase_dirs[0] / bank_id
        else:
            # Create default phase directory
            bank_dir = self.outputs_dir / f"phase-{phase}" / bank_id

        bank_dir.mkdir(parents=True, exist_ok=True)
        return bank_dir / "status.json"

    @contextmanager
    def _file_lock(self, path: Path):
        """
        Context manager for file locking.

        Uses exclusive lock file creation which works cross-platform.
        """
        lock_path = path.with_suffix('.lock')

        try:
            # Try to acquire lock
            start_time = time.time()
            while True:
                try:
                    # Create lock file exclusively
                    fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                    os.close(fd)
                    break
                except (FileExistsError, OSError) as e:
                    # Check for stale lock (older than 5 minutes)
                    if lock_path.exists():
                        lock_age = time.time() - lock_path.stat().st_mtime
                        if lock_age > 300:  # 5 minutes
                            logger.warning(f"Removing stale lock file: {lock_path}")
                            try:
                                lock_path.unlink()
                                continue
                            except OSError:
                                pass

                    if time.time() - start_time > self.lock_timeout:
                        raise StateLockError(f"Timeout waiting for lock on {path}")
                    time.sleep(0.1)

            yield

        finally:
            # Release lock
            try:
                lock_path.unlink()
            except (FileNotFoundError, OSError):
                pass

    def _atomic_write(self, path: Path, data: dict) -> None:
        """
        Atomically write data to a JSON file.

        Writes to a temp file first, then renames.
        """
        temp_path = path.with_suffix('.tmp')

        # Write to temp file
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        # Atomic rename
        temp_path.replace(path)

    def _load_json(self, path: Path, default: dict = None) -> dict:
        """Load JSON file, returning default if not exists."""
        if not path.exists():
            return default if default is not None else {}

        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Error loading {path}: {e}")
            return default if default is not None else {}

    # ========== Bank State Management ==========

    def load_bank_state(self, bank_id: str, phase: int) -> Optional[BankState]:
        """
        Load state for a specific bank.

        Args:
            bank_id: Bank identifier
            phase: Phase number

        Returns:
            BankState if exists, None otherwise
        """
        path = self._get_bank_status_path(bank_id, phase)

        if not path.exists():
            return None

        try:
            data = self._load_json(path)
            return BankState.from_dict(data)
        except Exception as e:
            logger.error(f"Error loading bank state for {bank_id}: {e}")
            return None

    def save_bank_state(self, state: BankState) -> None:
        """
        Save bank state with atomic write.

        Args:
            state: BankState to save
        """
        path = self._get_bank_status_path(state.bank_id, state.phase)

        # Update timestamp
        state.last_updated = datetime.now(timezone.utc).isoformat()

        # Atomic write
        self._atomic_write(path, state.to_dict())
        logger.debug(f"Saved state for {state.bank_id}")

    def create_bank_state(self, bank_id: str, bank_name: str, phase: int,
                          prior_probability: float = 0.30,
                          execution_tier: str = "B") -> BankState:
        """
        Create a new bank state.

        Args:
            bank_id: Bank identifier
            bank_name: Bank display name
            phase: Phase number
            prior_probability: Starting probability for Architect
            execution_tier: A, B, or C

        Returns:
            New BankState
        """
        state = BankState(
            bank_id=bank_id,
            bank_name=bank_name,
            phase=phase,
            prior_probability=prior_probability,
            current_probability=prior_probability,
            execution_tier=execution_tier
        )

        self.save_bank_state(state)
        return state

    def update_probability(self, bank_id: str, phase: int,
                          posterior: float, combined_lr: float,
                          evidence_count: int, stage: str) -> None:
        """
        Update probability for a bank.

        Args:
            bank_id: Bank identifier
            phase: Phase number
            posterior: New probability
            combined_lr: Combined likelihood ratio
            evidence_count: Number of evidence items
            stage: Current stage
        """
        state = self.load_bank_state(bank_id, phase)
        if state is None:
            raise ValueError(f"No state found for {bank_id}")

        state.update_probability(posterior, combined_lr, evidence_count, stage)
        self.save_bank_state(state)

    def mark_stage_complete(self, bank_id: str, phase: int, stage: str) -> None:
        """Mark a stage as completed for a bank."""
        state = self.load_bank_state(bank_id, phase)
        if state is None:
            raise ValueError(f"No state found for {bank_id}")

        state.mark_stage_complete(stage)

        # Update current stage to next in sequence
        next_stage = state.get_next_stage()
        if next_stage:
            state.current_stage = next_stage

        self.save_bank_state(state)

    def mark_stage_skipped(self, bank_id: str, phase: int, stage: str) -> None:
        """Mark a stage as skipped for a bank."""
        state = self.load_bank_state(bank_id, phase)
        if state is None:
            raise ValueError(f"No state found for {bank_id}")

        state.mark_stage_skipped(stage)
        self.save_bank_state(state)

    def set_bank_blocked(self, bank_id: str, phase: int,
                         checkpoint: str, reason: str) -> None:
        """Set a bank as blocked at a checkpoint."""
        state = self.load_bank_state(bank_id, phase)
        if state is None:
            raise ValueError(f"No state found for {bank_id}")

        state.set_blocked(checkpoint, reason)
        self.save_bank_state(state)

        # Also update workflow state
        workflow = self.load_workflow_state()
        workflow.mark_bank_blocked(bank_id)
        self.save_workflow_state(workflow)

    def clear_bank_block(self, bank_id: str, phase: int) -> None:
        """Clear the blocked status for a bank."""
        state = self.load_bank_state(bank_id, phase)
        if state is None:
            raise ValueError(f"No state found for {bank_id}")

        state.clear_block()
        self.save_bank_state(state)

    # ========== Workflow State Management ==========

    def load_workflow_state(self) -> WorkflowState:
        """Load the master workflow state."""
        if not self.workflow_state_path.exists():
            return WorkflowState()

        try:
            data = self._load_json(self.workflow_state_path)
            return WorkflowState.from_dict(data)
        except Exception as e:
            logger.error(f"Error loading workflow state: {e}")
            return WorkflowState()

    def save_workflow_state(self, state: WorkflowState) -> None:
        """Save the master workflow state."""
        state.last_updated = datetime.now(timezone.utc).isoformat()
        self._atomic_write(self.workflow_state_path, state.to_dict())

    def initialize_workflow(self, mode: str, bank_ids: List[str]) -> WorkflowState:
        """
        Initialize a new workflow.

        Args:
            mode: Execution mode (single_bank_test, phase_pilot, full_rollout)
            bank_ids: List of bank IDs to process

        Returns:
            New WorkflowState
        """
        state = WorkflowState(
            execution_mode=mode,
            banks_pending=bank_ids.copy()
        )
        state.log_event("workflow_initialized", f"Mode: {mode}, Banks: {len(bank_ids)}")
        self.save_workflow_state(state)
        return state

    # ========== Checkpoint Logging ==========

    def log_checkpoint(self, event: CheckpointEvent) -> None:
        """Log a checkpoint event."""
        data = self._load_json(self.checkpoint_log_path, {"checkpoints": [], "summary": {}})

        data["checkpoints"].append(event.to_dict())

        # Update summary
        summary = data.get("summary", {})
        summary["total_checkpoints"] = len(data["checkpoints"])
        summary["auto_proceed_count"] = sum(
            1 for c in data["checkpoints"] if c.get("action") == "auto_proceed"
        )
        summary["blocked_count"] = sum(
            1 for c in data["checkpoints"] if c.get("action") == "block"
        )
        data["summary"] = summary

        self._atomic_write(self.checkpoint_log_path, data)

    def get_checkpoints_for_bank(self, bank_id: str) -> List[CheckpointEvent]:
        """Get all checkpoint events for a bank."""
        data = self._load_json(self.checkpoint_log_path, {"checkpoints": []})
        return [
            CheckpointEvent.from_dict(c)
            for c in data["checkpoints"]
            if c.get("bank_id") == bank_id
        ]

    # ========== Error Logging ==========

    def log_error(self, event: ErrorEvent) -> None:
        """Log an error event."""
        data = self._load_json(self.error_log_path, {"errors": [], "summary": {}})

        data["errors"].append(event.to_dict())

        # Update summary
        summary = data.get("summary", {})
        summary["total_errors"] = len(data["errors"])
        data["summary"] = summary

        self._atomic_write(self.error_log_path, data)

        # Also add to bank state
        try:
            # Find phase from bank manifest or existing state
            state = None
            for phase in range(1, 10):
                state = self.load_bank_state(event.bank_id, phase)
                if state:
                    break

            if state:
                state.add_error(f"{event.stage}: {event.error_message}")
                self.save_bank_state(state)
        except Exception as e:
            logger.warning(f"Could not update bank state with error: {e}")

    def clear_errors(self, bank_id: str) -> None:
        """Clear errors for a bank."""
        data = self._load_json(self.error_log_path, {"errors": [], "summary": {}})

        data["errors"] = [
            e for e in data["errors"]
            if e.get("bank_id") != bank_id
        ]

        self._atomic_write(self.error_log_path, data)

    # ========== Review Queue ==========

    def add_to_review_queue(self, item: ReviewItem) -> None:
        """Add an item to the review queue."""
        data = self._load_json(self.review_queue_path, {"items": [], "last_updated": None})

        data["items"].append(item.to_dict())
        data["last_updated"] = datetime.now(timezone.utc).isoformat()

        self._atomic_write(self.review_queue_path, data)

    def get_pending_reviews(self) -> List[ReviewItem]:
        """Get all pending review items."""
        data = self._load_json(self.review_queue_path, {"items": []})
        return [
            ReviewItem.from_dict(item)
            for item in data["items"]
            if item.get("status") == "pending"
        ]

    def resolve_review(self, bank_id: str, resolution: str, resolved_by: str = "human") -> None:
        """Resolve a review item."""
        data = self._load_json(self.review_queue_path, {"items": []})

        for item in data["items"]:
            if item.get("bank_id") == bank_id and item.get("status") == "pending":
                item["status"] = "resolved"
                item["resolution"] = resolution
                item["resolved_at"] = datetime.now(timezone.utc).isoformat()
                item["resolved_by"] = resolved_by
                break

        data["last_updated"] = datetime.now(timezone.utc).isoformat()
        self._atomic_write(self.review_queue_path, data)

    # ========== Query Methods ==========

    def get_incomplete_banks(self) -> List[str]:
        """Get list of banks that are not complete."""
        workflow = self.load_workflow_state()
        return workflow.banks_in_progress + workflow.banks_pending

    def get_blocked_banks(self) -> List[str]:
        """Get list of banks that are blocked."""
        workflow = self.load_workflow_state()
        return workflow.banks_blocked

    def get_completed_banks(self) -> List[str]:
        """Get list of completed banks."""
        workflow = self.load_workflow_state()
        return workflow.banks_completed

    def get_bank_status_summary(self) -> Dict[str, int]:
        """Get summary of bank statuses."""
        workflow = self.load_workflow_state()
        return {
            "completed": len(workflow.banks_completed),
            "in_progress": len(workflow.banks_in_progress),
            "blocked": len(workflow.banks_blocked),
            "pending": len(workflow.banks_pending)
        }

    # ========== Validation ==========

    def validate_bank_state(self, state: BankState) -> List[str]:
        """
        Validate a bank state for consistency.

        Returns list of validation errors (empty if valid).
        """
        errors = []

        # Probability sanity check
        if not 0.0 <= state.current_probability <= 1.0:
            errors.append(f"Invalid probability: {state.current_probability}")

        # Check probability sum (should be ~1.0 for binary classification)
        p_pragmatist = 1.0 - state.current_probability
        if abs(state.current_probability + p_pragmatist - 1.0) > 0.02:
            errors.append("Probability sum not equal to 1.0")

        # Check stage is valid
        if state.current_stage not in STAGE_SEQUENCE:
            errors.append(f"Invalid stage: {state.current_stage}")

        # Check completed stages are in sequence
        for i, stage in enumerate(state.stages_completed):
            if stage not in STAGE_SEQUENCE:
                errors.append(f"Invalid completed stage: {stage}")

        # Check evidence counts are non-negative
        for tier, count in state.evidence_counts.items():
            if count < 0:
                errors.append(f"Negative evidence count for {tier}: {count}")

        # Confidence should be 0-100 if set
        if state.confidence is not None:
            if not 0 <= state.confidence <= 100:
                errors.append(f"Invalid confidence: {state.confidence}")

        return errors


# Convenience function for quick access
def get_state_manager(outputs_dir: Path = None) -> UnifiedStateManager:
    """Get a state manager instance."""
    if outputs_dir is None:
        outputs_dir = Path(__file__).parent.parent / "outputs"
    return UnifiedStateManager(outputs_dir)
