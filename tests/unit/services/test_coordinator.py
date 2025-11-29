"""
Unit tests for coordinator.py
"""

import pytest
from unittest.mock import Mock, MagicMock
from src.services.coordinator import Coordinator


class TestCoordinator:
    """Tests for Coordinator class."""

    def test_init(self):
        """Test Coordinator initialization."""
        coordinator = Coordinator("test_coordinator")
        assert coordinator.name == "test_coordinator"
        assert coordinator.logger is None
        assert coordinator.status["name"] == "test_coordinator"
        assert coordinator.status["status"] == "active"

    def test_init_with_logger(self):
        """Test Coordinator initialization with logger."""
        mock_logger = Mock()
        coordinator = Coordinator("test_coordinator", mock_logger)
        assert coordinator.name == "test_coordinator"
        assert coordinator.logger == mock_logger

    def test_get_status(self):
        """Test getting coordinator status."""
        coordinator = Coordinator("test_coordinator")
        status = coordinator.get_status()
        assert status["name"] == "test_coordinator"
        assert status["status"] == "active"

    def test_get_name(self):
        """Test getting coordinator name."""
        coordinator = Coordinator("test_coordinator")
        assert coordinator.get_name() == "test_coordinator"

    def test_shutdown(self):
        """Test coordinator shutdown."""
        mock_logger = Mock()
        coordinator = Coordinator("test_coordinator", mock_logger)
        coordinator.shutdown()
        assert coordinator.status["status"] == "shutdown"
        mock_logger.info.assert_called_once_with("Coordinator test_coordinator shut down")

    def test_shutdown_without_logger(self):
        """Test shutdown without logger (should not error)."""
        coordinator = Coordinator("test_coordinator")
        coordinator.shutdown()
        assert coordinator.status["status"] == "shutdown"



