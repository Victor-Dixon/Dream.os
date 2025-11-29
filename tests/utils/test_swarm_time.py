"""
Unit tests for swarm_time.py - Infrastructure Test Coverage Batch 10

Tests swarm time utility functions for centralized time management.
Target: ≥85% coverage, 5+ test methods.
"""

import pytest
from datetime import datetime
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.utils.swarm_time import (
    get_swarm_time,
    format_swarm_timestamp,
    format_swarm_timestamp_readable,
    format_swarm_timestamp_filename,
    get_swarm_time_display
)


class TestGetSwarmTime:
    """Test suite for get_swarm_time function."""

    def test_get_swarm_time_returns_datetime(self):
        """Test that get_swarm_time returns datetime object."""
        result = get_swarm_time()
        assert isinstance(result, datetime)

    def test_get_swarm_time_returns_current_time(self):
        """Test that get_swarm_time returns current local time."""
        before = datetime.now()
        result = get_swarm_time()
        after = datetime.now()
        
        assert before <= result <= after

    def test_get_swarm_time_is_local_time(self):
        """Test that get_swarm_time uses local system time."""
        result = get_swarm_time()
        # Should be close to datetime.now() (within 1 second)
        now = datetime.now()
        time_diff = abs((result - now).total_seconds())
        assert time_diff < 1.0


class TestFormatSwarmTimestamp:
    """Test suite for format_swarm_timestamp function."""

    def test_format_swarm_timestamp_with_none(self):
        """Test format_swarm_timestamp with None (uses current time)."""
        result = format_swarm_timestamp(None)
        assert isinstance(result, str)
        assert "T" in result  # ISO format contains T

    def test_format_swarm_timestamp_with_datetime(self):
        """Test format_swarm_timestamp with provided datetime."""
        dt = datetime(2025, 1, 27, 12, 30, 45)
        result = format_swarm_timestamp(dt)
        
        assert isinstance(result, str)
        assert "2025-01-27" in result
        assert "12:30:45" in result

    def test_format_swarm_timestamp_iso_format(self):
        """Test that format_swarm_timestamp returns ISO 8601 format."""
        dt = datetime(2025, 1, 27, 12, 30, 45, 123456)
        result = format_swarm_timestamp(dt)
        
        # ISO format: YYYY-MM-DDTHH:MM:SS.ffffff
        assert result.startswith("2025-01-27T12:30:45")
        assert "." in result  # Microseconds separator

    def test_format_swarm_timestamp_defaults_to_current(self):
        """Test format_swarm_timestamp defaults to current time when None."""
        before = datetime.now()
        result = format_swarm_timestamp()
        after = datetime.now()
        
        # Parse result back to datetime
        parsed = datetime.fromisoformat(result)
        assert before <= parsed <= after


class TestFormatSwarmTimestampReadable:
    """Test suite for format_swarm_timestamp_readable function."""

    def test_format_swarm_timestamp_readable_with_none(self):
        """Test format_swarm_timestamp_readable with None."""
        result = format_swarm_timestamp_readable(None)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_format_swarm_timestamp_readable_with_datetime(self):
        """Test format_swarm_timestamp_readable with provided datetime."""
        dt = datetime(2025, 1, 27, 12, 30, 45)
        result = format_swarm_timestamp_readable(dt)
        
        assert result == "2025-01-27 12:30:45"

    def test_format_swarm_timestamp_readable_format(self):
        """Test that format_swarm_timestamp_readable uses correct format."""
        dt = datetime(2025, 1, 27, 9, 5, 3)
        result = format_swarm_timestamp_readable(dt)
        
        # Format: YYYY-MM-DD HH:MM:SS
        assert result == "2025-01-27 09:05:03"

    def test_format_swarm_timestamp_readable_defaults_to_current(self):
        """Test format_swarm_timestamp_readable defaults to current time."""
        before = datetime.now()
        result = format_swarm_timestamp_readable()
        after = datetime.now()
        
        # Parse result (strip microseconds for comparison)
        parsed = datetime.strptime(result, "%Y-%m-%d %H:%M:%S")
        before_no_micro = before.replace(microsecond=0)
        after_no_micro = after.replace(microsecond=0)
        assert before_no_micro <= parsed <= after_no_micro


