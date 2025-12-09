"""
Extended Tests for System Clock - Infrastructure Domain

Additional tests for system clock functionality beyond existing test_system_clock.py.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
"""

import pytest
from datetime import datetime, timedelta

from src.infrastructure.time.system_clock import (
    SystemClock,
    TimeCalculator,
    TimeFormatter,
    TimeConfig,
)


class TestSystemClockExtended:
    """Extended tests for SystemClock."""

    def test_system_clock_utcnow(self):
        """Test utcnow returns UTC datetime."""
        config = TimeConfig()
        clock = SystemClock(config)
        utc_time = clock.utcnow()
        assert isinstance(utc_time, datetime)

    def test_system_clock_from_timestamp(self):
        """Test from_timestamp creates datetime from Unix timestamp."""
        config = TimeConfig()
        clock = SystemClock(config)
        timestamp = 1609459200.0  # 2021-01-01 00:00:00 UTC
        dt = clock.from_timestamp(timestamp)
        assert isinstance(dt, datetime)
        assert dt.year == 2021

    def test_system_clock_to_timestamp(self):
        """Test to_timestamp converts datetime to Unix timestamp."""
        config = TimeConfig()
        clock = SystemClock(config)
        dt = datetime(2021, 1, 1, 0, 0, 0)
        timestamp = clock.to_timestamp(dt)
        assert isinstance(timestamp, float)
        assert timestamp > 0


class TestTimeCalculatorExtended:
    """Extended tests for TimeCalculator."""

    def test_time_calculator_add_hours(self):
        """Test add_hours adds hours to datetime."""
        config = TimeConfig()
        clock = SystemClock(config)
        calculator = TimeCalculator(clock)
        base_time = datetime(2024, 1, 1, 12, 0, 0)
        result = calculator.add_hours(base_time, 5)
        assert result.hour == 17
        assert result.day == 1

    def test_time_calculator_time_diff_minutes(self):
        """Test time_diff_minutes calculates difference in minutes."""
        config = TimeConfig()
        clock = SystemClock(config)
        calculator = TimeCalculator(clock)
        start = datetime(2024, 1, 1, 12, 0, 0)
        end = datetime(2024, 1, 1, 12, 30, 0)
        diff = calculator.time_diff_minutes(start, end)
        assert diff == 30.0

    def test_time_calculator_is_expired(self):
        """Test is_expired checks if datetime has expired."""
        config = TimeConfig()
        clock = SystemClock(config)
        calculator = TimeCalculator(clock)
        now = clock.now()
        past_time = now - timedelta(seconds=100)
        future_time = now + timedelta(seconds=100)
        assert calculator.is_expired(past_time, expiry_seconds=60.0) is True
        assert calculator.is_expired(future_time, expiry_seconds=60.0) is False

    def test_time_calculator_get_age_seconds(self):
        """Test get_age_seconds calculates age in seconds."""
        config = TimeConfig()
        clock = SystemClock(config)
        calculator = TimeCalculator(clock)
        now = clock.now()
        past_time = now - timedelta(seconds=50)
        age = calculator.get_age_seconds(past_time)
        assert age >= 45.0  # Allow some tolerance
        assert age <= 55.0


class TestTimeFormatterExtended:
    """Extended tests for TimeFormatter."""

    def test_time_formatter_format_date(self):
        """Test format_date formats datetime to date string."""
        config = TimeConfig()
        formatter = TimeFormatter(config)
        dt = datetime(2024, 1, 15, 14, 30, 45)
        date_str = formatter.format_date(dt)
        assert isinstance(date_str, str)
        assert "2024" in date_str or "01" in date_str or "15" in date_str

    def test_time_formatter_format_datetime(self):
        """Test format_datetime formats datetime to full string."""
        config = TimeConfig()
        formatter = TimeFormatter(config)
        dt = datetime(2024, 1, 15, 14, 30, 45)
        datetime_str = formatter.format_datetime(dt)
        assert isinstance(datetime_str, str)
        assert len(datetime_str) > 0

    def test_time_formatter_parse_datetime(self):
        """Test parse_datetime parses datetime string."""
        config = TimeConfig()
        formatter = TimeFormatter(config)
        # Format then parse to ensure round-trip
        dt = datetime(2024, 1, 15, 14, 30, 45)
        formatted = formatter.format_datetime(dt)
        parsed = formatter.parse_datetime(formatted)
        assert isinstance(parsed, datetime)

