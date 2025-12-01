"""
Tests for messaging_cli_handlers.py

Comprehensive tests for CLI handlers, command processing, and message coordination.
Target: 10+ test methods, ≥85% coverage
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
from src.core.messaging_models_core import (
    UnifiedMessagePriority,
    UnifiedMessageType,
    UnifiedMessageTag,
)


class TestMessageCoordinator:
    """Tests for MessageCoordinator class."""

    @patch('src.services.messaging_cli_handlers.send_message')
    def test_send_to_agent_success(self, mock_send):
        """Test sending message to agent successfully."""
        mock_send.return_value = True
        result = MessageCoordinator.send_to_agent("Agent-6", "Test message")
        
        assert result is True
        mock_send.assert_called_once()
        call_args = mock_send.call_args
        assert call_args.kwargs["content"] == "Test message"
        assert call_args.kwargs["recipient"] == "Agent-6"
        assert call_args.kwargs["message_type"] == UnifiedMessageType.CAPTAIN_TO_AGENT

    @patch('src.services.messaging_cli_handlers.send_message')
    def test_send_to_agent_failure(self, mock_send):
        """Test sending message when it fails."""
        mock_send.side_effect = Exception("Test error")
        result = MessageCoordinator.send_to_agent("Agent-6", "Test message")
        
        assert result is False

    @patch('src.services.messaging_cli_handlers.send_message')
    def test_send_to_agent_with_priority(self, mock_send):
        """Test sending message with specific priority."""
        mock_send.return_value = True
        MessageCoordinator.send_to_agent(
            "Agent-6",
            "Test message",
            priority=UnifiedMessagePriority.URGENT
        )
        
        call_args = mock_send.call_args
        assert call_args.kwargs["priority"] == UnifiedMessagePriority.URGENT

    @patch('src.services.messaging_cli_handlers.send_message')
    def test_broadcast_to_all_success(self, mock_send):
        """Test broadcasting to all agents successfully."""
        mock_send.return_value = True
        result = MessageCoordinator.broadcast_to_all("Test broadcast")
        
        assert result == len(SWARM_AGENTS)
        assert mock_send.call_count == len(SWARM_AGENTS)

    @patch('src.services.messaging_cli_handlers.send_message')
    def test_broadcast_to_all_partial_failure(self, mock_send):
        """Test broadcasting when some messages fail."""
        # First 4 succeed, rest fail
        mock_send.side_effect = [True] * 4 + [False] * 4
        result = MessageCoordinator.broadcast_to_all("Test broadcast")
        
        assert result == 4

    @patch('src.services.messaging_cli_handlers.send_message')
    @patch('src.services.messaging_cli_handlers.send_message_pyautogui')
    def test_coordinate_survey(self, mock_pyautogui, mock_send):
        """Test coordinating survey."""
        mock_send.return_value = True
        mock_pyautogui.return_value = True
        result = MessageCoordinator.coordinate_survey()
        
        assert result > 0
        # Should broadcast survey message
        assert mock_send.call_count >= len(SWARM_AGENTS)
        # Should send individual assignments
        assert mock_pyautogui.call_count == len(SWARM_AGENTS)

    @patch('src.services.messaging_cli_handlers.send_message')
    def test_coordinate_consolidation(self, mock_send):
        """Test coordinating consolidation update."""
        mock_send.return_value = True
        result = MessageCoordinator.coordinate_consolidation("Batch 2", "58% complete")
        
        assert result == len(SWARM_AGENTS)
        assert mock_send.call_count == len(SWARM_AGENTS)
        # Check message content
        call_args = mock_send.call_args
        assert "Batch 2" in call_args.kwargs["content"]
        assert "58% complete" in call_args.kwargs["content"]


class TestHandlerFunctions:
    """Tests for handler functions."""

    @patch('src.services.messaging_cli_handlers.MessageCoordinator')
    def test_handle_message_broadcast(self, mock_coordinator):
        """Test handling broadcast message."""
        mock_coordinator.broadcast_to_all.return_value = 8
        args = Mock()
        args.message = "Test broadcast"
        args.broadcast = True
        args.agent = None
        args.priority = "regular"
        args.pyautogui = False
        
        result = handle_message(args, None)
        
        assert result == 0
        mock_coordinator.broadcast_to_all.assert_called_once()

    @patch('src.services.messaging_cli_handlers.MessageCoordinator')
    def test_handle_message_to_agent(self, mock_coordinator):
        """Test handling message to specific agent."""
        mock_coordinator.send_to_agent.return_value = True
        args = Mock()
        args.message = "Test message"
        args.broadcast = False
        args.agent = "Agent-6"
        args.priority = "urgent"
        args.pyautogui = False
        
        result = handle_message(args, None)
        
        assert result == 0
        mock_coordinator.send_to_agent.assert_called_once()

    def test_handle_message_no_message(self):
        """Test handling message when no message provided."""
        args = Mock()
        args.message = None
        args.broadcast = False
        
        result = handle_message(args, None)
        
        assert result == 1

    def test_handle_message_priority_normal(self):
        """Test handling message with 'normal' priority (should normalize to regular)."""
        with patch('src.services.messaging_cli_handlers.MessageCoordinator') as mock_coord:
            mock_coord.send_to_agent.return_value = True
            args = Mock()
            args.message = "Test"
            args.broadcast = False
            args.agent = "Agent-6"
            args.priority = "normal"  # Should normalize to regular
            args.pyautogui = False
            
            handle_message(args, None)
            
            # Check that regular priority was used (not urgent)
            call_args = mock_coord.send_to_agent.call_args
            assert call_args[2]["priority"] == UnifiedMessagePriority.REGULAR

    @patch('src.services.messaging_cli_handlers.MessageCoordinator')
    def test_handle_survey_success(self, mock_coordinator):
        """Test handling survey coordination successfully."""
        mock_coordinator.coordinate_survey.return_value = 8
        result = handle_survey()
        
        assert result == 0
        mock_coordinator.coordinate_survey.assert_called_once()

    @patch('src.services.messaging_cli_handlers.MessageCoordinator')
    def test_handle_survey_failure(self, mock_coordinator):
        """Test handling survey coordination when it fails."""
        mock_coordinator.coordinate_survey.return_value = 0
        result = handle_survey()
        
        assert result == 1

    @patch('src.services.messaging_cli_handlers.MessageCoordinator')
    def test_handle_consolidation_success(self, mock_coordinator):
        """Test handling consolidation coordination successfully."""
        mock_coordinator.coordinate_consolidation.return_value = 8
        args = Mock()
        args.consolidation_batch = "Batch 2"
        args.consolidation_status = "58% complete"
        
        result = handle_consolidation(args)
        
        assert result == 0
        mock_coordinator.coordinate_consolidation.assert_called_once_with(
            "Batch 2", "58% complete"
        )

    def test_handle_consolidation_missing_args(self):
        """Test handling consolidation when args are missing."""
        args = Mock()
        args.consolidation_batch = None
        args.consolidation_status = "58% complete"
        
        result = handle_consolidation(args)
        
        assert result == 1

    @patch('src.services.messaging_cli_handlers.get_coordinate_loader')
    def test_handle_coordinates_success(self, mock_loader):
        """Test handling coordinates display successfully."""
        mock_coord_loader = Mock()
        mock_coord_loader.get_all_agents.return_value = ["Agent-1", "Agent-6"]
        mock_coord_loader.get_chat_coordinates.return_value = (100, 200)
        mock_coord_loader.get_agent_description.return_value = "Test agent"
        mock_coord_loader.is_agent_active.return_value = True
        mock_loader.return_value = mock_coord_loader
        
        result = handle_coordinates()
        
        assert result == 0
        mock_coord_loader.get_all_agents.assert_called_once()

    @patch('src.services.messaging_cli_handlers.get_coordinate_loader')
    def test_handle_coordinates_no_agents(self, mock_loader):
        """Test handling coordinates when no agents found."""
        mock_coord_loader = Mock()
        mock_coord_loader.get_all_agents.return_value = []
        mock_loader.return_value = mock_coord_loader
        
        result = handle_coordinates()
        
        assert result == 1

    @patch('src.services.messaging_cli_handlers.send_message_to_onboarding_coords')
    def test_handle_start_agents_success(self, mock_send):
        """Test handling start agents command successfully."""
        mock_send.return_value = True
        args = Mock()
        args.start = [1, 2, 3]
        
        result = handle_start_agents(args)
        
        assert result == 0
        assert mock_send.call_count == 3

    def test_handle_start_agents_invalid_numbers(self):
        """Test handling start agents with invalid numbers."""
        with patch('src.services.messaging_cli_handlers.send_message_to_onboarding_coords') as mock_send:
            args = Mock()
            args.start = [0, 9, 10]  # Invalid numbers
            
            result = handle_start_agents(args)
            
            assert result == 1
            mock_send.assert_not_called()

    @patch('src.services.messaging_cli_handlers.get_coordinate_loader')
    @patch('src.services.messaging_cli_handlers.pyautogui')
    def test_handle_save_success(self, mock_pyautogui, mock_loader):
        """Test handling save command successfully."""
        mock_coord_loader = Mock()
        mock_coord_loader.get_chat_coordinates.return_value = (100, 200)
        mock_loader.return_value = mock_coord_loader
        
        args = Mock()
        args.message = "Test message"
        args.pyautogui = True
        
        result = handle_save(args, None)
        
        assert result == 0
        # Should call for each agent
        assert mock_pyautogui.moveTo.call_count == len(SWARM_AGENTS)

    def test_handle_save_no_message(self):
        """Test handling save command when no message provided."""
        parser = Mock()
        parser.error = Mock(side_effect=SystemExit)
        args = Mock()
        args.message = None
        
        with pytest.raises(SystemExit):
            handle_save(args, parser)

    @patch('src.services.messaging_cli_handlers.get_competition_system')
    def test_handle_leaderboard_success(self, mock_system):
        """Test handling leaderboard display successfully."""
        mock_comp_system = Mock()
        mock_score = Mock()
        mock_score.rank = 1
        mock_score.agent_name = "Agent-6"
        mock_score.total_points = 100
        mock_comp_system.get_leaderboard.return_value = [mock_score]
        mock_system.return_value = mock_comp_system
        
        result = handle_leaderboard()
        
        assert result == 0
        mock_comp_system.get_leaderboard.assert_called_once()


class TestConvenienceFunctions:
    """Tests for convenience functions."""

    @patch('src.services.messaging_cli_handlers.send_message')
    def test_send_message_pyautogui(self, mock_send):
        """Test send_message_pyautogui convenience function."""
        mock_send.return_value = True
        result = send_message_pyautogui("Agent-6", "Test message")
        
        assert result is True
        mock_send.assert_called_once()

    @patch('src.services.messaging_cli_handlers.send_message_pyautogui')
    def test_send_message_to_onboarding_coords(self, mock_pyautogui):
        """Test send_message_to_onboarding_coords alias."""
        mock_pyautogui.return_value = True
        result = send_message_to_onboarding_coords("Agent-6", "Test message")
        
        assert result is True
        mock_pyautogui.assert_called_once_with("Agent-6", "Test message", 30)