class TestFormatSwarmTimestampFilename:
    """Test suite for format_swarm_timestamp_filename function."""

    def test_format_swarm_timestamp_filename_with_none(self):
        """Test format_swarm_timestamp_filename with None."""
        result = format_swarm_timestamp_filename(None)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_format_swarm_timestamp_filename_with_datetime(self):
        """Test format_swarm_timestamp_filename with provided datetime."""
        dt = datetime(2025, 1, 27, 12, 30, 45, 123456)
        result = format_swarm_timestamp_filename(dt)
        
        assert result == "20250127_123045_123456"

    def test_format_swarm_timestamp_filename_format(self):
        """Test that format_swarm_timestamp_filename uses correct format."""
        dt = datetime(2025, 1, 5, 9, 5, 3, 789012)
        result = format_swarm_timestamp_filename(dt)
        
        # Format: YYYYMMDD_HHMMSS_ffffff
        assert result == "20250105_090503_789012"

    def test_format_swarm_timestamp_filename_safe_for_filesystem(self):
        """Test that format_swarm_timestamp_filename is filesystem-safe."""
        dt = datetime(2025, 1, 27, 12, 30, 45, 123456)
        result = format_swarm_timestamp_filename(dt)
        
        # Should not contain characters that are problematic in filenames
        assert ":" not in result
        assert "/" not in result
        assert "\\" not in result
        assert " " not in result

    def test_format_swarm_timestamp_filename_defaults_to_current(self):
        """Test format_swarm_timestamp_filename defaults to current time."""
        before = datetime.now()
        result = format_swarm_timestamp_filename()
        after = datetime.now()
        
        # Parse result (YYYYMMDD_HHMMSS_ffffff) - strip microseconds for comparison
        date_part = result[:8]
        time_part = result[9:15]
        parsed = datetime.strptime(f"{date_part}_{time_part}", "%Y%m%d_%H%M%S")
        before_no_micro = before.replace(microsecond=0)
        after_no_micro = after.replace(microsecond=0)
        assert before_no_micro <= parsed <= after_no_micro


class TestGetSwarmTimeDisplay:
    """Test suite for get_swarm_time_display function."""

    def test_get_swarm_time_display_returns_string(self):
        """Test that get_swarm_time_display returns string."""
        result = get_swarm_time_display()
        assert isinstance(result, str)

    def test_get_swarm_time_display_format(self):
        """Test that get_swarm_time_display uses readable format."""
        result = get_swarm_time_display()
        
        # Should match readable format: YYYY-MM-DD HH:MM:SS
        assert len(result) == 19  # "YYYY-MM-DD HH:MM:SS"
        assert result[4] == "-"
        assert result[7] == "-"
        assert result[10] == " "
        assert result[13] == ":"
        assert result[16] == ":"

    def test_get_swarm_time_display_current_time(self):
        """Test that get_swarm_time_display returns current time."""
        before = datetime.now()
        result = get_swarm_time_display()
        after = datetime.now()
        
        parsed = datetime.strptime(result, "%Y-%m-%d %H:%M:%S")
        # Strip microseconds for comparison
        before_no_micro = before.replace(microsecond=0)
        after_no_micro = after.replace(microsecond=0)
        assert before_no_micro <= parsed <= after_no_micro

    def test_get_swarm_time_display_consistent_with_readable(self):
        """Test that get_swarm_time_display matches readable format."""
        result_display = get_swarm_time_display()
        result_readable = format_swarm_timestamp_readable()
        
        assert result_display == result_readable


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

