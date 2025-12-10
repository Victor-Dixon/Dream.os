"""
Tests for Standard Logger - Infrastructure Domain

Tests for standard logger implementation.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
"""

import pytest
from unittest.mock import Mock, patch, MagicMock

from src.infrastructure.logging.std_logger import StdLogger
from src.domain.ports.logger import LogLevel


class TestStdLogger:
    """Tests for StdLogger SSOT."""

    def test_std_logger_initialization(self):
        """Test StdLogger initializes correctly."""
        logger = StdLogger(name="test_logger")
        assert hasattr(logger, '_logger')
        assert logger._logger is not None

    def test_std_logger_debug(self):
        """Test debug logging."""
        logger = StdLogger(name="test_logger")
        # Should not raise exception
        logger.debug("Test debug message")

    def test_std_logger_info(self):
        """Test info logging."""
        logger = StdLogger(name="test_logger")
        # Should not raise exception
        logger.info("Test info message")

    def test_std_logger_warning(self):
        """Test warning logging."""
        logger = StdLogger(name="test_logger")
        # Should not raise exception
        logger.warning("Test warning message")

    def test_std_logger_error(self):
        """Test error logging."""
        logger = StdLogger(name="test_logger")
        # Should not raise exception
        logger.error("Test error message")

    def test_std_logger_critical(self):
        """Test critical logging."""
        logger = StdLogger(name="test_logger")
        # Should not raise exception
        logger.critical("Test critical message")

    def test_std_logger_with_context(self):
        """Test logging with context."""
        logger = StdLogger(name="test_logger")
        # Should not raise exception - use non-conflicting context keys
        logger.info("Test message", component="test", ver="1.0")

