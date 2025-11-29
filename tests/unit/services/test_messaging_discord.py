"""
Tests for messaging_discord.py

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys

# Add project root to path
project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))

from src.services import messaging_discord
from src.core.messaging_core import UnifiedMessagePriority, UnifiedMessageTag, UnifiedMessageType


class TestMessagingDiscord:
    """Test messaging_discord module."""

    @patch('src.services.messaging_discord.send_message')
    def test_send_discord_message_default_priority(self, mock_send_message):
        """Test send_discord_message with default priority."""
        mock_send_message.return_value = True
        
        result = messaging_discord.send_discord_message(
            content="Test message",
            channel_id="channel_123"
        )
        
        assert result is True
        mock_send_message.assert_called_once()
        call_args = mock_send_message.call_args
        
        assert call_args.kwargs['content'] == "Test message"
        assert call_args.kwargs['sender'] == "DISCORD"
        assert call_args.kwargs['recipient'] == "channel_123"
        assert call_args.kwargs['message_type'] == UnifiedMessageType.BROADCAST
        assert call_args.kwargs['priority'] == UnifiedMessagePriority.REGULAR
        assert UnifiedMessageTag.SYSTEM in call_args.kwargs['tags']
        assert UnifiedMessageTag.COORDINATION in call_args.kwargs['tags']

    @patch('src.services.messaging_discord.send_message')
    def test_send_discord_message_urgent_priority(self, mock_send_message):
        """Test send_discord_message with urgent priority."""
        mock_send_message.return_value = True
        
        result = messaging_discord.send_discord_message(
            content="Urgent message",
            channel_id="channel_456",
            priority=UnifiedMessagePriority.URGENT
        )
        
        assert result is True
        call_args = mock_send_message.call_args
        assert call_args.kwargs['priority'] == UnifiedMessagePriority.URGENT

    @patch('src.services.messaging_discord.send_message')
    def test_send_discord_message_with_tags(self, mock_send_message):
        """Test send_discord_message includes correct tags."""
        mock_send_message.return_value = True
        
        messaging_discord.send_discord_message(
            content="Tagged message",
            channel_id="channel_789"
        )
        
        call_args = mock_send_message.call_args
        tags = call_args.kwargs['tags']
        
        assert UnifiedMessageTag.SYSTEM in tags
        assert UnifiedMessageTag.COORDINATION in tags
        assert len(tags) == 2

    @patch('src.services.messaging_discord.send_message')
    def test_send_discord_message_broadcast_type(self, mock_send_message):
        """Test send_discord_message uses BROADCAST message type."""
        mock_send_message.return_value = True
        
        messaging_discord.send_discord_message(
            content="Broadcast message",
            channel_id="channel_abc"
        )
        
        call_args = mock_send_message.call_args
        assert call_args.kwargs['message_type'] == UnifiedMessageType.BROADCAST

    @patch('src.services.messaging_discord.send_message')
    def test_send_discord_message_sender_is_discord(self, mock_send_message):
        """Test send_discord_message sets sender as DISCORD."""
        mock_send_message.return_value = True
        
        messaging_discord.send_discord_message(
            content="Test",
            channel_id="channel_xyz"
        )
        
        call_args = mock_send_message.call_args
        assert call_args.kwargs['sender'] == "DISCORD"

    @patch('src.services.messaging_discord.send_message')
    def test_send_discord_message_failure_handling(self, mock_send_message):
        """Test send_discord_message returns False on failure."""
        mock_send_message.return_value = False
        
        result = messaging_discord.send_discord_message(
            content="Failed message",
            channel_id="channel_fail"
        )
        
        assert result is False

    @patch('src.services.messaging_discord.send_message')
    def test_send_discord_message_different_channel_ids(self, mock_send_message):
        """Test send_discord_message with different channel IDs."""
        mock_send_message.return_value = True
        
        channel_ids = ["channel_1", "channel_2", "123456789", "special-channel"]
        
        for channel_id in channel_ids:
            messaging_discord.send_discord_message(
                content=f"Message to {channel_id}",
                channel_id=channel_id
            )
            
            call_args = mock_send_message.call_args
            assert call_args.kwargs['recipient'] == channel_id

    @patch('src.services.messaging_discord.send_message')
    def test_send_discord_message_long_content(self, mock_send_message):
        """Test send_discord_message with long content."""
        mock_send_message.return_value = True
        long_content = "A" * 1000
        
        result = messaging_discord.send_discord_message(
            content=long_content,
            channel_id="channel_long"
        )
        
        assert result is True
        call_args = mock_send_message.call_args
        assert call_args.kwargs['content'] == long_content

    @patch('src.services.messaging_discord.send_message')
    def test_send_discord_message_empty_content(self, mock_send_message):
        """Test send_discord_message with empty content."""
        mock_send_message.return_value = True
        
        result = messaging_discord.send_discord_message(
            content="",
            channel_id="channel_empty"
        )
        
        assert result is True
        call_args = mock_send_message.call_args
        assert call_args.kwargs['content'] == ""

    @patch('src.services.messaging_discord.send_message')
    def test_send_discord_message_exception_handling(self, mock_send_message):
        """Test send_discord_message exception handling."""
        mock_send_message.side_effect = Exception("Send error")
        
        # Should propagate exception
        with pytest.raises(Exception):
            messaging_discord.send_discord_message(
                content="Test",
                channel_id="channel_error"
            )

    @patch('src.services.messaging_discord.send_message')
    def test_send_discord_message_all_priorities(self, mock_send_message):
        """Test send_discord_message with all priority levels."""
        mock_send_message.return_value = True
        
        priorities = [
            UnifiedMessagePriority.REGULAR,
            UnifiedMessagePriority.URGENT,
            UnifiedMessagePriority.HIGH,
            UnifiedMessagePriority.NORMAL
        ]
        
        for priority in priorities:
            if hasattr(UnifiedMessagePriority, priority.name if hasattr(priority, 'name') else str(priority)):
                messaging_discord.send_discord_message(
                    content="Test",
                    channel_id="channel",
                    priority=priority
                )
                call_args = mock_send_message.call_args
                assert call_args.kwargs['priority'] == priority

    @patch('src.services.messaging_discord.send_message')
    def test_send_discord_message_tags_immutability(self, mock_send_message):
        """Test that tags list is properly constructed."""
        mock_send_message.return_value = True
        
        messaging_discord.send_discord_message(
            content="Test",
            channel_id="channel"
        )
        
        call_args = mock_send_message.call_args
        tags = call_args.kwargs['tags']
        
        # Tags should be a list with exactly 2 items
        assert isinstance(tags, list)
        assert len(tags) == 2
        assert UnifiedMessageTag.SYSTEM in tags
        assert UnifiedMessageTag.COORDINATION in tags

    @patch('src.services.messaging_discord.send_message')
    def test_send_discord_message_return_value_propagation(self, mock_send_message):
        """Test that return value from send_message is propagated."""
        mock_send_message.return_value = True
        result = messaging_discord.send_discord_message("Test", "channel")
        assert result is True
        
        mock_send_message.return_value = False
        result = messaging_discord.send_discord_message("Test", "channel")
        assert result is False

    def test_send_discord_message_function_signature(self):
        """Test function signature and default parameters."""
        import inspect
        sig = inspect.signature(messaging_discord.send_discord_message)
        
        assert 'content' in sig.parameters
        assert 'channel_id' in sig.parameters
        assert 'priority' in sig.parameters
        assert sig.parameters['priority'].default == UnifiedMessagePriority.REGULAR

