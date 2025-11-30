"""
Unit tests for command_handler.py

Target: ≥85% coverage, 15+ test methods
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, AsyncMock
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.services.handlers.command_handler import CommandHandler


class TestCommandHandler:
    """Test suite for CommandHandler."""

    @pytest.fixture
    def handler(self):
        """Create CommandHandler instance."""
        return CommandHandler()

    def test_handler_initialization(self, handler):
        """Test handler initializes correctly."""
        assert handler is not None
        assert handler.command_count == 0
        assert handler.successful_commands == 0
        assert handler.failed_commands == 0
        assert handler.command_history == []

    def test_can_handle_returns_false(self, handler):
        """Test base handler doesn't handle anything."""
        assert handler.can_handle(Mock()) is False

    @pytest.mark.asyncio
    async def test_process_command_unknown(self, handler):
        """Test processing unknown command."""
        result = await handler.process_command("unknown", {}, None, None, None)
        assert result["success"] is False
        assert "Unknown command" in result["error"]

    @pytest.mark.asyncio
    async def test_process_command_increments_count(self, handler):
        """Test command count increments."""
        initial_count = handler.command_count
        await handler.process_command("unknown", {}, None, None, None)
        assert handler.command_count == initial_count + 1

    @pytest.mark.asyncio
    async def test_process_command_tracks_success(self, handler):
        """Test successful command tracking."""
        mock_coord = AsyncMock()
        mock_coord.load_coordinates_async.return_value = {"success": True, "coordinates": {}}
        
        await handler.process_command("coordinates", {}, mock_coord, None, None)
        
        assert handler.successful_commands == 1
        assert handler.failed_commands == 0

    @pytest.mark.asyncio
    async def test_process_command_tracks_failure(self, handler):
        """Test failed command tracking."""
        await handler.process_command("unknown", {}, None, None, None)
        
        assert handler.successful_commands == 0
        assert handler.failed_commands == 1

    @pytest.mark.asyncio
    async def test_process_command_adds_to_history(self, handler):
        """Test command history tracking."""
        await handler.process_command("unknown", {"arg": "value"}, None, None, None)
        
        assert len(handler.command_history) == 1
        assert handler.command_history[0]["command"] == "unknown"
        assert handler.command_history[0]["args"] == {"arg": "value"}

    @pytest.mark.asyncio
    async def test_process_command_exception_handling(self, handler):
        """Test exception handling during command processing."""
        handler._handle_coordinates_command = AsyncMock(side_effect=Exception("Test error"))
        
        result = await handler.process_command("coordinates", {}, handler, None, None)
        
        assert result["success"] is False
        assert handler.failed_commands == 1

    @pytest.mark.asyncio
    async def test_history_limits_to_100(self, handler):
        """Test command history limits to 100 entries."""
        for i in range(105):
            await handler.process_command("unknown", {"i": i}, None, None, None)
        
        assert len(handler.command_history) == 100

    def test_history_entry_structure(self, handler):
        """Test command history entry structure."""
        import asyncio
        asyncio.run(handler.process_command("test", {"arg": "val"}, None, None, None))
        
        entry = handler.command_history[0]
        assert "command" in entry
        assert "args" in entry
        assert "success" in entry
        assert "execution_time" in entry
        assert "timestamp" in entry

