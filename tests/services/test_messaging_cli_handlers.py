"""
Tests for messaging_cli_handlers.py

Comprehensive tests for CLI command handlers.
Target: ≥85% coverage
"""

import pytest
from unittest.mock import MagicMock, patch, Mock
from src.services.messaging_cli_handlers import (
    send_message_pyautogui,
    send_message_to_onboarding_coords,
    MessageCoordinator,
    handle_message,
    handle_survey,
    handle_consolidation,
    handle_coordinates,
    handle_start_agents,
    handle_save,
    handle_leaderboard,
    SWARM_AGENTS,
)
from src.core.messaging_models_core import UnifiedMessagePriority, UnifiedMessageType


class TestSwarmAgents:
    """Tests for SWARM_AGENTS constant."""

    def test_swarm_agents_list(self):
        """Test that SWARM_AGENTS contains all agents."""
        assert isinstance(SWARM_AGENTS, list)
        assert len(SWARM_AGENTS) == 8
        assert "Agent-1" in SWARM_AGENTS
        assert "Agent-8" in SWARM_AGENTS


class TestSendMessagePyAutoGUI:
    """Tests for send_message_pyautogui function."""

    @patch('src.services.messaging_cli_handlers.send_message')
    def test_send_message_pyautogui_success(self, mock_send):
        """Test sending message via PyAutoGUI."""
        mock_send.return_value = True
        result = send_message_pyautogui("Agent-1", "Test message")
        
        assert result is True
        mock_send.assert_called_once()
        call_args = mock_send.call_args
        assert call_args.kwargs["content"] == "Test message"
        assert call_args.kwargs["recipient"] == "Agent-1"
        assert call_args.kwargs["message_type"] == UnifiedMessageType.CAPTAIN_TO_AGENT

    @patch('src.services.messaging_cli_handlers.send_message')
    def test_send_message_pyautogui_failure(self, mock_send):
        """Test send_message_pyautogui failure."""
        mock_send.return_value = False
        result = send_message_pyautogui("Agent-1", "Test message")
        
        assert result is False


class TestSendMessageToOnboardingCoords:
    """Tests for send_message_to_onboarding_coords function."""

    @patch('src.services.messaging_cli_handlers.send_message_pyautogui')
    def test_send_message_to_onboarding_coords(self, mock_send):
        """Test sending message to onboarding coordinates."""
        mock_send.return_value = True
        result = send_message_to_onboarding_coords("Agent-1", "Test message")
        
        assert result is True
        mock_send.assert_called_once_with("Agent-1", "Test message", 30)


class TestMessageCoordinator:
    """Tests for MessageCoordinator class."""

    @patch('src.services.messaging_cli_handlers.send_message')
    def test_send_to_agent_success(self, mock_send):
        """Test sending message to agent."""
        mock_send.return_value = True
        result = MessageCoordinator.send_to_agent("Agent-1", "Test message")
        
        assert result is True
        mock_send.assert_called_once()

    @patch('src.services.messaging_cli_handlers.send_message')
    def test_send_to_agent_exception(self, mock_send):
        """Test exception handling in send_to_agent."""
        mock_send.side_effect = Exception("Test error")
        result = MessageCoordinator.send_to_agent("Agent-1", "Test message")
        
        assert result is False

    @patch('src.services.messaging_cli_handlers.send_message')
    def test_broadcast_to_all(self, mock_send):
        """Test broadcasting to all agents."""
        mock_send.return_value = True
        result = MessageCoordinator.broadcast_to_all("Test message")
        
        assert result == 8  # All 8 agents
        assert mock_send.call_count == 8

    @patch('src.services.messaging_cli_handlers.send_message')
    def test_broadcast_to_all_partial_success(self, mock_send):
        """Test broadcast with partial success."""
        mock_send.side_effect = [True, False, True, False, True, False, True, False]
        result = MessageCoordinator.broadcast_to_all("Test message")
        
        assert result == 4  # 4 successful

    @patch('src.services.messaging_cli_handlers.send_message_pyautogui')
    @patch('src.services.messaging_cli_handlers.MessageCoordinator.broadcast_to_all')
    def test_coordinate_survey(self, mock_broadcast, mock_send):
        """Test coordinating survey."""
        from src.services.messaging_cli_formatters import AGENT_ASSIGNMENTS
        
        mock_broadcast.return_value = 8
        mock_send.return_value = True
        
        result = MessageCoordinator.coordinate_survey()
        
        assert result == 8
        assert mock_broadcast.call_count == 1
        assert mock_send.call_count == len(AGENT_ASSIGNMENTS)

    @patch('src.services.messaging_cli_handlers.send_message')
    def test_coordinate_consolidation(self, mock_send):
        """Test coordinating consolidation."""
        mock_send.return_value = True
        result = MessageCoordinator.coordinate_consolidation("Batch 1", "Complete")
        
        assert result == 8  # All 8 agents
        assert mock_send.call_count == 8


