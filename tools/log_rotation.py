"""
CDM Research Protocol - Log Rotation System

Provides automatic rotation and archival of log files to prevent unbounded growth.
Addresses Gap 4: Unbounded Log Growth.

Features:
- Configurable rotation thresholds per log type
- Gzip compression for archived logs
- Retention-based cleanup of old archives
- Atomic rotation to prevent data loss

Usage:
    from log_rotation import LogRotationManager

    manager = LogRotationManager(state_dir=Path("outputs/state"))
    manager.check_and_rotate("checkpoint_log")
    manager.cleanup_old_archives()
"""

import os
import sys
import json
import gzip
import shutil
import logging
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, List

# Flexible import handling for different execution contexts
try:
    # When imported as part of tools package
    from config_loader import load_decision_thresholds
except ImportError:
    # When run directly or from different context
    _tools_dir = Path(__file__).parent
    if str(_tools_dir) not in sys.path:
        sys.path.insert(0, str(_tools_dir))
    from config_loader import load_decision_thresholds

# Import file locking utilities for thread-safe rotation
# Use direct import to avoid broken orchestrator package __init__.py
try:
    import importlib.util
    _file_lock_path = Path(__file__).parent / "orchestrator" / "file_lock.py"
    if _file_lock_path.exists():
        spec = importlib.util.spec_from_file_location("file_lock", _file_lock_path)
        _file_lock_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_file_lock_module)
        file_lock = _file_lock_module.file_lock
        atomic_write = _file_lock_module.atomic_write
        _HAS_FILE_LOCK = True
    else:
        raise ImportError(f"file_lock.py not found at {_file_lock_path}")
except Exception as e:
    logging.getLogger(__name__).debug(f"File locking not available: {e}")
    _HAS_FILE_LOCK = False
    file_lock = None
    atomic_write = None

logger = logging.getLogger(__name__)


class LogRotationError(Exception):
    """Raised when log rotation fails."""
    pass


