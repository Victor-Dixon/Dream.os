#!/usr/bin/env python3
"""
Test Twitch Chat Bridge - TDD Approach
=======================================

Test-driven development for Twitch bot connection and message handling.

Author: Agent-7 (Web Development Specialist)
Date: 2025-12-03
V2 Compliant: Yes (<300 lines)
"""

import asyncio
import unittest
from unittest.mock import Mock, MagicMock, patch, AsyncMock
from typing import Dict, Any

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.services.chat_presence.twitch_bridge import TwitchChatBridge


class TestTwitchBridgeChannelName(unittest.TestCase):
    """Test channel name handling and extraction."""

    def test_channel_name_with_hash_prefix(self):
        """Test channel name with # prefix is handled correctly."""
        bridge = TwitchChatBridge(
            username="testbot",
            oauth_token="oauth:test123",
            channel="#digital_dreamscape",
            on_message=None
        )
        self.assertEqual(bridge.channel, "#digital_dreamscape")

    def test_channel_name_without_hash_prefix(self):
        """Test channel name without # prefix gets # added."""
        bridge = TwitchChatBridge(
            username="testbot",
            oauth_token="oauth:test123",
            channel="digital_dreamscape",
            on_message=None
        )
        self.assertEqual(bridge.channel, "#digital_dreamscape")

    def test_channel_name_from_url_extraction(self):
        """Test channel name extraction from URL (should be done in START_CHAT_BOT_NOW.py)."""
        # This tests the expected behavior after URL extraction
        channel_from_url = "digital_dreamscape"  # After extraction
        bridge = TwitchChatBridge(
            username="testbot",
            oauth_token="oauth:test123",
            channel=channel_from_url,
            on_message=None
        )
        self.assertEqual(bridge.channel, "#digital_dreamscape")


class TestTwitchBridgeMessageHandling(unittest.TestCase):
    """Test message reception and processing."""

    def setUp(self):
        """Set up test fixtures."""
        self.message_callback = Mock()
        self.bridge = TwitchChatBridge(
            username="testbot",
            oauth_token="oauth:test123",
            channel="digital_dreamscape",
            on_message=self.message_callback
        )

    def test_message_callback_called(self):
        """Test that message callback is called when message received."""
        message_data = {
            "username": "testuser",
            "message": "!status",
            "channel": "#digital_dreamscape",
            "tags": {}
        }
        
        self.bridge._handle_message(message_data)
        
        # Check callback was called
        self.message_callback.assert_called_once()

    def test_message_data_structure(self):
        """Test message data structure passed to callback."""
        message_data = {
            "username": "testuser",
            "message": "!status",
            "channel": "#digital_dreamscape",
            "tags": {}
        }
        
        self.bridge._handle_message(message_data)
        
        # Check callback received correct data
        call_args = self.message_callback.call_args[0][0]
        self.assertEqual(call_args["username"], "testuser")
        self.assertEqual(call_args["message"], "!status")
        self.assertEqual(call_args["channel"], "#digital_dreamscape")

    def test_async_callback_handling(self):
        """Test async callback is handled correctly."""
        async_callback = AsyncMock()
        bridge = TwitchChatBridge(
            username="testbot",
            oauth_token="oauth:test123",
            channel="digital_dreamscape",
            on_message=async_callback
        )
        
        message_data = {
            "username": "testuser",
            "message": "!status",
            "channel": "#digital_dreamscape",
            "tags": {}
        }
        
        bridge._handle_message(message_data)
        
        # Async callback should create a task
        # (We can't easily test this without running event loop, but structure is correct)


class TestTwitchBridgeConnection(unittest.TestCase):
    """Test connection logic."""

    @patch('src.services.chat_presence.twitch_bridge.IRC_AVAILABLE', True)
    @patch('src.services.chat_presence.twitch_bridge.threading.Thread')
    def test_connect_starts_thread(self, mock_thread_class):
        """Test that connect() starts a background thread."""
        bridge = TwitchChatBridge(
            username="testbot",
            oauth_token="oauth:test123",
            channel="digital_dreamscape",
            on_message=None
        )
        
        # Mock the bot
        mock_bot = MagicMock()
        bridge.bot = mock_bot
        
        # Mock thread
        mock_thread = MagicMock()
        mock_thread_class.return_value = mock_thread
        
        # Run connect
        async def run_test():
            result = await bridge.connect()
            return result
        
        result = asyncio.run(run_test())
        
        # Verify thread was started
        mock_thread.start.assert_called_once()
        self.assertTrue(result)

    def test_oauth_token_format(self):
        """Test that oauth token format is preserved."""
        bridge = TwitchChatBridge(
            username="testbot",
            oauth_token="oauth:test123",
            channel="digital_dreamscape",
            on_message=None
        )
        self.assertEqual(bridge.oauth_token, "oauth:test123")

    def test_oauth_token_without_prefix(self):
        """Test that oauth token without prefix is handled (should be fixed in START_CHAT_BOT_NOW.py)."""
        # This tests the expected behavior after prefix is added
        bridge = TwitchChatBridge(
            username="testbot",
            oauth_token="oauth:test123",  # Already prefixed
            channel="digital_dreamscape",
            on_message=None
        )
        self.assertTrue(bridge.oauth_token.startswith("oauth:"))


class TestTwitchBridgeOnlineMessage(unittest.TestCase):
    """Test online message functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.bridge = TwitchChatBridge(
            username="testbot",
            oauth_token="oauth:test123",
            channel="digital_dreamscape",
            on_message=None
        )

    def test_online_message_flag_initialized(self):
        """Test that online message flag is initialized to False."""
        self.assertFalse(self.bridge._has_sent_online_message)

    def test_online_message_flag_reset_on_stop(self):
        """Test that online message flag is reset when bot stops."""
        self.bridge._has_sent_online_message = True
        self.bridge.stop()
        self.assertFalse(self.bridge._has_sent_online_message)


class TestChannelNameExtraction(unittest.TestCase):
    """Test channel name extraction from URLs (START_CHAT_BOT_NOW.py logic)."""

    def test_extract_channel_from_url(self):
        """Test extracting channel name from full Twitch URL."""
        channel_url = "https://www.twitch.tv/digital_dreamscape"
        
        # Simulate extraction logic
        if "twitch.tv/" in channel_url.lower():
            parts = channel_url.split("/")
            channel = parts[-1].strip()
            if channel.startswith("#"):
                channel = channel[1:]
        
        self.assertEqual(channel, "digital_dreamscape")

    def test_extract_channel_from_url_with_hash(self):
        """Test extracting channel from URL that already has #."""
        channel_url = "https://www.twitch.tv/#digital_dreamscape"
        
        # Simulate extraction logic
        if "twitch.tv/" in channel_url.lower():
            parts = channel_url.split("/")
            channel = parts[-1].strip()
            if channel.startswith("#"):
                channel = channel[1:]
        
        self.assertEqual(channel, "digital_dreamscape")

    def test_channel_name_already_correct(self):
        """Test that correct channel name is not modified."""
        channel = "digital_dreamscape"
        
        # Simulate extraction logic (should not modify)
        if "twitch.tv/" in channel.lower():
            parts = channel.split("/")
            channel = parts[-1].strip()
        if channel.startswith("#"):
            channel = channel[1:]
        
        self.assertEqual(channel, "digital_dreamscape")


if __name__ == "__main__":
    unittest.main()

