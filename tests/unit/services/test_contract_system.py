#!/usr/bin/env python3
"""
Unit Tests for Contract System
==============================

Tests for contract models, storage, and manager.

<!-- SSOT Domain: testing -->

Author: Agent-1 (Integration & Core Systems Specialist)
"""

import json
import tempfile
import shutil
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


class TestContractModels:
    """Unit tests for contract models."""

    def test_contract_status_enum(self):
        """Test ContractStatus enum values."""
        from src.services.contract_system.models import ContractStatus
        
        assert ContractStatus.PENDING.value == "pending"
        assert ContractStatus.ACTIVE.value == "active"
        assert ContractStatus.COMPLETED.value == "completed"
        assert ContractStatus.CANCELLED.value == "cancelled"

    def test_contract_priority_enum(self):
        """Test ContractPriority enum values."""
        from src.services.contract_system.models import ContractPriority
        
        assert ContractPriority.LOW.value == "low"
        assert ContractPriority.MEDIUM.value == "medium"
        assert ContractPriority.HIGH.value == "high"
        assert ContractPriority.URGENT.value == "urgent"

    def test_contract_task_init_defaults(self):
        """Test ContractTask initialization with defaults."""
        from src.services.contract_system.models import ContractTask
        
        task = ContractTask()
        
        assert task.task_id == ""
        assert task.title == ""
        assert task.status == "pending"
        assert task.priority == "medium"

    def test_contract_task_init_with_data(self):
        """Test ContractTask initialization with data."""
        from src.services.contract_system.models import ContractTask
        
        task = ContractTask(
            task_id="task-123",
            title="Test Task",
            description="A test task",
            priority="high"
        )
        
        assert task.task_id == "task-123"
        assert task.title == "Test Task"
        assert task.description == "A test task"
        assert task.priority == "high"

    def test_contract_task_to_dict(self):
        """Test ContractTask to_dict method."""
        from src.services.contract_system.models import ContractTask
        
        task = ContractTask(task_id="task-123", title="Test")
        result = task.to_dict()
        
        assert isinstance(result, dict)
        assert result["task_id"] == "task-123"
        assert result["title"] == "Test"

    def test_contract_task_from_dict(self):
        """Test ContractTask from_dict method."""
        from src.services.contract_system.models import ContractTask
        
        data = {"task_id": "task-456", "title": "From Dict", "priority": "high"}
        task = ContractTask.from_dict(data)
        
        assert task.task_id == "task-456"
        assert task.title == "From Dict"
        assert task.priority == "high"

    def test_contract_task_update_status(self):
        """Test ContractTask status update."""
        from src.services.contract_system.models import ContractTask
        import time
        
        task = ContractTask(task_id="task-123")
        original_updated = task.last_updated
        
        # Small delay to ensure timestamp changes
        time.sleep(0.01)
        task.update_status("completed")
        
        assert task.status == "completed"
        assert task.completed_at != ""

    def test_contract_task_assign_to(self):
        """Test ContractTask assignment."""
        from src.services.contract_system.models import ContractTask
        
        task = ContractTask(task_id="task-123")
        task.assign_to("Agent-1")
        
        assert task.assigned_to == "Agent-1"
        assert task.status == "in_progress"

    def test_contract_init_defaults(self):
        """Test Contract initialization with defaults."""
        from src.services.contract_system.models import Contract
        
        contract = Contract()
        
        assert contract.contract_id == ""
        assert contract.status == "pending"
        assert contract.priority == "medium"
        assert contract.tasks == []
        assert contract.roi_score == 0.0

    def test_contract_init_with_data(self):
        """Test Contract initialization with data."""
        from src.services.contract_system.models import Contract
        
        contract = Contract(
            contract_id="contract-123",
            title="Test Contract",
            priority="high",
            user_value=100.0,
            effort=5.0,
            risk=2.0
        )
        
        assert contract.contract_id == "contract-123"
        assert contract.title == "Test Contract"
        assert contract.priority == "high"
        assert contract.user_value == 100.0

    def test_contract_to_dict(self):
        """Test Contract to_dict method."""
        from src.services.contract_system.models import Contract
        
        contract = Contract(contract_id="contract-123", title="Test")
        result = contract.to_dict()
        
        assert isinstance(result, dict)
        assert result["contract_id"] == "contract-123"

    def test_contract_from_dict(self):
        """Test Contract from_dict method."""
        from src.services.contract_system.models import Contract
        
        data = {"contract_id": "contract-456", "title": "From Dict"}
        contract = Contract.from_dict(data)
        
        assert contract.contract_id == "contract-456"
        assert contract.title == "From Dict"

    def test_contract_update_status(self):
        """Test Contract status update."""
        from src.services.contract_system.models import Contract
        
        contract = Contract(contract_id="contract-123")
        contract.update_status("completed")
        
        assert contract.status == "completed"
        assert contract.completed_at != ""

    def test_contract_assign_to(self):
        """Test Contract assignment."""
        from src.services.contract_system.models import Contract
        
        contract = Contract(contract_id="contract-123")
        contract.assign_to("Agent-1")
        
        assert contract.assigned_to == "Agent-1"
        assert contract.status == "active"
        assert contract.assigned_at != ""

    def test_contract_add_task(self):
        """Test adding task to contract."""
        from src.services.contract_system.models import Contract
        
        contract = Contract(contract_id="contract-123")
        task_data = {"task_id": "task-1", "title": "Task 1"}
        
        contract.add_task(task_data)
        
        assert len(contract.tasks) == 1
        assert contract.tasks[0]["task_id"] == "task-1"

    def test_contract_calculate_roi(self):
        """Test ROI calculation."""
        from src.services.contract_system.models import Contract
        
        contract = Contract(
            contract_id="contract-123",
            user_value=100.0,
            effort=10.0,
            risk=2.0,
            dependency_count=0
        )
        
        roi = contract.calculate_roi()
        
        # ROI = 100 / (10 + 0) / 2 = 5.0
        assert roi == 5.0
        assert contract.roi_score == 5.0

    def test_contract_calculate_roi_with_dependencies(self):
        """Test ROI calculation with dependencies."""
        from src.services.contract_system.models import Contract
        
        contract = Contract(
            contract_id="contract-123",
            user_value=100.0,
            effort=5.0,
            risk=2.0,
            dependency_count=5
        )
        
        roi = contract.calculate_roi()
        
        # ROI = 100 / (5 + 5) / 2 = 5.0
        assert roi == 5.0


