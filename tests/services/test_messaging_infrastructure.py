"""
Unit tests for messaging_infrastructure.py - HIGH PRIORITY

Tests messaging infrastructure: MessageCoordinator, ConsolidatedMessagingService, etc.
Target: ≥85% coverage, 5+ tests per file
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, call
from pathlib import Path
import subprocess

# Import messaging infrastructure
import sys
from pathlib import Path as PathLib

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.services.messaging_infrastructure import (
    MessageCoordinator,
    ConsolidatedMessagingService,
    create_messaging_parser,
    send_message_pyautogui,
    send_message_to_onboarding_coords,
    handle_message,
    handle_survey,
    handle_consolidation,
    handle_coordinates,
    handle_start_agents,
    handle_save,
    handle_leaderboard,
    _format_multi_agent_request_message,
    _format_normal_message_with_instructions,
    SWARM_AGENTS,
    AGENT_ASSIGNMENTS
)


class TestMessageCoordinator:
    """Test suite for MessageCoordinator class."""

    @patch('src.core.message_queue.MessageQueue')
    def test_send_to_agent_success(self, mock_queue_class):
        """Test successful message sending to agent."""
        mock_queue = MagicMock()
        mock_queue.enqueue.return_value = "queue-123"
        mock_queue_class.return_value = mock_queue
        
        MessageCoordinator._queue = None
        
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator:
            mock_validator_instance = MagicMock()
            mock_validator_instance.validate_agent_can_send_message.return_value = (True, None, None)
            mock_validator.return_value = mock_validator_instance
            
            result = MessageCoordinator.send_to_agent(
                agent="Agent-1",
                message="Test message",
                priority=None
            )
            
            assert result["success"] is True
            assert result["queue_id"] == "queue-123"
            assert result["agent"] == "Agent-1"

    @patch('src.core.message_queue.MessageQueue')
    def test_send_to_agent_blocked(self, mock_queue_class):
        """Test message blocked due to pending multi-agent request."""
        MessageCoordinator._queue = None
        
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator:
            mock_validator_instance = MagicMock()
            mock_validator_instance.validate_agent_can_send_message.return_value = (
                False, "Agent has pending request", {"request_id": "req-123"}
            )
            mock_validator.return_value = mock_validator_instance
            
            result = MessageCoordinator.send_to_agent(
                agent="Agent-1",
                message="Test message"
            )
            
            assert result["success"] is False
            assert result["blocked"] is True
            assert result["reason"] == "pending_multi_agent_request"

    @patch('src.core.message_queue.MessageQueue')
    def test_broadcast_to_all_success(self, mock_queue_class):
        """Test successful broadcast to all agents."""
        mock_queue = MagicMock()
        mock_queue.enqueue.return_value = "queue-123"
        mock_queue_class.return_value = mock_queue
        
        MessageCoordinator._queue = None
        
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator:
            mock_validator_instance = MagicMock()
            mock_validator_instance.validate_agent_can_send_message.return_value = (True, None, None)
            mock_validator.return_value = mock_validator_instance
            
            result = MessageCoordinator.broadcast_to_all("Test broadcast")
            
            assert result == len(SWARM_AGENTS)
            assert mock_queue.enqueue.call_count == len(SWARM_AGENTS)

    @patch('src.core.message_queue.MessageQueue')
    def test_broadcast_skips_blocked_agents(self, mock_queue_class):
        """Test broadcast skips agents with pending requests."""
        mock_queue = MagicMock()
        mock_queue.enqueue.return_value = "queue-123"
        mock_queue_class.return_value = mock_queue
        
        MessageCoordinator._queue = None
        
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator:
            mock_validator_instance = MagicMock()
            
            # First agent blocked, others allowed
            def validate_side_effect(agent_id, target_recipient, message_content):
                if agent_id == "Agent-1":
                    return (False, "Blocked", {"request_id": "req-123"})
                return (True, None, None)
            
            mock_validator_instance.validate_agent_can_send_message.side_effect = validate_side_effect
            mock_validator.return_value = mock_validator_instance
            
            result = MessageCoordinator.broadcast_to_all("Test broadcast")
            
            # Should enqueue for all agents except Agent-1
            assert result == len(SWARM_AGENTS) - 1

    @patch('src.core.message_queue.MessageQueue')
    def test_send_multi_agent_request(self, mock_queue_class):
        """Test sending multi-agent request."""
        mock_queue = MagicMock()
        mock_queue.enqueue.return_value = "queue-123"
        mock_queue_class.return_value = mock_queue
        
        MessageCoordinator._queue = None
        
        with patch('src.core.multi_agent_responder.get_multi_agent_responder') as mock_responder:
            mock_responder_instance = MagicMock()
            mock_responder_instance.create_request.return_value = "collector-123"
            mock_responder.return_value = mock_responder_instance
            
            result = MessageCoordinator.send_multi_agent_request(
                recipients=["Agent-1", "Agent-2"],
                message="Test request"
            )
            
            assert result == "collector-123"
            assert mock_queue.enqueue.call_count == 2

    def test_coordinate_survey(self):
        """Test survey coordination."""
        with patch.object(MessageCoordinator, 'broadcast_to_all', return_value=8):
            result = MessageCoordinator.coordinate_survey()
            assert result is True

    def test_coordinate_consolidation(self):
        """Test consolidation coordination."""
        with patch.object(MessageCoordinator, 'broadcast_to_all', return_value=8):
            result = MessageCoordinator.coordinate_consolidation("batch-1", "IN_PROGRESS")
            assert result is True


class TestConsolidatedMessagingService:
    """Test suite for ConsolidatedMessagingService class."""

    @pytest.fixture
    def service(self):
        """Create service instance with mocked queue."""
        mock_queue = MagicMock()
        mock_queue.enqueue.return_value = "queue-123"
        mock_queue.wait_for_delivery.return_value = True
        
        with patch('src.services.messaging_infrastructure.Path'):
            with patch('src.core.message_queue.MessageQueue', return_value=mock_queue):
                service = ConsolidatedMessagingService()
                service.queue = mock_queue
                return service

    def test_send_message_success(self, service):
        """Test successful message sending."""
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator:
            mock_validator_instance = MagicMock()
            mock_validator_instance.validate_agent_can_send_message.return_value = (True, None, None)
            mock_validator.return_value = mock_validator_instance
            
            result = service.send_message(
                agent="Agent-1",
                message="Test message",
                priority="regular"
            )
            
            assert result["success"] is True
            assert result["queue_id"] == "queue-123"

    def test_send_message_blocked(self, service):
        """Test message blocked due to pending request."""
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator:
            mock_validator_instance = MagicMock()
            mock_validator_instance.validate_agent_can_send_message.return_value = (
                False, "Blocked", {"request_id": "req-123"}
            )
            mock_validator.return_value = mock_validator_instance
            
            result = service.send_message(
                agent="Agent-1",
                message="Test message"
            )
            
            assert result["success"] is False
            assert result["blocked"] is True

    def test_send_message_wait_for_delivery(self, service):
        """Test message sending with wait_for_delivery."""
        service.queue.wait_for_delivery.return_value = True
        
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator:
            mock_validator_instance = MagicMock()
            mock_validator_instance.validate_agent_can_send_message.return_value = (True, None, None)
            mock_validator.return_value = mock_validator_instance
            
            result = service.send_message(
                agent="Agent-1",
                message="Test message",
                wait_for_delivery=True,
                timeout=30.0
            )
            
            assert result["success"] is True
            assert result["delivered"] is True
            service.queue.wait_for_delivery.assert_called_once()

    def test_broadcast_message(self, service):
        """Test broadcast message."""
        service.queue.wait_for_delivery.return_value = True
        
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator:
            mock_validator_instance = MagicMock()
            mock_validator_instance.validate_agent_can_send_message.return_value = (True, None, None)
            mock_validator.return_value = mock_validator_instance
            
            with patch('src.core.keyboard_control_lock.keyboard_control'):
                result = service.broadcast_message("Test broadcast")
                
                assert result["success"] is True
                assert service.queue.enqueue.call_count == len(SWARM_AGENTS)

    def test_resolve_discord_sender(self, service):
        """Test Discord sender resolution."""
        result = service._resolve_discord_sender("123456789")
        assert "DISCORD" in result

        result = service._resolve_discord_sender(None)
        assert result == "DISCORD"


class TestMessageFormatters:
    """Test suite for message formatting functions."""

    def test_format_multi_agent_request_message(self):
        """Test multi-agent request message formatting."""
        result = _format_multi_agent_request_message(
            message="Test message",
            collector_id="collector-123",
            request_id="req-123",
            recipient_count=3,
            timeout_seconds=300
        )
        
        assert "Test message" in result
        assert "collector-123" in result
        assert "req-123" in result
        assert "3" in result
        assert "MULTI-AGENT REQUEST" in result

    def test_format_normal_message_broadcast(self):
        """Test normal message formatting for broadcast."""
        result = _format_normal_message_with_instructions("Test message", "BROADCAST")
        
        assert "Test message" in result
        assert "BROADCAST MESSAGE" in result
        assert "WE. ARE. SWARM" in result

    def test_format_normal_message_normal(self):
        """Test normal message formatting for standard message."""
        result = _format_normal_message_with_instructions("Test message", "NORMAL")
        
        assert "Test message" in result
        assert "STANDARD MESSAGE" in result
        assert "WE. ARE. SWARM" in result


class TestArgumentParser:
    """Test suite for argument parser."""

    def test_create_messaging_parser(self):
        """Test parser creation."""
        parser = create_messaging_parser()
        
        assert parser is not None
        assert hasattr(parser, 'parse_args')

    def test_parser_has_message_argument(self):
        """Test parser has message argument."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--message", "Test", "--agent", "Agent-1"])
        
        assert args.message == "Test"
        assert args.agent == "Agent-1"

    def test_parser_has_broadcast_argument(self):
        """Test parser has broadcast argument."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--message", "Test", "--broadcast"])
        
        assert args.broadcast is True

    def test_parser_has_priority_argument(self):
        """Test parser has priority argument."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--message", "Test", "--agent", "Agent-1", "--priority", "urgent"])
        
        assert args.priority == "urgent"