class LogRotationManager:
    """
    Manages log file rotation and archival.

    Monitors configured log files and rotates them when they exceed
    configurable thresholds. Archived logs are optionally compressed
    and cleaned up based on retention policy.
    """

    # Mapping from config keys to actual file names
    LOG_FILE_MAPPING = {
        "checkpoint_log": "checkpoint-log.json",
        "error_log": "error-log.json",
        "review_queue": "review-queue.json",
        "violation_queue": "violation-queue.json",
    }

    def __init__(
        self,
        state_dir: Path = None,
        config: Dict[str, Any] = None
    ):
        """
        Initialize log rotation manager.

        Args:
            state_dir: Directory containing state/log files.
                       Defaults to outputs/state relative to project root.
            config: Optional override config. If None, loads from
                    decision-thresholds.json.
        """
        if state_dir is None:
            # Default to outputs/state relative to tools directory
            self.state_dir = Path(__file__).parent.parent / "outputs" / "state"
        else:
            self.state_dir = Path(state_dir)

        # Load configuration
        if config is not None:
            self.config = config
        else:
            self.config = self._load_config()

        # Ensure archive directory exists
        self.archive_dir = self.state_dir / self.config.get("archive_directory", "archives")
        self.archive_dir.mkdir(parents=True, exist_ok=True)

        # Track rotation counts for check_interval
        self._log_counts: Dict[str, int] = {}

    def _load_config(self) -> Dict[str, Any]:
        """Load rotation config from decision-thresholds.json."""
        try:
            thresholds = load_decision_thresholds()
            return thresholds.get("log_rotation", self._default_config())
        except Exception as e:
            logger.warning(f"Could not load rotation config: {e}. Using defaults.")
            return self._default_config()

    def _default_config(self) -> Dict[str, Any]:
        """Return default rotation configuration."""
        return {
            "enabled": True,
            "thresholds": {
                "checkpoint_log": {"max_entries": 1000, "archive_threshold": 800},
                "error_log": {"max_entries": 500, "archive_threshold": 400},
                "review_queue": {"max_entries": 200, "archive_threshold": 150},
                "violation_queue": {"max_entries": 200, "archive_threshold": 150},
            },
            "archive_directory": "archives",
            "retention_days": 90,
            "compress_archives": True,
            "check_interval": 100,
        }

    def get_log_path(self, log_type: str) -> Path:
        """Get the file path for a log type."""
        filename = self.LOG_FILE_MAPPING.get(log_type)
        if filename is None:
            raise ValueError(f"Unknown log type: {log_type}")
        return self.state_dir / filename

    def get_entry_count(self, log_type: str) -> int:
        """
        Get the current entry count for a log file.

        Args:
            log_type: One of checkpoint_log, error_log, review_queue, violation_queue

        Returns:
            Number of entries in the log, or 0 if file doesn't exist
        """
        log_path = self.get_log_path(log_type)

        if not log_path.exists():
            return 0

        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Handle different log structures
            if log_type == "checkpoint_log":
                return len(data.get("checkpoints", []))
            elif log_type == "error_log":
                return len(data.get("errors", []))
            elif log_type == "review_queue":
                return len(data.get("pending", []))
            elif log_type == "violation_queue":
                return len(data.get("violations", []))
            else:
                # Generic: count items if it's a list, keys if dict
                if isinstance(data, list):
                    return len(data)
                elif isinstance(data, dict):
                    # Sum all list values
                    return sum(len(v) for v in data.values() if isinstance(v, list))
                return 0

        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Could not read {log_path}: {e}")
            return 0

    def needs_rotation(self, log_type: str) -> bool:
        """
        Check if a log file needs rotation.

        Args:
            log_type: Log type to check

        Returns:
            True if entry count exceeds archive_threshold
        """
        if not self.config.get("enabled", True):
            return False

        thresholds = self.config.get("thresholds", {})
        log_config = thresholds.get(log_type, {})
        archive_threshold = log_config.get("archive_threshold", 800)

        entry_count = self.get_entry_count(log_type)
        return entry_count >= archive_threshold

    def rotate(self, log_type: str, force: bool = False) -> Optional[Path]:
        """
        Rotate a log file if it exceeds threshold (or if forced).

        The current log is archived with a timestamp suffix, then
        the active log is reset to an empty state. Uses file locking
        to prevent race conditions with concurrent writers.

        Args:
            log_type: Log type to rotate
            force: If True, rotate regardless of threshold

        Returns:
            Path to the archive file if rotation occurred, None otherwise
        """
        if not force and not self.needs_rotation(log_type):
            return None

        log_path = self.get_log_path(log_type)

        if not log_path.exists():
            logger.debug(f"No {log_type} file to rotate")
            return None

        # Execute rotation with or without locking depending on availability
        if _HAS_FILE_LOCK:
            with file_lock(log_path, operation=f"rotate_{log_type}"):
                return self._do_rotation(log_type, log_path)
        else:
            logger.warning(f"File locking not available - rotating {log_type} without lock")
            return self._do_rotation(log_type, log_path)

    def _do_rotation(self, log_type: str, log_path: Path) -> Optional[Path]:
        """
        Internal rotation logic - must be called with appropriate locking.

        Args:
            log_type: Log type being rotated
            log_path: Path to the log file

        Returns:
            Path to the archive file if successful
        """
        # Generate archive filename with timestamp
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        base_name = log_path.stem
        archive_name = f"{base_name}_{timestamp}.json"

        if self.config.get("compress_archives", True):
            archive_name += ".gz"

        archive_path = self.archive_dir / archive_name

        try:
            # Read current log
            with open(log_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Add rotation metadata
            rotation_meta = {
                "_rotation_meta": {
                    "rotated_at": datetime.now(timezone.utc).isoformat(),
                    "original_path": str(log_path),
                    "entry_count": self.get_entry_count(log_type),
                }
            }
            if isinstance(data, dict):
                data.update(rotation_meta)

            # Write archive (compressed or plain)
            if self.config.get("compress_archives", True):
                with gzip.open(archive_path, 'wt', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
            else:
                with open(archive_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)

            # Reset active log to empty state using atomic write if available
            empty_state = self._get_empty_state(log_type)
            if _HAS_FILE_LOCK and atomic_write is not None:
                atomic_write(log_path, empty_state)
            else:
                with open(log_path, 'w', encoding='utf-8') as f:
                    json.dump(empty_state, f, indent=2)

            logger.info(f"Rotated {log_type}: {archive_path.name}")
            return archive_path

        except Exception as e:
            logger.error(f"Failed to rotate {log_type}: {e}")
            raise LogRotationError(f"Failed to rotate {log_type}: {e}")

    def _get_empty_state(self, log_type: str) -> Dict[str, Any]:
        """Return the empty state structure for a log type."""
        if log_type == "checkpoint_log":
            return {
                "version": "2.0",
                "checkpoints": [],
                "_rotation_info": {
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "previous_archive": None,
                }
            }
        elif log_type == "error_log":
            return {
                "version": "1.0",
                "errors": [],
                "_rotation_info": {
                    "created_at": datetime.now(timezone.utc).isoformat(),
                }
            }
        elif log_type == "review_queue":
            return {
                "pending": [],
                "completed": [],
                "_rotation_info": {
                    "created_at": datetime.now(timezone.utc).isoformat(),
                }
            }
        elif log_type == "violation_queue":
            return {
                "violations": [],
                "resolved": [],
                "summary": {},
                "_rotation_info": {
                    "created_at": datetime.now(timezone.utc).isoformat(),
                }
            }
        else:
            return {
                "_rotation_info": {
                    "created_at": datetime.now(timezone.utc).isoformat(),
                }
            }

    def check_and_rotate(self, log_type: str) -> Optional[Path]:
        """
        Check if rotation is needed and rotate if so.

        This is the main entry point for callers who want automatic
        rotation based on thresholds.

        Args:
            log_type: Log type to check and potentially rotate

        Returns:
            Path to archive if rotated, None otherwise
        """
        return self.rotate(log_type, force=False)

    def check_all(self) -> Dict[str, Optional[Path]]:
        """
        Check and rotate all configured log types.

        Returns:
            Dict mapping log_type to archive path (or None if not rotated)
        """
        results = {}
        for log_type in self.LOG_FILE_MAPPING:
            try:
                results[log_type] = self.check_and_rotate(log_type)
            except LogRotationError as e:
                logger.error(f"Rotation check failed for {log_type}: {e}")
                results[log_type] = None
        return results

    def increment_and_check(self, log_type: str) -> Optional[Path]:
        """
        Increment log entry counter and check rotation if interval reached.

        Call this after adding an entry to a log. Rotation check only
        happens every check_interval entries to reduce I/O overhead.

        Args:
            log_type: Log type that was updated

        Returns:
            Path to archive if rotated, None otherwise
        """
        self._log_counts[log_type] = self._log_counts.get(log_type, 0) + 1

        check_interval = self.config.get("check_interval", 100)

        if self._log_counts[log_type] >= check_interval:
            self._log_counts[log_type] = 0
            return self.check_and_rotate(log_type)

        return None

    def get_archives(self, log_type: str = None) -> List[Path]:
        """
        Get list of archive files, optionally filtered by log type.

        Args:
            log_type: Optional filter for specific log type

        Returns:
            List of archive file paths, sorted by modification time (newest first)
        """
        if log_type:
            filename = self.LOG_FILE_MAPPING.get(log_type)
            if filename:
                base = Path(filename).stem
                pattern = f"{base}_*.json*"
            else:
                pattern = "*.json*"
        else:
            pattern = "*.json*"

        archives = list(self.archive_dir.glob(pattern))
        archives.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        return archives

    def cleanup_old_archives(self) -> int:
        """
        Remove archives older than retention_days.

        Returns:
            Number of archives deleted
        """
        retention_days = self.config.get("retention_days", 90)
        cutoff = datetime.now(timezone.utc) - timedelta(days=retention_days)
        cutoff_timestamp = cutoff.timestamp()

        deleted = 0
        for archive in self.get_archives():
            try:
                if archive.stat().st_mtime < cutoff_timestamp:
                    archive.unlink()
                    logger.info(f"Deleted expired archive: {archive.name}")
                    deleted += 1
            except OSError as e:
                logger.warning(f"Could not delete {archive}: {e}")

        if deleted > 0:
            logger.info(f"Cleaned up {deleted} expired archives (>{retention_days} days old)")

        return deleted

    def get_rotation_status(self) -> Dict[str, Any]:
        """
        Get current rotation status for all log types.

        Returns:
            Dict with entry counts, thresholds, and archive counts per log type
        """
        status = {
            "enabled": self.config.get("enabled", True),
            "archive_dir": str(self.archive_dir),
            "logs": {},
        }

        thresholds = self.config.get("thresholds", {})

        for log_type in self.LOG_FILE_MAPPING:
            log_config = thresholds.get(log_type, {})
            entry_count = self.get_entry_count(log_type)
            archive_threshold = log_config.get("archive_threshold", 800)
            max_entries = log_config.get("max_entries", 1000)

            status["logs"][log_type] = {
                "entry_count": entry_count,
                "archive_threshold": archive_threshold,
                "max_entries": max_entries,
                "needs_rotation": entry_count >= archive_threshold,
                "utilization_pct": round(entry_count / max_entries * 100, 1) if max_entries > 0 else 0,
                "archive_count": len(self.get_archives(log_type)),
            }

        return status

    def _config_fingerprint(self, config: Dict[str, Any] = None) -> str:
        """
        Generate fingerprint of config for change detection.

        Args:
            config: Config dict to fingerprint. Uses current config if None.

        Returns:
            8-character hash string uniquely identifying the config
        """
        import hashlib
        config_to_hash = config if config is not None else self.config
        config_str = json.dumps(config_to_hash, sort_keys=True)
        return hashlib.md5(config_str.encode()).hexdigest()[:8]

    def check_and_reload_config(self) -> bool:
        """
        Check if config has changed and reload if so.

        Compares current config fingerprint with fresh load from file.
        If different, reinitializes the manager with new config.

        Returns:
            True if config was reloaded, False if unchanged
        """
        new_config = self._load_config()
        old_fingerprint = self._config_fingerprint(self.config)
        new_fingerprint = self._config_fingerprint(new_config)

        if new_fingerprint != old_fingerprint:
            self.config = new_config
            # Update archive directory if changed
            self.archive_dir = self.state_dir / self.config.get("archive_directory", "archives")
            self.archive_dir.mkdir(parents=True, exist_ok=True)
            logger.info(
                f"LogRotationManager config reloaded "
                f"(fingerprint: {old_fingerprint} -> {new_fingerprint})"
            )
            return True
        return False


# Module-level convenience functions

_manager_instance: Optional[LogRotationManager] = None
_last_config_check: float = 0
_CONFIG_CHECK_INTERVAL: float = 60.0  # Check every 60 seconds


def get_manager(state_dir: Path = None) -> LogRotationManager:
    """
    Get or create the global LogRotationManager instance with periodic config check.

    Args:
        state_dir: Optional state directory path (used only on first initialization)

    Returns:
        LogRotationManager singleton instance

    Note:
        Config is automatically checked for changes every 60 seconds.
        If config has changed, the manager is reinitialized with new settings.
    """
    global _manager_instance, _last_config_check
    import time

    now = time.time()

    if _manager_instance is None:
        _manager_instance = LogRotationManager(state_dir)
        _last_config_check = now
    elif now - _last_config_check > _CONFIG_CHECK_INTERVAL:
        # Periodic config freshness check
        _manager_instance.check_and_reload_config()
        _last_config_check = now

    return _manager_instance


def check_and_rotate(log_type: str, state_dir: Path = None) -> Optional[Path]:
    """
    Convenience function to check and rotate a log type.

    Args:
        log_type: Log type to check
        state_dir: Optional state directory path

    Returns:
        Archive path if rotated, None otherwise
    """
    return get_manager(state_dir).check_and_rotate(log_type)


def notify_log_entry(log_type: str, state_dir: Path = None) -> Optional[Path]:
    """
    Notify that an entry was added to a log.

    Call this after adding entries to trigger periodic rotation checks.

    Args:
        log_type: Log type that was updated
        state_dir: Optional state directory path

    Returns:
        Archive path if rotated, None otherwise
    """
    return get_manager(state_dir).increment_and_check(log_type)
