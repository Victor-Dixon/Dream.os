"""
Tests for message_identity_clarification.py

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-11-27
"""

import pytest
from unittest.mock import Mock, MagicMock
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))

from src.services.message_identity_clarification import (
    MessageIdentityClarification,
    format_message_with_identity_clarification
)


class TestMessageIdentityClarification:
    """Test MessageIdentityClarification class."""

    def test_init(self):
        """Test MessageIdentityClarification initialization."""
        clarifier = MessageIdentityClarification()
        assert clarifier is not None
        assert hasattr(clarifier, 'format_message_with_identity_clarification')

    def test_format_agent_to_agent_message(self):
        """Test formatting agent-to-agent message."""
        clarifier = MessageIdentityClarification()
        message = Mock()
        message.message_type.value = "agent_to_agent"
        message.sender = "Agent-1"
        message.priority.value = "normal"
        message.content = "Test message content"
        
        result = clarifier.format_message_with_identity_clarification(message, "Agent-2")
        
        assert "ATTENTION Agent-2" in result
        assert "YOU ARE Agent-2" in result
        assert "A2A MESSAGE" in result
        assert "Agent-1" in result
        assert "Agent-2" in result
        assert "Test message content" in result

    def test_format_system_to_agent_message(self):
        """Test formatting system-to-agent message."""
        clarifier = MessageIdentityClarification()
        message = Mock()
        message.message_type.value = "system_to_agent"
        message.sender = "System"
        message.priority.value = "normal"
        message.content = "System message"
        
        result = clarifier.format_message_with_identity_clarification(message, "Agent-3")
        
        assert "ATTENTION Agent-3" in result
        assert "S2A MESSAGE" in result
        assert "System" in result
        assert "System message" in result

    def test_format_human_to_agent_message(self):
        """Test formatting human-to-agent message."""
        clarifier = MessageIdentityClarification()
        message = Mock()
        message.message_type.value = "human_to_agent"
        message.sender = "User"
        message.priority.value = "normal"
        message.content = "User message"
        
        result = clarifier.format_message_with_identity_clarification(message, "Agent-4")
        
        assert "ATTENTION Agent-4" in result
        assert "H2A MESSAGE" in result
        assert "User" in result
        assert "User message" in result

    def test_format_onboarding_message(self):
        """Test formatting onboarding message."""
        clarifier = MessageIdentityClarification()
        message = Mock()
        message.message_type.value = "onboarding"
        message.sender = "System"
        message.priority.value = "normal"
        message.content = "Onboarding content"
        
        result = clarifier.format_message_with_identity_clarification(message, "Agent-5")
        
        assert "ATTENTION Agent-5" in result
        assert "ONBOARDING MESSAGE" in result
        assert "Onboarding content" in result

    def test_format_captain_to_agent_message(self):
        """Test formatting captain-to-agent message."""
        clarifier = MessageIdentityClarification()
        message = Mock()
        message.message_type.value = "captain_to_agent"
        message.sender = "Captain Agent-4"
        message.priority.value = "normal"
        message.content = "Captain's orders"
        
        result = clarifier.format_message_with_identity_clarification(message, "Agent-6")
        
        assert "ATTENTION Agent-6" in result
        assert "C2A MESSAGE" in result
        assert "Captain Agent-4" in result
        assert "Captain's orders" in result

    def test_format_broadcast_message(self):
        """Test formatting broadcast message."""
        clarifier = MessageIdentityClarification()
        message = Mock()
        message.message_type.value = "broadcast"
        message.sender = "System"
        message.priority.value = "normal"
        message.content = "Broadcast to all"
        
        result = clarifier.format_message_with_identity_clarification(message, "Agent-7")
        
        assert "ATTENTION Agent-7" in result
        assert "BROADCAST MESSAGE" in result
        assert "All Agents" in result
        assert "Broadcast to all" in result

    def test_format_urgent_priority(self):
        """Test formatting message with urgent priority."""
        clarifier = MessageIdentityClarification()
        message = Mock()
        message.message_type.value = "agent_to_agent"
        message.sender = "Agent-1"
        message.priority.value = "urgent"
        message.content = "Urgent message"
        
        result = clarifier.format_message_with_identity_clarification(message, "Agent-8")
        
        assert "PRIORITY: URGENT" in result
        assert "Urgent message" in result

    def test_format_normal_priority(self):
        """Test formatting message with normal priority."""
        clarifier = MessageIdentityClarification()
        message = Mock()
        message.message_type.value = "agent_to_agent"
        message.sender = "Agent-1"
        message.priority.value = "normal"
        message.content = "Normal message"
        
        result = clarifier.format_message_with_identity_clarification(message, "Agent-2")
        
        assert "PRIORITY: URGENT" not in result
        assert "Normal message" in result

    def test_format_message_structure(self):
        """Test that formatted message has correct structure."""
        clarifier = MessageIdentityClarification()
        message = Mock()
        message.message_type.value = "agent_to_agent"
        message.sender = "Agent-1"
        message.priority.value = "normal"
        message.content = "Content"
        
        result = clarifier.format_message_with_identity_clarification(message, "Agent-2")
        
        # Should contain all required sections
        assert "ATTENTION" in result
        assert "A2A MESSAGE" in result
        assert "FROM:" in result
        assert "TO:" in result
        assert "Content" in result


class TestFormatMessageFunction:
    """Test format_message_with_identity_clarification function."""

    def test_format_message_function_calls_class(self):
        """Test that global function calls class method."""
        message = Mock()
        message.message_type.value = "agent_to_agent"
        message.sender = "Agent-1"
        message.priority.value = "normal"
        message.content = "Test"
        
        result = format_message_with_identity_clarification(message, "Agent-2")
        
        assert "ATTENTION Agent-2" in result
        assert "Test" in result

    def test_format_message_function_returns_string(self):
        """Test that function returns a string."""
        message = Mock()
        message.message_type.value = "system_to_agent"
        message.sender = "System"
        message.priority.value = "normal"
        message.content = "Test"
        
        result = format_message_with_identity_clarification(message, "Agent-3")
        
        assert isinstance(result, str)
        assert len(result) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

