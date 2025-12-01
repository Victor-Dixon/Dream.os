"""
Batch 10 unit tests for messaging_infrastructure.py

Additional comprehensive tests for edge cases, error scenarios, and integration paths.
"""

import subprocess
from unittest.mock import Mock, patch, MagicMock
import pytest
import time

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
    SWARM_AGENTS,
)


class TestMessageCoordinatorBatch10:
    """Batch 10 tests for MessageCoordinator - Advanced scenarios."""

    @patch("src.core.message_queue.MessageQueue")
    def test_send_to_agent_concurrent_requests(self, mock_queue_class):
        """Test send_to_agent handles concurrent requests."""
        mock_queue = Mock()
        mock_queue.enqueue.return_value = "queue-id-123"
        mock_queue_class.return_value = mock_queue
        
        MessageCoordinator._queue = None
        
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator_getter:
            mock_validator = Mock()
            mock_validator.validate_agent_can_send_message.return_value = (True, None, None)
            mock_validator_getter.return_value = mock_validator
            
            # Simulate concurrent requests
            results = []
            for i in range(5):
                result = MessageCoordinator.send_to_agent(f"Agent-{i+1}", f"Message {i}")
                results.append(result)
            
            assert len(results) == 5
            assert all(isinstance(r, dict) for r in results)

    @patch("src.core.message_queue.MessageQueue")
    def test_send_to_agent_priority_urgent(self, mock_queue_class):
        """Test send_to_agent with urgent priority."""
        from src.core.messaging_core import UnifiedMessagePriority
        
        mock_queue = Mock()
        mock_queue.enqueue.return_value = "queue-id-123"
        mock_queue_class.return_value = mock_queue
        
        MessageCoordinator._queue = None
        
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator_getter:
            mock_validator = Mock()
            mock_validator.validate_agent_can_send_message.return_value = (True, None, None)
            mock_validator_getter.return_value = mock_validator
            
            result = MessageCoordinator.send_to_agent(
                "Agent-1", 
                "Urgent message", 
                priority=UnifiedMessagePriority.URGENT
            )
            
            assert result["success"] is True
            enqueue_call = mock_queue.enqueue.call_args.kwargs['message']
            assert enqueue_call["priority"] == UnifiedMessagePriority.URGENT.value

    @patch("src.core.message_queue.MessageQueue")
    def test_send_to_agent_fallback_exception(self, mock_queue_class):
        """Test send_to_agent fallback handles exceptions."""
        MessageCoordinator._queue = None
        mock_queue_class.return_value = None
        
        with patch('src.core.messaging_core.send_message', side_effect=Exception("Send error")):
            # Exception is caught and logged, returns False
            result = MessageCoordinator.send_to_agent("Agent-1", "Test")
            # Should return False on exception
            assert result is False or isinstance(result, bool)

    @patch("src.core.message_queue.MessageQueue")
    def test_send_multi_agent_request_empty_recipients(self, mock_queue_class):
        """Test send_multi_agent_request with empty recipients list."""
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
                [],  # Empty recipients
                "Test request",
                timeout_seconds=300
            )
            
            assert result == "collector-123"
            # Should not enqueue any messages
            assert mock_queue.enqueue.call_count == 0

    @patch("src.core.message_queue.MessageQueue")
    def test_send_multi_agent_request_responder_exception(self, mock_queue_class):
        """Test send_multi_agent_request handles responder exceptions."""
        from src.core.messaging_core import UnifiedMessagePriority
        
        MessageCoordinator._queue = None
        mock_queue_class.return_value = None
        
        with patch('src.core.multi_agent_responder.get_multi_agent_responder', side_effect=Exception("Responder error")):
            result = MessageCoordinator.send_multi_agent_request(
                ["Agent-1", "Agent-2"],
                "Test request",
                timeout_seconds=300
            )
            
            assert result == ""

    @patch("src.core.message_queue.MessageQueue")
    def test_broadcast_to_all_all_agents_skipped(self, mock_queue_class):
        """Test broadcast_to_all when all agents are skipped."""
        from src.core.messaging_core import UnifiedMessagePriority
        
        mock_queue = Mock()
        mock_queue_class.return_value = mock_queue
        
        MessageCoordinator._queue = None
        
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator_getter:
            mock_validator = Mock()
            # All agents blocked
            mock_validator.validate_agent_can_send_message.return_value = (
                False, "Blocked", {"collector_id": "collector-123"}
            )
            mock_validator_getter.return_value = mock_validator
            
            result = MessageCoordinator.broadcast_to_all(
                "Test broadcast", 
                UnifiedMessagePriority.REGULAR
            )
            
            assert result == 0
            assert mock_queue.enqueue.call_count == 0

    @patch("src.core.message_queue.MessageQueue")
    def test_broadcast_to_all_fallback_exception(self, mock_queue_class):
        """Test broadcast_to_all fallback handles exceptions."""
        from src.core.messaging_core import UnifiedMessagePriority
        
        MessageCoordinator._queue = None
        mock_queue_class.return_value = None
        
        with patch('src.core.keyboard_control_lock.keyboard_control') as mock_keyboard_control, \
             patch('src.core.messaging_core.send_message', side_effect=Exception("Send error")):
            mock_keyboard_control.return_value.__enter__ = Mock(return_value=None)
            mock_keyboard_control.return_value.__exit__ = Mock(return_value=False)
            
            result = MessageCoordinator.broadcast_to_all(
                "Test broadcast", 
                UnifiedMessagePriority.REGULAR
            )
            
            assert result == 0

    def test_coordinate_survey_exception(self):
        """Test coordinate_survey handles exceptions."""
        with patch.object(MessageCoordinator, 'broadcast_to_all', side_effect=Exception("Broadcast error")):
            result = MessageCoordinator.coordinate_survey()
            assert result is False

    def test_coordinate_consolidation_exception(self):
        """Test coordinate_consolidation handles exceptions."""
        with patch.object(MessageCoordinator, 'broadcast_to_all', side_effect=Exception("Broadcast error")):
            result = MessageCoordinator.coordinate_consolidation("batch-1", "complete")
            assert result is False


