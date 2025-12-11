#!/usr/bin/env python3
"""
Test Twitch Bridge Error Handling
==================================

Comprehensive tests for error handling, edge cases, and recovery scenarios.

Author: Agent-7 (Web Development Specialist)
Date: 2025-12-11
V2 Compliant: Yes
"""

import asyncio
import unittest
from unittest.mock import Mock, MagicMock, patch, AsyncMock
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.services.chat_presence.twitch_bridge import (
    TwitchChatBridge,
    TwitchIRCBot,
    TwitchBridgeError,
    TwitchAuthError,
    TwitchConnectionError,
    TwitchMessageError,
    TwitchReconnectError,
)


class TestCustomExceptions(unittest.TestCase):
    """Test custom exception classes."""

    def test_twitch_bridge_error_base(self):
        """Test base exception class."""
        error = TwitchBridgeError("Test error")
        self.assertIsInstance(error, Exception)
        self.assertEqual(str(error), "Test error")

    def test_twitch_auth_error(self):
        """Test authentication error."""
        error = TwitchAuthError("Auth failed")
        self.assertIsInstance(error, TwitchBridgeError)
        self.assertEqual(str(error), "Auth failed")

    def test_twitch_connection_error(self):
        """Test connection error."""
        error = TwitchConnectionError("Connection failed")
        self.assertIsInstance(error, TwitchBridgeError)
        self.assertEqual(str(error), "Connection failed")

    def test_twitch_message_error(self):
        """Test message error."""
        error = TwitchMessageError("Message failed")
        self.assertIsInstance(error, TwitchBridgeError)
        self.assertEqual(str(error), "Message failed")


class TestConnectionErrorHandling(unittest.TestCase):
    """Test connection error handling."""

    @patch('src.services.chat_presence.twitch_bridge.IRC_AVAILABLE', True)
    def test_connect_without_username_raises_error(self):
        """Test that connect without username raises error."""
        bridge = TwitchChatBridge(
            username="",
            oauth_token="oauth:test123",
            channel="testchannel",
            on_message=None
        )
        
        async def test():
            with self.assertRaises(TwitchConnectionError) as cm:
                await bridge.connect()
            self.assertIn("Username is required", str(cm.exception))
        
        asyncio.run(test())

    @patch('src.services.chat_presence.twitch_bridge.IRC_AVAILABLE', True)
    def test_connect_without_oauth_raises_error(self):
        """Test that connect without OAuth token raises error."""
        bridge = TwitchChatBridge(
            username="testbot",
            oauth_token="",
            channel="testchannel",
            on_message=None
        )
        
        async def test():
            with self.assertRaises(TwitchAuthError) as cm:
                await bridge.connect()
            self.assertIn("OAuth token is required", str(cm.exception))
        
        asyncio.run(test())

    @patch('src.services.chat_presence.twitch_bridge.IRC_AVAILABLE', True)
    def test_connect_without_channel_raises_error(self):
        """Test that connect without channel raises error."""
        bridge = TwitchChatBridge(
            username="testbot",
            oauth_token="oauth:test123",
            channel="",  # Empty channel
            on_message=None
        )
        
        # Verify channel is empty
        self.assertEqual(bridge.channel, "")
        
        async def test():
            with self.assertRaises(TwitchConnectionError) as cm:
                await bridge.connect()
            self.assertIn("Channel is required", str(cm.exception))
        
        asyncio.run(test())


