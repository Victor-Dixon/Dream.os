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

    @patch("src.core.message_queue.MessageQueue")
    def test_send_message_blocked_pending_request(self, mock_queue_class):
        """Test send_message blocks when agent has pending multi-agent request."""
        # Setup
        mock_queue = Mock()
        mock_queue_class.return_value = mock_queue
        
        service = ConsolidatedMessagingService()
        service.queue = mock_queue
        
        # Mock validator to return blocked
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator_getter:
            mock_validator = Mock()
            mock_validator.validate_agent_can_send_message.return_value = (
                False, "Blocked - pending request", {"collector_id": "collector-123"}
            )
            mock_validator_getter.return_value = mock_validator
            
            # Execute
            result = service.send_message("Agent-1", "Test message", "regular", True)
            
            # Verify
            assert result["success"] is False
            assert result["blocked"] is True
            assert result["reason"] == "pending_multi_agent_request"
            assert "pending_info" in result
            # Queue should not be called when blocked
            mock_queue.enqueue.assert_not_called()

    def test_resolve_discord_sender_with_id(self):
        """Test _resolve_discord_sender with user ID."""
        service = ConsolidatedMessagingService()
        result = service._resolve_discord_sender("123456789")
        assert result.startswith("DISCORD-")
        assert "123456789"[:8] in result

    def test_resolve_discord_sender_none(self):
        """Test _resolve_discord_sender with None."""
        service = ConsolidatedMessagingService()
        result = service._resolve_discord_sender(None)
        assert result == "DISCORD"

    def test_get_discord_username_with_id(self):
        """Test _get_discord_username with user ID."""
        service = ConsolidatedMessagingService()
        result = service._get_discord_username("123456789")
        # Currently returns None, but method exists
        assert result is None or isinstance(result, str)

    def test_get_discord_username_none(self):
        """Test _get_discord_username with None."""
        service = ConsolidatedMessagingService()
        result = service._get_discord_username(None)
        assert result is None


class TestMessageCoordinator:
    """Test suite for MessageCoordinator class."""

    @patch("src.core.message_queue.MessageQueue")
    def test_send_to_agent_with_queue(self, mock_queue_class):
        """Test send_to_agent with queue available."""
        mock_queue = Mock()
        mock_queue.enqueue.return_value = "queue-id-123"
        mock_queue_class.return_value = mock_queue
        
        from src.services.messaging_infrastructure import MessageCoordinator
        
        # Reset queue for test
        MessageCoordinator._queue = None
        
        result = MessageCoordinator.send_to_agent("Agent-1", "Test message")
        
        assert isinstance(result, dict)
        assert result.get("success") is True
        assert result.get("queue_id") == "queue-id-123"

    @patch("src.core.message_queue.MessageQueue")
    def test_send_to_agent_blocked(self, mock_queue_class):
        """Test send_to_agent blocks when recipient has pending request."""
        mock_queue = Mock()
        mock_queue_class.return_value = mock_queue
        
        from src.services.messaging_infrastructure import MessageCoordinator
        
        # Reset queue for test
        MessageCoordinator._queue = None
        
        # Mock validator to return blocked
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator_getter:
            mock_validator = Mock()
            mock_validator.validate_agent_can_send_message.return_value = (
                False, "Blocked", {"collector_id": "collector-123"}
            )
            mock_validator_getter.return_value = mock_validator
            
            result = MessageCoordinator.send_to_agent("Agent-1", "Test message")
            
            assert isinstance(result, dict)
            assert result.get("success") is False
            assert result.get("blocked") is True

    @patch("src.core.message_queue.MessageQueue")
    def test_broadcast_to_all_with_queue(self, mock_queue_class):
        """Test broadcast_to_all with queue available."""
        mock_queue = Mock()
        mock_queue.enqueue.return_value = "queue-id-123"
        mock_queue_class.return_value = mock_queue
        
        from src.services.messaging_infrastructure import MessageCoordinator
        from src.core.messaging_core import UnifiedMessagePriority
        
        # Reset queue for test
        MessageCoordinator._queue = None
        
        # Mock validator to allow all
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator_getter:
            mock_validator = Mock()
            mock_validator.validate_agent_can_send_message.return_value = (True, None, None)
            mock_validator_getter.return_value = mock_validator
            
            result = MessageCoordinator.broadcast_to_all("Test broadcast", UnifiedMessagePriority.REGULAR)
            
            assert isinstance(result, int)
            assert result == 8  # Should queue 8 messages

    @patch("src.core.message_queue.MessageQueue")
    def test_broadcast_to_all_skips_blocked(self, mock_queue_class):
        """Test broadcast_to_all skips agents with pending requests."""
        mock_queue = Mock()
        mock_queue.enqueue.return_value = "queue-id-123"
        mock_queue_class.return_value = mock_queue
        
        from src.services.messaging_infrastructure import MessageCoordinator
        from src.core.messaging_core import UnifiedMessagePriority
        
        # Reset queue for test
        MessageCoordinator._queue = None
        
        # Mock validator to block Agent-1
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator_getter:
            mock_validator = Mock()
            def validate_side_effect(agent_id, target_recipient, message_content):
                if agent_id == "Agent-1":
                    return (False, "Blocked", {"collector_id": "collector-123"})
                return (True, None, None)
            mock_validator.validate_agent_can_send_message.side_effect = validate_side_effect
            mock_validator_getter.return_value = mock_validator
            
            result = MessageCoordinator.broadcast_to_all("Test broadcast", UnifiedMessagePriority.REGULAR)
            
            # Should queue 7 messages (skip Agent-1)
            assert result == 7
            assert mock_queue.enqueue.call_count == 7

    def test_coordinate_survey(self):
        """Test coordinate_survey method."""
        from src.services.messaging_infrastructure import MessageCoordinator
        from src.core.messaging_core import UnifiedMessagePriority
        
        with patch.object(MessageCoordinator, 'broadcast_to_all', return_value=8):
            result = MessageCoordinator.coordinate_survey()
            assert result is True

    def test_coordinate_consolidation(self):
        """Test coordinate_consolidation method."""
        from src.services.messaging_infrastructure import MessageCoordinator
        
        with patch.object(MessageCoordinator, 'broadcast_to_all', return_value=8):
            result = MessageCoordinator.coordinate_consolidation("batch-1", "complete")
            assert result is True

    def test_send_multi_agent_request(self):
        """Test send_multi_agent_request method."""
        from src.services.messaging_infrastructure import MessageCoordinator
        from src.core.messaging_core import UnifiedMessagePriority
        
        with patch('src.core.multi_agent_responder.get_multi_agent_responder') as mock_responder_getter:
            mock_responder = Mock()
            mock_responder.create_request.return_value = "collector-123"
            mock_responder_getter.return_value = mock_responder
            
            with patch.object(MessageCoordinator, '_get_queue') as mock_get_queue:
                mock_queue = Mock()
                mock_queue.enqueue.return_value = "queue-id-123"
                mock_get_queue.return_value = mock_queue
                
                result = MessageCoordinator.send_multi_agent_request(
                    ["Agent-1", "Agent-2"],
                    "Test request",
                    timeout_seconds=300
                )
                
                assert result == "collector-123"
                assert mock_queue.enqueue.call_count == 2


