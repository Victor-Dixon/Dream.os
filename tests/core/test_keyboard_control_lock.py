"""
Unit tests for keyboard_control_lock.py - NEXT PRIORITY

Tests keyboard control lock functionality for preventing race conditions.
Expanded to ≥85% coverage.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import threading
import time
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.keyboard_control_lock import (
    keyboard_control,
    is_locked,
    get_current_holder,
    acquire_lock,
    release_lock
)


class TestKeyboardControl:
    """Test suite for keyboard_control context manager."""

    def test_keyboard_control_acquires_lock(self):
        """Test that keyboard_control acquires lock."""
        with keyboard_control("test_source"):
            assert is_locked() is True

    def test_keyboard_control_releases_lock(self):
        """Test that keyboard_control releases lock after context."""
        with keyboard_control("test_source"):
            pass
        assert is_locked() is False

    def test_keyboard_control_sets_current_holder(self):
        """Test that keyboard_control sets current holder."""
        with keyboard_control("test_source"):
            holder = get_current_holder()
            assert holder == "test_source"

    def test_keyboard_control_clears_holder_on_exit(self):
        """Test that keyboard_control clears holder on exit."""
        with keyboard_control("test_source"):
            pass
        assert get_current_holder() is None

    def test_keyboard_control_default_source(self):
        """Test keyboard_control with default source."""
        with keyboard_control():
            holder = get_current_holder()
            assert holder == "unknown"

    def test_keyboard_control_custom_source(self):
        """Test keyboard_control with custom source."""
        with keyboard_control("discord_bot"):
            holder = get_current_holder()
            assert holder == "discord_bot"

    def test_keyboard_control_nested_blocks(self):
        """Test that nested keyboard_control blocks timeout correctly."""
        with keyboard_control("outer"):
            assert get_current_holder() == "outer"
            # Lock is already held, so inner should timeout
            with pytest.raises(RuntimeError):
                with keyboard_control("inner"):
                    pass
        assert get_current_holder() is None

    def test_keyboard_control_exception_handling(self):
        """Test that keyboard_control releases lock on exception."""
        try:
            with keyboard_control("test_source"):
                raise ValueError("Test error")
        except ValueError:
            pass
        assert is_locked() is False
        assert get_current_holder() is None

    def test_keyboard_control_exception_propagates(self):
        """Test that exceptions in context are propagated."""
        with pytest.raises(ValueError):
            with keyboard_control("test_source"):
                raise ValueError("Test error")

    @patch('src.core.keyboard_control_lock.logger')
    def test_keyboard_control_logs_acquire(self, mock_logger):
        """Test that keyboard_control logs lock acquisition."""
        with keyboard_control("test_source"):
            mock_logger.debug.assert_any_call("🔒 Keyboard lock acquired by: test_source")

    @patch('src.core.keyboard_control_lock.logger')
    def test_keyboard_control_logs_release(self, mock_logger):
        """Test that keyboard_control logs lock release."""
        with keyboard_control("test_source"):
            pass
        mock_logger.debug.assert_any_call("🔓 Keyboard lock released by: test_source")

    @patch('src.core.keyboard_control_lock.logger')
    def test_keyboard_control_logs_error(self, mock_logger):
        """Test that keyboard_control logs errors."""
        try:
            with keyboard_control("test_source"):
                raise ValueError("Test error")
        except ValueError:
            pass
        mock_logger.error.assert_called_once()


class TestIsLocked:
    """Test suite for is_locked function."""

    def test_is_locked_false_when_unlocked(self):
        """Test is_locked returns False when lock is not held."""
        assert is_locked() is False

    def test_is_locked_true_when_locked(self):
        """Test is_locked returns True when lock is held."""
        with keyboard_control("test_source"):
            assert is_locked() is True

    def test_is_locked_false_after_release(self):
        """Test is_locked returns False after lock is released."""
        with keyboard_control("test_source"):
            pass
        assert is_locked() is False


class TestGetCurrentHolder:
    """Test suite for get_current_holder function."""

    def test_get_current_holder_none_when_unlocked(self):
        """Test get_current_holder returns None when unlocked."""
        assert get_current_holder() is None

    def test_get_current_holder_returns_source(self):
        """Test get_current_holder returns source when locked."""
        with keyboard_control("test_source"):
            assert get_current_holder() == "test_source"

    def test_get_current_holder_returns_none_after_release(self):
        """Test get_current_holder returns None after release."""
        with keyboard_control("test_source"):
            pass
        assert get_current_holder() is None

    def test_get_current_holder_different_sources(self):
        """Test get_current_holder with different sources."""
        with keyboard_control("source1"):
            assert get_current_holder() == "source1"
        with keyboard_control("source2"):
            assert get_current_holder() == "source2"


class TestAcquireLock:
    """Test suite for acquire_lock function."""

    def test_acquire_lock_success(self):
        """Test successfully acquiring lock."""
        result = acquire_lock("test_source")
        assert result is True
        assert is_locked() is True
        assert get_current_holder() == "test_source"
        release_lock("test_source")

    def test_acquire_lock_sets_holder(self):
        """Test that acquire_lock sets current holder."""
        acquire_lock("test_source")
        assert get_current_holder() == "test_source"
        release_lock("test_source")

    @patch('src.core.keyboard_control_lock.logger')
    def test_acquire_lock_logs(self, mock_logger):
        """Test that acquire_lock logs acquisition."""
        acquire_lock("test_source")
        mock_logger.debug.assert_called_with("🔒 Keyboard lock manually acquired by: test_source")
        release_lock("test_source")

    def test_acquire_lock_custom_timeout(self):
        """Test acquire_lock with custom timeout."""
        result = acquire_lock("test_source", timeout=1.0)
        assert result is True
        release_lock("test_source")

    def test_acquire_lock_when_already_locked(self):
        """Test acquire_lock when lock is already held."""
        acquire_lock("source1")
        # Try to acquire again - should timeout
        result = acquire_lock("source2", timeout=0.1)
        assert result is False
        release_lock("source1")


class TestReleaseLock:
    """Test suite for release_lock function."""

    def test_release_lock_success(self):
        """Test successfully releasing lock."""
        acquire_lock("test_source")
        release_lock("test_source")
        assert is_locked() is False
        assert get_current_holder() is None

    def test_release_lock_clears_holder(self):
        """Test that release_lock clears current holder."""
        acquire_lock("test_source")
        release_lock("test_source")
        assert get_current_holder() is None

    @patch('src.core.keyboard_control_lock.logger')
    def test_release_lock_logs(self, mock_logger):
        """Test that release_lock logs release."""
        acquire_lock("test_source")
        release_lock("test_source")
        mock_logger.debug.assert_any_call("🔓 Keyboard lock manually released by: test_source")

    @patch('src.core.keyboard_control_lock.logger')
    def test_release_lock_mismatch_warning(self, mock_logger):
        """Test that release_lock warns on mismatch."""
        acquire_lock("source1")
        release_lock("source2")  # Different source
        mock_logger.warning.assert_called_once()
        assert "mismatch" in mock_logger.warning.call_args[0][0].lower()
        # Clean up
        if is_locked():
            release_lock("source1")

    def test_release_lock_after_context_manager(self):
        """Test release_lock after context manager."""
        with keyboard_control("test_source"):
            pass
        # Lock should already be released
        assert is_locked() is False


class TestLockTimeout:
    """Test suite for lock timeout behavior."""

    def test_lock_timeout_prevents_deadlock(self):
        """Test that lock timeout prevents deadlocks."""
        acquire_lock("source1")
        # Try to acquire with short timeout
        result = acquire_lock("source2", timeout=0.1)
        assert result is False
        release_lock("source1")

    def test_keyboard_control_timeout_raises_error(self):
        """Test that keyboard_control raises error on timeout."""
        acquire_lock("source1")
        # Try to use context manager while lock is held
        # This should timeout and raise RuntimeError
        with pytest.raises(RuntimeError):
            with keyboard_control("source2"):
                pass
        release_lock("source1")


class TestConcurrentAccess:
    """Test suite for concurrent access scenarios."""

    def test_sequential_access(self):
        """Test sequential lock acquisition."""
        with keyboard_control("source1"):
            assert get_current_holder() == "source1"
        with keyboard_control("source2"):
            assert get_current_holder() == "source2"

    def test_lock_exclusivity(self):
        """Test that lock ensures exclusive access."""
        lock_acquired = threading.Event()
        thread2_result = [None]
        
        def thread1():
            with keyboard_control("thread1"):
                lock_acquired.set()
                time.sleep(0.1)
        
        def thread2():
            lock_acquired.wait()
            # Try to acquire lock - should timeout since thread1 holds it
            thread2_result[0] = acquire_lock("thread2", timeout=0.05)
        
        t1 = threading.Thread(target=thread1)
        t2 = threading.Thread(target=thread2)
        
        t1.start()
        t2.start()
        
        t1.join()
        t2.join()
        
        # Thread2 should have failed to acquire lock due to timeout
        assert thread2_result[0] is False
        assert is_locked() is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

