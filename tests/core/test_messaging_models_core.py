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
    UnifiedMessage
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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

