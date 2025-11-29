"""
Unit tests for core_execution_manager.py - MEDIUM PRIORITY

Tests CoreExecutionManager class and execution operations.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.managers.contracts import ManagerContext, ManagerResult
from src.core.managers.core_execution_manager import CoreExecutionManager


class TestCoreExecutionManager:
    """Test suite for CoreExecutionManager class."""

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
        """Create CoreExecutionManager instance with mocked coordinator."""
        with patch('src.core.managers.core_execution_manager.ExecutionCoordinator') as mock_coord_class:
            mock_coord = MagicMock()
            mock_coord_class.return_value = mock_coord
            manager = CoreExecutionManager()
            manager.coordinator = mock_coord
            return manager

    def test_manager_initialization(self, manager):
        """Test manager initialization."""
        assert manager is not None
        assert hasattr(manager, 'coordinator')
        assert manager.coordinator is not None

    def test_initialize(self, manager, mock_context):
        """Test manager initialization with context."""
        with patch.object(manager.coordinator, 'initialize', return_value=True) as mock_init:
            result = manager.initialize(mock_context)
            assert result is True
            mock_init.assert_called_once_with(mock_context)

    def test_initialize_failure(self, manager, mock_context):
        """Test manager initialization failure."""
        with patch.object(manager.coordinator, 'initialize', return_value=False) as mock_init:
            result = manager.initialize(mock_context)
            assert result is False
            mock_init.assert_called_once_with(mock_context)

    def test_execute(self, manager, mock_context):
        """Test execute operation."""
        expected_result = ManagerResult(
            success=True,
            data={"result": "test"},
            metrics={}
        )
        with patch.object(manager.coordinator, 'execute', return_value=expected_result) as mock_exec:
            result = manager.execute(mock_context, "test_operation", {"key": "value"})
            assert result.success is True
            assert result.data == {"result": "test"}
            mock_exec.assert_called_once_with(mock_context, "test_operation", {"key": "value"})

    def test_execute_task(self, manager, mock_context):
        """Test execute_task operation."""
        expected_result = ManagerResult(
            success=True,
            data={"task_id": "task-123"},
            metrics={}
        )
        with patch.object(manager.coordinator, 'execute_task', return_value=expected_result) as mock_exec:
            result = manager.execute_task(mock_context, "task-123", {"data": "test"})
            assert result.success is True
            assert result.data == {"task_id": "task-123"}
            mock_exec.assert_called_once_with(mock_context, "task-123", {"data": "test"})

    def test_execute_task_with_none_id(self, manager, mock_context):
        """Test execute_task with None task_id."""
        expected_result = ManagerResult(
            success=True,
            data={"task_id": None},
            metrics={}
        )
        with patch.object(manager.coordinator, 'execute_task', return_value=expected_result) as mock_exec:
            result = manager.execute_task(mock_context, None, {"data": "test"})
            assert result.success is True
            mock_exec.assert_called_once_with(mock_context, None, {"data": "test"})

    def test_register_protocol(self, manager, mock_context):
        """Test register_protocol operation."""
        def protocol_handler(context, payload):
            return ManagerResult(success=True, data={}, metrics={})

        expected_result = ManagerResult(
            success=True,
            data={"protocol": "test_protocol"},
            metrics={}
        )
        with patch.object(manager.coordinator, 'register_protocol', return_value=expected_result) as mock_reg:
            result = manager.register_protocol(mock_context, "test_protocol", protocol_handler)
            assert result.success is True
            assert result.data == {"protocol": "test_protocol"}
            mock_reg.assert_called_once_with(mock_context, "test_protocol", protocol_handler)

    def test_get_execution_status(self, manager, mock_context):
        """Test get_execution_status operation."""
        expected_result = ManagerResult(
            success=True,
            data={"status": "running", "execution_id": "exec-123"},
            metrics={}
        )
        with patch.object(manager.coordinator, 'get_execution_status', return_value=expected_result) as mock_status:
            result = manager.get_execution_status(mock_context, "exec-123")
            assert result.success is True
            assert result.data["status"] == "running"
            mock_status.assert_called_once_with(mock_context, "exec-123")

    def test_get_execution_status_with_none_id(self, manager, mock_context):
        """Test get_execution_status with None execution_id."""
        expected_result = ManagerResult(
            success=True,
            data={"status": "idle"},
            metrics={}
        )
        with patch.object(manager.coordinator, 'get_execution_status', return_value=expected_result) as mock_status:
            result = manager.get_execution_status(mock_context, None)
            assert result.success is True
            mock_status.assert_called_once_with(mock_context, None)

    def test_cleanup(self, manager, mock_context):
        """Test cleanup operation."""
        with patch.object(manager.coordinator, 'cleanup', return_value=True) as mock_cleanup:
            result = manager.cleanup(mock_context)
            assert result is True
            mock_cleanup.assert_called_once_with(mock_context)

    def test_get_status(self, manager):
        """Test get_status operation."""
        expected_status = {"status": "active", "tasks": 5, "protocols": 3}
        with patch.object(manager.coordinator, 'get_status', return_value=expected_status) as mock_status:
            result = manager.get_status()
            assert result == expected_status
            assert result["status"] == "active"
            mock_status.assert_called_once()

    def test_create_task(self, manager, mock_context):
        """Test create_task public method."""
        expected_result = ManagerResult(
            success=True,
            data={"task_id": "task-456", "task_type": "test_task"},
            metrics={}
        )
        with patch.object(manager.coordinator, 'create_task', return_value=expected_result) as mock_create:
            result = manager.create_task(mock_context, "test_task", priority=8, data={"key": "value"})
            assert result.success is True
            assert result.data["task_id"] == "task-456"
            mock_create.assert_called_once_with(mock_context, "test_task", 8, {"key": "value"})

    def test_create_task_default_priority(self, manager, mock_context):
        """Test create_task with default priority."""
        expected_result = ManagerResult(
            success=True,
            data={"task_id": "task-789"},
            metrics={}
        )
        with patch.object(manager.coordinator, 'create_task', return_value=expected_result) as mock_create:
            result = manager.create_task(mock_context, "test_task")
            assert result.success is True
            mock_create.assert_called_once_with(mock_context, "test_task", 5, None)

    def test_execute_protocol(self, manager, mock_context):
        """Test execute_protocol public method."""
        expected_result = ManagerResult(
            success=True,
            data={"protocol": "test_protocol", "result": "success"},
            metrics={}
        )
        with patch.object(manager.coordinator, 'execute_protocol', return_value=expected_result) as mock_exec:
            result = manager.execute_protocol(mock_context, "test_protocol", {"param": "value"})
            assert result.success is True
            assert result.data["protocol"] == "test_protocol"
            mock_exec.assert_called_once_with(mock_context, "test_protocol", {"param": "value"})

    def test_execute_protocol_with_none_payload(self, manager, mock_context):
        """Test execute_protocol with None payload."""
        expected_result = ManagerResult(
            success=True,
            data={"protocol": "test_protocol"},
            metrics={}
        )
        with patch.object(manager.coordinator, 'execute_protocol', return_value=expected_result) as mock_exec:
            result = manager.execute_protocol(mock_context, "test_protocol", None)
            assert result.success is True
            mock_exec.assert_called_once_with(mock_context, "test_protocol", None)

    def test_get_task_status(self, manager, mock_context):
        """Test get_task_status public method."""
        expected_result = ManagerResult(
            success=True,
            data={"task_id": "task-123", "status": "completed"},
            metrics={}
        )
        with patch.object(manager.coordinator, 'get_task_status', return_value=expected_result) as mock_status:
            result = manager.get_task_status(mock_context, "task-123")
            assert result.success is True
            assert result.data["status"] == "completed"
            mock_status.assert_called_once_with(mock_context, "task-123")

    def test_error_handling_in_execute(self, manager, mock_context):
        """Test error handling in execute operation."""
        expected_result = ManagerResult(
            success=False,
            data={},
            metrics={},
            error="Execution failed"
        )
        with patch.object(manager.coordinator, 'execute', return_value=expected_result) as mock_exec:
            result = manager.execute(mock_context, "test_operation", {})
            assert result.success is False
            assert result.error == "Execution failed"
            mock_exec.assert_called_once()

    def test_error_handling_in_execute_task(self, manager, mock_context):
        """Test error handling in execute_task operation."""
        expected_result = ManagerResult(
            success=False,
            data={},
            metrics={},
            error="Task execution failed"
        )
        with patch.object(manager.coordinator, 'execute_task', return_value=expected_result) as mock_exec:
            result = manager.execute_task(mock_context, "task-123", {})
            assert result.success is False
            assert result.error == "Task execution failed"
            mock_exec.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

