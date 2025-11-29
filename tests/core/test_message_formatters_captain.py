"""
Test coverage for message_formatters.py - Captain Work
Created: 2025-11-28
Agent: Agent-4 (Captain)
Perpetual Motion Cycle - Batch 14
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.message_formatters import (
    format_message_full,
    format_message_compact,
    format_message_minimal,
    format_message
)
from src.core.messaging_models_core import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
    SenderType,
    RecipientType
)


class TestFormatMessageFull:
    """Test suite for format_message_full function - 10+ tests"""

    def test_format_message_full_basic(self):
        """Test format_message_full with basic message"""
        message = UnifiedMessage(
            content="test message",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT
        )
        result = format_message_full(message)
        assert isinstance(result, str)
        assert "test message" in result

    def test_format_message_full_with_metadata(self):
        """Test format_message_full with metadata"""
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            metadata={"channel": "test_channel", "session": "test_session"}
        )
        result = format_message_full(message)
        assert isinstance(result, str)

    def test_format_message_full_with_tags(self):
        """Test format_message_full with tags"""
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            tags=[UnifiedMessageTag.CAPTAIN]
        )
        result = format_message_full(message)
        assert isinstance(result, str)

    def test_format_message_full_captain_to_agent(self):
        """Test format_message_full with captain to agent"""
        message = UnifiedMessage(
            content="test",
            sender="Captain Agent-4",
            recipient="Agent-1",
            message_type=UnifiedMessageType.CAPTAIN_TO_AGENT,
            sender_type=SenderType.CAPTAIN
        )
        result = format_message_full(message)
        assert isinstance(result, str)

    def test_format_message_full_discord_source(self):
        """Test format_message_full with Discord source"""
        message = UnifiedMessage(
            content="test",
            sender="Discord Commander",
            recipient="Agent-1",
            message_type=UnifiedMessageType.TEXT,
            metadata={"source": "discord"}
        )
        result = format_message_full(message)
        assert isinstance(result, str)

    def test_format_message_full_agent_to_captain(self):
        """Test format_message_full with agent to captain"""
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-4",
            message_type=UnifiedMessageType.AGENT_TO_AGENT,
            recipient_type=RecipientType.CAPTAIN
        )
        result = format_message_full(message)
        assert isinstance(result, str)

    def test_format_message_full_urgent_priority(self):
        """Test format_message_full with urgent priority"""
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.URGENT
        )
        result = format_message_full(message)
        assert isinstance(result, str)

    def test_format_message_full_onboarding_type(self):
        """Test format_message_full with onboarding type"""
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.ONBOARDING,
            tags=[UnifiedMessageTag.ONBOARDING]
        )
        result = format_message_full(message)
        assert isinstance(result, str)

    def test_format_message_full_system_to_agent(self):
        """Test format_message_full with system to agent"""
        message = UnifiedMessage(
            content="test",
            sender="System",
            recipient="Agent-1",
            message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
            sender_type=SenderType.SYSTEM
        )
        result = format_message_full(message)
        assert isinstance(result, str)

    def test_format_message_full_human_to_agent(self):
        """Test format_message_full with human to agent"""
        message = UnifiedMessage(
            content="test",
            sender="Human",
            recipient="Agent-1",
            message_type=UnifiedMessageType.HUMAN_TO_AGENT,
            sender_type=SenderType.HUMAN
        )
        result = format_message_full(message)
        assert isinstance(result, str)


class TestFormatMessageCompact:
    """Test suite for format_message_compact function - 5+ tests"""

    def test_format_message_compact_basic(self):
        """Test format_message_compact with basic message"""
        message = UnifiedMessage(
            content="test message",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT
        )
        result = format_message_compact(message)
        assert isinstance(result, str)
        assert "test message" in result

    def test_format_message_compact_broadcast(self):
        """Test format_message_compact with broadcast type"""
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="ALL_AGENTS",
            message_type=UnifiedMessageType.BROADCAST
        )
        result = format_message_compact(message)
        assert isinstance(result, str)

    def test_format_message_compact_discord_sender(self):
        """Test format_message_compact with Discord sender"""
        message = UnifiedMessage(
            content="test",
            sender="Discord Commander",
            recipient="Agent-1",
            message_type=UnifiedMessageType.TEXT
        )
        result = format_message_compact(message)
        assert isinstance(result, str)

    def test_format_message_compact_agent_to_agent(self):
        """Test format_message_compact with agent to agent"""
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.AGENT_TO_AGENT
        )
        result = format_message_compact(message)
        assert isinstance(result, str)

    def test_format_message_compact_system_to_agent(self):
        """Test format_message_compact with system to agent"""
        message = UnifiedMessage(
            content="test",
            sender="System",
            recipient="Agent-1",
            message_type=UnifiedMessageType.SYSTEM_TO_AGENT
        )
        result = format_message_compact(message)
        assert isinstance(result, str)


class TestFormatMessageMinimal:
    """Test suite for format_message_minimal function - 3+ tests"""

    def test_format_message_minimal_basic(self):
        """Test format_message_minimal with basic message"""
        message = UnifiedMessage(
            content="test message",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT
        )
        result = format_message_minimal(message)
        assert isinstance(result, str)
        assert "test message" in result

    def test_format_message_minimal_short(self):
        """Test format_message_minimal with short message"""
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT
        )
        result = format_message_minimal(message)
        assert isinstance(result, str)

    def test_format_message_minimal_long(self):
        """Test format_message_minimal with long message"""
        long_content = "x" * 500
        message = UnifiedMessage(
            content=long_content,
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT
        )
        result = format_message_minimal(message)
        assert isinstance(result, str)


class TestFormatMessageRouter:
    """Test suite for format_message router function - 5+ tests"""

    def test_format_message_full_template(self):
        """Test format_message with full template"""
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT
        )
        result = format_message(message, template="full")
        assert isinstance(result, str)

    def test_format_message_compact_template(self):
        """Test format_message with compact template"""
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT
        )
        result = format_message(message, template="compact")
        assert isinstance(result, str)

    def test_format_message_minimal_template(self):
        """Test format_message with minimal template"""
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT
        )
        result = format_message(message, template="minimal")
        assert isinstance(result, str)

    def test_format_message_default_template(self):
        """Test format_message with default template"""
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT
        )
        result = format_message(message)
        assert isinstance(result, str)

    def test_format_message_unknown_template(self):
        """Test format_message with unknown template"""
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT
        )
        result = format_message(message, template="unknown")
        # Should default to compact
        assert isinstance(result, str)


class TestFormatterEdgeCases:
    """Test suite for formatter edge cases - 5+ tests"""

    def test_format_message_empty_content(self):
        """Test format_message with empty content"""
        message = UnifiedMessage(
            content="",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT
        )
        result = format_message(message)
        assert isinstance(result, str)

    def test_format_message_very_long_content(self):
        """Test format_message with very long content"""
        long_content = "x" * 10000
        message = UnifiedMessage(
            content=long_content,
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT
        )
        result = format_message(message)
        assert isinstance(result, str)

    def test_format_message_special_characters(self):
        """Test format_message with special characters"""
        message = UnifiedMessage(
            content="Test with special chars: !@#$%^&*()",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT
        )
        result = format_message(message)
        assert isinstance(result, str)

    def test_format_message_multiline_content(self):
        """Test format_message with multiline content"""
        message = UnifiedMessage(
            content="Line 1\nLine 2\nLine 3",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT
        )
        result = format_message(message)
        assert isinstance(result, str)

    def test_format_message_all_message_types(self):
        """Test format_message with all message types"""
        for msg_type in UnifiedMessageType:
            message = UnifiedMessage(
                content="test",
                sender="Agent-1",
                recipient="Agent-2",
                message_type=msg_type
            )
            result = format_message(message)
            assert isinstance(result, str)

