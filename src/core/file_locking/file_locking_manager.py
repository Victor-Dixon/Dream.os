#!/usr/bin/env python3
# SSOT Domain: infrastructure
"""
File Locking Manager - V2 Compliance Module
==========================================

High-level file locking management for V2 compliance.
SSOT: Single Source of Truth for high-level file locking operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

import time
from pathlib import Path
from typing import Any

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .file_locking_engine import FileLockEngine

from .file_locking_models import LockConfig, LockInfo, LockMetrics, LockResult, LockStatus


class FileLockManager:
    """High-level file locking manager."""

    def __init__(self, config: LockConfig = None):
        """Initialize file lock manager."""
        self.config = config or LockConfig()
        self._engine = None  # Lazy-loaded to avoid circular import

    @property
    def engine(self) -> "FileLockEngine":
        """Lazy-load engine to avoid circular import."""
        if self._engine is None:
            from .file_locking_engine import FileLockEngine
            self._engine = FileLockEngine(self.config)
        return self._engine

    def create_file_lock(self, filepath: str, metadata: dict[str, Any] = None) -> LockResult:
        """Create a file lock."""
        return self.engine.create_lock(filepath, metadata)

    def acquire_lock(self, filepath: str, metadata: dict[str, Any] = None) -> LockResult:
        """Acquire a file lock with retry logic."""
        lock_result = self.engine.create_lock(filepath, metadata)

        if not lock_result.success:
            return lock_result

        # Try to acquire lock with retry logic
        for attempt in range(self.config.max_retries):
            acquire_result = self.engine.acquire_lock(lock_result.lock_info)

            if acquire_result.success:
                return acquire_result

            if acquire_result.status == LockStatus.LOCKED:
                # Lock is held by another process, wait and retry
                time.sleep(self.config.retry_interval)
                continue
            else:
                # Error occurred, return immediately
                return acquire_result

        # Timeout reached
        return LockResult(
            success=False,
            status=LockStatus.TIMEOUT,
            error_message=f"Timeout after {self.config.max_retries} attempts",
            execution_time_ms=self.config.max_retries * self.config.retry_interval * 1000,
            retry_count=self.config.max_retries,
        )

    def release_lock(self, filepath: str) -> LockResult:
        """Release a file lock."""
        lock_file = f"{filepath}.lock"

        # Find the lock info
        lock_info = None
        for active_lock in self.engine._active_locks.values():
            if active_lock.lock_file == lock_file:
                lock_info = active_lock
                break

        if not lock_info:
            return LockResult(
                success=False, status=LockStatus.ERROR, error_message="Lock not found"
            )

        return self.engine.release_lock(lock_info)

    def is_locked(self, filepath: str) -> bool:
        """Check if file is locked."""
        return self.engine.is_locked(filepath)

    def cleanup_stale_locks(self) -> int:
        """Clean up stale locks."""
        return self.engine.cleanup_stale_locks()

    def get_active_locks(self) -> list[LockInfo]:
        """Get list of active locks."""
        return list(self.engine._active_locks.values())

    def get_lock_info(self, filepath: str) -> LockInfo | None:
        """Get lock information for a file."""
        lock_file = f"{filepath}.lock"
        return self.engine._active_locks.get(lock_file)

    def force_release_lock(self, filepath: str) -> LockResult:
        """Force release a lock (use with caution)."""
        lock_file = Path(f"{filepath}.lock")

        try:
            if lock_file.exists():
                lock_file.unlink()

            # Remove from active locks
            lock_key = f"{filepath}.lock"
            if lock_key in self.engine._active_locks:
                del self.engine._active_locks[lock_key]
                self.engine.metrics.active_locks = len(self.engine._active_locks)

            return LockResult(success=True, status=LockStatus.UNLOCKED, execution_time_ms=0.0)

        except Exception as e:
            return LockResult(success=False, status=LockStatus.ERROR, error_message=str(e))

    def get_metrics(self) -> LockMetrics:
        """Get locking metrics."""
        return self.engine.get_metrics()

    def reset_metrics(self) -> None:
        """Reset metrics."""
        self.engine.metrics = LockMetrics()

    def get_lock_summary(self) -> dict[str, Any]:
        """Get summary of lock status."""
        active_locks = self.get_active_locks()
        metrics = self.get_metrics()

        return {
            "active_locks": len(active_locks),
            "total_created": metrics.total_locks_created,
            "total_acquired": metrics.total_locks_acquired,
            "total_released": metrics.total_locks_released,
            "total_errors": metrics.total_errors,
            "total_timeouts": metrics.total_timeouts,
            "average_acquire_time_ms": metrics.average_acquire_time_ms,
            "average_release_time_ms": metrics.average_release_time_ms,
            "stale_cleanups": metrics.total_stale_cleanups,
        }

    # Batch operations
    def batch_acquire_locks(
        self, filepaths: list[str], metadata: dict[str, Any] = None
    ) -> dict[str, LockResult]:
        """Acquire multiple locks."""
        results = {}
        for filepath in filepaths:
            results[filepath] = self.acquire_lock(filepath, metadata)
        return results

    def batch_release_locks(self, filepaths: list[str]) -> dict[str, LockResult]:
        """Release multiple locks."""
        results = {}
        for filepath in filepaths:
            results[filepath] = self.release_lock(filepath)
        return results

    # Extended operations
    def extend_lock(self, filepath: str, duration: int) -> LockResult:
        """Extend lock duration (placeholder - locks are file-based, duration managed by stale_age)."""
        # File locks don't have explicit duration - they're managed by stale_age
        # This method exists for API compatibility
        lock_info = self.get_lock_info(filepath)
        if not lock_info:
            return LockResult(
                success=False, status=LockStatus.ERROR, error_message="Lock not found"
            )
        # Update timestamp to extend lock
        lock_info.timestamp = time.time()
        return LockResult(success=True, status=LockStatus.LOCKED, lock_info=lock_info)

    def cleanup_expired_locks(self) -> int:
        """Clean up expired locks (alias for cleanup_stale_locks)."""
        return self.cleanup_stale_locks()

    # Query operations (using LockQueries utility)
    def get_locks_by_process(self, pid: int) -> list[LockInfo]:
        """Get locks owned by specific process."""
        from .operations.lock_queries import LockQueries
        queries = LockQueries(self)
        return queries.get_locks_by_process(pid)

    def get_locks_by_thread(self, thread_id: str) -> list[LockInfo]:
        """Get locks owned by specific thread."""
        from .operations.lock_queries import LockQueries
        queries = LockQueries(self)
        return queries.get_locks_by_thread(thread_id)

    def get_locks_by_owner(self, owner: str) -> list[LockInfo]:
        """Get locks owned by specific owner."""
        from .operations.lock_queries import LockQueries
        queries = LockQueries(self)
        return queries.get_locks_by_owner(owner)

    def get_locks_by_type(self, lock_type: str) -> list[LockInfo]:
        """Get locks by type."""
        from .operations.lock_queries import LockQueries
        queries = LockQueries(self)
        return queries.get_locks_by_type(lock_type)

    def get_locks_by_duration(self, min_duration: int, max_duration: int = None) -> list[LockInfo]:
        """Get locks by duration range."""
        from .operations.lock_queries import LockQueries
        queries = LockQueries(self)
        return queries.get_locks_by_duration(min_duration, max_duration)

    def get_locks_by_metadata(self, metadata_key: str, metadata_value: Any) -> list[LockInfo]:
        """Get locks by metadata key-value pair."""
        from .operations.lock_queries import LockQueries
        queries = LockQueries(self)
        return queries.get_locks_by_metadata(metadata_key, metadata_value)

    def get_lock_statistics(self) -> dict[str, Any]:
        """Get lock statistics."""
        from .operations.lock_queries import LockQueries
        queries = LockQueries(self)
        return queries.get_lock_statistics()

    def find_conflicting_locks(self, filepath: str) -> list[LockInfo]:
        """Find locks that conflict with the given filepath."""
        from .operations.lock_queries import LockQueries
        queries = LockQueries(self)
        return queries.find_conflicting_locks(filepath)

    def get_lock_health_status(self) -> dict[str, Any]:
        """Get lock health status."""
        from .operations.lock_queries import LockQueries
        queries = LockQueries(self)
        return queries.get_lock_health_status()


class FileLockContext:
    """Context manager for file locking."""

    def __init__(self, manager: "FileLockManager", filepath: str, metadata: dict[str, Any] = None):
        """Initialize context manager."""
        self.manager = manager
        self.filepath = filepath
        self.metadata = metadata
        self.lock_result = None

    def __enter__(self):
        """Enter context and acquire lock."""
        self.lock_result = self.manager.acquire_lock(self.filepath, self.metadata)
        if not self.lock_result.success:
            raise RuntimeError(f"Failed to acquire lock: {self.lock_result.error_message}")
        return self.lock_result

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context and release lock."""
        if self.lock_result and self.lock_result.success:
            self.manager.release_lock(self.filepath)


# Global instance for backward compatibility
_global_file_lock_manager = None


def get_file_lock_manager() -> FileLockManager:
    """Get global file lock manager instance."""
    global _global_file_lock_manager

    if _global_file_lock_manager is None:
        _global_file_lock_manager = FileLockManager()

    return _global_file_lock_manager
