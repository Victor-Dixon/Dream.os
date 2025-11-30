"""
Tests for Unified Logging System
"""

import logging
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.core.unified_logging_system import (
    UnifiedLoggingSystem,
    get_logger,
    configure_logging,
    get_logging_system
)


class TestUnifiedLoggingSystem:
    """Test suite for UnifiedLoggingSystem class."""

    def test_init(self):
        """Test UnifiedLoggingSystem initialization."""
        system = UnifiedLoggingSystem()
        assert system._loggers == {}
        assert system._configured is False

    @patch('logging.basicConfig')
    def test_configure_default(self, mock_basic_config):
        """Test configure with default parameters."""
        system = UnifiedLoggingSystem()
        system.configure()
        
        assert system._configured is True
        mock_basic_config.assert_called_once()

    @patch('logging.basicConfig')
    def test_configure_custom_level(self, mock_basic_config):
        """Test configure with custom log level."""
        system = UnifiedLoggingSystem()
        system.configure(level="DEBUG")
        
        assert system._configured is True
        call_args = mock_basic_config.call_args
        assert call_args[1]['level'] == logging.DEBUG

    @patch('logging.basicConfig')
    def test_configure_with_log_file(self, mock_basic_config, tmp_path):
        """Test configure with log file."""
        log_file = tmp_path / "test.log"
        system = UnifiedLoggingSystem()
        system.configure(log_file=log_file)
        
        assert system._configured is True
        call_args = mock_basic_config.call_args
        handlers = call_args[1]['handlers']
        assert len(handlers) >= 1

    @patch('logging.basicConfig')
    def test_configure_custom_format(self, mock_basic_config):
        """Test configure with custom format string."""
        system = UnifiedLoggingSystem()
        custom_format = "%(levelname)s - %(message)s"
        system.configure(format_string=custom_format)
        
        call_args = mock_basic_config.call_args
        # Format is passed to handlers, verify it's configured
        assert system._configured is True

    @patch('logging.basicConfig')
    def test_configure_idempotent(self, mock_basic_config):
        """Test configure only runs once."""
        system = UnifiedLoggingSystem()
        system.configure()
        system.configure()  # Second call should be ignored
        
        assert mock_basic_config.call_count == 1

    def test_get_logger_creates_new(self):
        """Test get_logger creates new logger."""
        system = UnifiedLoggingSystem()
        logger1 = system.get_logger("test.module")
        
        assert isinstance(logger1, logging.Logger)
        assert logger1.name == "test.module"

    def test_get_logger_returns_same_instance(self):
        """Test get_logger returns same instance for same name."""
        system = UnifiedLoggingSystem()
        logger1 = system.get_logger("test.module")
        logger2 = system.get_logger("test.module")
        
        assert logger1 is logger2

    def test_get_logger_different_names(self):
        """Test get_logger returns different loggers for different names."""
        system = UnifiedLoggingSystem()
        logger1 = system.get_logger("module1")
        logger2 = system.get_logger("module2")
        
        assert logger1 is not logger2
        assert logger1.name == "module1"
        assert logger2.name == "module2"

    @patch('logging.FileHandler')
    @patch('logging.StreamHandler')
    @patch('logging.basicConfig')
    def test_get_handlers_with_file(self, mock_basic_config, mock_stream, mock_file, tmp_path):
        """Test _get_handlers includes file handler when log_file provided."""
        system = UnifiedLoggingSystem()
        log_file = tmp_path / "test.log"
        handlers = system._get_handlers(log_file)
        
        assert len(handlers) >= 2  # Console + File handler
        mock_file.assert_called_once()

    @patch('logging.StreamHandler')
    @patch('logging.basicConfig')
    def test_get_handlers_without_file(self, mock_basic_config, mock_stream):
        """Test _get_handlers only console handler when no log_file."""
        system = UnifiedLoggingSystem()
        handlers = system._get_handlers(None)
        
        assert len(handlers) == 1  # Only console handler


class TestModuleFunctions:
    """Test suite for module-level functions."""

    @patch('src.core.unified_logging_system._logging_system')
    def test_get_logger_function(self, mock_system):
        """Test get_logger module function."""
        mock_logger = MagicMock()
        mock_system.get_logger.return_value = mock_logger
        
        result = get_logger("test.module")
        
        mock_system.get_logger.assert_called_once_with("test.module")
        assert result == mock_logger

    @patch('src.core.unified_logging_system._logging_system')
    def test_configure_logging_function(self, mock_system):
        """Test configure_logging module function."""
        configure_logging(level="DEBUG", log_file=Path("test.log"))
        
        mock_system.configure.assert_called_once_with("DEBUG", Path("test.log"), None)

    @patch('src.core.unified_logging_system._logging_system')
    def test_get_logging_system_function(self, mock_system):
        """Test get_logging_system module function."""
        result = get_logging_system()
        
        assert result == mock_system

