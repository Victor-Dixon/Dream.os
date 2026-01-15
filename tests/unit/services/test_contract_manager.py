"""
Tests for contract_system/manager.py - ContractManager class.

Target: ≥85% coverage, 15+ tests.
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from src.services.unified_service_managers import UnifiedContractManager



class TestContractManager:
    """Test ContractManager class."""

    def test_init(self):
        """Test ContractManager initialization."""

        manager = UnifiedContractManager()

        assert manager.storage is not None
        assert manager.logger is not None

    def test_get_system_status_success(self):
        """Test successful system status retrieval."""

        manager = UnifiedContractManager()


        # Mock storage - create mock Contract objects with to_dict method
        class MockContract:
            def __init__(self, status, id_val):
                self.status = status
                self.id = id_val
            def to_dict(self):
                return {"status": self.status, "id": self.id}

        mock_contracts = [
            MockContract("active", "1"),
            MockContract("active", "2"),
            MockContract("completed", "3"),
            MockContract("pending", "4"),
        ]

        manager.storage.get_all_contracts = Mock(return_value=mock_contracts)

        status = manager.get_system_status()

        assert status["total_contracts"] == 4
        assert status["active_contracts"] == 2
        assert status["completed_contracts"] == 1
        assert status["pending_contracts"] == 1
        assert "last_updated" in status

    def test_get_system_status_exception(self):
        """Test system status retrieval with exception."""

        manager = UnifiedContractManager()

        manager.storage.get_all_contracts = Mock(
            side_effect=Exception("Error"))

        status = manager.get_system_status()

        assert "error" in status

    def test_get_agent_status_success(self):
        """Test successful agent status retrieval."""

        manager = UnifiedContractManager()


        # Mock storage - create mock Contract objects with to_dict method
        class MockContract:
            def __init__(self, status, id_val):
                self.status = status
                self.id = id_val
            def to_dict(self):
                return {"status": self.status, "id": self.id}

        mock_contracts = [
            MockContract("active", "1"),
            MockContract("completed", "2"),
        ]

        manager.storage.get_agent_contracts = Mock(return_value=mock_contracts)

        status = manager.get_agent_status("Agent-1")

        assert status["agent_id"] == "Agent-1"
        assert status["total_contracts"] == 2
        assert status["active_contracts"] == 1
        assert status["completed_contracts"] == 1
        assert "contracts" in status

    def test_get_agent_status_empty(self):
        """Test agent status retrieval with no contracts."""

        manager = UnifiedContractManager()

        manager.storage.get_agent_contracts = Mock(return_value=[])

        status = manager.get_agent_status("Agent-1")

        assert status["agent_id"] == "Agent-1"
        assert status["total_contracts"] == 0

    def test_get_agent_status_exception(self):
        """Test agent status retrieval with exception."""

        manager = UnifiedContractManager()

        manager.storage.get_agent_contracts = Mock(
            side_effect=Exception("Error"))

        status = manager.get_agent_status("Agent-1")

        assert "error" in status
        assert status["agent_id"] == "Agent-1"

    def test_get_next_task_success(self):
        """Test successful next task retrieval."""

        manager = UnifiedContractManager()


        mock_contracts = [
            {"id": "task1", "status": "pending", "title": "Task 1"},
            {"id": "task2", "status": "pending", "title": "Task 2"},
        ]

        manager.storage.get_all_contracts = Mock(return_value=mock_contracts)
        manager.storage.save_contract = Mock(return_value=True)

        result = manager.get_next_task("Agent-1")

        assert result["agent_id"] == "Agent-1"
        assert result["status"] == "assigned"
        assert result["task"]["assigned_to"] == "Agent-1"
        assert result["task"]["status"] == "active"
        assert "assigned_at" in result["task"]

    def test_get_next_task_no_tasks(self):
        """Test next task retrieval with no available tasks."""

        manager = UnifiedContractManager()

        # Mock both cycle planner and storage to return no tasks
        manager.cycle_planner.get_next_cycle_task = Mock(return_value=None)
        manager.storage.get_all_contracts = Mock(return_value=[])

        result = manager.get_next_task("Agent-1")

        assert result["agent_id"] == "Agent-1"
        assert result["task"] is None
        assert result["status"] == "no_tasks"
        assert result["message"] == "No available tasks"

    def test_get_next_task_only_active(self):
        """Test next task retrieval when only active tasks exist."""

        manager = UnifiedContractManager()


        mock_contracts = [
            {"id": "task1", "status": "active", "title": "Task 1"},
        ]

        manager.storage.get_all_contracts = Mock(return_value=mock_contracts)

        result = manager.get_next_task("Agent-1")

        assert result["status"] == "no_tasks"

    def test_get_next_task_exception(self):
        """Test next task retrieval with exception."""

        manager = UnifiedContractManager()

        manager.storage.get_all_contracts = Mock(
            side_effect=Exception("Error"))

        result = manager.get_next_task("Agent-1")

        assert "error" in result
        assert result["agent_id"] == "Agent-1"

    def test_add_task_to_contract_success(self):
        """Test successful task addition to contract."""

        manager = UnifiedContractManager()


        mock_contract = {
            "id": "contract1",
            "tasks": [],
            "last_updated": None,
        }

        manager.storage.get_contract = Mock(return_value=mock_contract)
        manager.storage.save_contract = Mock(return_value=True)

        task = {"id": "task1", "title": "New Task"}

        result = manager.add_task_to_contract("contract1", task)

        assert result is True
        assert len(mock_contract["tasks"]) == 1
        assert mock_contract["tasks"][0] == task
        assert mock_contract["last_updated"] is not None

    def test_add_task_to_contract_not_found(self):
        """Test task addition when contract not found."""

        manager = UnifiedContractManager()

        manager.storage.get_contract = Mock(return_value=None)

        result = manager.add_task_to_contract("nonexistent", {"id": "task1"})

        assert result is False

    def test_add_task_to_contract_no_tasks_key(self):
        """Test task addition when contract has no tasks key."""

        manager = UnifiedContractManager()


        mock_contract = {"id": "contract1"}

        manager.storage.get_contract = Mock(return_value=mock_contract)
        manager.storage.save_contract = Mock(return_value=True)

        task = {"id": "task1"}

        result = manager.add_task_to_contract("contract1", task)

        assert result is True
        assert "tasks" in mock_contract
        assert len(mock_contract["tasks"]) == 1

    def test_add_task_to_contract_exception(self):
        """Test task addition with exception."""

        manager = UnifiedContractManager()

        manager.storage.get_contract = Mock(side_effect=Exception("Error"))

        result = manager.add_task_to_contract("contract1", {"id": "task1"})

        assert result is False