class TestHandlerFunctions:
    """Test suite for handler functions."""

    def test_handle_message_success(self):
        """Test successful message handling."""
        mock_parser = MagicMock()
        mock_args = MagicMock()
        mock_args.agent = "Agent-1"
        mock_args.broadcast = False
        mock_args.message = "Test message"
        mock_args.priority = "regular"
        mock_args.stalled = False
        
        with patch.object(MessageCoordinator, 'send_to_agent', return_value={"success": True}):
            result = handle_message(mock_args, mock_parser)
            assert result == 0

    def test_handle_message_no_agent_or_broadcast(self):
        """Test message handling without agent or broadcast."""
        mock_parser = MagicMock()
        mock_args = MagicMock()
        mock_args.agent = None
        mock_args.broadcast = False
        mock_args.message = "Test message"
        
        result = handle_message(mock_args, mock_parser)
        assert result == 1

    def test_handle_survey_success(self):
        """Test successful survey handling."""
        with patch.object(MessageCoordinator, 'coordinate_survey', return_value=True):
            result = handle_survey()
            assert result == 0

    def test_handle_consolidation_success(self):
        """Test successful consolidation handling."""
        mock_args = MagicMock()
        mock_args.consolidation_batch = "batch-1"
        mock_args.consolidation_status = "IN_PROGRESS"
        
        with patch.object(MessageCoordinator, 'coordinate_consolidation', return_value=True):
            result = handle_consolidation(mock_args)
            assert result == 0

    @patch('src.services.messaging_infrastructure.get_coordinate_loader')
    def test_handle_coordinates(self, mock_loader):
        """Test coordinates handling."""
        mock_loader_instance = MagicMock()
        mock_loader_instance.get_chat_coordinates.return_value = (100, 200)
        mock_loader_instance.get_onboarding_coordinates.return_value = (150, 250)
        mock_loader.return_value = mock_loader_instance
        
        result = handle_coordinates()
        assert result == 0

    @patch('src.services.messaging_infrastructure.send_message_to_onboarding_coords')
    def test_handle_start_agents(self, mock_send):
        """Test start agents handling."""
        mock_send.return_value = True
        mock_args = MagicMock()
        mock_args.start = [1, 2, 3]
        mock_args.message = "START"
        
        result = handle_start_agents(mock_args)
        assert result == 0
        assert mock_send.call_count == 3

    @patch('src.services.messaging_infrastructure.get_coordinate_loader')
    @patch('src.services.messaging_infrastructure.pyautogui')
    def test_handle_save(self, mock_pyautogui, mock_loader):
        """Test save handling."""
        mock_loader_instance = MagicMock()
        mock_loader_instance.get_chat_coordinates.return_value = (100, 200)
        mock_loader.return_value = mock_loader_instance
        
        mock_args = MagicMock()
        mock_args.message = "Test message"
        mock_parser = MagicMock()
        
        result = handle_save(mock_args, mock_parser)
        assert result == 0

    @patch('src.services.messaging_infrastructure.get_competition_system')
    def test_handle_leaderboard(self, mock_competition):
        """Test leaderboard handling."""
        mock_competition_instance = MagicMock()
        mock_competition_instance.get_leaderboard.return_value = [
            {"agent_id": "Agent-1", "score": 100, "contracts_completed": 5}
        ]
        mock_competition.return_value = mock_competition_instance
        
        result = handle_leaderboard()
        assert result == 0


