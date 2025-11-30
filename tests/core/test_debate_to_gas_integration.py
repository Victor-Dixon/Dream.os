#!/usr/bin/env python3
"""
Unit tests for debate_to_gas_integration.py - Infrastructure Test Coverage

Tests DebateToGasIntegration class and debate decision processing.
Target: ≥85% coverage, comprehensive test methods.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
"""

import pytest
from unittest.mock import Mock, patch, MagicMock, mock_open
from datetime import datetime
import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.debate_to_gas_integration import DebateToGasIntegration, activate_debate_decision


class TestDebateToGasIntegration:
    """Test suite for DebateToGasIntegration class."""

    @pytest.fixture
    def temp_project_root(self, tmp_path):
        """Create temporary project root for testing."""
        return tmp_path

    @pytest.fixture
    def integration(self, temp_project_root):
        """Create DebateToGasIntegration instance with temp root."""
        integrator = DebateToGasIntegration()
        integrator.project_root = temp_project_root
        integrator.proposals_dir = temp_project_root / "swarm_proposals"
        integrator.brain_dir = temp_project_root / "swarm_brain"
        return integrator

    def test_initialization(self, temp_project_root):
        """Test integration initialization."""
        integrator = DebateToGasIntegration()
        integrator.project_root = temp_project_root
        
        assert integrator.project_root == temp_project_root
        assert integrator.proposals_dir is not None
        assert integrator.brain_dir is not None

    def test_store_in_swarm_brain(self, integration, temp_project_root):
        """Test storing decision in swarm brain."""
        topic = "test_topic"
        decision = "Test decision"
        execution_plan = {"step1": "Do something"}
        
        integration._store_in_swarm_brain(topic, decision, execution_plan)
        
        decisions_file = temp_project_root / "swarm_brain" / "decisions" / f"{topic}_decision.json"
        assert decisions_file.exists()
        
        data = json.loads(decisions_file.read_text())
        assert data["topic"] == topic
        assert data["decision"] == decision
        assert data["execution_plan"] == execution_plan
        assert data["status"] == "activated"

    def test_generate_activation_messages(self, integration):
        """Test generating activation messages for agents."""
        topic = "test_topic"
        decision = "Test decision"
        execution_plan = {"step1": "Do something"}
        agent_assignments = {
            "Agent-1": "Task 1",
            "Agent-2": "Task 2"
        }
        
        messages = integration._generate_activation_messages(
            topic, decision, execution_plan, agent_assignments
        )
        
        assert len(messages) == 2
        assert messages[0]["agent_id"] == "Agent-1"
        assert messages[0]["priority"] == "urgent"
        assert "DEBATE DECISION → ACTION!" in messages[0]["message"]
        assert "Task 1" in messages[0]["message"]

    def test_deliver_via_gasline_success(self, integration):
        """Test delivering messages via gasline successfully."""
        messages = [
            {"agent_id": "Agent-1", "message": "Test message", "priority": "urgent"}
        ]
        
        # Mock the import inside the method
        with patch('src.core.debate_to_gas_integration.logger') as mock_logger:
            # Create a mock module with send_message_to_agent
            mock_module = MagicMock()
            mock_module.send_message_to_agent = MagicMock(return_value=True)
            
            with patch('builtins.__import__', side_effect=lambda name, *args, **kwargs: mock_module if name == 'src.services.messaging_cli_handlers' else __import__(name, *args, **kwargs)):
                integration._deliver_via_gasline(messages)
                
                # Should have called send_message_to_agent
                assert mock_module.send_message_to_agent.called
                mock_logger.info.assert_called()

    def test_deliver_via_gasline_import_error_fallback(self, integration, temp_project_root):
        """Test delivering messages falls back to inbox on import error."""
        messages = [
            {"agent_id": "Agent-1", "message": "Test message", "priority": "urgent"}
        ]
        
        # Mock ImportError when trying to import messaging_cli_handlers
        original_import = __import__
        def mock_import(name, *args, **kwargs):
            if name == 'src.services.messaging_cli_handlers':
                raise ImportError("Module not found")
            return original_import(name, *args, **kwargs)
        
        with patch('builtins.__import__', side_effect=mock_import):
            integration._deliver_via_gasline(messages)
            
            # Should create inbox file
            inbox_dir = temp_project_root / "agent_workspaces" / "Agent-1" / "inbox"
            assert inbox_dir.exists()
            files = list(inbox_dir.glob("DEBATE_DECISION_*.md"))
            assert len(files) > 0

    def test_create_execution_tracker(self, integration, temp_project_root):
        """Test creating execution tracker file."""
        topic = "test_topic"
        agent_assignments = {
            "Agent-1": "Task 1",
            "Agent-2": "Task 2"
        }
        
        integration._create_execution_tracker(topic, agent_assignments)
        
        tracker_file = temp_project_root / "workflow_states" / f"{topic}_execution.json"
        assert tracker_file.exists()
        
        data = json.loads(tracker_file.read_text())
        assert data["topic"] == topic
        assert "Agent-1" in data["agents"]
        assert "Agent-2" in data["agents"]
        assert data["agents"]["Agent-1"]["task"] == "Task 1"
        assert data["agents"]["Agent-1"]["status"] == "assigned"

    def test_process_debate_decision_success(self, integration):
        """Test processing debate decision successfully."""
        topic = "test_topic"
        decision = "Test decision"
        execution_plan = {"step1": "Do something"}
        agent_assignments = {"Agent-1": "Task 1"}
        
        with patch.object(integration, '_store_in_swarm_brain') as mock_store, \
             patch.object(integration, '_generate_activation_messages', return_value=[]), \
             patch.object(integration, '_deliver_via_gasline') as mock_deliver, \
             patch.object(integration, '_create_execution_tracker') as mock_tracker:
            
            result = integration.process_debate_decision(
                topic, decision, execution_plan, agent_assignments
            )
            
            assert result is True
            mock_store.assert_called_once()
            mock_deliver.assert_called_once()
            mock_tracker.assert_called_once()

    def test_process_debate_decision_failure(self, integration):
        """Test processing debate decision handles exceptions."""
        topic = "test_topic"
        decision = "Test decision"
        execution_plan = {"step1": "Do something"}
        agent_assignments = {"Agent-1": "Task 1"}
        
        with patch.object(integration, '_store_in_swarm_brain', side_effect=Exception("Error")):
            result = integration.process_debate_decision(
                topic, decision, execution_plan, agent_assignments
            )
            
            assert result is False


class TestActivateDebateDecision:
    """Test suite for activate_debate_decision convenience function."""

    def test_activate_debate_decision_success(self):
        """Test activate_debate_decision function."""
        topic = "test_topic"
        decision = "Test decision"
        execution_plan = {"step1": "Do something"}
        agent_assignments = {"Agent-1": "Task 1"}
        
        with patch('src.core.debate_to_gas_integration.DebateToGasIntegration') as mock_class:
            mock_integrator = MagicMock()
            mock_integrator.process_debate_decision.return_value = True
            mock_class.return_value = mock_integrator
            
            result = activate_debate_decision(
                topic, decision, execution_plan, agent_assignments
            )
            
            assert result is True
            mock_integrator.process_debate_decision.assert_called_once_with(
                topic, decision, execution_plan, agent_assignments
            )
