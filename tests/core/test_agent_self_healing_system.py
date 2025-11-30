#!/usr/bin/env python3
"""
Unit tests for agent_self_healing_system.py - Infrastructure Test Coverage

Tests AgentSelfHealingSystem progressive recovery, terminal cancellation, and healing actions.
Target: ≥85% coverage, comprehensive test methods.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, AsyncMock
import asyncio
import json
import time
import sys
from pathlib import Path
from datetime import datetime, date
from tempfile import TemporaryDirectory

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.agent_self_healing_system import (
    AgentSelfHealingSystem,
    SelfHealingConfig,
    HealingAction,
    TERMINAL_CANCEL_THRESHOLD,
    RESCUE_THRESHOLD,
    HARD_ONBOARD_THRESHOLD,
    get_self_healing_system,
)


class TestSelfHealingConfig:
    """Test suite for SelfHealingConfig dataclass."""

    def test_default_config(self):
        """Test default configuration values."""
        config = SelfHealingConfig()
        assert config.check_interval_seconds == 30
        assert config.stall_threshold_seconds == 120
        assert config.recovery_attempts_max == 3
        assert config.auto_reset_enabled is True
        assert config.force_update_enabled is True
        assert config.clear_stuck_tasks is True
        assert config.healing_history_limit == 100
        assert config.terminal_cancel_enabled is True
        assert config.hard_onboard_enabled is True

    def test_custom_config(self):
        """Test custom configuration values."""
        config = SelfHealingConfig(
            check_interval_seconds=60,
            stall_threshold_seconds=180,
            recovery_attempts_max=5
        )
        assert config.check_interval_seconds == 60
        assert config.stall_threshold_seconds == 180
        assert config.recovery_attempts_max == 5


class TestHealingAction:
    """Test suite for HealingAction dataclass."""

    def test_healing_action_creation(self):
        """Test creating a healing action."""
        action = HealingAction(
            agent_id="Agent-1",
            action_type="rescue",
            timestamp=datetime.now(),
            reason="Agent stalled",
            success=True
        )
        assert action.agent_id == "Agent-1"
        assert action.action_type == "rescue"
        assert action.success is True
        assert action.error is None

    def test_healing_action_with_error(self):
        """Test creating a healing action with error."""
        action = HealingAction(
            agent_id="Agent-1",
            action_type="rescue",
            timestamp=datetime.now(),
            reason="Failed",
            success=False,
            error="Connection error"
        )
        assert action.success is False
        assert action.error == "Connection error"


class TestAgentSelfHealingSystemInitialization:
    """Test suite for system initialization."""

    @pytest.fixture
    def temp_workspace(self, tmp_path):
        """Create temporary workspace directory."""
        workspace = tmp_path / "agent_workspaces"
        workspace.mkdir()
        return workspace

    def test_initialization_default_config(self, temp_workspace):
        """Test initialization with default config."""
        with patch('src.core.agent_self_healing_system.Path', return_value=temp_workspace):
            system = AgentSelfHealingSystem()
            assert system.config is not None
            assert system.workspace_root == temp_workspace
            assert system.healing_history == []
            assert system.recovery_attempts == {}
            assert system.running is False

    def test_initialization_custom_config(self, temp_workspace):
        """Test initialization with custom config."""
        config = SelfHealingConfig(check_interval_seconds=60)
        with patch('src.core.agent_self_healing_system.Path', return_value=temp_workspace):
            system = AgentSelfHealingSystem(config=config)
            assert system.config.check_interval_seconds == 60

    def test_initialization_loads_coordinates(self, temp_workspace):
        """Test that coordinates are loaded on initialization."""
        coord_file = Path("cursor_agent_coords.json")
        with patch.object(AgentSelfHealingSystem, '_load_agent_coordinates') as mock_load:
            with patch('src.core.agent_self_healing_system.Path', return_value=temp_workspace):
                AgentSelfHealingSystem()
                mock_load.assert_called_once()

    def test_initialization_loads_cancellation_tracking(self, temp_workspace):
        """Test that cancellation tracking is loaded on initialization."""
        with patch.object(AgentSelfHealingSystem, '_load_cancellation_tracking') as mock_load:
            with patch('src.core.agent_self_healing_system.Path', return_value=temp_workspace):
                AgentSelfHealingSystem()
                mock_load.assert_called_once()


class TestCancellationTracking:
    """Test suite for terminal cancellation tracking."""

    @pytest.fixture
    def system(self, tmp_path):
        """Create system instance with temp workspace."""
        with patch('src.core.agent_self_healing_system.Path', return_value=tmp_path / "agent_workspaces"):
            system = AgentSelfHealingSystem()
            system.cancellation_tracking_file = tmp_path / "tracking.json"
            system.cancellation_counts = {}
            return system

    def test_record_terminal_cancellation(self, system):
        """Test recording terminal cancellation."""
        count = system._record_terminal_cancellation("Agent-1")
        assert count == 1
        today = date.today().isoformat()
        assert system.cancellation_counts["Agent-1"][today] == 1

    def test_record_multiple_cancellations(self, system):
        """Test recording multiple cancellations."""
        count1 = system._record_terminal_cancellation("Agent-1")
        count2 = system._record_terminal_cancellation("Agent-1")
        count3 = system._record_terminal_cancellation("Agent-1")
        assert count1 == 1
        assert count2 == 2
        assert count3 == 3

    def test_get_cancellation_count_today(self, system):
        """Test getting cancellation count for today."""
        system._record_terminal_cancellation("Agent-1")
        system._record_terminal_cancellation("Agent-1")
        count = system.get_cancellation_count_today("Agent-1")
        assert count == 2

    def test_get_cancellation_count_nonexistent(self, system):
        """Test getting count for agent with no cancellations."""
        count = system.get_cancellation_count_today("Agent-999")
        assert count == 0


class TestSystemStartStop:
    """Test suite for system start/stop operations."""

    @pytest.fixture
    def system(self, tmp_path):
        """Create system instance."""
        with patch('src.core.agent_self_healing_system.Path', return_value=tmp_path / "agent_workspaces"):
            return AgentSelfHealingSystem()

    def test_start_system(self, system):
        """Test starting the system."""
        with patch('asyncio.get_event_loop') as mock_loop:
            mock_task = AsyncMock()
            mock_loop.return_value.create_task.return_value = mock_task
            system.start()
            assert system.running is True
            assert system._monitoring_task is not None

    def test_start_already_running(self, system):
        """Test starting when already running."""
        system.running = True
        with patch('asyncio.get_event_loop'):
            system.start()
            # Should not crash or create duplicate tasks

    def test_stop_system(self, system):
        """Test stopping the system."""
        system.running = True
        system._monitoring_task = AsyncMock()
        system.stop()
        assert system.running is False

    def test_stop_without_task(self, system):
        """Test stopping when no task exists."""
        system.running = True
        system._monitoring_task = None
        system.stop()
        assert system.running is False


class TestStallDetection:
    """Test suite for stall detection methods."""

    @pytest.fixture
    def system(self, tmp_path):
        """Create system instance with temp workspace."""
        workspace = tmp_path / "agent_workspaces"
        workspace.mkdir()
        with patch('src.core.agent_self_healing_system.Path', return_value=workspace):
            system = AgentSelfHealingSystem()
            system.workspace_root = workspace
            return system

    @pytest.mark.asyncio
    async def test_detect_stalled_agents_with_activity_detector(self, system):
        """Test detection using enhanced activity detector."""
        system.activity_detector = Mock()
        system.activity_detector.get_stale_agents = Mock(return_value=[("Agent-1", 300.0)])
        
        stalled = await system._detect_stalled_agents()
        assert len(stalled) == 1
        assert stalled[0] == ("Agent-1", 300.0)

    @pytest.mark.asyncio
    async def test_detect_stalled_agents_fallback(self, system):
        """Test fallback detection using status.json file times."""
        # Create stale status file
        agent_dir = system.workspace_root / "Agent-1"
        agent_dir.mkdir()
        status_file = agent_dir / "status.json"
        status_file.write_text('{"status": "ACTIVE"}')
        
        # Make file old (3 minutes ago)
        old_time = time.time() - 180
        with patch('pathlib.Path.stat') as mock_stat:
            mock_stat.return_value.st_mtime = old_time
            stalled = await system._detect_stalled_agents()
            assert len(stalled) > 0

    @pytest.mark.asyncio
    async def test_detect_stalled_agents_missing_file(self, system):
        """Test detection when status file is missing."""
        stalled = await system._detect_stalled_agents()
        # Should detect agents with missing files
        assert isinstance(stalled, list)


class TestHealingActions:
    """Test suite for healing action methods."""

    @pytest.fixture
    def system(self, tmp_path):
        """Create system instance."""
        workspace = tmp_path / "agent_workspaces"
        workspace.mkdir()
        with patch('src.core.agent_self_healing_system.Path', return_value=workspace):
            system = AgentSelfHealingSystem()
            system.workspace_root = workspace
            return system

    def test_record_healing(self, system):
        """Test recording a healing action."""
        system._record_healing("Agent-1", "rescue", "Test reason", True)
        assert len(system.healing_history) == 1
        assert system.healing_history[0].agent_id == "Agent-1"
        assert system.healing_history[0].action_type == "rescue"
        assert system.healing_history[0].success is True

    def test_record_healing_history_limit(self, system):
        """Test that healing history is limited."""
        system.config.healing_history_limit = 5
        for i in range(10):
            system._record_healing(f"Agent-{i}", "test", "reason", True)
        assert len(system.healing_history) == 5

    @pytest.mark.asyncio
    async def test_clear_stuck_tasks(self, system):
        """Test clearing stuck tasks from status."""
        agent_dir = system.workspace_root / "Agent-1"
        agent_dir.mkdir()
        status_file = agent_dir / "status.json"
        status_file.write_text(json.dumps({
            "current_tasks": ["stuck task"],
            "status": "ACTIVE"
        }))
        
        result = await system._clear_stuck_tasks("Agent-1")
        assert result is True
        
        # Verify tasks cleared
        data = json.loads(status_file.read_text())
        assert data["current_tasks"] == []

    @pytest.mark.asyncio
    async def test_reset_agent_status(self, system):
        """Test resetting agent status."""
        agent_dir = system.workspace_root / "Agent-1"
        agent_dir.mkdir()
        
        result = await system._reset_agent_status("Agent-1")
        assert result is True
        
        status_file = agent_dir / "status.json"
        assert status_file.exists()
        data = json.loads(status_file.read_text())
        assert data["status"] == "ACTIVE_AGENT_MODE"

    @pytest.mark.asyncio
    async def test_check_agent_recovered(self, system):
        """Test checking if agent recovered."""
        agent_dir = system.workspace_root / "Agent-1"
        agent_dir.mkdir()
        status_file = agent_dir / "status.json"
        status_file.write_text('{"status": "ACTIVE"}')
        
        # Make file recent
        with patch('time.time', return_value=time.time()):
            with patch('pathlib.Path.stat') as mock_stat:
                mock_stat.return_value.st_mtime = time.time() - 10  # 10 seconds ago
                recovered = await system._check_agent_recovered("Agent-1")
                assert recovered is True


class TestProgressiveRecovery:
    """Test suite for progressive recovery timeline."""

    @pytest.fixture
    def system(self, tmp_path):
        """Create system instance."""
        workspace = tmp_path / "agent_workspaces"
        workspace.mkdir()
        with patch('src.core.agent_self_healing_system.Path', return_value=workspace):
            system = AgentSelfHealingSystem()
            system.workspace_root = workspace
            return system

    @pytest.mark.asyncio
    async def test_terminal_cancel_threshold(self, system):
        """Test terminal cancellation at 5 minute threshold."""
        system.config.terminal_cancel_enabled = True
        system.pyautogui_available = True
        system.pyautogui = Mock()
        system.agent_coordinates = {"Agent-1": (100, 200)}
        
        with patch.object(system, '_check_agent_recovered', return_value=False):
            with patch.object(system, '_cancel_terminal_operations', return_value=True):
                # Stall duration just over 5 minutes
                await system._heal_stalled_agent("Agent-1", TERMINAL_CANCEL_THRESHOLD + 10)
                # Should attempt terminal cancellation

    @pytest.mark.asyncio
    async def test_rescue_threshold(self, system):
        """Test rescue protocol at 8 minute threshold."""
        with patch.object(system, '_send_rescue_message', return_value=True):
            with patch.object(system, '_clear_stuck_tasks', return_value=True):
                with patch.object(system, '_reset_agent_status', return_value=True):
                    # Stall duration just over 8 minutes
                    await system._heal_stalled_agent("Agent-1", RESCUE_THRESHOLD + 10)
                    # Should attempt rescue actions

    @pytest.mark.asyncio
    async def test_hard_onboard_threshold(self, system):
        """Test hard onboarding at 10 minute threshold."""
        system.config.hard_onboard_enabled = True
        with patch.object(system, '_hard_onboard_agent', return_value=True):
            # Stall duration just over 10 minutes
            await system._heal_stalled_agent("Agent-1", HARD_ONBOARD_THRESHOLD + 10)
            # Should attempt hard onboarding


class TestGlobalFunctions:
    """Test suite for global module functions."""

    def test_get_self_healing_system_singleton(self):
        """Test singleton pattern for global system."""
        import src.core.agent_self_healing_system as mod
        mod._healing_system_instance = None  # Reset
        
        system1 = get_self_healing_system()
        system2 = get_self_healing_system()
        
        assert system1 is system2
        assert isinstance(system1, AgentSelfHealingSystem)

