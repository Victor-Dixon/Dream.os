"""
Tests for message_identity_clarification.py

Comprehensive tests for message identity clarification.
Target: ≥85% coverage
"""

import pytest
from src.services.message_identity_clarification import (
    MessageIdentityClarification,
    format_message_with_identity_clarification,
)
from src.core.messaging_models_core import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    SenderType,
)


class TestMessageIdentityClarification:
    """Tests for MessageIdentityClarification."""

    def test_initialization(self):
        """Test initialization."""
        clarifier = MessageIdentityClarification()
        assert clarifier is not None

    def test_format_message_agent_to_agent(self):
        """Test formatting agent-to-agent message."""
        clarifier = MessageIdentityClarification()
        message = UnifiedMessage(
            content="Test message",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.AGENT_TO_AGENT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        result = clarifier.format_message_with_identity_clarification(message, "Agent-2")
        
        assert "ATTENTION Agent-2" in result
        assert "YOU ARE Agent-2" in result
        assert "A2A MESSAGE" in result or "Agent-to-Agent" in result
        assert "Agent-1" in result
        assert "Agent-2" in result
        assert "Test message" in result

    def test_format_message_system_to_agent(self):
        """Test formatting system-to-agent message."""
        clarifier = MessageIdentityClarification()
        message = UnifiedMessage(
            content="System message",
            sender="System",
            recipient="Agent-1",
            message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.SYSTEM,
        )
        
        result = clarifier.format_message_with_identity_clarification(message, "Agent-1")
        
        assert "S2A MESSAGE" in result or "System-to-Agent" in result
        assert "System" in result
        assert "Agent-1" in result
        assert "System message" in result

    def test_format_message_human_to_agent(self):
        """Test formatting human-to-agent message."""
        clarifier = MessageIdentityClarification()
        message = UnifiedMessage(
            content="Human message",
            sender="User",
            recipient="Agent-1",
            message_type=UnifiedMessageType.HUMAN_TO_AGENT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.HUMAN,
        )
        
        result = clarifier.format_message_with_identity_clarification(message, "Agent-1")
        
        assert "H2A MESSAGE" in result or "Human-to-Agent" in result
        assert "User" in result
        assert "Agent-1" in result
        assert "Human message" in result

    def test_format_message_onboarding(self):
        """Test formatting onboarding message."""
        clarifier = MessageIdentityClarification()
        message = UnifiedMessage(
            content="Onboarding message",
            sender="System",
            recipient="Agent-1",
            message_type=UnifiedMessageType.ONBOARDING,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.SYSTEM,
        )
        
        result = clarifier.format_message_with_identity_clarification(message, "Agent-1")
        
        assert "ONBOARDING MESSAGE" in result or "System-to-Agent" in result
        assert "System" in result
        assert "Agent-1" in result
        assert "Onboarding message" in result

    def test_format_message_captain_to_agent(self):
        """Test formatting captain-to-agent message."""
        clarifier = MessageIdentityClarification()
        message = UnifiedMessage(
            content="Captain message",
            sender="Captain Agent-4",
            recipient="Agent-1",
            message_type=UnifiedMessageType.CAPTAIN_TO_AGENT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.CAPTAIN,
        )
        
        result = clarifier.format_message_with_identity_clarification(message, "Agent-1")
        
        assert "C2A MESSAGE" in result or "Captain-to-Agent" in result
        assert "Captain Agent-4" in result or "Captain" in result
        assert "Agent-1" in result
        assert "Captain message" in result

    def test_format_message_broadcast(self):
        """Test formatting broadcast message."""
        clarifier = MessageIdentityClarification()
        message = UnifiedMessage(
            content="Broadcast message",
            sender="System",
            recipient="all",
            message_type=UnifiedMessageType.BROADCAST,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.SYSTEM,
        )
        
        result = clarifier.format_message_with_identity_clarification(message, "Agent-1")
        
        assert "BROADCAST MESSAGE" in result
        assert "System" in result
        assert "All Agents" in result
        assert "Broadcast message" in result

    def test_format_message_urgent_priority(self):
        """Test formatting message with urgent priority."""
        clarifier = MessageIdentityClarification()
        message = UnifiedMessage(
            content="Urgent message",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.AGENT_TO_AGENT,
            priority=UnifiedMessagePriority.URGENT,
            sender_type=SenderType.AGENT,
        )
        
        result = clarifier.format_message_with_identity_clarification(message, "Agent-2")
        
        assert "PRIORITY: URGENT" in result
        assert "Urgent message" in result

    def test_format_message_regular_priority(self):
        """Test formatting message with regular priority."""
        clarifier = MessageIdentityClarification()
        message = UnifiedMessage(
            content="Regular message",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.AGENT_TO_AGENT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        result = clarifier.format_message_with_identity_clarification(message, "Agent-2")
        
        # Should not have priority info for regular
        assert "PRIORITY: URGENT" not in result
        assert "Regular message" in result

    def test_format_message_text_type(self):
        """Test formatting text message type."""
        clarifier = MessageIdentityClarification()
        message = UnifiedMessage(
            content="Text message",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        result = clarifier.format_message_with_identity_clarification(message, "Agent-2")
        
        # Text type doesn't have specific header, should still have identity reminder
        assert "ATTENTION Agent-2" in result
        assert "Text message" in result

    def test_format_message_identity_reminder_always_present(self):
        """Test that identity reminder is always present."""
        clarifier = MessageIdentityClarification()
        message = UnifiedMessage(
            content="Test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        result = clarifier.format_message_with_identity_clarification(message, "Agent-3")
        
        # Should use the recipient parameter, not message.recipient
        assert "ATTENTION Agent-3" in result
        assert "YOU ARE Agent-3" in result


class TestFormatMessageWithIdentityClarification:
    """Tests for convenience function."""

    def test_format_message_function(self):
        """Test format_message_with_identity_clarification function."""
        message = UnifiedMessage(
            content="Test message",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.AGENT_TO_AGENT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        result = format_message_with_identity_clarification(message, "Agent-2")
        
        assert "ATTENTION Agent-2" in result
        assert "Test message" in result

    def test_format_message_function_uses_global_instance(self):
        """Test that function uses global instance."""
        message = UnifiedMessage(
            content="Test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        result1 = format_message_with_identity_clarification(message, "Agent-2")
        result2 = format_message_with_identity_clarification(message, "Agent-2")
        
        # Should produce same result (same instance)
        assert result1 == result2

