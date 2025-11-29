"""
Tests for swarm_coordinator.py

Comprehensive tests for OSRS swarm coordination.
Target: ≥85% coverage
"""

import pytest
from unittest.mock import MagicMock, patch, Mock
from datetime import datetime
import sys
from pathlib import Path

# Import directly from file to avoid __init__.py issues
swarm_coordinator_path = Path(__file__).parent.parent.parent / "src" / "integrations" / "osrs" / "swarm_coordinator.py"
spec = __import__('importlib.util', fromlist=['spec_from_file_location']).spec_from_file_location(
    "swarm_coordinator", swarm_coordinator_path
)
swarm_coordinator = __import__('importlib.util', fromlist=['module_from_spec']).module_from_spec(spec)
spec.loader.exec_module(swarm_coordinator)

OSRS_Swarm_Coordinator = swarm_coordinator.OSRS_Swarm_Coordinator
SwarmMessage = swarm_coordinator.SwarmMessage
SwarmActivity = swarm_coordinator.SwarmActivity
create_swarm_coordinator = swarm_coordinator.create_swarm_coordinator


class TestSwarmMessage:
    """Tests for SwarmMessage dataclass."""

    def test_swarm_message_creation(self):
        """Test creating a swarm message."""
        message = SwarmMessage(
            message_id="test-123",
            from_agent="Agent-1",
            to_agent="Agent-2",
            message_type="test",
            content={"key": "value"},
            timestamp=datetime.now(),
            priority="high",
        )
        assert message.message_id == "test-123"
        assert message.from_agent == "Agent-1"
        assert message.to_agent == "Agent-2"
        assert message.message_type == "test"
        assert message.content == {"key": "value"}
        assert message.priority == "high"

    def test_swarm_message_broadcast(self):
        """Test creating broadcast message."""
        message = SwarmMessage(
            message_id="broadcast-1",
            from_agent="Coordinator",
            to_agent=None,
            message_type="broadcast",
            content={"message": "test"},
            timestamp=datetime.now(),
        )
        assert message.to_agent is None
        assert message.priority == "normal"  # Default


class TestSwarmActivity:
    """Tests for SwarmActivity dataclass."""

    def test_swarm_activity_creation(self):
        """Test creating a swarm activity."""
        activity = SwarmActivity(
            activity_id="act-1",
            activity_type="test",
            description="Test activity",
            participating_agents=["Agent-1", "Agent-2"],
            start_time=datetime.now(),
            end_time=None,
            status="planned",
            requirements={"key": "value"},
        )
        assert activity.activity_id == "act-1"
        assert activity.activity_type == "test"
        assert activity.status == "planned"
        assert len(activity.participating_agents) == 2


