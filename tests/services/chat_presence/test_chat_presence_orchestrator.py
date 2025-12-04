#!/usr/bin/env python3
"""
Test Chat Presence Orchestrator - TDD Approach
==============================================

Test-driven development for message handling and command processing.

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

from src.services.chat_presence.chat_presence_orchestrator import ChatPresenceOrchestrator
from src.services.chat_presence.message_interpreter import MessageInterpreter


class TestMessageInterpreter(unittest.TestCase):
    """Test message interpretation and command detection."""

    def setUp(self):
        """Set up test fixtures."""
        self.interpreter = MessageInterpreter()

    def test_status_command_detection(self):
        """Test that status commands are detected."""
        self.assertTrue(self.interpreter.is_status_command("!status"))
        self.assertTrue(self.interpreter.is_status_command("!swarm"))
        self.assertTrue(self.interpreter.is_status_command("!agents"))
        self.assertFalse(self.interpreter.is_status_command("!agent7 hello"))

    def test_status_command_parsing_all(self):
        """Test parsing status command for all agents."""
        cmd_type, agent_id = self.interpreter.parse_status_command("!status")
        self.assertEqual(cmd_type, "all")
        self.assertIsNone(agent_id)

    def test_status_command_parsing_specific_agent(self):
        """Test parsing status command for specific agent."""
        cmd_type, agent_id = self.interpreter.parse_status_command("!status agent7")
        self.assertEqual(cmd_type, "agent")
        self.assertEqual(agent_id, "Agent-7")

    def test_agent_command_detection(self):
        """Test that agent commands are detected."""
        agent_id = self.interpreter._check_explicit_command("!agent7 hello")
        self.assertEqual(agent_id, "Agent-7")
        
        agent_id = self.interpreter._check_explicit_command("!agent-7 test")
        self.assertEqual(agent_id, "Agent-7")

    def test_broadcast_command_detection(self):
        """Test that broadcast commands are detected."""
        self.assertTrue(self.interpreter._is_broadcast_command("!team status"))
        self.assertTrue(self.interpreter._is_broadcast_command("!swarm hello"))
        self.assertFalse(self.interpreter._is_broadcast_command("!agent7 hello"))


class TestAdminChecking(unittest.TestCase):
    """Test admin user checking logic."""

    def setUp(self):
        """Set up test fixtures."""
        twitch_config = {
            "channel": "digital_dreamscape",
            "admin_users": []
        }
        self.orchestrator = ChatPresenceOrchestrator(
            twitch_config=twitch_config,
            obs_config=None
        )

    def test_channel_owner_is_admin(self):
        """Test that channel owner is automatically admin."""
        is_admin = self.orchestrator._is_admin_user("digital_dreamscape", {})
        self.assertTrue(is_admin)

    def test_configured_admin_is_admin(self):
        """Test that configured admin users are admins."""
        self.orchestrator.admin_users.add("testadmin")
        is_admin = self.orchestrator._is_admin_user("testadmin", {})
        self.assertTrue(is_admin)

    def test_broadcaster_badge_is_admin(self):
        """Test that users with broadcaster badge are admins."""
        tags = {"badges": "broadcaster/1"}
        is_admin = self.orchestrator._is_admin_user("someuser", tags)
        self.assertTrue(is_admin)

    def test_moderator_badge_is_admin(self):
        """Test that users with moderator badge are admins."""
        tags = {"badges": "moderator/1"}
        is_admin = self.orchestrator._is_admin_user("someuser", tags)
        self.assertTrue(is_admin)

    def test_regular_user_is_not_admin(self):
        """Test that regular users are not admins."""
        is_admin = self.orchestrator._is_admin_user("regularuser", {})
        self.assertFalse(is_admin)


class TestStatusCommandHandling(unittest.TestCase):
    """Test status command handling."""

    def setUp(self):
        """Set up test fixtures."""
        twitch_config = {
            "channel": "digital_dreamscape"
        }
        self.orchestrator = ChatPresenceOrchestrator(
            twitch_config=twitch_config,
            obs_config=None
        )
        # Mock twitch bridge
        self.orchestrator.twitch_bridge = AsyncMock()

    @patch('src.services.chat_presence.chat_presence_orchestrator.AgentStatusReader')
    async def test_status_command_all_agents(self, mock_status_reader):
        """Test handling !status command for all agents."""
        # Mock status reader
        mock_reader = MagicMock()
        mock_reader.format_all_agents_summary.return_value = "📊 Swarm Status Summary"
        self.orchestrator.status_reader = mock_reader
        
        # Test
        await self.orchestrator._handle_status_command("!status")
        
        # Verify message was sent
        self.orchestrator.twitch_bridge.send_message.assert_called_once()

    @patch('src.services.chat_presence.chat_presence_orchestrator.AgentStatusReader')
    async def test_status_command_specific_agent(self, mock_status_reader):
        """Test handling !status agent7 command."""
        # Mock status reader
        mock_reader = MagicMock()
        mock_reader.format_agent_status_compact.return_value = "🟢 Agent-7: ACTIVE"
        self.orchestrator.status_reader = mock_reader
        
        # Test
        await self.orchestrator._handle_status_command("!status agent7")
        
        # Verify message was sent
        self.orchestrator.twitch_bridge.send_message.assert_called_once()


if __name__ == "__main__":
    unittest.main()

