"""
Tests for unified_messaging_service.py - UnifiedMessagingService class.

Target: ≥85% coverage, 15+ tests.
"""

import pytest
from unittest.mock import Mock, patch
from src.services.unified_messaging_service import UnifiedMessagingService, MessagingService


class TestUnifiedMessagingService:
    """Test UnifiedMessagingService class."""

    def test_init(self):
        """Test UnifiedMessagingService initialization."""
        with patch("src.services.unified_messaging_service.ConsolidatedMessagingService") as mock_service:
            service = UnifiedMessagingService()
            assert service.messaging is not None
            mock_service.assert_called_once()

    def test_send_message_success(self):
        """Test successful message sending."""
        service = UnifiedMessagingService()
        service.messaging = Mock()
        service.messaging.send_message = Mock(return_value=True)

        result = service.send_message("Agent-1", "Test message")

        assert result is True
        service.messaging.send_message.assert_called_once_with(
            "Agent-1", "Test message", "regular", True
        )

    def test_send_message_with_priority(self):
        """Test message sending with custom priority."""
        service = UnifiedMessagingService()
        service.messaging = Mock()
        service.messaging.send_message = Mock(return_value=True)

        result = service.send_message("Agent-1", "Test message", priority="urgent")

        assert result is True
        service.messaging.send_message.assert_called_once_with(
            "Agent-1", "Test message", "urgent", True
        )

    def test_send_message_no_pyautogui(self):
        """Test message sending without PyAutoGUI."""
        service = UnifiedMessagingService()
        service.messaging = Mock()
        service.messaging.send_message = Mock(return_value=True)

        result = service.send_message("Agent-1", "Test message", use_pyautogui=False)

        assert result is True
        service.messaging.send_message.assert_called_once_with(
            "Agent-1", "Test message", "regular", False
        )

    def test_send_message_failure(self):
        """Test message sending failure."""
        service = UnifiedMessagingService()
        service.messaging = Mock()
        service.messaging.send_message = Mock(return_value=False)

        result = service.send_message("Agent-1", "Test message")

        assert result is False

    def test_send_message_exception(self):
        """Test message sending with exception."""
        service = UnifiedMessagingService()
        service.messaging = Mock()
        service.messaging.send_message = Mock(side_effect=Exception("Error"))

        with pytest.raises(Exception):
            service.send_message("Agent-1", "Test message")

    def test_broadcast_message_success(self):
        """Test successful broadcast message."""
        service = UnifiedMessagingService()
        service.messaging = Mock()
        service.messaging.broadcast_message = Mock(return_value={"Agent-1": True, "Agent-2": True})

        result = service.broadcast_message("Test broadcast")

        assert result == {"Agent-1": True, "Agent-2": True}
        service.messaging.broadcast_message.assert_called_once_with("Test broadcast", "regular")

    def test_broadcast_message_with_priority(self):
        """Test broadcast message with custom priority."""
        service = UnifiedMessagingService()
        service.messaging = Mock()
        service.messaging.broadcast_message = Mock(return_value={"Agent-1": True})

        result = service.broadcast_message("Test broadcast", priority="urgent")

        assert result == {"Agent-1": True}
        service.messaging.broadcast_message.assert_called_once_with("Test broadcast", "urgent")

    def test_broadcast_message_partial_failure(self):
        """Test broadcast message with partial failures."""
        service = UnifiedMessagingService()
        service.messaging = Mock()
        service.messaging.broadcast_message = Mock(return_value={"Agent-1": True, "Agent-2": False})

        result = service.broadcast_message("Test broadcast")

        assert result == {"Agent-1": True, "Agent-2": False}

    def test_broadcast_message_exception(self):
        """Test broadcast message with exception."""
        service = UnifiedMessagingService()
        service.messaging = Mock()
        service.messaging.broadcast_message = Mock(side_effect=Exception("Error"))

        with pytest.raises(Exception):
            service.broadcast_message("Test broadcast")

    def test_messaging_service_alias(self):
        """Test MessagingService alias."""
        assert MessagingService == UnifiedMessagingService

    def test_send_message_empty_message(self):
        """Test sending empty message."""
        service = UnifiedMessagingService()
        service.messaging = Mock()
        service.messaging.send_message = Mock(return_value=True)

        result = service.send_message("Agent-1", "")

        assert result is True
        service.messaging.send_message.assert_called_once_with("Agent-1", "", "regular", True)

    def test_send_message_none_agent(self):
        """Test sending message with None agent."""
        service = UnifiedMessagingService()
        service.messaging = Mock()
        service.messaging.send_message = Mock(return_value=False)

        result = service.send_message(None, "Test message")

        assert result is False

    def test_broadcast_message_empty(self):
        """Test broadcasting empty message."""
        service = UnifiedMessagingService()
        service.messaging = Mock()
        service.messaging.broadcast_message = Mock(return_value={})

        result = service.broadcast_message("")

        assert result == {}
        service.messaging.broadcast_message.assert_called_once_with("", "regular")

    def test_broadcast_message_all_failures(self):
        """Test broadcast message with all failures."""
        service = UnifiedMessagingService()
        service.messaging = Mock()
        service.messaging.broadcast_message = Mock(return_value={"Agent-1": False, "Agent-2": False})

        result = service.broadcast_message("Test broadcast")

        assert result == {"Agent-1": False, "Agent-2": False}




