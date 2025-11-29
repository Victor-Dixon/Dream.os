"""
Unit tests for contract_system/models.py
Target: ≥85% coverage
"""

import pytest
from datetime import datetime
from src.services.contract_system.models import (
    ContractStatus,
    ContractPriority,
    TaskStatus,
    Task,
    Contract,
)


class TestEnums:
    """Tests for enum classes."""

    def test_contract_status_values(self):
        """Test ContractStatus enum values."""
        assert ContractStatus.PENDING.value == "pending"
        assert ContractStatus.ACTIVE.value == "active"
        assert ContractStatus.COMPLETED.value == "completed"
        assert ContractStatus.CANCELLED.value == "cancelled"

    def test_contract_priority_values(self):
        """Test ContractPriority enum values."""
        assert ContractPriority.LOW.value == "low"
        assert ContractPriority.MEDIUM.value == "medium"
        assert ContractPriority.HIGH.value == "high"
        assert ContractPriority.URGENT.value == "urgent"

    def test_task_status_values(self):
        """Test TaskStatus enum values."""
        assert TaskStatus.PENDING.value == "pending"
        assert TaskStatus.IN_PROGRESS.value == "in_progress"
        assert TaskStatus.COMPLETED.value == "completed"
        assert TaskStatus.CANCELLED.value == "cancelled"


class TestTask:
    """Tests for Task class."""

    def test_init_defaults(self):
        """Test Task initialization with defaults."""
        task = Task()
        assert task.task_id == ""
        assert task.title == ""
        assert task.description == ""
        assert task.status == TaskStatus.PENDING.value
        assert task.priority == ContractPriority.MEDIUM.value
        assert task.assigned_to == ""
        assert task.created_at is not None
        assert task.due_date == ""
        assert task.completed_at == ""
        assert task.last_updated is not None

    def test_init_with_kwargs(self):
        """Test Task initialization with provided values."""
        task = Task(
            task_id="T1",
            title="Test Task",
            description="Test Description",
            status="in_progress",
            priority="high",
            assigned_to="Agent-1"
        )
        assert task.task_id == "T1"
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.status == "in_progress"
        assert task.priority == "high"
        assert task.assigned_to == "Agent-1"

    def test_to_dict(self):
        """Test Task.to_dict conversion."""
        task = Task(
            task_id="T1",
            title="Test Task",
            status="pending"
        )
        result = task.to_dict()
        
        assert isinstance(result, dict)
        assert result["task_id"] == "T1"
        assert result["title"] == "Test Task"
        assert result["status"] == "pending"
        assert "created_at" in result
        assert "last_updated" in result

    def test_from_dict(self):
        """Test Task.from_dict creation."""
        data = {
            "task_id": "T1",
            "title": "Test Task",
            "status": "pending",
            "priority": "high"
        }
        task = Task.from_dict(data)
        
        assert task.task_id == "T1"
        assert task.title == "Test Task"
        assert task.status == "pending"
        assert task.priority == "high"

    def test_update_status_pending(self):
        """Test update_status with pending status."""
        task = Task(task_id="T1")
        original_updated = task.last_updated
        
        task.update_status("pending")
        
        assert task.status == "pending"
        assert task.completed_at == ""
        assert task.last_updated != original_updated

    def test_update_status_completed(self):
        """Test update_status with completed status sets completed_at."""
        task = Task(task_id="T1")
        
        task.update_status(TaskStatus.COMPLETED.value)
        
        assert task.status == TaskStatus.COMPLETED.value
        assert task.completed_at is not None
        assert task.completed_at != ""

    def test_assign_to(self):
        """Test assign_to method."""
        task = Task(task_id="T1")
        original_updated = task.last_updated
        
        task.assign_to("Agent-1")
        
        assert task.assigned_to == "Agent-1"
        assert task.status == TaskStatus.IN_PROGRESS.value
        assert task.last_updated != original_updated


