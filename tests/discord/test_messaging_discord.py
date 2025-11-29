#!/usr/bin/env python3
"""
Tests for Messaging Discord Integration
========================================

Comprehensive tests for Discord messaging service integration.

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-01-27
"""

import pytest
from unittest.mock import patch, MagicMock


class TestMessagingDiscord:
    """Test suite for Discord messaging integration."""

    def test_send_discord_message_success(self):
        """Test successful Discord message sending."""
        from src.services.messaging_discord import send_discord_message
        from src.core.messaging_core import UnifiedMessagePriority
        
        with patch('src.services.messaging_discord.send_message') as mock_send:
            mock_send.return_value = True
            
            result = send_discord_message(
                content="Test message",
                channel_id="123456789",
                priority=UnifiedMessagePriority.REGULAR
            )
            
            assert result is True
            mock_send.assert_called_once()
            
            # Verify call arguments
            call_args = mock_send.call_args
            assert call_args[1]['content'] == "Test message"
            assert call_args[1]['recipient'] == "123456789"
            assert call_args[1]['sender'] == "DISCORD"
            assert call_args[1]['priority'] == UnifiedMessagePriority.REGULAR

    def test_send_discord_message_urgent_priority(self):
        """Test Discord message with urgent priority."""
        from src.services.messaging_discord import send_discord_message
        from src.core.messaging_core import UnifiedMessagePriority, UnifiedMessageType, UnifiedMessageTag
        
        with patch('src.services.messaging_discord.send_message') as mock_send:
            mock_send.return_value = True
            
            result = send_discord_message(
                content="Urgent message",
                channel_id="987654321",
                priority=UnifiedMessagePriority.URGENT
            )
            
            assert result is True
            call_args = mock_send.call_args
            assert call_args[1]['priority'] == UnifiedMessagePriority.URGENT

    def test_send_discord_message_default_priority(self):
        """Test Discord message with default priority."""
        from src.services.messaging_discord import send_discord_message
        from src.core.messaging_core import UnifiedMessagePriority
        
        with patch('src.services.messaging_discord.send_message') as mock_send:
            mock_send.return_value = True
            
            # Don't specify priority - should default to REGULAR
            result = send_discord_message(
                content="Default priority message",
                channel_id="111222333"
            )
            
            assert result is True
            call_args = mock_send.call_args
            assert call_args[1]['priority'] == UnifiedMessagePriority.REGULAR

    def test_send_discord_message_tags(self):
        """Test Discord message includes correct tags."""
        from src.services.messaging_discord import send_discord_message
        from src.core.messaging_core import UnifiedMessageTag, UnifiedMessageType
        
        with patch('src.services.messaging_discord.send_message') as mock_send:
            mock_send.return_value = True
            
            send_discord_message(
                content="Tagged message",
                channel_id="444555666"
            )
            
            call_args = mock_send.call_args
            tags = call_args[1]['tags']
            
            assert UnifiedMessageTag.SYSTEM in tags
            assert UnifiedMessageTag.BROADCAST in tags
            assert len(tags) == 2

    def test_send_discord_message_type(self):
        """Test Discord message uses BROADCAST type."""
        from src.services.messaging_discord import send_discord_message
        from src.core.messaging_core import UnifiedMessageType
        
        with patch('src.services.messaging_discord.send_message') as mock_send:
            mock_send.return_value = True
            
            send_discord_message(
                content="Broadcast message",
                channel_id="777888999"
            )
            
            call_args = mock_send.call_args
            assert call_args[1]['message_type'] == UnifiedMessageType.BROADCAST

    def test_send_discord_message_failure(self):
        """Test Discord message sending failure."""
        from src.services.messaging_discord import send_discord_message
        
        with patch('src.services.messaging_discord.send_message') as mock_send:
            mock_send.return_value = False
            
            result = send_discord_message(
                content="Failed message",
                channel_id="000111222"
            )
            
            assert result is False

    def test_send_discord_message_exception_handling(self):
        """Test Discord message exception handling."""
        from src.services.messaging_discord import send_discord_message
        
        with patch('src.services.messaging_discord.send_message') as mock_send:
            mock_send.side_effect = Exception("Network error")
            
            # Should propagate exception
            with pytest.raises(Exception) as exc_info:
                send_discord_message(
                    content="Error message",
                    channel_id="333444555"
                )
            
            assert "Network error" in str(exc_info.value)

    def test_send_discord_message_long_content(self):
        """Test Discord message with long content."""
        from src.services.messaging_discord import send_discord_message
        
        long_content = "A" * 2000  # Long message
        
        with patch('src.services.messaging_discord.send_message') as mock_send:
            mock_send.return_value = True
            
            result = send_discord_message(
                content=long_content,
                channel_id="666777888"
            )
            
            assert result is True
            call_args = mock_send.call_args
            assert call_args[1]['content'] == long_content

    def test_send_discord_message_empty_content(self):
        """Test Discord message with empty content."""
        from src.services.messaging_discord import send_discord_message
        
        with patch('src.services.messaging_discord.send_message') as mock_send:
            mock_send.return_value = True
            
            result = send_discord_message(
                content="",
                channel_id="999000111"
            )
            
            assert result is True
            call_args = mock_send.call_args
            assert call_args[1]['content'] == ""

    def test_send_discord_message_integration(self):
        """Test Discord message integration with messaging core."""
        from src.services.messaging_discord import send_discord_message
        from src.core.messaging_core import (
            UnifiedMessagePriority,
            UnifiedMessageType,
            UnifiedMessageTag
        )
        
        with patch('src.services.messaging_discord.send_message') as mock_send:
            mock_send.return_value = True
            
            send_discord_message(
                content="Integration test",
                channel_id="channel_123",
                priority=UnifiedMessagePriority.URGENT
            )
            
            # Verify all parameters passed correctly
            call_args = mock_send.call_args
            assert call_args[1]['content'] == "Integration test"
            assert call_args[1]['sender'] == "DISCORD"
            assert call_args[1]['recipient'] == "channel_123"
            assert call_args[1]['message_type'] == UnifiedMessageType.BROADCAST
            assert call_args[1]['priority'] == UnifiedMessagePriority.URGENT
            assert UnifiedMessageTag.SYSTEM in call_args[1]['tags']
            assert UnifiedMessageTag.BROADCAST in call_args[1]['tags']
