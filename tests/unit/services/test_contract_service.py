"""
Unit tests for src/services/contract_service.py

Tests contract service functionality including:
- Contract definitions
- Contract storage operations
- Agent status checking
- Contract display
- Contract service operations
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, mock_open

from src.services.contract_service import (
    ContractDefinitions,
    AgentStatusChecker,
    ContractDisplay,
    ContractService,
    IContractStorage
)


class TestContractDefinitions:
    """Test contract definitions."""

    def test_get_contract_definitions(self):
        """Test getting contract definitions."""
        definitions = ContractDefinitions.get_contract_definitions()
        
        assert isinstance(definitions, dict)
        assert len(definitions) > 0
        
        # Verify structure
        for agent_id, contract in definitions.items():
            assert 'name' in contract
            assert 'category' in contract
            assert 'priority' in contract
            assert 'points' in contract
            assert 'description' in contract

    def test_contract_definitions_contains_agents(self):
        """Test that definitions contain expected agents."""
        definitions = ContractDefinitions.get_contract_definitions()
        
        expected_agents = ['Agent-1', 'Agent-2', 'Agent-3', 'Agent-5', 
                         'Agent-6', 'Agent-7', 'Agent-8']
        
        for agent in expected_agents:
            assert agent in definitions, f"{agent} not found in definitions"

    def test_contract_structure(self):
        """Test contract data structure."""
        definitions = ContractDefinitions.get_contract_definitions()
        
        # Check Agent-7 contract structure
        if 'Agent-7' in definitions:
            contract = definitions['Agent-7']
            assert contract['name'] == 'Web Development V2 Compliance Implementation'
            assert contract['category'] == 'Web Development'
            assert contract['priority'] == 'HIGH'
            assert isinstance(contract['points'], int)
            assert contract['points'] > 0


class TestAgentStatusChecker:
    """Test agent status checker."""

    @pytest.fixture
    def temp_workspace(self):
        """Create temporary workspace structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace_dir = Path(tmpdir) / "agent_workspaces"
            workspace_dir.mkdir()
            
            # Create sample status files
            for agent_id in ['Agent-1', 'Agent-2']:
                agent_dir = workspace_dir / agent_id
                agent_dir.mkdir()
                status_file = agent_dir / "status.json"
                status_file.write_text(json.dumps({
                    'status': 'ACTIVE',
                    'current_mission': 'Test mission'
                }))
            
            yield workspace_dir

    @patch('src.services.contract_service.os.path.exists')
    @patch('src.services.contract_service.logger')
    def test_check_agent_status_with_files(self, mock_logger, mock_exists, temp_workspace):
        """Test checking agent status when files exist."""
        def exists_side_effect(path):
            return str(path).endswith('status.json')
        
        mock_exists.side_effect = exists_side_effect
        
        with patch('builtins.open', mock_open(read_data=json.dumps({
            'status': 'ACTIVE',
            'current_mission': 'Test mission'
        }))):
            checker = AgentStatusChecker()
            checker.check_agent_status()
            
            # Verify logger was called
            assert mock_logger.info.called

    @patch('src.services.contract_service.os.path.exists')
    @patch('src.services.contract_service.logger')
    def test_check_agent_status_no_files(self, mock_logger, mock_exists):
        """Test checking agent status when no files exist."""
        mock_exists.return_value = False
        
        checker = AgentStatusChecker()
        checker.check_agent_status()
        
        # Verify logger was called for missing files
        assert mock_logger.info.called

    @patch('src.services.contract_service.os.path.exists')
    @patch('src.services.contract_service.logger')
    def test_check_agent_status_unreadable_file(self, mock_logger, mock_exists):
        """Test handling unreadable status files."""
        def exists_side_effect(path):
            return str(path).endswith('status.json')
        
        mock_exists.side_effect = exists_side_effect
        
        # Simulate file read error
        with patch('builtins.open', side_effect=IOError("Cannot read file")):
            checker = AgentStatusChecker()
            checker.check_agent_status()
            
            # Should handle error gracefully
            assert mock_logger.info.called


class TestContractDisplay:
    """Test contract display functionality."""

    @pytest.fixture
    def sample_contract(self):
        """Create sample contract data."""
        return {
            'name': 'Test Contract',
            'category': 'Testing',
            'priority': 'HIGH',
            'points': 100,
            'description': 'Test contract description'
        }

    @patch('src.services.contract_service.logger')
    def test_display_contract_assignment(self, mock_logger, sample_contract):
        """Test displaying contract assignment."""
        display = ContractDisplay()
        display.display_contract_assignment('Agent-1', sample_contract)
        
        # Verify logger was called multiple times
        assert mock_logger.info.call_count >= 5
        
        # Verify key information was logged
        log_calls = [str(call) for call in mock_logger.info.call_args_list]
        assert any('Test Contract' in str(call) for call in log_calls)
        assert any('Testing' in str(call) for call in log_calls)
        assert any('HIGH' in str(call) for call in log_calls)


