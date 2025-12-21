"""
CDM Research Protocol - Centralized Locking Service

Provides a singleton locking service for all components with configurable
timing parameters from decision-thresholds.json.

Addresses Gap 8: Inconsistent Lock Scope

Usage:
    from locking_service import LockingService, get_locking_service

    # Get singleton instance
    service = get_locking_service()

    # Acquire lock with configured timeout
    with service.lock_file(path, operation="update"):
        # ... modify file ...

    # Or use locked_update helper
    service.locked_update(path, update_fn, default={})
"""

import sys
import json
import time
import logging
from pathlib import Path
from typing import Optional, Callable, Dict, Any
from contextlib import contextmanager

# Import the underlying file lock implementation
# Use direct import to avoid broken orchestrator package __init__.py
import importlib.util
_file_lock_path = Path(__file__).parent / "orchestrator" / "file_lock.py"
if not _file_lock_path.exists():
    raise ImportError(f"file_lock.py not found at {_file_lock_path}")

_spec = importlib.util.spec_from_file_location("file_lock", _file_lock_path)
_file_lock_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_file_lock_module)

file_lock = _file_lock_module.file_lock
atomic_write = _file_lock_module.atomic_write
load_json = _file_lock_module.load_json
_base_locked_update = _file_lock_module.locked_update
FileLockError = _file_lock_module.FileLockError
FileLockTimeout = _file_lock_module.FileLockTimeout

# Import config - flexible import handling
try:
    from config_loader import get_state_management_config
except ImportError:
    _tools_dir = Path(__file__).parent
    if str(_tools_dir) not in sys.path:
        sys.path.insert(0, str(_tools_dir))
    from config_loader import get_state_management_config

logger = logging.getLogger(__name__)