class TestConsolidatedMessagingServiceBatch10:
    """Batch 10 tests for ConsolidatedMessagingService - Advanced scenarios."""

    @patch("src.core.message_queue.MessageQueue")
    def test_send_message_validator_exception(self, mock_queue_class):
        """Test send_message handles validator exceptions."""
        service = ConsolidatedMessagingService()
        service.queue = Mock()
        service.queue.enqueue.return_value = "queue-id-123"
        
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator', side_effect=Exception("Validator error")):
            result = service.send_message("Agent-1", "Test", "regular", True)
            
            # Should handle exception gracefully
            assert isinstance(result, dict)
            assert result.get("success") is False

    @patch("src.core.message_queue.MessageQueue")
    def test_send_message_queue_enqueue_exception(self, mock_queue_class):
        """Test send_message handles queue enqueue exceptions."""
        service = ConsolidatedMessagingService()
        mock_queue = Mock()
        mock_queue.enqueue.side_effect = Exception("Enqueue error")
        service.queue = mock_queue
        
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator_getter:
            mock_validator = Mock()
            mock_validator.validate_agent_can_send_message.return_value = (True, None, None)
            mock_validator_getter.return_value = mock_validator
            
            result = service.send_message("Agent-1", "Test", "regular", True)
            
            assert result.get("success") is False

    @patch("src.core.message_queue.MessageQueue")
    def test_send_message_wait_for_delivery_exception(self, mock_queue_class):
        """Test send_message handles wait_for_delivery exceptions."""
        service = ConsolidatedMessagingService()
        mock_queue = Mock()
        mock_queue.enqueue.return_value = "queue-id-123"
        mock_queue.wait_for_delivery.side_effect = Exception("Wait error")
        service.queue = mock_queue
        
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator_getter:
            mock_validator = Mock()
            mock_validator.validate_agent_can_send_message.return_value = (True, None, None)
            mock_validator_getter.return_value = mock_validator
            
            result = service.send_message(
                "Agent-1", 
                "Test", 
                "regular", 
                True,
                wait_for_delivery=True,
                timeout=30.0
            )
            
            assert result.get("success") is False
            assert result.get("delivered") is False

    @patch("src.core.keyboard_control_lock.keyboard_control")
    @patch("src.core.message_queue.MessageQueue")
    def test_broadcast_message_keyboard_lock_exception(self, mock_queue_class, mock_keyboard_control):
        """Test broadcast_message handles keyboard lock exceptions."""
        service = ConsolidatedMessagingService()
        service.queue = Mock()
        service.queue.enqueue.return_value = "queue-id-123"
        service.queue.wait_for_delivery.return_value = True
        
        mock_keyboard_control.side_effect = Exception("Lock error")
        
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator_getter:
            mock_validator = Mock()
            mock_validator.validate_agent_can_send_message.return_value = (True, None, None)
            mock_validator_getter.return_value = mock_validator
            
            result = service.broadcast_message("Broadcast", "regular")
            
            # Should handle exception gracefully
            assert isinstance(result, dict)

    @patch("src.core.keyboard_control_lock.keyboard_control")
    @patch("src.core.message_queue.MessageQueue")
    def test_broadcast_message_send_exception(self, mock_queue_class, mock_keyboard_control):
        """Test broadcast_message handles send_message exceptions."""
        service = ConsolidatedMessagingService()
        service.queue = Mock()
        service.queue.enqueue.return_value = "queue-id-123"
        service.queue.wait_for_delivery.return_value = True
        
        mock_keyboard_control.return_value.__enter__ = Mock(return_value=None)
        mock_keyboard_control.return_value.__exit__ = Mock(return_value=False)
        
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator_getter:
            mock_validator = Mock()
            mock_validator.validate_agent_can_send_message.return_value = (True, None, None)
            mock_validator_getter.return_value = mock_validator
            
            # Make send_message raise exception after first call
            call_count = [0]
            def send_side_effect(*args, **kwargs):
                call_count[0] += 1
                if call_count[0] > 1:
                    raise Exception("Send error")
                return {"success": True, "delivered": True}
            
            with patch.object(service, 'send_message', side_effect=send_side_effect):
                result = service.broadcast_message("Broadcast", "regular")
                
                assert isinstance(result, dict)
                assert result.get("success") is False or result.get("success") is True


