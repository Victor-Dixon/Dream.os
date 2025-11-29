#!/usr/bin/env python3
"""
Tests for Messaging Commands - Comprehensive Coverage
====================================================

Expanded test suite for messaging_commands.py targeting ≥85% coverage.

Author: Agent-7
Date: 2025-01-28
Target: ≥85% coverage, 10+ test methods
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime


class TestMessagingCommands:
    """Comprehensive test suite for messaging commands."""

    @pytest.fixture
    def mock_bot(self):
        """Mock bot instance."""
        bot = MagicMock()
        bot.walk_commands = MagicMock(return_value=[])
        return bot

    @pytest.fixture
    def mock_messaging_controller(self):
        """Mock messaging controller."""
        controller = MagicMock()
        controller.send_agent_message = AsyncMock(return_value=True)
        controller.broadcast_to_swarm = AsyncMock(return_value=True)
        controller.get_agent_status = MagicMock(return_value={
            "Agent-1": {"active": True, "coordinates": (100, 200), "name": "Agent-1"}
        })
        controller.create_agent_messaging_view = MagicMock(return_value=MagicMock())
        controller.create_swarm_status_view = MagicMock(return_value=MagicMock())
        return controller

    @pytest.fixture
    def mock_ctx(self):
        """Mock command context."""
        ctx = MagicMock()
        ctx.send = AsyncMock()
        ctx.author.display_name = "TestUser"
        ctx.user.display_name = "TestUser"
        return ctx

    def test_command_initialization(self, mock_bot, mock_messaging_controller):
        """Test command initialization."""
        try:
            from src.discord_commander.messaging_commands import MessagingCommands
            commands = MessagingCommands(mock_bot, mock_messaging_controller)
            assert commands is not None
            assert commands.bot == mock_bot
            assert commands.messaging_controller == mock_messaging_controller
        except ImportError:
            pytest.skip("Messaging commands not available")

    @pytest.mark.asyncio
    async def test_message_agent_command_success(self, mock_bot, mock_messaging_controller, mock_ctx):
        """Test message_agent command success."""
        try:
            from src.discord_commander.messaging_commands import MessagingCommands
            commands = MessagingCommands(mock_bot, mock_messaging_controller)
            
            await commands.message_agent(mock_ctx, "Agent-1", "Test message", "NORMAL")
            
            mock_ctx.send.assert_called_once()
            mock_messaging_controller.send_agent_message.assert_called_once()
        except ImportError:
            pytest.skip("Messaging commands not available")

    @pytest.mark.asyncio
    async def test_message_agent_command_failure(self, mock_bot, mock_messaging_controller, mock_ctx):
        """Test message_agent command failure."""
        try:
            from src.discord_commander.messaging_commands import MessagingCommands
            commands = MessagingCommands(mock_bot, mock_messaging_controller)
            mock_messaging_controller.send_agent_message.return_value = False
            
            await commands.message_agent(mock_ctx, "Agent-1", "Test message", "NORMAL")
            
            mock_ctx.send.assert_called_once()
        except ImportError:
            pytest.skip("Messaging commands not available")

    @pytest.mark.asyncio
    async def test_message_agent_command_invalid_priority(self, mock_bot, mock_messaging_controller, mock_ctx):
        """Test message_agent command with invalid priority."""
        try:
            from src.discord_commander.messaging_commands import MessagingCommands
            commands = MessagingCommands(mock_bot, mock_messaging_controller)
            
            await commands.message_agent(mock_ctx, "Agent-1", "Test message", "INVALID")
            
            # Should default to NORMAL
            mock_messaging_controller.send_agent_message.assert_called_with(
                agent_id="Agent-1", message="Test message", priority="NORMAL"
            )
        except ImportError:
            pytest.skip("Messaging commands not available")

    @pytest.mark.asyncio
    async def test_agent_interact_command(self, mock_bot, mock_messaging_controller, mock_ctx):
        """Test agent_interact command."""
        try:
            from src.discord_commander.messaging_commands import MessagingCommands
            commands = MessagingCommands(mock_bot, mock_messaging_controller)
            
            await commands.agent_interact(mock_ctx)
            
            mock_ctx.send.assert_called_once()
            mock_messaging_controller.create_agent_messaging_view.assert_called_once()
        except ImportError:
            pytest.skip("Messaging commands not available")

    @pytest.mark.asyncio
    async def test_swarm_status_command(self, mock_bot, mock_messaging_controller, mock_ctx):
        """Test swarm_status command."""
        try:
            from src.discord_commander.messaging_commands import MessagingCommands
            commands = MessagingCommands(mock_bot, mock_messaging_controller)
            
            mock_view = MagicMock()
            mock_view._create_status_embed = AsyncMock(return_value=MagicMock())
            mock_messaging_controller.create_swarm_status_view.return_value = mock_view
            
            await commands.swarm_status(mock_ctx)
            
            mock_ctx.send.assert_called_once()
        except ImportError:
            pytest.skip("Messaging commands not available")

    @pytest.mark.asyncio
    async def test_broadcast_command_success(self, mock_bot, mock_messaging_controller, mock_ctx):
        """Test broadcast command success."""
        try:
            from src.discord_commander.messaging_commands import MessagingCommands
            commands = MessagingCommands(mock_bot, mock_messaging_controller)
            
            await commands.broadcast(mock_ctx, "Test broadcast", "NORMAL")
            
            mock_ctx.send.assert_called_once()
            mock_messaging_controller.broadcast_to_swarm.assert_called_once()
        except ImportError:
            pytest.skip("Messaging commands not available")

    @pytest.mark.asyncio
    async def test_broadcast_command_failure(self, mock_bot, mock_messaging_controller, mock_ctx):
        """Test broadcast command failure."""
        try:
            from src.discord_commander.messaging_commands import MessagingCommands
            commands = MessagingCommands(mock_bot, mock_messaging_controller)
            mock_messaging_controller.broadcast_to_swarm.return_value = False
            
            await commands.broadcast(mock_ctx, "Test broadcast", "NORMAL")
            
            mock_ctx.send.assert_called_once()
        except ImportError:
            pytest.skip("Messaging commands not available")

    @pytest.mark.asyncio
    async def test_agent_list_command(self, mock_bot, mock_messaging_controller, mock_ctx):
        """Test agent_list command."""
        try:
            from src.discord_commander.messaging_commands import MessagingCommands
            commands = MessagingCommands(mock_bot, mock_messaging_controller)
            
            await commands.agent_list(mock_ctx)
            
            mock_ctx.send.assert_called_once()
            mock_messaging_controller.get_agent_status.assert_called_once()
        except ImportError:
            pytest.skip("Messaging commands not available")

    @pytest.mark.asyncio
    async def test_agent_list_command_no_agents(self, mock_bot, mock_messaging_controller, mock_ctx):
        """Test agent_list command with no agents."""
        try:
            from src.discord_commander.messaging_commands import MessagingCommands
            commands = MessagingCommands(mock_bot, mock_messaging_controller)
            mock_messaging_controller.get_agent_status.return_value = {}
            
            await commands.agent_list(mock_ctx)
            
            mock_ctx.send.assert_called_once()
        except ImportError:
            pytest.skip("Messaging commands not available")

    @pytest.mark.asyncio
    async def test_agent_command_success(self, mock_bot, mock_messaging_controller, mock_ctx):
        """Test agent command (C-057) success."""
        try:
            from src.discord_commander.messaging_commands import MessagingCommands
            commands = MessagingCommands(mock_bot, mock_messaging_controller)
            
            await commands.agent_command(mock_ctx, "Agent-1", message="Test message")
            
            mock_ctx.send.assert_called_once()
            mock_messaging_controller.send_agent_message.assert_called_once()
        except ImportError:
            pytest.skip("Messaging commands not available")

    @pytest.mark.asyncio
    async def test_agent_command_without_prefix(self, mock_bot, mock_messaging_controller, mock_ctx):
        """Test agent command without Agent- prefix."""
        try:
            from src.discord_commander.messaging_commands import MessagingCommands
            commands = MessagingCommands(mock_bot, mock_messaging_controller)
            
            await commands.agent_command(mock_ctx, "1", message="Test message")
            
            # Should add Agent- prefix
            mock_messaging_controller.send_agent_message.assert_called_with(
                agent_id="Agent-1", message="Test message", priority="NORMAL"
            )
        except ImportError:
            pytest.skip("Messaging commands not available")

    @pytest.mark.asyncio
    async def test_agent_command_failure(self, mock_bot, mock_messaging_controller, mock_ctx):
        """Test agent command failure."""
        try:
            from src.discord_commander.messaging_commands import MessagingCommands
            commands = MessagingCommands(mock_bot, mock_messaging_controller)
            mock_messaging_controller.send_agent_message.return_value = False
            
            await commands.agent_command(mock_ctx, "Agent-1", message="Test message")
            
            mock_ctx.send.assert_called_once()
        except ImportError:
            pytest.skip("Messaging commands not available")

    @pytest.mark.asyncio
    async def test_help_messaging_command(self, mock_bot, mock_messaging_controller, mock_ctx):
        """Test help_messaging command."""
        try:
            from src.discord_commander.messaging_commands import MessagingCommands
            commands = MessagingCommands(mock_bot, mock_messaging_controller)
            
            await commands.help_messaging(mock_ctx)
            
            mock_ctx.send.assert_called_once()
        except ImportError:
            pytest.skip("Messaging commands not available")

    @pytest.mark.asyncio
    async def test_message_agent_command_error_handling(self, mock_bot, mock_messaging_controller, mock_ctx):
        """Test message_agent command error handling."""
        try:
            from src.discord_commander.messaging_commands import MessagingCommands
            commands = MessagingCommands(mock_bot, mock_messaging_controller)
            mock_messaging_controller.send_agent_message.side_effect = Exception("Test error")
            
            await commands.message_agent(mock_ctx, "Agent-1", "Test message", "NORMAL")
            
            mock_ctx.send.assert_called_once()
        except ImportError:
            pytest.skip("Messaging commands not available")

    @pytest.mark.asyncio
    async def test_broadcast_command_error_handling(self, mock_bot, mock_messaging_controller, mock_ctx):
        """Test broadcast command error handling."""
        try:
            from src.discord_commander.messaging_commands import MessagingCommands
            commands = MessagingCommands(mock_bot, mock_messaging_controller)
            mock_messaging_controller.broadcast_to_swarm.side_effect = Exception("Test error")
            
            await commands.broadcast(mock_ctx, "Test broadcast", "NORMAL")
            
            mock_ctx.send.assert_called_once()
        except ImportError:
            pytest.skip("Messaging commands not available")


def test_setup_function(mock_bot, mock_messaging_controller):
    """Test setup function."""
    try:
        from src.discord_commander.messaging_commands import setup
        mock_bot.add_cog = MagicMock()
        
        setup(mock_bot, mock_messaging_controller)
        
        mock_bot.add_cog.assert_called_once()
    except ImportError:
        pytest.skip("Messaging commands not available")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src.discord_commander.messaging_commands", "--cov-report=term-missing"])
