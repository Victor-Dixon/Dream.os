"""
Tests for coordinator_status_parser.py

Comprehensive tests for coordinator status parsing and filtering.
Target: ≥85% coverage
"""

import pytest
from unittest.mock import MagicMock
from src.core.coordinator_status_parser import (
    CoordinatorStatusParser,
    CoordinatorStatusFilter,
)
from src.core.coordinator_models import CoordinationStatus, CoordinatorStatus as StatusModel


class TestCoordinatorStatusParser:
    """Tests for CoordinatorStatusParser."""

    def test_parse_status_with_get_status_method(self):
        """Test parsing status when coordinator has get_status method."""
        parser = CoordinatorStatusParser()
        coordinator = MagicMock()
        coordinator.get_status = MagicMock(return_value={"status": "active"})
        
        result = parser.parse_status(coordinator)
        
        assert result == {"status": "active"}

    def test_parse_status_with_to_dict_method(self):
        """Test parsing status when status has to_dict method."""
        parser = CoordinatorStatusParser()
        status_obj = MagicMock()
        status_obj.to_dict = MagicMock(return_value={"status": "operational"})
        coordinator = MagicMock()
        coordinator.get_status = MagicMock(return_value=status_obj)
        
        result = parser.parse_status(coordinator)
        
        assert result == {"status": "operational"}

    def test_parse_status_with_dict_status(self):
        """Test parsing status when status is already a dict."""
        parser = CoordinatorStatusParser()
        coordinator = MagicMock()
        coordinator.get_status = MagicMock(return_value={"status": "active", "count": 5})
        
        result = parser.parse_status(coordinator)
        
        assert result == {"status": "active", "count": 5}

    def test_parse_status_with_non_dict_status(self):
        """Test parsing status when status is not a dict."""
        parser = CoordinatorStatusParser()
        coordinator = MagicMock()
        coordinator.get_status = MagicMock(return_value="active")
        
        result = parser.parse_status(coordinator)
        
        assert result == {"status": "active"}

    def test_parse_status_no_get_status_method(self):
        """Test parsing status when coordinator has no get_status method."""
        parser = CoordinatorStatusParser()
        coordinator = MagicMock()
        coordinator.name = "test_coordinator"
        del coordinator.get_status
        
        result = parser.parse_status(coordinator)
        
        assert result["name"] == "test_coordinator"
        assert result["status"] == "unknown"
        assert "error" in result

    def test_parse_status_no_name_attribute(self):
        """Test parsing status when coordinator has no name attribute."""
        parser = CoordinatorStatusParser()
        coordinator = MagicMock()
        del coordinator.get_status
        del coordinator.name
        
        result = parser.parse_status(coordinator)
        
        assert result["name"] == "unknown"
        assert result["status"] == "unknown"

    def test_parse_status_exception_handling(self):
        """Test exception handling during parsing."""
        parser = CoordinatorStatusParser()
        coordinator = MagicMock()
        coordinator.get_status = MagicMock(side_effect=Exception("Test error"))
        coordinator.name = "test_coordinator"
        
        result = parser.parse_status(coordinator)
        
        assert result["name"] == "test_coordinator"
        assert result["status"] == "error"
        assert "Test error" in result["error"]

    def test_can_parse_status_with_method(self):
        """Test can_parse_status when coordinator has get_status method."""
        parser = CoordinatorStatusParser()
        coordinator = MagicMock()
        coordinator.get_status = MagicMock()
        
        result = parser.can_parse_status(coordinator)
        
        assert result is True

    def test_can_parse_status_without_method(self):
        """Test can_parse_status when coordinator has no get_status method."""
        parser = CoordinatorStatusParser()
        coordinator = MagicMock()
        del coordinator.get_status
        
        result = parser.can_parse_status(coordinator)
        
        assert result is False


