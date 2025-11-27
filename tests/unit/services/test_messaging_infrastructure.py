"""
Unit tests for messaging_infrastructure.py

Tests ConsolidatedMessagingService functionality with message queue support.
"""

import subprocess
import sys
import time
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

from src.services.messaging_infrastructure import ConsolidatedMessagingService


class TestConsolidatedMessagingService:
    """Test suite for ConsolidatedMessagingService (production implementation)."""

    def test_init(self):
        """Test service initialization."""
        service = ConsolidatedMessagingService()
        assert service.project_root is not None
        assert service.messaging_cli.exists() or service.messaging_cli.name == "messaging_cli.py"
        # Queue may or may not be initialized depending on availability
        assert hasattr(service, 'queue')

    @patch("src.services.messaging_infrastructure.subprocess.run")
    def test_send_message_success_fallback(self, mock_subprocess):
        """Test successful message sending via subprocess fallback (no queue)."""
        # Setup - service without queue
        service = ConsolidatedMessagingService()
        service.queue = None  # Simulate queue unavailable
        
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stderr = ""
        mock_subprocess.return_value = mock_result

        # Execute
        result = service.send_message("Agent-1", "Test message", "regular", True)

        # Verify
        assert result["success"] is True
        assert result["agent"] == "Agent-1"
        assert "Message sent" in result["message"] or "Message queued" in result["message"]
        mock_subprocess.assert_called_once()

    @patch("src.services.messaging_infrastructure.subprocess.run")
    def test_send_message_failure_fallback(self, mock_subprocess):
        """Test failed message sending via subprocess fallback."""
        # Setup - service without queue
        service = ConsolidatedMessagingService()
        service.queue = None
        
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stderr = "Error message"
        mock_subprocess.return_value = mock_result

        # Execute
        result = service.send_message("Agent-1", "Test message", "regular", True)

        # Verify
        assert result["success"] is False
        assert result["agent"] == "Agent-1"
        assert "Failed" in result["message"]

    @patch("src.services.messaging_infrastructure.subprocess.run")
    def test_send_message_timeout_fallback(self, mock_subprocess):
        """Test message sending timeout via subprocess fallback."""
        # Setup - service without queue
        service = ConsolidatedMessagingService()
        service.queue = None
        
        mock_subprocess.side_effect = subprocess.TimeoutExpired("cmd", 30)

        # Execute
        result = service.send_message("Agent-1", "Test message", "regular", True)

        # Verify
        assert result["success"] is False
        assert result["agent"] == "Agent-1"
        assert "timeout" in result["message"].lower()

    @patch("src.services.messaging_infrastructure.subprocess.run")
    def test_send_message_priority_urgent_fallback(self, mock_subprocess):
        """Test sending urgent priority message via subprocess fallback."""
        # Setup - service without queue
        service = ConsolidatedMessagingService()
        service.queue = None
        
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stderr = ""
        mock_subprocess.return_value = mock_result

        # Execute
        result = service.send_message("Agent-1", "Urgent message", "urgent", True)

        # Verify
        assert result["success"] is True
        # Verify priority was passed in command
        call_args = mock_subprocess.call_args[0][0]
        assert "--priority" in call_args
        priority_index = call_args.index("--priority")
        assert call_args[priority_index + 1] == "urgent"

    @patch("src.services.messaging_infrastructure.subprocess.run")
    def test_send_message_without_pyautogui_fallback(self, mock_subprocess):
        """Test sending message without PyAutoGUI via subprocess fallback."""
        # Setup - service without queue
        service = ConsolidatedMessagingService()
        service.queue = None
        
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stderr = ""
        mock_subprocess.return_value = mock_result

        # Execute
        result = service.send_message("Agent-1", "Test message", "regular", False)

        # Verify
        assert result["success"] is True
        # Verify --pyautogui flag not in command when use_pyautogui=False
        call_args = mock_subprocess.call_args[0][0]
        assert "--pyautogui" not in call_args

    @patch("src.services.messaging_infrastructure.subprocess.run")
    def test_broadcast_message_success(self, mock_subprocess):
        """Test successful broadcast message."""
        # Setup - service without queue (uses subprocess fallback)
        service = ConsolidatedMessagingService()
        service.queue = None
        
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stderr = ""
        mock_subprocess.return_value = mock_result

        # Execute
        result = service.broadcast_message("Broadcast message", "regular")

        # Verify
        assert result["success"] is True
        # Broadcast sends to each agent individually with wait_for_delivery
        # Should be called 8 times (once per agent)
        assert mock_subprocess.call_count == 8

    @patch("src.services.messaging_infrastructure.subprocess.run")
    def test_broadcast_message_failure(self, mock_subprocess):
        """Test failed broadcast message."""
        # Setup - service without queue
        service = ConsolidatedMessagingService()
        service.queue = None
        
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stderr = "Broadcast error"
        mock_subprocess.return_value = mock_result

        # Execute
        result = service.broadcast_message("Broadcast message", "regular")

        # Verify
        # Broadcast returns success=True if any agent succeeds, False if all fail
        # In this case, all fail (0/8), so success should be False
        assert result["success"] is False
        assert "0/8" in result["message"] or "0/" in result["message"]

    def test_send_message_command_structure_fallback(self):
        """Test command structure for send_message via subprocess fallback."""
        # Setup - service without queue
        service = ConsolidatedMessagingService()
        service.queue = None

        # Execute
        with patch("src.services.messaging_infrastructure.subprocess.run") as mock_subprocess:
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stderr = ""
            mock_subprocess.return_value = mock_result

            service.send_message("Agent-1", "Test", "regular", True)

            # Verify command structure
            call_args = mock_subprocess.call_args[0][0]
            assert "python" in call_args[0] or sys.executable in call_args[0]
            assert "--agent" in call_args
            assert "Agent-1" in call_args
            assert "--message" in call_args
            assert "Test" in call_args
            assert "--priority" in call_args
            assert "regular" in call_args