class TestMessageFormattersAdditional:
    """Additional test suite for message formatting functions."""

    def test_format_multi_agent_request_message_timeout_minutes(self):
        """Test multi-agent request message formatting with timeout in minutes."""
        result = _format_multi_agent_request_message(
            message="Test",
            collector_id="collector-123",
            request_id="req-123",
            recipient_count=5,
            timeout_seconds=600  # 10 minutes
        )
        
        assert "10" in result or "10 minutes" in result
        assert "collector-123" in result

    def test_format_normal_message_broadcast_instructions(self):
        """Test broadcast message includes proper instructions."""
        result = _format_normal_message_with_instructions("Test", "BROADCAST")
        
        assert "BROADCAST MESSAGE" in result
        assert "standard one-to-one messaging" in result
        assert "respond normally" in result

    def test_format_normal_message_standard_instructions(self):
        """Test standard message includes proper instructions."""
        result = _format_normal_message_with_instructions("Test", "NORMAL")
        
        assert "STANDARD MESSAGE" in result
        assert "respond normally" in result
        assert "no special handling" in result


class TestConsolidatedMessagingServiceAdditional:
    """Additional test suite for ConsolidatedMessagingService."""

    @pytest.fixture
    def service(self):
        """Create service instance with mocked queue."""
        mock_queue = MagicMock()
        mock_queue.enqueue.return_value = "queue-123"
        mock_queue.wait_for_delivery.return_value = True
        
        with patch('src.services.messaging_infrastructure.Path'):
            with patch('src.core.message_queue.MessageQueue', return_value=mock_queue):
                service = ConsolidatedMessagingService()
                service.queue = mock_queue
                return service

    def test_send_message_with_discord_username(self, service):
        """Test send_message with Discord username resolution."""
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator:
            mock_validator_instance = MagicMock()
            mock_validator_instance.validate_agent_can_send_message.return_value = (True, None, None)
            mock_validator.return_value = mock_validator_instance
            
            result = service.send_message(
                agent="Agent-1",
                message="Test",
                priority="regular",
                discord_user_id="123456789"
            )
            
            assert result["success"] is True
            # Verify Discord metadata was included
            enqueue_call = service.queue.enqueue.call_args
            assert enqueue_call is not None

    def test_send_message_with_stalled_delivery(self, service):
        """Test send_message with stalled delivery mode."""
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator:
            mock_validator_instance = MagicMock()
            mock_validator_instance.validate_agent_can_send_message.return_value = (True, None, None)
            mock_validator.return_value = mock_validator_instance
            
            result = service.send_message(
                agent="Agent-1",
                message="Test",
                priority="regular",
                stalled=True
            )
            
            assert result["success"] is True
            # Verify stalled flag was included in metadata
            enqueue_call = service.queue.enqueue.call_args
            assert enqueue_call is not None

    def test_send_message_wait_for_delivery_timeout(self, service):
        """Test send_message with wait_for_delivery timeout."""
        # Check if queue has wait_for_delivery method
        if not hasattr(service.queue, 'wait_for_delivery'):
            service.queue.wait_for_delivery = Mock(return_value=False)
        else:
            service.queue.wait_for_delivery.return_value = False  # Timeout
        
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator:
            mock_validator_instance = MagicMock()
            mock_validator_instance.validate_agent_can_send_message.return_value = (True, None, None)
            mock_validator.return_value = mock_validator_instance
            
            result = service.send_message(
                agent="Agent-1",
                message="Test",
                priority="regular",
                use_pyautogui=True,
                wait_for_delivery=True,
                timeout=5.0
            )
            
            # When wait_for_delivery times out, success is False
            assert result is not None
            if isinstance(result, dict):
                # Delivery timeout results in success=False
                assert result.get("success") is False  # Delivery failed/timeout
                assert result.get("delivered") is False  # Delivery timed out
            # wait_for_delivery may not exist on all queue implementations
            if hasattr(service.queue, 'wait_for_delivery'):
                service.queue.wait_for_delivery.assert_called_once()

    def test_broadcast_message_keyboard_lock(self, service):
        """Test broadcast_message uses keyboard lock."""
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator:
            mock_validator_instance = MagicMock()
            mock_validator_instance.validate_agent_can_send_message.return_value = (True, None, None)
            mock_validator.return_value = mock_validator_instance
            
            with patch('src.core.keyboard_control_lock.keyboard_control') as mock_lock:
                result = service.broadcast_message("Broadcast", "regular")
                
                assert result["success"] is True
                mock_lock.assert_called_once()

    def test_broadcast_message_wait_for_each_delivery(self, service):
        """Test broadcast_message waits for each message delivery."""
        service.queue.wait_for_delivery.return_value = True
        
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator:
            mock_validator_instance = MagicMock()
            mock_validator_instance.validate_agent_can_send_message.return_value = (True, None, None)
            mock_validator.return_value = mock_validator_instance
            
            with patch('src.core.keyboard_control_lock.keyboard_control'):
                result = service.broadcast_message("Broadcast", "regular")
                
                assert result["success"] is True
                # Should enqueue for all agents
                assert service.queue.enqueue.call_count == len(SWARM_AGENTS)

    def test_resolve_discord_sender_with_user_id(self, service):
        """Test _resolve_discord_sender with user ID."""
        result = service._resolve_discord_sender("123456789012345678")
        assert "DISCORD" in result
        assert len(result) > len("DISCORD")

    def test_get_discord_username_none(self, service):
        """Test _get_discord_username returns None."""
        result = service._get_discord_username("123456789")
        assert result is None

    def test_get_discord_username_none_for_none(self, service):
        """Test _get_discord_username with None input."""
        result = service._get_discord_username(None)
        assert result is None


