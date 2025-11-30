"""
Tests for AgentLifecycle - Automated status.json management
"""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, call
from datetime import datetime, timezone
import subprocess

from src.core.agent_lifecycle import (
    AgentLifecycle,
    quick_cycle_start,
    quick_task_complete,
    quick_cycle_end
)


class TestAgentLifecycle:
    """Test suite for AgentLifecycle class."""

    @pytest.fixture
    def temp_workspace(self, tmp_path):
        """Create temporary workspace for testing."""
        workspace = tmp_path / "agent_workspaces" / "TestAgent"
        workspace.mkdir(parents=True)
        return workspace

    @pytest.fixture
    def lifecycle(self, temp_workspace):
        """Create AgentLifecycle instance with temp workspace."""
        with patch('src.core.agent_lifecycle.Path') as mock_path:
            mock_path.return_value = temp_workspace / "status.json"
            mock_path.side_effect = lambda p: Path(
                p) if isinstance(p, str) else p

            lifecycle = AgentLifecycle('TestAgent')
            lifecycle.workspace = temp_workspace
            lifecycle.status_file = temp_workspace / "status.json"
            return lifecycle

    def test_init_creates_default_status(self, lifecycle):
        """Test initialization creates default status."""
        assert lifecycle.agent_id == 'TestAgent'
        assert lifecycle.status['agent_id'] == 'TestAgent'
        assert lifecycle.status['status'] == 'IDLE'
        assert lifecycle.status['cycle_count'] == 0
        assert lifecycle.status['points_earned'] == 0

    def test_init_loads_existing_status(self, temp_workspace):
        """Test initialization loads existing status.json."""
        status_file = temp_workspace / "status.json"
        existing_status = {
            "agent_id": "TestAgent",
            "status": "ACTIVE",
            "cycle_count": 5,
            "points_earned": 100
        }
        status_file.write_text(json.dumps(existing_status))

        lifecycle = AgentLifecycle('TestAgent')
        lifecycle.workspace = temp_workspace
        lifecycle.status_file = status_file
        lifecycle._load_status()

        assert lifecycle.status['cycle_count'] == 5
        assert lifecycle.status['points_earned'] == 100

    def test_start_cycle_updates_status(self, lifecycle):
        """Test start_cycle updates status correctly."""
        initial_count = lifecycle.status.get('cycle_count', 0)
        lifecycle.start_cycle()

        assert lifecycle.status['status'] == 'ACTIVE'
        assert lifecycle.status['fsm_state'] == 'active'
        assert lifecycle.status['cycle_count'] == initial_count + 1
        assert 'last_cycle' in lifecycle.status

    def test_start_mission_updates_status(self, lifecycle):
        """Test start_mission updates status correctly."""
        lifecycle.start_mission("Test Mission", "HIGH")

        assert lifecycle.status['current_mission'] == "Test Mission"
        assert lifecycle.status['mission_priority'] == "HIGH"
        assert lifecycle.status['status'] == 'ACTIVE'
        assert lifecycle.status['current_tasks'] == []
        assert lifecycle.status['blockers'] == []

    def test_update_phase(self, lifecycle):
        """Test update_phase updates current_phase."""
        lifecycle.update_phase("Testing phase")
        assert lifecycle.status['current_phase'] == "Testing phase"

    def test_add_task(self, lifecycle):
        """Test add_task adds task to current_tasks."""
        lifecycle.add_task("Task 1")
        assert "Task 1" in lifecycle.status['current_tasks']

        lifecycle.add_task("Task 2")
        assert len(lifecycle.status['current_tasks']) == 2

    def test_complete_task_removes_from_current(self, lifecycle):
        """Test complete_task removes task from current_tasks."""
        lifecycle.add_task("Task 1")
        lifecycle.complete_task("Task 1", points=10)

        assert "Task 1" not in lifecycle.status['current_tasks']
        assert "Task 1" in lifecycle.status['completed_tasks']
        assert lifecycle.status['points_earned'] == 10

    def test_complete_task_adds_points(self, lifecycle):
        """Test complete_task adds points correctly."""
        lifecycle.complete_task("Task 1", points=50)
        assert lifecycle.status['points_earned'] == 50

        lifecycle.complete_task("Task 2", points=25)
        assert lifecycle.status['points_earned'] == 75

    def test_add_blocker_sets_blocked_status(self, lifecycle):
        """Test add_blocker sets status to BLOCKED."""
        lifecycle.add_blocker("Test blocker")

        assert lifecycle.status['status'] == 'BLOCKED'
        assert lifecycle.status['fsm_state'] == 'blocked'
        assert "Test blocker" in lifecycle.status['blockers']

    def test_clear_blockers_resumes_active(self, lifecycle):
        """Test clear_blockers resumes ACTIVE status."""
        lifecycle.add_blocker("Test blocker")
        lifecycle.clear_blockers()

        assert lifecycle.status['status'] == 'ACTIVE'
        assert lifecycle.status['fsm_state'] == 'active'
        assert lifecycle.status['blockers'] == []

    def test_add_achievement(self, lifecycle):
        """Test add_achievement adds to achievements list."""
        lifecycle.add_achievement("First test")
        assert "First test" in lifecycle.status['achievements']

        lifecycle.add_achievement("Second test")
        assert len(lifecycle.status['achievements']) == 2

    def test_set_next_actions(self, lifecycle):
        """Test set_next_actions updates next_actions."""
        actions = ["Action 1", "Action 2", "Action 3"]
        lifecycle.set_next_actions(actions)
        assert lifecycle.status['next_actions'] == actions

    def test_complete_mission(self, lifecycle):
        """Test complete_mission marks mission as complete."""
        lifecycle.start_mission("Test Mission", "HIGH")
        lifecycle.complete_mission()

        assert lifecycle.status['status'] == 'COMPLETE'
        assert lifecycle.status['fsm_state'] == 'complete'
        assert lifecycle.status['current_tasks'] == []

    @patch('subprocess.run')
    def test_end_cycle_with_commit(self, mock_subprocess, lifecycle):
        """Test end_cycle commits to git when commit=True."""
        mock_subprocess.return_value = MagicMock(returncode=0)
        lifecycle.status['cycle_count'] = 1
        lifecycle.end_cycle(commit=True)

        assert mock_subprocess.call_count >= 2  # git add + git commit

    def test_end_cycle_without_commit(self, lifecycle):
        """Test end_cycle without git commit."""
        lifecycle.status['cycle_count'] = 1
        lifecycle.end_cycle(commit=False)

        # Should just update last_updated timestamp
        assert 'last_updated' in lifecycle.status

    def test_get_status_returns_copy(self, lifecycle):
        """Test get_status returns a copy of status."""
        status1 = lifecycle.get_status()
        status1['test'] = 'value'

        status2 = lifecycle.get_status()
        assert 'test' not in status2

    def test_get_cycle_count(self, lifecycle):
        """Test get_cycle_count returns current cycle count."""
        lifecycle.status['cycle_count'] = 5
        assert lifecycle.get_cycle_count() == 5

    def test_get_points(self, lifecycle):
        """Test get_points returns total points."""
        lifecycle.status['points_earned'] = 150
        assert lifecycle.get_points() == 150

    def test_is_blocked(self, lifecycle):
        """Test is_blocked returns correct status."""
        assert not lifecycle.is_blocked()
        lifecycle.add_blocker("Test")
        assert lifecycle.is_blocked()

    def test_get_blockers(self, lifecycle):
        """Test get_blockers returns blockers list."""
        lifecycle.add_blocker("Blocker 1")
        lifecycle.add_blocker("Blocker 2")

        blockers = lifecycle.get_blockers()
        assert len(blockers) == 2
        assert "Blocker 1" in blockers

    @patch('subprocess.run')
    def test_commit_to_git_success(self, mock_subprocess, lifecycle):
        """Test _commit_to_git succeeds."""
        mock_subprocess.return_value = MagicMock(returncode=0)
        lifecycle.status['cycle_count'] = 1

        result = lifecycle._commit_to_git()
        assert result is True

    @patch('subprocess.run')
    def test_commit_to_git_failure(self, mock_subprocess, lifecycle):
        """Test _commit_to_git handles failure."""
        mock_subprocess.side_effect = subprocess.CalledProcessError(1, 'git')
        lifecycle.status['cycle_count'] = 1

        result = lifecycle._commit_to_git()
        assert result is False


