"""
Message Queue Persistence - V2 Compliance Module
===============================================

<!-- SSOT Domain: communication -->

Handles queue persistence operations following SRP.
"""

import json
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional
from .message_queue_interfaces import IQueuePersistence, IQueueEntry, IQueueEntry

class FileQueuePersistence(IQueuePersistence):
    """Handles file-based queue persistence operations."""

    def __init__(self, queue_file: Path, lock_manager: Optional[Any] = None):
        """Initialize file persistence."""
        self.queue_file = queue_file
        self.lock_manager = lock_manager

    def load_entries(self) -> List[IQueueEntry]:
        """Load queue entries from JSON file with robust error handling.

        Handles:
        - Corrupted JSON (multiple JSON objects, invalid structure)
        - Empty files
        - Partial JSON writes
        - Encoding issues
        """
        if not self.queue_file.exists():
            # Auto-create empty queue file if it doesn't exist
            self.queue_file.parent.mkdir(parents=True, exist_ok=True)
            self.queue_file.write_text("[]", encoding="utf-8")
            return []

        try:
            # Read raw file content
            raw_content = self.queue_file.read_text(encoding="utf-8").strip()

            if not raw_content:
                # Empty file - return empty list
                return []

            # Try to parse as standard JSON array
            try:
                data = json.loads(raw_content)

                # Validate structure
                if not isinstance(data, list):
                    # If it's a dict, try to extract entries
                    if isinstance(data, dict) and "entries" in data:
                        data = data["entries"]
                    elif isinstance(data, dict) and "pending_pushes" in data:
                        # Handle deferred push queue format
                        data = data["pending_pushes"]
                    else:
                        # Invalid structure - backup and reset
                        self._backup_corrupted_file()
                        return []

                # Parse entries with error isolation
                entries = []
                for idx, entry_data in enumerate(data):
                    try:
                        entry = QueueEntry.from_dict(entry_data)
                        entries.append(entry)
                    except (KeyError, ValueError, TypeError) as entry_error:
                        # Skip invalid entries but continue processing
                        print(
                            f"⚠️ Skipping invalid entry at index {idx}: {entry_error}")
                        continue

                return entries

            except json.JSONDecodeError as json_error:
                # Handle corrupted JSON - try recovery strategies
                return self._recover_corrupted_json(raw_content, json_error)

        except (FileNotFoundError, PermissionError, UnicodeDecodeError) as e:
            print(f"⚠️ Failed to load queue entries: {e}")
            return []
        except Exception as e:
            # Last resort: backup and reset
            print(f"❌ Critical error loading queue entries: {e}")
            self._backup_corrupted_file()
            return []

    def _recover_corrupted_json(self, raw_content: str, json_error: json.JSONDecodeError) -> List[IQueueEntry]:
        """Attempt to recover from corrupted JSON.

        Strategies:
        1. Try to find valid JSON objects in the file
        2. Extract entries from partial JSON
        3. Fall back to backup or empty list
        """
        try:
            # Strategy 1: Try to find array start
            if raw_content.startswith('['):
                # Try to parse up to the error position
                error_pos = json_error.pos if hasattr(
                    json_error, 'pos') else len(raw_content)
                partial_content = raw_content[:error_pos]

                # Try to find last valid array closing
                last_bracket = partial_content.rfind(']')
                if last_bracket > 0:
                    try:
                        data = json.loads(partial_content[:last_bracket + 1])
                        if isinstance(data, list):
                            entries = []
                            for entry_data in data:
                                try:
                                    entries.append(
                                        QueueEntry.from_dict(entry_data))
                                except Exception:
                                    continue
                            if entries:
                                # Backup corrupted file and save recovered entries
                                self._backup_corrupted_file()
                                self.save_entries(entries)
                                print(
                                    f"✅ Recovered {len(entries)} entries from corrupted JSON")
                                return entries
                    except Exception:
                        pass

            # Strategy 2: Try to extract individual JSON objects
            # Look for JSON object patterns { ... }
            entries = []
            bracket_count = 0
            current_obj = ""

            for char in raw_content:
                if char == '{':
                    if bracket_count == 0:
                        current_obj = ""
                    bracket_count += 1
                    current_obj += char
                elif char == '}':
                    current_obj += char
                    bracket_count -= 1

                    if bracket_count == 0:
                        # Found complete object
                        try:
                            obj_data = json.loads(current_obj)
                            entry = QueueEntry.from_dict(obj_data)
                            entries.append(entry)
                        except Exception:
                            pass
                        current_obj = ""

            if entries:
                # Backup and save recovered entries
                self._backup_corrupted_file()
                self.save_entries(entries)
                print(
                    f"✅ Recovered {len(entries)} entries using object extraction")
                return entries

        except Exception as recovery_error:
            print(f"⚠️ Recovery attempt failed: {recovery_error}")

        # All recovery strategies failed - backup and return empty
        self._backup_corrupted_file()
        return []

    def _backup_corrupted_file(self) -> None:
        """Backup corrupted queue file before reset with improved error handling."""
        try:
            if self.queue_file.exists():
                from datetime import datetime
                import shutil

                # Create backup directory if it doesn't exist
                backup_dir = self.queue_file.parent / "backups"
                backup_dir.mkdir(exist_ok=True)

                # Generate unique backup filename with timestamp
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_name = f"{self.queue_file.stem}_{timestamp}_corrupted.json"
                backup_path = backup_dir / backup_name

                # Use copy instead of rename to preserve original for analysis
                shutil.copy2(self.queue_file, backup_path)

                # Only remove original after successful backup
                self.queue_file.unlink()

                print(f"📦 Backed up corrupted queue file to: {backup_path}")
        except PermissionError as e:
            print(f"⚠️ Permission denied backing up corrupted file: {e}")
        except Exception as e:
            print(f"⚠️ Failed to backup corrupted file: {e}")

    def save_entries(self, entries: List[IQueueEntry], max_retries: int = 8, base_delay: float = 0.15) -> None:
        """Save queue entries to JSON file with atomic write and retry logic.

        Args:
            entries: List of queue entries to save
            max_retries: Maximum number of retry attempts (default: 8, increased for WinError 32)
            base_delay: Base delay in seconds for exponential backoff (default: 0.15, increased for file locks)
        """
        # Try to import monitor (optional, fails gracefully if not available)
        monitor = None
        try:
            from tools.file_locking_monitor import FileLockingMonitor
            monitor = FileLockingMonitor()
        except (ImportError, Exception):
            pass  # Monitoring optional, continue without it

        data = [entry.to_dict() for entry in entries]
        temp_file = self.queue_file.with_suffix('.json.tmp')
        start_time = time.time()
        total_delay = 0.0

        # Ensure directory exists before writing
        temp_file.parent.mkdir(parents=True, exist_ok=True)
        self.queue_file.parent.mkdir(parents=True, exist_ok=True)

        # Write to temp file first
        try:
            # CRITICAL FIX: Ensure temp file directory exists before writing
            temp_file.parent.mkdir(parents=True, exist_ok=True)
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(data, f, separators=(',', ':'),
                          ensure_ascii=False, default=str)
            # CRITICAL FIX: Verify temp file was actually written before proceeding
            if not temp_file.exists() or temp_file.stat().st_size == 0:
                raise IOError(
                    f"Temp file was not created or is empty: {temp_file}")
        except Exception as e:
            print(f"❌ Failed to write temp file: {e}")
            # Clean up partial temp file if it exists
            if temp_file.exists():
                try:
                    temp_file.unlink()
                except Exception:
                    pass
            raise

        # Atomic rename with retry logic for Windows file locking
        last_error = None
        for attempt in range(max_retries):
            try:
                # Try to remove existing file if it exists
                if self.queue_file.exists():
                    try:
                        self.queue_file.unlink()
                    except PermissionError:
                        # File may be locked, wait and retry
                        if attempt < max_retries - 1:
                            delay = base_delay * (2 ** attempt)
                            time.sleep(delay)
                            continue
                        else:
                            raise

                # CRITICAL FIX: Verify temp file exists before attempting move
                if not temp_file.exists():
                    raise FileNotFoundError(
                        f"Temp file does not exist before move: {temp_file}. "
                        f"This indicates the write operation failed silently."
                    )

                # Use shutil.move instead of rename for better Windows compatibility
                shutil.move(str(temp_file), str(self.queue_file))

                # Success - record metrics if monitoring enabled
                if monitor and attempt > 0:
                    monitor.record_retry_success(
                        attempts=attempt + 1,
                        total_delay=total_delay,
                        winerror_code=None,
                    )

                # Success - return
                return

            except PermissionError as e:
                # Windows file locking issue (WinError 5)
                last_error = e
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    delay = min(delay, 2.0)  # Cap max delay
                    total_delay += delay

                    # Record error for monitoring
                    if monitor:
                        monitor.record_error(
                            error_type="PermissionError",
                            winerror_code=5,
                            attempt=attempt + 1,
                            delay=delay,
                            file_path=str(self.queue_file),
                        )

                    print(
                        f"⚠️ File locked (attempt {attempt + 1}/{max_retries}), retrying in {delay:.2f}s...")
                    time.sleep(delay)
                else:
                    # Record retry failure
                    if monitor:
                        monitor.record_retry_failure(
                            attempts=max_retries,
                            winerror_code=5,
                        )

                    print(
                        f"❌ Failed to save queue entries after {max_retries} attempts: {e}")
                    # Clean up temp file
                    if temp_file.exists():
                        try:
                            temp_file.unlink()
                        except Exception:
                            pass
                    raise PermissionError(
                        f"Failed to save queue entries: File locked after {max_retries} retries. {e}")

            except OSError as e:
                # Windows-specific errors: WinError 5 (Access Denied) and WinError 32 (File in use)
                winerror_code = getattr(e, 'winerror', None)
                if winerror_code in (5, 32):
                    # WinError 5: Access Denied
                    # WinError 32: The process cannot access the file because it is being used by another process
                    last_error = e
                    error_name = "Access denied" if winerror_code == 5 else "File in use"
                    if attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt)
                        # Cap max delay at 2.0 seconds to prevent excessive waits
                        delay = min(delay, 2.0)
                        total_delay += delay

                        # Record error for monitoring
                        if monitor:
                            monitor.record_error(
                                error_type="OSError",
                                winerror_code=winerror_code,
                                attempt=attempt + 1,
                                delay=delay,
                                file_path=str(self.queue_file),
                            )

                        print(
                            f"⚠️ {error_name} (WinError {winerror_code}, attempt {attempt + 1}/{max_retries}), retrying in {delay:.2f}s...")
                        time.sleep(delay)
                    else:
                        # Record retry failure
                        if monitor:
                            monitor.record_retry_failure(
                                attempts=max_retries,
                                winerror_code=winerror_code,
                            )

                        print(
                            f"❌ Failed to save queue entries after {max_retries} attempts: {e}")
                        # Clean up temp file
                        if temp_file.exists():
                            try:
                                temp_file.unlink()
                            except Exception:
                                pass
                        raise PermissionError(
                            f"Failed to save queue entries: {error_name} (WinError {winerror_code}) after {max_retries} retries. {e}")
                else:
                    # Other OSError - don't retry
                    print(f"❌ Failed to save queue entries: {e}")
                    if temp_file.exists():
                        try:
                            temp_file.unlink()
                        except Exception:
                            pass
                    raise

            except Exception as e:
                # Other errors - don't retry
                print(f"❌ Failed to save queue entries: {e}")
                if temp_file.exists():
                    try:
                        temp_file.unlink()
                    except Exception:
                        pass
                raise

        # Should not reach here, but handle just in case
        if last_error:
            raise last_error

    def atomic_operation(self, operation: Callable[[], Any]) -> Any:
        """Perform atomic file operation with locking."""
        if self.lock_manager:
            # Use provided lock manager for atomic operations
            return self.lock_manager.atomic_operation(self.queue_file, operation)
        else:
            # Simple atomic operation without locking
            return operation()


class QueueEntry:
    """Queue entry data structure."""

    def __init__(
        self,
        message: Any,
        queue_id: str,
        priority_score: float,
        status: str,
        created_at: Any,
        updated_at: Any,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Initialize queue entry."""
        self.message = message
        self.queue_id = queue_id
        self.priority_score = priority_score
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary using SSOT utility."""
        from src.core.utils.serialization_utils import to_dict
        return to_dict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'QueueEntry':
        """Create from dictionary"""
        return cls(
            message=data['message'],
            queue_id=data['queue_id'],
            priority_score=data['priority_score'],
            status=data['status'],
            created_at=data['created_at'],
            updated_at=data['updated_at'],
            metadata=data.get('metadata', {})
        )
