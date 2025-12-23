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
import gzip
import hashlib
import logging
import platform
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any, Tuple
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
from config_loader import (
    get_prior_for_bank,
    get_state_validation_config,
    get_state_versioning_config,
    get_state_management_config
)

# Import shared locking utilities using direct import (avoid broken __init__.py)
import importlib.util
_file_lock_path = Path(__file__).parent / "orchestrator" / "file_lock.py"
if _file_lock_path.exists():
    _spec = importlib.util.spec_from_file_location("file_lock", _file_lock_path)
    _file_lock_module = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_file_lock_module)
    _shared_process_exists = _file_lock_module.process_exists
    _shared_file_lock = _file_lock_module.file_lock
    _shared_handle_stale_lock = _file_lock_module.handle_stale_lock
    SHARED_LOCK_AVAILABLE = True
else:
    SHARED_LOCK_AVAILABLE = False
    _shared_file_lock = None
    _shared_handle_stale_lock = None

# Import LockingService for centralized locking configuration
try:
    from locking_service import get_locking_service
    LOCKING_SERVICE_AVAILABLE = True
except ImportError:
    LOCKING_SERVICE_AVAILABLE = False
    get_locking_service = None

# Import log rotation manager
try:
    from log_rotation import notify_log_entry as _notify_log_rotation
    LOG_ROTATION_AVAILABLE = True
except ImportError:
    LOG_ROTATION_AVAILABLE = False
    def _notify_log_rotation(log_type: str, state_dir=None):
        pass  # No-op if module not available

logger = logging.getLogger(__name__)


class StateLockError(Exception):
    """Raised when state file is locked by another process."""
    pass


class StateValidationError(Exception):
    """Raised when state validation fails."""
    pass


class TransactionRollbackError(Exception):
    """Raised when transaction rollback fails."""
    pass


class PhaseResolutionError(Exception):
    """
    Raised when phase directory cannot be uniquely determined.

    This indicates ambiguous state in the outputs directory that
    requires manual resolution (e.g., duplicate phase-N-* directories
    for the same bank).

    Gap 9 fix: Fail loudly on ambiguity instead of silent fallback.
    """
    pass


class ValidationMode:
    """
    Validation mode for state operations.

    Modes:
        STRICT: Raise exception on validation errors (production default)
        WARN: Log warning but proceed with save (development/debugging)
        OFF: Disable validation entirely (emergency override only)
    """
    STRICT = "strict"
    WARN = "warn"
    OFF = "off"


def _determine_validation_mode() -> str:
    """
    Determine validation mode from environment variable or config.

    Priority:
        1. CDM_VALIDATION_MODE environment variable
        2. state_validation.mode from config/validation-rules.json
        3. Default to STRICT

    Returns:
        Validation mode string (strict, warn, or off)

    Note:
        Non-strict modes are logged as security audit events.
    """
    import os

    # Check environment variable first
    config = get_state_validation_config()
    env_var = config.get("mode_override_env_var", "CDM_VALIDATION_MODE")
    env_mode = os.environ.get(env_var, "").lower()

    effective_mode = None
    source = None

    if env_mode in (ValidationMode.STRICT, ValidationMode.WARN, ValidationMode.OFF):
        effective_mode = env_mode
        source = f"environment variable {env_var}"
    else:
        # Fall back to config file
        config_mode = config.get("mode", ValidationMode.STRICT).lower()
        if config_mode in (ValidationMode.STRICT, ValidationMode.WARN, ValidationMode.OFF):
            effective_mode = config_mode
            source = "config file"
        else:
            effective_mode = ValidationMode.STRICT
            source = "default"

    # SECURITY AUDIT: Log when using non-strict validation mode
    if effective_mode != ValidationMode.STRICT:
        severity = "disabled" if effective_mode == ValidationMode.OFF else "weakened"
        logger.warning(
            f"SECURITY AUDIT: Validation mode set to '{effective_mode}' via {source}. "
            f"Data integrity checks {severity}. This should only be used for "
            f"debugging or emergency recovery."
        )

    return effective_mode


