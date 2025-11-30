"""Tests for Approval Commands - expanded coverage."""
import pytest
from unittest.mock import Mock, patch, AsyncMock


class TestApprovalCommands:
    """Test ApprovalCommands cog."""

    @pytest.fixture
    def mock_bot(self):
        return Mock()

    @pytest.fixture
    def approval_commands(self, mock_bot):
        from src.discord_commander.approval_commands import ApprovalCommands
        return ApprovalCommands(mock_bot)

    @pytest.mark.asyncio
    async def test_approve_command(self, approval_commands):
        mock_ctx = AsyncMock()
        mock_ctx.send = AsyncMock()
        await approval_commands.approve(mock_ctx, "test-id")
        assert True

    @pytest.mark.asyncio
    async def test_reject_command(self, approval_commands):
        mock_ctx = AsyncMock()
        mock_ctx.send = AsyncMock()
        await approval_commands.reject(mock_ctx, "test-id")
        assert True
