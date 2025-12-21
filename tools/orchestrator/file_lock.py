"""
CDM Research Protocol - Shared File Locking Utilities

Provides file locking primitives for use across orchestrator modules.
Designed to avoid circular dependencies with state_manager.py.

Features:
- Cross-platform lock acquisition (Windows/Unix)
- Stale lock detection with PID + age checking
- Robust Windows PID verification with fallback chain
- atomic_write() and load_json() helpers

Usage:
    from orchestrator.file_lock import file_lock, atomic_write, load_json

    with file_lock(path):
        data = load_json(path)
        data["items"].append(new_item)
        atomic_write(path, data)
"""

import os
import sys
import json
import time
import platform
import logging
from pathlib import Path
from datetime import datetime, timezone, timedelta
from contextlib import contextmanager
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

# Cross-platform detection
WINDOWS = sys.platform == 'win32'


class FileLockError(Exception):
    """Raised when file lock cannot be acquired."""
    pass


class FileLockTimeout(FileLockError):
    """Raised when lock acquisition times out."""
    pass


def process_exists(pid: int) -> bool:
    """
    Check if a process with given PID exists.

    Uses robust fallback chain for Windows to avoid silent failures.

    Args:
        pid: Process ID to check

    Returns:
        True if process exists, False otherwise
    """
    if WINDOWS:
        return _process_exists_windows(pid)
    else:
        return _process_exists_unix(pid)


def _process_exists_unix(pid: int) -> bool:
    """Unix-specific process existence check."""
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def _process_exists_windows(pid: int) -> bool:
    """
    Windows-specific process existence check with fallback chain.

    Fallback order:
    1. ctypes OpenProcess (most reliable, fastest)
    2. tasklist subprocess (reliable but slower)
    3. psutil if available (optional dependency)
    4. Return False (conservative - allows lock cleanup)

    IMPORTANT: Unlike previous implementation, we return False on
    failure rather than True. This allows stale lock cleanup rather
    than causing permanent lock blockage.
    """
    # Method 1: ctypes OpenProcess
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000

        handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
        if handle:
            kernel32.CloseHandle(handle)
            return True

        # Check if access denied (process exists but no permission)
        # Use GetLastError via ctypes
        error = ctypes.get_last_error()
        if error == 5:  # ERROR_ACCESS_DENIED
            return True

        return False

    except Exception as e:
        logger.debug(f"ctypes PID check failed for PID {pid}: {e}")

    # Method 2: tasklist subprocess
    try:
        import subprocess
        # Use CREATE_NO_WINDOW to avoid console popup
        creationflags = subprocess.CREATE_NO_WINDOW if WINDOWS else 0
        result = subprocess.run(
            ['tasklist', '/FI', f'PID eq {pid}', '/NH', '/FO', 'CSV'],
            capture_output=True,
            text=True,
            timeout=5,
            creationflags=creationflags
        )
        # tasklist returns the PID in output if process exists
        return str(pid) in result.stdout

    except Exception as e:
        logger.debug(f"tasklist PID check failed for PID {pid}: {e}")

    # Method 3: psutil (if available)
    try:
        import psutil
        return psutil.pid_exists(pid)
    except ImportError:
        pass
    except Exception as e:
        logger.debug(f"psutil PID check failed for PID {pid}: {e}")

    # Method 4: Conservative default - assume NOT exists
    # This allows stale lock cleanup rather than permanent blocking
    logger.warning(f"Could not verify PID {pid} exists - assuming stale lock")
    return False


def _parse_lock_info(lock_path: Path) -> Optional[Dict[str, Any]]:
    """
    Parse lock file contents.

    Returns:
        Lock info dict or None if file doesn't exist or is corrupted
    """
    if not lock_path.exists():
        return None

    try:
        content = lock_path.read_text(encoding='utf-8')
        return json.loads(content)
    except (json.JSONDecodeError, IOError, OSError) as e:
        logger.debug(f"Could not parse lock file {lock_path}: {e}")
        return None


def _is_lock_stale(lock_info: Dict[str, Any], stale_lock_age: int = 300) -> bool:
    """
    Check if a lock is stale based on PID and age.

    Args:
        lock_info: Parsed lock file contents
        stale_lock_age: Age in seconds after which lock is considered stale

    Returns:
        True if lock is stale (should be cleaned up)
    """
    # Check if PID still running
    lock_pid = lock_info.get('pid')
    if lock_pid and not process_exists(lock_pid):
        logger.debug(f"Lock PID {lock_pid} no longer exists - stale")
        return True

    # Check age
    acquired_str = lock_info.get('acquired')
    if acquired_str:
        try:
            acquired = datetime.fromisoformat(acquired_str.replace('Z', '+00:00'))
            age = (datetime.now(timezone.utc) - acquired).total_seconds()

            if age > stale_lock_age:
                logger.debug(f"Lock held for {age:.0f}s exceeds {stale_lock_age}s - stale")
                return True
        except (ValueError, TypeError) as e:
            logger.debug(f"Could not parse lock timestamp: {e}")

    return False