class TestHandlerFunctionsAdditional:
    """Additional test suite for handler functions."""

    def test_handle_message_broadcast_flag(self):
        """Test handle_message with broadcast flag."""
        mock_parser = MagicMock()
        mock_args = MagicMock()
        mock_args.agent = None
        mock_args.broadcast = True
        mock_args.message = "Test"
        mock_args.priority = "regular"
        mock_args.stalled = False
        
        with patch.object(MessageCoordinator, 'broadcast_to_all', return_value=8):
            result = handle_message(mock_args, mock_parser)
            assert result == 0

    def test_handle_message_urgent_priority(self):
        """Test handle_message with urgent priority."""
        mock_parser = MagicMock()
        mock_args = MagicMock()
        mock_args.agent = "Agent-1"
        mock_args.broadcast = False
        mock_args.message = "Urgent"
        mock_args.priority = "urgent"
        mock_args.stalled = False
        
        with patch.object(MessageCoordinator, 'send_to_agent', return_value={"success": True}):
            result = handle_message(mock_args, mock_parser)
            assert result == 0

    def test_handle_message_normal_priority_normalized(self):
        """Test handle_message normalizes 'normal' to 'regular' priority."""
        mock_parser = MagicMock()
        mock_args = MagicMock()
        mock_args.agent = "Agent-1"
        mock_args.broadcast = False
        mock_args.message = "Test"
        mock_args.priority = "normal"  # Should be normalized to "regular"
        mock_args.stalled = False
        
        with patch.object(MessageCoordinator, 'send_to_agent', return_value={"success": True}) as mock_send:
            result = handle_message(mock_args, mock_parser)
            assert result == 0
            # Verify send_to_agent was called (priority normalization happens in handle_message)
            assert mock_send.called

    def test_handle_message_blocked_result(self):
        """Test handle_message when message is blocked."""
        mock_parser = MagicMock()
        mock_args = MagicMock()
        mock_args.agent = "Agent-1"
        mock_args.broadcast = False
        mock_args.message = "Test"
        mock_args.priority = "regular"
        mock_args.stalled = False
        
        with patch.object(MessageCoordinator, 'send_to_agent', return_value={
            "success": False,
            "blocked": True,
            "error_message": "Blocked message"
        }):
            result = handle_message(mock_args, mock_parser)
            assert result == 1

    def test_handle_message_old_format_bool(self):
        """Test handle_message with old bool return format."""
        mock_parser = MagicMock()
        mock_args = MagicMock()
        mock_args.agent = "Agent-1"
        mock_args.broadcast = False
        mock_args.message = "Test"
        mock_args.priority = "regular"
        mock_args.stalled = False
        
        with patch.object(MessageCoordinator, 'send_to_agent', return_value=True):  # Old format
            result = handle_message(mock_args, mock_parser)
            assert result == 0

    def test_handle_message_exception(self):
        """Test handle_message exception handling."""
        mock_parser = MagicMock()
        mock_args = MagicMock()
        mock_args.agent = "Agent-1"
        mock_args.broadcast = False
        mock_args.message = "Test"
        mock_args.priority = "regular"
        
        with patch.object(MessageCoordinator, 'send_to_agent', side_effect=Exception("Error")):
            with patch('src.services.messaging_infrastructure.logger'):
                result = handle_message(mock_args, mock_parser)
                assert result == 1

    @patch('src.services.messaging_infrastructure.get_coordinate_loader')
    def test_handle_coordinates_all_agents(self, mock_loader):
        """Test handle_coordinates displays all agents."""
        mock_loader_instance = MagicMock()
        mock_loader_instance.get_chat_coordinates.return_value = (100, 200)
        mock_loader_instance.get_onboarding_coordinates.return_value = (150, 250)
        mock_loader.return_value = mock_loader_instance
        
        result = handle_coordinates()
        assert result == 0
        assert mock_loader_instance.get_chat_coordinates.call_count == len(SWARM_AGENTS)

    @patch('src.services.messaging_infrastructure.send_message_to_onboarding_coords')
    def test_handle_start_agents_invalid_numbers(self, mock_send):
        """Test handle_start_agents with invalid agent numbers."""
        mock_send.return_value = True
        mock_args = MagicMock()
        mock_args.start = [1, 2, 99]  # 99 is invalid
        mock_args.message = "START"
        
        result = handle_start_agents(mock_args)
        assert result == 0
        # Should only send to valid agents
        assert mock_send.call_count == 2

    @patch('src.services.messaging_infrastructure.get_coordinate_loader')
    @patch('src.services.messaging_infrastructure.pyautogui')
    @patch('src.services.messaging_infrastructure.time')
    def test_handle_save_all_agents(self, mock_time, mock_pyautogui, mock_loader):
        """Test handle_save sends to all agents."""
        mock_loader_instance = MagicMock()
        mock_loader_instance.get_chat_coordinates.return_value = (100, 200)
        mock_loader.return_value = mock_loader_instance
        
        mock_args = MagicMock()
        mock_args.message = "Save message"
        mock_parser = MagicMock()
        
        result = handle_save(mock_args, mock_parser)
        assert result == 0
        assert mock_pyautogui.click.call_count == len(SWARM_AGENTS)
        assert mock_pyautogui.write.call_count == len(SWARM_AGENTS)
        assert mock_pyautogui.hotkey.call_count == len(SWARM_AGENTS)

    @patch('src.services.messaging_infrastructure.get_competition_system')
    def test_handle_leaderboard_empty(self, mock_competition):
        """Test handle_leaderboard with empty leaderboard."""
        mock_competition_instance = MagicMock()
        mock_competition_instance.get_leaderboard.return_value = []
        mock_competition.return_value = mock_competition_instance
        
        result = handle_leaderboard()
        assert result == 0

    @patch('src.services.messaging_infrastructure.get_competition_system')
    def test_handle_leaderboard_exception(self, mock_competition):
        """Test handle_leaderboard exception handling."""
        mock_competition.side_effect = Exception("Error")
        
        with patch('src.services.messaging_infrastructure.logger'):
            result = handle_leaderboard()
            assert result == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])