class TestContract:
    """Tests for Contract class."""

    def test_init_defaults(self):
        """Test Contract initialization with defaults."""
        contract = Contract()
        assert contract.contract_id == ""
        assert contract.title == ""
        assert contract.description == ""
        assert contract.status == ContractStatus.PENDING.value
        assert contract.priority == ContractPriority.MEDIUM.value
        assert contract.assigned_to == ""
        assert contract.created_at is not None
        assert contract.assigned_at == ""
        assert contract.completed_at == ""
        assert contract.tasks == []
        assert contract.last_updated is not None

    def test_init_with_kwargs(self):
        """Test Contract initialization with provided values."""
        contract = Contract(
            contract_id="C1",
            title="Test Contract",
            description="Test Description",
            status="active",
            priority="high",
            assigned_to="Agent-1"
        )
        assert contract.contract_id == "C1"
        assert contract.title == "Test Contract"
        assert contract.description == "Test Description"
        assert contract.status == "active"
        assert contract.priority == "high"
        assert contract.assigned_to == "Agent-1"

    def test_to_dict(self):
        """Test Contract.to_dict conversion."""
        contract = Contract(
            contract_id="C1",
            title="Test Contract",
            status="pending"
        )
        result = contract.to_dict()
        
        assert isinstance(result, dict)
        assert result["contract_id"] == "C1"
        assert result["title"] == "Test Contract"
        assert result["status"] == "pending"
        assert result["tasks"] == []
        assert "created_at" in result
        assert "last_updated" in result

    def test_from_dict(self):
        """Test Contract.from_dict creation."""
        data = {
            "contract_id": "C1",
            "title": "Test Contract",
            "status": "active",
            "priority": "high",
            "tasks": []
        }
        contract = Contract.from_dict(data)
        
        assert contract.contract_id == "C1"
        assert contract.title == "Test Contract"
        assert contract.status == "active"
        assert contract.priority == "high"
        assert contract.tasks == []

    def test_update_status_pending(self):
        """Test update_status with pending status."""
        contract = Contract(contract_id="C1")
        original_updated = contract.last_updated
        
        contract.update_status("pending")
        
        assert contract.status == "pending"
        assert contract.completed_at == ""
        assert contract.last_updated != original_updated

    def test_update_status_completed(self):
        """Test update_status with completed status sets completed_at."""
        contract = Contract(contract_id="C1")
        
        contract.update_status(ContractStatus.COMPLETED.value)
        
        assert contract.status == ContractStatus.COMPLETED.value
        assert contract.completed_at is not None
        assert contract.completed_at != ""

    def test_assign_to(self):
        """Test assign_to method."""
        contract = Contract(contract_id="C1")
        original_updated = contract.last_updated
        
        contract.assign_to("Agent-1")
        
        assert contract.assigned_to == "Agent-1"
        assert contract.status == ContractStatus.ACTIVE.value
        assert contract.assigned_at is not None
        assert contract.assigned_at != ""
        assert contract.last_updated != original_updated

    def test_add_task_empty_list(self):
        """Test add_task creates tasks list if empty."""
        contract = Contract(contract_id="C1")
        original_updated = contract.last_updated
        
        task = {"task_id": "T1", "title": "New Task"}
        contract.add_task(task)
        
        assert len(contract.tasks) == 1
        assert contract.tasks[0] == task
        assert contract.last_updated != original_updated

    def test_add_task_existing_list(self):
        """Test add_task appends to existing tasks list."""
        contract = Contract(contract_id="C1", tasks=[{"task_id": "T1"}])
        
        task = {"task_id": "T2", "title": "New Task"}
        contract.add_task(task)
        
        assert len(contract.tasks) == 2
        assert contract.tasks[1] == task

    def test_add_task_multiple(self):
        """Test add_task with multiple tasks."""
        contract = Contract(contract_id="C1")
        
        task1 = {"task_id": "T1"}
        task2 = {"task_id": "T2"}
        task3 = {"task_id": "T3"}
        
        contract.add_task(task1)
        contract.add_task(task2)
        contract.add_task(task3)
        
        assert len(contract.tasks) == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

