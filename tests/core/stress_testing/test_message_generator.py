"""
Unit tests for MessageGenerator

Tests message generation functionality.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-11-28
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.stress_testing.message_generator import MessageGenerator


class TestMessageGenerator:
    """Test suite for MessageGenerator."""

    def test_initialization_default(self):
        """Test default initialization."""
        generator = MessageGenerator()
        
        assert generator.num_agents == 9
        assert len(generator.agents) == 9
        assert generator.agents[0] == "Agent-1"
        assert generator.agents[8] == "Agent-9"

    def test_initialization_custom_agents(self):
        """Test initialization with custom number of agents."""
        generator = MessageGenerator(num_agents=5)
        
        assert generator.num_agents == 5
        assert len(generator.agents) == 5
        assert generator.agents[0] == "Agent-1"
        assert generator.agents[4] == "Agent-5"

    def test_initialization_custom_types(self):
        """Test initialization with custom message types."""
        generator = MessageGenerator(message_types=["direct", "broadcast"])
        
        assert "direct" in generator.message_types
        assert "broadcast" in generator.message_types
        assert len(generator.message_types) == 2

    def test_generate_batch_count(self):
        """Test generating correct number of messages."""
        generator = MessageGenerator()
        
        messages = generator.generate_batch(10)
        
        assert len(messages) == 10

    def test_generate_batch_structure(self):
        """Test message structure."""
        generator = MessageGenerator()
        
        messages = generator.generate_batch(1)
        msg = messages[0]
        
        assert "type" in msg
        assert "sender" in msg
        assert "recipient" in msg
        assert "content" in msg
        assert "priority" in msg
        assert "message_type" in msg
        assert "tags" in msg
        assert "metadata" in msg

    def test_generate_batch_direct_message(self):
        """Test generating direct messages."""
        generator = MessageGenerator(message_types=["direct"])
        
        messages = generator.generate_batch(10)
        
        # All should have valid agents as recipients (not ALL)
        for msg in messages:
            assert msg["recipient"] in generator.agents

    def test_generate_batch_broadcast_message(self):
        """Test generating broadcast messages."""
        generator = MessageGenerator(message_types=["broadcast"])
        
        messages = generator.generate_batch(10)
        
        # All should have ALL as recipient
        for msg in messages:
            assert msg["recipient"] == "ALL"

    def test_map_message_type(self):
        """Test message type mapping."""
        generator = MessageGenerator()
        
        # Check that mapping returns valid message type values
        direct_type = generator._map_message_type("direct")
        broadcast_type = generator._map_message_type("broadcast")
        hard_type = generator._map_message_type("hard_onboard")
        soft_type = generator._map_message_type("soft_onboard")
        
        # Values should be strings (enum value)
        assert isinstance(direct_type, str)
        assert isinstance(broadcast_type, str)
        assert isinstance(hard_type, str)
        assert isinstance(soft_type, str)
        assert hard_type == soft_type  # Both should map to ONBOARDING

    def test_generate_batch_metadata(self):
        """Test message metadata."""
        generator = MessageGenerator()
        
        messages = generator.generate_batch(5)
        
        for i, msg in enumerate(messages):
            assert msg["metadata"]["test"] is True
            assert msg["metadata"]["message_id"] == i + 1
            assert "msg_type" in msg["metadata"]

