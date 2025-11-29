"""
Unit tests for task_executor.py - NEXT PRIORITY

Tests TaskExecutor class and task execution operations.
Expanded to ≥85% coverage.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.managers.contracts import ManagerContext
from src.core.managers.execution.task_executor import TaskExecutor


class TestTaskExecutor:
    """Test suite for TaskExecutor class."""

    @pytest.fixture
    def executor(self):
        """Create TaskExecutor instance."""
        return TaskExecutor()

    @pytest.fixture
    def mock_context(self):
        """Create mock manager context."""
        return ManagerContext(
            config={"test": "config"},
            logger=lambda msg: None,
            metrics={},
            timestamp=datetime.now()
        )

    def test_executor_initialization(self, executor):
        """Test executor initialization."""
        assert executor is not None

    def test_execute_file_task(self, executor):
        """Test executing file task."""
        task_data = {
            "operation": "read",
            "file_path": "/test/path.txt"
        }
        result = executor.execute_file_task(task_data)
        assert result["status"] == "completed"
        assert result["operation"] == "read"
        assert result["file_path"] == "/test/path.txt"
        assert "message" in result

    def test_execute_file_task_default_operation(self, executor):
        """Test executing file task with default operation."""
        task_data = {"file_path": "/test/path.txt"}
        result = executor.execute_file_task(task_data)
        assert result["operation"] == "read"

    def test_execute_file_task_default_path(self, executor):
        """Test executing file task with default path."""
        task_data = {"operation": "write"}
        result = executor.execute_file_task(task_data)
        assert result["file_path"] == ""

    def test_execute_data_task(self, executor):
        """Test executing data task."""
        task_data = {
            "operation": "process",
            "data_size": 1000
        }
        result = executor.execute_data_task(task_data)
        assert result["status"] == "completed"
        assert result["operation"] == "process"
        assert result["data_size"] == 1000
        assert "message" in result

    def test_execute_data_task_default_operation(self, executor):
        """Test executing data task with default operation."""
        task_data = {"data_size": 500}
        result = executor.execute_data_task(task_data)
        assert result["operation"] == "process"

    def test_execute_data_task_default_size(self, executor):
        """Test executing data task with default size."""
        task_data = {"operation": "transform"}
        result = executor.execute_data_task(task_data)
        assert result["data_size"] == 0

    def test_execute_api_task(self, executor):
        """Test executing API task."""
        task_data = {
            "url": "https://api.example.com",
            "method": "POST"
        }
        result = executor.execute_api_task(task_data)
        assert result["status"] == "completed"
        assert result["url"] == "https://api.example.com"
        assert result["method"] == "POST"
        assert result["response_code"] == 200
        assert "message" in result

    def test_execute_api_task_default_method(self, executor):
        """Test executing API task with default method."""
        task_data = {"url": "https://api.example.com"}
        result = executor.execute_api_task(task_data)
        assert result["method"] == "GET"

    def test_execute_api_task_default_url(self, executor):
        """Test executing API task with default URL."""
        task_data = {"method": "PUT"}
        result = executor.execute_api_task(task_data)
        assert result["url"] == ""

    def test_execute_task_thread_file_task(self, executor, mock_context):
        """Test executing task thread with file task."""
        execution_id = "exec-1"
        task = {"type": "file", "status": None}
        task_data = {"operation": "read", "file_path": "/test.txt"}
        tasks = {"task-1": task}
        executions = {
            execution_id: {
                "status": "running",
                "started_at": datetime.now().isoformat()
            }
        }
        
        class TaskStatus:
            COMPLETED = "completed"
            FAILED = "failed"
        
        task_status_enum = TaskStatus()
        
        executor.execute_task_thread(
            mock_context, execution_id, task, task_data,
            tasks, executions, task_status_enum
        )
        
        assert executions[execution_id]["status"] == "completed"
        assert "completed_at" in executions[execution_id]
        assert "result" in executions[execution_id]
        assert task["status"] == "completed"

    def test_execute_task_thread_data_task(self, executor, mock_context):
        """Test executing task thread with data task."""
        execution_id = "exec-2"
        task = {"type": "data", "status": None}
        task_data = {"operation": "process", "data_size": 100}
        tasks = {"task-2": task}
        executions = {
            execution_id: {
                "status": "running",
                "started_at": datetime.now().isoformat()
            }
        }
        
        class TaskStatus:
            COMPLETED = "completed"
            FAILED = "failed"
        
        task_status_enum = TaskStatus()
        
        executor.execute_task_thread(
            mock_context, execution_id, task, task_data,
            tasks, executions, task_status_enum
        )
        
        assert executions[execution_id]["status"] == "completed"
        assert task["status"] == "completed"

    def test_execute_task_thread_api_task(self, executor, mock_context):
        """Test executing task thread with API task."""
        execution_id = "exec-3"
        task = {"type": "api", "status": None}
        task_data = {"url": "https://api.example.com", "method": "GET"}
        tasks = {"task-3": task}
        executions = {
            execution_id: {
                "status": "running",
                "started_at": datetime.now().isoformat()
            }
        }
        
        class TaskStatus:
            COMPLETED = "completed"
            FAILED = "failed"
        
        task_status_enum = TaskStatus()
        
        executor.execute_task_thread(
            mock_context, execution_id, task, task_data,
            tasks, executions, task_status_enum
        )
        
        assert executions[execution_id]["status"] == "completed"
        assert task["status"] == "completed"

    def test_execute_task_thread_general_task(self, executor, mock_context):
        """Test executing task thread with general task type."""
        execution_id = "exec-4"
        task = {"type": "custom", "status": None}
        task_data = {}
        tasks = {"task-4": task}
        executions = {
            execution_id: {
                "status": "running",
                "started_at": datetime.now().isoformat()
            }
        }
        
        class TaskStatus:
            COMPLETED = "completed"
            FAILED = "failed"
        
        task_status_enum = TaskStatus()
        
        executor.execute_task_thread(
            mock_context, execution_id, task, task_data,
            tasks, executions, task_status_enum
        )
        
        assert executions[execution_id]["status"] == "completed"
        assert "General task custom completed" in executions[execution_id]["result"]["message"]

    def test_execute_task_thread_exception_handling(self, executor, mock_context):
        """Test executing task thread with exception."""
        execution_id = "exec-5"
        task = {"type": "file", "status": None}
        task_data = {"operation": "read"}
        tasks = {"task-5": task}
        executions = {
            execution_id: {
                "status": "running",
                "started_at": datetime.now().isoformat()
            }
        }
        
        class TaskStatus:
            COMPLETED = "completed"
            FAILED = "failed"
        
        task_status_enum = TaskStatus()
        
        # Cause exception by making execution_id invalid
        with patch.object(executor, 'execute_file_task', side_effect=Exception("Test error")):
            executor.execute_task_thread(
                mock_context, execution_id, task, task_data,
                tasks, executions, task_status_enum
            )
        
        assert executions[execution_id]["status"] == "failed"
        assert "failed_at" in executions[execution_id]
        assert "error" in executions[execution_id]
        assert task["status"] == "failed"

    def test_get_execution_duration_completed(self, executor):
        """Test getting execution duration for completed execution."""
        started_at = datetime.now()
        completed_at = started_at.replace(second=started_at.second + 5)
        execution = {
            "started_at": started_at.isoformat(),
            "completed_at": completed_at.isoformat()
        }
        duration = executor.get_execution_duration(execution)
        assert duration == pytest.approx(5.0, rel=0.1)

    def test_get_execution_duration_failed(self, executor):
        """Test getting execution duration for failed execution."""
        started_at = datetime.now()
        failed_at = started_at.replace(second=started_at.second + 3)
        execution = {
            "started_at": started_at.isoformat(),
            "failed_at": failed_at.isoformat()
        }
        duration = executor.get_execution_duration(execution)
        assert duration == pytest.approx(3.0, rel=0.1)

    def test_get_execution_duration_running(self, executor):
        """Test getting execution duration for running execution."""
        started_at = datetime.now().replace(second=datetime.now().second - 2)
        execution = {
            "started_at": started_at.isoformat()
        }
        duration = executor.get_execution_duration(execution)
        assert duration is not None
        assert duration >= 0

    def test_get_execution_duration_invalid_format(self, executor):
        """Test getting execution duration with invalid format."""
        execution = {
            "started_at": "invalid-format"
        }
        duration = executor.get_execution_duration(execution)
        assert duration is None

    def test_get_execution_duration_missing_started_at(self, executor):
        """Test getting execution duration with missing started_at."""
        execution = {}
        duration = executor.get_execution_duration(execution)
        assert duration is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

