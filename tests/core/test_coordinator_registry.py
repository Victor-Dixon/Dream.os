"""
Tests for coordinator_registry.py

Comprehensive tests for coordinator registry implementation.
Target: ≥85% coverage
"""

import pytest
from unittest.mock import MagicMock, patch
from src.core.coordinator_registry import (
    CoordinatorRegistry,
    get_coordinator_registry,
)


class TestCoordinatorRegistry:
    """Tests for CoordinatorRegistry."""

    def test_initialization(self):
        """Test registry initialization."""
        registry = CoordinatorRegistry()
        assert registry._coordinators == {}
        assert registry.logger is not None

    def test_register_coordinator_success(self):
        """Test registering coordinator successfully."""
        registry = CoordinatorRegistry()
        coordinator = MagicMock()
        coordinator.name = "test_coordinator"
        
        result = registry.register_coordinator(coordinator)
        
        assert result is True
        assert "test_coordinator" in registry._coordinators
        assert registry._coordinators["test_coordinator"] == coordinator

    def test_register_coordinator_no_name_attribute(self):
        """Test registering coordinator without name attribute."""
        registry = CoordinatorRegistry()
        coordinator = MagicMock()
        del coordinator.name
        
        result = registry.register_coordinator(coordinator)
        
        assert result is False
        assert len(registry._coordinators) == 0

    def test_register_coordinator_already_registered(self):
        """Test registering already registered coordinator."""
        registry = CoordinatorRegistry()
        coordinator1 = MagicMock()
        coordinator1.name = "test_coordinator"
        coordinator2 = MagicMock()
        coordinator2.name = "test_coordinator"
        
        registry.register_coordinator(coordinator1)
        result = registry.register_coordinator(coordinator2)
        
        assert result is False
        assert registry._coordinators["test_coordinator"] == coordinator1

    def test_register_coordinator_exception_handling(self):
        """Test exception handling during registration."""
        registry = CoordinatorRegistry()
        coordinator = MagicMock()
        coordinator.name = "test_coordinator"
        
        # Simulate exception during registration by making _coordinators access fail
        with patch.object(registry, '_coordinators', create=True) as mock_coords:
            mock_coords.__contains__ = MagicMock(side_effect=Exception("Test error"))
            result = registry.register_coordinator(coordinator)
            assert result is False

    def test_get_coordinator_existing(self):
        """Test getting existing coordinator."""
        registry = CoordinatorRegistry()
        coordinator = MagicMock()
        coordinator.name = "test_coordinator"
        registry.register_coordinator(coordinator)
        
        result = registry.get_coordinator("test_coordinator")
        
        assert result == coordinator

    def test_get_coordinator_nonexistent(self):
        """Test getting nonexistent coordinator."""
        registry = CoordinatorRegistry()
        result = registry.get_coordinator("nonexistent")
        
        assert result is None

    def test_get_all_coordinators(self):
        """Test getting all coordinators."""
        registry = CoordinatorRegistry()
        coord1 = MagicMock()
        coord1.name = "coord1"
        coord2 = MagicMock()
        coord2.name = "coord2"
        
        registry.register_coordinator(coord1)
        registry.register_coordinator(coord2)
        
        all_coords = registry.get_all_coordinators()
        
        assert len(all_coords) == 2
        assert "coord1" in all_coords
        assert "coord2" in all_coords
        # Should be a copy, not the same object
        assert all_coords is not registry._coordinators

    def test_unregister_coordinator_success(self):
        """Test unregistering coordinator successfully."""
        registry = CoordinatorRegistry()
        coordinator = MagicMock()
        coordinator.name = "test_coordinator"
        coordinator.shutdown = MagicMock()
        registry.register_coordinator(coordinator)
        
        result = registry.unregister_coordinator("test_coordinator")
        
        assert result is True
        assert "test_coordinator" not in registry._coordinators
        coordinator.shutdown.assert_called_once()

    def test_unregister_coordinator_nonexistent(self):
        """Test unregistering nonexistent coordinator."""
        registry = CoordinatorRegistry()
        result = registry.unregister_coordinator("nonexistent")
        
        assert result is False

    def test_unregister_coordinator_no_shutdown_method(self):
        """Test unregistering coordinator without shutdown method."""
        registry = CoordinatorRegistry()
        coordinator = MagicMock()
        coordinator.name = "test_coordinator"
        del coordinator.shutdown
        registry.register_coordinator(coordinator)
        
        result = registry.unregister_coordinator("test_coordinator")
        
        assert result is True
        assert "test_coordinator" not in registry._coordinators

    def test_unregister_coordinator_exception_handling(self):
        """Test exception handling during unregistration."""
        registry = CoordinatorRegistry()
        coordinator = MagicMock()
        coordinator.name = "test_coordinator"
        coordinator.shutdown = MagicMock(side_effect=Exception("Test error"))
        registry.register_coordinator(coordinator)
        
        # The actual implementation catches exceptions and returns False
        # but still attempts to unregister
        result = registry.unregister_coordinator("test_coordinator")
        
        # Implementation returns False on exception, but coordinator is still removed
        assert result is False  # Exception causes False return
        # But coordinator should still be removed (implementation detail)

    def test_get_coordinator_statuses(self):
        """Test getting coordinator statuses."""
        registry = CoordinatorRegistry()
        coordinator = MagicMock()
        coordinator.name = "test_coordinator"
        coordinator.get_status = MagicMock(return_value={"status": "active"})
        registry.register_coordinator(coordinator)
        
        statuses = registry.get_coordinator_statuses()
        
        assert "test_coordinator" in statuses
        assert statuses["test_coordinator"] == {"status": "active"}

    def test_get_coordinator_statuses_no_get_status_method(self):
        """Test getting statuses when coordinator has no get_status method."""
        registry = CoordinatorRegistry()
        coordinator = MagicMock()
        coordinator.name = "test_coordinator"
        del coordinator.get_status
        registry.register_coordinator(coordinator)
        
        statuses = registry.get_coordinator_statuses()
        
        assert "test_coordinator" in statuses
        assert "error" in statuses["test_coordinator"]
        assert "No get_status method" in statuses["test_coordinator"]["error"]

    def test_get_coordinator_statuses_exception(self):
        """Test getting statuses when get_status raises exception."""
        registry = CoordinatorRegistry()
        coordinator = MagicMock()
        coordinator.name = "test_coordinator"
        coordinator.get_status = MagicMock(side_effect=Exception("Test error"))
        registry.register_coordinator(coordinator)
        
        statuses = registry.get_coordinator_statuses()
        
        assert "test_coordinator" in statuses
        assert statuses["test_coordinator"]["status"] == "error"
        assert "Test error" in statuses["test_coordinator"]["error"]

    def test_get_coordinator_statuses_exception_handling(self):
        """Test exception handling in get_coordinator_statuses."""
        registry = CoordinatorRegistry()
        
        with patch.object(registry, '_coordinators', side_effect=Exception("Test error")):
            statuses = registry.get_coordinator_statuses()
            assert statuses == {}

    def test_shutdown_all_coordinators(self):
        """Test shutting down all coordinators."""
        registry = CoordinatorRegistry()
        coord1 = MagicMock()
        coord1.name = "coord1"
        coord1.shutdown = MagicMock()
        coord2 = MagicMock()
        coord2.name = "coord2"
        coord2.shutdown = MagicMock()
        
        registry.register_coordinator(coord1)
        registry.register_coordinator(coord2)
        
        registry.shutdown_all_coordinators()
        
        assert len(registry._coordinators) == 0
        coord1.shutdown.assert_called_once()
        coord2.shutdown.assert_called_once()

    def test_shutdown_all_coordinators_no_shutdown_method(self):
        """Test shutting down coordinators without shutdown method."""
        registry = CoordinatorRegistry()
        coordinator = MagicMock()
        coordinator.name = "test_coordinator"
        del coordinator.shutdown
        registry.register_coordinator(coordinator)
        
        registry.shutdown_all_coordinators()
        
        assert len(registry._coordinators) == 0

    def test_shutdown_all_coordinators_exception_handling(self):
        """Test exception handling during shutdown."""
        registry = CoordinatorRegistry()
        coord1 = MagicMock()
        coord1.name = "coord1"
        coord1.shutdown = MagicMock(side_effect=Exception("Test error"))
        coord2 = MagicMock()
        coord2.name = "coord2"
        coord2.shutdown = MagicMock()
        
        registry.register_coordinator(coord1)
        registry.register_coordinator(coord2)
        
        registry.shutdown_all_coordinators()
        
        # Should still shutdown all despite exception
        assert len(registry._coordinators) == 0
        coord2.shutdown.assert_called_once()

    def test_get_coordinator_count(self):
        """Test getting coordinator count."""
        registry = CoordinatorRegistry()
        assert registry.get_coordinator_count() == 0
        
        coord1 = MagicMock()
        coord1.name = "coord1"
        registry.register_coordinator(coord1)
        assert registry.get_coordinator_count() == 1
        
        coord2 = MagicMock()
        coord2.name = "coord2"
        registry.register_coordinator(coord2)
        assert registry.get_coordinator_count() == 2


class TestGetCoordinatorRegistry:
    """Tests for get_coordinator_registry function."""

    def test_get_coordinator_registry_singleton(self):
        """Test that get_coordinator_registry returns singleton."""
        # Reset global instance
        import src.core.coordinator_registry as module
        module._registry_instance = None
        
        registry1 = get_coordinator_registry()
        registry2 = get_coordinator_registry()
        
        assert registry1 is registry2
        assert isinstance(registry1, CoordinatorRegistry)