class TestHandleMessage:
    """Tests for handle_message function."""

    def test_handle_message_no_message(self):
        """Test handle_message with no message."""
        args = MagicMock()
        args.message = None
        args.broadcast = False
        args.agent = None
        
        result = handle_message(args, None)
        assert result == 1

    @patch('src.services.messaging_cli_handlers.MessageCoordinator.broadcast_to_all')
    def test_handle_message_broadcast(self, mock_broadcast):
        """Test handle_message with broadcast."""
        args = MagicMock()
        args.message = "Test message"
        args.broadcast = True
        args.priority = "urgent"
        
        mock_broadcast.return_value = 8
        result = handle_message(args, None)
        
        assert result == 0
        mock_broadcast.assert_called_once()

    @patch('src.services.messaging_cli_handlers.MessageCoordinator.broadcast_to_all')
    def test_handle_message_broadcast_failure(self, mock_broadcast):
        """Test handle_message broadcast failure."""
        args = MagicMock()
        args.message = "Test message"
        args.broadcast = True
        args.priority = "regular"
        
        mock_broadcast.return_value = 0
        result = handle_message(args, None)
        
        assert result == 1

    @patch('src.services.messaging_cli_handlers.MessageCoordinator.send_to_agent')
    def test_handle_message_to_agent(self, mock_send):
        """Test handle_message to specific agent."""
        args = MagicMock()
        args.message = "Test message"
        args.broadcast = False
        args.agent = "Agent-1"
        args.priority = "normal"  # Should normalize to "regular"
        args.pyautogui = False
        
        mock_send.return_value = True
        result = handle_message(args, None)
        
        assert result == 0
        mock_send.assert_called_once()

    @patch('src.services.messaging_cli_handlers.MessageCoordinator.send_to_agent')
    def test_handle_message_to_agent_failure(self, mock_send):
        """Test handle_message to agent failure."""
        args = MagicMock()
        args.message = "Test message"
        args.broadcast = False
        args.agent = "Agent-1"
        args.priority = "urgent"
        args.pyautogui = False
        
        mock_send.return_value = False
        result = handle_message(args, None)
        
        assert result == 1


class TestHandleSurvey:
    """Tests for handle_survey function."""

    @patch('src.services.messaging_cli_handlers.MessageCoordinator.coordinate_survey')
    def test_handle_survey_success(self, mock_coordinate):
        """Test handle_survey success."""
        mock_coordinate.return_value = 8
        result = handle_survey()
        
        assert result == 0

    @patch('src.services.messaging_cli_handlers.MessageCoordinator.coordinate_survey')
    def test_handle_survey_failure(self, mock_coordinate):
        """Test handle_survey failure."""
        mock_coordinate.return_value = 0
        result = handle_survey()
        
        assert result == 1


class TestHandleConsolidation:
    """Tests for handle_consolidation function."""

    def test_handle_consolidation_missing_args(self):
        """Test handle_consolidation with missing arguments."""
        args = MagicMock()
        args.consolidation_batch = None
        args.consolidation_status = "Complete"
        
        result = handle_consolidation(args)
        assert result == 1

    @patch('src.services.messaging_cli_handlers.MessageCoordinator.coordinate_consolidation')
    def test_handle_consolidation_success(self, mock_coordinate):
        """Test handle_consolidation success."""
        args = MagicMock()
        args.consolidation_batch = "Batch 1"
        args.consolidation_status = "Complete"
        
        mock_coordinate.return_value = 8
        result = handle_consolidation(args)
        
        assert result == 0
        mock_coordinate.assert_called_once_with("Batch 1", "Complete")