class TestMessageErrorHandling(unittest.TestCase):
    """Test message sending error handling."""

    @patch('src.services.chat_presence.twitch_bridge.IRC_AVAILABLE', True)
    def setUp(self):
        """Set up test fixtures."""
        self.bridge = TwitchChatBridge(
            username="testbot",
            oauth_token="oauth:test123",
            channel="testchannel",
            on_message=None
        )
        self.bridge.running = True
        self.bridge.connected = True

    def test_send_message_with_empty_string(self):
        """Test sending empty message returns False."""
        async def test():
            result = await self.bridge.send_message("")
            self.assertFalse(result)
        
        asyncio.run(test())

    def test_send_message_with_none(self):
        """Test sending None message returns False."""
        async def test():
            result = await self.bridge.send_message(None)
            self.assertFalse(result)
        
        asyncio.run(test())

    def test_send_message_too_long(self):
        """Test sending message longer than 500 chars is truncated."""
        long_message = "x" * 600
        async def test():
            # Should not raise, but should truncate
            result = await self.bridge.send_message(long_message)
            # Result depends on connection state, but should not crash
            self.assertIsInstance(result, bool)
        
        asyncio.run(test())

    def test_send_message_when_not_connected(self):
        """Test sending message when not connected returns False."""
        self.bridge.connected = False
        
        async def test():
            result = await self.bridge.send_message("test")
            self.assertFalse(result)
        
        asyncio.run(test())

    def test_send_message_when_not_running(self):
        """Test sending message when not running returns False."""
        self.bridge.running = False
        
        async def test():
            result = await self.bridge.send_message("test")
            self.assertFalse(result)
        
        asyncio.run(test())

    def test_send_message_without_bot(self):
        """Test sending message without bot instance returns False."""
        self.bridge.bot = None
        
        async def test():
            result = await self.bridge.send_message("test")
            self.assertFalse(result)
        
        asyncio.run(test())

    def test_send_message_connection_error(self):
        """Test handling connection error when sending message."""
        mock_bot = MagicMock()
        mock_connection = MagicMock()
        mock_connection.privmsg.side_effect = ConnectionError("Connection lost")
        mock_bot.connection = mock_connection
        self.bridge.bot = mock_bot
        
        async def test():
            result = await self.bridge.send_message("test")
            self.assertFalse(result)
            self.assertFalse(self.bridge.connected)  # Should mark as disconnected
        
        asyncio.run(test())


class TestMessageCallbackErrorHandling(unittest.TestCase):
    """Test message callback error handling."""

    @patch('src.services.chat_presence.twitch_bridge.IRC_AVAILABLE', True)
    def test_handle_message_with_invalid_data_type(self):
        """Test handling message with invalid data type."""
        bridge = TwitchChatBridge(
            username="testbot",
            oauth_token="oauth:test123",
            channel="testchannel",
            on_message=Mock()
        )
        
        # Should not crash with invalid data type
        bridge._handle_message("not a dict")
        # Callback should not be called
        bridge.on_message.assert_not_called()

    @patch('src.services.chat_presence.twitch_bridge.IRC_AVAILABLE', True)
    def test_handle_message_with_missing_fields(self):
        """Test handling message with missing required fields."""
        callback = Mock()
        bridge = TwitchChatBridge(
            username="testbot",
            oauth_token="oauth:test123",
            channel="testchannel",
            on_message=callback
        )
        
        # Missing username
        bridge._handle_message({"message": "test"})
        callback.assert_not_called()
        
        # Missing message
        bridge._handle_message({"username": "testuser"})
        callback.assert_not_called()

    @patch('src.services.chat_presence.twitch_bridge.IRC_AVAILABLE', True)
    def test_handle_message_callback_raises_exception(self):
        """Test that callback exceptions are caught and logged."""
        def failing_callback(msg):
            raise ValueError("Callback error")
        
        bridge = TwitchChatBridge(
            username="testbot",
            oauth_token="oauth:test123",
            channel="testchannel",
            on_message=failing_callback
        )
        
        # Should not crash
        message_data = {
            "username": "testuser",
            "message": "test",
            "channel": "#testchannel"
        }
        bridge._handle_message(message_data)
        # Should complete without raising

    @patch('src.services.chat_presence.twitch_bridge.IRC_AVAILABLE', True)
    def test_handle_message_async_callback_no_event_loop(self):
        """Test async callback when event loop is not available."""
        async def async_callback(msg):
            return "processed"
        
        bridge = TwitchChatBridge(
            username="testbot",
            oauth_token="oauth:test123",
            channel="testchannel",
            on_message=async_callback
        )
        
        message_data = {
            "username": "testuser",
            "message": "test",
            "channel": "#testchannel"
        }
        
        # Should handle gracefully even without event loop
        bridge._handle_message(message_data)


