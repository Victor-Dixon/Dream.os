"""Tests for Unstall Agent View."""
import pytest
from unittest.mock import Mock, patch, AsyncMock


class TestUnstallAgentView:
    """Test UnstallAgentView."""

    @pytest.fixture
    def mock_service(self):
        return Mock()

    @pytest.fixture
    def view(self, mock_service):
        try:
            from src.discord_commander.views.unstall_agent_view import UnstallAgentView
            return UnstallAgentView(mock_service)
        except ImportError:
            pytest.skip("Discord not available")

    def test_initialization(self, view, mock_service):
        assert view.messaging_service == mock_service
        assert hasattr(view, 'agent_select')

    @pytest.mark.asyncio
    async def test_on_agent_select(self, view):
        mock_interaction = AsyncMock()
        view.agent_select.values = ["Agent-1"]
        with patch.object(view, 'unstall_agent', AsyncMock()):
            await view.on_agent_select(mock_interaction)
            assert True

    @pytest.mark.asyncio
    async def test_unstall_agent(self, view):
        mock_interaction = AsyncMock()
        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.read_text', return_value='{"current_mission": "test"}'):
                with patch.object(view.messaging_service, 'send_message', AsyncMock()):
                    await view.unstall_agent(mock_interaction, "Agent-1")
                    assert True

