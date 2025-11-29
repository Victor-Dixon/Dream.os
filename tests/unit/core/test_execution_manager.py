"""
Unit tests for src/core/ssot/unified_ssot/execution/execution_manager.py
"""

import pytest
from datetime import datetime

from src.core.ssot.unified_ssot.execution.execution_manager import ExecutionManager
from src.core.ssot.ssot_models import SSOTIntegrationResult, SSOTStatus


class TestExecutionManager:
    """Test ExecutionManager functionality."""

    @pytest.fixture
    def execution_manager(self):
        """Create ExecutionManager instance."""
        return ExecutionManager()

    @pytest.fixture
    def sample_result(self):
        """Create sample SSOTIntegrationResult."""
        return SSOTIntegrationResult(
            component_id="test_component",
            status=SSOTStatus.COMPLETED,
            execution_time=1.5,
            message="Test execution"
        )

    def test_execution_manager_creation(self, execution_manager):
        """Test that ExecutionManager can be created."""
        assert execution_manager is not None
        assert execution_manager.execution_history == []
        assert execution_manager.performance_metrics == {}

    def test_add_execution_result(self, execution_manager, sample_result):
        """Test that add_execution_result() adds result to history."""
        execution_manager.add_execution_result(sample_result)
        assert len(execution_manager.execution_history) == 1
        assert execution_manager.execution_history[0] == sample_result

    def test_get_execution_history(self, execution_manager, sample_result):
        """Test that get_execution_history() returns history."""
        execution_manager.add_execution_result(sample_result)
        history = execution_manager.get_execution_history()
        assert len(history) == 1
        assert history[0] == sample_result

    def test_get_execution_history_limit(self, execution_manager, sample_result):
        """Test that get_execution_history() respects limit."""
        for i in range(5):
            execution_manager.add_execution_result(sample_result)
        history = execution_manager.get_execution_history(limit=3)
        assert len(history) == 3

    def test_get_performance_metrics_empty(self, execution_manager):
        """Test that get_performance_metrics() returns empty metrics when no history."""
        metrics = execution_manager.get_performance_metrics()
        assert metrics["total_executions"] == 0
        assert metrics["success_rate"] == 0.0
        assert metrics["average_execution_time"] == 0.0

    def test_get_performance_metrics_with_history(self, execution_manager, sample_result):
        """Test that get_performance_metrics() calculates metrics correctly."""
        execution_manager.add_execution_result(sample_result)
        metrics = execution_manager.get_performance_metrics()
        assert metrics["total_executions"] == 1
        assert metrics["success_rate"] == 100.0
        assert metrics["average_execution_time"] == 1.5