class TestHandleCoordinates:
    """Tests for handle_coordinates function."""

    @patch('src.services.messaging_cli_handlers.get_coordinate_loader')
    def test_handle_coordinates_success(self, mock_loader):
        """Test handle_coordinates success."""
        mock_coord_loader = MagicMock()
        mock_coord_loader.get_all_agents.return_value = ["Agent-1", "Agent-2"]
        mock_coord_loader.get_chat_coordinates.return_value = (100, 200)
        mock_coord_loader.get_agent_description.return_value = "Test description"
        mock_coord_loader.is_agent_active.return_value = True
        mock_loader.return_value = mock_coord_loader
        
        result = handle_coordinates()
        
        assert result == 0

    @patch('src.services.messaging_cli_handlers.get_coordinate_loader')
    def test_handle_coordinates_no_agents(self, mock_loader):
        """Test handle_coordinates with no agents."""
        mock_coord_loader = MagicMock()
        mock_coord_loader.get_all_agents.return_value = []
        mock_loader.return_value = mock_coord_loader
        
        result = handle_coordinates()
        
        assert result == 1

    @patch('src.services.messaging_cli_handlers.get_coordinate_loader')
    def test_handle_coordinates_exception(self, mock_loader):
        """Test handle_coordinates exception handling."""
        mock_loader.side_effect = Exception("Test error")
        
        result = handle_coordinates()
        
        assert result == 1


class TestHandleStartAgents:
    """Tests for handle_start_agents function."""

    @patch('src.services.messaging_cli_handlers.send_message_to_onboarding_coords')
    def test_handle_start_agents_success(self, mock_send):
        """Test handle_start_agents success."""
        args = MagicMock()
        args.start = [1, 2, 3]
        
        mock_send.return_value = True
        result = handle_start_agents(args)
        
        assert result == 0
        assert mock_send.call_count == 3

    @patch('src.services.messaging_cli_handlers.send_message_to_onboarding_coords')
    def test_handle_start_agents_invalid_numbers(self, mock_send):
        """Test handle_start_agents with invalid agent numbers."""
        args = MagicMock()
        args.start = [0, 9, 10]  # Invalid numbers
        
        result = handle_start_agents(args)
        
        assert result == 1
        mock_send.assert_not_called()

    @patch('src.services.messaging_cli_handlers.send_message_to_onboarding_coords')
    def test_handle_start_agents_partial_success(self, mock_send):
        """Test handle_start_agents with partial success."""
        args = MagicMock()
        args.start = [1, 2]
        
        mock_send.side_effect = [True, False]
        result = handle_start_agents(args)
        
        assert result == 0  # At least one success

    @patch('src.services.messaging_cli_handlers.send_message_to_onboarding_coords')
    def test_handle_start_agents_exception(self, mock_send):
        """Test handle_start_agents exception handling."""
        args = MagicMock()
        args.start = [1]
        
        mock_send.side_effect = Exception("Test error")
        result = handle_start_agents(args)
        
        assert result == 1


class TestHandleSave:
    """Tests for handle_save function."""

    @patch('src.services.messaging_cli_handlers.get_coordinate_loader')
    @patch('src.services.messaging_cli_handlers.pyautogui')
    def test_handle_save_success(self, mock_pyautogui, mock_loader):
        """Test handle_save success."""
        args = MagicMock()
        args.message = "Test message"
        args.pyautogui = False
        
        mock_coord_loader = MagicMock()
        mock_coord_loader.get_chat_coordinates.return_value = (100, 200)
        mock_loader.return_value = mock_coord_loader
        
        result = handle_save(args, None)
        
        assert result == 0
        # Should call for all 8 agents
        assert mock_pyautogui.moveTo.call_count == 8

    def test_handle_save_no_message(self):
        """Test handle_save with no message."""
        args = MagicMock()
        args.message = None
        
        parser = MagicMock()
        parser.error = MagicMock(side_effect=SystemExit)
        
        with pytest.raises(SystemExit):
            handle_save(args, parser)


class TestHandleLeaderboard:
    """Tests for handle_leaderboard function."""

    @patch('src.services.messaging_cli_handlers.get_competition_system')
    def test_handle_leaderboard_success(self, mock_system):
        """Test handle_leaderboard success."""
        mock_competition = MagicMock()
        mock_score = MagicMock()
        mock_score.rank = 1
        mock_score.agent_name = "Agent-1"
        mock_score.total_points = 100
        mock_competition.get_leaderboard.return_value = [mock_score]
        mock_system.return_value = mock_competition
        
        result = handle_leaderboard()
        
        assert result == 0