class TestCoordinatorStatusFilter:
    """Tests for CoordinatorStatusFilter."""

    def test_initialization(self):
        """Test filter initialization."""
        parser = CoordinatorStatusParser()
        filter_obj = CoordinatorStatusFilter(parser)
        
        assert filter_obj.status_parser == parser

    def test_get_coordinators_by_status_matching(self):
        """Test filtering coordinators by matching status."""
        parser = CoordinatorStatusParser()
        filter_obj = CoordinatorStatusFilter(parser)
        
        coord1 = MagicMock()
        coord1.get_status = MagicMock(return_value={"status": "active"})
        coord2 = MagicMock()
        coord2.get_status = MagicMock(return_value={"status": "inactive"})
        
        coordinators = {"coord1": coord1, "coord2": coord2}
        
        result = filter_obj.get_coordinators_by_status(coordinators, "active")
        
        assert "coord1" in result
        assert "coord2" not in result

    def test_get_coordinators_by_status_coordination_status_enum(self):
        """Test filtering by CoordinationStatus enum."""
        parser = CoordinatorStatusParser()
        filter_obj = CoordinatorStatusFilter(parser)
        
        coord1 = MagicMock()
        # Return a dict with coordination_status as enum
        coord1.get_status = MagicMock(return_value={"coordination_status": CoordinationStatus.OPERATIONAL})
        
        coordinators = {"coord1": coord1}
        
        result = filter_obj.get_coordinators_by_status(coordinators, "operational")
        
        # Should match via enum value
        assert "coord1" in result

    def test_get_coordinators_by_status_coordination_status_string(self):
        """Test filtering by coordination_status string."""
        parser = CoordinatorStatusParser()
        filter_obj = CoordinatorStatusFilter(parser)
        
        coord1 = MagicMock()
        coord1.get_status = MagicMock(return_value={"coordination_status": "operational"})
        
        coordinators = {"coord1": coord1}
        
        result = filter_obj.get_coordinators_by_status(coordinators, "operational")
        
        assert "coord1" in result

    def test_get_coordinators_by_status_no_match(self):
        """Test filtering when no coordinators match."""
        parser = CoordinatorStatusParser()
        filter_obj = CoordinatorStatusFilter(parser)
        
        coord1 = MagicMock()
        coord1.get_status = MagicMock(return_value={"status": "active"})
        
        coordinators = {"coord1": coord1}
        
        result = filter_obj.get_coordinators_by_status(coordinators, "inactive")
        
        assert len(result) == 0

    def test_get_coordinators_by_status_exception_handling(self):
        """Test exception handling during filtering."""
        parser = CoordinatorStatusParser()
        filter_obj = CoordinatorStatusFilter(parser)
        
        coord1 = MagicMock()
        coord1.get_status = MagicMock(side_effect=Exception("Test error"))
        coord2 = MagicMock()
        coord2.get_status = MagicMock(return_value={"status": "active"})
        
        coordinators = {"coord1": coord1, "coord2": coord2}
        
        result = filter_obj.get_coordinators_by_status(coordinators, "active")
        
        # Should skip coord1 due to exception, include coord2
        assert "coord1" not in result
        assert "coord2" in result

    def test_matches_status_coordination_status_enum(self):
        """Test matching status with CoordinationStatus enum."""
        parser = CoordinatorStatusParser()
        filter_obj = CoordinatorStatusFilter(parser)
        
        status_info = {"coordination_status": CoordinationStatus.OPERATIONAL}
        
        result = filter_obj._matches_status(status_info, "operational")
        
        assert result is True

    def test_matches_status_coordination_status_string(self):
        """Test matching status with coordination_status string."""
        parser = CoordinatorStatusParser()
        filter_obj = CoordinatorStatusFilter(parser)
        
        status_info = {"coordination_status": "operational"}
        
        result = filter_obj._matches_status(status_info, "operational")
        
        assert result is True

    def test_matches_status_direct_status_field(self):
        """Test matching status with direct status field."""
        parser = CoordinatorStatusParser()
        filter_obj = CoordinatorStatusFilter(parser)
        
        status_info = {"status": "active"}
        
        result = filter_obj._matches_status(status_info, "active")
        
        assert result is True

    def test_matches_status_no_match(self):
        """Test matching status when no match found."""
        parser = CoordinatorStatusParser()
        filter_obj = CoordinatorStatusFilter(parser)
        
        status_info = {"other_field": "value"}
        
        result = filter_obj._matches_status(status_info, "active")
        
        assert result is False

    def test_matches_status_different_value(self):
        """Test matching status with different value."""
        parser = CoordinatorStatusParser()
        filter_obj = CoordinatorStatusFilter(parser)
        
        status_info = {"status": "active"}
        
        result = filter_obj._matches_status(status_info, "inactive")
        
        assert result is False

