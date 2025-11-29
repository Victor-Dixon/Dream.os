"""
Expanded unit tests for messaging_handlers.py - Batch 9

Additional tests for comprehensive coverage.
"""

import pytest
from unittest.mock import Mock, patch
from src.services.messaging_handlers import handle_message, handle_broadcast


class TestHandleMessageExpanded:
    """Expanded tests for handle_message function."""

    @patch('src.services.messaging_handlers.MessageCoordinator')
    def test_handle_message_long_content(self, mock_coordinator):
        """Test handle_message with very long content."""
        mock_coordinator.send_to_agent = Mock(return_value=True)
        
        long_content = "A" * 10000
        result = handle_message(long_content, "Agent-1", use_pyautogui=True)
        
        assert result is True
        mock_coordinator.send_to_agent.assert_called_once()

    @patch('src.services.messaging_handlers.MessageCoordinator')
    def test_handle_message_special_characters(self, mock_coordinator):
        """Test handle_message with special characters."""
        mock_coordinator.send_to_agent = Mock(return_value=True)
        
        special_content = "Test with special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?"
        result = handle_message(special_content, "Agent-1", use_pyautogui=True)
        
        assert result is True

    @patch('src.services.messaging_handlers.MessageCoordinator')
    def test_handle_message_multiline(self, mock_coordinator):
        """Test handle_message with multiline content."""
        mock_coordinator.send_to_agent = Mock(return_value=True)
        
        multiline_content = "Line 1\nLine 2\nLine 3"
        result = handle_message(multiline_content, "Agent-1", use_pyautogui=True)
        
        assert result is True

    @patch('src.services.messaging_handlers.send_message')
    def test_handle_message_without_pyautogui_special_chars(self, mock_send_message):
        """Test handle_message without PyAutoGUI with special characters."""
        mock_send_message.return_value = True
        
        special_content = "Test: émojis 🚀 and unicode 中文"
        result = handle_message(special_content, "Agent-1", use_pyautogui=False)
        
        assert result is True
        mock_send_message.assert_called_once()

    @patch('src.services.messaging_handlers.MessageCoordinator')
    def test_handle_message_all_agents(self, mock_coordinator):
        """Test handle_message with all agent IDs."""
        mock_coordinator.send_to_agent = Mock(return_value=True)
        
        agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
        for agent in agents:
            result = handle_message("Test", agent, use_pyautogui=True)
            assert result is True
        
        assert mock_coordinator.send_to_agent.call_count == 8


class TestHandleBroadcastExpanded:
    """Expanded tests for handle_broadcast function."""

    @patch('src.services.messaging_handlers.broadcast_message')
    def test_handle_broadcast_long_content(self, mock_broadcast):
        """Test handle_broadcast with very long content."""
        mock_broadcast.return_value = True
        
        long_content = "B" * 10000
        result = handle_broadcast(long_content)
        
        assert result is True
        mock_broadcast.assert_called_once_with(content=long_content, sender="HANDLER")

    @patch('src.services.messaging_handlers.broadcast_message')
    def test_handle_broadcast_special_characters(self, mock_broadcast):
        """Test handle_broadcast with special characters."""
        mock_broadcast.return_value = True
        
        special_content = "Broadcast with special: !@#$%^&*()"
        result = handle_broadcast(special_content)
        
        assert result is True

    @patch('src.services.messaging_handlers.broadcast_message')
    def test_handle_broadcast_multiline(self, mock_broadcast):
        """Test handle_broadcast with multiline content."""
        mock_broadcast.return_value = True
        
        multiline_content = "Line 1\nLine 2\nLine 3"
        result = handle_broadcast(multiline_content)
        
        assert result is True

    @patch('src.services.messaging_handlers.broadcast_message')
    def test_handle_broadcast_unicode(self, mock_broadcast):
        """Test handle_broadcast with unicode content."""
        mock_broadcast.return_value = True
        
        unicode_content = "Unicode test: émojis 🚀 and 中文"
        result = handle_broadcast(unicode_content)
        
        assert result is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

