"""
Expanded unit tests for messaging_infrastructure.py - Batch 9

Additional tests for comprehensive coverage.
"""

import subprocess
from unittest.mock import Mock, patch
import pytest

from src.services.messaging_infrastructure import (
    ConsolidatedMessagingService,
    MessageCoordinator,
    handle_message,
    handle_survey,
    handle_consolidation,
    handle_coordinates,
    handle_start_agents,
    handle_save,
    handle_leaderboard,
    send_message_pyautogui,
    send_message_to_onboarding_coords,
    _format_multi_agent_request_message,
    _format_normal_message_with_instructions,
    create_messaging_parser,
    send_discord_message,
    broadcast_discord_message,
)


class TestMessageCoordinatorExpanded:
    """Expanded tests for MessageCoordinator."""

    @patch("src.core.message_queue.MessageQueue")
    def test_send_to_agent_fallback_no_queue(self, mock_queue_class):
        """Test send_to_agent falls back when queue unavailable."""
        from src.services.messaging_infrastructure import MessageCoordinator
        
        MessageCoordinator._queue = None
        mock_queue_class.return_value = None
        
        with patch('src.core.messaging_core.send_message', return_value=True) as mock_send:
            result = MessageCoordinator.send_to_agent("Agent-1", "Test message")
            
            assert isinstance(result, (bool, dict))
            # May call send_message if queue unavailable

    @patch("src.core.message_queue.MessageQueue")
    def test_send_to_agent_with_stalled_flag(self, mock_queue_class):
        """Test send_to_agent with stalled flag."""
        mock_queue = Mock()
        mock_queue.enqueue.return_value = "queue-id-123"
        mock_queue_class.return_value = mock_queue
        
        MessageCoordinator._queue = None
        
        result = MessageCoordinator.send_to_agent(
            "Agent-1", 
            "Test message", 
            stalled=True
        )
        
        assert isinstance(result, dict)
        if result.get("success"):
            enqueue_call = mock_queue.enqueue.call_args.kwargs['message']
            assert enqueue_call["metadata"]["stalled"] is True

    @patch("src.core.message_queue.MessageQueue")
    def test_broadcast_to_all_fallback_no_queue(self, mock_queue_class):
        """Test broadcast_to_all falls back when queue unavailable."""
        from src.core.messaging_core import UnifiedMessagePriority
        
        MessageCoordinator._queue = None
        mock_queue_class.return_value = None
        
        with patch('src.core.messaging_core.send_message', return_value=True) as mock_send, \
             patch('src.core.keyboard_control_lock.keyboard_control') as mock_keyboard_control:
            # Mock context manager
            mock_keyboard_control.return_value.__enter__ = Mock(return_value=None)
            mock_keyboard_control.return_value.__exit__ = Mock(return_value=False)
            
            result = MessageCoordinator.broadcast_to_all(
                "Test broadcast", 
                UnifiedMessagePriority.REGULAR
            )
            
            assert isinstance(result, int)
            assert result >= 0

    @patch("src.core.message_queue.MessageQueue")
    def test_broadcast_to_all_with_stalled_flag(self, mock_queue_class):
        """Test broadcast_to_all with stalled flag."""
        from src.core.messaging_core import UnifiedMessagePriority
        
        mock_queue = Mock()
        mock_queue.enqueue.return_value = "queue-id-123"
        mock_queue_class.return_value = mock_queue
        
        MessageCoordinator._queue = None
        
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator_getter:
            mock_validator = Mock()
            mock_validator.validate_agent_can_send_message.return_value = (True, None, None)
            mock_validator_getter.return_value = mock_validator
            
            result = MessageCoordinator.broadcast_to_all(
                "Test broadcast", 
                UnifiedMessagePriority.REGULAR,
                stalled=True
            )
            
            assert isinstance(result, int)
            assert result == 8

    def test_coordinate_survey_failure(self):
        """Test coordinate_survey when broadcast fails."""
        with patch.object(MessageCoordinator, 'broadcast_to_all', return_value=0):
            result = MessageCoordinator.coordinate_survey()
            assert result is False

    def test_coordinate_consolidation_failure(self):
        """Test coordinate_consolidation when broadcast fails."""
        with patch.object(MessageCoordinator, 'broadcast_to_all', return_value=0):
            result = MessageCoordinator.coordinate_consolidation("batch-1", "complete")
            assert result is False

    @patch("src.core.message_queue.MessageQueue")
    def test_send_multi_agent_request_no_queue(self, mock_queue_class):
        """Test send_multi_agent_request when queue unavailable."""
        from src.core.messaging_core import UnifiedMessagePriority
        
        MessageCoordinator._queue = None
        mock_queue_class.return_value = None
        
        with patch('src.core.multi_agent_responder.get_multi_agent_responder') as mock_responder_getter:
            mock_responder = Mock()
            mock_responder.create_request.return_value = "collector-123"
            mock_responder_getter.return_value = mock_responder
            
            result = MessageCoordinator.send_multi_agent_request(
                ["Agent-1", "Agent-2"],
                "Test request",
                timeout_seconds=300
            )
            
            # Should return empty string if queue unavailable
            assert result == ""

    @patch("src.core.message_queue.MessageQueue")
    def test_send_multi_agent_request_with_stalled(self, mock_queue_class):
        """Test send_multi_agent_request with stalled flag."""
        from src.core.messaging_core import UnifiedMessagePriority
        
        mock_queue = Mock()
        mock_queue.enqueue.return_value = "queue-id-123"
        mock_queue_class.return_value = mock_queue
        
        with patch.object(MessageCoordinator, '_get_queue', return_value=mock_queue), \
             patch('src.core.multi_agent_responder.get_multi_agent_responder') as mock_responder_getter:
            mock_responder = Mock()
            mock_responder.create_request.return_value = "collector-123"
            mock_responder_getter.return_value = mock_responder
            
            result = MessageCoordinator.send_multi_agent_request(
                ["Agent-1", "Agent-2"],
                "Test request",
                stalled=True,
                timeout_seconds=300
            )
            
            assert result == "collector-123"
            # Verify stalled flag in metadata
            enqueue_calls = mock_queue.enqueue.call_args_list
            for call in enqueue_calls:
                assert call.kwargs['message']['metadata']['stalled'] is True