class LockingService:
    """
    Singleton locking service for all state management components.

    Provides centralized locking with configurable timing parameters
    and consistent lock handling across the codebase.

    Configuration is loaded from decision-thresholds.json:
        state_management:
            lock_timeout_seconds: 30
            stale_lock_age_seconds: 300
            retry_config:
                max_retries: 5
                base_delay_seconds: 0.1
                max_delay_seconds: 2.0

    Features:
    - Singleton pattern ensures all components use same config
    - Configurable timeouts from central config file
    - Metrics tracking for lock contention
    - Consistent error handling
    """

    _instance: Optional['LockingService'] = None
    _initialized: bool = False

    def __new__(cls, *args, **kwargs):
        """Ensure only one instance exists (singleton pattern)."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config: Dict[str, Any] = None, force_reinit: bool = False):
        """
        Initialize locking service.

        Args:
            config: Optional override config. If None, loads from file.
            force_reinit: If True, reload config even if already initialized.
        """
        if self._initialized and not force_reinit:
            return

        if config is not None:
            self._config = config
        else:
            self._config = self._load_config()

        # Extract timing parameters
        self.lock_timeout = self._config.get('lock_timeout_seconds', 30)
        self.stale_lock_age = self._config.get('stale_lock_age_seconds', 300)

        retry_config = self._config.get('retry_config', {})
        self.max_retries = retry_config.get('max_retries', 5)
        self.base_delay = retry_config.get('base_delay_seconds', 0.1)
        self.max_delay = retry_config.get('max_delay_seconds', 2.0)

        # Metrics tracking
        self._metrics = {
            'locks_acquired': 0,
            'lock_contentions': 0,
            'stale_locks_cleaned': 0,
            'timeouts': 0,
        }

        self._initialized = True
        logger.debug(
            f"LockingService initialized: timeout={self.lock_timeout}s, "
            f"stale_age={self.stale_lock_age}s"
        )

    def _load_config(self) -> Dict[str, Any]:
        """Load locking configuration from decision-thresholds.json."""
        try:
            return get_state_management_config()
        except Exception as e:
            logger.warning(f"Could not load locking config: {e}. Using defaults.")
            return {
                'lock_timeout_seconds': 30,
                'stale_lock_age_seconds': 300,
                'retry_config': {
                    'max_retries': 5,
                    'base_delay_seconds': 0.1,
                    'max_delay_seconds': 2.0
                }
            }

    @contextmanager
    def lock_file(
        self,
        path: Path,
        operation: str = None,
        timeout: float = None,
        stale_lock_age: int = None
    ):
        """
        Acquire exclusive lock on a file.

        Uses configured timeout and stale lock age unless overridden.

        Args:
            path: Path to the file to lock
            operation: Optional description for logging
            timeout: Override default timeout (seconds)
            stale_lock_age: Override default stale lock age (seconds)

        Yields:
            None (lock is held for duration of context)

        Raises:
            FileLockTimeout: If lock cannot be acquired within timeout
            FileLockError: If lock cannot be acquired due to other errors
        """
        effective_timeout = timeout if timeout is not None else self.lock_timeout
        effective_stale_age = stale_lock_age if stale_lock_age is not None else self.stale_lock_age

        try:
            with file_lock(
                path,
                timeout=effective_timeout,
                stale_lock_age=effective_stale_age,
                operation=operation
            ):
                self._metrics['locks_acquired'] += 1
                yield
        except FileLockTimeout:
            self._metrics['timeouts'] += 1
            raise
        except FileLockError:
            self._metrics['lock_contentions'] += 1
            raise

    def locked_update(
        self,
        path: Path,
        update_fn: Callable[[dict], dict],
        default: dict = None,
        operation: str = None,
        timeout: float = None
    ) -> Any:
        """
        Perform atomic read-modify-write with locking.

        Args:
            path: Path to JSON file
            update_fn: Function that takes data dict and returns modified dict
            default: Default value if file doesn't exist
            operation: Optional operation description for logging
            timeout: Optional timeout override

        Returns:
            Result of update_fn

        Usage:
            def add_item(data):
                data["items"].append(new_item)
                return data

            service.locked_update(path, add_item, default={"items": []})
        """
        effective_timeout = timeout if timeout is not None else self.lock_timeout

        return _base_locked_update(
            path,
            update_fn,
            default=default,
            timeout=effective_timeout,
            stale_lock_age=self.stale_lock_age,
            operation=operation
        )

    def atomic_write(self, path: Path, data: dict, indent: int = 2) -> None:
        """
        Atomically write JSON data to file.

        Note: This does NOT acquire a lock. Use lock_file() if you need
        exclusive access during read-modify-write operations.

        Args:
            path: Target file path
            data: Dictionary to serialize as JSON
            indent: JSON indentation level
        """
        atomic_write(path, data, indent)

    def load_json(self, path: Path, default: dict = None) -> dict:
        """
        Load JSON file, returning default if not exists.

        Note: This does NOT acquire a lock. Use lock_file() if you need
        exclusive access during read-modify-write operations.

        Args:
            path: Path to JSON file
            default: Default value if file doesn't exist

        Returns:
            Parsed JSON as dict, or default value
        """
        return load_json(path, default)

    def get_metrics(self) -> Dict[str, int]:
        """Get lock contention metrics."""
        return self._metrics.copy()

    def reset_metrics(self) -> None:
        """Reset lock contention metrics."""
        self._metrics = {
            'locks_acquired': 0,
            'lock_contentions': 0,
            'stale_locks_cleaned': 0,
            'timeouts': 0,
        }

    @property
    def config(self) -> Dict[str, Any]:
        """Get current configuration."""
        return self._config.copy()

    def _config_fingerprint(self, config: Dict[str, Any] = None) -> str:
        """
        Generate fingerprint of config for change detection.

        Args:
            config: Config dict to fingerprint. Uses current config if None.

        Returns:
            8-character hash string uniquely identifying the config
        """
        import hashlib
        config_to_hash = config if config is not None else self._config
        config_str = json.dumps(config_to_hash, sort_keys=True)
        return hashlib.md5(config_str.encode()).hexdigest()[:8]

    def check_and_reload_config(self) -> bool:
        """
        Check if config has changed and reload if so.

        Compares current config fingerprint with fresh load from file.
        If different, reinitializes the service with new config.

        Returns:
            True if config was reloaded, False if unchanged
        """
        new_config = self._load_config()
        old_fingerprint = self._config_fingerprint(self._config)
        new_fingerprint = self._config_fingerprint(new_config)

        if new_fingerprint != old_fingerprint:
            self.__init__(config=new_config, force_reinit=True)
            logger.info(
                f"LockingService config reloaded "
                f"(fingerprint: {old_fingerprint} -> {new_fingerprint})"
            )
            return True
        return False

    def reload_config(self) -> None:
        """Reload configuration from file."""
        self.__init__(force_reinit=True)


# Module-level singleton accessor

_service_instance: Optional[LockingService] = None
_last_config_check: float = 0
_CONFIG_CHECK_INTERVAL: float = 60.0  # Check every 60 seconds


def get_locking_service() -> LockingService:
    """
    Get the global LockingService singleton with periodic config freshness check.

    Returns:
        LockingService instance with configuration from decision-thresholds.json

    Note:
        Config is automatically checked for changes every 60 seconds.
        If config has changed, the service is reinitialized with new settings.
    """
    global _service_instance, _last_config_check

    now = time.time()

    if _service_instance is None:
        _service_instance = LockingService()
        _last_config_check = now
    elif now - _last_config_check > _CONFIG_CHECK_INTERVAL:
        # Periodic config freshness check
        _service_instance.check_and_reload_config()
        _last_config_check = now

    return _service_instance


def reset_locking_service() -> None:
    """
    Reset the global LockingService singleton.

    Call this after modifying configuration to force reload.
    """
    global _service_instance
    _service_instance = None


# Convenience functions that use the singleton

def lock_file(path: Path, operation: str = None, timeout: float = None):
    """Acquire file lock using the global LockingService."""
    return get_locking_service().lock_file(path, operation, timeout)


def locked_update(
    path: Path,
    update_fn: Callable[[dict], dict],
    default: dict = None,
    operation: str = None
) -> Any:
    """Perform locked update using the global LockingService."""
    return get_locking_service().locked_update(path, update_fn, default, operation)
