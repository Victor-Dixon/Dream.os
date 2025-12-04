"""
Tests for discord_commander/messaging_commands.py - MessagingCommands class.

Target: ≥85% coverage, 15+ test methods.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from datetime import datetime
import sys

# Mock discord imports before importing messaging_commands
sys.modules['discord'] = MagicMock()
sys.modules['discord.ext'] = MagicMock()
sys.modules['discord.ext.commands'] = MagicMock()

from src.discord_commander.messaging_commands import MessagingCommands


class TestMessagingCommands:
    """Test MessagingCommands class."""

    @pytest.fixture
    def mock_bot(self):
        """Create mock Discord bot."""
        bot = MagicMock()
        bot.user = MagicMock()
        bot.user.display_name = "TestBot"
        return bot

    @pytest.fixture
    def mock_messaging_controller(self):
        """Create mock messaging controller."""
        controller = AsyncMock()
        controller.send_agent_message = AsyncMock(return_value=True)
        controller.create_agent_messaging_view = MagicMock(return_value=MagicMock())
        controller.create_swarm_status_view = MagicMock(return_value=MagicMock())
        return controller

    @pytest.fixture
    def mock_ctx(self):
        """Create mock Discord context."""
        ctx = AsyncMock()
        ctx.user = MagicMock()
        ctx.user.display_name = "TestUser"
        ctx.send = AsyncMock()
        return ctx

    @pytest.fixture
    def messaging_commands(self, mock_bot, mock_messaging_controller):
        """Create MessagingCommands instance."""
        return MessagingCommands(mock_bot, mock_messaging_controller)

    def test_init(self, mock_bot, mock_messaging_controller):
        """Test MessagingCommands initialization."""
        commands = MessagingCommands(mock_bot, mock_messaging_controller)
        assert commands.bot == mock_bot
        assert commands.messaging_controller == mock_messaging_controller
        assert commands.logger is not None

    @pytest.mark.asyncio
    async def test_message_agent_success(self, messaging_commands, mock_ctx, mock_messaging_controller):
        """Test message_agent command with successful send."""
        mock_messaging_controller.send_agent_message = AsyncMock(return_value=True)
        
        await messaging_commands.message_agent(mock_ctx, "Agent-1", "Test message", "NORMAL")
        
        mock_messaging_controller.send_agent_message.assert_called_once_with(
            agent_id="Agent-1",
            message="Test message",
            priority="NORMAL"
        )
        mock_ctx.send.assert_called_once()
        embed = mock_ctx.send.call_args[0][0]
        assert embed.title == "✅ Message Sent"
        assert "Agent-1" in embed.description

    @pytest.mark.asyncio
    async def test_message_agent_failure(self, messaging_commands, mock_ctx, mock_messaging_controller):
        """Test message_agent command with failed send."""
        mock_messaging_controller.send_agent_message = AsyncMock(return_value=False)
        
        await messaging_commands.message_agent(mock_ctx, "Agent-1", "Test message", "HIGH")
        
        mock_ctx.send.assert_called_once()
        embed = mock_ctx.send.call_args[0][0]
        assert embed.title == "❌ Message Failed"

    @pytest.mark.asyncio
    async def test_message_agent_invalid_priority(self, messaging_commands, mock_ctx, mock_messaging_controller):
        """Test message_agent command with invalid priority (defaults to NORMAL)."""
        await messaging_commands.message_agent(mock_ctx, "Agent-1", "Test message", "INVALID")
        
        mock_messaging_controller.send_agent_message.assert_called_once_with(
            agent_id="Agent-1",
            message="Test message",
            priority="NORMAL"
        )

    @pytest.mark.asyncio
    async def test_message_agent_exception(self, messaging_commands, mock_ctx, mock_messaging_controller):
        """Test message_agent command with exception handling."""
        mock_messaging_controller.send_agent_message = AsyncMock(side_effect=Exception("Test error"))
        
        await messaging_commands.message_agent(mock_ctx, "Agent-1", "Test message")
        
        mock_ctx.send.assert_called_once()
        embed = mock_ctx.send.call_args[0][0]
        assert embed.title == "❌ Error"

    @pytest.mark.asyncio
    async def test_message_agent_priority_critical(self, messaging_commands, mock_ctx, mock_messaging_controller):
        """Test message_agent command with CRITICAL priority."""
        await messaging_commands.message_agent(mock_ctx, "Agent-1", "Test message", "CRITICAL")
        
        mock_messaging_controller.send_agent_message.assert_called_once_with(
            agent_id="Agent-1",
            message="Test message",
            priority="CRITICAL"
        )

    @pytest.mark.asyncio
    async def test_agent_interact_success(self, messaging_commands, mock_ctx, mock_messaging_controller):
        """Test agent_interact command success."""
        mock_view = MagicMock()
        mock_messaging_controller.create_agent_messaging_view = MagicMock(return_value=mock_view)
        
        await messaging_commands.agent_interact(mock_ctx)
        
        mock_messaging_controller.create_agent_messaging_view.assert_called_once()
        mock_ctx.send.assert_called_once()
        call_args = mock_ctx.send.call_args
        assert call_args[1]['view'] == mock_view

    @pytest.mark.asyncio
    async def test_agent_interact_exception(self, messaging_commands, mock_ctx, mock_messaging_controller):
        """Test agent_interact command with exception handling."""
        mock_messaging_controller.create_agent_messaging_view = MagicMock(side_effect=Exception("Test error"))
        
        await messaging_commands.agent_interact(mock_ctx)
        
        mock_ctx.send.assert_called_once()
        assert "Error creating interface" in mock_ctx.send.call_args[0][0]

    @pytest.mark.asyncio
    async def test_swarm_status_success(self, messaging_commands, mock_ctx, mock_messaging_controller):
        """Test swarm_status command success."""
        mock_view = MagicMock()
        mock_embed = MagicMock()
        mock_view._create_status_embed = AsyncMock(return_value=mock_embed)
        mock_messaging_controller.create_swarm_status_view = MagicMock(return_value=mock_view)
        
        await messaging_commands.swarm_status(mock_ctx)
        
        mock_messaging_controller.create_swarm_status_view.assert_called_once()
        mock_ctx.send.assert_called_once()
        call_args = mock_ctx.send.call_args
        assert call_args[0][0] == mock_embed
        assert call_args[1]['view'] == mock_view

    @pytest.mark.asyncio
    async def test_swarm_status_exception(self, messaging_commands, mock_ctx, mock_messaging_controller):
        """Test swarm_status command with exception handling."""
        mock_messaging_controller.create_swarm_status_view = MagicMock(side_effect=Exception("Test error"))
        
        await messaging_commands.swarm_status(mock_ctx)
        
        mock_ctx.send.assert_called_once()
        embed = mock_ctx.send.call_args[0][0]
        assert embed.title == "❌ Error"

    @pytest.mark.asyncio
    async def test_message_agent_long_message(self, messaging_commands, mock_ctx, mock_messaging_controller):
        """Test message_agent command with long message (truncation)."""
        long_message = "A" * 1000
        await messaging_commands.message_agent(mock_ctx, "Agent-1", long_message)
        
        mock_ctx.send.assert_called_once()
        embed = mock_ctx.send.call_args[0][0]
        # Message should be truncated to 500 chars
        assert len(embed.fields[0].value) <= 500

    @pytest.mark.asyncio
    async def test_message_agent_all_priorities(self, messaging_commands, mock_ctx, mock_messaging_controller):
        """Test message_agent command with all valid priorities."""
        priorities = ["NORMAL", "HIGH", "CRITICAL"]
        
        for priority in priorities:
            await messaging_commands.message_agent(mock_ctx, "Agent-1", "Test", priority)
            mock_messaging_controller.send_agent_message.assert_called_with(
                agent_id="Agent-1",
                message="Test",
                priority=priority
            )

    def test_logger_initialized(self, messaging_commands):
        """Test that logger is properly initialized."""
        assert messaging_commands.logger is not None
        assert messaging_commands.logger.name == "src.discord_commander.messaging_commands"

    @pytest.mark.asyncio
    async def test_broadcast_success(self, messaging_commands, mock_ctx, mock_messaging_controller):
        """Test broadcast command with successful broadcast."""
        mock_messaging_controller.broadcast_to_swarm = AsyncMock(return_value=True)
        
        await messaging_commands.broadcast(mock_ctx, "Test broadcast", "NORMAL")
        
        mock_messaging_controller.broadcast_to_swarm.assert_called_once_with(
            message="Test broadcast",
            priority="NORMAL"
        )
        mock_ctx.send.assert_called_once()
        embed = mock_ctx.send.call_args[0][0]
        assert embed.title == "✅ Broadcast Sent"

    @pytest.mark.asyncio
    async def test_broadcast_failure(self, messaging_commands, mock_ctx, mock_messaging_controller):
        """Test broadcast command with failed broadcast."""
        mock_messaging_controller.broadcast_to_swarm = AsyncMock(return_value=False)
        
        await messaging_commands.broadcast(mock_ctx, "Test broadcast", "HIGH")
        
        mock_ctx.send.assert_called_once()
        embed = mock_ctx.send.call_args[0][0]
        assert embed.title == "❌ Broadcast Failed"

    @pytest.mark.asyncio
    async def test_broadcast_exception(self, messaging_commands, mock_ctx, mock_messaging_controller):
        """Test broadcast command with exception handling."""
        mock_messaging_controller.broadcast_to_swarm = AsyncMock(side_effect=Exception("Test error"))
        
        await messaging_commands.broadcast(mock_ctx, "Test broadcast")
        
        mock_ctx.send.assert_called_once()
        embed = mock_ctx.send.call_args[0][0]
        assert embed.title == "❌ Error"

    @pytest.mark.asyncio
    async def test_agent_list_success(self, messaging_commands, mock_ctx, mock_messaging_controller):
        """Test agent_list command with agents available."""
        mock_status = {
            "Agent-1": {"active": True, "coordinates": (100, 200), "name": "Agent-1"},
            "Agent-2": {"active": False, "coordinates": (300, 400), "name": "Agent-2"}
        }
        mock_messaging_controller.get_agent_status = MagicMock(return_value=mock_status)
        
        await messaging_commands.agent_list(mock_ctx)
        
        mock_messaging_controller.get_agent_status.assert_called_once()
        mock_ctx.send.assert_called_once()
        embed = mock_ctx.send.call_args[0][0]
        assert embed.title == "🤖 Available Agents"
        assert len(embed.fields) == 2

    @pytest.mark.asyncio
    async def test_agent_list_no_agents(self, messaging_commands, mock_ctx, mock_messaging_controller):
        """Test agent_list command with no agents available."""
        mock_messaging_controller.get_agent_status = MagicMock(return_value={})
        
        await messaging_commands.agent_list(mock_ctx)
        
        mock_ctx.send.assert_called_once()
        embed = mock_ctx.send.call_args[0][0]
        assert embed.title == "❌ No Agents Found"

    @pytest.mark.asyncio
    async def test_agent_list_exception(self, messaging_commands, mock_ctx, mock_messaging_controller):
        """Test agent_list command with exception handling."""
        mock_messaging_controller.get_agent_status = MagicMock(side_effect=Exception("Test error"))
        
        await messaging_commands.agent_list(mock_ctx)
        
        mock_ctx.send.assert_called_once()
        embed = mock_ctx.send.call_args[0][0]
        assert embed.title == "❌ Error"

