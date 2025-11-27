"""
Unit tests for core_results_manager.py - MEDIUM PRIORITY

Tests CoreResultsManager class and result processing operations.
"""

import pytest
from unittest.mock import Mock, MagicMock
from datetime import datetime
import sys
import uuid
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.managers.contracts import ManagerContext, ManagerResult
from src.core.managers.core_results_manager import CoreResultsManager


class TestCoreResultsManager:
    """Test suite for CoreResultsManager class."""

    @pytest.fixture
    def mock_context(self):
        """Create mock manager context."""
        return ManagerContext(
            config={"test": "config"},
            logger=lambda msg: None,
            metrics={},
            timestamp=datetime.now()
        )

    @pytest.fixture
    def manager(self):
        """Create CoreResultsManager instance."""
        return CoreResultsManager()

    def test_manager_initialization(self, manager):
        """Test manager initialization."""
        assert manager is not None
        assert hasattr(manager, '_results')
        assert hasattr(manager, '_v2_compliant')
        assert manager._v2_compliant is True

    def test_initialize(self, manager, mock_context):
        """Test manager initialization with context."""
        result = manager.initialize(mock_context)
        assert result is True

    def test_execute_process_results(self, manager, mock_context):
        """Test execute process_results operation."""
        payload = {
            "result_type": "test_result",
            "data": {"key": "value"},
            "metadata": {"source": "test"}
        }
        result = manager.execute(mock_context, "process_results", payload)
        assert result.success is True
        assert "result_id" in result.data
        assert len(manager._results) == 1

    def test_execute_process_results_with_existing_id(self, manager, mock_context):
        """Test process_results with existing result_id."""
        result_id = str(uuid.uuid4())
        payload = {
            "result_id": result_id,
            "result_type": "test",
            "data": {}
        }
        result = manager.execute(mock_context, "process_results", payload)
        assert result.success is True
        assert result.data["result_id"] == result_id
        assert result_id in manager._results

    def test_execute_get_results(self, manager, mock_context):
        """Test execute get_results operation."""
        # Add some results first
        manager._results["result-1"] = {"result_type": "test", "data": {}}
        manager._results["result-2"] = {"result_type": "test", "data": {}}
        
        result = manager.execute(mock_context, "get_results", {})
        assert result.success is True
        assert "results" in result.data
        assert len(result.data["results"]) == 2

    def test_execute_unknown_operation(self, manager, mock_context):
        """Test execute with unknown operation."""
        result = manager.execute(mock_context, "unknown_operation", {})
        assert result.success is False
        assert result.error is not None
        assert "Unknown operation" in result.error

    def test_process_results(self, manager, mock_context):
        """Test process_results method."""
        payload = {
            "result_type": "analysis",
            "data": {"score": 95},
            "metadata": {"agent": "Agent-5"}
        }
        result = manager.process_results(mock_context, payload)
        assert result.success is True
        assert "result_id" in result.data
        result_id = result.data["result_id"]
        assert result_id in manager._results
        assert manager._results[result_id]["result_type"] == "analysis"
        assert manager._results[result_id]["data"]["score"] == 95

    def test_get_results(self, manager, mock_context):
        """Test get_results method."""
        # Add multiple results
        manager._results["r1"] = {"result_type": "type1", "data": {}}
        manager._results["r2"] = {"result_type": "type2", "data": {}}
        
        result = manager.get_results(mock_context, {})
        assert result.success is True
        assert len(result.data["results"]) == 2

    def test_cleanup(self, manager, mock_context):
        """Test cleanup operation."""
        manager._results["result-1"] = {"result_type": "test", "data": {}}
        manager._results["result-2"] = {"result_type": "test", "data": {}}
        
        result = manager.cleanup(mock_context)
        assert result is True
        assert len(manager._results) == 0

    def test_get_status(self, manager):
        """Test get_status operation."""
        manager._results["result-1"] = {"result_type": "test", "data": {}}
        manager._results["result-2"] = {"result_type": "test", "data": {}}
        
        status = manager.get_status()
        assert status["active_results"] == 2
        assert status["v2_compliant"] is True

    def test_get_status_empty(self, manager):
        """Test get_status with no results."""
        status = manager.get_status()
        assert status["active_results"] == 0
        assert status["v2_compliant"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

