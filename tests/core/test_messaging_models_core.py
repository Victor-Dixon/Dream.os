"""
Unit tests for messaging_models_core.py - HIGH PRIORITY

Tests messaging models: UnifiedMessage, DeliveryMethod, UnifiedMessageType, etc.
"""

import pytest
from datetime import datetime
from enum import Enum

# Import messaging models
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.messaging_models_core import (
    DeliveryMethod,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
    UnifiedMessage,
    RecipientType,
    SenderType
)


class TestDeliveryMethod:
    """Test suite for DeliveryMethod enum."""

    def test_delivery_method_values(self):
        """Test delivery method enum values."""
        assert DeliveryMethod.PYAUTOGUI.value == "pyautogui"
        assert DeliveryMethod.INBOX.value == "inbox"

    def test_delivery_method_enum(self):
        """Test delivery method is an enum."""
        assert issubclass(DeliveryMethod, Enum)


class TestUnifiedMessageType:
    """Test suite for UnifiedMessageType enum."""

    def test_message_type_values(self):
        """Test message type enum values."""
        assert UnifiedMessageType.TEXT.value == "text"
        assert UnifiedMessageType.BROADCAST.value == "broadcast"
        assert UnifiedMessageType.ONBOARDING.value == "onboarding"

    def test_message_type_enum(self):
        """Test message type is an enum."""
        assert issubclass(UnifiedMessageType, Enum)


class TestUnifiedMessagePriority:
    """Test suite for UnifiedMessagePriority enum."""

    def test_priority_values(self):
        """Test priority enum values."""
        assert UnifiedMessagePriority.REGULAR.value == "regular"
        assert UnifiedMessagePriority.URGENT.value == "urgent"

    def test_priority_enum(self):
        """Test priority is an enum."""
        assert issubclass(UnifiedMessagePriority, Enum)


class TestUnifiedMessageTag:
    """Test suite for UnifiedMessageTag enum."""

    def test_tag_values(self):
        """Test tag enum values."""
        assert UnifiedMessageTag.CAPTAIN.value == "captain"
        assert UnifiedMessageTag.ONBOARDING.value == "onboarding"
        assert UnifiedMessageTag.WRAPUP.value == "wrapup"

    def test_tag_enum(self):
        """Test tag is an enum."""
        assert issubclass(UnifiedMessageTag, Enum)


