"""
Test coverage for messaging_models_core.py - Captain Work
Created: 2025-11-28
Agent: Agent-4 (Captain)
Perpetual Motion Cycle - Batch 13
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.messaging_models_core import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
    DeliveryMethod,
    RecipientType,
    SenderType
)


class TestUnifiedMessage:
    """Test suite for UnifiedMessage class - 15+ tests"""

    def test_unified_message_initialization(self):
        """Test UnifiedMessage initialization"""
        message = UnifiedMessage(
            content="test message",
            sender="Agent-1",
            recipient="Agent-2"
        )
        assert message.content == "test message"
        assert message.sender == "Agent-1"
        assert message.recipient == "Agent-2"

    def test_unified_message_with_type(self):
        """Test UnifiedMessage with message type"""
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT
        )
        assert message.message_type == UnifiedMessageType.TEXT

    def test_unified_message_with_priority(self):
        """Test UnifiedMessage with priority"""
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            priority=UnifiedMessagePriority.URGENT
        )
        assert message.priority == UnifiedMessagePriority.URGENT

    def test_unified_message_with_tags(self):
        """Test UnifiedMessage with tags"""
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            tags=[UnifiedMessageTag.CAPTAIN]
        )
        assert UnifiedMessageTag.CAPTAIN in message.tags

    def test_unified_message_with_metadata(self):
        """Test UnifiedMessage with metadata"""
        metadata = {"key": "value"}
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            metadata=metadata
        )
        assert message.metadata == metadata

    def test_unified_message_dataclass_fields(self):
        """Test UnifiedMessage dataclass fields"""
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT
        )
        assert hasattr(message, 'content')
        assert hasattr(message, 'sender')
        assert hasattr(message, 'recipient')
        assert hasattr(message, 'message_type')

    def test_unified_message_default_priority(self):
        """Test UnifiedMessage default priority"""
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT
        )
        assert message.priority == UnifiedMessagePriority.REGULAR

    def test_unified_message_default_tags(self):
        """Test UnifiedMessage default tags"""
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT
        )
        assert isinstance(message.tags, list)
        assert len(message.tags) == 0

    def test_unified_message_timestamp(self):
        """Test UnifiedMessage timestamp generation"""
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT
        )
        assert message.timestamp is not None
        assert isinstance(message.timestamp, datetime)

    def test_unified_message_message_id(self):
        """Test UnifiedMessage message ID generation"""
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT
        )
        assert message.message_id is not None
        assert isinstance(message.message_id, str)
        assert len(message.message_id) > 0

    def test_unified_message_broadcast_type(self):
        """Test UnifiedMessage with broadcast type"""
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="ALL_AGENTS",
            message_type=UnifiedMessageType.BROADCAST
        )
        assert message.message_type == UnifiedMessageType.BROADCAST

    def test_unified_message_onboarding_type(self):
        """Test UnifiedMessage with onboarding type"""
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.ONBOARDING
        )
        assert message.message_type == UnifiedMessageType.ONBOARDING

    def test_unified_message_urgent_priority(self):
        """Test UnifiedMessage with urgent priority"""
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.URGENT
        )
        assert message.priority == UnifiedMessagePriority.URGENT

    def test_unified_message_multiple_tags(self):
        """Test UnifiedMessage with multiple tags"""
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            tags=[UnifiedMessageTag.CAPTAIN, UnifiedMessageTag.ONBOARDING]
        )
        assert len(message.tags) == 2

    def test_unified_message_sender_type(self):
        """Test UnifiedMessage sender_type"""
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            sender_type=SenderType.AGENT
        )
        assert message.sender_type == SenderType.AGENT

    def test_unified_message_recipient_type(self):
        """Test UnifiedMessage recipient_type"""
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            recipient_type=RecipientType.AGENT
        )
        assert message.recipient_type == RecipientType.AGENT


class TestMessageEnums:
    """Test suite for Message Enums - 10+ tests"""

    def test_unified_message_type_values(self):
        """Test UnifiedMessageType enum values"""
        assert UnifiedMessageType.TEXT.value == "text"
        assert UnifiedMessageType.BROADCAST.value == "broadcast"
        assert UnifiedMessageType.ONBOARDING.value == "onboarding"
        assert UnifiedMessageType.AGENT_TO_AGENT.value == "agent_to_agent"
        assert UnifiedMessageType.CAPTAIN_TO_AGENT.value == "captain_to_agent"

    def test_unified_message_priority_values(self):
        """Test UnifiedMessagePriority enum values"""
        assert UnifiedMessagePriority.REGULAR.value == "regular"
        assert UnifiedMessagePriority.URGENT.value == "urgent"

    def test_unified_message_tag_values(self):
        """Test UnifiedMessageTag enum values"""
        assert UnifiedMessageTag.CAPTAIN.value == "captain"
        assert UnifiedMessageTag.ONBOARDING.value == "onboarding"
        assert UnifiedMessageTag.WRAPUP.value == "wrapup"
        assert UnifiedMessageTag.COORDINATION.value == "coordination"
        assert UnifiedMessageTag.SYSTEM.value == "system"

    def test_delivery_method_values(self):
        """Test DeliveryMethod enum values"""
        assert DeliveryMethod.PYAUTOGUI.value == "pyautogui"
        assert DeliveryMethod.INBOX.value == "inbox"
        assert DeliveryMethod.BROADCAST.value == "broadcast"

    def test_recipient_type_values(self):
        """Test RecipientType enum values"""
        assert RecipientType.AGENT.value == "agent"
        assert RecipientType.CAPTAIN.value == "captain"
        assert RecipientType.SYSTEM.value == "system"
        assert RecipientType.HUMAN.value == "human"

    def test_sender_type_values(self):
        """Test SenderType enum values"""
        assert SenderType.AGENT.value == "agent"
        assert SenderType.CAPTAIN.value == "captain"
        assert SenderType.SYSTEM.value == "system"
        assert SenderType.HUMAN.value == "human"

    def test_message_type_from_string(self):
        """Test UnifiedMessageType from string"""
        assert UnifiedMessageType("text") == UnifiedMessageType.TEXT
        assert UnifiedMessageType("broadcast") == UnifiedMessageType.BROADCAST

    def test_message_priority_from_string(self):
        """Test UnifiedMessagePriority from string"""
        assert UnifiedMessagePriority("regular") == UnifiedMessagePriority.REGULAR
        assert UnifiedMessagePriority("urgent") == UnifiedMessagePriority.URGENT

    def test_message_tag_from_string(self):
        """Test UnifiedMessageTag from string"""
        assert UnifiedMessageTag("captain") == UnifiedMessageTag.CAPTAIN
        assert UnifiedMessageTag("onboarding") == UnifiedMessageTag.ONBOARDING


class TestMessageEdgeCases:
    """Test suite for message edge cases - 5+ tests"""

    def test_unified_message_empty_content(self):
        """Test UnifiedMessage with empty content"""
        message = UnifiedMessage(
            content="",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT
        )
        assert message.content == ""

    def test_unified_message_long_content(self):
        """Test UnifiedMessage with long content"""
        long_content = "x" * 1000
        message = UnifiedMessage(
            content=long_content,
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT
        )
        assert len(message.content) == 1000

    def test_unified_message_unique_ids(self):
        """Test UnifiedMessage generates unique IDs"""
        message1 = UnifiedMessage(
            content="test1",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT
        )
        message2 = UnifiedMessage(
            content="test2",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT
        )
        assert message1.message_id != message2.message_id

    def test_unified_message_all_message_types(self):
        """Test UnifiedMessage with all message types"""
        for msg_type in UnifiedMessageType:
            message = UnifiedMessage(
                content="test",
                sender="Agent-1",
                recipient="Agent-2",
                message_type=msg_type
            )
            assert message.message_type == msg_type

    def test_unified_message_all_priorities(self):
        """Test UnifiedMessage with all priorities"""
        for priority in UnifiedMessagePriority:
            message = UnifiedMessage(
                content="test",
                sender="Agent-1",
                recipient="Agent-2",
                message_type=UnifiedMessageType.TEXT,
                priority=priority
            )
            assert message.priority == priority

    def test_unified_message_all_tags(self):
        """Test UnifiedMessage with all tags"""
        all_tags = list(UnifiedMessageTag)
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            tags=all_tags
        )
        assert len(message.tags) == len(all_tags)