class TestConvenienceFunctions:
    """Test suite for convenience functions."""

    @patch('src.core.agent_lifecycle.AgentLifecycle')
    def test_quick_cycle_start(self, mock_lifecycle_class):
        """Test quick_cycle_start helper."""
        mock_instance = MagicMock()
        mock_lifecycle_class.return_value = mock_instance

        result = quick_cycle_start('TestAgent')

        mock_lifecycle_class.assert_called_once_with('TestAgent')
        mock_instance.start_cycle.assert_called_once()
        assert result == mock_instance

    @patch('src.core.agent_lifecycle.AgentLifecycle')
    def test_quick_task_complete(self, mock_lifecycle_class):
        """Test quick_task_complete helper."""
        mock_instance = MagicMock()
        mock_lifecycle_class.return_value = mock_instance

        quick_task_complete('TestAgent', 'Task 1', points=50)

        mock_lifecycle_class.assert_called_once_with('TestAgent')
        mock_instance.complete_task.assert_called_once_with('Task 1', 50)

    @patch('src.core.agent_lifecycle.AgentLifecycle')
    def test_quick_cycle_end(self, mock_lifecycle_class):
        """Test quick_cycle_end helper."""
        mock_instance = MagicMock()
        mock_lifecycle_class.return_value = mock_instance

        quick_cycle_end('TestAgent', commit=True)

        mock_lifecycle_class.assert_called_once_with('TestAgent')
        mock_instance.end_cycle.assert_called_once_with(commit=True)
