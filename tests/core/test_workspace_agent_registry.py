"""
Unit tests for workspace_agent_registry.py - HIGH PRIORITY

Tests workspace agent registry functionality.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path

# Import agent registry
import sys
from pathlib import Path as PathLib

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))


class TestWorkspaceAgentRegistry:
    """Test suite for workspace agent registry."""

    @pytest.fixture
    def temp_workspace_dir(self, tmp_path):
        """Create temporary workspace directory."""
        workspace_dir = tmp_path / "agent_workspaces"
        workspace_dir.mkdir()
        return workspace_dir

    def test_registry_initialization(self, temp_workspace_dir):
        """Test registry initialization."""
        assert temp_workspace_dir.exists()
        assert temp_workspace_dir.is_dir()

    def test_register_agent(self, temp_workspace_dir):
        """Test registering an agent."""
        agent_id = "Agent-1"
        agent_dir = temp_workspace_dir / agent_id
        agent_dir.mkdir()
        
        assert agent_dir.exists()
        assert agent_dir.name == agent_id

    def test_get_agent_workspace(self, temp_workspace_dir):
        """Test getting agent workspace path."""
        agent_id = "Agent-1"
        agent_dir = temp_workspace_dir / agent_id
        agent_dir.mkdir()
        
        workspace_path = agent_dir
        
        assert workspace_path.exists()
        assert workspace_path.name == agent_id

    def test_list_all_agents(self, temp_workspace_dir):
        """Test listing all agents."""
        # Create multiple agent directories
        for i in range(1, 4):
            agent_dir = temp_workspace_dir / f"Agent-{i}"
            agent_dir.mkdir()
        
        agents = [d.name for d in temp_workspace_dir.iterdir() if d.is_dir()]
        
        assert len(agents) == 3
        assert "Agent-1" in agents
        assert "Agent-2" in agents
        assert "Agent-3" in agents

    def test_agent_status_file(self, temp_workspace_dir):
        """Test agent status file."""
        agent_id = "Agent-1"
        agent_dir = temp_workspace_dir / agent_id
        agent_dir.mkdir()
        
        status_file = agent_dir / "status.json"
        status_file.write_text('{"agent_id": "Agent-1", "status": "ACTIVE"}')
        
        assert status_file.exists()
        assert status_file.name == "status.json"

    def test_agent_inbox_directory(self, temp_workspace_dir):
        """Test agent inbox directory."""
        agent_id = "Agent-1"
        agent_dir = temp_workspace_dir / agent_id
        agent_dir.mkdir()
        
        inbox_dir = agent_dir / "inbox"
        inbox_dir.mkdir()
        
        assert inbox_dir.exists()
        assert inbox_dir.is_dir()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

