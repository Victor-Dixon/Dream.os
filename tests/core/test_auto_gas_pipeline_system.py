#!/usr/bin/env python3
"""
Unit tests for auto_gas_pipeline_system.py - Infrastructure Test Coverage

Tests AutoGasPipelineSystem, pipeline agents, and automatic gas delivery.
Target: ≥85% coverage, comprehensive test methods.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.auto_gas_pipeline_system import (
    AutoGasPipelineSystem,
    PipelineAgent,
    AgentState
)


class TestAgentState:
    """Test suite for AgentState enum."""

    def test_agent_state_values(self):
        """Test AgentState enum values."""
        assert AgentState.IDLE.value == "idle"
        assert AgentState.STARTING.value == "starting"
        assert AgentState.EXECUTING.value == "executing"
        assert AgentState.COMPLETING.value == "completing"
        assert AgentState.COMPLETE.value == "complete"
        assert AgentState.OUT_OF_GAS.value == "out_of_gas"


class TestPipelineAgent:
    """Test suite for PipelineAgent dataclass."""

    def test_pipeline_agent_creation(self):
        """Test creating a pipeline agent."""
        agent = PipelineAgent(
            agent_id="Agent-1",
            repos_assigned=(1, 10),
            next_agent="Agent-2"
        )
        assert agent.agent_id == "Agent-1"
        assert agent.repos_assigned == (1, 10)
        assert agent.next_agent == "Agent-2"
        assert agent.current_repo == 0
        assert agent.state == AgentState.IDLE

    def test_pipeline_agent_defaults(self):
        """Test pipeline agent default values."""
        agent = PipelineAgent(
            agent_id="Agent-1",
            repos_assigned=(1, 10),
            next_agent=None
        )
        assert agent.last_gas_sent is None
        assert agent.gas_sent_at_75 is False
        assert agent.gas_sent_at_90 is False
        assert agent.gas_sent_at_100 is False


class TestAutoGasPipelineSystemInitialization:
    """Test suite for system initialization."""

    @pytest.fixture
    def system(self, tmp_path):
        """Create system instance with temp workspace."""
        with patch('src.core.auto_gas_pipeline_system.Path', return_value=tmp_path / "agent_workspaces"):
            return AutoGasPipelineSystem()

    def test_initialization(self, system):
        """Test system initialization."""
        assert system is not None
        assert system.workspace_path is not None
        assert system.monitoring_active is False
        assert len(system.agents) > 0

    def test_pipeline_setup(self, system):
        """Test pipeline agent setup."""
        assert "Agent-1" in system.agents
        assert "Agent-2" in system.agents
        assert system.agents["Agent-1"].repos_assigned == (1, 10)
        assert system.agents["Agent-2"].repos_assigned == (11, 20)


class TestStatusReading:
    """Test suite for status reading methods."""

    @pytest.fixture
    def system(self, tmp_path):
        """Create system with temp workspace."""
        workspace = tmp_path / "agent_workspaces"
        workspace.mkdir()
        with patch('src.core.auto_gas_pipeline_system.Path', return_value=workspace):
            system = AutoGasPipelineSystem()
            system.workspace_path = workspace
            return system

    def test_read_agent_status_exists(self, system):
        """Test reading existing status file."""
        agent_dir = system.workspace_path / "Agent-1"
        agent_dir.mkdir()
        status_file = agent_dir / "status.json"
        status_file.write_text(json.dumps({"status": "ACTIVE"}))
        
        status = system._read_agent_status("Agent-1")
        assert status is not None
        assert status["status"] == "ACTIVE"

    def test_read_agent_status_missing(self, system):
        """Test reading missing status file."""
        status = system._read_agent_status("Agent-999")
        assert status is None

    def test_read_agent_status_invalid_json(self, system):
        """Test reading invalid JSON status."""
        agent_dir = system.workspace_path / "Agent-1"
        agent_dir.mkdir()
        status_file = agent_dir / "status.json"
        status_file.write_text("invalid json")
        
        status = system._read_agent_status("Agent-1")
        # Should handle error gracefully
        assert status is None or isinstance(status, dict)


class TestProgressCalculation:
    """Test suite for progress calculation."""

    @pytest.fixture
    def system(self, tmp_path):
        """Create system with temp workspace."""
        workspace = tmp_path / "agent_workspaces"
        workspace.mkdir()
        with patch('src.core.auto_gas_pipeline_system.Path', return_value=workspace):
            system = AutoGasPipelineSystem()
            system.workspace_path = workspace
            return system

    def test_calculate_progress_no_status(self, system):
        """Test progress calculation with no status."""
        progress = system._calculate_progress("Agent-999")
        assert progress == 0.0

    def test_calculate_progress_from_completed_tasks(self, system):
        """Test progress calculation from completed tasks."""
        agent_dir = system.workspace_path / "Agent-1"
        agent_dir.mkdir()
        status_file = agent_dir / "status.json"
        status_file.write_text(json.dumps({
            "completed_tasks": ["Repo #1 complete", "Repo #2 complete"]
        }))
        
        progress = system._calculate_progress("Agent-1")
        assert progress > 0.0

    def test_calculate_progress_zero(self, system):
        """Test progress calculation with no progress."""
        agent_dir = system.workspace_path / "Agent-1"
        agent_dir.mkdir()
        status_file = agent_dir / "status.json"
        status_file.write_text(json.dumps({
            "completed_tasks": [],
            "current_tasks": []
        }))
        
        progress = system._calculate_progress("Agent-1")
        assert progress == 0.0


class TestFSMStateManagement:
    """Test suite for FSM state management."""

    @pytest.fixture
    def system(self, tmp_path):
        """Create system instance."""
        with patch('src.core.auto_gas_pipeline_system.Path', return_value=tmp_path / "agent_workspaces"):
            return AutoGasPipelineSystem()

    def test_update_fsm_state_idle(self, system):
        """Test FSM state update to idle."""
        system._update_fsm_state("Agent-1", 0.0)
        assert system.agents["Agent-1"].state == AgentState.IDLE

    def test_update_fsm_state_starting(self, system):
        """Test FSM state update to starting."""
        system._update_fsm_state("Agent-1", 10.0)
        assert system.agents["Agent-1"].state == AgentState.STARTING

    def test_update_fsm_state_executing(self, system):
        """Test FSM state update to executing."""
        system._update_fsm_state("Agent-1", 50.0)
        assert system.agents["Agent-1"].state == AgentState.EXECUTING

    def test_update_fsm_state_completing(self, system):
        """Test FSM state update to completing."""
        system._update_fsm_state("Agent-1", 96.0)
        assert system.agents["Agent-1"].state == AgentState.COMPLETING

    def test_update_fsm_state_complete(self, system):
        """Test FSM state update to complete."""
        system._update_fsm_state("Agent-1", 100.0)
        assert system.agents["Agent-1"].state == AgentState.COMPLETE


class TestGasDelivery:
    """Test suite for gas delivery methods."""

    @pytest.fixture
    def system(self, tmp_path):
        """Create system instance."""
        with patch('src.core.auto_gas_pipeline_system.Path', return_value=tmp_path / "agent_workspaces"):
            return AutoGasPipelineSystem()

    def test_should_send_gas_75_percent(self, system):
        """Test gas delivery at 75% threshold."""
        reasons = system._should_send_gas("Agent-1", 76.0)
        assert "PRIMARY_HANDOFF_75_PERCENT" in reasons

    def test_should_send_gas_90_percent(self, system):
        """Test gas delivery at 90% threshold."""
        reasons = system._should_send_gas("Agent-1", 92.0)
        assert "SAFETY_BACKUP_90_PERCENT" in reasons

    def test_should_send_gas_100_percent(self, system):
        """Test gas delivery at 100% threshold."""
        reasons = system._should_send_gas("Agent-1", 100.0)
        assert "COMPLETION_100_PERCENT" in reasons

    def test_should_send_gas_already_sent(self, system):
        """Test that gas is not sent again if already sent."""
        system.agents["Agent-1"].gas_sent_at_75 = True
        reasons = system._should_send_gas("Agent-1", 76.0)
        assert "PRIMARY_HANDOFF_75_PERCENT" not in reasons

    def test_should_send_gas_no_reasons(self, system):
        """Test when no gas should be sent."""
        reasons = system._should_send_gas("Agent-1", 50.0)
        assert len(reasons) == 0

    def test_send_auto_gas_no_next_agent(self, system):
        """Test gas delivery when no next agent."""
        # Agent-4 is last in pipeline (next_agent is None)
        system._send_auto_gas("Agent-4", "COMPLETION_100_PERCENT", 100.0)
        # Should not crash

    def test_send_auto_gas_with_next_agent(self, system):
        """Test gas delivery to next agent."""
        with patch('src.core.auto_gas_pipeline_system.send_message_to_agent'):
            system._send_auto_gas("Agent-1", "PRIMARY_HANDOFF_75_PERCENT", 76.0)
            # Should mark gas as sent
            assert system.agents["Agent-1"].gas_sent_at_75 is True

