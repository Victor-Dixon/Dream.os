"""
Unit tests for contract_handler.py

Target: ≥85% coverage, 15+ test methods
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.services.handlers.contract_handler import ContractHandler


class TestContractHandler:
    """Test suite for ContractHandler."""

    @pytest.fixture
    def handler(self):
        """Create ContractHandler instance."""
        with patch('src.services.handlers.contract_handler.ContractManager'):
            return ContractHandler()

    def test_handler_initialization(self, handler):
        """Test handler initializes correctly."""
        assert handler is not None

    def test_can_handle_get_next_task(self, handler):
        """Test can_handle detects get_next_task."""
        args = Mock()
        args.get_next_task = True
        args.check_contracts = False
        
        assert handler.can_handle(args) is True

    def test_can_handle_check_contracts(self, handler):
        """Test can_handle detects check_contracts."""
        args = Mock()
        args.get_next_task = False
        args.check_contracts = True
        
        assert handler.can_handle(args) is True

    def test_can_handle_neither(self, handler):
        """Test can_handle returns False for non-contract commands."""
        args = Mock()
        args.get_next_task = False
        args.check_contracts = False
        
        assert handler.can_handle(args) is False

    def test_handle_contracts_calls_handler(self, handler):
        """Test handle method routes to contract handler."""
        args = Mock()
        args.get_next_task = False
        args.check_contracts = True
        handler.handle_contract_commands = Mock(return_value=True)
        
        result = handler.handle(args)
        
        handler.handle_contract_commands.assert_called_once_with(args)
        assert result is True

    def test_get_next_task_missing_agent(self, handler):
        """Test get_next_task requires agent."""
        args = Mock()
        args.get_next_task = True
        args.agent = None
        
        result = handler.handle_contract_commands(args)
        
        assert result is True  # Command handled, but with error logged

    def test_get_next_task_with_agent(self, handler):
        """Test get_next_task with agent specified."""
        args = Mock()
        args.get_next_task = True
        args.agent = "Agent-1"
        handler.manager = Mock()
        handler.manager.get_next_task.return_value = {
            "title": "Test Task",
            "description": "Test",
            "task_type": "test",
            "priority": "HIGH",
            "estimated_duration": "1h",
            "task_id": "test-123"
        }
        
        result = handler.handle_contract_commands(args)
        
        assert result is True
        handler.manager.get_next_task.assert_called_once_with("Agent-1")

    def test_get_next_task_no_available(self, handler):
        """Test get_next_task when no tasks available."""
        args = Mock()
        args.get_next_task = True
        args.agent = "Agent-1"
        handler.manager = Mock()
        handler.manager.get_next_task.return_value = None
        
        result = handler.handle_contract_commands(args)
        
        assert result is True

    def test_check_contracts_displays_status(self, handler):
        """Test check_contracts displays system status."""
        args = Mock()
        args.get_next_task = False
        args.check_contracts = True
        handler.manager = Mock()
        handler.manager.get_system_status.return_value = {
            "total_contracts": 10,
            "active_contracts": 5,
            "completed_contracts": 5,
            "total_tasks": 20,
            "completed_tasks": 15,
            "completion_rate": 75.0,
            "total_points": 1000,
            "completed_points": 750,
            "agent_summaries": {
                "Agent-1": {"completion_rate": 80.0, "completed_points": 100, "total_points": 125}
            }
        }
        
        result = handler.handle_contract_commands(args)
        
        assert result is True
        handler.manager.get_system_status.assert_called_once()

    def test_handle_contracts_exception(self, handler):
        """Test exception handling in contract commands."""
        args = Mock()
        args.get_next_task = True
        args.agent = "Agent-1"
        handler.manager = Mock()
        handler.manager.get_next_task.side_effect = Exception("Test error")
        
        result = handler.handle_contract_commands(args)
        
        assert result is False

    def test_get_next_task_method(self, handler):
        """Test get_next_task method."""
        handler.manager = Mock()
        handler.manager.get_next_task.return_value = {"task": "test"}
        
        result = handler.get_next_task("Agent-1")
        
        assert result == {"task": "test"}
        handler.manager.get_next_task.assert_called_once_with("Agent-1")

