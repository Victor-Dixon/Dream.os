"""
Tests for System Clock - Infrastructure Domain

Tests for time management functionality.

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-12-06
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock

from src.infrastructure.time.system_clock import SystemClock, TimeConfig


class TestSystemClock:
    """Tests for SystemClock SSOT."""

    def test_system_clock_initialization(self):
        """Test SystemClock initializes correctly."""
        config = TimeConfig()
        clock = SystemClock(config)
        assert clock is not None

    def test_system_clock_now(self):
        """Test now() returns current time."""
        config = TimeConfig()
        clock = SystemClock(config)
        now = clock.now()
        assert isinstance(now, datetime)

    def test_system_clock_utc_now(self):
        """Test utcnow() returns UTC time."""
        config = TimeConfig()
        clock = SystemClock(config)
        utc_now = clock.utcnow()
        assert isinstance(utc_now, datetime)

    def test_system_clock_timestamp(self):
        """Test timestamp operations work correctly."""
        config = TimeConfig()
        clock = SystemClock(config)
        dt = clock.now()
        timestamp = clock.to_timestamp(dt)
        dt_from_ts = clock.from_timestamp(timestamp)
        assert isinstance(timestamp, float)
        assert isinstance(dt_from_ts, datetime)

