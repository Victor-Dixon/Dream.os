"""Tests for coordinator_status_parser.py - V2 Compliant Test Suite"""

import unittest
from unittest.mock import Mock

from src.core.coordinator_status_parser import (
    CoordinatorStatusParser,
    CoordinatorStatusFilter,
)


class TestCoordinatorStatusParser(unittest.TestCase):
    """Test suite for CoordinatorStatusParser class."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = CoordinatorStatusParser()

    def test_parse_status_with_get_status_dict(self):
        """Test parsing status when coordinator returns dict."""
        coordinator = Mock()
        coordinator.get_status = Mock(return_value={"status": "active", "count": 5})
        
        result = self.parser.parse_status(coordinator)
        
        self.assertEqual(result["status"], "active")
        self.assertEqual(result["count"], 5)

    def test_parse_status_with_get_status_object(self):
        """Test parsing status when coordinator returns object with to_dict."""
        status_obj = Mock()
        status_obj.to_dict = Mock(return_value={"status": "active"})
        coordinator = Mock()
        coordinator.get_status = Mock(return_value=status_obj)
        
        result = self.parser.parse_status(coordinator)
        
        self.assertEqual(result["status"], "active")
        status_obj.to_dict.assert_called_once()

    def test_parse_status_with_get_status_string(self):
        """Test parsing status when coordinator returns string."""
        coordinator = Mock()
        coordinator.get_status = Mock(return_value="active")
        
        result = self.parser.parse_status(coordinator)
        
        self.assertEqual(result["status"], "active")

    def test_parse_status_no_get_status(self):
        """Test parsing status when coordinator has no get_status method."""
        coordinator = Mock(spec=[])  # No attributes by default
        coordinator.name = "test_coord"
        del coordinator.get_status  # Ensure no get_status
        
        result = self.parser.parse_status(coordinator)
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result["name"], "test_coord")
        self.assertEqual(result["status"], "unknown")
        self.assertIn("error", result)

    def test_parse_status_exception(self):
        """Test parsing status when exception occurs."""
        coordinator = Mock()
        coordinator.get_status = Mock(side_effect=Exception("Test error"))
        coordinator.name = "test_coord"
        
        result = self.parser.parse_status(coordinator)
        
        self.assertEqual(result["name"], "test_coord")
        self.assertEqual(result["status"], "error")
        self.assertIn("error", result)

    def test_can_parse_status_true(self):
        """Test can_parse_status returns True when coordinator has get_status."""
        coordinator = Mock()
        coordinator.get_status = Mock()
        
        result = self.parser.can_parse_status(coordinator)
        
        self.assertTrue(result)

    def test_can_parse_status_false(self):
        """Test can_parse_status returns False when coordinator has no get_status."""
        coordinator = Mock(spec=[])  # No attributes by default
        # Ensure get_status doesn't exist
        if hasattr(coordinator, 'get_status'):
            delattr(coordinator, 'get_status')
        
        result = self.parser.can_parse_status(coordinator)
        
        self.assertFalse(result)


class TestCoordinatorStatusFilter(unittest.TestCase):
    """Test suite for CoordinatorStatusFilter class."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = CoordinatorStatusParser()
        self.filter = CoordinatorStatusFilter(self.parser)

    def test_get_coordinators_by_status_matches(self):
        """Test filtering coordinators by matching status."""
        coord1 = Mock()
        coord1.get_status = Mock(return_value={"status": "active"})
        coord2 = Mock()
        coord2.get_status = Mock(return_value={"status": "inactive"})
        
        coordinators = {"coord1": coord1, "coord2": coord2}
        
        result = self.filter.get_coordinators_by_status(coordinators, "active")
        
        self.assertIn("coord1", result)
        self.assertNotIn("coord2", result)

    def test_get_coordinators_by_status_coordination_status(self):
        """Test filtering by coordination_status field."""
        from enum import Enum
        
        class Status(Enum):
            ACTIVE = "active"
        
        coord = Mock()
        coord.get_status = Mock(return_value={"coordination_status": Status.ACTIVE})
        
        coordinators = {"coord1": coord}
        
        result = self.filter.get_coordinators_by_status(coordinators, "active")
        
        self.assertIn("coord1", result)

    def test_get_coordinators_by_status_exception(self):
        """Test filtering handles exceptions gracefully."""
        coord = Mock()
        coord.get_status = Mock(side_effect=Exception("Test error"))
        
        coordinators = {"coord1": coord}
        
        result = self.filter.get_coordinators_by_status(coordinators, "active")
        
        self.assertEqual(len(result), 0)

    def test_get_coordinators_by_status_no_match(self):
        """Test filtering when no coordinators match."""
        coord = Mock()
        coord.get_status = Mock(return_value={"status": "inactive"})
        
        coordinators = {"coord1": coord}
        
        result = self.filter.get_coordinators_by_status(coordinators, "active")
        
        self.assertEqual(len(result), 0)


if __name__ == "__main__":
    unittest.main()