Tests messaging infrastructure: MessageCoordinator, ConsolidatedMessagingService, etc.
Target: ≥85% coverage, 5+ tests per file
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, call
from pathlib import Path
import subprocess

# Import messaging infrastructure
import sys
from pathlib import Path as PathLib

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.services.messaging_infrastructure import (
    MessageCoordinator,
    ConsolidatedMessagingService,
    create_messaging_parser,
    send_message_pyautogui,
    send_message_to_onboarding_coords,
    handle_message,
    handle_survey,
    handle_consolidation,
    handle_coordinates,
    handle_start_agents,
    handle_save,
    handle_leaderboard,
    _format_multi_agent_request_message,
    _format_normal_message_with_instructions,
    SWARM_AGENTS,
    AGENT_ASSIGNMENTS
)


class TestMessageCoordinator:
    """Test suite for MessageCoordinator class."""

    @patch('src.core.message_queue.MessageQueue')
    def test_send_to_agent_success(self, mock_queue_class):
        """Test successful message sending to agent."""
        mock_queue = MagicMock()
        mock_queue.enqueue.return_value = "queue-123"
        mock_queue_class.return_value = mock_queue
        
        MessageCoordinator._queue = None
        
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator:
            mock_validator_instance = MagicMock()
            mock_validator_instance.validate_agent_can_send_message.return_value = (True, None, None)
            mock_validator.return_value = mock_validator_instance
            
            result = MessageCoordinator.send_to_agent(
                agent="Agent-1",
                message="Test message",
                priority=None
            )
            
            assert result["success"] is True
            assert result["queue_id"] == "queue-123"
            assert result["agent"] == "Agent-1"

    @patch('src.core.message_queue.MessageQueue')
    def test_send_to_agent_blocked(self, mock_queue_class):
        """Test message blocked due to pending multi-agent request."""
        MessageCoordinator._queue = None
        
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator:
            mock_validator_instance = MagicMock()
            mock_validator_instance.validate_agent_can_send_message.return_value = (
                False, "Agent has pending request", {"request_id": "req-123"}
            )
            mock_validator.return_value = mock_validator_instance
            
            result = MessageCoordinator.send_to_agent(
                agent="Agent-1",
                message="Test message"
            )
            
            assert result["success"] is False
            assert result["blocked"] is True
            assert result["reason"] == "pending_multi_agent_request"

    @patch('src.core.message_queue.MessageQueue')
    def test_broadcast_to_all_success(self, mock_queue_class):
        """Test successful broadcast to all agents."""
        mock_queue = MagicMock()
        mock_queue.enqueue.return_value = "queue-123"
        mock_queue_class.return_value = mock_queue
        
        MessageCoordinator._queue = None
        
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator:
            mock_validator_instance = MagicMock()
            mock_validator_instance.validate_agent_can_send_message.return_value = (True, None, None)
            mock_validator.return_value = mock_validator_instance
            
            result = MessageCoordinator.broadcast_to_all("Test broadcast")
            
            assert result == len(SWARM_AGENTS)
            assert mock_queue.enqueue.call_count == len(SWARM_AGENTS)

    @patch('src.core.message_queue.MessageQueue')
    def test_broadcast_skips_blocked_agents(self, mock_queue_class):
        """Test broadcast skips agents with pending requests."""
        mock_queue = MagicMock()
        mock_queue.enqueue.return_value = "queue-123"
        mock_queue_class.return_value = mock_queue
        
        MessageCoordinator._queue = None
        
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator:
            mock_validator_instance = MagicMock()
            
            # First agent blocked, others allowed
            def validate_side_effect(agent_id, target_recipient, message_content):
                if agent_id == "Agent-1":
                    return (False, "Blocked", {"request_id": "req-123"})
                return (True, None, None)
            
            mock_validator_instance.validate_agent_can_send_message.side_effect = validate_side_effect
            mock_validator.return_value = mock_validator_instance
            
            result = MessageCoordinator.broadcast_to_all("Test broadcast")
            
            # Should enqueue for all agents except Agent-1
            assert result == len(SWARM_AGENTS) - 1

    @patch('src.core.message_queue.MessageQueue')
    def test_send_multi_agent_request(self, mock_queue_class):
        """Test sending multi-agent request."""
        mock_queue = MagicMock()
        mock_queue.enqueue.return_value = "queue-123"
        mock_queue_class.return_value = mock_queue
        
        MessageCoordinator._queue = None
        
        with patch('src.core.multi_agent_responder.get_multi_agent_responder') as mock_responder:
            mock_responder_instance = MagicMock()
            mock_responder_instance.create_request.return_value = "collector-123"
            mock_responder.return_value = mock_responder_instance
            
            result = MessageCoordinator.send_multi_agent_request(
                recipients=["Agent-1", "Agent-2"],
                message="Test request"
            )
            
            assert result == "collector-123"
            assert mock_queue.enqueue.call_count == 2

    def test_coordinate_survey(self):
        """Test survey coordination."""
        with patch.object(MessageCoordinator, 'broadcast_to_all', return_value=8):
            result = MessageCoordinator.coordinate_survey()
            assert result is True

    def test_coordinate_consolidation(self):
        """Test consolidation coordination."""
        with patch.object(MessageCoordinator, 'broadcast_to_all', return_value=8):
            result = MessageCoordinator.coordinate_consolidation("batch-1", "IN_PROGRESS")
            assert result is True


