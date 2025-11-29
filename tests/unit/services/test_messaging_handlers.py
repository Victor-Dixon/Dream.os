"""
Unit tests for messaging_handlers.py
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.services.messaging_handlers import handle_message, handle_broadcast


class TestHandleMessage:
    """Tests for handle_message function."""

    @patch('src.services.messaging_handlers.MessageCoordinator')
    @patch('src.services.messaging_handlers.send_message')
    def test_handle_message_with_pyautogui(self, mock_send_message, mock_coordinator):
        """Test handle_message with PyAutoGUI enabled."""
        # Setup - MessageCoordinator is a class with static method
        mock_coordinator.send_to_agent = Mock(return_value=True)
        
        # Execute
        result = handle_message("Test message", "Agent-1", use_pyautogui=True)
        
        # Assert
        assert result is True
        mock_coordinator.send_to_agent.assert_called_once_with(
            "Agent-1", "Test message", use_pyautogui=True
        )
        mock_send_message.assert_not_called()

    @patch('src.services.messaging_handlers.send_message')
    def test_handle_message_without_pyautogui(self, mock_send_message):
        """Test handle_message without PyAutoGUI."""
        # Setup
        mock_send_message.return_value = True
        
        # Execute
        result = handle_message("Test message", "Agent-1", use_pyautogui=False)
        
        # Assert
        assert result is True
        mock_send_message.assert_called_once()
        call_args = mock_send_message.call_args
        assert call_args.kwargs['content'] == "Test message"
        assert call_args.kwargs['recipient'] == "Agent-1"
        assert call_args.kwargs['sender'] == "HANDLER"

    @patch('src.services.messaging_handlers.MessageCoordinator')
    def test_handle_message_pyautogui_failure(self, mock_coordinator):
        """Test handle_message when PyAutoGUI delivery fails."""
        # Setup - MessageCoordinator is a class with static method
        mock_coordinator.send_to_agent = Mock(return_value=False)
        
        # Execute
        result = handle_message("Test message", "Agent-1", use_pyautogui=True)
        
        # Assert
        assert result is False
        mock_coordinator.send_to_agent.assert_called_once()


class TestHandleBroadcast:
    """Tests for handle_broadcast function."""

    @patch('src.services.messaging_handlers.broadcast_message')
    def test_handle_broadcast_success(self, mock_broadcast):
        """Test successful broadcast."""
        # Setup
        mock_broadcast.return_value = True
        
        # Execute
        result = handle_broadcast("Broadcast message")
        
        # Assert
        assert result is True
        mock_broadcast.assert_called_once_with(
            content="Broadcast message", sender="HANDLER"
        )

    @patch('src.services.messaging_handlers.broadcast_message')
    def test_handle_broadcast_failure(self, mock_broadcast):
        """Test broadcast failure."""
        # Setup
        mock_broadcast.return_value = False
        
        # Execute
        result = handle_broadcast("Broadcast message")
        
        # Assert
        assert result is False
        mock_broadcast.assert_called_once()

    @patch('src.services.messaging_handlers.MessageCoordinator')
    @patch('src.services.messaging_handlers.send_message')
    def test_handle_message_empty_content(self, mock_send_message, mock_coordinator):
        """Test handle_message with empty content."""
        # Setup
        mock_send_message.return_value = True
        
        # Execute
        result = handle_message("", "Agent-1", use_pyautogui=False)
        
        # Assert
        assert result is True
        mock_send_message.assert_called_once()
        call_args = mock_send_message.call_args
        assert call_args.kwargs['content'] == ""

    @patch('src.services.messaging_handlers.MessageCoordinator')
    def test_handle_message_pyautogui_exception(self, mock_coordinator):
        """Test handle_message when PyAutoGUI raises exception."""
        # Setup
        mock_coordinator.send_to_agent = Mock(side_effect=Exception("PyAutoGUI error"))
        
        # Execute & Assert
        with pytest.raises(Exception):
            handle_message("Test message", "Agent-1", use_pyautogui=True)

    @patch('src.services.messaging_handlers.send_message')
    def test_handle_message_send_exception(self, mock_send_message):
        """Test handle_message when send_message raises exception."""
        # Setup
        mock_send_message.side_effect = Exception("Send error")
        
        # Execute & Assert
        with pytest.raises(Exception):
            handle_message("Test message", "Agent-1", use_pyautogui=False)

    @patch('src.services.messaging_handlers.broadcast_message')
    def test_handle_broadcast_exception(self, mock_broadcast):
        """Test handle_broadcast when broadcast_message raises exception."""
        # Setup
        mock_broadcast.side_effect = Exception("Broadcast error")
        
        # Execute & Assert
        with pytest.raises(Exception):
            handle_broadcast("Broadcast message")

    @patch('src.services.messaging_handlers.MessageCoordinator')
    def test_handle_message_different_agents(self, mock_coordinator):
        """Test handle_message with different agent IDs."""
        # Setup
        mock_coordinator.send_to_agent = Mock(return_value=True)
        
        # Execute
        agents = ["Agent-1", "Agent-2", "Agent-3"]
        for agent in agents:
            result = handle_message("Test", agent, use_pyautogui=True)
            assert result is True
        
        # Assert
        assert mock_coordinator.send_to_agent.call_count == 3

    @patch('src.services.messaging_handlers.broadcast_message')
    def test_handle_broadcast_empty_message(self, mock_broadcast):
        """Test handle_broadcast with empty message."""
        mock_broadcast.return_value = True
        
        result = handle_broadcast("")
        
        assert result is True
        mock_broadcast.assert_called_once_with(content="", sender="HANDLER")

    @patch('src.services.messaging_handlers.MessageCoordinator')
    def test_handle_message_different_priorities(self, mock_coordinator):
        """Test handle_message with different priority settings."""
        mock_coordinator.send_to_agent = Mock(return_value=True)
        
        # Test with use_pyautogui=True
        result1 = handle_message("Test", "Agent-1", use_pyautogui=True)
        assert result1 is True
        
        # Test with use_pyautogui=False
        with patch('src.services.messaging_handlers.send_message', return_value=True):
            result2 = handle_message("Test", "Agent-1", use_pyautogui=False)
            assert result2 is True

    @patch('src.services.messaging_handlers.MessageCoordinator')
    def test_handle_message_with_dict_result(self, mock_coordinator):
        """Test handle_message when MessageCoordinator returns dict."""
        mock_coordinator.send_to_agent = Mock(return_value={"success": True, "queue_id": "q123"})
        
        result = handle_message("Test", "Agent-1", use_pyautogui=True)
        
        # Should handle dict return value
        assert result is not None

    @patch('src.services.messaging_handlers.MessageCoordinator')
    def test_handle_message_blocked_result(self, mock_coordinator):
        """Test handle_message when message is blocked."""
        mock_coordinator.send_to_agent = Mock(return_value={"success": False, "blocked": True})
        
        result = handle_message("Test", "Agent-1", use_pyautogui=True)
        
        # Should handle blocked result
        assert result is not None

    @patch('src.services.messaging_handlers.send_message')
    def test_handle_message_long_content(self, mock_send_message):
        """Test handle_message with very long content."""
        long_content = "A" * 10000
        mock_send_message.return_value = True
        
        result = handle_message(long_content, "Agent-1", use_pyautogui=False)
        
        assert result is True
        mock_send_message.assert_called_once()

    @patch('src.services.messaging_handlers.broadcast_message')
    def test_handle_broadcast_long_message(self, mock_broadcast):
        """Test handle_broadcast with very long message."""
        long_message = "B" * 10000
        mock_broadcast.return_value = True
        
        result = handle_broadcast(long_message)
        
        assert result is True
        mock_broadcast.assert_called_once_with(content=long_message, sender="HANDLER")

    @patch('src.services.messaging_handlers.MessageCoordinator')
    def test_handle_message_all_swarm_agents(self, mock_coordinator):
        """Test handle_message with all swarm agents."""
        mock_coordinator.send_to_agent = Mock(return_value=True)
        
        agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
        for agent in agents:
            result = handle_message("Test", agent, use_pyautogui=True)
            assert result is True
        
        assert mock_coordinator.send_to_agent.call_count == len(agents)


    def test_handle_message_with_dict_result(self, mock_coordinator):
        """Test handle_message when MessageCoordinator returns dict."""
        mock_coordinator.send_to_agent = Mock(return_value={"success": True, "queue_id": "q123"})
        
        result = handle_message("Test", "Agent-1", use_pyautogui=True)
        
        # Should handle dict return value
        assert result is not None

    @patch('src.services.messaging_handlers.MessageCoordinator')
    def test_handle_message_blocked_result(self, mock_coordinator):
        """Test handle_message when message is blocked."""
        mock_coordinator.send_to_agent = Mock(return_value={"success": False, "blocked": True})
        
        result = handle_message("Test", "Agent-1", use_pyautogui=True)
        
        # Should handle blocked result
        assert result is not None

    @patch('src.services.messaging_handlers.send_message')
    def test_handle_message_long_content(self, mock_send_message):
        """Test handle_message with very long content."""
        long_content = "A" * 10000
        mock_send_message.return_value = True
        
        result = handle_message(long_content, "Agent-1", use_pyautogui=False)
        
        assert result is True
        mock_send_message.assert_called_once()

    @patch('src.services.messaging_handlers.broadcast_message')
    def test_handle_broadcast_long_message(self, mock_broadcast):
        """Test handle_broadcast with very long message."""
        long_message = "B" * 10000
        mock_broadcast.return_value = True
        
        result = handle_broadcast(long_message)
        
        assert result is True
        mock_broadcast.assert_called_once_with(content=long_message, sender="HANDLER")

    @patch('src.services.messaging_handlers.MessageCoordinator')
    def test_handle_message_all_swarm_agents(self, mock_coordinator):
        """Test handle_message with all swarm agents."""
        mock_coordinator.send_to_agent = Mock(return_value=True)
        
        agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
        for agent in agents:
            result = handle_message("Test", agent, use_pyautogui=True)
            assert result is True
        
        assert mock_coordinator.send_to_agent.call_count == len(agents)

