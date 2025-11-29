"""
Tests for coordinator.py

Comprehensive tests for coordinator service.
Target: ≥85% coverage
"""

import pytest
from unittest.mock import MagicMock
from src.services.coordinator import Coordinator


class TestCoordinator:
    """Tests for Coordinator service."""

    def test_initialization_with_name(self):
        """Test coordinator initialization with name."""
        coordinator = Coordinator("test_coordinator")
        
        assert coordinator.name == "test_coordinator"
        assert coordinator.status["name"] == "test_coordinator"
        assert coordinator.status["status"] == "active"

    def test_initialization_with_logger(self):
        """Test coordinator initialization with logger."""
        logger = MagicMock()
        coordinator = Coordinator("test_coordinator", logger=logger)
        
        assert coordinator.name == "test_coordinator"
        assert coordinator.logger == logger

    def test_initialization_without_logger(self):
        """Test coordinator initialization without logger."""
        coordinator = Coordinator("test_coordinator", logger=None)
        
        assert coordinator.name == "test_coordinator"
        assert coordinator.logger is None

    def test_get_status(self):
        """Test getting coordinator status."""
        coordinator = Coordinator("test_coordinator")
        
        status = coordinator.get_status()
        
        assert status["name"] == "test_coordinator"
        assert status["status"] == "active"
        assert isinstance(status, dict)

    def test_get_name(self):
        """Test getting coordinator name."""
        coordinator = Coordinator("test_coordinator")
        
        name = coordinator.get_name()
        
        assert name == "test_coordinator"

    def test_shutdown_with_logger(self):
        """Test shutting down coordinator with logger."""
        logger = MagicMock()
        coordinator = Coordinator("test_coordinator", logger=logger)
        
        coordinator.shutdown()
        
        assert coordinator.status["status"] == "shutdown"
        logger.info.assert_called_once()
        assert "shut down" in logger.info.call_args[0][0]

    def test_shutdown_without_logger(self):
        """Test shutting down coordinator without logger."""
        coordinator = Coordinator("test_coordinator", logger=None)
        
        # Should not raise
        coordinator.shutdown()
        
        assert coordinator.status["status"] == "shutdown"

    def test_status_persistence(self):
        """Test that status persists after operations."""
        coordinator = Coordinator("test_coordinator")
        initial_status = coordinator.get_status()
        
        coordinator.get_name()  # Should not change status
        status_after = coordinator.get_status()
        
        assert initial_status == status_after

    def test_shutdown_changes_status(self):
        """Test that shutdown changes status."""
        coordinator = Coordinator("test_coordinator")
        assert coordinator.status["status"] == "active"
        
        coordinator.shutdown()
        
        assert coordinator.status["status"] == "shutdown"

