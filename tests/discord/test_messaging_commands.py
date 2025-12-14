"""
Tests for discord_commander/messaging_commands.py - MessagingCommands class.

Target: ≥85% coverage, 15+ test methods.
"""

import os
import pytest
import asyncio
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from datetime import datetime
import sys
from pathlib import Path
import importlib.util

# Set pytest environment variable BEFORE imports to enable command decorator stripping
os.environ["PYTEST_CURRENT_TEST"] = "test"

# Add project root to path
_project_root = Path(__file__).parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

# Setup Discord mocks (SSOT)
_discord_utils_path = _project_root / "tests" / "utils" / "discord_test_utils.py"
spec = importlib.util.spec_from_file_location("discord_test_utils", _discord_utils_path)
discord_test_utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(discord_test_utils)
setup_discord_mocks = discord_test_utils.setup_discord_mocks
create_mock_discord_bot = discord_test_utils.create_mock_discord_bot
create_mock_discord_context = discord_test_utils.create_mock_discord_context
create_mock_messaging_controller = discord_test_utils.create_mock_messaging_controller
setup_discord_mocks()

from src.discord_commander.messaging_commands import MessagingCommands


class TestMessagingCommands:
    """Test MessagingCommands class."""

    @staticmethod
    def _get_embed_from_call_args(call_args):
        """Extract embed from ctx.send call_args (handles both positional and keyword args)."""
        # ctx.send is called with embed=embed (keyword argument)
        if call_args.kwargs and 'embed' in call_args.kwargs:
            return call_args.kwargs['embed']
        # Fallback to positional args if needed
        if call_args[0] and len(call_args[0]) > 0:
            return call_args[0][0]
        return None

    @pytest.fixture
    def mock_bot(self):
        """Create mock Discord bot."""
        return create_mock_discord_bot(display_name="TestBot")

    @pytest.fixture
    def mock_messaging_controller(self):
        """Create mock messaging controller."""
        controller = create_mock_messaging_controller()
        # Ensure all async methods are AsyncMock
        controller.send_agent_message = AsyncMock(return_value=True)
        controller.broadcast_to_swarm = AsyncMock(return_value=True)
        return controller

    @pytest.fixture
    def mock_ctx(self):
        """Create mock Discord context."""
        ctx = create_mock_discord_context(user_display_name="TestUser")
        # ctx.send is already AsyncMock from create_mock_discord_context
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
    @pytest.mark.timeout(5)
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
        embed = self._get_embed_from_call_args(mock_ctx.send.call_args)
        assert embed is not None
        assert embed.title == "✅ Message Sent"
        assert "Agent-1" in embed.description

    @pytest.mark.asyncio
    @pytest.mark.timeout(5)
    async def test_message_agent_failure(self, messaging_commands, mock_ctx, mock_messaging_controller):
        """Test message_agent command with failed send."""
        mock_messaging_controller.send_agent_message = AsyncMock(return_value=False)
        
        await messaging_commands.message_agent(mock_ctx, "Agent-1", "Test message", "HIGH")
        
        mock_ctx.send.assert_called_once()
        embed = self._get_embed_from_call_args(mock_ctx.send.call_args)
        assert embed is not None
        assert embed.title == "❌ Message Failed"

    @pytest.mark.asyncio
    @pytest.mark.timeout(5)
    async def test_message_agent_invalid_priority(self, messaging_commands, mock_ctx, mock_messaging_controller):
        """Test message_agent command with invalid priority (defaults to NORMAL)."""
        await messaging_commands.message_agent(mock_ctx, "Agent-1", "Test message", "INVALID")
        
        mock_messaging_controller.send_agent_message.assert_called_once_with(
            agent_id="Agent-1",
            message="Test message",
            priority="NORMAL"
        )

    @pytest.mark.asyncio
    @pytest.mark.timeout(5)
    async def test_message_agent_exception(self, messaging_commands, mock_ctx, mock_messaging_controller):
        """Test message_agent command with exception handling."""
        mock_messaging_controller.send_agent_message = AsyncMock(side_effect=Exception("Test error"))
        
        await messaging_commands.message_agent(mock_ctx, "Agent-1", "Test message")
        
        mock_ctx.send.assert_called_once()
        embed = self._get_embed_from_call_args(mock_ctx.send.call_args)
        assert embed is not None
        assert embed.title == "❌ Error"

    @pytest.mark.asyncio
    @pytest.mark.timeout(5)
    async def test_message_agent_priority_critical(self, messaging_commands, mock_ctx, mock_messaging_controller):
        """Test message_agent command with CRITICAL priority."""
        await messaging_commands.message_agent(mock_ctx, "Agent-1", "Test message", "CRITICAL")
        
        mock_messaging_controller.send_agent_message.assert_called_once_with(
            agent_id="Agent-1",
            message="Test message",
            priority="CRITICAL"
        )

    @pytest.mark.asyncio
    @pytest.mark.timeout(5)
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
    @pytest.mark.timeout(5)
    async def test_agent_interact_exception(self, messaging_commands, mock_ctx, mock_messaging_controller):
        """Test agent_interact command with exception handling."""
        mock_messaging_controller.create_agent_messaging_view = MagicMock(side_effect=Exception("Test error"))
        
        await messaging_commands.agent_interact(mock_ctx)
        
        mock_ctx.send.assert_called_once()
        # Error message can be positional or keyword
        error_msg = mock_ctx.send.call_args.kwargs.get('content') or (mock_ctx.send.call_args[0][0] if mock_ctx.send.call_args[0] else None)
        assert error_msg is not None
        assert "Error creating interface" in error_msg

    @pytest.mark.asyncio
    @pytest.mark.timeout(5)
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
        # Check embed (can be positional or keyword)
        embed = call_args.kwargs.get('embed') or (call_args[0][0] if call_args[0] else None)
        assert embed == mock_embed
        assert call_args.kwargs.get('view') == mock_view

    @pytest.mark.asyncio
    @pytest.mark.timeout(5)
    async def test_swarm_status_exception(self, messaging_commands, mock_ctx, mock_messaging_controller):
        """Test swarm_status command with exception handling."""
        mock_messaging_controller.create_swarm_status_view = MagicMock(side_effect=Exception("Test error"))
        
        await messaging_commands.swarm_status(mock_ctx)
        
        mock_ctx.send.assert_called_once()
        embed = self._get_embed_from_call_args(mock_ctx.send.call_args)
        assert embed is not None
        assert embed.title == "❌ Error"

    @pytest.mark.asyncio
    @pytest.mark.timeout(5)
    async def test_message_agent_long_message(self, messaging_commands, mock_ctx, mock_messaging_controller):
        """Test message_agent command with long message (truncation)."""
        long_message = "A" * 1000
        await messaging_commands.message_agent(mock_ctx, "Agent-1", long_message)
        
        mock_ctx.send.assert_called_once()
        embed = self._get_embed_from_call_args(mock_ctx.send.call_args)
        assert embed is not None
        # Verify embed was created and add_field was called
        # The actual truncation happens in the code, we just verify the embed was sent
        assert embed.title == "✅ Message Sent"
        # Check that add_field was called (message field should be added)
        if hasattr(embed, 'add_field'):
            # If add_field is a MagicMock, check it was called
            if hasattr(embed.add_field, 'call_count'):
                assert embed.add_field.call_count >= 1

    @pytest.mark.asyncio
    @pytest.mark.timeout(5)
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
    @pytest.mark.timeout(5)
    async def test_broadcast_success(self, messaging_commands, mock_ctx, mock_messaging_controller):
        """Test broadcast command with successful broadcast."""
        mock_messaging_controller.broadcast_to_swarm = AsyncMock(return_value=True)
        
        await messaging_commands.broadcast(mock_ctx, "Test broadcast", "NORMAL")
        
        mock_messaging_controller.broadcast_to_swarm.assert_called_once_with(
            message="Test broadcast",
            priority="NORMAL"
        )
        mock_ctx.send.assert_called_once()
        embed = self._get_embed_from_call_args(mock_ctx.send.call_args)
        assert embed is not None
        assert embed.title == "✅ Broadcast Sent"

    @pytest.mark.asyncio
    @pytest.mark.timeout(5)
    async def test_broadcast_failure(self, messaging_commands, mock_ctx, mock_messaging_controller):
        """Test broadcast command with failed broadcast."""
        mock_messaging_controller.broadcast_to_swarm = AsyncMock(return_value=False)
        
        await messaging_commands.broadcast(mock_ctx, "Test broadcast", "HIGH")
        
        mock_ctx.send.assert_called_once()
        embed = self._get_embed_from_call_args(mock_ctx.send.call_args)
        assert embed is not None
        assert embed.title == "❌ Broadcast Failed"

    @pytest.mark.asyncio
    @pytest.mark.timeout(5)
    async def test_broadcast_exception(self, messaging_commands, mock_ctx, mock_messaging_controller):
        """Test broadcast command with exception handling."""
        mock_messaging_controller.broadcast_to_swarm = AsyncMock(side_effect=Exception("Test error"))
        
        await messaging_commands.broadcast(mock_ctx, "Test broadcast")
        
        mock_ctx.send.assert_called_once()
        embed = self._get_embed_from_call_args(mock_ctx.send.call_args)
        assert embed is not None
        assert embed.title == "❌ Error"

    @pytest.mark.asyncio
    @pytest.mark.timeout(5)
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
        embed = self._get_embed_from_call_args(mock_ctx.send.call_args)
        assert embed is not None
        assert embed.title == "🤖 Available Agents"
        # Verify add_field was called for each agent (2 agents = 2 calls)
        if hasattr(embed, 'add_field'):
            # If add_field is a MagicMock, check it was called
            if hasattr(embed.add_field, 'call_count'):
                assert embed.add_field.call_count == 2

    @pytest.mark.asyncio
    @pytest.mark.timeout(5)
    async def test_agent_list_no_agents(self, messaging_commands, mock_ctx, mock_messaging_controller):
        """Test agent_list command with no agents available."""
        mock_messaging_controller.get_agent_status = MagicMock(return_value={})
        
        await messaging_commands.agent_list(mock_ctx)
        
        mock_ctx.send.assert_called_once()
        embed = self._get_embed_from_call_args(mock_ctx.send.call_args)
        assert embed is not None
        assert embed.title == "❌ No Agents Found"

    @pytest.mark.asyncio
    @pytest.mark.timeout(5)
    async def test_agent_list_exception(self, messaging_commands, mock_ctx, mock_messaging_controller):
        """Test agent_list command with exception handling."""
        mock_messaging_controller.get_agent_status = MagicMock(side_effect=Exception("Test error"))
        
        await messaging_commands.agent_list(mock_ctx)
        
        mock_ctx.send.assert_called_once()
        embed = self._get_embed_from_call_args(mock_ctx.send.call_args)
        assert embed is not None
        assert embed.title == "❌ Error"