def handle_stale_lock(lock_path: Path, stale_lock_age: int = 300) -> bool:
    """
    Detect and handle stale locks.

    Args:
        lock_path: Path to the lock file
        stale_lock_age: Age in seconds after which lock is considered stale

    Returns:
        True if stale lock was removed, False otherwise
    """
    if not lock_path.exists():
        return False

    # Check for corrupted lock file
    lock_info = _parse_lock_info(lock_path)
    if lock_info is None:
        # Corrupted or empty - safe to remove
        try:
            logger.warning(f"Removing corrupted lock file: {lock_path}")
            lock_path.unlink()
            return True
        except OSError as e:
            logger.debug(f"Could not remove corrupted lock: {e}")
            return False

    # Check if stale
    if _is_lock_stale(lock_info, stale_lock_age):
        try:
            lock_pid = lock_info.get('pid', 'unknown')
            logger.warning(f"Removing stale lock (PID {lock_pid}): {lock_path}")
            lock_path.unlink()
            return True
        except OSError as e:
            logger.debug(f"Could not remove stale lock: {e}")
            return False

    return False


@contextmanager
def file_lock(
    path: Path,
    timeout: float = 30.0,
    stale_lock_age: int = 300,
    operation: str = None
):
    """
    Context manager for exclusive file locking.

    Creates a lock file (path.lock) that contains process info for
    debugging and stale detection.

    Args:
        path: Path to the file being locked
        timeout: Maximum time to wait for lock (seconds)
        stale_lock_age: Age in seconds after which lock is considered stale
        operation: Optional description for logging

    Yields:
        None (lock is held for duration of context)

    Raises:
        FileLockTimeout: If lock cannot be acquired within timeout
        FileLockError: If lock cannot be acquired due to other errors

    Usage:
        with file_lock(Path("data.json"), operation="update"):
            data = load_json(path)
            data["key"] = "value"
            atomic_write(path, data)
    """
    lock_path = path.with_suffix(path.suffix + '.lock')
    fd = None
    retries = 0
    op_desc = f" ({operation})" if operation else ""

    try:
        start_time = time.time()

        while True:
            try:
                # Attempt to create lock file exclusively
                fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_RDWR)

                # Write lock info for debugging and stale detection
                lock_info = json.dumps({
                    "pid": os.getpid(),
                    "acquired": datetime.now(timezone.utc).isoformat(),
                    "host": platform.node(),
                    "file": str(path),
                    "operation": operation,
                })
                os.write(fd, lock_info.encode('utf-8'))

                # Log if we had contention
                if retries > 0:
                    elapsed = time.time() - start_time
                    logger.debug(
                        f"Lock acquired after {retries} retries "
                        f"({elapsed:.2f}s){op_desc}: {path.name}"
                    )

                break

            except FileExistsError:
                # Lock exists - check if stale
                if handle_stale_lock(lock_path, stale_lock_age):
                    continue  # Stale lock removed, try again

                # Check timeout
                elapsed = time.time() - start_time
                if elapsed > timeout:
                    # Try to get lock holder info for error message
                    lock_info = _parse_lock_info(lock_path)
                    holder_pid = lock_info.get('pid', 'unknown') if lock_info else 'unknown'
                    raise FileLockTimeout(
                        f"Timeout ({timeout}s) waiting for lock on {path.name} "
                        f"(held by PID {holder_pid}){op_desc}"
                    )

                retries += 1
                time.sleep(0.1)  # Brief wait before retry

            except OSError as e:
                elapsed = time.time() - start_time
                if elapsed > timeout:
                    raise FileLockError(f"Error acquiring lock on {path}: {e}")
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


def atomic_write(path: Path, data: dict, indent: int = 2) -> None:
    """
    Atomically write JSON data to file.

    Writes to a temp file then renames for crash safety.
    The rename operation is atomic on most filesystems.

    Args:
        path: Target file path
        data: Dictionary to serialize as JSON
        indent: JSON indentation level (default 2)
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix('.tmp')

    try:
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)

        # Atomic rename
        temp_path.replace(path)

    except Exception:
        # Clean up temp file on error
        try:
            temp_path.unlink()
        except (FileNotFoundError, OSError):
            pass
        raise


def load_json(path: Path, default: dict = None) -> dict:
    """
    Load JSON file, returning default if not exists or on error.

    Args:
        path: Path to JSON file
        default: Default value if file doesn't exist or is invalid

    Returns:
        Parsed JSON as dict, or default value
    """
    if not path.exists():
        return default if default is not None else {}

    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError, OSError) as e:
        logger.error(f"Error loading {path}: {e}")
        return default if default is not None else {}


def locked_update(
    path: Path,
    update_fn,
    default: dict = None,
    timeout: float = 30.0,
    stale_lock_age: int = 300,
    operation: str = None
) -> Any:
    """
    Convenience function for atomic read-modify-write with locking.

    Args:
        path: Path to JSON file
        update_fn: Function that takes data dict and returns modified dict
        default: Default value if file doesn't exist
        timeout: Lock timeout in seconds
        stale_lock_age: Stale lock age in seconds
        operation: Optional operation description for logging

    Returns:
        Result of update_fn

    Usage:
        def add_item(data):
            data["items"].append(new_item)
            return data

        locked_update(path, add_item, default={"items": []})
    """
    with file_lock(path, timeout, stale_lock_age, operation):
        data = load_json(path, default)
        result = update_fn(data)
        atomic_write(path, result)
        return result
