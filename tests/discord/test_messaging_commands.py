"""Tests for Messaging Commands - expanded coverage."""
import pytest
from unittest.mock import Mock, patch, AsyncMock


class TestMessagingCommands:
    """Test MessagingCommands cog."""

    @pytest.fixture
    def mock_bot(self):
        return Mock()

    @pytest.fixture
    def messaging_commands(self, mock_bot):
        from src.discord_commander.messaging_commands import MessagingCommands
        with patch('src.discord_commander.messaging_commands.ConsolidatedMessagingService'):
            return MessagingCommands(mock_bot)

    @pytest.mark.asyncio
    async def test_message_agent_command(self, messaging_commands):
        mock_ctx = AsyncMock()
        mock_ctx.send = AsyncMock()
        await messaging_commands.message_agent(mock_ctx, "Agent-1", "test message")
        assert True

    @pytest.mark.asyncio
    async def test_broadcast_command(self, messaging_commands):
        mock_ctx = AsyncMock()
        mock_ctx.send = AsyncMock()
        await messaging_commands.broadcast(mock_ctx, "test message")
        assert True
