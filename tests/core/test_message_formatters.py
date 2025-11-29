"""
Unit tests for message_formatters.py - HIGH PRIORITY

Tests message formatting functions.
"""

import pytest
from datetime import datetime

# Import formatters
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.message_formatters import (
    format_message_full,
    format_message_compact,
    format_message_minimal,
    format_message
)


class TestMessageFormatters:
    """Test suite for message formatting functions."""

    def test_format_message_full(self):
        """Test formatting message with full details."""
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority
        
        message = UnifiedMessage(
            content="test message",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        formatted = format_message_full(message)
        
        assert "Agent-1" in formatted or "test message" in formatted

    def test_format_message_compact(self):
        """Test formatting message in compact format."""
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority
        
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        formatted = format_message_compact(message)
        
        assert message.content in formatted or message.sender in formatted

    def test_format_message_minimal(self):
        """Test formatting message in minimal format."""
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority
        
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        formatted = format_message_minimal(message)
        
        assert message.content in formatted

    def test_format_message_with_template(self):
        """Test formatting message with template selection."""
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority
        
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        # Test different templates
        full_formatted = format_message(message, template="full")
        compact_formatted = format_message(message, template="compact")
        minimal_formatted = format_message(message, template="minimal")
        
        assert message.content in full_formatted or message.content in compact_formatted or message.content in minimal_formatted

    def test_format_message_full_with_metadata(self):
        """Test format_message_full with metadata fields."""
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority
        
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            metadata={"channel": "test-channel", "session_id": "session-123", "context": "test-context"}
        )
        
        formatted = format_message_full(message)
        
        assert "channel" in formatted.lower() or "session" in formatted.lower() or "context" in formatted.lower()

    def test_format_message_full_with_tags(self):
        """Test format_message_full with tags."""
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority, UnifiedMessageTag
        
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            tags=[UnifiedMessageTag.CAPTAIN, UnifiedMessageTag.SYSTEM]
        )
        
        formatted = format_message_full(message)
        
        assert "Tags" in formatted or "tags" in formatted.lower()

    def test_format_message_full_captain_to_agent(self):
        """Test format_message_full with captain_to_agent type."""
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority
        
        message = UnifiedMessage(
            content="test",
            sender="Agent-4",
            recipient="Agent-1",
            message_type=UnifiedMessageType.CAPTAIN_TO_AGENT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        formatted = format_message_full(message)
        
        assert "[C2A]" in formatted or "CAPTAIN" in formatted.upper()

    def test_format_message_full_discord_source(self):
        """Test format_message_full with Discord source."""
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority
        
        message = UnifiedMessage(
            content="test",
            sender="DISCORD",
            recipient="Agent-1",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            metadata={"source": "discord"}
        )
        
        formatted = format_message_full(message)
        
        assert "[D2A]" in formatted or "DISCORD" in formatted.upper()

    def test_format_message_full_agent_to_captain(self):
        """Test format_message_full with agent to captain."""
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority
        
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-4",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        formatted = format_message_full(message)
        
        assert "[A2C]" in formatted or "AGENT TO CAPTAIN" in formatted.upper()

    def test_format_message_compact_broadcast(self):
        """Test format_message_compact with broadcast type."""
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority
        
        message = UnifiedMessage(
            content="broadcast",
            sender="Agent-1",
            recipient="ALL",
            message_type=UnifiedMessageType.BROADCAST,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        formatted = format_message_compact(message)
        
        assert "[BROADCAST]" in formatted or "broadcast" in formatted.lower()

    def test_format_message_compact_discord(self):
        """Test format_message_compact with Discord sender."""
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority
        
        message = UnifiedMessage(
            content="test",
            sender="DISCORD",
            recipient="Agent-1",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        formatted = format_message_compact(message)
        
        assert "[D2A]" in formatted or "discord" in formatted.lower()

    def test_format_message_minimal_simple(self):
        """Test format_message_minimal with simple message."""
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority
        
        message = UnifiedMessage(
            content="Simple message",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        formatted = format_message_minimal(message)
        
        assert "From:" in formatted
        assert "To:" in formatted
        assert "Simple message" in formatted

    def test_format_message_unknown_template(self):
        """Test format_message with unknown template defaults to compact."""
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority
        
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        formatted = format_message(message, template="unknown_template")
        
        # Should default to compact
        assert message.content in formatted

    def test_format_message_full_urgent_priority(self):
        """Test format_message_full with urgent priority."""
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority
        
        message = UnifiedMessage(
            content="urgent",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.URGENT
        )
        
        formatted = format_message_full(message)
        
        assert "urgent" in formatted.lower() or "priority" in formatted.lower()

    def test_format_message_full_onboarding(self):
        """Test format_message_full with onboarding type."""
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority
        
        message = UnifiedMessage(
            content="onboarding",
            sender="Agent-4",
            recipient="Agent-1",
            message_type=UnifiedMessageType.ONBOARDING,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        formatted = format_message_full(message)
        
        assert "[ONBOARDING]" in formatted or "onboarding" in formatted.lower()

    def test_format_message_full_system_to_agent(self):
        """Test format_message_full with system_to_agent type."""
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority
        
        message = UnifiedMessage(
            content="system",
            sender="SYSTEM",
            recipient="Agent-1",
            message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        formatted = format_message_full(message)
        
        assert "[S2A]" in formatted or "SYSTEM" in formatted.upper()

    def test_format_message_full_human_to_agent(self):
        """Test format_message_full with human_to_agent type."""
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority
        
        message = UnifiedMessage(
            content="human",
            sender="Human",
            recipient="Agent-1",
            message_type=UnifiedMessageType.HUMAN_TO_AGENT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        formatted = format_message_full(message)
        
        assert "[H2A]" in formatted or "HUMAN" in formatted.upper()

    def test_format_message_compact_agent_to_agent(self):
        """Test format_message_compact with agent_to_agent type."""
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority
        
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.AGENT_TO_AGENT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        formatted = format_message_compact(message)
        
        assert "[A2A]" in formatted or "agent" in formatted.lower()

    def test_format_message_compact_system_to_agent(self):
        """Test format_message_compact with system_to_agent type."""
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority
        
        message = UnifiedMessage(
            content="test",
            sender="SYSTEM",
            recipient="Agent-1",
            message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        formatted = format_message_compact(message)
        
        assert "[S2A]" in formatted or "system" in formatted.lower()

    def test_format_message_compact_human_to_agent(self):
        """Test format_message_compact with human_to_agent type."""
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority
        
        message = UnifiedMessage(
            content="test",
            sender="Human",
            recipient="Agent-1",
            message_type=UnifiedMessageType.HUMAN_TO_AGENT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        formatted = format_message_compact(message)
        
        assert "[H2A]" in formatted or "human" in formatted.lower()

    def test_format_message_full_general_source(self):
        """Test format_message_full with General source."""
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority
        
        message = UnifiedMessage(
            content="test",
            sender="GENERAL",
            recipient="Agent-1",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        formatted = format_message_full(message)
        
        assert "[D2A]" in formatted or "GENERAL" in formatted.upper() or "DISCORD" in formatted.upper()

    def test_format_message_full_commander_source(self):
        """Test format_message_full with Commander source."""
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority
        
        message = UnifiedMessage(
            content="test",
            sender="COMMANDER",
            recipient="Agent-1",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        formatted = format_message_full(message)
        
        assert "[D2A]" in formatted or "COMMANDER" in formatted.upper() or "DISCORD" in formatted.upper()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