class StateTransaction:
    """
    Transaction manager for multi-state atomic updates.

    Implements the Saga pattern with compensation:
    - Acquires all locks upfront (prevents deadlock via consistent ordering)
    - Tracks original state for rollback
    - Provides atomic commit or full rollback

    Usage:
        with manager.multi_state_transaction() as txn:
            txn.acquire_locks([bank_path, workflow_path])

            # Modify states
            bank_state.set_blocked(...)
            workflow.mark_bank_blocked(...)

            # Stage writes
            txn.stage_write(bank_path, bank_state.to_dict())
            txn.stage_write(workflow_path, workflow.to_dict())

            # Commit atomically
            txn.commit()
    """

    def __init__(self, manager: 'UnifiedStateManager'):
        self.manager = manager
        self._locks_held: List[Path] = []
        self._lock_fds: Dict[Path, int] = {}
        self._original_states: Dict[Path, dict] = {}
        self._pending_writes: Dict[Path, dict] = {}
        self._committed = False

    def acquire_locks(self, paths: List[Path]) -> None:
        """
        Acquire all locks in consistent order to prevent deadlock.

        Sorts paths alphabetically to ensure all processes acquire
        locks in the same order.

        Args:
            paths: List of file paths to lock

        Raises:
            StateLockError: If any lock cannot be acquired
        """
        # Sort for consistent ordering (prevents deadlock)
        sorted_paths = sorted(paths, key=lambda p: str(p))

        for path in sorted_paths:
            try:
                fd = self._acquire_single_lock(path)
                self._lock_fds[path] = fd
                self._locks_held.append(path)

                # Snapshot original state for rollback
                if path.exists():
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            self._original_states[path] = json.load(f)
                    except (json.JSONDecodeError, IOError):
                        pass  # No original state to restore

            except Exception as e:
                # Failed to acquire - release all held locks
                self._release_all_locks()
                raise StateLockError(f"Failed to acquire lock on {path}: {e}")

    def _acquire_single_lock(self, path: Path) -> int:
        """Acquire lock on single file, returning file descriptor."""
        lock_path = path.with_suffix('.lock')
        start_time = time.time()

        while True:
            try:
                fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_RDWR)

                lock_info = json.dumps({
                    "pid": os.getpid(),
                    "acquired": datetime.now(timezone.utc).isoformat(),
                    "host": platform.node(),
                    "file": str(path),
                    "transaction": True,  # Mark as part of transaction
                })
                os.write(fd, lock_info.encode('utf-8'))
                return fd

            except FileExistsError:
                # Use shared stale lock handler if available
                if SHARED_LOCK_AVAILABLE and _shared_handle_stale_lock is not None:
                    if _shared_handle_stale_lock(lock_path, self.manager.stale_lock_age):
                        continue  # Stale lock removed, try again
                # No stale lock handler - just wait and retry

                if time.time() - start_time > self.manager.lock_timeout:
                    raise StateLockError(f"Timeout acquiring lock: {path}")

                time.sleep(0.1)

            except OSError as e:
                if time.time() - start_time > self.manager.lock_timeout:
                    raise StateLockError(f"Error acquiring lock on {path}: {e}")
                time.sleep(0.1)

    def stage_write(self, path: Path, data: dict) -> None:
        """
        Stage a write for atomic commit.

        Args:
            path: File path to write to
            data: Data to write (will be JSON serialized)
        """
        import copy
        self._pending_writes[path] = copy.deepcopy(data)

    def commit(self) -> None:
        """
        Atomically commit all staged writes.

        If any write fails, rolls back all changes.

        Raises:
            ValueError: If transaction already committed
            TransactionRollbackError: If rollback fails after write error
        """
        if self._committed:
            raise ValueError("Transaction already committed")

        written_paths = []

        try:
            for path, data in self._pending_writes.items():
                self.manager._atomic_write(path, data)
                written_paths.append(path)

            self._committed = True
            logger.debug(f"Transaction committed: {len(written_paths)} files written")

        except Exception as e:
            logger.error(f"Transaction write failed, rolling back: {e}")
            self._rollback(written_paths)
            raise

        finally:
            self._release_all_locks()

    def commit_with_versioning(self, triggers: Dict[Path, str] = None) -> None:
        """
        Commit all staged writes with automatic versioning.

        Creates version backups of all modified status.json files BEFORE
        committing, enabling rollback of entire transactions via the
        versioning system.

        Args:
            triggers: Optional mapping of path -> trigger name for version metadata
                     e.g., {bank_path: "complete", workflow_path: "workflow_update"}

        Raises:
            ValueError: If transaction already committed
            TransactionRollbackError: If rollback fails after write error
        """
        if self._committed:
            raise ValueError("Transaction already committed")

        triggers = triggers or {}
        versioned_paths = []

        try:
            # Step 1: Create version backups for all existing status.json files
            versioning_config = get_state_versioning_config()
            if versioning_config.get('enabled', True):
                for path in self._pending_writes.keys():
                    if path.exists() and path.name == 'status.json':
                        trigger = triggers.get(path, 'transaction')
                        try:
                            self.manager._create_version_backup(path, trigger=trigger)
                            versioned_paths.append(path)
                        except Exception as e:
                            logger.warning(f"Could not create version backup for {path}: {e}")

            # Step 2: Perform normal commit
            self.commit()

            logger.debug(
                f"Transaction committed with versioning: "
                f"{len(self._pending_writes)} files, {len(versioned_paths)} versions"
            )

        except Exception as e:
            # Versions were created before failure - they serve as recovery point
            logger.error(f"Transaction failed after creating {len(versioned_paths)} versions: {e}")
            raise

    def _rollback(self, written_paths: List[Path]) -> None:
        """Restore original state for all written paths."""
        rollback_errors = []

        for path in written_paths:
            if path in self._original_states:
                try:
                    self.manager._atomic_write(path, self._original_states[path])
                    logger.debug(f"Rolled back: {path}")
                except Exception as e:
                    rollback_errors.append(f"{path}: {e}")
            else:
                # File was new - delete it
                try:
                    if path.exists():
                        path.unlink()
                        logger.debug(f"Removed new file: {path}")
                except Exception as e:
                    rollback_errors.append(f"delete {path}: {e}")

        if rollback_errors:
            raise TransactionRollbackError(
                f"Rollback failed for: {'; '.join(rollback_errors)}"
            )

    def _release_all_locks(self) -> None:
        """Release all held locks."""
        for path in reversed(self._locks_held):
            fd = self._lock_fds.get(path)
            lock_path = path.with_suffix('.lock')

            if fd is not None:
                try:
                    os.close(fd)
                except OSError:
                    pass

            try:
                lock_path.unlink()
            except (FileNotFoundError, OSError):
                pass

        self._locks_held.clear()
        self._lock_fds.clear()


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

        # Lock configuration from config file (Gap 10 fix)
        self._timing_config = self._load_timing_config()
        self.lock_timeout = self._timing_config.get('lock_timeout_seconds', 30)
        self.stale_lock_age = self._timing_config.get('stale_lock_age_seconds', 300)
        self.workflow_staleness_hours = self._timing_config.get('workflow_staleness_hours', 1)

        # Phase scan range from config
        phase_range = self._timing_config.get('phase_scan_range', {'min': 1, 'max': 9})
        self.phase_min = phase_range.get('min', 1)
        self.phase_max = phase_range.get('max', 9)

        # Phase 5: Auto-sync workflow state from bank states on startup
        if auto_sync:
            self._auto_sync_if_needed()

        # Phase 5 Gap 7: Check for ambiguous phase directories on startup
        self._check_phase_ambiguity_startup()

    def _check_phase_ambiguity_startup(self) -> None:
        """
        Check for ambiguous phase directories at startup and log warnings.

        This helps catch configuration issues early rather than failing
        when a specific bank is accessed.
        """
        phase_config = self._timing_config.get('phase_resolution', {})
        if not phase_config.get('warn_on_ambiguity', True):
            return

        ambiguities = []
        for phase in range(self.phase_min, self.phase_max + 1):
            phase_dirs = list(self.outputs_dir.glob(f"phase-{phase}-*"))
            if len(phase_dirs) > 1:
                # Check each bank for presence in multiple directories
                all_banks = {}
                for pdir in phase_dirs:
                    if pdir.is_dir():
                        for bank_dir in pdir.iterdir():
                            if bank_dir.is_dir() and (bank_dir / "status.json").exists():
                                bank_name = bank_dir.name
                                if bank_name not in all_banks:
                                    all_banks[bank_name] = []
                                all_banks[bank_name].append(pdir.name)

                # Report banks in multiple directories
                for bank, dirs in all_banks.items():
                    if len(dirs) > 1:
                        ambiguities.append(
                            f"AMBIGUITY: Bank '{bank}' exists in multiple phase-{phase} "
                            f"directories: {dirs}"
                        )

        if ambiguities:
            for warning in ambiguities:
                logger.warning(warning)
            if not phase_config.get('legacy_fallback', False):
                logger.warning(
                    f"Found {len(ambiguities)} ambiguous bank location(s). "
                    f"Set state_management.phase_resolution.legacy_fallback=true to "
                    f"use first match instead of failing."
                )

    def _load_timing_config(self) -> Dict[str, Any]:
        """Load timing configuration from decision-thresholds.json (Gap 10 fix)."""
        try:
            return get_state_management_config()
        except Exception as e:
            logger.warning(f"Could not load timing config: {e}. Using defaults.")
            return {
                'lock_timeout_seconds': 30,
                'stale_lock_age_seconds': 300,
                'workflow_staleness_hours': 1,
                'phase_scan_range': {'min': 1, 'max': 9}
            }

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
            # Check for stale state (configurable staleness threshold - Gap 10 fix)
            try:
                last = datetime.fromisoformat(workflow.last_updated.replace('Z', '+00:00'))
                age = (datetime.now(timezone.utc) - last).total_seconds()
                staleness_seconds = self.workflow_staleness_hours * 3600
                if age > staleness_seconds:
                    logger.info(f"Workflow state is stale ({age/3600:.1f}h old), syncing from bank states...")
                    self._scan_and_sync_all_phases()
            except Exception as e:
                logger.debug(f"Could not check workflow state age: {e}")

    def _scan_and_sync_all_phases(self) -> None:
        """Phase 5: Scan all phase directories and sync workflow state."""
        for phase in range(self.phase_min, self.phase_max + 1):
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
                    # Note: Remove space but keep "Tier1" as single unit
                    normalized = name.lower().replace(" ", "-")
                    # Fix: tier-1 -> tier1 to match canonical naming
                    return normalized.replace("tier-1", "tier1").replace("tier-2", "tier2")
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

        Uses deterministic path resolution via bank manifest.
        Fails loudly on ambiguity (Gap 9 fix).

        Args:
            bank_id: Bank identifier
            phase: Phase number

        Returns:
            Path to status.json file

        Raises:
            PhaseResolutionError: If multiple phase directories exist for
                                  the same phase number and manifest lookup fails
        """
        # First try the canonical name from manifest
        phase_name = self._get_phase_name(phase)

        if phase_name:
            # Manifest-based resolution (preferred)
            bank_dir = self.outputs_dir / f"phase-{phase}-{phase_name}" / bank_id
        else:
            # Fall back to glob if manifest not available
            phase_dirs = sorted(self.outputs_dir.glob(f"phase-{phase}-*"))

            if len(phase_dirs) == 0:
                # No existing phase directory - create default
                bank_dir = self.outputs_dir / f"phase-{phase}" / bank_id
            elif len(phase_dirs) == 1:
                # Single match - use it
                bank_dir = phase_dirs[0] / bank_id
            else:
                # AMBIGUITY DETECTED - fail loudly (Gap 9 fix)
                # Check if bank exists in any of them
                matches = [d for d in phase_dirs if (d / bank_id).exists()]

                if len(matches) == 0:
                    # Bank doesn't exist in any - use first directory
                    bank_dir = phase_dirs[0] / bank_id
                elif len(matches) == 1:
                    # Bank exists in exactly one - use that
                    bank_dir = matches[0] / bank_id
                else:
                    # Bank exists in multiple directories - ambiguous!
                    # Check for legacy fallback mode
                    phase_config = self._timing_config.get('phase_resolution', {})
                    if phase_config.get('legacy_fallback', False):
                        logger.warning(
                            f"AMBIGUITY: Bank '{bank_id}' exists in multiple phase-{phase} "
                            f"directories: {[d.name for d in matches]}. Using first match "
                            f"(legacy mode). Set phase_resolution.legacy_fallback=false to "
                            f"enable strict mode."
                        )
                        bank_dir = matches[0] / bank_id
                    else:
                        raise PhaseResolutionError(
                            f"Ambiguous phase {phase} resolution for {bank_id}. "
                            f"Bank found in multiple directories: {[d.name for d in matches]}. "
                            f"Fix bank-manifest.json or remove duplicate directories."
                        )

        bank_dir.mkdir(parents=True, exist_ok=True)
        return bank_dir / "status.json"

    # NOTE: _process_exists, _process_exists_windows, and _handle_stale_lock
    # have been removed - these are now handled by the shared file_lock module
    # in tools/orchestrator/file_lock.py via the LockingService.

    @contextmanager
    def _file_lock(self, path: Path, operation: str = None):
        """
        Context manager for file locking - delegates to centralized LockingService.

        Uses the shared file locking infrastructure for consistent lock handling
        across all components. Falls back to direct file_lock if LockingService
        is not available.

        Args:
            path: Path to the file being locked (lock file is path.lock)
            operation: Optional description for logging

        Raises:
            StateLockError: If lock cannot be acquired within timeout
        """
        try:
            # Prefer LockingService for centralized configuration
            if LOCKING_SERVICE_AVAILABLE and get_locking_service is not None:
                with get_locking_service().lock_file(path, operation=operation):
                    yield
            # Fall back to shared file_lock
            elif SHARED_LOCK_AVAILABLE and _shared_file_lock is not None:
                with _shared_file_lock(
                    path,
                    timeout=self.lock_timeout,
                    stale_lock_age=self.stale_lock_age,
                    operation=operation
                ):
                    yield
            else:
                # No locking available - proceed without lock (log warning)
                logger.warning(f"No locking mechanism available - proceeding without lock: {path}")
                yield
        except Exception as e:
            # Convert locking exceptions to StateLockError for consistency
            if "timeout" in str(e).lower() or "Timeout" in str(e):
                raise StateLockError(f"Timeout waiting for lock on {path}: {e}")
            raise StateLockError(f"Error acquiring lock on {path}: {e}")

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

    @contextmanager
    def multi_state_transaction(self):
        """
        Context manager for multi-state atomic updates.

        Provides transactional semantics with rollback on failure.
        All locks are acquired upfront to prevent deadlocks.

        Usage:
            with manager.multi_state_transaction() as txn:
                txn.acquire_locks([bank_path, workflow_path])

                # Load and modify states
                bank_state = self.load_bank_state(bank_id, phase)
                bank_state.set_blocked(checkpoint, reason)

                workflow = self.load_workflow_state()
                workflow.mark_bank_blocked(bank_id)

                # Stage writes
                txn.stage_write(bank_path, bank_state.to_dict())
                txn.stage_write(workflow_path, workflow.to_dict())

                # Commit atomically
                txn.commit()

        Yields:
            StateTransaction: Transaction object with acquire_locks,
                             stage_write, and commit methods
        """
        txn = StateTransaction(self)
        try:
            yield txn
        except Exception:
            # Transaction will auto-release locks
            raise

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
                         strict: bool = None) -> None:
        """
        Save bank state with atomic write.

        Validation mode is determined by (in priority order):
        1. CDM_VALIDATION_MODE environment variable
        2. state_validation.mode from config/validation-rules.json
        3. Default to STRICT

        Args:
            state: BankState to save
            validate: If True, run validation (default True)
            strict: DEPRECATED - use config or env var instead.
                   If explicitly True/False, overrides config for backwards compat.
        """
        # Determine validation mode from config (Gap 5 fix)
        validation_mode = _determine_validation_mode()

        # Handle legacy strict parameter for backwards compatibility
        if strict is True:
            validation_mode = ValidationMode.STRICT
        elif strict is False:
            validation_mode = ValidationMode.WARN

        # Skip validation entirely if mode is OFF
        if validation_mode == ValidationMode.OFF:
            validate = False

        # Validate state before saving
        if validate:
            errors = self.validate_bank_state(state)
            if errors:
                if validation_mode == ValidationMode.STRICT:
                    # STRICT mode: fail on validation errors (production default)
                    raise StateValidationError(
                        f"Validation failed for {state.bank_id}: {errors}"
                    )
                else:
                    # WARN mode: log warning but proceed
                    logger.warning(f"Validation warnings for {state.bank_id}: {errors}")

        path = self._get_bank_status_path(state.bank_id, state.phase)

        # Update timestamp
        state.last_updated = datetime.now(timezone.utc).isoformat()

        # Atomic write
        self._atomic_write(path, state.to_dict())
        logger.debug(f"Saved state for {state.bank_id}")

    # ========== State Versioning (Gap 6 fix) ==========

    def _get_versions_dir(self, bank_id: str, phase: int) -> Path:
        """Get the versions directory for a bank's state files."""
        bank_dir = self._get_bank_dir(bank_id, phase)
        config = get_state_versioning_config()
        version_dir_name = config.get("version_directory", "versions")
        return bank_dir / version_dir_name

    def _create_version_backup(
        self,
        state_path: Path,
        trigger: str = "manual"
    ) -> Optional[Path]:
        """
        Create a version backup of a state file.

        Args:
            state_path: Path to the state file to backup
            trigger: What triggered this backup (stage_complete, probability_update, etc.)

        Returns:
            Path to the version file, or None if versioning disabled/failed
        """
        config = get_state_versioning_config()

        if not config.get("enabled", True):
            return None

        if not state_path.exists():
            return None

        try:
            # Read current state
            with open(state_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Add version metadata
            content_str = json.dumps(data, sort_keys=True)
            checksum = hashlib.sha256(content_str.encode()).hexdigest()[:16]

            # Get version number (next sequential)
            versions_dir = state_path.parent / config.get("version_directory", "versions")
            versions_dir.mkdir(parents=True, exist_ok=True)

            existing = list(versions_dir.glob(f"{state_path.stem}.*.json*"))
            version_num = len(existing) + 1

            # Create version filename
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            version_name = f"{state_path.stem}.{version_num:03d}.{timestamp}.json"

            # Add version metadata to the backup
            data["_version_meta"] = {
                "version": version_num,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "trigger": trigger,
                "checksum": checksum,
                "original_path": str(state_path)
            }

            # Write version (optionally compressed)
            if config.get("compress_old_versions", True) and version_num > 1:
                version_path = versions_dir / (version_name + ".gz")
                with gzip.open(version_path, 'wt', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
            else:
                version_path = versions_dir / version_name
                with open(version_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)

            # Cleanup old versions if exceeding max
            self._cleanup_old_versions(versions_dir, state_path.stem, config.get("max_versions", 5))

            logger.debug(f"Created version backup: {version_path.name} (trigger: {trigger})")
            return version_path

        except Exception as e:
            logger.warning(f"Failed to create version backup for {state_path}: {e}")
            return None

    def _cleanup_old_versions(self, versions_dir: Path, base_name: str, max_versions: int) -> int:
        """
        Remove old versions exceeding the max limit.

        Args:
            versions_dir: Directory containing version files
            base_name: Base name of the state file (e.g., "status")
            max_versions: Maximum versions to keep

        Returns:
            Number of versions deleted
        """
        versions = list(versions_dir.glob(f"{base_name}.*"))
        versions.sort(key=lambda p: p.stat().st_mtime)

        deleted = 0
        while len(versions) > max_versions:
            oldest = versions.pop(0)
            try:
                oldest.unlink()
                logger.debug(f"Deleted old version: {oldest.name}")
                deleted += 1
            except OSError as e:
                logger.warning(f"Could not delete old version {oldest}: {e}")

        return deleted

    def get_state_versions(self, bank_id: str, phase: int) -> List[Dict[str, Any]]:
        """
        List available state versions for a bank.

        Args:
            bank_id: Bank identifier
            phase: Phase number

        Returns:
            List of version info dicts, sorted newest first
        """
        versions_dir = self._get_versions_dir(bank_id, phase)

        if not versions_dir.exists():
            return []

        versions = []
        for path in versions_dir.glob("status.*"):
            try:
                # Read version metadata
                if path.suffix == '.gz':
                    with gzip.open(path, 'rt', encoding='utf-8') as f:
                        data = json.load(f)
                else:
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                meta = data.get("_version_meta", {})
                versions.append({
                    "path": str(path),
                    "filename": path.name,
                    "version": meta.get("version", 0),
                    "created_at": meta.get("created_at"),
                    "trigger": meta.get("trigger"),
                    "checksum": meta.get("checksum"),
                    "size_bytes": path.stat().st_size,
                    "compressed": path.suffix == '.gz'
                })
            except Exception as e:
                logger.warning(f"Could not read version {path}: {e}")

        # Sort by version number descending
        versions.sort(key=lambda v: v.get("version", 0), reverse=True)
        return versions

    def rollback_bank_state(
        self,
        bank_id: str,
        phase: int,
        version: int = None,
        create_backup: bool = True
    ) -> Optional[BankState]:
        """
        Rollback bank state to a previous version.

        Args:
            bank_id: Bank identifier
            phase: Phase number
            version: Version number to restore (default: latest version before current)
            create_backup: If True, backup current state before rollback

        Returns:
            Restored BankState, or None if rollback failed

        Raises:
            ValueError: If version not found
        """
        versions = self.get_state_versions(bank_id, phase)

        if not versions:
            raise ValueError(f"No versions available for {bank_id} phase {phase}")

        # Find the requested version
        if version is None:
            # Default to the most recent version
            target = versions[0]
        else:
            target = next((v for v in versions if v["version"] == version), None)
            if target is None:
                available = [v["version"] for v in versions]
                raise ValueError(f"Version {version} not found. Available: {available}")

        # Backup current state before rollback
        if create_backup:
            state_path = self._get_bank_status_path(bank_id, phase)
            self._create_version_backup(state_path, trigger="pre_rollback")

        # Restore the version
        try:
            version_path = Path(target["path"])

            if version_path.suffix == '.gz':
                with gzip.open(version_path, 'rt', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                with open(version_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

            # Remove version metadata from restored state
            data.pop("_version_meta", None)

            # Save as current state
            state = BankState.from_dict(data)
            state.log_event("rollback", f"Restored from version {target['version']}")
            self.save_bank_state(state, validate=False)

            logger.info(f"Rolled back {bank_id} to version {target['version']}")
            return state

        except Exception as e:
            logger.error(f"Rollback failed for {bank_id}: {e}")
            raise

    def save_bank_state_versioned(
        self,
        state: BankState,
        trigger: str = "manual",
        validate: bool = True
    ) -> None:
        """
        Save bank state with automatic version backup.

        Use this instead of save_bank_state when you want to
        create a version backup before the save.

        Args:
            state: BankState to save
            trigger: What triggered this save (for version metadata)
            validate: If True, run validation
        """
        state_path = self._get_bank_status_path(state.bank_id, state.phase)

        # Create version backup of current state if it exists
        if state_path.exists():
            self._create_version_backup(state_path, trigger=trigger)

        # Save the new state
        self.save_bank_state(state, validate=validate)

    def create_bank_state(self, bank_id: str, bank_name: str, phase: int,
                          prior_probability: Optional[float] = None,
                          execution_tier: str = "B") -> BankState:
        """
        Create a new bank state with calculated prior from bank-manifest.json.

        Args:
            bank_id: Bank identifier
            bank_name: Bank display name
            phase: Phase number
            prior_probability: Optional explicit prior (if None, calculated from manifest)
            execution_tier: A, B, or C

        Returns:
            New BankState with adjusted prior based on bank metadata
        """
        # Calculate prior from manifest if not explicitly provided
        if prior_probability is None:
            prior_probability = get_prior_for_bank(bank_id)
            logger.info(f"Using calculated prior {prior_probability*100:.1f}% for {bank_id} from manifest")

        state = BankState(
            bank_id=bank_id,
            bank_name=bank_name,
            phase=phase,
            prior_probability=prior_probability,
            current_probability=prior_probability,
            execution_tier=execution_tier
        )

        # Initialize stage timing for the initial stage
        state.start_stage(state.current_stage)

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
        # CRITICAL: Use start_stage() to initialize stage timing for timeout detection
        next_stage = state.get_next_stage()
        if next_stage:
            state.start_stage(next_stage)

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

        Uses StateTransaction for atomic update of both BankState and
        WorkflowState. If either update fails, both are rolled back.
        """
        bank_path = self._get_bank_status_path(bank_id, phase)

        with self.multi_state_transaction() as txn:
            # Acquire both locks upfront (prevents race conditions)
            txn.acquire_locks([bank_path, self.workflow_state_path])

            # Load and modify bank state
            state = self.load_bank_state(bank_id, phase)
            if state is None:
                raise ValueError(f"No state found for {bank_id}")

            state.set_blocked(checkpoint, reason)
            state.last_updated = datetime.now(timezone.utc).isoformat()

            # Load and modify workflow state
            workflow = self.load_workflow_state()
            workflow.mark_bank_blocked(bank_id)
            workflow.last_updated = datetime.now(timezone.utc).isoformat()

            # Stage both writes
            txn.stage_write(bank_path, state.to_dict())
            txn.stage_write(self.workflow_state_path, workflow.to_dict())

            # Atomic commit (rolls back on failure)
            txn.commit()

        logger.debug(f"Blocked {bank_id} at {checkpoint}: {reason}")

    def clear_bank_block(self, bank_id: str, phase: int) -> None:
        """
        Clear the blocked status for a bank and sync workflow state.

        Uses StateTransaction for atomic update of both BankState and
        WorkflowState. If either update fails, both are rolled back.
        """
        bank_path = self._get_bank_status_path(bank_id, phase)

        with self.multi_state_transaction() as txn:
            # Acquire both locks upfront
            txn.acquire_locks([bank_path, self.workflow_state_path])

            # Load and modify bank state
            state = self.load_bank_state(bank_id, phase)
            if state is None:
                raise ValueError(f"No state found for {bank_id}")

            state.clear_block()
            state.last_updated = datetime.now(timezone.utc).isoformat()

            # Load and modify workflow state
            workflow = self.load_workflow_state()
            workflow.mark_bank_unblocked(bank_id)
            workflow.last_updated = datetime.now(timezone.utc).isoformat()

            # Stage both writes
            txn.stage_write(bank_path, state.to_dict())
            txn.stage_write(self.workflow_state_path, workflow.to_dict())

            # Atomic commit
            txn.commit()

        logger.debug(f"Unblocked {bank_id}")

    def check_and_handle_timeouts(self, phase: int,
                                   stage_timeouts: Dict[str, int] = None,
                                   default_timeout: int = 30) -> List[Dict[str, Any]]:
        """
        Check all in-progress banks for stage timeouts and auto-block if exceeded.

        Args:
            phase: Phase number to check
            stage_timeouts: Dict mapping stage name to timeout in minutes
            default_timeout: Default timeout if stage not in dict (30 min)

        Returns:
            List of dicts describing timed-out banks that were blocked
        """
        timed_out = []

        # Get all in-progress banks
        workflow = self.load_workflow_state()
        for bank_id in workflow.banks_in_progress:
            try:
                state = self.load_bank_state(bank_id, phase)
                if not state:
                    continue

                # Skip if already blocked or complete
                if state.is_blocked() or state.current_stage == "complete":
                    continue

                # Get timeout for this stage
                timeout = default_timeout
                if stage_timeouts and state.current_stage in stage_timeouts:
                    timeout = stage_timeouts[state.current_stage]

                # Check if timed out
                if state.is_stage_timed_out(timeout):
                    elapsed = state.get_stage_elapsed_minutes() or 0
                    reason = f"Stage '{state.current_stage}' exceeded {timeout} minute timeout (elapsed: {elapsed:.1f} min)"

                    # Block the bank
                    self.set_bank_blocked(
                        bank_id=bank_id,
                        phase=phase,
                        checkpoint=f"timeout_{state.current_stage}",
                        reason=reason
                    )

                    timed_out.append({
                        "bank_id": bank_id,
                        "stage": state.current_stage,
                        "timeout_minutes": timeout,
                        "elapsed_minutes": elapsed,
                        "reason": reason
                    })

                    logger.warning(f"Bank {bank_id} timed out: {reason}")

            except Exception as e:
                logger.error(f"Error checking timeout for {bank_id}: {e}")

        return timed_out

    def get_stage_timeouts_from_config(self) -> Tuple[Dict[str, int], int]:
        """Load stage timeout configuration from decision-thresholds.json."""
        try:
            config_path = self.outputs_dir.parent / "config" / "decision-thresholds.json"
            if config_path.exists():
                data = json.loads(config_path.read_text(encoding='utf-8'))
                timeouts_config = data.get('stage_timeouts', {})
                return (
                    timeouts_config.get('per_stage', {}),
                    timeouts_config.get('default_timeout', 30)
                )
        except Exception as e:
            logger.warning(f"Could not load stage timeouts from config: {e}")
        return ({}, 30)

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

    def log_checkpoint(self, event: CheckpointEvent) -> bool:
        """
        Log a checkpoint event with atomic read-modify-write.

        Uses file locking to prevent concurrent appends from losing data.
        Triggers rotation check after write to prevent unbounded growth.
        Includes duplicate detection via checkpoint_id+bank_id (Gap 7 fix).

        Returns:
            True if logged, False if duplicate detected
        """
        with self._file_lock(self.checkpoint_log_path):
            data = self._load_json(self.checkpoint_log_path, {"checkpoints": [], "summary": {}})

            # Check for duplicate checkpoint (same checkpoint_id + bank_id)
            for existing in data["checkpoints"]:
                if (existing.get("checkpoint_id") == event.checkpoint_id and
                    existing.get("bank_id") == event.bank_id):
                    logger.debug(
                        f"Duplicate checkpoint detected: {event.checkpoint_id} for {event.bank_id}"
                    )
                    return False

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

        # Notify log rotation manager (triggers check every N entries)
        _notify_log_rotation("checkpoint_log", self.state_dir)
        return True

    def get_checkpoints_for_bank(self, bank_id: str) -> List[CheckpointEvent]:
        """Get all checkpoint events for a bank."""
        data = self._load_json(self.checkpoint_log_path, {"checkpoints": []})
        return [
            CheckpointEvent.from_dict(c)
            for c in data["checkpoints"]
            if c.get("bank_id") == bank_id
        ]

    # ========== Error Logging ==========

    def log_error(self, event: ErrorEvent) -> bool:
        """
        Log an error event with atomic read-modify-write.

        Uses file locking to prevent concurrent appends from losing data.
        Triggers rotation check after write to prevent unbounded growth.
        Includes duplicate detection for same error within 60s (Gap 7 fix).

        Returns:
            True if logged, False if duplicate detected
        """
        with self._file_lock(self.error_log_path):
            data = self._load_json(self.error_log_path, {"errors": [], "summary": {}})

            # Check for duplicate error (same error_type + bank_id + stage within 60s)
            now = datetime.now(timezone.utc)
            for existing in data["errors"]:
                if (existing.get("error_type") == event.error_type and
                    existing.get("bank_id") == event.bank_id and
                    existing.get("stage") == event.stage):
                    try:
                        existing_time = datetime.fromisoformat(
                            existing.get("timestamp", "").replace('Z', '+00:00')
                        )
                        delta = abs((now - existing_time).total_seconds())
                        if delta < 60:
                            logger.debug(
                                f"Duplicate error detected: {event.error_type} for {event.bank_id}"
                            )
                            return False
                    except (ValueError, TypeError):
                        pass

            data["errors"].append(event.to_dict())

            # Update summary
            summary = data.get("summary", {})
            summary["total_errors"] = len(data["errors"])
            summary["last_updated"] = datetime.now(timezone.utc).isoformat()
            data["summary"] = summary

            self._atomic_write(self.error_log_path, data)

        # Notify log rotation manager (triggers check every N entries)
        _notify_log_rotation("error_log", self.state_dir)

        # Also add to bank state
        try:
            # Find phase from bank manifest or existing state
            state = None
            for phase in range(self.phase_min, self.phase_max + 1):
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

    def add_to_review_queue(self, item: ReviewItem) -> bool:
        """
        Add an item to the review queue with locking to prevent race conditions.

        Includes duplicate detection for same bank_id + checkpoint_id (Gap 7 fix).

        Returns:
            True if added, False if duplicate pending item detected
        """
        with self._file_lock(self.review_queue_path):
            data = self._load_json(self.review_queue_path, {"items": [], "last_updated": None})

            # Check for duplicate pending item (same bank_id + checkpoint_id)
            for existing in data["items"]:
                if (existing.get("bank_id") == item.bank_id and
                    existing.get("checkpoint_id") == item.checkpoint_id and
                    existing.get("status") == "pending"):
                    logger.debug(
                        f"Duplicate review item detected: {item.checkpoint_id} for {item.bank_id}"
                    )
                    return False

            data["items"].append(item.to_dict())
            data["last_updated"] = datetime.now(timezone.utc).isoformat()

            self._atomic_write(self.review_queue_path, data)

        # Notify log rotation manager (triggers check every N entries)
        _notify_log_rotation("review_queue", self.state_dir)
        return True

    def get_pending_reviews(self) -> List[ReviewItem]:
        """Get all pending review items."""
        data = self._load_json(self.review_queue_path, {"items": []})
        return [
            ReviewItem.from_dict(item)
            for item in data["items"]
            if item.get("status") == "pending"
        ]

    def resolve_review(self, bank_id: str, resolution: str, resolved_by: str = "human") -> None:
        """Resolve a review item with locking to prevent race conditions."""
        with self._file_lock(self.review_queue_path):
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
        Mark a bank as complete in BOTH BankState AND WorkflowState atomically.

        Uses StateTransaction to ensure both states are updated together
        or neither is updated (saga pattern with rollback on failure).

        Args:
            bank_id: Bank identifier
            phase: Phase number

        Raises:
            ValueError: If no state found for bank
            TransactionRollbackError: If atomic update fails
        """
        # Load BankState first to validate it exists
        bank_state = self.load_bank_state(bank_id, phase)
        if bank_state is None:
            raise ValueError(f"No state found for {bank_id}")

        bank_path = self._get_bank_dir(bank_id, phase) / "status.json"

        # Use transaction for atomic multi-state update
        with self.multi_state_transaction() as txn:
            # Acquire locks on both files upfront
            txn.acquire_locks([bank_path, self.workflow_state_path])

            # Prepare BankState update
            bank_state.completed_at = datetime.now(timezone.utc).isoformat()
            bank_state.mark_stage_complete("complete")

            # Load and prepare WorkflowState update
            workflow = self.load_workflow_state()
            workflow.mark_bank_completed(bank_id)

            # Stage both writes
            txn.stage_write(bank_path, bank_state.to_dict())
            txn.stage_write(self.workflow_state_path, workflow.to_dict())

            # Atomic commit (both succeed or rollback)
            txn.commit()

        logger.info(f"Marked {bank_id} as complete (atomic transaction)")

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
