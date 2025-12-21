"""
CDM Research Protocol - Unified State Manager v1.1

Single source of truth for all workflow state.
Replaces disparate state management across orchestration tools.

IMPORTANT: All probabilities use 0-1 scale (not 0-100).
Legacy 0-100 values are automatically converted on load.

Features:
- Atomic writes (write to temp, rename)
- Lock file for concurrent access
- State validation on load/save
- Provenance tracking
- Schema versioning for migration support

Usage:
    from state_manager import UnifiedStateManager

    manager = UnifiedStateManager(Path("outputs"))
    state = manager.load_bank_state("deutsche-bank", phase=1)
    state.update_probability(0.65, combined_lr=2.5, evidence_count=5, stage="bayesian_1")
    manager.save_bank_state(state)
"""

import json
import os
import sys
import time
import logging
import platform
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

    def __init__(self, outputs_dir: Path, auto_sync: bool = True):
        """
        Initialize the state manager.

        Args:
            outputs_dir: Path to the outputs directory
            auto_sync: If True, auto-sync workflow state from bank states on startup
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

        # Lock configuration
        self.lock_timeout = 30  # seconds
        self.stale_lock_age = 300  # 5 minutes - Phase 7: reduced for faster recovery

        # Phase 5: Auto-sync workflow state from bank states on startup
        if auto_sync:
            self._auto_sync_if_needed()

    def _auto_sync_if_needed(self) -> None:
        """
        Phase 5: Sync workflow state if it appears stale or empty.

        Automatically detects if workflow state needs refresh by checking:
        1. If no banks are tracked (fresh start or stale state)
        2. If last update was > 1 hour ago (stale state)
        """
        try:
            workflow = self.load_workflow_state()
        except Exception:
            workflow = None

        if not workflow:
            # No workflow state exists - create fresh
            logger.info("No workflow state found, scanning for existing bank states...")
            self._scan_and_sync_all_phases()
            return

        # Check if workflow state tracks any banks
        total_tracked = (len(workflow.banks_completed) + len(workflow.banks_in_progress) +
                         len(workflow.banks_pending) + len(workflow.banks_blocked))

        if total_tracked == 0:
            # No banks tracked - scan for existing bank states
            logger.info("Workflow state empty, scanning for existing bank states...")
            self._scan_and_sync_all_phases()
        else:
            # Check for stale state (last update > 1 hour ago)
            try:
                last = datetime.fromisoformat(workflow.last_updated.replace('Z', '+00:00'))
                age = (datetime.now(timezone.utc) - last).total_seconds()
                if age > 3600:  # 1 hour
                    logger.info(f"Workflow state is stale ({age/3600:.1f}h old), syncing from bank states...")
                    self._scan_and_sync_all_phases()
            except Exception as e:
                logger.debug(f"Could not check workflow state age: {e}")

    def _scan_and_sync_all_phases(self) -> None:
        """Phase 5: Scan all phase directories and sync workflow state."""
        for phase in range(1, 10):
            try:
                self.sync_workflow_state_from_bank_states(phase)
            except Exception as e:
                logger.debug(f"Could not sync phase {phase}: {e}")

    def _get_phase_name(self, phase: int) -> Optional[str]:
        """
        Get the canonical phase name from bank manifest (Issue #8 fix).

        Args:
            phase: Phase number

        Returns:
            Phase name (e.g., "european-tier1") or None if not found
        """
        try:
            manifest_path = self.outputs_dir.parent / "config" / "bank-manifest.json"
            if manifest_path.exists():
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    manifest = json.load(f)

                phase_key = f"phase_{phase}"
                phase_info = manifest.get("phase_summary", {}).get(phase_key, {})
                name = phase_info.get("name", "")
                if name:
                    # Convert "European Tier 1" to "european-tier1"
                    return name.lower().replace(" ", "-")
        except Exception as e:
            logger.debug(f"Could not load phase name from manifest: {e}")

        return None

    def _get_bank_dir(self, bank_id: str, phase: int) -> Path:
        """Get the directory for a bank's outputs."""
        phase_name = self._get_phase_name(phase)
        if phase_name:
            return self.outputs_dir / f"phase-{phase}-{phase_name}" / bank_id
        return self.outputs_dir / f"phase-{phase}" / bank_id

    def _get_bank_status_path(self, bank_id: str, phase: int) -> Path:
        """
        Get the path to a bank's status.json file.

        Uses deterministic path resolution via bank manifest (Issue #8 fix).
        """
        # First try the canonical name from manifest
        phase_name = self._get_phase_name(phase)

        if phase_name:
            bank_dir = self.outputs_dir / f"phase-{phase}-{phase_name}" / bank_id
        else:
            # Fall back to glob if manifest not available
            phase_dirs = sorted(self.outputs_dir.glob(f"phase-{phase}-*"))
            if phase_dirs:
                bank_dir = phase_dirs[0] / bank_id
            else:
                # Create default phase directory
                bank_dir = self.outputs_dir / f"phase-{phase}" / bank_id

        bank_dir.mkdir(parents=True, exist_ok=True)
        return bank_dir / "status.json"

    def _process_exists(self, pid: int) -> bool:
        """
        Check if a process with given PID exists.

        Args:
            pid: Process ID to check

        Returns:
            True if process exists, False otherwise
        """
        if WINDOWS:
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
                handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
                if handle:
                    kernel32.CloseHandle(handle)
                    return True
                return False
            except Exception:
                return True  # Assume exists if we can't check
        else:
            try:
                os.kill(pid, 0)
                return True
            except OSError:
                return False

    def _handle_stale_lock(self, lock_path: Path) -> bool:
        """
        Detect and handle stale locks using multiple signals.

        Args:
            lock_path: Path to the lock file

        Returns:
            True if stale lock was removed, False otherwise
        """
        if not lock_path.exists():
            return False

        try:
            # Try to read lock info
            lock_content = lock_path.read_text(encoding='utf-8')
            try:
                lock_info = json.loads(lock_content)
            except json.JSONDecodeError:
                # Corrupted lock file - safe to remove
                logger.warning(f"Removing corrupted lock file: {lock_path}")
                lock_path.unlink()
                return True

            # Check 1: Is the process still running?
            lock_pid = lock_info.get('pid')
            if lock_pid and not self._process_exists(lock_pid):
                logger.warning(f"Removing stale lock - PID {lock_pid} no longer exists: {lock_path}")
                lock_path.unlink()
                return True

            # Check 2: Is lock older than maximum allowed time?
            acquired_str = lock_info.get('acquired')
            if acquired_str:
                try:
                    acquired = datetime.fromisoformat(acquired_str.replace('Z', '+00:00'))
                    age_seconds = (datetime.now(timezone.utc) - acquired).total_seconds()

                    if age_seconds > self.stale_lock_age:
                        logger.warning(f"Removing stale lock - held for {age_seconds:.0f}s: {lock_path}")
                        lock_path.unlink()
                        return True
                except (ValueError, TypeError):
                    pass

            return False

        except OSError as e:
            logger.debug(f"Error checking stale lock: {e}")
            return False

    @contextmanager
    def _file_lock(self, path: Path):
        """
        Context manager for file locking with proper lock held during operations.

        Uses exclusive lock file creation with PID/timestamp tracking.
        The lock is held for the duration of the context.

        Args:
            path: Path to the file being locked (lock file is path.lock)

        Raises:
            StateLockError: If lock cannot be acquired within timeout
        """
        lock_path = path.with_suffix('.lock')
        fd = None
        retries = 0

        try:
            start_time = time.time()
            while True:
                try:
                    # Create lock file exclusively
                    fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_RDWR)

                    # Write lock info for debugging and stale detection
                    lock_info = json.dumps({
                        "pid": os.getpid(),
                        "acquired": datetime.now(timezone.utc).isoformat(),
                        "host": platform.node(),
                        "file": str(path),
                    })
                    os.write(fd, lock_info.encode('utf-8'))

                    # Log contention if we had to retry
                    if retries > 0:
                        elapsed = time.time() - start_time
                        logger.debug(f"Lock acquired after {retries} retries ({elapsed:.2f}s): {lock_path}")

                    break

                except FileExistsError:
                    # Lock exists - check if stale
                    if self._handle_stale_lock(lock_path):
                        continue  # Stale lock removed, try again

                    # Check timeout
                    if time.time() - start_time > self.lock_timeout:
                        raise StateLockError(
                            f"Timeout ({self.lock_timeout}s) waiting for lock on {path}"
                        )

                    retries += 1
                    time.sleep(0.1)

                except OSError as e:
                    if time.time() - start_time > self.lock_timeout:
                        raise StateLockError(f"Error acquiring lock on {path}: {e}")
                    time.sleep(0.1)

            yield

        finally:
            # Release lock
            if fd is not None:
                try:
                    os.close(fd)
                except OSError:
                    pass

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

    def save_bank_state(self, state: BankState, validate: bool = True,
                         strict: bool = False) -> None:
        """
        Save bank state with atomic write.

        Args:
            state: BankState to save
            validate: If True, run validation and log warnings (default True)
            strict: If True, raise exception on validation errors (default False)
        """
        # Validate state before saving (Issue #6 fix)
        if validate:
            errors = self.validate_bank_state(state)
            if errors:
                if strict:
                    # Phase 6: Strict mode - fail on validation errors
                    raise StateValidationError(
                        f"Validation failed for {state.bank_id}: {errors}"
                    )
                else:
                    logger.warning(f"Validation warnings for {state.bank_id}: {errors}")

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
        """
        Set a bank as blocked at a checkpoint.

        Uses proper locking to prevent race conditions when multiple
        processes update state simultaneously.
        """
        bank_path = self._get_bank_status_path(bank_id, phase)

        # Lock and update bank state
        with self._file_lock(bank_path):
            state = self.load_bank_state(bank_id, phase)
            if state is None:
                raise ValueError(f"No state found for {bank_id}")

            state.set_blocked(checkpoint, reason)
            self.save_bank_state(state)

        # Lock and update workflow state (separate lock to avoid deadlock)
        with self._file_lock(self.workflow_state_path):
            workflow = self.load_workflow_state()
            workflow.mark_bank_blocked(bank_id)
            self.save_workflow_state(workflow)

    def clear_bank_block(self, bank_id: str, phase: int) -> None:
        """Clear the blocked status for a bank and sync workflow state."""
        state = self.load_bank_state(bank_id, phase)
        if state is None:
            raise ValueError(f"No state found for {bank_id}")

        state.clear_block()
        self.save_bank_state(state)

        # Sync workflow state to reflect unblocked status
        with self._file_lock(self.workflow_state_path):
            workflow = self.load_workflow_state()
            workflow.mark_bank_unblocked(bank_id)
            self.save_workflow_state(workflow)

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
        """
        Log a checkpoint event with atomic read-modify-write.

        Uses file locking to prevent concurrent appends from losing data.
        """
        with self._file_lock(self.checkpoint_log_path):
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
            summary["last_updated"] = datetime.now(timezone.utc).isoformat()
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
        """
        Log an error event with atomic read-modify-write.

        Uses file locking to prevent concurrent appends from losing data.
        """
        with self._file_lock(self.error_log_path):
            data = self._load_json(self.error_log_path, {"errors": [], "summary": {}})

            data["errors"].append(event.to_dict())

            # Update summary
            summary = data.get("summary", {})
            summary["total_errors"] = len(data["errors"])
            summary["last_updated"] = datetime.now(timezone.utc).isoformat()
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

    def clear_errors(self, bank_id: str, phase: Optional[int] = None) -> None:
        """
        Clear errors for a bank (Issue #10 fix).

        Clears errors from both the global error log AND the bank state.

        Args:
            bank_id: Bank identifier
            phase: Optional phase number. If provided, also clears bank state errors.
        """
        # Clear from global error log
        with self._file_lock(self.error_log_path):
            data = self._load_json(self.error_log_path, {"errors": [], "summary": {}})

            data["errors"] = [
                e for e in data["errors"]
                if e.get("bank_id") != bank_id
            ]

            self._atomic_write(self.error_log_path, data)

        # Also clear from bank state if phase provided
        if phase is not None:
            try:
                state = self.load_bank_state(bank_id, phase)
                if state and state.errors:
                    state.errors = []
                    self.save_bank_state(state, validate=False)
                    logger.debug(f"Cleared errors from bank state for {bank_id}")
            except Exception as e:
                logger.warning(f"Could not clear bank state errors: {e}")

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

    # ========== Authoritative Completion Methods ==========

    def is_bank_complete(self, bank_id: str, phase: int) -> bool:
        """
        AUTHORITATIVE completion check - single source of truth.

        This is the ONLY method that should be used to check if a bank
        has completed research. Uses BankState.is_complete() which checks
        completed_at timestamp or "complete" in stages_completed.

        Args:
            bank_id: Bank identifier
            phase: Phase number

        Returns:
            True if bank research is complete, False otherwise
        """
        bank_state = self.load_bank_state(bank_id, phase)
        if bank_state is None:
            return False
        return bank_state.is_complete()

    def mark_bank_complete(self, bank_id: str, phase: int) -> None:
        """
        Mark a bank as complete in BOTH BankState AND WorkflowState.

        This ensures state consistency between the authoritative per-bank
        state (status.json) and the workflow index (workflow-state.json).

        Args:
            bank_id: Bank identifier
            phase: Phase number

        Raises:
            ValueError: If no state found for bank
        """
        # Update BankState (authoritative source)
        bank_state = self.load_bank_state(bank_id, phase)
        if bank_state is None:
            raise ValueError(f"No state found for {bank_id}")

        bank_state.completed_at = datetime.now(timezone.utc).isoformat()
        bank_state.mark_stage_complete("complete")
        self.save_bank_state(bank_state)

        # Sync to WorkflowState (index/cache)
        with self._file_lock(self.workflow_state_path):
            workflow = self.load_workflow_state()
            workflow.mark_bank_completed(bank_id)
            self.save_workflow_state(workflow)

        logger.info(f"Marked {bank_id} as complete (both states synchronized)")

    def sync_workflow_state_from_bank_states(self, phase: int) -> 'WorkflowState':
        """
        Rebuild WorkflowState by scanning all BankState files.

        Use this for recovery or initialization to ensure workflow-state.json
        accurately reflects the actual per-bank status.json files.

        Args:
            phase: Phase number to sync

        Returns:
            Updated WorkflowState
        """
        # Load bank manifest for the phase
        manifest_path = self.outputs_dir.parent / "config" / "bank-manifest.json"
        banks_in_phase = []

        if manifest_path.exists():
            try:
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    manifest = json.load(f)
                banks_in_phase = [
                    b['bank_id'] for b in manifest.get('banks', [])
                    if b.get('phase') == phase
                ]
            except Exception as e:
                logger.warning(f"Could not load bank manifest: {e}")

        # Lock and rebuild workflow state
        with self._file_lock(self.workflow_state_path):
            workflow = self.load_workflow_state()

            # Clear existing lists for this rebuild
            workflow.banks_completed = []
            workflow.banks_in_progress = []
            workflow.banks_pending = []
            workflow.banks_blocked = []

            for bank_id in banks_in_phase:
                bank_state = self.load_bank_state(bank_id, phase)

                if bank_state is None:
                    workflow.banks_pending.append(bank_id)
                elif bank_state.is_complete():
                    workflow.banks_completed.append(bank_id)
                elif bank_state.is_blocked():
                    workflow.banks_blocked.append(bank_id)
                else:
                    workflow.banks_in_progress.append(bank_id)

            workflow.log_event(
                "workflow_synced",
                f"Rebuilt from {len(banks_in_phase)} bank states: "
                f"{len(workflow.banks_completed)} complete, "
                f"{len(workflow.banks_in_progress)} in progress, "
                f"{len(workflow.banks_blocked)} blocked, "
                f"{len(workflow.banks_pending)} pending"
            )

            self.save_workflow_state(workflow)

        logger.info(
            f"Synced workflow state from bank states: "
            f"{len(workflow.banks_completed)} complete, "
            f"{len(workflow.banks_in_progress)} in progress"
        )

        return workflow

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

        # Check probability history consistency
        if state.probability_history:
            last_update = state.probability_history[-1]
            if hasattr(last_update, 'posterior'):
                if abs(last_update.posterior - state.current_probability) > 0.001:
                    errors.append(
                        f"Current probability {state.current_probability:.4f} doesn't match "
                        f"last update posterior {last_update.posterior:.4f}"
                    )

        # Check stage is valid
        if state.current_stage not in STAGE_SEQUENCE:
            errors.append(f"Invalid stage: {state.current_stage}")

        # Check completed stages are in sequence
        for stage in state.stages_completed:
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

        # Check blocked state consistency
        if state.blocked_at is not None:
            if state.blocked_checkpoint is None:
                errors.append("Bank is blocked but blocked_checkpoint is None")
            if state.blocked_reason is None:
                errors.append("Bank is blocked but blocked_reason is None")

        # Check classification consistency
        if state.classification is not None:
            valid_classifications = {"ARCHITECT", "PRAGMATIST", "OBSERVER", "UNKNOWN"}
            if state.classification not in valid_classifications:
                errors.append(f"Invalid classification: {state.classification}")

        return errors


# Convenience function for quick access
def get_state_manager(outputs_dir: Path = None) -> UnifiedStateManager:
    """Get a state manager instance."""
    if outputs_dir is None:
        outputs_dir = Path(__file__).parent.parent / "outputs"
    return UnifiedStateManager(outputs_dir)
