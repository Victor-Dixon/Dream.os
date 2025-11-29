"""
Expanded unit tests for unified_messaging_service.py - Batch 9

Additional tests for comprehensive coverage.
"""

from unittest.mock import Mock, patch
import pytest

from src.services.unified_messaging_service import UnifiedMessagingService, MessagingService


class TestUnifiedMessagingServiceExpanded:
    """Expanded tests for UnifiedMessagingService."""

    @patch("src.services.unified_messaging_service.ConsolidatedMessagingService")
    def test_send_message_long_content(self, mock_consolidated):
        """Test send_message with very long content."""
        mock_instance = Mock()
        mock_instance.send_message.return_value = {"success": True, "message": "Sent"}
        mock_consolidated.return_value = mock_instance
        
        service = UnifiedMessagingService()
        long_content = "A" * 10000
        result = service.send_message("Agent-1", long_content, "regular", True)
        
        assert result["success"] is True
        mock_instance.send_message.assert_called_once()

    @patch("src.services.unified_messaging_service.ConsolidatedMessagingService")
    def test_send_message_special_characters(self, mock_consolidated):
        """Test send_message with special characters."""
        mock_instance = Mock()
        mock_instance.send_message.return_value = {"success": True, "message": "Sent"}
        mock_consolidated.return_value = mock_instance
        
        service = UnifiedMessagingService()
        special_content = "Test: !@#$%^&*()_+-=[]{}|;':\",./<>?"
        result = service.send_message("Agent-1", special_content, "regular", True)
        
        assert result["success"] is True

    @patch("src.services.unified_messaging_service.ConsolidatedMessagingService")
    def test_send_message_multiline(self, mock_consolidated):
        """Test send_message with multiline content."""
        mock_instance = Mock()
        mock_instance.send_message.return_value = {"success": True, "message": "Sent"}
        mock_consolidated.return_value = mock_instance
        
        service = UnifiedMessagingService()
        multiline_content = "Line 1\nLine 2\nLine 3"
        result = service.send_message("Agent-1", multiline_content, "regular", True)
        
        assert result["success"] is True

    @patch("src.services.unified_messaging_service.ConsolidatedMessagingService")
    def test_broadcast_message_long_content(self, mock_consolidated):
        """Test broadcast_message with very long content."""
        mock_instance = Mock()
        mock_instance.broadcast_message.return_value = {"success": True, "results": {}}
        mock_consolidated.return_value = mock_instance
        
        service = UnifiedMessagingService()
        long_content = "B" * 10000
        result = service.broadcast_message(long_content, "regular")
        
        assert result["success"] is True

    @patch("src.services.unified_messaging_service.ConsolidatedMessagingService")
    def test_broadcast_message_special_characters(self, mock_consolidated):
        """Test broadcast_message with special characters."""
        mock_instance = Mock()
        mock_instance.broadcast_message.return_value = {"success": True, "results": {}}
        mock_consolidated.return_value = mock_instance
        
        service = UnifiedMessagingService()
        special_content = "Broadcast: !@#$%^&*()"
        result = service.broadcast_message(special_content, "regular")
        
        assert result["success"] is True

    @patch("src.services.unified_messaging_service.ConsolidatedMessagingService")
    def test_send_message_all_agents(self, mock_consolidated):
        """Test send_message with all agent IDs."""
        mock_instance = Mock()
        mock_instance.send_message.return_value = {"success": True, "message": "Sent"}
        mock_consolidated.return_value = mock_instance
        
        service = UnifiedMessagingService()
        agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
        
        for agent in agents:
            result = service.send_message(agent, "Test", "regular", True)
            assert result["success"] is True
        
        assert mock_instance.send_message.call_count == 8

    @patch("src.services.unified_messaging_service.ConsolidatedMessagingService")
    def test_broadcast_message_all_priorities(self, mock_consolidated):
        """Test broadcast_message with all priority levels."""
        mock_instance = Mock()
        mock_instance.broadcast_message.return_value = {"success": True, "results": {}}
        mock_consolidated.return_value = mock_instance
        
        service = UnifiedMessagingService()
        priorities = ["regular", "urgent"]
        
        for priority in priorities:
            result = service.broadcast_message("Test", priority)
            assert result["success"] is True
        
        assert mock_instance.broadcast_message.call_count == 2

    @patch("src.services.unified_messaging_service.ConsolidatedMessagingService")
    def test_messaging_service_alias_initialization(self, mock_consolidated):
        """Test MessagingService alias can be initialized."""
        mock_instance = Mock()
        mock_consolidated.return_value = mock_instance
        
        service = MessagingService()
        assert service.messaging is not None
        assert isinstance(service, UnifiedMessagingService)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