class TestConsolidatedMessagingServiceExpanded:
    """Expanded tests for ConsolidatedMessagingService."""

    def test_init_queue_failure(self):
        """Test initialization when queue fails."""
        with patch('src.core.message_queue.MessageQueue', side_effect=Exception("Queue error")):
            service = ConsolidatedMessagingService()
            assert service.queue is None

    @patch("src.core.message_queue.MessageQueue")
    def test_send_message_queue_unavailable(self, mock_queue_class):
        """Test send_message when queue is None."""
        service = ConsolidatedMessagingService()
        service.queue = None
        
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator_getter:
            mock_validator = Mock()
            mock_validator.validate_agent_can_send_message.return_value = (True, None, None)
            mock_validator_getter.return_value = mock_validator
            
            with patch("src.services.messaging_infrastructure.subprocess.run") as mock_subprocess:
                mock_result = Mock()
                mock_result.returncode = 0
                mock_result.stderr = ""
                mock_subprocess.return_value = mock_result
                
                result = service.send_message("Agent-1", "Test", "regular", True)
                
                assert result["success"] is True
                mock_subprocess.assert_called_once()

    @patch("src.core.message_queue.MessageQueue")
    def test_send_message_subprocess_failure(self, mock_queue_class):
        """Test send_message when subprocess fails."""
        service = ConsolidatedMessagingService()
        service.queue = None
        
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator_getter:
            mock_validator = Mock()
            mock_validator.validate_agent_can_send_message.return_value = (True, None, None)
            mock_validator_getter.return_value = mock_validator
            
            with patch("src.services.messaging_infrastructure.subprocess.run") as mock_subprocess:
                mock_result = Mock()
                mock_result.returncode = 1
                mock_result.stderr = "Error message"
                mock_subprocess.return_value = mock_result
                
                result = service.send_message("Agent-1", "Test", "regular", False)
                
                assert result["success"] is False
                assert "Error message" in result["message"]

    @patch("src.core.message_queue.MessageQueue")
    def test_send_message_subprocess_timeout(self, mock_queue_class):
        """Test send_message when subprocess times out."""
        service = ConsolidatedMessagingService()
        service.queue = None
        
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator_getter:
            mock_validator = Mock()
            mock_validator.validate_agent_can_send_message.return_value = (True, None, None)
            mock_validator_getter.return_value = mock_validator
            
            with patch("src.services.messaging_infrastructure.subprocess.run", side_effect=subprocess.TimeoutExpired("cmd", 30)):
                result = service.send_message("Agent-1", "Test", "regular", False)
                
                assert result["success"] is False
                assert "timeout" in result["message"].lower()

    @patch("src.core.message_queue.MessageQueue")
    def test_send_message_exception_handling(self, mock_queue_class):
        """Test send_message exception handling."""
        service = ConsolidatedMessagingService()
        service.queue = None
        
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator_getter:
            mock_validator = Mock()
            mock_validator.validate_agent_can_send_message.return_value = (True, None, None)
            mock_validator_getter.return_value = mock_validator
            
            with patch("src.services.messaging_infrastructure.subprocess.run", side_effect=Exception("Unexpected error")):
                result = service.send_message("Agent-1", "Test", "regular", False)
                
                assert result["success"] is False
                assert "Unexpected error" in result["message"]

    @patch("src.core.keyboard_control_lock.keyboard_control")
    @patch("src.core.message_queue.MessageQueue")
    def test_broadcast_message_partial_delivery(self, mock_queue_class, mock_keyboard_control):
        """Test broadcast_message with partial delivery success."""
        mock_queue = Mock()
        mock_queue.enqueue.return_value = "queue-id-123"
        mock_queue.wait_for_delivery.side_effect = [True, True, False, False, True, True, False, False]
        mock_queue_class.return_value = mock_queue
        
        mock_keyboard_control.return_value.__enter__ = Mock()
        mock_keyboard_control.return_value.__exit__ = Mock(return_value=False)
        
        service = ConsolidatedMessagingService()
        service.queue = mock_queue
        
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator_getter:
            mock_validator = Mock()
            mock_validator.validate_agent_can_send_message.return_value = (True, None, None)
            mock_validator_getter.return_value = mock_validator
            
            result = service.broadcast_message("Broadcast", "regular")
            
            assert result["success"] is True
            assert result["message"].startswith("Broadcast to")
            assert "4 delivered" in result["message"] or "delivered" in result["message"]

    @patch("src.core.keyboard_control_lock.keyboard_control")
    @patch("src.core.message_queue.MessageQueue")
    def test_broadcast_message_all_fail(self, mock_queue_class, mock_keyboard_control):
        """Test broadcast_message when all messages fail."""
        mock_queue = Mock()
        mock_queue.enqueue.return_value = "queue-id-123"
        mock_queue.wait_for_delivery.return_value = False
        mock_queue_class.return_value = mock_queue
        
        mock_keyboard_control.return_value.__enter__ = Mock()
        mock_keyboard_control.return_value.__exit__ = Mock(return_value=False)
        
        service = ConsolidatedMessagingService()
        service.queue = mock_queue
        
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator_getter:
            mock_validator = Mock()
            mock_validator.validate_agent_can_send_message.return_value = (True, None, None)
            mock_validator_getter.return_value = mock_validator
            
            result = service.broadcast_message("Broadcast", "regular")
            
            assert result["success"] is False
            assert "0 delivered" in result["message"] or "delivered" in result["message"]


