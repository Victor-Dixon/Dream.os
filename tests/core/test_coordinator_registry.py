"""Tests for coordinator_registry.py - V2 Compliant Test Suite"""

import unittest
from unittest.mock import Mock, MagicMock

from src.core.coordinator_registry import CoordinatorRegistry, get_coordinator_registry


class TestCoordinatorRegistry(unittest.TestCase):
    """Test suite for CoordinatorRegistry class."""

    def setUp(self):
        """Set up test fixtures."""
        self.registry = CoordinatorRegistry()
        self.mock_coordinator = Mock()
        self.mock_coordinator.name = "test_coordinator"

    def test_initialization(self):
        """Test CoordinatorRegistry initialization."""
        self.assertEqual(len(self.registry._coordinators), 0)

    def test_register_coordinator_success(self):
        """Test successful coordinator registration."""
        result = self.registry.register_coordinator(self.mock_coordinator)
        
        self.assertTrue(result)
        self.assertIn("test_coordinator", self.registry._coordinators)
        self.assertEqual(self.registry._coordinators["test_coordinator"], self.mock_coordinator)

    def test_register_coordinator_no_name(self):
        """Test registration fails when coordinator has no name attribute."""
        coordinator = Mock()
        del coordinator.name
        
        result = self.registry.register_coordinator(coordinator)
        
        self.assertFalse(result)
        self.assertEqual(len(self.registry._coordinators), 0)

    def test_register_coordinator_duplicate(self):
        """Test registration fails for duplicate coordinator."""
        self.registry.register_coordinator(self.mock_coordinator)
        result = self.registry.register_coordinator(self.mock_coordinator)
        
        self.assertFalse(result)
        self.assertEqual(len(self.registry._coordinators), 1)

    def test_get_coordinator(self):
        """Test getting coordinator by name."""
        self.registry.register_coordinator(self.mock_coordinator)
        
        coordinator = self.registry.get_coordinator("test_coordinator")
        
        self.assertEqual(coordinator, self.mock_coordinator)

    def test_get_coordinator_not_found(self):
        """Test getting non-existent coordinator."""
        coordinator = self.registry.get_coordinator("nonexistent")
        
        self.assertIsNone(coordinator)

    def test_get_all_coordinators(self):
        """Test getting all coordinators."""
        coord1 = Mock()
        coord1.name = "coord1"
        coord2 = Mock()
        coord2.name = "coord2"
        
        self.registry.register_coordinator(coord1)
        self.registry.register_coordinator(coord2)
        
        all_coords = self.registry.get_all_coordinators()
        
        self.assertEqual(len(all_coords), 2)
        self.assertIn("coord1", all_coords)
        self.assertIn("coord2", all_coords)

    def test_unregister_coordinator_success(self):
        """Test successful coordinator unregistration."""
        self.registry.register_coordinator(self.mock_coordinator)
        
        result = self.registry.unregister_coordinator("test_coordinator")
        
        self.assertTrue(result)
        self.assertNotIn("test_coordinator", self.registry._coordinators)

    def test_unregister_coordinator_with_shutdown(self):
        """Test unregistration calls shutdown if available."""
        self.mock_coordinator.shutdown = Mock()
        self.registry.register_coordinator(self.mock_coordinator)
        
        self.registry.unregister_coordinator("test_coordinator")
        
        self.mock_coordinator.shutdown.assert_called_once()

    def test_unregister_coordinator_not_found(self):
        """Test unregistering non-existent coordinator."""
        result = self.registry.unregister_coordinator("nonexistent")
        
        self.assertFalse(result)

    def test_get_coordinator_statuses(self):
        """Test getting status of all coordinators."""
        self.mock_coordinator.get_status = Mock(return_value={"status": "active"})
        self.registry.register_coordinator(self.mock_coordinator)
        
        statuses = self.registry.get_coordinator_statuses()
        
        self.assertIn("test_coordinator", statuses)
        self.assertEqual(statuses["test_coordinator"]["status"], "active")

    def test_get_coordinator_statuses_no_get_status(self):
        """Test status retrieval when coordinator has no get_status method."""
        coord = Mock()
        coord.name = "test_coordinator"
        # Ensure no get_status method
        if hasattr(coord, 'get_status'):
            delattr(coord, 'get_status')
        
        self.registry.register_coordinator(coord)
        
        statuses = self.registry.get_coordinator_statuses()
        
        self.assertIn("test_coordinator", statuses)
        self.assertIsInstance(statuses["test_coordinator"], dict)
        self.assertEqual(statuses["test_coordinator"]["status"], "unknown")

    def test_shutdown_all_coordinators(self):
        """Test shutting down all coordinators."""
        coord1 = Mock()
        coord1.name = "coord1"
        coord1.shutdown = Mock()
        coord2 = Mock()
        coord2.name = "coord2"
        coord2.shutdown = Mock()
        
        self.registry.register_coordinator(coord1)
        self.registry.register_coordinator(coord2)
        
        self.registry.shutdown_all_coordinators()
        
        coord1.shutdown.assert_called_once()
        coord2.shutdown.assert_called_once()
        self.assertEqual(len(self.registry._coordinators), 0)

    def test_get_coordinator_count(self):
        """Test getting coordinator count."""
        self.assertEqual(self.registry.get_coordinator_count(), 0)
        
        self.registry.register_coordinator(self.mock_coordinator)
        
        self.assertEqual(self.registry.get_coordinator_count(), 1)

    def test_get_coordinator_registry_singleton(self):
        """Test get_coordinator_registry returns singleton."""
        registry1 = get_coordinator_registry()
        registry2 = get_coordinator_registry()
        
        self.assertIs(registry1, registry2)


if __name__ == "__main__":
    unittest.main()