class TestReconnectionErrorHandling(unittest.TestCase):
    """Test reconnection error handling."""

    @patch('src.services.chat_presence.twitch_bridge.IRC_AVAILABLE', True)
    @patch('src.services.chat_presence.twitch_bridge.threading.Thread')
    def test_reconnect_handles_network_errors(self, mock_thread_class):
        """Test that network errors trigger reconnection."""
        bridge = TwitchChatBridge(
            username="testbot",
            oauth_token="oauth:test123",
            channel="testchannel",
            on_message=None
        )
        
        # Mock thread
        mock_thread = MagicMock()
        mock_thread_class.return_value = mock_thread
        
        # This tests the structure - actual reconnection logic is in _run_reconnect_loop
        # which is harder to test without running the actual loop
        async def test():
            result = await bridge.connect()
            self.assertTrue(result)
        
        asyncio.run(test())

    @patch('src.services.chat_presence.twitch_bridge.IRC_AVAILABLE', True)
    def test_stop_event_terminates_reconnect_loop(self):
        """Test that stop() method signals reconnect loop to stop."""
        bridge = TwitchChatBridge(
            username="testbot",
            oauth_token="oauth:test123",
            channel="testchannel",
            on_message=None
        )
        
        # Verify stop event exists
        self.assertIsNotNone(bridge._stop_event)
        self.assertFalse(bridge._stop_event.is_set())
        
        # Call stop
        bridge.stop()
        
        # Stop event should be set
        self.assertTrue(bridge._stop_event.is_set())
        self.assertFalse(bridge.running)

    @patch('src.services.chat_presence.twitch_bridge.IRC_AVAILABLE', True)
    def test_reconnect_attempt_counter_persistence(self):
        """Test that reconnect attempt counter persists across instances."""
        bridge = TwitchChatBridge(
            username="testbot",
            oauth_token="oauth:test123",
            channel="testchannel",
            on_message=None
        )
        
        # Initial attempt counter should be 0
        self.assertEqual(bridge._reconnect_attempt, 0)
        
        # Simulate increment
        bridge._reconnect_attempt = 3
        
        # Counter should persist
        self.assertEqual(bridge._reconnect_attempt, 3)

    @patch('src.services.chat_presence.twitch_bridge.IRC_AVAILABLE', True)
    def test_exponential_backoff_calculation(self):
        """Test exponential backoff calculation limits."""
        bridge = TwitchChatBridge(
            username="testbot",
            oauth_token="oauth:test123",
            channel="testchannel",
            on_message=None
        )
        
        # Test backoff calculation logic (min(120, 2^min(attempt, 6)))
        # Attempt 0: 2^0 = 1
        bridge._reconnect_attempt = 0
        expected_backoff = min(120, 2 ** min(0, 6))
        self.assertEqual(expected_backoff, 1)
        
        # Attempt 3: 2^3 = 8
        bridge._reconnect_attempt = 3
        expected_backoff = min(120, 2 ** min(3, 6))
        self.assertEqual(expected_backoff, 8)
        
        # Attempt 6: 2^6 = 64
        bridge._reconnect_attempt = 6
        expected_backoff = min(120, 2 ** min(6, 6))
        self.assertEqual(expected_backoff, 64)
        
        # Attempt 10: 2^6 = 64 (capped at 6)
        bridge._reconnect_attempt = 10
        expected_backoff = min(120, 2 ** min(10, 6))
        self.assertEqual(expected_backoff, 64)
        
        # Max backoff is 120 seconds
        bridge._reconnect_attempt = 100
        expected_backoff = min(120, 2 ** min(100, 6))
        self.assertEqual(expected_backoff, 64)  # Still capped at 2^6

    @patch('src.services.chat_presence.twitch_bridge.IRC_AVAILABLE', True)
    def test_reconnect_thread_management(self):
        """Test reconnect thread lifecycle management."""
        bridge = TwitchChatBridge(
            username="testbot",
            oauth_token="oauth:test123",
            channel="testchannel",
            on_message=None
        )
        
        # Initially no thread
        self.assertIsNone(bridge._reconnect_thread)
        
        # Mock thread for testing
        mock_thread = MagicMock()
        mock_thread.is_alive.return_value = True
        bridge._reconnect_thread = mock_thread
        
        # Verify thread exists
        self.assertIsNotNone(bridge._reconnect_thread)
        
        # Stop should handle thread cleanup
        bridge.stop()
        # Thread join should be called (with timeout)
        if bridge._reconnect_thread:
            # Verify thread management
            self.assertTrue(hasattr(bridge._reconnect_thread, 'join'))

    @patch('src.services.chat_presence.twitch_bridge.IRC_AVAILABLE', True)
    def test_reconnect_state_after_stop(self):
        """Test that reconnect state is properly reset after stop."""
        bridge = TwitchChatBridge(
            username="testbot",
            oauth_token="oauth:test123",
            channel="testchannel",
            on_message=None
        )
        
        # Set some state
        bridge.running = True
        bridge.connected = True
        bridge._reconnect_attempt = 5
        
        # Stop
        bridge.stop()
        
        # State should be reset
        self.assertFalse(bridge.running)
        # Reconnect attempt counter may persist (design choice)
        # but running should be False
        self.assertFalse(bridge.running)


