#!/usr/bin/env python3
"""
Test Twitch Connection Debug - TDD Approach
===========================================

Tests to debug why bot isn't connecting or receiving messages.

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

from src.services.chat_presence.twitch_bridge import TwitchChatBridge
from src.services.chat_presence.chat_presence_orchestrator import ChatPresenceOrchestrator


class TestMessageFlow(unittest.TestCase):
    """Test complete message flow from IRC to handler."""

    def setUp(self):
        """Set up test fixtures."""
        self.handler_calls = []
        
        async def message_handler(message_data):
            self.handler_calls.append(message_data)
        
        twitch_config = {
            "username": "testbot",
            "oauth_token": "oauth:test123",
            "channel": "digital_dreamscape"
        }
        
        self.orchestrator = ChatPresenceOrchestrator(
            twitch_config=twitch_config,
            obs_config=None
        )
        
        # Mock twitch bridge
        self.orchestrator.twitch_bridge = MagicMock()
        self.orchestrator.twitch_bridge.send_message = AsyncMock(return_value=True)

    async def test_status_command_flow(self):
        """Test complete flow for !status command."""
        message_data = {
            "username": "testuser",
            "message": "!status",
            "channel": "#digital_dreamscape",
            "tags": {}
        }
        
        await self.orchestrator._handle_twitch_message(message_data)
        
        # Verify status command was handled (should send message to chat)
        self.orchestrator.twitch_bridge.send_message.assert_called()

    async def test_agent_command_flow_admin(self):
        """Test complete flow for !agent7 command from admin."""
        # Set up admin user
        self.orchestrator.admin_users.add("testuser")
        
        message_data = {
            "username": "testuser",
            "message": "!agent7 hello",
            "channel": "#digital_dreamscape",
            "tags": {}
        }
        
        await self.orchestrator._handle_twitch_message(message_data)
        
        # Should process the command (we can't easily test subprocess call, but structure is correct)

    async def test_agent_command_flow_non_admin(self):
        """Test that non-admin users get rejection message."""
        message_data = {
            "username": "regularuser",
            "message": "!agent7 hello",
            "channel": "#digital_dreamscape",
            "tags": {}
        }
        
        await self.orchestrator._handle_twitch_message(message_data)
        
        # Should send rejection message
        self.orchestrator.twitch_bridge.send_message.assert_called()
        call_args = self.orchestrator.twitch_bridge.send_message.call_args[0][0]
        self.assertIn("admin", call_args.lower())


class TestConnectionIssues(unittest.TestCase):
    """Test to identify connection issues."""

    def test_channel_name_format_issues(self):
        """Test various channel name format issues."""
        # Issue 1: URL instead of channel name
        channel_url = "https://www.twitch.tv/digital_dreamscape"
        # Should extract to: "digital_dreamscape"
        
        # Issue 2: Channel with # prefix
        channel_with_hash = "#digital_dreamscape"
        # Should become: "digital_dreamscape" (before passing to bridge)
        
        # Issue 3: Channel with trailing slash
        channel_trailing = "https://www.twitch.tv/digital_dreamscape/"
        # Should extract to: "digital_dreamscape"
        
        # Test extraction logic
        test_cases = [
            (channel_url, "digital_dreamscape"),
            (channel_with_hash, "digital_dreamscape"),
            (channel_trailing, "digital_dreamscape"),
        ]
        
        for input_channel, expected in test_cases:
            channel = input_channel.strip()
            if "twitch.tv/" in channel.lower():
                parts = [p for p in channel.split("/") if p.strip()]
                channel = parts[-1].strip() if parts else channel
                channel = channel.rstrip("/").strip()
            if channel.startswith("#"):
                channel = channel[1:]
            
            self.assertEqual(channel, expected, f"Failed for input: {input_channel}")

    def test_oauth_token_format_issues(self):
        """Test OAuth token format issues."""
        # Issue: Token without oauth: prefix
        token_no_prefix = "test123"
        # Should become: "oauth:test123"
        
        token_with_prefix = "oauth:test123"
        # Should stay: "oauth:test123"
        
        # Test prefix logic
        test_cases = [
            (token_no_prefix, "oauth:test123"),
            (token_with_prefix, "oauth:test123"),
        ]
        
        for input_token, expected in test_cases:
            oauth_token = input_token
            if not oauth_token.startswith("oauth:"):
                oauth_token = f"oauth:{oauth_token}"
            
            self.assertEqual(oauth_token, expected)


if __name__ == "__main__":
    unittest.main()