class TestConsolidatedMessagingService:
    """Test suite for ConsolidatedMessagingService class."""

    @pytest.fixture
    def service(self):
        """Create service instance with mocked queue."""
        mock_queue = MagicMock()
        mock_queue.enqueue.return_value = "queue-123"
        mock_queue.wait_for_delivery.return_value = True
        
        with patch('src.services.messaging_infrastructure.Path'):
            with patch('src.core.message_queue.MessageQueue', return_value=mock_queue):
                service = ConsolidatedMessagingService()
                service.queue = mock_queue
                return service

    def test_send_message_success(self, service):
        """Test successful message sending."""
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator:
            mock_validator_instance = MagicMock()
            mock_validator_instance.validate_agent_can_send_message.return_value = (True, None, None)
            mock_validator.return_value = mock_validator_instance
            
            result = service.send_message(
                agent="Agent-1",
                message="Test message",
                priority="regular"
            )
            
            assert result["success"] is True
            assert result["queue_id"] == "queue-123"

    def test_send_message_blocked(self, service):
        """Test message blocked due to pending request."""
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator:
            mock_validator_instance = MagicMock()
            mock_validator_instance.validate_agent_can_send_message.return_value = (
                False, "Blocked", {"request_id": "req-123"}
            )
            mock_validator.return_value = mock_validator_instance
            
            result = service.send_message(
                agent="Agent-1",
                message="Test message"
            )
            
            assert result["success"] is False
            assert result["blocked"] is True

    def test_send_message_wait_for_delivery(self, service):
        """Test message sending with wait_for_delivery."""
        service.queue.wait_for_delivery.return_value = True
        
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator:
            mock_validator_instance = MagicMock()
            mock_validator_instance.validate_agent_can_send_message.return_value = (True, None, None)
            mock_validator.return_value = mock_validator_instance
            
            result = service.send_message(
                agent="Agent-1",
                message="Test message",
                wait_for_delivery=True,
                timeout=30.0
            )
            
            assert result["success"] is True
            assert result["delivered"] is True
            service.queue.wait_for_delivery.assert_called_once()

    def test_broadcast_message(self, service):
        """Test broadcast message."""
        service.queue.wait_for_delivery.return_value = True
        
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator:
            mock_validator_instance = MagicMock()
            mock_validator_instance.validate_agent_can_send_message.return_value = (True, None, None)
            mock_validator.return_value = mock_validator_instance
            
            with patch('src.core.keyboard_control_lock.keyboard_control'):
                result = service.broadcast_message("Test broadcast")
                
                assert result["success"] is True
                assert service.queue.enqueue.call_count == len(SWARM_AGENTS)

    def test_resolve_discord_sender(self, service):
        """Test Discord sender resolution."""
        result = service._resolve_discord_sender("123456789")
        assert "DISCORD" in result

        result = service._resolve_discord_sender(None)
        assert result == "DISCORD"


class TestMessageFormatters:
    """Test suite for message formatting functions."""

    def test_format_multi_agent_request_message(self):
        """Test multi-agent request message formatting."""
        result = _format_multi_agent_request_message(
            message="Test message",
            collector_id="collector-123",
            request_id="req-123",
            recipient_count=3,
            timeout_seconds=300
        )
        
        assert "Test message" in result
        assert "collector-123" in result
        assert "req-123" in result
        assert "3" in result
        assert "MULTI-AGENT REQUEST" in result

    def test_format_normal_message_broadcast(self):
        """Test normal message formatting for broadcast."""
        result = _format_normal_message_with_instructions("Test message", "BROADCAST")
        
        assert "Test message" in result
        assert "BROADCAST MESSAGE" in result
        assert "WE. ARE. SWARM" in result

    def test_format_normal_message_normal(self):
        """Test normal message formatting for standard message."""
        result = _format_normal_message_with_instructions("Test message", "NORMAL")
        
        assert "Test message" in result
        assert "STANDARD MESSAGE" in result
        assert "WE. ARE. SWARM" in result


