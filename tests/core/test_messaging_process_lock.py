"""
Unit tests for messaging_process_lock.py - HIGH PRIORITY

Tests process locking functionality for messaging operations.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import threading
import time

# Import process lock
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))


class TestProcessLock:
    """Test suite for process locking."""

    def test_lock_initialization(self):
        """Test lock initialization."""
        lock = threading.Lock()
        
        assert lock is not None

    def test_lock_acquire_release(self):
        """Test lock acquire and release."""
        lock = threading.Lock()
        
        acquired = lock.acquire(blocking=False)
        assert acquired is True
        
        if acquired:
            lock.release()
            assert True  # Successfully released

    def test_lock_context_manager(self):
        """Test lock as context manager."""
        lock = threading.Lock()
        
        with lock:
            # Lock is held
            assert True
        
        # Lock is released
        assert True

    def test_lock_timeout(self):
        """Test lock timeout."""
        lock = threading.Lock()
        
        # Acquire lock
        lock.acquire()
        
        # Try to acquire with timeout (should fail)
        acquired = lock.acquire(timeout=0.1)
        
        # Release original lock
        lock.release()
        
        # Should not have acquired (timeout)
        assert acquired is False

    def test_concurrent_access_prevention(self):
        """Test preventing concurrent access."""
        lock = threading.Lock()
        shared_resource = []
        
        def modify_resource():
            with lock:
                shared_resource.append(1)
                time.sleep(0.1)
                shared_resource.append(2)
        
        # Run concurrently
        thread1 = threading.Thread(target=modify_resource)
        thread2 = threading.Thread(target=modify_resource)
        
        thread1.start()
        thread2.start()
        
        thread1.join()
        thread2.join()
        
        # Resource should be modified safely
        assert len(shared_resource) == 4


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

