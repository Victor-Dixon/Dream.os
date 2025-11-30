"""Tests for Main Control Panel View."""
import pytest
from unittest.mock import Mock, patch, AsyncMock


class TestMainControlPanelView:
    """Test MainControlPanelView."""

    @pytest.fixture
    def mock_service(self):
        return Mock()

    @pytest.fixture
    def view(self, mock_service):
        try:
            from src.discord_commander.views.main_control_panel_view import MainControlPanelView
            return MainControlPanelView(mock_service)
        except ImportError:
            pytest.skip("Discord not available")

    def test_initialization(self, view, mock_service):
        assert view.messaging_service == mock_service
        assert hasattr(view, 'msg_agent_btn')
        assert hasattr(view, 'broadcast_btn')
        assert hasattr(view, 'status_btn')

    @pytest.mark.asyncio
    async def test_show_agent_selector(self, view):
        mock_interaction = AsyncMock()
        mock_interaction.response.send_message = AsyncMock()
        with patch('src.discord_commander.views.main_control_panel_view.AgentMessagingView'):
            await view.show_agent_selector(mock_interaction)
            assert True

    @pytest.mark.asyncio
    async def test_show_broadcast_modal(self, view):
        mock_interaction = AsyncMock()
        mock_interaction.response.send_modal = AsyncMock()
        with patch('src.discord_commander.views.main_control_panel_view.BroadcastControllerView'):
            await view.show_broadcast_modal(mock_interaction)
            assert True