class TestContractService:
    """Test contract service operations."""

    @pytest.fixture
    def mock_storage(self):
        """Create mock storage."""
        storage = MagicMock(spec=IContractStorage)
        storage.save_contract.return_value = True
        storage.load_contract.return_value = {'test': 'data'}
        storage.list_contracts.return_value = {'Agent-1': {'name': 'Test'}}
        return storage

    @pytest.fixture
    def contract_service(self, mock_storage):
        """Create contract service instance."""
        return ContractService(storage=mock_storage)

    @pytest.fixture
    def contract_service_no_storage(self):
        """Create contract service without storage."""
        return ContractService(storage=None)

    def test_service_initialization(self, contract_service):
        """Test service initialization."""
        assert contract_service is not None
        assert contract_service.contract_definitions is not None
        assert contract_service.contracts is not None
        assert contract_service.status_checker is not None
        assert contract_service.display is not None

    def test_get_contract_existing(self, contract_service_no_storage):
        """Test getting existing contract."""
        contract = contract_service_no_storage.get_contract('Agent-7')
        
        assert contract is not None
        assert contract['name'] == 'Web Development V2 Compliance Implementation'

    def test_get_contract_nonexistent(self, contract_service_no_storage):
        """Test getting non-existent contract."""
        contract = contract_service_no_storage.get_contract('Agent-99')
        
        assert contract is None

    @patch.object(ContractDisplay, 'display_contract_assignment')
    def test_display_contract_assignment(self, mock_display, contract_service):
        """Test displaying contract assignment."""
        contract = {'name': 'Test', 'category': 'Test', 'priority': 'HIGH', 
                   'points': 100, 'description': 'Test'}
        
        contract_service.display_contract_assignment('Agent-1', contract)
        
        mock_display.assert_called_once_with('Agent-1', contract)

    @patch.object(AgentStatusChecker, 'check_agent_status')
    def test_check_agent_status(self, mock_check, contract_service):
        """Test checking agent status."""
        contract_service.check_agent_status()
        
        mock_check.assert_called_once()

    def test_save_contract_with_storage(self, contract_service, mock_storage):
        """Test saving contract with storage."""
        contract_data = {'name': 'Test Contract', 'points': 100}
        
        result = contract_service.save_contract('Agent-1', contract_data)
        
        assert result is True
        mock_storage.save_contract.assert_called_once_with('Agent-1', contract_data)

    def test_save_contract_without_storage(self, contract_service_no_storage):
        """Test saving contract without storage."""
        contract_data = {'name': 'Test Contract', 'points': 100}
        
        result = contract_service_no_storage.save_contract('Agent-1', contract_data)
        
        # Should return True even without storage
        assert result is True

    def test_load_contract_with_storage(self, contract_service, mock_storage):
        """Test loading contract with storage."""
        contract = contract_service.load_contract('Agent-1')
        
        assert contract is not None
        mock_storage.load_contract.assert_called_once_with('Agent-1')

    def test_load_contract_without_storage(self, contract_service_no_storage):
        """Test loading contract without storage."""
        contract = contract_service_no_storage.load_contract('Agent-7')
        
        # Should fall back to contract definitions
        assert contract is not None
        assert contract['name'] == 'Web Development V2 Compliance Implementation'

    def test_list_all_contracts_with_storage(self, contract_service, mock_storage):
        """Test listing contracts with storage."""
        contracts = contract_service.list_all_contracts()
        
        assert contracts is not None
        mock_storage.list_contracts.assert_called_once()

    def test_list_all_contracts_without_storage(self, contract_service_no_storage):
        """Test listing contracts without storage."""
        contracts = contract_service_no_storage.list_all_contracts()
        
        # Should return contract definitions
        assert contracts is not None
        assert isinstance(contracts, dict)
        assert len(contracts) > 0

    def test_service_dependency_injection(self):
        """Test dependency injection pattern."""
        custom_storage = MagicMock(spec=IContractStorage)
        service = ContractService(storage=custom_storage)
        
        assert service.storage == custom_storage

    def test_service_without_dependency_injection(self):
        """Test service without dependency injection."""
        service = ContractService(storage=None)
        
        assert service.storage is None
        # Should still work with fallback to contract definitions
        contract = service.get_contract('Agent-7')
        assert contract is not None

