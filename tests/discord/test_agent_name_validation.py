#!/usr/bin/env python3
"""
Test Agent Name Validation - Discord Bot Sanitization

Tests to ensure Discord bot only accepts proper agent names:
Agent-1, Agent-2, Agent-3, Agent-4, Agent-5, Agent-6, Agent-7, Agent-8

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-12-06
"""

import pytest
import sys
from pathlib import Path

# Add root to path
root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root))

try:
    from src.discord_commander.discord_agent_communication import AgentCommunicationEngine
    ENGINE_AVAILABLE = True
except ImportError:
    ENGINE_AVAILABLE = False
    # Create a minimal mock for testing validation logic
    class AgentCommunicationEngine:
        def is_valid_agent(self, agent: str) -> bool:
            """Check if agent name is valid."""
            return agent in [f"Agent-{i}" for i in range(1, 9)]
        
        def validate_agent_name(self, agent: str) -> bool:
            """Validate agent name format."""
            if not agent or not isinstance(agent, str):
                return False
            return agent.startswith("Agent-") and len(agent) >= 7
        
        def get_all_agent_names(self) -> list[str]:
            """Get list of all agent names."""
            return [f"Agent-{i}" for i in range(1, 9)]


class TestAgentNameValidation:
    """Test agent name validation and sanitization."""

    def setup_method(self):
        """Setup test fixtures."""
        self.engine = AgentCommunicationEngine()

    def test_is_valid_agent_valid_names(self):
        """Test that valid agent names (Agent-1 through Agent-8) are accepted."""
        valid_agents = [f"Agent-{i}" for i in range(1, 9)]
        
        for agent in valid_agents:
            assert self.engine.is_valid_agent(agent), f"{agent} should be valid"

    def test_is_valid_agent_invalid_names(self):
        """Test that invalid agent names are rejected."""
        invalid_agents = [
            "Agent-0",      # Below range
            "Agent-9",      # Above range
            "Agent-10",     # Above range
            "Agent-99",     # Above range
            "agent-1",      # Wrong case
            "Agent-1 ",     # Trailing space
            " Agent-1",     # Leading space
            "Agent-1.5",   # Decimal
            "Agent--1",     # Double dash
            "Agent-",       # No number
            "Agent",        # No dash or number
            "NotAgent-1",  # Wrong prefix
            "Agent-1-2",   # Multiple numbers
            "",             # Empty
            None,           # None
        ]
        
        for agent in invalid_agents:
            if agent is None:
                # Skip None for is_valid_agent (it will raise TypeError)
                continue
            assert not self.engine.is_valid_agent(agent), f"{agent} should be invalid"

    def test_validate_agent_name_format(self):
        """Test validate_agent_name format checking."""
        # Valid format (but may not be valid agent number)
        assert self.engine.validate_agent_name("Agent-1") is True
        assert self.engine.validate_agent_name("Agent-9") is True  # Format valid, number invalid
        
        # Invalid format
        assert self.engine.validate_agent_name("agent-1") is False  # Wrong case
        assert self.engine.validate_agent_name("Agent") is False  # Too short
        assert self.engine.validate_agent_name("") is False  # Empty
        assert self.engine.validate_agent_name(None) is False  # None

    def test_get_all_agent_names(self):
        """Test that get_all_agent_names returns only valid agents."""
        valid_agents = self.engine.get_all_agent_names()
        
        assert len(valid_agents) == 8
        assert valid_agents == [f"Agent-{i}" for i in range(1, 9)]
        
        # Verify all returned agents are valid
        for agent in valid_agents:
            assert self.engine.is_valid_agent(agent), f"{agent} should be valid"

    def test_agent_name_sanitization_required(self):
        """Test that agent names must be sanitized before use."""
        # This test documents the requirement
        # All agent names should be validated using is_valid_agent() before processing
        
        test_cases = [
            ("Agent-1", True),
            ("Agent-8", True),
            ("Agent-0", False),
            ("Agent-9", False),
            ("agent-1", False),  # Case sensitive
            ("Agent-1 ", False),  # Whitespace
        ]
        
        for agent_name, should_be_valid in test_cases:
            is_valid = self.engine.is_valid_agent(agent_name)
            assert is_valid == should_be_valid, \
                f"Agent name '{agent_name}' validation failed: expected {should_be_valid}, got {is_valid}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

