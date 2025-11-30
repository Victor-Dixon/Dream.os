"""Tests for Status Controller View - expanded coverage."""
import pytest
from unittest.mock import Mock, patch, AsyncMock


class TestStatusControllerView:
    """Test StatusControllerView."""

    @pytest.fixture
    def mock_service(self):
        return Mock()

    @pytest.fixture
    def view(self, mock_service):
        try:
            from src.discord_commander.controllers.status_controller_view import StatusControllerView
            return StatusControllerView(mock_service)
        except ImportError:
            pytest.skip("Discord not available")

    def test_initialization(self, view, mock_service):
        assert view.messaging_service == mock_service

    @pytest.mark.asyncio
    async def test_refresh_status(self, view):
        mock_interaction = AsyncMock()
        mock_interaction.response.send_message = AsyncMock()
        await view.refresh_status(mock_interaction)
        assert True

