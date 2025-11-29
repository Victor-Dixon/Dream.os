"""
Unit tests for logging_utilities.py - NEXT PRIORITY

Tests LoggingManager class and logging operations.
Expanded to ≥85% coverage.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import logging
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.utilities.logging_utilities import LoggingManager, create_logging_manager


class TestLoggingManager:
    """Test suite for LoggingManager class."""

    @pytest.fixture
    def manager(self):
        """Create LoggingManager instance."""
        return LoggingManager()

    def test_manager_initialization(self, manager):
        """Test manager initialization."""
        assert manager is not None
        assert manager.log_level == logging.INFO
        assert manager.logger is not None
        assert manager.name == "LoggingManager"

    def test_manager_initialization_with_name(self):
        """Test manager initialization with custom name."""
        manager = LoggingManager()
        # Name should default to class name
        assert manager.name == "LoggingManager"

    def test_initialize(self, manager):
        """Test manager initialization."""
        with patch('logging.basicConfig') as mock_basic_config:
            result = manager.initialize()
            assert result is True
            mock_basic_config.assert_called_once_with(level=logging.INFO)

    def test_initialize_logs_message(self, manager):
        """Test that initialize logs a message."""
        with patch.object(manager.logger, 'info') as mock_info:
            manager.initialize()
            mock_info.assert_called_once_with("LoggingManager initialized")

    def test_cleanup(self, manager):
        """Test cleanup operation."""
        result = manager.cleanup()
        assert result is True

    def test_set_log_level(self, manager):
        """Test setting log level."""
        with patch('logging.getLogger') as mock_get_logger:
            mock_logger = MagicMock()
            mock_get_logger.return_value = mock_logger
            
            manager.set_log_level(logging.DEBUG)
            assert manager.log_level == logging.DEBUG
            mock_logger.setLevel.assert_called_once_with(logging.DEBUG)

    def test_set_log_level_info(self, manager):
        """Test setting log level to INFO."""
        manager.set_log_level(logging.INFO)
        assert manager.log_level == logging.INFO

    def test_set_log_level_warning(self, manager):
        """Test setting log level to WARNING."""
        manager.set_log_level(logging.WARNING)
        assert manager.log_level == logging.WARNING

    def test_set_log_level_error(self, manager):
        """Test setting log level to ERROR."""
        manager.set_log_level(logging.ERROR)
        assert manager.log_level == logging.ERROR

    def test_set_log_level_critical(self, manager):
        """Test setting log level to CRITICAL."""
        manager.set_log_level(logging.CRITICAL)
        assert manager.log_level == logging.CRITICAL

    def test_log_info(self, manager):
        """Test logging info message."""
        with patch.object(manager.logger, 'info') as mock_info:
            manager.log_info("Test info message")
            mock_info.assert_called_once_with("Test info message")

    def test_log_error(self, manager):
        """Test logging error message."""
        with patch.object(manager.logger, 'error') as mock_error:
            manager.log_error("Test error message")
            mock_error.assert_called_once_with("Test error message")

    def test_log_info_multiple_messages(self, manager):
        """Test logging multiple info messages."""
        with patch.object(manager.logger, 'info') as mock_info:
            manager.log_info("Message 1")
            manager.log_info("Message 2")
            assert mock_info.call_count == 2

    def test_log_error_multiple_messages(self, manager):
        """Test logging multiple error messages."""
        with patch.object(manager.logger, 'error') as mock_error:
            manager.log_error("Error 1")
            manager.log_error("Error 2")
            assert mock_error.call_count == 2

    def test_logger_inheritance(self, manager):
        """Test that logger is properly inherited from BaseUtility."""
        assert hasattr(manager, 'logger')
        assert manager.logger is not None
        assert isinstance(manager.logger, logging.Logger)

    def test_logger_name_matches_manager_name(self, manager):
        """Test that logger name matches manager name."""
        assert manager.logger.name == manager.name


class TestCreateLoggingManager:
    """Test suite for create_logging_manager function."""

    def test_create_logging_manager(self):
        """Test creating logging manager."""
        manager = create_logging_manager()
        assert manager is not None
        assert isinstance(manager, LoggingManager)

    def test_create_logging_manager_multiple_instances(self):
        """Test creating multiple logging manager instances."""
        manager1 = create_logging_manager()
        manager2 = create_logging_manager()
        assert manager1 is not manager2
        assert isinstance(manager1, LoggingManager)
        assert isinstance(manager2, LoggingManager)

    def test_create_logging_manager_initialized(self):
        """Test that created manager can be initialized."""
        manager = create_logging_manager()
        with patch('logging.basicConfig'):
            result = manager.initialize()
            assert result is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

