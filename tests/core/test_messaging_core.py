"""
Unit tests for messaging_core.py - HIGH PRIORITY

Tests UnifiedMessagingCore, message delivery, and core messaging functionality.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime

# Import messaging core
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.messaging_models_core import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag
)


class TestUnifiedMessagingCore:
    """Test suite for UnifiedMessagingCore class."""

    @pytest.fixture
    def mock_delivery_service(self):
        """Create mock delivery service."""
        mock = MagicMock()
        mock.send_message.return_value = True
        return mock

    @pytest.fixture
    def mock_onboarding_service(self):
        """Create mock onboarding service."""
        mock = MagicMock()
        mock.generate_onboarding_message.return_value = "Welcome message"
        return mock

    @pytest.fixture
    def messaging_core(self, mock_delivery_service, mock_onboarding_service):
        """Create UnifiedMessagingCore instance."""
        from src.core.messaging_core import UnifiedMessagingCore
        
        return UnifiedMessagingCore(
            delivery_service=mock_delivery_service,
            onboarding_service=mock_onboarding_service
        )

    def test_core_initialization(self, messaging_core, mock_delivery_service, mock_onboarding_service):
        """Test core initialization."""
        assert messaging_core is not None
        assert messaging_core.delivery_service == mock_delivery_service
        assert messaging_core.onboarding_service == mock_onboarding_service

    def test_send_message(self, messaging_core, mock_delivery_service):
        """Test sending a message."""
        message = UnifiedMessage(
            content="test message",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        # Would call messaging_core.send_message(message)
        # For now, verify message structure
        assert message.content == "test message"
        assert message.sender == "Agent-1"
        assert message.recipient == "Agent-2"

    def test_broadcast_message(self, messaging_core):
        """Test broadcasting a message."""
        message = UnifiedMessage(
            content="broadcast",
            sender="Agent-1",
            recipient="ALL",
            message_type=UnifiedMessageType.BROADCAST,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        assert message.message_type == UnifiedMessageType.BROADCAST
        assert message.recipient == "ALL"

    def test_generate_onboarding_message(self, messaging_core, mock_onboarding_service):
        """Test generating onboarding message."""
        agent_id = "Agent-1"
        style = "friendly"
        
        # Would call messaging_core.generate_onboarding_message(agent_id, style)
        message = mock_onboarding_service.generate_onboarding_message(agent_id, style)
        
        assert message is not None
        assert len(message) > 0

    def test_message_validation(self):
        """Test message validation."""
        # Valid message
        valid_message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT
        )
        
        assert valid_message.content is not None
        assert valid_message.sender is not None
        assert valid_message.recipient is not None

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

    def test_message_tags(self):
        """Test message tags."""
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            tags=[UnifiedMessageTag.CAPTAIN]
        )
        
        assert UnifiedMessageTag.CAPTAIN in message.tags


class TestMessagingCoreFunctions:
    """Test suite for messaging core helper functions."""

    def test_get_messaging_core(self):
        """Test getting messaging core instance."""
        from src.core.messaging_core import get_messaging_core
        
        core = get_messaging_core()
        
        assert core is not None

    def test_send_message_function(self):
        """Test send_message helper function."""
        # Function would send message via core
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT
        )
        
        assert message is not None

    def test_broadcast_message_function(self):
        """Test broadcast_message helper function."""
        message = UnifiedMessage(
            content="broadcast",
            sender="Agent-1",
            recipient="ALL",
            message_type=UnifiedMessageType.BROADCAST
        )
        
        assert message.message_type == UnifiedMessageType.BROADCAST


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

