"""
Tests for messaging_infrastructure.py - ConsolidatedMessagingService and MessageCoordinator.

Target: ≥85% coverage, 15+ tests.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.services.messaging_infrastructure import (
    ConsolidatedMessagingService,
    MessageCoordinator,
    _format_multi_agent_request_message,
    _format_normal_message_with_instructions,
    _apply_template,
    create_messaging_parser,
    send_message_pyautogui,
    send_message_to_onboarding_coords,
)
from src.core.messaging_models_core import (
    MessageCategory,
    UnifiedMessagePriority,
    UnifiedMessageType,
)


class TestConsolidatedMessagingService:
    """Test ConsolidatedMessagingService class."""

    @patch("src.core.message_queue.MessageQueue")
    def test_init(self, mock_queue_class):
        """Test ConsolidatedMessagingService initialization."""
        mock_queue = Mock()
        mock_queue_class.return_value = mock_queue
        service = ConsolidatedMessagingService()
        assert service is not None
        assert service.queue == mock_queue

    @patch("src.core.message_queue.MessageQueue")
    @patch("src.core.multi_agent_request_validator.get_multi_agent_validator")
    def test_send_message_success(self, mock_validator, mock_queue_class):
        """Test successful message sending."""
        mock_queue = Mock()
        mock_queue.enqueue = Mock(return_value="queue_id_123")
        mock_queue_class.return_value = mock_queue
        mock_validator_instance = Mock()
        mock_validator_instance.validate_agent_can_send_message = Mock(
            return_value=(True, None, None))
        mock_validator.return_value = mock_validator_instance

        service = ConsolidatedMessagingService()
        result = service.send_message("Agent-1", "Test message")

        assert result["success"] is True
        assert "queue_id" in result

    @patch("src.core.message_queue.MessageQueue")
    @patch("src.core.multi_agent_request_validator.get_multi_agent_validator")
    def test_send_message_with_priority(self, mock_validator, mock_queue_class):
        """Test message sending with priority."""
        mock_queue = Mock()
        mock_queue.enqueue = Mock(return_value="queue_id_123")
        mock_queue_class.return_value = mock_queue
        mock_validator_instance = Mock()
        mock_validator_instance.validate_agent_can_send_message = Mock(
            return_value=(True, None, None))
        mock_validator.return_value = mock_validator_instance

        service = ConsolidatedMessagingService()
        result = service.send_message("Agent-1", "Test", priority="urgent")

        assert result["success"] is True

    @patch("src.core.message_queue.MessageQueue")
    @patch("src.services.messaging.discord_message_helpers.send_discord_via_queue")
    def test_send_message_blocked(self, mock_send, mock_queue_class):
        """Test message sending when blocked by pending request.

        Note: Blocking logic moved to agent_message_helpers.validate_and_prepare_message.
        Discord flow currently doesn't check blocking - messages go through queue.
        This test verifies the service still sends messages (blocking handled elsewhere).
        """
        mock_queue = Mock()
        mock_queue.enqueue = Mock(return_value="queue_id_123")
        mock_queue_class.return_value = mock_queue
        mock_send.return_value = {"success": True, "queue_id": "queue_id_123"}

        service = ConsolidatedMessagingService()
        result = service.send_message("Agent-1", "Test message")

        # Service sends message successfully (blocking checked in different layer)
        assert result["success"] is True

    @patch("src.core.message_queue.MessageQueue")
    @patch("src.services.messaging.discord_message_helpers.route_discord_delivery")
    def test_send_message_exception(self, mock_route, mock_queue_class):
        """Test message sending with exception."""
        mock_queue = Mock()
        mock_queue_class.return_value = mock_queue
        mock_route.side_effect = Exception("Error")

        service = ConsolidatedMessagingService()
        result = service.send_message("Agent-1", "Test message")

        assert result["success"] is False
        assert "Error" in result.get("message", "")


def test_apply_template_d2a_includes_required_fields():
    """D2A should include interpretation/actions/policy/report/fallback fields."""
    rendered = _apply_template(
        category=MessageCategory.D2A,
        message="Hello from Discord",
        sender="User",
        recipient="Agent-6",
        priority=UnifiedMessagePriority.REGULAR,
        message_id="msg-1",
        extra={"interpretation": "Greet", "actions": "Acknowledge"},
    )
    assert "D2A DISCORD INTAKE" in rendered
    assert "Hello from Discord" in rendered
    assert "Interpretation" in rendered
    assert "Proposed Action" in rendered
    # Response policy/report defaults should be injected
    assert "Preferred Reply Format" in rendered or "Preferred reply format" in rendered
    assert "If clarification needed" in rendered
    assert "python tools/devlog_poster.py --agent Agent-6" in rendered
    assert "#DISCORD #D2A" in rendered


def test_apply_template_a2a_populates_fields():
    """A2A should render ask/context/next_step/fallback without empty placeholders."""
    rendered = _apply_template(
        category=MessageCategory.A2A,
        message="coordination ping",
        sender="Agent-7",
        recipient="Agent-6",
        priority=UnifiedMessagePriority.REGULAR,
        message_id="msg-2",
        extra={
            "ask": "Need verification status",
            "context": "Batch2 DreamVault PRs",
            "next_step": "Confirm merged state",
        },
    )
    assert "[HEADER] A2A COORDINATION" in rendered
    assert "Need verification status" in rendered
    assert "Batch2 DreamVault PRs" in rendered
    assert "Confirm merged state" in rendered

    @patch("src.core.message_queue.MessageQueue")
    @patch("src.core.multi_agent_request_validator.get_multi_agent_validator")
    @patch("src.core.keyboard_control_lock.keyboard_control")
    def test_broadcast_message_success(self, mock_lock, mock_validator, mock_queue_class):
        """Test successful broadcast message."""
        mock_queue = Mock()
        mock_queue.enqueue = Mock(return_value="queue_id_1")
        mock_queue_class.return_value = mock_queue
        mock_validator_instance = Mock()
        mock_validator_instance.validate_agent_can_send_message = Mock(
            return_value=(True, None, None))
        mock_validator.return_value = mock_validator_instance
        mock_lock.return_value.__enter__ = Mock()
        mock_lock.return_value.__exit__ = Mock(return_value=None)

        service = ConsolidatedMessagingService()
        result = service.broadcast_message(
            "Test broadcast", priority="regular")

        assert isinstance(result, dict)
        assert "success" in result or "results" in result

    @patch("src.core.message_queue.MessageQueue")
    @patch("src.core.keyboard_control_lock.keyboard_control")
    def test_broadcast_message_no_queue(self, mock_lock, mock_queue_class):
        """Test broadcast message when queue unavailable."""
        mock_queue_class.return_value = None
        mock_lock.return_value.__enter__ = Mock()
        mock_lock.return_value.__exit__ = Mock(return_value=None)

        service = ConsolidatedMessagingService()
        service.queue = None
        # Mock send_message to return success dict
        with patch.object(service, "send_message", return_value={"success": True, "agent": "Agent-1"}):
            result = service.broadcast_message("Test broadcast")

            assert isinstance(result, dict)


class TestMessageCoordinator:
    """Test MessageCoordinator class."""

    @patch("src.core.message_queue.MessageQueue")
    def test_get_queue_success(self, mock_queue_class):
        """Test successful queue initialization."""
        mock_queue = Mock()
        mock_queue_class.return_value = mock_queue

        MessageCoordinator._queue = None
        result = MessageCoordinator._get_queue()

        assert result == mock_queue

    @patch("src.core.message_queue.MessageQueue")
    def test_get_queue_exception(self, mock_queue_class):
        """Test queue initialization with exception."""
        mock_queue_class.side_effect = Exception("Error")

        MessageCoordinator._queue = None
        result = MessageCoordinator._get_queue()

        assert result is None

    @patch("src.core.message_queue.MessageQueue")
    @patch("src.core.multi_agent_request_validator.get_multi_agent_validator")
    def test_send_to_agent_success(self, mock_validator, mock_queue_class):
        """Test successful send_to_agent."""
        mock_queue = Mock()
        mock_queue.enqueue = Mock(return_value="queue_id")
        mock_queue_class.return_value = mock_queue
        MessageCoordinator._queue = mock_queue

        mock_validator_instance = Mock()
        mock_validator_instance.validate_agent_can_send_message = Mock(
            return_value=(True, None, None))
        mock_validator.return_value = mock_validator_instance

        with patch("src.services.messaging_infrastructure.MessageCoordinator._detect_sender", return_value="CAPTAIN"):
            with patch("src.services.messaging_infrastructure.MessageCoordinator._determine_message_type", return_value=(Mock(), "CAPTAIN")):
                result = MessageCoordinator.send_to_agent(
                    "Agent-1", "Test message")

                assert result["success"] is True
                assert "queue_id" in result

    @patch("src.core.message_queue.MessageQueue")
    @patch("src.core.multi_agent_request_validator.get_multi_agent_validator")
    def test_send_to_agent_a2a_templates_content(self, mock_validator, mock_queue_class):
        """Agent-to-Agent messages with A2A category should be templated before enqueue."""
        mock_queue = Mock()
        recorded = {}

        def fake_enqueue(message):
            # Capture enqueued message for inspection
            recorded.update(message)
            return "queue_id_a2a"

        mock_queue.enqueue = fake_enqueue
        mock_queue_class.return_value = mock_queue
        MessageCoordinator._queue = mock_queue

        mock_validator_instance = Mock()
        mock_validator_instance.validate_agent_can_send_message = Mock(
            return_value=(True, None, None)
        )
        mock_validator.return_value = mock_validator_instance

        # Force Agent-to-Agent semantics and A2A category
        with patch(
            "src.services.messaging_infrastructure.MessageCoordinator._detect_sender",
            return_value="Agent-1",
        ):
            with patch(
                "src.services.messaging_infrastructure.MessageCoordinator._determine_message_type",
                return_value=(UnifiedMessageType.AGENT_TO_AGENT, "Agent-1"),
            ):
                result = MessageCoordinator.send_to_agent(
                    agent="Agent-2",
                    message="coordination ping",
                    priority=UnifiedMessagePriority.REGULAR,
                    use_pyautogui=True,
                    stalled=False,
                    message_category=MessageCategory.A2A,
                )

        assert result["success"] is True
        assert "queue_id" in result
        # Enqueued content should have the A2A header applied by the template layer
        assert "[HEADER] A2A COORDINATION" in recorded.get("content", "")

    @patch("src.core.message_queue.MessageQueue")
    @patch("src.core.multi_agent_request_validator.get_multi_agent_validator")
    def test_send_to_agent_a2a_prefix_invalid_sender_errors(self, mock_validator, mock_queue_class):
        """Messages starting with 'A2A:' from non-Agent senders should be blocked with guidance."""
        mock_queue = Mock()
        mock_queue.enqueue = Mock(return_value="queue_id")
        mock_queue_class.return_value = mock_queue
        MessageCoordinator._queue = mock_queue

        mock_validator_instance = Mock()
        mock_validator_instance.validate_agent_can_send_message = Mock(
            return_value=(True, None, None)
        )
        mock_validator.return_value = mock_validator_instance

        with patch(
            "src.services.messaging_infrastructure.MessageCoordinator._detect_sender",
            return_value="CAPTAIN",
        ):
            with patch(
                "src.services.messaging_infrastructure.MessageCoordinator._determine_message_type",
                return_value=(UnifiedMessageType.CAPTAIN_TO_AGENT, "CAPTAIN"),
            ):
                result = MessageCoordinator.send_to_agent(
                    agent="Agent-2",
                    message="A2A: coordination ping from captain",
                    priority=UnifiedMessagePriority.REGULAR,
                    use_pyautogui=True,
                    stalled=False,
                )

        assert isinstance(result, dict)
        assert result.get("success") is False
        assert result.get("blocked") is True
        assert result.get("reason") == "invalid_a2a_sender"
        # Error message should give clear operational guidance
        assert "AGENT_CONTEXT" in result.get("error_message", "")

    @patch("src.core.message_queue.MessageQueue")
    @patch("src.core.multi_agent_request_validator.get_multi_agent_validator")
    def test_send_to_agent_blocked(self, mock_validator, mock_queue_class):
        """Test send_to_agent when agent is blocked."""
        mock_queue = Mock()
        mock_queue_class.return_value = mock_queue
        MessageCoordinator._queue = mock_queue

        mock_validator_instance = Mock()
        mock_validator_instance.validate_agent_can_send_message = Mock(
            return_value=(False, "Blocked", {"request_id": "req_1"})
        )
        mock_validator.return_value = mock_validator_instance

        with patch("src.services.messaging_infrastructure.MessageCoordinator._detect_sender", return_value="CAPTAIN"):
            with patch("src.services.messaging_infrastructure.MessageCoordinator._determine_message_type", return_value=(Mock(), "CAPTAIN")):
                result = MessageCoordinator.send_to_agent(
                    "Agent-1", "Test message")

                assert result["success"] is False
                assert result["blocked"] is True

    @patch("src.core.message_queue.MessageQueue")
    @patch("src.core.multi_agent_request_validator.get_multi_agent_validator")
    def test_broadcast_to_all_success(self, mock_validator, mock_queue_class):
        """Test successful broadcast_to_all."""
        mock_queue = Mock()
        mock_queue.enqueue = Mock(return_value="queue_id")
        mock_queue_class.return_value = mock_queue
        MessageCoordinator._queue = mock_queue

        mock_validator_instance = Mock()
        mock_validator_instance.validate_agent_can_send_message = Mock(
            return_value=(True, None, None))
        mock_validator.return_value = mock_validator_instance

        from src.core.messaging_core import UnifiedMessagePriority

        result = MessageCoordinator.broadcast_to_all(
            "Test", UnifiedMessagePriority.REGULAR)

        assert result > 0

    def test_coordinate_survey(self):
        """Test coordinate_survey method."""
        with patch("src.services.messaging_infrastructure.MessageCoordinator.broadcast_to_all") as mock_broadcast:
            mock_broadcast.return_value = 5

            result = MessageCoordinator.coordinate_survey()

            assert result is True
            mock_broadcast.assert_called_once()

    def test_coordinate_consolidation(self):
        """Test coordinate_consolidation method."""
        with patch("src.services.messaging_infrastructure.MessageCoordinator.broadcast_to_all") as mock_broadcast:
            mock_broadcast.return_value = 5

            result = MessageCoordinator.coordinate_consolidation(
                "batch1", "COMPLETE")

            assert result is True
            mock_broadcast.assert_called_once()

    def test_detect_sender_from_env(self):
        """Test _detect_sender from environment variable."""
        with patch("os.getenv", return_value="Agent-1"):
            result = MessageCoordinator._detect_sender()

            assert result == "Agent-1"

    def test_detect_sender_default(self):
        """Test _detect_sender defaults to CAPTAIN."""
        with patch("os.getenv", return_value=None):
            with patch("pathlib.Path.cwd", return_value=Mock(as_posix=Mock(return_value="/other/path"))):
                result = MessageCoordinator._detect_sender()

                assert result == "CAPTAIN"


class TestUtilityFunctions:
    """Test utility functions."""

    def test_format_multi_agent_request_message(self):
        """Test _format_multi_agent_request_message."""
        result = _format_multi_agent_request_message(
            "Test message", "collector_1", "req_1", 3, 120
        )

        assert "Test message" in result
        assert "collector_1" in result
        assert "req_1" in result
        assert "3 agent(s)" in result

    def test_format_normal_message_broadcast(self):
        """Test _format_normal_message_with_instructions for BROADCAST."""
        result = _format_normal_message_with_instructions("Test", "BROADCAST")

        assert "Test" in result
        assert "BROADCAST MESSAGE" in result

    def test_format_normal_message_normal(self):
        """Test _format_normal_message_with_instructions for NORMAL."""
        result = _format_normal_message_with_instructions("Test", "NORMAL")

        assert "Test" in result
        assert "STANDARD MESSAGE" in result

    def test_create_messaging_parser(self):
        """Test create_messaging_parser."""
        parser = create_messaging_parser()

        assert parser is not None
        assert hasattr(parser, "add_argument")

    @patch("src.services.messaging.delivery_handlers.send_message")
    def test_send_message_pyautogui(self, mock_send):
        """Test send_message_pyautogui."""
        mock_send.return_value = True

        result = send_message_pyautogui("Agent-1", "Test message")

        assert result is True
        mock_send.assert_called_once()

    @patch("src.services.messaging.delivery_handlers.send_message")
    def test_send_message_to_onboarding_coords(self, mock_send):
        """Test send_message_to_onboarding_coords alias."""
        mock_send.return_value = True

        result = send_message_to_onboarding_coords("Agent-1", "Test")

        assert result is True
        # Should call send_message_pyautogui which calls send_message
        assert mock_send.call_count >= 1
