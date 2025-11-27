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