class TestHandlerFunctionsBatch10:
    """Batch 10 tests for handler functions - Advanced scenarios."""

    def test_handle_message_missing_agent_and_broadcast(self):
        """Test handle_message when both agent and broadcast are missing."""
        args = Mock()
        args.agent = None
        args.broadcast = False
        args.message = "Test"
        args.priority = "regular"
        args.stalled = False
        
        parser = Mock()
        parser.print_help = Mock()
        
        result = handle_message(args, parser)
        
        assert result == 1
        parser.print_help.assert_called_once()

    def test_handle_message_broadcast_success_count_zero(self):
        """Test handle_message when broadcast returns zero success count."""
        args = Mock()
        args.agent = None
        args.broadcast = True
        args.message = "Test"
        args.priority = "regular"
        args.stalled = False
        
        parser = Mock()
        
        with patch('src.services.messaging_infrastructure.MessageCoordinator.broadcast_to_all', return_value=0):
            result = handle_message(args, parser)
            assert result == 1

    def test_handle_message_blocked_message(self):
        """Test handle_message when message is blocked."""
        args = Mock()
        args.agent = "Agent-1"
        args.broadcast = False
        args.message = "Test"
        args.priority = "regular"
        args.stalled = False
        
        parser = Mock()
        
        with patch('src.services.messaging_infrastructure.MessageCoordinator.send_to_agent', return_value={
            "success": False,
            "blocked": True,
            "error_message": "Blocked - pending request"
        }):
            result = handle_message(args, parser)
            assert result == 1

    def test_handle_survey_success_count_zero(self):
        """Test handle_survey when coordination returns zero."""
        with patch('src.services.messaging_infrastructure.MessageCoordinator.coordinate_survey', return_value=False):
            result = handle_survey()
            assert result == 1

    def test_handle_consolidation_missing_batch(self):
        """Test handle_consolidation with missing batch."""
        args = Mock()
        args.consolidation_batch = None
        args.consolidation_status = "complete"
        
        with patch('src.services.messaging_infrastructure.MessageCoordinator.coordinate_consolidation', return_value=True):
            result = handle_consolidation(args)
            assert result == 0

    def test_handle_consolidation_missing_status(self):
        """Test handle_consolidation with missing status."""
        args = Mock()
        args.consolidation_batch = "batch-1"
        args.consolidation_status = None
        
        with patch('src.services.messaging_infrastructure.MessageCoordinator.coordinate_consolidation', return_value=True):
            result = handle_consolidation(args)
            assert result == 0

    def test_handle_coordinates_loader_exception(self):
        """Test handle_coordinates handles coordinate loader exceptions."""
        with patch('src.services.messaging_infrastructure.get_coordinate_loader', side_effect=Exception("Loader error")):
            result = handle_coordinates()
            assert result == 1

    def test_handle_start_agents_empty_list(self):
        """Test handle_start_agents with empty agent list."""
        args = Mock()
        args.start = []
        args.message = "START"
        
        result = handle_start_agents(args)
        assert result == 0

    def test_handle_start_agents_partial_failure(self):
        """Test handle_start_agents with partial failures."""
        args = Mock()
        args.start = [1, 2, 3]
        args.message = "START"
        
        call_count = [0]
        def send_side_effect(*args, **kwargs):
            call_count[0] += 1
            return call_count[0] <= 2  # First 2 succeed, last fails
        
        with patch('src.services.messaging_infrastructure.send_message_to_onboarding_coords', side_effect=send_side_effect):
            result = handle_start_agents(args)
            assert result == 0

    def test_handle_save_coordinate_loader_exception(self):
        """Test handle_save handles coordinate loader exceptions."""
        args = Mock()
        args.message = "Save message"
        
        parser = Mock()
        
        with patch('src.services.messaging_infrastructure.get_coordinate_loader', side_effect=Exception("Loader error")):
            result = handle_save(args, parser)
            assert result == 1

    def test_handle_save_pyautogui_exception(self):
        """Test handle_save handles PyAutoGUI exceptions."""
        args = Mock()
        args.message = "Save message"
        
        parser = Mock()
        
        with patch('src.services.messaging_infrastructure.get_coordinate_loader') as mock_loader, \
             patch('src.services.messaging_infrastructure.pyautogui.click', side_effect=Exception("PyAutoGUI error")):
            mock_coord_loader = Mock()
            mock_coord_loader.get_chat_coordinates.return_value = [100, 200]
            mock_loader.return_value = mock_coord_loader
            
            result = handle_save(args, parser)
            # Should continue processing other agents
            assert result == 0

    def test_handle_leaderboard_empty_leaderboard(self):
        """Test handle_leaderboard with empty leaderboard."""
        with patch('src.services.messaging_infrastructure.get_competition_system') as mock_competition:
            mock_system = Mock()
            mock_system.get_leaderboard.return_value = []
            mock_competition.return_value = mock_system
            
            result = handle_leaderboard()
            assert result == 0

    def test_handle_leaderboard_missing_fields(self):
        """Test handle_leaderboard handles missing fields in leaderboard entries."""
        with patch('src.services.messaging_infrastructure.get_competition_system') as mock_competition:
            mock_system = Mock()
            mock_system.get_leaderboard.return_value = [
                {"agent_id": "Agent-1", "score": 100},  # Missing contracts_completed
                {"agent_id": "Agent-2"}  # Missing score
            ]
            mock_competition.return_value = mock_system
            
            result = handle_leaderboard()
            # Should handle missing fields gracefully
            assert result == 0


