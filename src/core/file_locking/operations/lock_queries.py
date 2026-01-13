"""
<!-- SSOT Domain: core -->

File Lock Queries - V2 Compliance Module
=======================================

File locking query functionality.

V2 Compliance: < 300 lines, single responsibility, lock queries.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from typing import Any

from ..file_locking_manager import FileLockManager
from ..file_locking_models import LockInfo


class LockQueries:
    """File locking query functionality."""

    def __init__(self, manager: FileLockManager):
        """Initialize lock queries."""
        self.manager = manager

    def get_locks_by_process(self, pid: int) -> list[LockInfo]:
        """Get locks owned by specific process."""
        active_locks = self.manager.get_active_locks()
        return [lock for lock in active_locks if lock.pid == pid]

    def get_locks_by_thread(self, thread_id: str) -> list[LockInfo]:
        """Get locks owned by specific thread."""
        active_locks = self.manager.get_active_locks()
        return [lock for lock in active_locks if lock.thread_id == thread_id]

    def get_locks_by_owner(self, owner: str) -> list[LockInfo]:
        """Get locks owned by specific owner (uses process_name or metadata['owner'])."""
        active_locks = self.manager.get_active_locks()
        return [
            lock
            for lock in active_locks
            if lock.process_name == owner
            or (lock.metadata and lock.metadata.get("owner") == owner)
        ]

    def get_locks_by_type(self, lock_type: str) -> list[LockInfo]:
        """Get locks by type (uses metadata['lock_type'])."""
        active_locks = self.manager.get_active_locks()
        return [
            lock
            for lock in active_locks
            if lock.metadata and lock.metadata.get("lock_type") == lock_type
        ]

    def get_locks_by_duration(self, min_duration: int, max_duration: int = None) -> list[LockInfo]:
        """Get locks by duration range (calculates from timestamp)."""
        import time

        active_locks = self.manager.get_active_locks()
        filtered_locks = []

        for lock in active_locks:
            duration = time.time() - lock.timestamp
            if min_duration <= duration:
                if max_duration is None or duration <= max_duration:
                    filtered_locks.append(lock)

        return filtered_locks

    def get_locks_by_metadata(self, metadata_key: str, metadata_value: Any) -> list[LockInfo]:
        """Get locks by metadata key-value pair."""
        active_locks = self.manager.get_active_locks()
        return [
            lock
            for lock in active_locks
            if lock.metadata and lock.metadata.get(metadata_key) == metadata_value
        ]

    def get_lock_statistics(self) -> dict[str, Any]:
        """Get lock statistics."""
        import time

        active_locks = self.manager.get_active_locks()

        if not active_locks:
            return {
                "total_locks": 0,
                "locks_by_type": {},
                "locks_by_owner": {},
                "average_duration": 0,
            }

        locks_by_type = {}
        locks_by_owner = {}
        total_duration = 0

        for lock in active_locks:
            # Count by type (from metadata)
            lock_type = lock.metadata.get("lock_type", "default") if lock.metadata else "default"
            locks_by_type[lock_type] = locks_by_type.get(lock_type, 0) + 1

            # Count by owner (process_name or metadata)
            owner = lock.process_name or (
                lock.metadata.get("owner", "unknown") if lock.metadata else "unknown"
            )
            locks_by_owner[owner] = locks_by_owner.get(owner, 0) + 1

            # Sum duration (calculate from timestamp)
            duration = time.time() - lock.timestamp
            total_duration += duration

        return {
            "total_locks": len(active_locks),
            "locks_by_type": locks_by_type,
            "locks_by_owner": locks_by_owner,
            "average_duration": (total_duration / len(active_locks) if active_locks else 0),
        }

    def find_conflicting_locks(self, filepath: str) -> list[LockInfo]:
        """Find locks that conflict with the given filepath (extracts from lock_file)."""
        active_locks = self.manager.get_active_locks()
        conflicting_locks = []

        for lock in active_locks:
            # Extract filepath from lock_file (removes .lock extension)
            lock_filepath = lock.lock_file.replace(".lock", "")
            if lock_filepath == filepath:
                conflicting_locks.append(lock)

        return conflicting_locks

    def get_lock_health_status(self) -> dict[str, Any]:
        """Get lock health status."""
        metrics = self.manager.get_metrics()
        active_locks = self.manager.get_active_locks()

        # Calculate success rate from metrics
        total_ops = metrics.total_locks_acquired + metrics.total_errors
        success_rate = (
            (metrics.total_locks_acquired / total_ops) if total_ops > 0 else 1.0
        )

        return {
            "total_locks": len(active_locks),
            "active_locks": len(active_locks),
            "total_errors": metrics.total_errors,
            "total_timeouts": metrics.total_timeouts,
            "success_rate": success_rate,
            "health_status": "healthy" if success_rate > 0.9 else "degraded",
        }
