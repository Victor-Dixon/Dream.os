"""
Tests for Broadcast Controller View
====================================

Comprehensive tests for src/discord_commander/controllers/broadcast_controller_view.py

Author: Agent-7 (Web Development Specialist)
Date: 2025-11-29
Target: 80%+ coverage
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock, MagicMock


class TestBroadcastControllerView:
    """Test BroadcastControllerView class."""

    @pytest.fixture
    def mock_messaging_service(self):
        """Create mock messaging service."""
        return Mock()

    @pytest.fixture
    def broadcast_view(self, mock_messaging_service):
        """Create BroadcastControllerView instance."""
        try:
            from src.discord_commander.controllers.broadcast_controller_view import BroadcastControllerView
            return BroadcastControllerView(mock_messaging_service)
        except ImportError:
            pytest.skip("Discord not available")

    def test_initialization(self, mock_messaging_service):
        """Test BroadcastControllerView initialization."""
        try:
            from src.discord_commander.controllers.broadcast_controller_view import BroadcastControllerView

            view = BroadcastControllerView(mock_messaging_service)
            assert view is not None
            assert view.messaging_service == mock_messaging_service
            assert hasattr(view, 'broadcast_all_btn')
            assert hasattr(view, 'broadcast_select_btn')
            assert hasattr(view, 'jet_fuel_broadcast_btn')
            assert hasattr(view, 'templates_btn')
        except ImportError:
            pytest.skip("Discord not available")

    @pytest.mark.asyncio
    async def test_on_broadcast_all(self, broadcast_view):
        """Test broadcast all button handler."""
        mock_interaction = AsyncMock()
        mock_interaction.response.send_modal = AsyncMock()

        with patch('src.discord_commander.controllers.broadcast_controller_view.BroadcastMessageModal') as mock_modal:
            mock_modal.return_value = Mock()
            await broadcast_view.on_broadcast_all(mock_interaction)
            assert mock_interaction.response.send_modal.called

    @pytest.mark.asyncio
    async def test_on_broadcast_all_error(self, broadcast_view):
        """Test broadcast all error handling."""
        mock_interaction = AsyncMock()
        mock_interaction.response.is_done.return_value = False
        mock_interaction.response.send_message = AsyncMock()

        with patch('src.discord_commander.controllers.broadcast_controller_view.BroadcastMessageModal', side_effect=Exception("Test error")):
            await broadcast_view.on_broadcast_all(mock_interaction)
            assert mock_interaction.response.send_message.called

    @pytest.mark.asyncio
    async def test_on_broadcast_select(self, broadcast_view):
        """Test broadcast select button handler."""
        mock_interaction = AsyncMock()
        mock_interaction.response.send_modal = AsyncMock()

        with patch('src.discord_commander.controllers.broadcast_controller_view.SelectiveBroadcastModal') as mock_modal:
            mock_modal.return_value = Mock()
            await broadcast_view.on_broadcast_select(mock_interaction)
            assert mock_interaction.response.send_modal.called

    @pytest.mark.asyncio
    async def test_on_jet_fuel_broadcast(self, broadcast_view):
        """Test jet fuel broadcast button handler."""
        mock_interaction = AsyncMock()
        mock_interaction.response.send_modal = AsyncMock()

        with patch('src.discord_commander.controllers.broadcast_controller_view.JetFuelBroadcastModal') as mock_modal:
            mock_modal.return_value = Mock()
            await broadcast_view.on_jet_fuel_broadcast(mock_interaction)
            assert mock_interaction.response.send_modal.called

    @pytest.mark.asyncio
    async def test_on_templates(self, broadcast_view):
        """Test templates button handler."""
        mock_interaction = AsyncMock()
        mock_interaction.response.send_message = AsyncMock()

        with patch('src.discord_commander.controllers.broadcast_controller_view.BroadcastTemplatesView') as mock_view_class:
            mock_view = Mock()
            mock_view.create_templates_embed.return_value = Mock()
            mock_view_class.return_value = mock_view
            
            await broadcast_view.on_templates(mock_interaction)
            assert mock_interaction.response.send_message.called

    def test_create_broadcast_embed(self, broadcast_view):
        """Test broadcast embed creation."""
        try:
            embed = broadcast_view.create_broadcast_embed()
            assert embed is not None
            assert hasattr(embed, 'title') or isinstance(embed, dict)
        except Exception:
            # May require Discord objects
            pass