class TestOSRSSwarmCoordinator:
    """Tests for OSRS_Swarm_Coordinator."""

    def test_initialization(self):
        """Test coordinator initialization."""
        coordinator = OSRS_Swarm_Coordinator()
        assert isinstance(coordinator.agents, dict)
        assert isinstance(coordinator.message_queues, dict)
        assert isinstance(coordinator.coordination_activities, dict)
        assert coordinator.is_running is False
        assert coordinator.logger is not None

    def test_register_agent(self):
        """Test registering an agent."""
        coordinator = OSRS_Swarm_Coordinator()
        agent = MagicMock()
        agent.agent_id = "test-agent"
        agent.role = MagicMock()
        agent.role.value = "test_role"
        
        coordinator.register_agent(agent)
        
        assert "test-agent" in coordinator.agents
        assert "test-agent" in coordinator.message_queues
        assert coordinator.agents["test-agent"] == agent

    def test_send_message_to_specific_agent(self):
        """Test sending message to specific agent."""
        coordinator = OSRS_Swarm_Coordinator()
        coordinator.message_queues["agent-1"] = []
        
        message = SwarmMessage(
            message_id="msg-1",
            from_agent="Coordinator",
            to_agent="agent-1",
            message_type="test",
            content={},
            timestamp=datetime.now(),
        )
        
        coordinator.send_message(message)
        
        assert len(coordinator.message_queues["agent-1"]) == 1
        assert coordinator.message_queues["agent-1"][0] == message

    def test_send_message_broadcast(self):
        """Test broadcasting message to all agents."""
        coordinator = OSRS_Swarm_Coordinator()
        coordinator.message_queues["agent-1"] = []
        coordinator.message_queues["agent-2"] = []
        
        message = SwarmMessage(
            message_id="broadcast-1",
            from_agent="Coordinator",
            to_agent=None,
            message_type="broadcast",
            content={},
            timestamp=datetime.now(),
        )
        
        coordinator.send_message(message)
        
        assert len(coordinator.message_queues["agent-1"]) == 1
        assert len(coordinator.message_queues["agent-2"]) == 1

    def test_send_message_error_handling(self):
        """Test error handling in send_message."""
        coordinator = OSRS_Swarm_Coordinator()
        message = SwarmMessage(
            message_id="msg-1",
            from_agent="Coordinator",
            to_agent="nonexistent",
            message_type="test",
            content={},
            timestamp=datetime.now(),
        )
        
        # Should not raise, just log error
        coordinator.send_message(message)

    def test_execute_coordination_activity(self):
        """Test executing coordination activity."""
        coordinator = OSRS_Swarm_Coordinator()
        agent = MagicMock()
        agent.agent_id = "agent-1"
        coordinator.agents["agent-1"] = agent
        
        activity = SwarmActivity(
            activity_id="act-1",
            activity_type="test",
            description="Test",
            participating_agents=["agent-1"],
            start_time=datetime.now(),
            end_time=None,
            status="active",
            requirements={},
        )
        
        coordinator.execute_coordination_activity(activity)
        
        # Should send message to agent
        assert len(coordinator.message_queues.get("agent-1", [])) > 0

    def test_execute_coordination_activity_error_handling(self):
        """Test error handling in execute_coordination_activity."""
        coordinator = OSRS_Swarm_Coordinator()
        activity = SwarmActivity(
            activity_id="act-1",
            activity_type="test",
            description="Test",
            participating_agents=["nonexistent"],
            start_time=datetime.now(),
            end_time=None,
            status="active",
            requirements={},
        )
        
        # Should not raise, just log error
        coordinator.execute_coordination_activity(activity)

    def test_check_activity_readiness_all_ready(self):
        """Test checking activity readiness when all agents ready."""
        coordinator = OSRS_Swarm_Coordinator()
        from src.integrations.agents.osrs_agent_core import AgentStatus
        
        agent1 = MagicMock()
        agent1.agent_id = "agent-1"
        agent1.status = AgentStatus.ACTIVE
        
        agent2 = MagicMock()
        agent2.agent_id = "agent-2"
        agent2.status = AgentStatus.ACTIVE
        
        coordinator.agents["agent-1"] = agent1
        coordinator.agents["agent-2"] = agent2
        
        activity = SwarmActivity(
            activity_id="act-1",
            activity_type="test",
            description="Test",
            participating_agents=["agent-1", "agent-2"],
            start_time=datetime.now(),
            end_time=None,
            status="planned",
            requirements={},
        )
        
        coordinator.check_activity_readiness(activity)
        
        assert activity.status == "active"

    def test_check_activity_readiness_not_ready(self):
        """Test checking activity readiness when agents not ready."""
        coordinator = OSRS_Swarm_Coordinator()
        from src.integrations.agents.osrs_agent_core import AgentStatus
        
        agent1 = MagicMock()
        agent1.agent_id = "agent-1"
        agent1.status = AgentStatus.INACTIVE
        
        coordinator.agents["agent-1"] = agent1
        
        activity = SwarmActivity(
            activity_id="act-1",
            activity_type="test",
            description="Test",
            participating_agents=["agent-1"],
            start_time=datetime.now(),
            end_time=None,
            status="planned",
            requirements={},
        )
        
        coordinator.check_activity_readiness(activity)
        
        assert activity.status == "planned"

    def test_process_resource_request(self):
        """Test processing resource request."""
        coordinator = OSRS_Swarm_Coordinator()
        from src.integrations.agents.osrs_agent_core import AgentStatus
        
        requesting_agent = MagicMock()
        requesting_agent.agent_id = "agent-1"
        requesting_agent.status = AgentStatus.ACTIVE
        
        supplier_agent = MagicMock()
        supplier_agent.agent_id = "agent-2"
        supplier_agent.status = AgentStatus.ACTIVE
        supplier_agent.game_state = MagicMock()
        supplier_agent.game_state.inventory_items = ["item-1"]
        
        coordinator.agents["agent-1"] = requesting_agent
        coordinator.agents["agent-2"] = supplier_agent
        
        request = {
            "requesting_agent": "agent-1",
            "requested_item": "item-1",
            "priority": "high",
        }
        
        coordinator.process_resource_request(request)
        
        # Should send message to supplier
        assert len(coordinator.message_queues.get("agent-2", [])) > 0

    def test_process_resource_request_error_handling(self):
        """Test error handling in process_resource_request."""
        coordinator = OSRS_Swarm_Coordinator()
        request = {
            "requesting_agent": "nonexistent",
            "requested_item": "item-1",
            "priority": "high",
        }
        
        # Should not raise, just log error
        coordinator.process_resource_request(request)

    @patch('src.integrations.osrs.swarm_coordinator.OSRSStrategicPlanner')
    def test_coordinate_strategic_activities(self, mock_planner):
        """Test coordinating strategic activities."""
        coordinator = OSRS_Swarm_Coordinator()
        activity = SwarmActivity(
            activity_id="act-1",
            activity_type="strategic",
            description="Test",
            participating_agents=[],
            start_time=datetime.now(),
            end_time=None,
            status="planned",
            requirements={},
        )
        mock_planner.plan_strategic_activities.return_value = [activity]
        
        coordinator.coordinate_strategic_activities()
        
        assert "act-1" in coordinator.coordination_activities

    def test_monitor_agent_health_error_state(self):
        """Test monitoring agent health with error state."""
        coordinator = OSRS_Swarm_Coordinator()
        from src.integrations.agents.osrs_agent_core import AgentStatus
        
        agent = MagicMock()
        agent.agent_id = "agent-1"
        agent.status = AgentStatus.ERROR
        
        coordinator.agents["agent-1"] = agent
        
        coordinator.monitor_agent_health()
        
        # Should attempt restart
        agent.shutdown.assert_not_called()

    def test_monitor_agent_health_shutdown_state(self):
        """Test monitoring agent health with shutdown state."""
        coordinator = OSRS_Swarm_Coordinator()
        from src.integrations.agents.osrs_agent_core import AgentStatus
        
        agent = MagicMock()
        agent.agent_id = "agent-1"
        agent.status = AgentStatus.SHUTDOWN
        
        coordinator.agents["agent-1"] = agent
        
        coordinator.monitor_agent_health()
        
        # Should remove from agents
        assert "agent-1" not in coordinator.agents

    def test_restart_agent(self):
        """Test restarting an agent."""
        coordinator = OSRS_Swarm_Coordinator()
        
        # Should not raise, just log
        coordinator.restart_agent("agent-1")

    def test_update_coordination_status(self):
        """Test updating coordination status."""
        coordinator = OSRS_Swarm_Coordinator()
        agent = MagicMock()
        agent.agent_id = "agent-1"
        agent.role = MagicMock()
        agent.role.value = "test_role"
        agent.status = MagicMock()
        agent.status.value = "active"
        agent.current_activity = "test_activity"
        
        coordinator.agents["agent-1"] = agent
        coordinator.is_running = True
        
        with patch('builtins.open', create=True) as mock_open:
            coordinator.update_coordination_status()
            mock_open.assert_called_once()

    def test_shutdown(self):
        """Test shutting down coordinator."""
        coordinator = OSRS_Swarm_Coordinator()
        agent = MagicMock()
        agent.shutdown = MagicMock()
        coordinator.agents["agent-1"] = agent
        coordinator.is_running = True
        
        with patch.object(coordinator, 'update_coordination_status'):
            coordinator.shutdown()
        
        assert coordinator.is_running is False
        agent.shutdown.assert_called_once()

    def test_start_coordination(self):
        """Test starting coordination."""
        coordinator = OSRS_Swarm_Coordinator()
        agent = MagicMock()
        agent.start_autonomous_operation = MagicMock()
        coordinator.agents["agent-1"] = agent
        
        coordinator.start_coordination()
        
        assert coordinator.is_running is True

    def test_create_swarm_coordinator(self):
        """Test factory function."""
        coordinator = create_swarm_coordinator()
        assert isinstance(coordinator, OSRS_Swarm_Coordinator)