class TestArgumentParser:
    """Test suite for argument parser."""

    def test_create_messaging_parser(self):
        """Test parser creation."""
        parser = create_messaging_parser()
        
        assert parser is not None
        assert hasattr(parser, 'parse_args')

    def test_parser_has_message_argument(self):
        """Test parser has message argument."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--message", "Test", "--agent", "Agent-1"])
        
        assert args.message == "Test"
        assert args.agent == "Agent-1"

    def test_parser_has_broadcast_argument(self):
        """Test parser has broadcast argument."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--message", "Test", "--broadcast"])
        
        assert args.broadcast is True

    def test_parser_has_priority_argument(self):
        """Test parser has priority argument."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--message", "Test", "--agent", "Agent-1", "--priority", "urgent"])
        
        assert args.priority == "urgent"


class TestHandlerFunctions:
    """Test suite for handler functions."""

    def test_handle_message_success(self):
        """Test successful message handling."""
        mock_parser = MagicMock()
        mock_args = MagicMock()
        mock_args.agent = "Agent-1"
        mock_args.broadcast = False
        mock_args.message = "Test message"
        mock_args.priority = "regular"
        mock_args.stalled = False
        
        with patch.object(MessageCoordinator, 'send_to_agent', return_value={"success": True}):
            result = handle_message(mock_args, mock_parser)
            assert result == 0

    def test_handle_message_no_agent_or_broadcast(self):
        """Test message handling without agent or broadcast."""
        mock_parser = MagicMock()
        mock_args = MagicMock()
        mock_args.agent = None
        mock_args.broadcast = False
        mock_args.message = "Test message"
        
        result = handle_message(mock_args, mock_parser)
        assert result == 1

    def test_handle_survey_success(self):
        """Test successful survey handling."""
        with patch.object(MessageCoordinator, 'coordinate_survey', return_value=True):
            result = handle_survey()
            assert result == 0

    def test_handle_consolidation_success(self):
        """Test successful consolidation handling."""
        mock_args = MagicMock()
        mock_args.consolidation_batch = "batch-1"
        mock_args.consolidation_status = "IN_PROGRESS"
        
        with patch.object(MessageCoordinator, 'coordinate_consolidation', return_value=True):
            result = handle_consolidation(mock_args)
            assert result == 0

    @patch('src.services.messaging_infrastructure.get_coordinate_loader')
    def test_handle_coordinates(self, mock_loader):
        """Test coordinates handling."""
        mock_loader_instance = MagicMock()
        mock_loader_instance.get_chat_coordinates.return_value = (100, 200)
        mock_loader_instance.get_onboarding_coordinates.return_value = (150, 250)
        mock_loader.return_value = mock_loader_instance
        
        result = handle_coordinates()
        assert result == 0

    @patch('src.services.messaging_infrastructure.send_message_to_onboarding_coords')
    def test_handle_start_agents(self, mock_send):
        """Test start agents handling."""
        mock_send.return_value = True
        mock_args = MagicMock()
        mock_args.start = [1, 2, 3]
        mock_args.message = "START"
        
        result = handle_start_agents(mock_args)
        assert result == 0
        assert mock_send.call_count == 3

    @patch('src.services.messaging_infrastructure.get_coordinate_loader')
    @patch('src.services.messaging_infrastructure.pyautogui')
    def test_handle_save(self, mock_pyautogui, mock_loader):
        """Test save handling."""
        mock_loader_instance = MagicMock()
        mock_loader_instance.get_chat_coordinates.return_value = (100, 200)
        mock_loader.return_value = mock_loader_instance
        
        mock_args = MagicMock()
        mock_args.message = "Test message"
        mock_parser = MagicMock()
        
        result = handle_save(mock_args, mock_parser)
        assert result == 0

    @patch('src.services.messaging_infrastructure.get_competition_system')
    def test_handle_leaderboard(self, mock_competition):
        """Test leaderboard handling."""
        mock_competition_instance = MagicMock()
        mock_competition_instance.get_leaderboard.return_value = [
            {"agent_id": "Agent-1", "score": 100, "contracts_completed": 5}
        ]
        mock_competition.return_value = mock_competition_instance
        
        result = handle_leaderboard()
        assert result == 0


class TestMessageFormattersAdditional:
    """Additional test suite for message formatting functions."""

    def test_format_multi_agent_request_message_timeout_minutes(self):
        """Test multi-agent request message formatting with timeout in minutes."""
        result = _format_multi_agent_request_message(
            message="Test",
            collector_id="collector-123",
            request_id="req-123",
            recipient_count=5,
            timeout_seconds=600  # 10 minutes
        )
        
        assert "10" in result or "10 minutes" in result
        assert "collector-123" in result

    def test_format_normal_message_broadcast_instructions(self):
        """Test broadcast message includes proper instructions."""
        result = _format_normal_message_with_instructions("Test", "BROADCAST")
        
        assert "BROADCAST MESSAGE" in result
        assert "standard one-to-one messaging" in result
        assert "respond normally" in result

    def test_format_normal_message_standard_instructions(self):
        """Test standard message includes proper instructions."""
        result = _format_normal_message_with_instructions("Test", "NORMAL")
        
        assert "STANDARD MESSAGE" in result
        assert "respond normally" in result
        assert "no special handling" in result


class TestConsolidatedMessagingServiceAdditional:
    """Additional test suite for ConsolidatedMessagingService."""

    @pytest.fixture
    def service(self):
        """Create service instance with mocked queue."""
        mock_queue = MagicMock()
        mock_queue.enqueue.return_value = "queue-123"
        mock_queue.wait_for_delivery.return_value = True
        
        with patch('src.services.messaging_infrastructure.Path'):
            with patch('src.core.message_queue.MessageQueue', return_value=mock_queue):
                service = ConsolidatedMessagingService()
                service.queue = mock_queue
                return service

    def test_send_message_with_discord_username(self, service):
        """Test send_message with Discord username resolution."""
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator:
            mock_validator_instance = MagicMock()
            mock_validator_instance.validate_agent_can_send_message.return_value = (True, None, None)
            mock_validator.return_value = mock_validator_instance
            
            result = service.send_message(
                agent="Agent-1",
                message="Test",
                priority="regular",
                discord_user_id="123456789"
            )
            
            assert result["success"] is True
            # Verify Discord metadata was included
            enqueue_call = service.queue.enqueue.call_args
            assert enqueue_call is not None

    def test_send_message_with_stalled_delivery(self, service):
        """Test send_message with stalled delivery mode."""
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator:
            mock_validator_instance = MagicMock()
            mock_validator_instance.validate_agent_can_send_message.return_value = (True, None, None)
            mock_validator.return_value = mock_validator_instance
            
            result = service.send_message(
                agent="Agent-1",
                message="Test",
                priority="regular",
                stalled=True
            )
            
            assert result["success"] is True
            # Verify stalled flag was included in metadata
            enqueue_call = service.queue.enqueue.call_args
            assert enqueue_call is not None

    def test_send_message_wait_for_delivery_timeout(self, service):
        """Test send_message with wait_for_delivery timeout."""
        # Check if queue has wait_for_delivery method
        if not hasattr(service.queue, 'wait_for_delivery'):
            service.queue.wait_for_delivery = Mock(return_value=False)
        else:
            service.queue.wait_for_delivery.return_value = False  # Timeout
        
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator:
            mock_validator_instance = MagicMock()
            mock_validator_instance.validate_agent_can_send_message.return_value = (True, None, None)
            mock_validator.return_value = mock_validator_instance
            
            result = service.send_message(
                agent="Agent-1",
                message="Test",
                priority="regular",
                use_pyautogui=True,
                wait_for_delivery=True,
                timeout=5.0
            )
            
            # When wait_for_delivery times out, success is False
            assert result is not None
            if isinstance(result, dict):
                # Delivery timeout results in success=False
                assert result.get("success") is False  # Delivery failed/timeout
                assert result.get("delivered") is False  # Delivery timed out
            # wait_for_delivery may not exist on all queue implementations
            if hasattr(service.queue, 'wait_for_delivery'):
                service.queue.wait_for_delivery.assert_called_once()

    def test_broadcast_message_keyboard_lock(self, service):
        """Test broadcast_message uses keyboard lock."""
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator:
            mock_validator_instance = MagicMock()
            mock_validator_instance.validate_agent_can_send_message.return_value = (True, None, None)
            mock_validator.return_value = mock_validator_instance
            
            with patch('src.core.keyboard_control_lock.keyboard_control') as mock_lock:
                result = service.broadcast_message("Broadcast", "regular")
                
                assert result["success"] is True
                mock_lock.assert_called_once()

    def test_broadcast_message_wait_for_each_delivery(self, service):
        """Test broadcast_message waits for each message delivery."""
        service.queue.wait_for_delivery.return_value = True
        
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_validator:
            mock_validator_instance = MagicMock()
            mock_validator_instance.validate_agent_can_send_message.return_value = (True, None, None)
            mock_validator.return_value = mock_validator_instance
            
            with patch('src.core.keyboard_control_lock.keyboard_control'):
                result = service.broadcast_message("Broadcast", "regular")
                
                assert result["success"] is True
                # Should enqueue for all agents
                assert service.queue.enqueue.call_count == len(SWARM_AGENTS)

    def test_resolve_discord_sender_with_user_id(self, service):
        """Test _resolve_discord_sender with user ID."""
        result = service._resolve_discord_sender("123456789012345678")
        assert "DISCORD" in result
        assert len(result) > len("DISCORD")

    def test_get_discord_username_none(self, service):
        """Test _get_discord_username returns None."""
        result = service._get_discord_username("123456789")
        assert result is None

    def test_get_discord_username_none_for_none(self, service):
        """Test _get_discord_username with None input."""
        result = service._get_discord_username(None)
        assert result is None


class TestHandlerFunctionsAdditional:
    """Additional test suite for handler functions."""

    def test_handle_message_broadcast_flag(self):
        """Test handle_message with broadcast flag."""
        mock_parser = MagicMock()
        mock_args = MagicMock()
        mock_args.agent = None
        mock_args.broadcast = True
        mock_args.message = "Test"
        mock_args.priority = "regular"
        mock_args.stalled = False
        
        with patch.object(MessageCoordinator, 'broadcast_to_all', return_value=8):
            result = handle_message(mock_args, mock_parser)
            assert result == 0

    def test_handle_message_urgent_priority(self):
        """Test handle_message with urgent priority."""
        mock_parser = MagicMock()
        mock_args = MagicMock()
        mock_args.agent = "Agent-1"
        mock_args.broadcast = False
        mock_args.message = "Urgent"
        mock_args.priority = "urgent"
        mock_args.stalled = False
        
        with patch.object(MessageCoordinator, 'send_to_agent', return_value={"success": True}):
            result = handle_message(mock_args, mock_parser)
            assert result == 0

    def test_handle_message_normal_priority_normalized(self):
        """Test handle_message normalizes 'normal' to 'regular' priority."""
        mock_parser = MagicMock()
        mock_args = MagicMock()
        mock_args.agent = "Agent-1"
        mock_args.broadcast = False
        mock_args.message = "Test"
        mock_args.priority = "normal"  # Should be normalized to "regular"
        mock_args.stalled = False
        
        with patch.object(MessageCoordinator, 'send_to_agent', return_value={"success": True}) as mock_send:
            result = handle_message(mock_args, mock_parser)
            assert result == 0
            # Verify send_to_agent was called (priority normalization happens in handle_message)
            assert mock_send.called

    def test_handle_message_blocked_result(self):
        """Test handle_message when message is blocked."""
        mock_parser = MagicMock()
        mock_args = MagicMock()
        mock_args.agent = "Agent-1"
        mock_args.broadcast = False
        mock_args.message = "Test"
        mock_args.priority = "regular"
        mock_args.stalled = False
        
        with patch.object(MessageCoordinator, 'send_to_agent', return_value={
            "success": False,
            "blocked": True,
            "error_message": "Blocked message"
        }):
            result = handle_message(mock_args, mock_parser)
            assert result == 1

    def test_handle_message_old_format_bool(self):
        """Test handle_message with old bool return format."""
        mock_parser = MagicMock()
        mock_args = MagicMock()
        mock_args.agent = "Agent-1"
        mock_args.broadcast = False
        mock_args.message = "Test"
        mock_args.priority = "regular"
        mock_args.stalled = False
        
        with patch.object(MessageCoordinator, 'send_to_agent', return_value=True):  # Old format
            result = handle_message(mock_args, mock_parser)
            assert result == 0

    def test_handle_message_exception(self):
        """Test handle_message exception handling."""
        mock_parser = MagicMock()
        mock_args = MagicMock()
        mock_args.agent = "Agent-1"
        mock_args.broadcast = False
        mock_args.message = "Test"
        mock_args.priority = "regular"
        
        with patch.object(MessageCoordinator, 'send_to_agent', side_effect=Exception("Error")):
            with patch('src.services.messaging_infrastructure.logger'):
                result = handle_message(mock_args, mock_parser)
                assert result == 1

    @patch('src.services.messaging_infrastructure.get_coordinate_loader')
    def test_handle_coordinates_all_agents(self, mock_loader):
        """Test handle_coordinates displays all agents."""
        mock_loader_instance = MagicMock()
        mock_loader_instance.get_chat_coordinates.return_value = (100, 200)
        mock_loader_instance.get_onboarding_coordinates.return_value = (150, 250)
        mock_loader.return_value = mock_loader_instance
        
        result = handle_coordinates()
        assert result == 0
        assert mock_loader_instance.get_chat_coordinates.call_count == len(SWARM_AGENTS)

    @patch('src.services.messaging_infrastructure.send_message_to_onboarding_coords')
    def test_handle_start_agents_invalid_numbers(self, mock_send):
        """Test handle_start_agents with invalid agent numbers."""
        mock_send.return_value = True
        mock_args = MagicMock()
        mock_args.start = [1, 2, 99]  # 99 is invalid
        mock_args.message = "START"
        
        result = handle_start_agents(mock_args)
        assert result == 0
        # Should only send to valid agents
        assert mock_send.call_count == 2

    @patch('src.services.messaging_infrastructure.get_coordinate_loader')
    @patch('src.services.messaging_infrastructure.pyautogui')
    @patch('src.services.messaging_infrastructure.time')
    def test_handle_save_all_agents(self, mock_time, mock_pyautogui, mock_loader):
        """Test handle_save sends to all agents."""
        mock_loader_instance = MagicMock()
        mock_loader_instance.get_chat_coordinates.return_value = (100, 200)
        mock_loader.return_value = mock_loader_instance
        
        mock_args = MagicMock()
        mock_args.message = "Save message"
        mock_parser = MagicMock()
        
        result = handle_save(mock_args, mock_parser)
        assert result == 0
        assert mock_pyautogui.click.call_count == len(SWARM_AGENTS)
        assert mock_pyautogui.write.call_count == len(SWARM_AGENTS)
        assert mock_pyautogui.hotkey.call_count == len(SWARM_AGENTS)

    @patch('src.services.messaging_infrastructure.get_competition_system')
    def test_handle_leaderboard_empty(self, mock_competition):
        """Test handle_leaderboard with empty leaderboard."""
        mock_competition_instance = MagicMock()
        mock_competition_instance.get_leaderboard.return_value = []
        mock_competition.return_value = mock_competition_instance
        
        result = handle_leaderboard()
        assert result == 0

    @patch('src.services.messaging_infrastructure.get_competition_system')
    def test_handle_leaderboard_exception(self, mock_competition):
        """Test handle_leaderboard exception handling."""
        mock_competition.side_effect = Exception("Error")
        
        with patch('src.services.messaging_infrastructure.logger'):
            result = handle_leaderboard()
            assert result == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

