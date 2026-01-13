#!/usr/bin/env python3
# SSOT Domain: infrastructure
"""
File Locking Engine - V2 Compliance Module
==========================================

Core engine for file locking operations. Combines operations and platform-specific functionality.
SSOT: Single Source of Truth for file locking engine operations.

Author: Agent-7 (Web Development Specialist) - Circular Import Fix
License: MIT
"""

import os
import platform
import threading
import time
from pathlib import Path
from typing import Any

from .file_locking_models import LockConfig, LockInfo, LockMetrics, LockResult, LockStatus


class FileLockEngine:
    """Core file locking engine combining operations and platform functionality."""

    def __init__(self, config: LockConfig = None):
        """Initialize file lock engine."""
        self.config = config or LockConfig()
        self._active_locks: dict[str, LockInfo] = {}
        self._lock = threading.Lock()
        self.metrics = LockMetrics()

        # Platform detection
        self._is_windows = platform.system() == "Windows"
        
        # Load platform modules immediately (needed for operations)
        self._load_platform_modules()

        # Platform-specific modules (lazy-loaded to avoid circular imports)
        self._msvcrt = None
        self._fcntl = None
        self._operations = None
        self._platform = None

    @property
    def operations(self):
        """Lazy-load operations to avoid circular import."""
        if self._operations is None:
            from .file_locking_engine_operations import FileLockEngineOperations
            self._operations = FileLockEngineOperations(self, logger=None)
        return self._operations

    @property
    def platform_ops(self):
        """Lazy-load platform operations to avoid circular import."""
        if self._platform is None:
            from .file_locking_engine_platform import FileLockEnginePlatform
            self._platform = FileLockEnginePlatform(self, logger=None)
        return self._platform

    def _load_platform_modules(self):
        """Load platform-specific modules."""
        if self._is_windows:
            try:
                import msvcrt
                self._msvcrt = msvcrt
            except ImportError:
                self._msvcrt = None
        else:
            try:
                import fcntl
                self._fcntl = fcntl
            except ImportError:
                self._fcntl = None

    def create_lock(self, filepath: str, metadata: dict[str, Any] = None) -> LockResult:
        """Create a lock info object."""
        lock_file = f"{filepath}.lock"
        lock_info = LockInfo(
            lock_file=lock_file,
            pid=os.getpid(),
            thread_id=str(threading.current_thread().ident),
            timestamp=time.time(),
            process_name=os.path.basename(__file__),
            metadata=metadata or {},
        )

        return LockResult(
            success=True,
            status=LockStatus.UNLOCKED,
            lock_info=lock_info,
            execution_time_ms=0.0,
        )

    def acquire_lock(self, lock_info: LockInfo) -> LockResult:
        """Acquire a file lock."""
        return self.operations.acquire_lock(lock_info)

    def release_lock(self, lock_info: LockInfo) -> LockResult:
        """Release a file lock."""
        return self.operations.release_lock(lock_info)

    def is_locked(self, filepath: str) -> bool:
        """Check if file is locked."""
        lock_file = f"{filepath}.lock"
        with self._lock:
            return lock_file in self._active_locks

    def cleanup_stale_locks(self) -> int:
        """Clean up stale locks."""
        return self.operations.cleanup_stale_locks()

    def _update_metrics(self, operation: str, success: bool, execution_time: float) -> None:
        """Update metrics for an operation."""
        if not self.config.enable_metrics:
            return

        if operation == "acquire_lock":
            if success:
                self.metrics.total_locks_acquired += 1
            else:
                self.metrics.total_errors += 1
        elif operation == "release_lock":
            if success:
                self.metrics.total_locks_released += 1
            else:
                self.metrics.total_errors += 1
        elif operation == "cleanup_stale_locks":
            if success:
                self.metrics.total_stale_cleanups += 1

        self.metrics.total_execution_time_ms += execution_time * 1000
        self.metrics.active_locks = len(self._active_locks)
        self.metrics.update_averages()

    def get_metrics(self) -> LockMetrics:
        """Get current metrics."""
        return self.metrics

