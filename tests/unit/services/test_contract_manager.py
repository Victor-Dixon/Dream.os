"""
Unit tests for contract_system/manager.py
Target: ≥85% coverage
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from src.services.contract_system.manager import ContractManager


class TestContractManager:
    """Tests for ContractManager class."""

    def test_init(self):
        """Test ContractManager initialization."""
        manager = ContractManager()
        assert manager.storage is not None
        assert manager.logger is not None

    def test_get_system_status_success(self):
        """Test get_system_status returns correct status."""
        manager = ContractManager()
        
        mock_contracts = [
            {"status": "active", "contract_id": "C1"},
            {"status": "active", "contract_id": "C2"},
            {"status": "completed", "contract_id": "C3"},
            {"status": "pending", "contract_id": "C4"},
        ]
        
        with patch.object(manager.storage, 'get_all_contracts', return_value=mock_contracts):
            status = manager.get_system_status()
            
            assert status["total_contracts"] == 4
            assert status["active_contracts"] == 2
            assert status["completed_contracts"] == 1
            assert status["pending_contracts"] == 1
            assert "last_updated" in status

    def test_get_system_status_empty(self):
        """Test get_system_status with no contracts."""
        manager = ContractManager()
        
        with patch.object(manager.storage, 'get_all_contracts', return_value=[]):
            status = manager.get_system_status()
            
            assert status["total_contracts"] == 0
            assert status["active_contracts"] == 0
            assert status["completed_contracts"] == 0
            assert status["pending_contracts"] == 0

    def test_get_system_status_exception(self):
        """Test get_system_status handles exceptions."""
        manager = ContractManager()
        
        with patch.object(manager.storage, 'get_all_contracts', side_effect=Exception("Storage error")):
            status = manager.get_system_status()
            
            assert "error" in status
            assert "Storage error" in status["error"]

    def test_get_agent_status_success(self):
        """Test get_agent_status returns correct status."""
        manager = ContractManager()
        
        mock_contracts = [
            {"status": "active", "contract_id": "C1"},
            {"status": "completed", "contract_id": "C2"},
        ]
        
        with patch.object(manager.storage, 'get_agent_contracts', return_value=mock_contracts):
            status = manager.get_agent_status("Agent-1")
            
            assert status["agent_id"] == "Agent-1"
            assert status["total_contracts"] == 2
            assert status["active_contracts"] == 1
            assert status["completed_contracts"] == 1
            assert "contracts" in status
            assert "last_updated" in status

    def test_get_agent_status_empty(self):
        """Test get_agent_status with no contracts."""
        manager = ContractManager()
        
        with patch.object(manager.storage, 'get_agent_contracts', return_value=[]):
            status = manager.get_agent_status("Agent-1")
            
            assert status["agent_id"] == "Agent-1"
            assert status["total_contracts"] == 0
            assert status["active_contracts"] == 0
            assert status["completed_contracts"] == 0

    def test_get_agent_status_exception(self):
        """Test get_agent_status handles exceptions."""
        manager = ContractManager()
        
        with patch.object(manager.storage, 'get_agent_contracts', side_effect=Exception("Storage error")):
            status = manager.get_agent_status("Agent-1")
            
            assert "error" in status
            assert status["agent_id"] == "Agent-1"

    def test_get_next_task_available(self):
        """Test get_next_task assigns available task."""
        manager = ContractManager()
        
        mock_contracts = [
            {"status": "pending", "contract_id": "C1", "title": "Task 1"},
            {"status": "active", "contract_id": "C2", "title": "Task 2"},
        ]
        
        with patch.object(manager.storage, 'get_all_contracts', return_value=mock_contracts):
            with patch.object(manager.storage, 'save_contract', return_value=True) as mock_save:
                result = manager.get_next_task("Agent-1")
                
                assert result["agent_id"] == "Agent-1"
                assert result["status"] == "assigned"
                assert result["task"] is not None
                assert result["task"]["assigned_to"] == "Agent-1"
                assert result["task"]["status"] == "active"
                assert "assigned_at" in result["task"]
                mock_save.assert_called_once()

    def test_get_next_task_no_available(self):
        """Test get_next_task when no tasks available."""
        manager = ContractManager()
        
        mock_contracts = [
            {"status": "active", "contract_id": "C1"},
            {"status": "completed", "contract_id": "C2"},
        ]
        
        with patch.object(manager.storage, 'get_all_contracts', return_value=mock_contracts):
            result = manager.get_next_task("Agent-1")
            
            assert result["agent_id"] == "Agent-1"
            assert result["task"] is None
            assert result["status"] == "no_tasks"
            assert "No available tasks" in result["message"]

    def test_get_next_task_empty_list(self):
        """Test get_next_task with empty contract list."""
        manager = ContractManager()
        
        with patch.object(manager.storage, 'get_all_contracts', return_value=[]):
            result = manager.get_next_task("Agent-1")
            
            assert result["status"] == "no_tasks"
            assert result["task"] is None

    def test_get_next_task_exception(self):
        """Test get_next_task handles exceptions."""
        manager = ContractManager()
        
        with patch.object(manager.storage, 'get_all_contracts', side_effect=Exception("Storage error")):
            result = manager.get_next_task("Agent-1")
            
            assert "error" in result
            assert result["agent_id"] == "Agent-1"

    def test_add_task_to_contract_success(self):
        """Test add_task_to_contract successfully adds task."""
        manager = ContractManager()
        
        mock_contract = {
            "contract_id": "C1",
            "title": "Test Contract",
            "tasks": []
        }
        
        new_task = {"task_id": "T1", "title": "New Task"}
        
        with patch.object(manager.storage, 'get_contract', return_value=mock_contract):
            with patch.object(manager.storage, 'save_contract', return_value=True) as mock_save:
                result = manager.add_task_to_contract("C1", new_task)
                
                assert result is True
                assert len(mock_contract["tasks"]) == 1
                assert "last_updated" in mock_contract
                mock_save.assert_called_once()

    def test_add_task_to_contract_no_existing_tasks(self):
        """Test add_task_to_contract creates tasks list if missing."""
        manager = ContractManager()
        
        mock_contract = {
            "contract_id": "C1",
            "title": "Test Contract"
        }
        
        new_task = {"task_id": "T1", "title": "New Task"}
        
        with patch.object(manager.storage, 'get_contract', return_value=mock_contract):
            with patch.object(manager.storage, 'save_contract', return_value=True):
                result = manager.add_task_to_contract("C1", new_task)
                
                assert result is True
                assert "tasks" in mock_contract
                assert len(mock_contract["tasks"]) == 1

    def test_add_task_to_contract_not_found(self):
        """Test add_task_to_contract returns False when contract not found."""
        manager = ContractManager()
        
        with patch.object(manager.storage, 'get_contract', return_value=None):
            result = manager.add_task_to_contract("C1", {"task_id": "T1"})
            
            assert result is False

    def test_add_task_to_contract_exception(self):
        """Test add_task_to_contract handles exceptions."""
        manager = ContractManager()
        
        with patch.object(manager.storage, 'get_contract', side_effect=Exception("Storage error")):
            result = manager.add_task_to_contract("C1", {"task_id": "T1"})
            
            assert result is False

    def test_add_task_to_contract_save_failure(self):
        """Test add_task_to_contract handles save failure."""
        manager = ContractManager()
        
        mock_contract = {
            "contract_id": "C1",
            "tasks": []
        }
        
        with patch.object(manager.storage, 'get_contract', return_value=mock_contract):
            with patch.object(manager.storage, 'save_contract', return_value=False):
                result = manager.add_task_to_contract("C1", {"task_id": "T1"})
                
                assert result is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
