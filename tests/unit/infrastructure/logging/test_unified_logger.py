"""
Tests for Unified Logger - Infrastructure Domain

Tests for unified logger implementation.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
"""

import pytest
from unittest.mock import Mock, patch, MagicMock

from src.infrastructure.logging.unified_logger import UnifiedLogger, LoggingConfig, LogLevel


class TestUnifiedLogger:
    """Tests for UnifiedLogger SSOT."""

    def test_unified_logger_initialization(self):
        """Test UnifiedLogger initializes correctly."""
        config = LoggingConfig()
        logger = UnifiedLogger(name="test_logger", config=config)
        assert logger.name == "test_logger"
        assert logger.config == config

    def test_unified_logger_with_default_config(self):
        """Test UnifiedLogger with default config."""
        config = LoggingConfig()
        logger = UnifiedLogger(name="test_logger", config=config)
        assert logger.name == "test_logger"
        assert logger.config is not None

    def test_unified_logger_debug(self):
        """Test debug logging."""
        config = LoggingConfig()
        logger = UnifiedLogger(name="test_logger", config=config)
        # Should not raise exception
        logger.debug("Test debug message")

    def test_unified_logger_info(self):
        """Test info logging."""
        config = LoggingConfig()
        logger = UnifiedLogger(name="test_logger", config=config)
        # Should not raise exception
        logger.info("Test info message")

    def test_unified_logger_warning(self):
        """Test warning logging."""
        config = LoggingConfig()
        logger = UnifiedLogger(name="test_logger", config=config)
        # Should not raise exception
        logger.warning("Test warning message")

    def test_unified_logger_error(self):
        """Test error logging."""
        config = LoggingConfig()
        logger = UnifiedLogger(name="test_logger", config=config)
        # Should not raise exception
        logger.error("Test error message")

    def test_unified_logger_critical(self):
        """Test critical logging."""
        config = LoggingConfig()
        logger = UnifiedLogger(name="test_logger", config=config)
        # Should not raise exception
        logger.critical("Test critical message")

    def test_unified_logger_with_context(self):
        """Test logging with context."""
        config = LoggingConfig()
        logger = UnifiedLogger(name="test_logger", config=config)
        # Should not raise exception - use non-conflicting context keys
        logger.info("Test message", component="test", ver="1.0")

    def test_unified_logger_different_log_levels(self):
        """Test logger with different log levels."""
        config_debug = LoggingConfig(level=LogLevel.DEBUG)
        logger_debug = UnifiedLogger(name="debug_logger", config=config_debug)
        assert logger_debug.config.level == LogLevel.DEBUG

        config_info = LoggingConfig(level=LogLevel.INFO)
        logger_info = UnifiedLogger(name="info_logger", config=config_info)
        assert logger_info.config.level == LogLevel.INFO