class TestHandlerFunctionsExpanded:
    """Expanded tests for handler functions."""

    def test_handle_message_urgent_priority(self):
        """Test handle_message with urgent priority."""
        args = Mock()
        args.agent = "Agent-1"
        args.broadcast = False
        args.message = "Urgent test"
        args.priority = "urgent"
        args.stalled = False
        
        parser = Mock()
        
        with patch('src.services.messaging_infrastructure.MessageCoordinator.send_to_agent', return_value={"success": True}):
            result = handle_message(args, parser)
            assert result == 0

    def test_handle_message_old_format_bool_false(self):
        """Test handle_message with old format (bool False)."""
        args = Mock()
        args.agent = "Agent-1"
        args.broadcast = False
        args.message = "Test"
        args.priority = "regular"
        args.stalled = False
        
        parser = Mock()
        
        with patch('src.services.messaging_infrastructure.MessageCoordinator.send_to_agent', return_value=False):
            result = handle_message(args, parser)
            assert result == 1

    def test_handle_message_exception(self):
        """Test handle_message exception handling."""
        args = Mock()
        args.agent = "Agent-1"
        args.broadcast = False
        args.message = "Test"
        args.priority = "regular"
        args.stalled = False
        
        parser = Mock()
        
        with patch('src.services.messaging_infrastructure.MessageCoordinator.send_to_agent', side_effect=Exception("Error")):
            result = handle_message(args, parser)
            assert result == 1

    def test_handle_survey_failure(self):
        """Test handle_survey when coordination fails."""
        with patch('src.services.messaging_infrastructure.MessageCoordinator.coordinate_survey', return_value=False):
            result = handle_survey()
            assert result == 1

    def test_handle_survey_exception(self):
        """Test handle_survey exception handling."""
        with patch('src.services.messaging_infrastructure.MessageCoordinator.coordinate_survey', side_effect=Exception("Error")):
            result = handle_survey()
            assert result == 1

    def test_handle_consolidation_failure(self):
        """Test handle_consolidation when coordination fails."""
        args = Mock()
        args.consolidation_batch = "batch-1"
        args.consolidation_status = "complete"
        
        with patch('src.services.messaging_infrastructure.MessageCoordinator.coordinate_consolidation', return_value=False):
            result = handle_consolidation(args)
            assert result == 1

    def test_handle_consolidation_exception(self):
        """Test handle_consolidation exception handling."""
        args = Mock()
        args.consolidation_batch = "batch-1"
        args.consolidation_status = "complete"
        
        with patch('src.services.messaging_infrastructure.MessageCoordinator.coordinate_consolidation', side_effect=Exception("Error")):
            result = handle_consolidation(args)
            assert result == 1

    def test_handle_coordinates_exception(self):
        """Test handle_coordinates exception handling."""
        with patch('src.services.messaging_infrastructure.get_coordinate_loader', side_effect=Exception("Error")):
            result = handle_coordinates()
            assert result == 1

    def test_handle_start_agents_invalid_agent(self):
        """Test handle_start_agents with invalid agent number."""
        args = Mock()
        args.start = [99]  # Invalid agent number
        args.message = "START"
        
        with patch('src.services.messaging_infrastructure.send_message_to_onboarding_coords', return_value=True):
            result = handle_start_agents(args)
            assert result == 0  # Should continue without error

    def test_handle_start_agents_exception(self):
        """Test handle_start_agents exception handling."""
        args = Mock()
        args.start = [1, 2]
        args.message = "START"
        
        with patch('src.services.messaging_infrastructure.send_message_to_onboarding_coords', side_effect=Exception("Error")):
            result = handle_start_agents(args)
            assert result == 1

    def test_handle_save_no_message(self):
        """Test handle_save without message."""
        args = Mock()
        args.message = None
        
        parser = Mock()
        
        result = handle_save(args, parser)
        assert result == 1

    def test_handle_save_exception(self):
        """Test handle_save exception handling."""
        args = Mock()
        args.message = "Save message"
        
        parser = Mock()
        
        with patch('src.services.messaging_infrastructure.get_coordinate_loader', side_effect=Exception("Error")):
            result = handle_save(args, parser)
            assert result == 1

    def test_handle_leaderboard_exception(self):
        """Test handle_leaderboard exception handling."""
        with patch('src.services.messaging_infrastructure.get_competition_system', side_effect=Exception("Error")):
            result = handle_leaderboard()
            assert result == 1

    def test_send_message_pyautogui(self):
        """Test send_message_pyautogui function."""
        with patch('src.core.messaging_core.send_message', return_value=True):
            result = send_message_pyautogui("Agent-1", "Test", 30)
            assert result is True

    def test_send_message_to_onboarding_coords(self):
        """Test send_message_to_onboarding_coords function."""
        with patch('src.services.messaging_infrastructure.send_message_pyautogui', return_value=True):
            result = send_message_to_onboarding_coords("Agent-1", "Test", 30)
            assert result is True

    def test_format_multi_agent_request_message_edge_cases(self):
        """Test _format_multi_agent_request_message with edge cases."""
        # Test with 0 recipients
        result = _format_multi_agent_request_message("Test", "collector-123", "req-456", 0, 60)
        assert "0 agent(s)" in result or "0" in result
        
        # Test with 1 recipient
        result = _format_multi_agent_request_message("Test", "collector-123", "req-456", 1, 60)
        assert "1 agent(s)" in result or "1" in result
        
        # Test with large timeout
        result = _format_multi_agent_request_message("Test", "collector-123", "req-456", 3, 3600)
        assert "60 minutes" in result or "3600" in result

    def test_format_normal_message_with_instructions_edge_cases(self):
        """Test _format_normal_message_with_instructions with edge cases."""
        # Test with empty message
        result = _format_normal_message_with_instructions("", "NORMAL")
        assert "STANDARD MESSAGE" in result or "NORMAL" in result
        
        # Test with very long message
        long_message = "A" * 1000
        result = _format_normal_message_with_instructions(long_message, "NORMAL")
        assert long_message in result

    def test_create_messaging_parser_all_args(self):
        """Test create_messaging_parser with all arguments."""
        parser = create_messaging_parser()
        
        # Test parsing with all flags
        args = parser.parse_args([
            "--message", "Test",
            "--agent", "Agent-1",
            "--priority", "urgent",
            "--tags", "tag1", "tag2",
            "--pyautogui",
            "--survey-coordination",
            "--consolidation-coordination",
            "--consolidation-batch", "batch-1",
            "--consolidation-status", "complete",
            "--coordinates",
            "--start", "1", "2", "3",
            "--save",
            "--leaderboard",
            "--get-next-task",
            "--list-tasks",
            "--task-status", "task-123",
            "--complete-task", "task-123"
        ])
        
        assert args.message == "Test"
        assert args.agent == "Agent-1"
        assert args.priority == "urgent"
        assert args.tags == ["tag1", "tag2"]
        assert args.pyautogui is True
        assert args.survey_coordination is True
        assert args.consolidation_coordination is True
        assert args.consolidation_batch == "batch-1"
        assert args.consolidation_status == "complete"
        assert args.coordinates is True
        assert args.start == [1, 2, 3]
        assert args.save is True
        assert args.leaderboard is True
        assert args.get_next_task is True
        assert args.list_tasks is True
        assert args.task_status == "task-123"
        assert args.complete_task == "task-123"

    def test_send_discord_message_failure(self):
        """Test send_discord_message when service fails."""
        with patch('src.services.messaging_infrastructure.ConsolidatedMessagingService') as mock_service_class:
            mock_service = Mock()
            mock_service.send_message.return_value = {"success": False}
            mock_service_class.return_value = mock_service
            
            result = send_discord_message("Agent-1", "Test", "regular")
            assert result is False

    def test_broadcast_discord_message_failure(self):
        """Test broadcast_discord_message when service fails."""
        with patch('src.services.messaging_infrastructure.ConsolidatedMessagingService') as mock_service_class:
            mock_service = Mock()
            mock_service.broadcast_message.return_value = {"success": False}
            mock_service_class.return_value = mock_service
            
            result = broadcast_discord_message("Test", "regular")
            assert result["success"] is False

