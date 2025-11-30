"""Tests for Swarm Tasks Controller View."""
import pytest
from unittest.mock import Mock, patch, AsyncMock


class TestSwarmTasksControllerView:
    """Test SwarmTasksControllerView."""

    @pytest.fixture
    def mock_service(self):
        return Mock()

    @pytest.fixture
    def view(self, mock_service):
        try:
            from src.discord_commander.controllers.swarm_tasks_controller_view import SwarmTasksControllerView
            return SwarmTasksControllerView(mock_service)
        except ImportError:
            pytest.skip("Discord not available")

    def test_initialization(self, view, mock_service):
        assert view.messaging_service == mock_service
        assert view.current_page == 0
        assert hasattr(view, 'prev_btn')
        assert hasattr(view, 'refresh_btn')

    @pytest.mark.asyncio
    async def test_on_previous(self, view):
        mock_interaction = AsyncMock()
        view.current_page = 1
        await view.on_previous(mock_interaction)
        assert view.current_page == 0

    @pytest.mark.asyncio
    async def test_on_next(self, view):
        mock_interaction = AsyncMock()
        view.current_page = 0
        await view.on_next(mock_interaction)
        assert view.current_page == 1