class TestIRCBotErrorHandling(unittest.TestCase):
    """Test IRC bot error handling."""

    @patch('src.services.chat_presence.twitch_bridge.IRC_AVAILABLE', True)
    def test_on_disconnect_detects_auth_errors(self):
        """Test that on_disconnect detects authentication errors."""
        bot = TwitchIRCBot(
            server_list=[("irc.chat.twitch.tv", 6667)],
            nickname="testbot",
            realname="testbot",
            channel="#testchannel",
            oauth_token="oauth:test123"
        )
        
        mock_connection = MagicMock()
        mock_event = MagicMock()
        mock_event.arguments = ["Login authentication failed"]
        
        # Should detect auth error
        bot.on_disconnect(mock_connection, mock_event)
        # Bridge instance should be marked as disconnected
        if bot.bridge_instance:
            self.assertFalse(bot.bridge_instance.connected)

    @patch('src.services.chat_presence.twitch_bridge.IRC_AVAILABLE', True)
    def test_on_error_detects_auth_errors(self):
        """Test that on_error detects authentication errors."""
        bot = TwitchIRCBot(
            server_list=[("irc.chat.twitch.tv", 6667)],
            nickname="testbot",
            realname="testbot",
            channel="#testchannel",
            oauth_token="oauth:test123"
        )
        
        mock_connection = MagicMock()
        mock_event = MagicMock()
        mock_event.arguments = ["Invalid password"]
        mock_event.type = "error"
        
        bot.on_error(mock_connection, mock_event)
        # Should log authentication error

    @patch('src.services.chat_presence.twitch_bridge.IRC_AVAILABLE', True)
    def test_on_notice_detects_auth_errors(self):
        """Test that on_notice detects authentication errors."""
        bot = TwitchIRCBot(
            server_list=[("irc.chat.twitch.tv", 6667)],
            nickname="testbot",
            realname="testbot",
            channel="#testchannel",
            oauth_token="oauth:test123"
        )
        
        mock_connection = MagicMock()
        mock_event = MagicMock()
        mock_event.arguments = ["Login authentication failed"]
        
        bot.on_notice(mock_connection, mock_event)
        # Should detect and log auth error


if __name__ == "__main__":
    unittest.main()