class TestContractStorage:
    """Unit tests for ContractStorage."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        
        from src.services.contract_system.storage import ContractStorage
        self.storage = ContractStorage(base_path=self.temp_dir)

    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_init_creates_directories(self):
        """Test that init creates necessary directories."""
        assert Path(self.temp_dir).exists()
        assert self.storage.agent_contracts_dir.exists()

    def test_save_contract(self):
        """Test saving a contract."""
        from src.services.contract_system.models import Contract
        
        contract = Contract(contract_id="test-123", title="Test Contract")
        result = self.storage.save_contract(contract)
        
        assert result is True
        assert self.storage.contracts_file.exists()

    def test_load_contract(self):
        """Test loading a contract."""
        from src.services.contract_system.models import Contract
        
        # Save first
        contract = Contract(contract_id="test-123", title="Test Contract")
        self.storage.save_contract(contract)
        
        # Load
        loaded = self.storage.load_contract("test-123")
        
        assert loaded is not None
        assert loaded.contract_id == "test-123"
        assert loaded.title == "Test Contract"

    def test_load_contract_not_found(self):
        """Test loading non-existent contract."""
        loaded = self.storage.load_contract("nonexistent")
        assert loaded is None

    def test_get_contract_alias(self):
        """Test get_contract is alias for load_contract."""
        from src.services.contract_system.models import Contract
        
        contract = Contract(contract_id="test-456", title="Test")
        self.storage.save_contract(contract)
        
        loaded = self.storage.get_contract("test-456")
        assert loaded is not None
        assert loaded.contract_id == "test-456"

    def test_load_all_contracts_empty(self):
        """Test loading all contracts when empty."""
        contracts = self.storage.load_all_contracts()
        assert contracts == {}

    def test_load_all_contracts(self):
        """Test loading all contracts."""
        from src.services.contract_system.models import Contract
        
        self.storage.save_contract(Contract(contract_id="c1", title="Contract 1"))
        self.storage.save_contract(Contract(contract_id="c2", title="Contract 2"))
        
        contracts = self.storage.load_all_contracts()
        
        assert len(contracts) == 2
        assert "c1" in contracts
        assert "c2" in contracts

    def test_get_all_contracts_as_list(self):
        """Test get_all_contracts returns list."""
        from src.services.contract_system.models import Contract
        
        self.storage.save_contract(Contract(contract_id="c1", title="Contract 1"))
        self.storage.save_contract(Contract(contract_id="c2", title="Contract 2"))
        
        contracts = self.storage.get_all_contracts()
        
        assert isinstance(contracts, list)
        assert len(contracts) == 2

    def test_save_contract_with_agent(self):
        """Test saving contract with assigned agent."""
        from src.services.contract_system.models import Contract
        
        contract = Contract(contract_id="test-789", title="Test")
        contract.assign_to("Agent-1")
        
        result = self.storage.save_contract(contract)
        
        assert result is True
        agent_file = self.storage.agent_contracts_dir / "Agent-1_contracts.json"
        assert agent_file.exists()

    def test_load_agent_contracts(self):
        """Test loading agent-specific contracts."""
        from src.services.contract_system.models import Contract
        
        contract = Contract(contract_id="test-agent", title="Agent Contract")
        contract.assign_to("Agent-2")
        self.storage.save_contract(contract)
        
        agent_contracts = self.storage.load_agent_contracts("Agent-2")
        
        assert "test-agent" in agent_contracts

    def test_load_agent_contracts_empty(self):
        """Test loading agent contracts when none exist."""
        contracts = self.storage.load_agent_contracts("NonexistentAgent")
        assert contracts == {}

    def test_get_agent_contracts_as_objects(self):
        """Test get_agent_contracts returns Contract objects."""
        from src.services.contract_system.models import Contract
        
        contract = Contract(contract_id="test-obj", title="Object Contract")
        contract.assign_to("Agent-3")
        self.storage.save_contract(contract)
        
        contracts = self.storage.get_agent_contracts("Agent-3")
        
        assert len(contracts) > 0
        assert isinstance(contracts[0], Contract)


class TestContractManager:
    """Unit tests for ContractManager."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        
        # Patch storage to use temp directory
        with patch('src.services.contract_system.manager.ContractStorage') as mock_storage:
            from src.services.contract_system.storage import ContractStorage
            mock_storage.return_value = ContractStorage(base_path=self.temp_dir)
            
            from src.services.contract_system.manager import ContractManager
            self.manager = ContractManager()
            self.manager.storage = ContractStorage(base_path=self.temp_dir)

    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_get_system_status_empty(self):
        """Test system status when no contracts exist."""
        status = self.manager.get_system_status()
        
        assert status["total_contracts"] == 0
        assert status["active_contracts"] == 0
        assert status["completed_contracts"] == 0
        assert status["pending_contracts"] == 0

    def test_get_system_status_with_contracts(self):
        """Test system status with existing contracts."""
        from src.services.contract_system.models import Contract
        
        # Add some contracts with explicit status values
        c1 = Contract(contract_id="c1", title="Test 1")
        c1.status = "pending"
        c2 = Contract(contract_id="c2", title="Test 2")
        c2.status = "active"
        c3 = Contract(contract_id="c3", title="Test 3")
        c3.status = "completed"
        
        self.manager.storage.save_contract(c1)
        self.manager.storage.save_contract(c2)
        self.manager.storage.save_contract(c3)
        
        status = self.manager.get_system_status()
        
        # Verify total contracts saved
        assert status["total_contracts"] == 3

    def test_get_agent_status(self):
        """Test getting agent-specific status."""
        status = self.manager.get_agent_status("Agent-1")
        
        assert status["agent_id"] == "Agent-1"
        assert status["total_contracts"] == 0

    def test_get_next_task_no_tasks(self):
        """Test getting next task when none available."""
        with patch.object(self.manager.cycle_planner, 'get_next_cycle_task', return_value=None):
            result = self.manager.get_next_task("Agent-1")
        
        assert result["agent_id"] == "Agent-1"
        assert result["status"] == "no_tasks"

    def test_get_next_task_from_cycle_planner(self):
        """Test getting next task from cycle planner."""
        mock_task = {
            "task_id": "cycle-task-1",
            "title": "Cycle Planner Task",
            "status": "pending"
        }
        
        with patch.object(self.manager.cycle_planner, 'get_next_cycle_task', return_value=mock_task):
            with patch.object(self.manager, '_mark_cycle_task_active', return_value=True):
                result = self.manager.get_next_task("Agent-1")
        
        assert result["status"] == "assigned"
        assert result["source"] == "cycle_planner"
        assert result["task"]["task_id"] == "cycle-task-1"

    def test_get_next_task_from_contracts(self):
        """Test getting next task from contract system."""
        from src.services.contract_system.models import Contract
        
        # Add pending contract with non-empty tasks to pass validation
        contract = Contract(
            contract_id="contract-1",
            title="Test Contract",
            status="pending",
            user_value=100.0,
            effort=10.0,
            risk=1.0
        )
        # Add tasks to avoid empty tasks array check
        contract.tasks = [{"task_id": "t1", "title": "Sub-task 1"}]
        self.manager.storage.save_contract(contract)
        
        with patch.object(self.manager.cycle_planner, 'get_next_cycle_task', return_value=None):
            with patch.object(self.manager, '_bootstrap_tasks_from_master_log', return_value=False):
                with patch.object(self.manager, '_notify_captain_no_tasks'):
                    result = self.manager.get_next_task("Agent-1")
        
        assert result["status"] == "assigned"
        assert result["source"] == "contract_system"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

