"""
Unit tests for workspace_agent_registry.py - Infrastructure Test Coverage Batch 10

Tests AgentRegistry class and workspace management operations.
Target: ≥85% coverage, 5+ test methods.
"""

from src.core.workspace_agent_registry import AgentRegistry
import pytest
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path
import json
import os
import sys

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))


class TestAgentRegistry:
    """Test suite for AgentRegistry class."""

    @pytest.fixture
    def temp_workspace_dir(self, tmp_path):
        """Create temporary workspace directory."""
        workspace_dir = tmp_path / "agent_workspaces"
        return str(workspace_dir)

    @pytest.fixture
    def registry(self, temp_workspace_dir):
        """Create AgentRegistry instance."""
        return AgentRegistry(root=temp_workspace_dir)

    def test_registry_initialization_default(self):
        """Test registry initialization with default root."""
        registry = AgentRegistry()
        assert registry.root == "agent_workspaces"

    def test_registry_initialization_custom_root(self, temp_workspace_dir):
        """Test registry initialization with custom root."""
        registry = AgentRegistry(root=temp_workspace_dir)
        assert registry.root == temp_workspace_dir
        assert os.path.exists(temp_workspace_dir)

    def test_list_agents_empty(self, registry):
        """Test list_agents with empty workspace."""
        agents = registry.list_agents()
        assert agents == []

    def test_list_agents_with_agents(self, registry, tmp_path):
        """Test list_agents with multiple agents."""
        workspace_path = Path(registry.root)
        for i in range(1, 4):
            agent_dir = workspace_path / f"Agent-{i}"
            agent_dir.mkdir(parents=True, exist_ok=True)

        agents = registry.list_agents()
        assert len(agents) == 3
        assert "Agent-1" in agents
        assert "Agent-2" in agents
        assert "Agent-3" in agents

    def test_list_agents_sorted(self, registry, tmp_path):
        """Test that list_agents returns sorted list."""
        workspace_path = Path(registry.root)
        for i in [3, 1, 2]:
            agent_dir = workspace_path / f"Agent-{i}"
            agent_dir.mkdir(parents=True, exist_ok=True)

        agents = registry.list_agents()
        assert agents == ["Agent-1", "Agent-2", "Agent-3"]

    def test_list_agents_filters_non_agent_dirs(self, registry, tmp_path):
        """Test that list_agents filters out non-Agent directories."""
        workspace_path = Path(registry.root)
        workspace_path.mkdir(parents=True, exist_ok=True)

        # Create agent and non-agent directories
        (workspace_path / "Agent-1").mkdir()
        (workspace_path / "other_dir").mkdir()
        (workspace_path / "not_agent").mkdir()

        agents = registry.list_agents()
        assert agents == ["Agent-1"]

    def test_reset_statuses(self, registry):
        """Test reset_statuses creates status files."""
        agents = ["Agent-1", "Agent-2"]
        registry.reset_statuses(agents)

        for agent_id in agents:
            status_path = registry._status_path(agent_id)
            assert os.path.exists(status_path)
            with open(status_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                assert data["state"] == "RESET"
                assert data["updated"] is True

    def test_reset_statuses_creates_directories(self, registry):
        """Test reset_statuses creates agent directories."""
        agents = ["Agent-1"]
        registry.reset_statuses(agents)

        agent_dir = os.path.join(registry.root, "Agent-1")
        assert os.path.isdir(agent_dir)

    def test_clear_onboarding_flags(self, registry):
        """Test clear_onboarding_flags creates onboarding files."""
        agents = ["Agent-1"]
        registry.clear_onboarding_flags(agents)

        onboard_path = registry._onboard_path("Agent-1")
        assert os.path.exists(onboard_path)
        with open(onboard_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            assert data["onboarded"] is False
            assert data["hard_onboarding"] is True

    def test_force_onboard(self, registry):
        """Test force_onboard creates onboarding file."""
        # Ensure directory exists
        os.makedirs(os.path.dirname(
            registry._onboard_path("Agent-1")), exist_ok=True)
        registry.force_onboard("Agent-1", timeout=60)

        onboard_path = registry._onboard_path("Agent-1")
        assert os.path.exists(onboard_path)
        with open(onboard_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            assert data["onboarded"] is True
            assert data["hard_onboarding"] is True
            assert data["timeout"] == 60

    def test_force_onboard_default_timeout(self, registry):
        """Test force_onboard uses default timeout."""
        # Ensure directory exists
        os.makedirs(os.path.dirname(
            registry._onboard_path("Agent-1")), exist_ok=True)
        registry.force_onboard("Agent-1")

        onboard_path = registry._onboard_path("Agent-1")
        with open(onboard_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            assert data["timeout"] == 30

    def test_verify_onboarded_true(self, registry):
        """Test verify_onboarded returns True when onboarded."""
        # Ensure directory exists
        os.makedirs(os.path.dirname(
            registry._onboard_path("Agent-1")), exist_ok=True)
        registry.force_onboard("Agent-1")
        result = registry.verify_onboarded("Agent-1")
        assert result is True

    def test_verify_onboarded_false_no_file(self, registry):
        """Test verify_onboarded returns False when file doesn't exist."""
        result = registry.verify_onboarded("Agent-1")
        assert result is False

    def test_verify_onboarded_false_not_onboarded(self, registry):
        """Test verify_onboarded returns False when not onboarded."""
        registry.clear_onboarding_flags(["Agent-1"])
        result = registry.verify_onboarded("Agent-1")
        assert result is False

    def test_verify_onboarded_handles_invalid_json(self, registry):
        """Test verify_onboarded handles invalid JSON gracefully."""
        onboard_path = registry._onboard_path("Agent-1")
        os.makedirs(os.path.dirname(onboard_path), exist_ok=True)
        with open(onboard_path, 'w', encoding='utf-8') as f:
            f.write("invalid json")

        result = registry.verify_onboarded("Agent-1")
        assert result is False

    def test_synchronize(self, registry):
        """Test synchronize creates sync marker file."""
        registry.synchronize()

        sync_file = os.path.join(registry.root, "_sync.ok")
        assert os.path.exists(sync_file)
        with open(sync_file, 'r', encoding='utf-8') as f:
            assert f.read() == "ok"

    def test_save_last_onboarding_message(self, registry):
        """Test save_last_onboarding_message creates message file."""
        registry.save_last_onboarding_message("Agent-1", "Test message")

        message_path = os.path.join(
            registry.root, "Agent-1", "last_onboarding_message.txt")
        assert os.path.exists(message_path)
        with open(message_path, 'r', encoding='utf-8') as f:
            assert f.read() == "Test message"

    def test_save_last_onboarding_message_creates_directory(self, registry):
        """Test save_last_onboarding_message creates agent directory."""
        registry.save_last_onboarding_message("Agent-1", "Test")

        agent_dir = os.path.join(registry.root, "Agent-1")
        assert os.path.isdir(agent_dir)

    def test_get_onboarding_coords_success(self, registry):
        """Test get_onboarding_coords with successful coordinate loader."""
        with patch('src.core.coordinate_loader.get_coordinate_loader') as mock_get_loader:
            mock_loader = MagicMock()
            mock_loader.get_onboarding_coordinates.return_value = (100, 200)
            mock_get_loader.return_value = mock_loader

            coords = registry.get_onboarding_coords("Agent-1")

            assert coords == (100, 200)
            mock_loader.get_onboarding_coordinates.assert_called_once_with(
                "Agent-1")

    def test_get_onboarding_coords_exception_returns_default(self, registry):
        """Test get_onboarding_coords returns (0, 0) on exception."""
        with patch('src.core.coordinate_loader.get_coordinate_loader', side_effect=Exception("Error")):
            coords = registry.get_onboarding_coords("Agent-1")
            assert coords == (0, 0)

    def test_get_onboarding_coords_import_error(self, registry):
        """Test get_onboarding_coords handles ImportError."""
        with patch('builtins.__import__', side_effect=ImportError("Module not found")):
            coords = registry.get_onboarding_coords("Agent-1")
            assert coords == (0, 0)

    def test_status_path_format(self, registry):
        """Test _status_path returns correct path format."""
        path = registry._status_path("Agent-1")
        # Handle both Windows and Unix path separators
        assert "Agent-1" in path
        assert "status.json" in path
        assert "agent_workspaces" in path or registry.root in path

    def test_onboard_path_format(self, registry):
        """Test _onboard_path returns correct path format."""
        path = registry._onboard_path("Agent-1")
        # Handle both Windows and Unix path separators
        assert "Agent-1" in path
        assert "onboarding.json" in path
        assert "agent_workspaces" in path or registry.root in path


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