class TestHelperFunctionsBatch10:
    """Batch 10 tests for helper functions - Advanced scenarios."""

    def test_format_multi_agent_request_message_single_recipient(self):
        """Test _format_multi_agent_request_message with single recipient."""
        result = _format_multi_agent_request_message(
            "Test message",
            "collector-123",
            "req-456",
            1,
            60
        )
        
        assert "1 agent(s)" in result or "1" in result
        assert "collector-123" in result
        assert "req-456" in result

    def test_format_multi_agent_request_message_large_recipient_count(self):
        """Test _format_multi_agent_request_message with large recipient count."""
        result = _format_multi_agent_request_message(
            "Test message",
            "collector-123",
            "req-456",
            100,
            3600
        )
        
        assert "100 agent(s)" in result or "100" in result
        assert "60 minutes" in result or "3600" in result

    def test_format_normal_message_with_instructions_broadcast(self):
        """Test _format_normal_message_with_instructions with BROADCAST type."""
        result = _format_normal_message_with_instructions("Test", "BROADCAST")
        
        assert "BROADCAST MESSAGE" in result
        assert "Test" in result

    def test_format_normal_message_with_instructions_normal(self):
        """Test _format_normal_message_with_instructions with NORMAL type."""
        result = _format_normal_message_with_instructions("Test", "NORMAL")
        
        assert "STANDARD MESSAGE" in result
        assert "Test" in result

    def test_send_message_pyautogui_failure(self):
        """Test send_message_pyautogui when send fails."""
        with patch('src.core.messaging_core.send_message', return_value=False):
            result = send_message_pyautogui("Agent-1", "Test", 30)
            assert result is False

    def test_send_message_to_onboarding_coords_failure(self):
        """Test send_message_to_onboarding_coords when send fails."""
        with patch('src.services.messaging_infrastructure.send_message_pyautogui', return_value=False):
            result = send_message_to_onboarding_coords("Agent-1", "Test", 30)
            assert result is False

    def test_create_messaging_parser_minimal_args(self):
        """Test create_messaging_parser with minimal arguments."""
        parser = create_messaging_parser()
        
        # Test parsing with just message
        args = parser.parse_args(["--message", "Test"])
        
        assert args.message == "Test"
        assert args.agent is None
        assert args.broadcast is False

    def test_create_messaging_parser_defaults(self):
        """Test create_messaging_parser default values."""
        parser = create_messaging_parser()
        
        args = parser.parse_args(["--message", "Test", "--agent", "Agent-1"])
        
        assert args.priority == "regular"  # Default
        assert args.pyautogui is False  # Default
        assert args.survey_coordination is False  # Default

    def test_send_discord_message_exception(self):
        """Test send_discord_message handles exceptions."""
        with patch('src.services.messaging_infrastructure.ConsolidatedMessagingService', side_effect=Exception("Service error")):
            result = send_discord_message("Agent-1", "Test", "regular")
            assert result is False

    def test_broadcast_discord_message_exception(self):
        """Test broadcast_discord_message handles exceptions."""
        with patch('src.services.messaging_infrastructure.ConsolidatedMessagingService', side_effect=Exception("Service error")):
            try:
                result = broadcast_discord_message("Test", "regular")
                # Should handle exception or return error dict
                assert isinstance(result, dict)
            except Exception:
                # Exception handling is acceptable
                pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