class TestHandlerFunctions:
    """Test suite for handler functions."""

    def test_handle_message_broadcast(self):
        """Test handle_message with broadcast flag."""
        from src.services.messaging_infrastructure import handle_message
        from src.core.messaging_core import UnifiedMessagePriority
        
        args = Mock()
        args.agent = None
        args.broadcast = True
        args.message = "Broadcast test"
        args.priority = "regular"
        args.stalled = False
        
        parser = Mock()
        
        with patch('src.services.messaging_infrastructure.MessageCoordinator.broadcast_to_all', return_value=8):
            result = handle_message(args, parser)
            assert result == 0

    def test_handle_message_agent(self):
        """Test handle_message with agent flag."""
        from src.services.messaging_infrastructure import handle_message
        
        args = Mock()
        args.agent = "Agent-1"
        args.broadcast = False
        args.message = "Test message"
        args.priority = "regular"
        args.stalled = False
        
        parser = Mock()
        
        with patch('src.services.messaging_infrastructure.MessageCoordinator.send_to_agent', return_value={"success": True}):
            result = handle_message(args, parser)
            assert result == 0

    def test_handle_message_blocked(self):
        """Test handle_message when message is blocked."""
        from src.services.messaging_infrastructure import handle_message
        
        args = Mock()
        args.agent = "Agent-1"
        args.broadcast = False
        args.message = "Test message"
        args.priority = "regular"
        args.stalled = False
        
        parser = Mock()
        
        with patch('src.services.messaging_infrastructure.MessageCoordinator.send_to_agent', return_value={"success": False, "blocked": True, "error_message": "Pending request"}):
            result = handle_message(args, parser)
            assert result == 1

    def test_handle_message_no_agent_no_broadcast(self):
        """Test handle_message with neither agent nor broadcast."""
        from src.services.messaging_infrastructure import handle_message
        
        args = Mock()
        args.agent = None
        args.broadcast = False
        args.message = "Test"
        
        parser = Mock()
        parser.print_help = Mock()
        
        result = handle_message(args, parser)
        assert result == 1
        parser.print_help.assert_called_once()

    def test_handle_message_priority_normal(self):
        """Test handle_message normalizes 'normal' priority to 'regular'."""
        from src.services.messaging_infrastructure import handle_message
        from src.core.messaging_core import UnifiedMessagePriority
        
        args = Mock()
        args.agent = "Agent-1"
        args.broadcast = False
        args.message = "Test"
        args.priority = "normal"
        args.stalled = False
        
        parser = Mock()
        
        with patch('src.services.messaging_infrastructure.MessageCoordinator.send_to_agent', return_value={"success": True}) as mock_send:
            handle_message(args, parser)
            # Verify priority was normalized
            call_args = mock_send.call_args
            assert call_args[0][2] in [UnifiedMessagePriority.REGULAR, "regular"]

    def test_handle_survey(self):
        """Test handle_survey function."""
        from src.services.messaging_infrastructure import handle_survey
        
        with patch('src.services.messaging_infrastructure.MessageCoordinator.coordinate_survey', return_value=True):
            result = handle_survey()
            assert result == 0

    def test_handle_consolidation(self):
        """Test handle_consolidation function."""
        from src.services.messaging_infrastructure import handle_consolidation
        
        args = Mock()
        args.consolidation_batch = "batch-1"
        args.consolidation_status = "complete"
        
        with patch('src.services.messaging_infrastructure.MessageCoordinator.coordinate_consolidation', return_value=True):
            result = handle_consolidation(args)
            assert result == 0

    def test_handle_coordinates(self):
        """Test handle_coordinates function."""
        from src.services.messaging_infrastructure import handle_coordinates
        
        with patch('src.services.messaging_infrastructure.get_coordinate_loader') as mock_loader_getter:
            mock_loader = Mock()
            mock_loader.get_chat_coordinates.return_value = [100, 200]
            mock_loader.get_onboarding_coordinates.return_value = [300, 400]
            mock_loader_getter.return_value = mock_loader
            
            result = handle_coordinates()
            assert result == 0

    def test_handle_start_agents(self):
        """Test handle_start_agents function."""
        from src.services.messaging_infrastructure import handle_start_agents
        
        args = Mock()
        args.start = [1, 2, 3]
        args.message = "START"
        
        with patch('src.services.messaging_infrastructure.send_message_to_onboarding_coords', return_value=True):
            result = handle_start_agents(args)
            assert result == 0

    def test_handle_save(self):
        """Test handle_save function."""
        from src.services.messaging_infrastructure import handle_save
        
        args = Mock()
        args.message = "Save message"
        
        parser = Mock()
        
        with patch('src.services.messaging_infrastructure.get_coordinate_loader') as mock_loader_getter:
            mock_loader = Mock()
            mock_loader.get_chat_coordinates.return_value = [100, 200]
            mock_loader_getter.return_value = mock_loader
            
            with patch('src.services.messaging_infrastructure.pyautogui') as mock_pyautogui:
                result = handle_save(args, parser)
                assert result == 0

    def test_handle_leaderboard(self):
        """Test handle_leaderboard function."""
        from src.services.messaging_infrastructure import handle_leaderboard
        
        with patch('src.services.messaging_infrastructure.get_competition_system') as mock_comp_getter:
            mock_comp = Mock()
            mock_comp.get_leaderboard.return_value = [
                {"agent_id": "Agent-1", "score": 100, "contracts_completed": 5}
            ]
            mock_comp_getter.return_value = mock_comp
            
            result = handle_leaderboard()
            assert result == 0

    def test_format_multi_agent_request_message(self):
        """Test _format_multi_agent_request_message function."""
        from src.services.messaging_infrastructure import _format_multi_agent_request_message
        
        result = _format_multi_agent_request_message(
            "Test message",
            "collector-123",
            "request-456",
            3,
            300
        )
        
        assert "Test message" in result
        assert "collector-123" in result
        assert "request-456" in result
        assert "3 agent(s)" in result or "3" in result
        assert "5 minutes" in result or "300" in result

    def test_format_normal_message_with_instructions(self):
        """Test _format_normal_message_with_instructions function."""
        from src.services.messaging_infrastructure import _format_normal_message_with_instructions
        
        result = _format_normal_message_with_instructions("Test message", "NORMAL")
        assert "Test message" in result
        assert "NORMAL" in result or "normal" in result.lower()
        
        result_broadcast = _format_normal_message_with_instructions("Test", "BROADCAST")
        assert "BROADCAST" in result_broadcast or "broadcast" in result_broadcast.lower()

    def test_create_messaging_parser(self):
        """Test create_messaging_parser function."""
        from src.services.messaging_infrastructure import create_messaging_parser
        
        parser = create_messaging_parser()
        assert parser is not None
        
        # Test parsing some arguments
        args = parser.parse_args(["--message", "Test", "--agent", "Agent-1"])
        assert args.message == "Test"
        assert args.agent == "Agent-1"

    def test_send_discord_message(self):
        """Test send_discord_message function."""
        from src.services.messaging_infrastructure import send_discord_message
        
        with patch('src.services.messaging_infrastructure.ConsolidatedMessagingService') as mock_service_class:
            mock_service = Mock()
            mock_service.send_message.return_value = {"success": True}
            mock_service_class.return_value = mock_service
            
            result = send_discord_message("Agent-1", "Test", "regular")
            assert result is True

    def test_broadcast_discord_message(self):
        """Test broadcast_discord_message function."""
        from src.services.messaging_infrastructure import broadcast_discord_message
        
        with patch('src.services.messaging_infrastructure.ConsolidatedMessagingService') as mock_service_class:
            mock_service = Mock()
            mock_service.broadcast_message.return_value = {"success": True}
            mock_service_class.return_value = mock_service
            
            result = broadcast_discord_message("Test", "regular")
            assert result["success"] is True

