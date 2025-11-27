"""
Unit tests for unified_messaging_service.py

Tests UnifiedMessagingService wrapper functionality.
"""

from unittest.mock import Mock, patch

import pytest

from src.services.unified_messaging_service import UnifiedMessagingService


class TestUnifiedMessagingService:
    """Test suite for UnifiedMessagingService."""

    @patch("src.services.unified_messaging_service.ConsolidatedMessagingService")
    def test_init(self, mock_consolidated):
        """Test service initialization."""
        mock_instance = Mock()
        mock_consolidated.return_value = mock_instance

        service = UnifiedMessagingService()

        assert service.messaging is not None
        mock_consolidated.assert_called_once()

    @patch("src.services.unified_messaging_service.ConsolidatedMessagingService")
    def test_send_message_success(self, mock_consolidated):
        """Test successful message sending."""
        # Setup
        mock_instance = Mock()
        mock_instance.send_message.return_value = {"success": True, "message": "Sent"}
        mock_consolidated.return_value = mock_instance

        service = UnifiedMessagingService()

        # Execute
        result = service.send_message("Agent-1", "Test message", "regular", True)

        # Verify - send_message returns the dict, not boolean
        assert result == {"success": True, "message": "Sent"}
        mock_instance.send_message.assert_called_once_with(
            "Agent-1", "Test message", "regular", True
        )

    @patch("src.services.unified_messaging_service.ConsolidatedMessagingService")
    def test_send_message_failure(self, mock_consolidated):
        """Test failed message sending."""
        # Setup
        mock_instance = Mock()
        mock_instance.send_message.return_value = {"success": False, "message": "Failed"}
        mock_consolidated.return_value = mock_instance

        service = UnifiedMessagingService()

        # Execute
        result = service.send_message("Agent-1", "Test message", "regular", True)

        # Verify - send_message returns the dict, not boolean
        assert result == {"success": False, "message": "Failed"}
        mock_instance.send_message.assert_called_once()

    @patch("src.services.unified_messaging_service.ConsolidatedMessagingService")
    def test_broadcast_message_success(self, mock_consolidated):
        """Test successful broadcast message."""
        # Setup
        mock_instance = Mock()
        mock_instance.broadcast_message.return_value = {"success": True, "results": {}}
        mock_consolidated.return_value = mock_instance

        service = UnifiedMessagingService()

        # Execute
        result = service.broadcast_message("Broadcast message", "regular")

        # Verify
        assert result["success"] is True
        mock_instance.broadcast_message.assert_called_once_with("Broadcast message", "regular")

    @patch("src.services.unified_messaging_service.ConsolidatedMessagingService")
    def test_broadcast_message_failure(self, mock_consolidated):
        """Test failed broadcast message."""
        # Setup
        mock_instance = Mock()
        mock_instance.broadcast_message.return_value = {"success": False, "message": "Failed"}
        mock_consolidated.return_value = mock_instance

        service = UnifiedMessagingService()

        # Execute
        result = service.broadcast_message("Broadcast message", "regular")

        # Verify
        assert result["success"] is False
        mock_instance.broadcast_message.assert_called_once()

    @patch("src.services.unified_messaging_service.ConsolidatedMessagingService")
    def test_send_message_with_urgent_priority(self, mock_consolidated):
        """Test sending message with urgent priority."""
        # Setup
        mock_instance = Mock()
        mock_instance.send_message.return_value = {"success": True, "message": "Sent"}
        mock_consolidated.return_value = mock_instance

        service = UnifiedMessagingService()

        # Execute
        result = service.send_message("Agent-1", "Urgent", "urgent", True)

        # Verify - send_message returns the dict, not boolean
        assert result == {"success": True, "message": "Sent"}
        mock_instance.send_message.assert_called_once_with("Agent-1", "Urgent", "urgent", True)

    @patch("src.services.unified_messaging_service.ConsolidatedMessagingService")
    def test_send_message_without_pyautogui(self, mock_consolidated):
        """Test sending message without PyAutoGUI."""
        # Setup
        mock_instance = Mock()
        mock_instance.send_message.return_value = {"success": True, "message": "Sent"}
        mock_consolidated.return_value = mock_instance

        service = UnifiedMessagingService()

        # Execute
        result = service.send_message("Agent-1", "Test", "regular", False)

        # Verify - send_message returns the dict, not boolean
        assert result == {"success": True, "message": "Sent"}
        mock_instance.send_message.assert_called_once_with("Agent-1", "Test", "regular", False)

