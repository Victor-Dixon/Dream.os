"""
Unit tests for consolidation/utility_consolidation/utility_consolidation_engine.py - HIGH PRIORITY

Tests UtilityConsolidationEngine class functionality (utility_consolidator).
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Import the module
from src.core.consolidation.utility_consolidation.utility_consolidation_engine import (
    UtilityConsolidationEngine,
    create_utility_consolidation_engine
)


class TestUtilityConsolidationEngine:
    """Test suite for UtilityConsolidationEngine class."""

    @pytest.fixture
    def engine(self):
        """Create a UtilityConsolidationEngine instance."""
        return UtilityConsolidationEngine()

    @pytest.fixture
    def engine_with_config(self):
        """Create engine with custom config."""
        config = {"setting1": "value1"}
        return UtilityConsolidationEngine(config)

    def test_initialization(self, engine):
        """Test UtilityConsolidationEngine initialization."""
        assert engine.config == {}
        assert engine.consolidation_history == []
        assert engine.utilities == {}
        assert engine.logger is not None

    def test_initialization_with_config(self, engine_with_config):
        """Test initialization with custom config."""
        assert engine_with_config.config["setting1"] == "value1"

    def test_consolidate_utilities_empty_list(self, engine):
        """Test consolidate_utilities with empty list."""
        result = engine.consolidate_utilities([])
        
        assert "error" in result
        assert result["error"] == "No utilities provided"

    def test_consolidate_utilities_success(self, engine):
        """Test consolidate_utilities with valid utilities."""
        utilities = [
            {"name": "util1", "function": "def func1(): pass"},
            {"name": "util2", "function": "def func2(): pass"}
        ]
        
        result = engine.consolidate_utilities(utilities)
        
        assert "error" not in result
        assert result["original_count"] == 2
        assert result["consolidated_count"] == 2
        assert "consolidated" in result
        assert "optimized" in result
        assert "timestamp" in result

    def test_consolidate_utilities_with_duplicates(self, engine):
        """Test consolidate_utilities with duplicate utilities."""
        utilities = [
            {"name": "util1", "function": "def func1(): pass"},
            {"name": "util1", "function": "def func1(): pass"},  # Duplicate
            {"name": "util2", "function": "def func2(): pass"}
        ]
        
        result = engine.consolidate_utilities(utilities)
        
        assert result["original_count"] == 3
        assert result["consolidated_count"] == 2  # Duplicate removed
        assert result["duplicates_found"] == 1

    def test_merge_utilities(self, engine):
        """Test _merge_utilities method."""
        utilities = [
            {"name": "util1", "value": 1},
            {"name": "util2", "value": 2},
            {"name": "util1", "value": 3}  # Duplicate name
        ]
        
        merged = engine._merge_utilities(utilities)
        
        assert len(merged) == 2
        assert any(u["name"] == "util1" for u in merged)
        assert any(u["name"] == "util2" for u in merged)

    def test_find_duplicates(self, engine):
        """Test _find_duplicates method."""
        utilities = [
            {"name": "util1", "value": 1},
            {"name": "util2", "value": 2},
            {"name": "util1", "value": 3}  # Duplicate
        ]
        
        duplicates = engine._find_duplicates(utilities)
        
        assert len(duplicates) == 1
        assert duplicates[0]["name"] == "util1"

    def test_find_duplicates_no_duplicates(self, engine):
        """Test _find_duplicates with no duplicates."""
        utilities = [
            {"name": "util1", "value": 1},
            {"name": "util2", "value": 2}
        ]
        
        duplicates = engine._find_duplicates(utilities)
        
        assert len(duplicates) == 0

    def test_optimize_utilities(self, engine):
        """Test _optimize_utilities method."""
        utilities = [
            {"name": "util1", "value": 1},
            {"name": "util2", "value": 2}
        ]
        
        optimized = engine._optimize_utilities(utilities)
        
        assert len(optimized) == 2
        assert all(u.get("optimized") is True for u in optimized)

    def test_get_consolidation_summary_empty(self, engine):
        """Test get_consolidation_summary with no history."""
        summary = engine.get_consolidation_summary()
        
        assert "message" in summary
        assert summary["message"] == "No consolidation data available"

    def test_get_consolidation_summary_with_history(self, engine):
        """Test get_consolidation_summary with consolidation history."""
        utilities = [{"name": "util1"}]
        engine.consolidate_utilities(utilities)
        
        summary = engine.get_consolidation_summary()
        
        assert "total_consolidations" in summary
        assert summary["total_consolidations"] == 1
        assert "recent_consolidation" in summary
        assert "timestamp" in summary

    def test_clear_consolidation_history(self, engine):
        """Test clear_consolidation_history method."""
        utilities = [{"name": "util1"}]
        engine.consolidate_utilities(utilities)
        
        assert len(engine.consolidation_history) == 1
        
        engine.clear_consolidation_history()
        
        assert len(engine.consolidation_history) == 0

    def test_get_status(self, engine):
        """Test get_status method."""
        status = engine.get_status()
        
        assert status["active"] is True
        assert status["consolidation_count"] == 0
        assert "timestamp" in status

    def test_get_status_with_history(self, engine):
        """Test get_status with consolidation history."""
        utilities = [{"name": "util1"}]
        engine.consolidate_utilities(utilities)
        
        status = engine.get_status()
        
        assert status["consolidation_count"] == 1

    def test_consolidation_history_limit(self, engine):
        """Test that consolidation history is limited to 100 entries."""
        # Add 101 consolidations
        for i in range(101):
            engine.consolidate_utilities([{"name": f"util{i}"}])
        
        assert len(engine.consolidation_history) == 100
        # First consolidation should be removed
        assert engine.consolidation_history[0]["consolidated"][0]["name"] != "util0"

    def test_merge_utilities_invalid_input(self, engine):
        """Test _merge_utilities with invalid input."""
        utilities = [
            {"name": "util1"},
            "not a dict",  # Invalid
            {"no_name": "missing name"}  # Missing name key
        ]
        
        merged = engine._merge_utilities(utilities)
        
        # Should only include valid utilities with "name" key
        assert len(merged) == 1
        assert merged[0]["name"] == "util1"

    def test_create_utility_consolidation_engine(self):
        """Test factory function create_utility_consolidation_engine."""
        engine = create_utility_consolidation_engine()
        
        assert isinstance(engine, UtilityConsolidationEngine)

    def test_create_utility_consolidation_engine_with_config(self):
        """Test factory function with config."""
        config = {"test": "value"}
        engine = create_utility_consolidation_engine(config)
        
        assert isinstance(engine, UtilityConsolidationEngine)
        assert engine.config["test"] == "value"