class TestConsolidatedMessagingServiceWithQueue:
    """Test suite for ConsolidatedMessagingService with message queue."""

    @patch("src.core.message_queue.MessageQueue")
    def test_send_message_with_queue_enqueue(self, mock_queue_class):
        """Test message queuing when queue is available."""
        # Setup
        mock_queue = Mock()
        mock_queue.enqueue.return_value = "queue-id-123"
        mock_queue_class.return_value = mock_queue
        
        service = ConsolidatedMessagingService()
        service.queue = mock_queue

        # Execute
        result = service.send_message("Agent-1", "Test message", "regular", True)

        # Verify
        assert result["success"] is True
        assert result["agent"] == "Agent-1"
        assert "queue_id" in result
        assert result["queue_id"] == "queue-id-123"
        mock_queue.enqueue.assert_called_once()
        
        # Verify message structure
        enqueue_call = mock_queue.enqueue.call_args.kwargs['message']
        assert enqueue_call["type"] == "agent_message"
        assert enqueue_call["recipient"] == "Agent-1"
        assert enqueue_call["content"] == "Test message"
        assert enqueue_call["priority"] == "regular"

    @patch("src.core.message_queue.MessageQueue")
    def test_send_message_with_queue_wait_for_delivery(self, mock_queue_class):
        """Test message queuing with wait_for_delivery=True."""
        # Setup
        mock_queue = Mock()
        mock_queue.enqueue.return_value = "queue-id-123"
        mock_queue.wait_for_delivery.return_value = True
        mock_queue_class.return_value = mock_queue
        
        service = ConsolidatedMessagingService()
        service.queue = mock_queue

        # Execute
        result = service.send_message(
            "Agent-1", 
            "Test message", 
            "regular", 
            True,
            wait_for_delivery=True,
            timeout=30.0
        )

        # Verify
        assert result["success"] is True
        assert result["delivered"] is True
        assert result["queue_id"] == "queue-id-123"
        mock_queue.enqueue.assert_called_once()
        mock_queue.wait_for_delivery.assert_called_once_with("queue-id-123", timeout=30.0)

    @patch("src.core.message_queue.MessageQueue")
    def test_send_message_with_queue_delivery_timeout(self, mock_queue_class):
        """Test message queuing with wait_for_delivery timeout."""
        # Setup
        mock_queue = Mock()
        mock_queue.enqueue.return_value = "queue-id-123"
        mock_queue.wait_for_delivery.return_value = False  # Timeout
        mock_queue_class.return_value = mock_queue
        
        service = ConsolidatedMessagingService()
        service.queue = mock_queue

        # Execute
        result = service.send_message(
            "Agent-1", 
            "Test message", 
            "regular", 
            True,
            wait_for_delivery=True,
            timeout=30.0
        )

        # Verify
        assert result["success"] is False
        assert result["delivered"] is False
        assert result["queue_id"] == "queue-id-123"
        mock_queue.wait_for_delivery.assert_called_once_with("queue-id-123", timeout=30.0)

    @patch("src.core.message_queue.MessageQueue")
    def test_send_message_with_discord_user_id(self, mock_queue_class):
        """Test message queuing with discord_user_id."""
        # Setup
        mock_queue = Mock()
        mock_queue.enqueue.return_value = "queue-id-123"
        mock_queue_class.return_value = mock_queue
        
        service = ConsolidatedMessagingService()
        service.queue = mock_queue
        # Mock helper methods if they don't exist
        if not hasattr(service, '_resolve_discord_sender'):
            service._resolve_discord_sender = lambda x: f"User-{x}"
        if not hasattr(service, '_get_discord_username'):
            service._get_discord_username = lambda x: f"username-{x}"

        # Execute
        result = service.send_message(
            "Agent-1", 
            "Test message", 
            "regular", 
            True,
            discord_user_id="123456789"
        )

        # Verify
        assert result["success"] is True
        enqueue_call = mock_queue.enqueue.call_args.kwargs['message']
        assert enqueue_call["discord_user_id"] == "123456789"
        assert "discord_user_id" in enqueue_call["metadata"]

    @patch("src.core.message_queue.MessageQueue")
    def test_send_message_with_stalled_flag(self, mock_queue_class):
        """Test message queuing with stalled flag."""
        # Setup
        mock_queue = Mock()
        mock_queue.enqueue.return_value = "queue-id-123"
        mock_queue_class.return_value = mock_queue
        
        service = ConsolidatedMessagingService()
        service.queue = mock_queue

        # Execute
        result = service.send_message(
            "Agent-1", 
            "Test message", 
            "regular", 
            True,
            stalled=True
        )

        # Verify
        assert result["success"] is True
        enqueue_call = mock_queue.enqueue.call_args.kwargs['message']
        assert enqueue_call["metadata"]["stalled"] is True

    @patch("src.core.message_queue.MessageQueue")
    def test_send_message_without_pyautogui_uses_fallback(self, mock_queue_class):
        """Test that use_pyautogui=False bypasses queue and uses subprocess."""
        # Setup
        mock_queue = Mock()
        mock_queue_class.return_value = mock_queue
        
        service = ConsolidatedMessagingService()
        service.queue = mock_queue

        with patch("src.services.messaging_infrastructure.subprocess.run") as mock_subprocess:
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stderr = ""
            mock_subprocess.return_value = mock_result

            # Execute
            result = service.send_message("Agent-1", "Test message", "regular", False)

            # Verify - queue should not be used
            mock_queue.enqueue.assert_not_called()
            mock_subprocess.assert_called_once()
            assert result["success"] is True

    @patch("src.core.keyboard_control_lock.keyboard_control")
    @patch("src.core.message_queue.MessageQueue")
    def test_broadcast_message_with_queue(self, mock_queue_class, mock_keyboard_control):
        """Test broadcast message with queue and keyboard lock."""
        # Setup
        mock_queue = Mock()
        mock_queue.enqueue.return_value = "queue-id-{agent}"
        mock_queue.wait_for_delivery.return_value = True
        mock_queue_class.return_value = mock_queue
        
        # Mock keyboard_control context manager
        mock_keyboard_control.return_value.__enter__ = Mock()
        mock_keyboard_control.return_value.__exit__ = Mock(return_value=False)
        
        service = ConsolidatedMessagingService()
        service.queue = mock_queue

        # Execute
        result = service.broadcast_message("Broadcast message", "regular")

        # Verify
        assert result["success"] is True
        # Should enqueue 8 messages (one per agent)
        assert mock_queue.enqueue.call_count == 8
        # Should wait for delivery 8 times
        assert mock_queue.wait_for_delivery.call_count == 8
        # Keyboard lock should be used
        mock_keyboard_control.assert_called_once_with("broadcast_operation")

