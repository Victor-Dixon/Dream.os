"""
Unit tests for contract_system/storage.py
Target: ≥85% coverage
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
from src.services.contract_system.storage import ContractStorage
from src.services.contract_system.models import Contract, Task, TaskStatus


class TestContractStorage:
    """Tests for ContractStorage class."""

    @pytest.fixture
    def temp_storage(self):
        """Create temporary storage for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = ContractStorage(base_path=tmpdir)
            yield storage

    def test_init_creates_directories(self, temp_storage):
        """Test initialization creates required directories."""
        assert temp_storage.base_path.exists()
        assert temp_storage.contracts_file.exists() or temp_storage.base_path.exists()
        assert temp_storage.agent_contracts_dir.exists()

    def test_save_contract_success(self, temp_storage):
        """Test save_contract successfully saves contract."""
        contract = Contract(
            contract_id="C1",
            title="Test Contract",
            agent_id="Agent-1"
        )
        
        result = temp_storage.save_contract(contract)
        
        assert result is True
        assert temp_storage.contracts_file.exists()

    def test_save_contract_exception(self, temp_storage):
        """Test save_contract handles exceptions."""
        contract = Contract(contract_id="C1")
        
        with patch.object(temp_storage, 'load_all_contracts', side_effect=Exception("Error")):
            result = temp_storage.save_contract(contract)
            assert result is False

    def test_load_contract_found(self, temp_storage):
        """Test load_contract returns contract when found."""
        contract_data = {
            "contract_id": "C1",
            "title": "Test Contract",
            "status": "pending"
        }
        
        with patch.object(temp_storage, 'load_all_contracts', return_value={"C1": contract_data}):
            contract = temp_storage.load_contract("C1")
            
            assert contract is not None
            assert contract.contract_id == "C1"
            assert contract.title == "Test Contract"

    def test_load_contract_not_found(self, temp_storage):
        """Test load_contract returns None when not found."""
        with patch.object(temp_storage, 'load_all_contracts', return_value={}):
            contract = temp_storage.load_contract("C1")
            assert contract is None

    def test_load_contract_exception(self, temp_storage):
        """Test load_contract handles exceptions."""
        with patch.object(temp_storage, 'load_all_contracts', side_effect=Exception("Error")):
            contract = temp_storage.load_contract("C1")
            assert contract is None

    def test_get_contract_alias(self, temp_storage):
        """Test get_contract is alias for load_contract."""
        with patch.object(temp_storage, 'load_contract', return_value=None) as mock_load:
            temp_storage.get_contract("C1")
            mock_load.assert_called_once_with("C1")

    def test_load_all_contracts_file_exists(self, temp_storage):
        """Test load_all_contracts loads from file when exists."""
        test_data = {"C1": {"contract_id": "C1", "title": "Test"}}
        
        with patch.object(temp_storage.contracts_file, 'exists', return_value=True):
            with patch.object(temp_storage, '_read_json', return_value=test_data):
                result = temp_storage.load_all_contracts()
                assert result == test_data

    def test_load_all_contracts_file_not_exists(self, temp_storage):
        """Test load_all_contracts returns empty dict when file doesn't exist."""
        with patch.object(temp_storage.contracts_file, 'exists', return_value=False):
            result = temp_storage.load_all_contracts()
            assert result == {}

    def test_load_all_contracts_exception(self, temp_storage):
        """Test load_all_contracts handles exceptions."""
        with patch.object(temp_storage.contracts_file, 'exists', return_value=True):
            with patch.object(temp_storage, '_read_json', side_effect=Exception("Error")):
                result = temp_storage.load_all_contracts()
                assert result == {}

    def test_get_all_contracts_success(self, temp_storage):
        """Test get_all_contracts returns list of contracts."""
        test_data = {
            "C1": {"contract_id": "C1", "title": "Test 1"},
            "C2": {"contract_id": "C2", "title": "Test 2"}
        }
        
        with patch.object(temp_storage, 'load_all_contracts', return_value=test_data):
            result = temp_storage.get_all_contracts()
            
            assert isinstance(result, list)
            assert len(result) == 2

    def test_get_all_contracts_exception(self, temp_storage):
        """Test get_all_contracts handles exceptions."""
        with patch.object(temp_storage, 'load_all_contracts', side_effect=Exception("Error")):
            result = temp_storage.get_all_contracts()
            assert result == []

    def test_load_agent_contracts_file_exists(self, temp_storage):
        """Test load_agent_contracts loads from file when exists."""
        test_data = {"C1": {"contract_id": "C1", "agent_id": "Agent-1"}}
        agent_file = temp_storage.agent_contracts_dir / "Agent-1_contracts.json"
        
        with patch.object(agent_file, 'exists', return_value=True):
            with patch.object(temp_storage, '_read_json', return_value=test_data):
                result = temp_storage.load_agent_contracts("Agent-1")
                assert result == test_data

    def test_load_agent_contracts_file_not_exists(self, temp_storage):
        """Test load_agent_contracts returns empty dict when file doesn't exist."""
        agent_file = temp_storage.agent_contracts_dir / "Agent-1_contracts.json"
        
        with patch.object(agent_file, 'exists', return_value=False):
            result = temp_storage.load_agent_contracts("Agent-1")
            assert result == {}

    def test_get_agent_contracts_success(self, temp_storage):
        """Test get_agent_contracts returns Contract objects."""
        test_data = {
            "C1": {"contract_id": "C1", "title": "Test 1"},
            "C2": {"contract_id": "C2", "title": "Test 2"}
        }
        
        with patch.object(temp_storage, 'load_agent_contracts', return_value=test_data):
            result = temp_storage.get_agent_contracts("Agent-1")
            
            assert isinstance(result, list)
            assert len(result) == 2
            assert all(isinstance(c, Contract) for c in result)

    def test_get_agent_contracts_exception(self, temp_storage):
        """Test get_agent_contracts handles exceptions."""
        with patch.object(temp_storage, 'load_agent_contracts', side_effect=Exception("Error")):
            result = temp_storage.get_agent_contracts("Agent-1")
            assert result == []

    def test_read_json_success(self, temp_storage):
        """Test _read_json successfully reads JSON file."""
        test_data = {"key": "value"}
        
        with patch('builtins.open', mock_open(read_data=json.dumps(test_data))):
            result = temp_storage._read_json(temp_storage.contracts_file)
            assert result == test_data

    def test_read_json_file_not_found(self, temp_storage):
        """Test _read_json returns empty dict when file not found."""
        with patch('builtins.open', side_effect=FileNotFoundError):
            result = temp_storage._read_json(temp_storage.contracts_file)
            assert result == {}

    def test_read_json_exception(self, temp_storage):
        """Test _read_json handles exceptions."""
        with patch('builtins.open', side_effect=Exception("Error")):
            result = temp_storage._read_json(temp_storage.contracts_file)
            assert result == {}

    def test_write_json_success(self, temp_storage):
        """Test _write_json successfully writes JSON file."""
        test_data = {"key": "value"}
        
        with patch('builtins.open', mock_open()) as mock_file:
            result = temp_storage._write_json(temp_storage.contracts_file, test_data)
            
            assert result is True
            mock_file.assert_called_once()

    def test_write_json_exception(self, temp_storage):
        """Test _write_json handles exceptions."""
        test_data = {"key": "value"}
        
        with patch('builtins.open', side_effect=Exception("Error")):
            result = temp_storage._write_json(temp_storage.contracts_file, test_data)
            assert result is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
