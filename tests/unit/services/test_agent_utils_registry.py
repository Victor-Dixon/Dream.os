"""
Tests for agent_utils_registry.py

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
"""

import pytest
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))

from src.services.utils.agent_utils_registry import AGENTS, list_agents


class TestAgentsRegistry:
    """Test AGENTS registry constant."""

    def test_agents_exists(self):
        """Test AGENTS constant exists."""
        assert AGENTS is not None
        assert isinstance(AGENTS, dict)
        assert len(AGENTS) == 8  # All 8 agents

    def test_agents_has_all_agents(self):
        """Test AGENTS has all 8 agents."""
        expected_agents = [
            "Agent-1", "Agent-2", "Agent-3", "Agent-4",
            "Agent-5", "Agent-6", "Agent-7", "Agent-8"
        ]
        for agent in expected_agents:
            assert agent in AGENTS

    def test_agent_structure(self):
        """Test each agent has required structure."""
        for agent_id, agent_data in AGENTS.items():
            assert isinstance(agent_data, dict)
            assert "description" in agent_data
            assert "coords" in agent_data
            assert "inbox" in agent_data

    def test_agent_description(self):
        """Test agent descriptions are strings."""
        for agent_id, agent_data in AGENTS.items():
            assert isinstance(agent_data["description"], str)
            assert len(agent_data["description"]) > 0

    def test_agent_coords(self):
        """Test agent coordinates structure."""
        for agent_id, agent_data in AGENTS.items():
            coords = agent_data["coords"]
            assert isinstance(coords, dict)
            assert "x" in coords
            assert "y" in coords
            assert isinstance(coords["x"], (int, float))
            assert isinstance(coords["y"], (int, float))

    def test_agent_inbox(self):
        """Test agent inbox paths are strings."""
        for agent_id, agent_data in AGENTS.items():
            inbox = agent_data["inbox"]
            assert isinstance(inbox, str)
            assert len(inbox) > 0
            assert "agent_workspaces" in inbox
            assert agent_id in inbox

    def test_agent_1_structure(self):
        """Test Agent-1 has correct structure."""
        agent1 = AGENTS["Agent-1"]
        assert agent1["description"] == "Integration & Core Systems"
        assert "coords" in agent1
        assert "inbox" in agent1

    def test_agent_4_structure(self):
        """Test Agent-4 (Captain) has correct structure."""
        agent4 = AGENTS["Agent-4"]
        assert "Strategic" in agent4["description"] or "Captain" in agent4["description"]
        assert "coords" in agent4
        assert "inbox" in agent4


class TestListAgents:
    """Test list_agents function."""

    def test_list_agents_returns_list(self):
        """Test list_agents returns a list."""
        agents = list_agents()
        assert isinstance(agents, list)

    def test_list_agents_returns_all_agents(self):
        """Test list_agents returns all 8 agents."""
        agents = list_agents()
        assert len(agents) == 8

    def test_list_agents_sorted(self):
        """Test list_agents returns sorted list."""
        agents = list_agents()
        assert agents == sorted(agents)

    def test_list_agents_contains_all_agent_ids(self):
        """Test list_agents contains all agent IDs."""
        agents = list_agents()
        expected_agents = [
            "Agent-1", "Agent-2", "Agent-3", "Agent-4",
            "Agent-5", "Agent-6", "Agent-7", "Agent-8"
        ]
        for agent in expected_agents:
            assert agent in agents

    def test_list_agents_sorted_order(self):
        """Test list_agents returns agents in sorted order."""
        agents = list_agents()
        # Should be sorted: Agent-1, Agent-2, ..., Agent-8
        assert agents[0] == "Agent-1"
        assert agents[-1] == "Agent-8"

    def test_list_agents_no_duplicates(self):
        """Test list_agents has no duplicates."""
        agents = list_agents()
        assert len(agents) == len(set(agents))

    def test_list_agents_matches_agents_keys(self):
        """Test list_agents matches AGENTS.keys()."""
        agents = list_agents()
        agents_keys = sorted(AGENTS.keys())
        assert agents == agents_keys

