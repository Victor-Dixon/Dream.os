"""
Unit tests for messaging_cli_handlers.py
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.services.messaging_cli_handlers import (
    send_message_pyautogui,
    send_message_to_onboarding_coords,
    MessageCoordinator,
    handle_message,
    handle_survey,
    handle_consolidation,
    handle_coordinates,
    handle_start_agents,
    handle_leaderboard,
    SWARM_AGENTS,
)


class TestSendMessagePyAutoGUI:
    """Tests for send_message_pyautogui function."""

    @patch('src.services.messaging_cli_handlers.send_message')
    def test_send_message_pyautogui_success(self, mock_send):
        """Test successful PyAutoGUI message send."""
        mock_send.return_value = True
        result = send_message_pyautogui("Agent-1", "Test message")
        assert result is True
        mock_send.assert_called_once()
        call_kwargs = mock_send.call_args.kwargs
        assert call_kwargs['content'] == "Test message"
        assert call_kwargs['recipient'] == "Agent-1"
        assert call_kwargs['sender'] == "CAPTAIN"

    @patch('src.services.messaging_cli_handlers.send_message')
    def test_send_message_pyautogui_failure(self, mock_send):
        """Test failed PyAutoGUI message send."""
        mock_send.return_value = False
        result = send_message_pyautogui("Agent-1", "Test message")
        assert result is False


class TestSendMessageToOnboardingCoords:
    """Tests for send_message_to_onboarding_coords function."""

    @patch('src.services.messaging_cli_handlers.send_message_pyautogui')
    def test_send_message_to_onboarding_coords(self, mock_send):
        """Test onboarding coordinates message send."""
        mock_send.return_value = True
        result = send_message_to_onboarding_coords("Agent-1", "Test message")
        assert result is True
        mock_send.assert_called_once_with("Agent-1", "Test message", timeout=30)


class TestMessageCoordinator:
    """Tests for MessageCoordinator class."""

    @patch('src.services.messaging_cli_handlers.send_message')
    def test_send_to_agent_success(self, mock_send):
        """Test successful send_to_agent."""
        mock_send.return_value = True
        result = MessageCoordinator.send_to_agent("Agent-1", "Test message")
        assert result is True
        mock_send.assert_called_once()

    @patch('src.services.messaging_cli_handlers.send_message')
    def test_send_to_agent_failure(self, mock_send):
        """Test failed send_to_agent."""
        mock_send.side_effect = Exception("Error")
        result = MessageCoordinator.send_to_agent("Agent-1", "Test message")
        assert result is False

    @patch('src.services.messaging_cli_handlers.send_message')
    def test_broadcast_to_all(self, mock_send):
        """Test broadcast_to_all."""
        mock_send.return_value = True
        result = MessageCoordinator.broadcast_to_all("Broadcast message")
        assert result == len(SWARM_AGENTS)
        assert mock_send.call_count == len(SWARM_AGENTS)

    @patch('src.services.messaging_cli_handlers.send_message_pyautogui')
    @patch('src.services.messaging_cli_handlers.MessageCoordinator.broadcast_to_all')
    def test_coordinate_survey(self, mock_broadcast, mock_send):
        """Test coordinate_survey."""
        mock_broadcast.return_value = 8
        mock_send.return_value = True
        result = MessageCoordinator.coordinate_survey()
        assert result == 8
        assert mock_broadcast.call_count == 1
        assert mock_send.call_count == len(SWARM_AGENTS)

    @patch('src.services.messaging_cli_handlers.send_message')
    def test_coordinate_consolidation(self, mock_send):
        """Test coordinate_consolidation."""
        mock_send.return_value = True
        result = MessageCoordinator.coordinate_consolidation("batch1", "complete")
        assert result == len(SWARM_AGENTS)
        assert mock_send.call_count == len(SWARM_AGENTS)


class TestHandleMessage:
    """Tests for handle_message function."""

    def test_handle_message_no_message_no_broadcast(self):
        """Test handle_message with no message and no broadcast."""
        args = Mock()
        args.message = None
        args.broadcast = False
        args.agent = None
        result = handle_message(args, Mock())
        assert result == 1

    @patch('src.services.messaging_cli_handlers.MessageCoordinator')
    def test_handle_message_broadcast(self, mock_coordinator):
        """Test handle_message with broadcast."""
        args = Mock()
        args.message = "Broadcast message"
        args.broadcast = True
        args.agent = None
        args.priority = "regular"
        mock_coordinator.broadcast_to_all.return_value = 8
        result = handle_message(args, Mock())
        assert result == 0
        mock_coordinator.broadcast_to_all.assert_called_once()

    @patch('src.services.messaging_cli_handlers.MessageCoordinator')
    def test_handle_message_to_agent(self, mock_coordinator):
        """Test handle_message to specific agent."""
        args = Mock()
        args.message = "Test message"
        args.broadcast = False
        args.agent = "Agent-1"
        args.priority = "regular"
        args.pyautogui = False
        mock_coordinator.send_to_agent.return_value = True
        result = handle_message(args, Mock())
        assert result == 0
        mock_coordinator.send_to_agent.assert_called_once()


class TestHandleSurvey:
    """Tests for handle_survey function."""

    @patch('src.services.messaging_cli_handlers.MessageCoordinator')
    def test_handle_survey_success(self, mock_coordinator):
        """Test successful survey coordination."""
        mock_coordinator.coordinate_survey.return_value = 8
        result = handle_survey()
        assert result == 0

    @patch('src.services.messaging_cli_handlers.MessageCoordinator')
    def test_handle_survey_failure(self, mock_coordinator):
        """Test failed survey coordination."""
        mock_coordinator.coordinate_survey.return_value = 0
        result = handle_survey()
        assert result == 1


class TestHandleConsolidation:
    """Tests for handle_consolidation function."""

    def test_handle_consolidation_missing_args(self):
        """Test handle_consolidation with missing arguments."""
        args = Mock()
        args.consolidation_batch = None
        args.consolidation_status = None
        result = handle_consolidation(args)
        assert result == 1

    @patch('src.services.messaging_cli_handlers.MessageCoordinator')
    def test_handle_consolidation_success(self, mock_coordinator):
        """Test successful consolidation coordination."""
        args = Mock()
        args.consolidation_batch = "batch1"
        args.consolidation_status = "complete"
        mock_coordinator.coordinate_consolidation.return_value = 8
        result = handle_consolidation(args)
        assert result == 0

    @patch('src.services.messaging_cli_handlers.MessageCoordinator')
    def test_handle_consolidation_failure(self, mock_coordinator):
        """Test failed consolidation coordination."""
        args = Mock()
        args.consolidation_batch = "batch1"
        args.consolidation_status = "complete"
        mock_coordinator.coordinate_consolidation.return_value = 0
        result = handle_consolidation(args)
        assert result == 1


class TestHandleCoordinates:
    """Tests for handle_coordinates function."""

    @patch('src.services.messaging_cli_handlers.get_coordinate_loader')
    def test_handle_coordinates_success(self, mock_loader):
        """Test successful coordinate display."""
        mock_coord_loader = Mock()
        mock_coord_loader.get_all_agents.return_value = ["Agent-1", "Agent-2"]
        mock_coord_loader.get_chat_coordinates.return_value = (100, 200)
        mock_coord_loader.get_agent_description.return_value = "Test agent"
        mock_coord_loader.is_agent_active.return_value = True
        mock_loader.return_value = mock_coord_loader
        result = handle_coordinates()
        assert result == 0

    @patch('src.services.messaging_cli_handlers.get_coordinate_loader')
    def test_handle_coordinates_no_agents(self, mock_loader):
        """Test coordinate display with no agents."""
        mock_coord_loader = Mock()
        mock_coord_loader.get_all_agents.return_value = []
        mock_loader.return_value = mock_coord_loader
        result = handle_coordinates()
        assert result == 1

    @patch('src.services.messaging_cli_handlers.get_coordinate_loader')
    def test_handle_coordinates_exception(self, mock_loader):
        """Test coordinate display with exception."""
        mock_loader.side_effect = Exception("Error")
        result = handle_coordinates()
        assert result == 1


class TestHandleStartAgents:
    """Tests for handle_start_agents function."""

    @patch('src.services.messaging_cli_handlers.send_message_to_onboarding_coords')
    def test_handle_start_agents_success(self, mock_send):
        """Test successful agent start."""
        args = Mock()
        args.start = [1, 2, 3]
        mock_send.return_value = True
        result = handle_start_agents(args)
        assert result == 0
        assert mock_send.call_count == 3

    @patch('src.services.messaging_cli_handlers.send_message_to_onboarding_coords')
    def test_handle_start_agents_invalid_numbers(self, mock_send):
        """Test agent start with invalid numbers."""
        args = Mock()
        args.start = [0, 9, 10]  # Invalid agent numbers
        result = handle_start_agents(args)
        assert result == 1
        mock_send.assert_not_called()

    @patch('src.services.messaging_cli_handlers.send_message_to_onboarding_coords')
    def test_handle_start_agents_partial_failure(self, mock_send):
        """Test agent start with partial failures."""
        args = Mock()
        args.start = [1, 2]
        mock_send.side_effect = [True, False]
        result = handle_start_agents(args)
        assert result == 0  # At least one succeeded


class TestHandleLeaderboard:
    """Tests for handle_leaderboard function."""

    @patch('src.services.messaging_cli_handlers.get_competition_system')
    def test_handle_leaderboard_success(self, mock_system):
        """Test successful leaderboard display."""
        mock_competition = Mock()
        mock_score1 = Mock()
        mock_score1.rank = 1
        mock_score1.agent_name = "Agent-1"
        mock_score1.total_points = 100
        mock_score2 = Mock()
        mock_score2.rank = 2
        mock_score2.agent_name = "Agent-2"
        mock_score2.total_points = 50
        mock_competition.get_leaderboard.return_value = [mock_score1, mock_score2]
        mock_system.return_value = mock_competition
        result = handle_leaderboard()
        assert result == 0

