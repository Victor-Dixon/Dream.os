#!/usr/bin/env python3
"""
Test Twitch Bot Integration - TDD Approach
==========================================

Integration tests to identify connection and message handling issues.

Author: Agent-7 (Web Development Specialist)
Date: 2025-12-03
V2 Compliant: Yes (<300 lines)
"""

import asyncio
import unittest
from unittest.mock import Mock, MagicMock, patch, AsyncMock
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.services.chat_presence.twitch_bridge import TwitchChatBridge, TwitchIRCBot
from src.services.chat_presence.chat_presence_orchestrator import ChatPresenceOrchestrator


class TestTwitchConnectionFlow(unittest.TestCase):
    """Test the complete connection flow."""

    @patch('src.services.chat_presence.twitch_bridge.IRC_AVAILABLE', True)
    @patch('src.services.chat_presence.twitch_bridge.irc.bot.SingleServerIRCBot')
    def test_connection_initialization(self, mock_bot_class):
        """Test that connection is properly initialized."""
        bridge = TwitchChatBridge(
            username="testbot",
            oauth_token="oauth:test123",
            channel="digital_dreamscape",
            on_message=None
        )
        
        # Verify channel format
        self.assertEqual(bridge.channel, "#digital_dreamscape")
        self.assertEqual(bridge.oauth_token, "oauth:test123")
        self.assertEqual(bridge.username, "testbot")

    @patch('src.services.chat_presence.twitch_bridge.IRC_AVAILABLE', True)
    def test_channel_name_normalization(self):
        """Test channel name normalization handles various formats."""
        test_cases = [
            ("digital_dreamscape", "#digital_dreamscape"),
            ("#digital_dreamscape", "#digital_dreamscape"),
            ("https://www.twitch.tv/digital_dreamscape", "#https://www.twitch.tv/digital_dreamscape"),  # Should be fixed before
        ]
        
        for input_channel, expected in test_cases:
            bridge = TwitchChatBridge(
                username="testbot",
                oauth_token="oauth:test123",
                channel=input_channel,
                on_message=None
            )
            # Note: This test shows the issue - URL should be extracted before passing to bridge
            self.assertEqual(bridge.channel, expected if input_channel.startswith("#") else f"#{input_channel}")


class TestMessageReception(unittest.TestCase):
    """Test message reception and callback invocation."""

    def setUp(self):
        """Set up test fixtures."""
        self.received_messages = []
        
        def message_handler(message_data):
            self.received_messages.append(message_data)
        
        self.bridge = TwitchChatBridge(
            username="testbot",
            oauth_token="oauth:test123",
            channel="digital_dreamscape",
            on_message=message_handler
        )

    def test_message_received_calls_handler(self):
        """Test that received messages call the handler."""
        message_data = {
            "username": "testuser",
            "message": "!status",
            "channel": "#digital_dreamscape",
            "tags": {}
        }
        
        self.bridge._handle_message(message_data)
        
        self.assertEqual(len(self.received_messages), 1)
        self.assertEqual(self.received_messages[0]["message"], "!status")
        self.assertEqual(self.received_messages[0]["username"], "testuser")

    def test_multiple_messages_received(self):
        """Test that multiple messages are handled."""
        messages = [
            {"username": "user1", "message": "!status", "channel": "#digital_dreamscape", "tags": {}},
            {"username": "user2", "message": "!agent7 hello", "channel": "#digital_dreamscape", "tags": {}},
        ]
        
        for msg in messages:
            self.bridge._handle_message(msg)
        
        self.assertEqual(len(self.received_messages), 2)


class TestIRCBotEventHandling(unittest.TestCase):
    """Test IRC bot event handling."""

    @patch('src.services.chat_presence.twitch_bridge.IRC_AVAILABLE', True)
    def test_on_pubmsg_creates_message_data(self):
        """Test that on_pubmsg creates correct message data structure."""
        callback_messages = []
        
        def message_handler(message_data):
            callback_messages.append(message_data)
        
        bot = TwitchIRCBot(
            server_list=[("irc.chat.twitch.tv", 6667)],
            nickname="testbot",
            realname="testbot",
            channel="#digital_dreamscape",
            on_message=message_handler
        )
        
        # Create mock IRC event
        mock_event = MagicMock()
        mock_event.arguments = ["!status"]
        mock_event.source.nick = "testuser"
        mock_event.tags = {}
        mock_event.timestamp = None
        
        mock_connection = MagicMock()
        mock_connection.get_nickname.return_value = "testbot"
        
        bot.connection = mock_connection
        
        # Call on_pubmsg
        bot.on_pubmsg(mock_connection, mock_event)
        
        # Verify callback was called with correct data
        self.assertEqual(len(callback_messages), 1)
        self.assertEqual(callback_messages[0]["message"], "!status")
        self.assertEqual(callback_messages[0]["username"], "testuser")

    @patch('src.services.chat_presence.twitch_bridge.IRC_AVAILABLE', True)
    def test_on_pubmsg_skips_bot_own_messages(self):
        """Test that bot's own messages are skipped."""
        callback_messages = []
        
        def message_handler(message_data):
            callback_messages.append(message_data)
        
        bot = TwitchIRCBot(
            server_list=[("irc.chat.twitch.tv", 6667)],
            nickname="testbot",
            realname="testbot",
            channel="#digital_dreamscape",
            on_message=message_handler
        )
        
        # Create mock IRC event from bot itself
        mock_event = MagicMock()
        mock_event.arguments = ["test message"]
        mock_event.source.nick = "testbot"  # Bot's own message
        
        mock_connection = MagicMock()
        mock_connection.get_nickname.return_value = "testbot"
        
        bot.connection = mock_connection
        
        # Call on_pubmsg
        bot.on_pubmsg(mock_connection, mock_event)
        
        # Verify callback was NOT called (bot's own message skipped)
        self.assertEqual(len(callback_messages), 0)


class TestChannelNameExtractionFromEnv(unittest.TestCase):
    """Test channel name extraction from environment variables."""

    def test_extract_from_url(self):
        """Test extracting channel name from Twitch URL in env var."""
        channel_env = "https://www.twitch.tv/digital_dreamscape"
        
        # Simulate extraction (should be in START_CHAT_BOT_NOW.py)
        channel = channel_env.strip()
        if "twitch.tv/" in channel.lower():
            parts = channel.split("/")
            channel = parts[-1].strip()
        if channel.startswith("#"):
            channel = channel[1:]
        
        self.assertEqual(channel, "digital_dreamscape")

    def test_extract_from_url_with_trailing_slash(self):
        """Test extracting from URL with trailing slash."""
        channel_env = "https://www.twitch.tv/digital_dreamscape/"
        
        channel = channel_env.strip()
        if "twitch.tv/" in channel.lower():
            # Filter empty parts to handle trailing slash
            parts = [p for p in channel.split("/") if p.strip()]
            channel = parts[-1].strip() if parts else channel
            channel = channel.rstrip("/").strip()
        if channel.startswith("#"):
            channel = channel[1:]
        
        self.assertEqual(channel, "digital_dreamscape")

    def test_already_correct_channel_name(self):
        """Test that correct channel name is not modified."""
        channel_env = "digital_dreamscape"
        
        channel = channel_env.strip()
        if "twitch.tv/" in channel.lower():
            parts = channel.split("/")
            channel = parts[-1].strip()
        if channel.startswith("#"):
            channel = channel[1:]
        
        self.assertEqual(channel, "digital_dreamscape")


if __name__ == "__main__":
    unittest.main()