class TestUnifiedMessage:
    """Test suite for UnifiedMessage class."""

    def test_message_creation(self):
        """Test creating a unified message."""
        message = UnifiedMessage(
            content="test message",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        assert message.content == "test message"
        assert message.sender == "Agent-1"
        assert message.recipient == "Agent-2"
        assert message.message_type == UnifiedMessageType.TEXT
        assert message.priority == UnifiedMessagePriority.REGULAR

    def test_message_with_tags(self):
        """Test message with tags."""
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            tags=[UnifiedMessageTag.CAPTAIN]
        )
        
        assert UnifiedMessageTag.CAPTAIN in message.tags

    def test_message_serialization(self):
        """Test message serialization."""
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT
        )
        
        # Message should be serializable
        assert hasattr(message, 'content')
        assert hasattr(message, 'sender')
        assert hasattr(message, 'recipient')

    def test_message_priority_handling(self):
        """Test message priority handling."""
        urgent_message = UnifiedMessage(
            content="urgent",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.URGENT
        )
        
        assert urgent_message.priority == UnifiedMessagePriority.URGENT

    def test_message_type_handling(self):
        """Test message type handling."""
        broadcast_message = UnifiedMessage(
            content="broadcast",
            sender="Agent-1",
            recipient="ALL",
            message_type=UnifiedMessageType.BROADCAST
        )
        
        assert broadcast_message.message_type == UnifiedMessageType.BROADCAST

    def test_message_defaults(self):
        """Test message with default values."""
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT
        )
        
        assert message.priority == UnifiedMessagePriority.REGULAR
        assert message.tags == []
        assert message.metadata == {}
        assert message.message_id is not None
        assert message.timestamp is not None
        assert message.sender_type.value == "system"
        assert message.recipient_type.value == "agent"

    def test_message_with_metadata(self):
        """Test message with metadata."""
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            metadata={"key": "value", "number": 123}
        )
        
        assert message.metadata["key"] == "value"
        assert message.metadata["number"] == 123

    def test_message_with_multiple_tags(self):
        """Test message with multiple tags."""
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            tags=[UnifiedMessageTag.CAPTAIN, UnifiedMessageTag.SYSTEM]
        )
        
        assert len(message.tags) == 2
        assert UnifiedMessageTag.CAPTAIN in message.tags
        assert UnifiedMessageTag.SYSTEM in message.tags

    def test_message_unique_id(self):
        """Test each message gets unique ID."""
        msg1 = UnifiedMessage(
            content="test1",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT
        )
        msg2 = UnifiedMessage(
            content="test2",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT
        )
        
        assert msg1.message_id != msg2.message_id

    def test_message_timestamp(self):
        """Test message timestamp is set."""
        from datetime import datetime
        before = datetime.now()
        
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT
        )
        
        after = datetime.now()
        assert before <= message.timestamp <= after

    def test_all_message_types(self):
        """Test all message type enum values."""
        assert UnifiedMessageType.TEXT.value == "text"
        assert UnifiedMessageType.BROADCAST.value == "broadcast"
        assert UnifiedMessageType.ONBOARDING.value == "onboarding"
        assert UnifiedMessageType.AGENT_TO_AGENT.value == "agent_to_agent"
        assert UnifiedMessageType.CAPTAIN_TO_AGENT.value == "captain_to_agent"
        assert UnifiedMessageType.SYSTEM_TO_AGENT.value == "system_to_agent"
        assert UnifiedMessageType.HUMAN_TO_AGENT.value == "human_to_agent"
        assert UnifiedMessageType.MULTI_AGENT_REQUEST.value == "multi_agent_request"

    def test_all_priority_values(self):
        """Test all priority enum values."""
        assert UnifiedMessagePriority.REGULAR.value == "regular"
        assert UnifiedMessagePriority.URGENT.value == "urgent"

    def test_all_tag_values(self):
        """Test all tag enum values."""
        assert UnifiedMessageTag.CAPTAIN.value == "captain"
        assert UnifiedMessageTag.ONBOARDING.value == "onboarding"
        assert UnifiedMessageTag.WRAPUP.value == "wrapup"
        assert UnifiedMessageTag.COORDINATION.value == "coordination"
        assert UnifiedMessageTag.SYSTEM.value == "system"

    def test_recipient_type_enum(self):
        """Test RecipientType enum."""
        from src.core.messaging_models_core import RecipientType
        
        assert RecipientType.AGENT.value == "agent"
        assert RecipientType.CAPTAIN.value == "captain"
        assert RecipientType.SYSTEM.value == "system"
        assert RecipientType.HUMAN.value == "human"
        assert issubclass(RecipientType, Enum)

    def test_sender_type_enum(self):
        """Test SenderType enum."""
        from src.core.messaging_models_core import SenderType
        
        assert SenderType.AGENT.value == "agent"
        assert SenderType.CAPTAIN.value == "captain"
        assert SenderType.SYSTEM.value == "system"
        assert SenderType.HUMAN.value == "human"
        assert issubclass(SenderType, Enum)

    def test_delivery_method_broadcast(self):
        """Test DeliveryMethod.BROADCAST."""
        assert DeliveryMethod.BROADCAST.value == "broadcast"

    def test_message_with_custom_sender_type(self):
        """Test message with custom sender_type."""
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            sender_type=RecipientType.AGENT
        )
        
        assert message.sender_type.value == "agent"

    def test_message_with_custom_recipient_type(self):
        """Test message with custom recipient_type."""
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            recipient_type=RecipientType.AGENT
        )
        
        assert message.recipient_type.value == "agent"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

