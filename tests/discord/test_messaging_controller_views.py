#!/usr/bin/env python3
"""
Tests for Messaging Controller Views
=====================================

Tests for Discord messaging controller views.

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-01-27
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch


class TestMessagingControllerViews:
    """Test suite for messaging controller views."""

    @pytest.fixture
    def mock_discord(self):
        """Mock Discord library."""
        mock_discord_module = MagicMock()
        mock_discord_module.ui = MagicMock()
        mock_discord_module.ui.View = MagicMock
        mock_discord_module.ui.Select = MagicMock
        mock_discord_module.ui.Button = MagicMock
        mock_discord_module.ui.SelectOption = MagicMock
        mock_discord_module.ButtonStyle = MagicMock()
        mock_discord_module.ButtonStyle.primary = "primary"
        mock_discord_module.ButtonStyle.secondary = "secondary"
        mock_discord_module.Interaction = MagicMock
        mock_discord_module.Embed = MagicMock()
        mock_discord_module.Color = MagicMock()
        mock_discord_module.Color.blue = MagicMock()
        
        with patch.dict('sys.modules', {
            'discord': mock_discord_module,
            'discord.ui': mock_discord_module.ui,
        }):
            yield mock_discord_module

    @pytest.fixture
    def mock_messaging_service(self):
        """Mock messaging service."""
        service = MagicMock()
        service.agent_data = {
            "Agent-1": {"name": "Agent-1", "active": True, "coordinates": (1, 1)},
            "Agent-2": {"name": "Agent-2", "active": False, "coordinates": (2, 2)}
        }
        return service

    def test_agent_messaging_view_initialization(self, mock_discord, mock_messaging_service):
        """Test AgentMessagingView initialization."""
        from src.discord_commander.messaging_controller_views import AgentMessagingView
        
        view = AgentMessagingView(mock_messaging_service)
        
        assert view is not None
        assert view.messaging_service == mock_messaging_service
        assert len(view.agents) > 0

    def test_agent_messaging_view_load_agents_from_service(self, mock_discord, mock_messaging_service):
        """Test loading agents from messaging service."""
        from src.discord_commander.messaging_controller_views import AgentMessagingView
        
        view = AgentMessagingView(mock_messaging_service)
        
        assert len(view.agents) == 2
        assert any(a["id"] == "Agent-1" for a in view.agents)
        assert any(a["id"] == "Agent-2" for a in view.agents)

    def test_agent_messaging_view_fallback_to_status_reader(self, mock_discord):
        """Test fallback to StatusReader when service has no agent_data."""
        mock_service = MagicMock()
        mock_service.agent_data = None
        
        mock_status_reader = MagicMock()
        mock_status_reader.read_all_statuses = MagicMock(return_value={
            "Agent-1": {
                "agent_name": "Test Agent",
                "status": "ACTIVE",
                "coordinate_position": "(1, 1)"
            }
        })
        
        with patch('src.discord_commander.messaging_controller_views.StatusReader', return_value=mock_status_reader):
            from src.discord_commander.messaging_controller_views import AgentMessagingView
            
            view = AgentMessagingView(mock_service)
            
            assert len(view.agents) > 0

    def test_agent_messaging_view_emergency_fallback(self, mock_discord):
        """Test emergency fallback to static list."""
        mock_service = MagicMock()
        mock_service.agent_data = None
        
        with patch('src.discord_commander.messaging_controller_views.StatusReader', side_effect=Exception("Error")):
            from src.discord_commander.messaging_controller_views import AgentMessagingView
            
            view = AgentMessagingView(mock_service)
            
            # Should have emergency fallback (8 agents)
            assert len(view.agents) == 8

    def test_create_agent_options(self, mock_discord, mock_messaging_service):
        """Test creating agent select options."""
        from src.discord_commander.messaging_controller_views import AgentMessagingView
        
        view = AgentMessagingView(mock_messaging_service)
        options = view._create_agent_options()
        
        assert len(options) > 0
        for option in options:
            assert hasattr(option, 'label') or 'label' in str(type(option))
            assert hasattr(option, 'value') or 'value' in str(type(option))

    @pytest.mark.asyncio
    async def test_on_agent_select(self, mock_discord, mock_messaging_service):
        """Test agent selection handler."""
        from src.discord_commander.messaging_controller_views import AgentMessagingView
        
        mock_modal = MagicMock()
        mock_modal_class = MagicMock(return_value=mock_modal)
        
        with patch('src.discord_commander.messaging_controller_views.MessageModal', mock_modal_class):
            view = AgentMessagingView(mock_messaging_service)
            
            interaction = AsyncMock()
            interaction.data = {"values": ["Agent-1"]}
            interaction.response = AsyncMock()
            interaction.response.send_modal = AsyncMock()
            
            await view.on_agent_select(interaction)
            
            interaction.response.send_modal.assert_called_once()

    @pytest.mark.asyncio
    async def test_on_agent_select_error(self, mock_discord, mock_messaging_service):
        """Test agent selection error handling."""
        from src.discord_commander.messaging_controller_views import AgentMessagingView
        
        view = AgentMessagingView(mock_messaging_service)
        
        interaction = AsyncMock()
        interaction.data = {"values": []}  # Empty selection
        interaction.response = AsyncMock()
        interaction.response.send_modal = AsyncMock(side_effect=Exception("Error"))
        interaction.response.is_done = MagicMock(return_value=False)
        interaction.response.send_message = AsyncMock()
        
        await view.on_agent_select(interaction)
        
        # Should send error message
        assert interaction.response.send_message.called

    def test_swarm_status_view_initialization(self, mock_discord, mock_messaging_service):
        """Test SwarmStatusView initialization."""
        from src.discord_commander.messaging_controller_views import SwarmStatusView
        
        view = SwarmStatusView(mock_messaging_service)
        
        assert view is not None
        assert view.messaging_service == mock_messaging_service

    @pytest.mark.asyncio
    async def test_refresh_status(self, mock_discord, mock_messaging_service):
        """Test status refresh."""
        from src.discord_commander.messaging_controller_views import SwarmStatusView
        
        mock_status_reader = MagicMock()
        mock_status_reader.clear_cache = MagicMock()
        mock_status_reader.read_all_statuses = MagicMock(return_value={
            "Agent-1": {
                "agent_name": "Test",
                "status": "ACTIVE",
                "current_mission": "Test mission",
                "current_tasks": ["Task 1"],
                "last_updated": "2025-01-27",
                "current_phase": "EXECUTION"
            }
        })
        
        with patch('src.discord_commander.messaging_controller_views.StatusReader', return_value=mock_status_reader):
            view = SwarmStatusView(mock_messaging_service)
            
            interaction = AsyncMock()
            interaction.response = AsyncMock()
            interaction.response.is_done = MagicMock(return_value=False)
            interaction.response.edit_message = AsyncMock()
            
            await view.refresh_status(interaction)
            
            mock_status_reader.clear_cache.assert_called_once()
            interaction.response.edit_message.assert_called_once()

    @pytest.mark.asyncio
    async def test_broadcast_message(self, mock_discord, mock_messaging_service):
        """Test broadcast message button."""
        from src.discord_commander.messaging_controller_views import SwarmStatusView
        
        mock_modal = MagicMock()
        mock_modal_class = MagicMock(return_value=mock_modal)
        
        with patch('src.discord_commander.messaging_controller_views.BroadcastModal', mock_modal_class):
            view = SwarmStatusView(mock_messaging_service)
            
            interaction = AsyncMock()
            interaction.response = AsyncMock()
            interaction.response.send_modal = AsyncMock()
            
            await view.broadcast_message(interaction)
            
            interaction.response.send_modal.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_status_embed(self, mock_discord, mock_messaging_service):
        """Test creating status embed."""
        from src.discord_commander.messaging_controller_views import SwarmStatusView
        
        mock_status_reader = MagicMock()
        mock_status_reader.read_all_statuses = MagicMock(return_value={
            "Agent-1": {
                "agent_name": "Test Agent",
                "status": "ACTIVE_AGENT_MODE",
                "current_mission": "Test mission",
                "current_tasks": ["Task 1"],
                "last_updated": "2025-01-27",
                "current_phase": "EXECUTION"
            }
        })
        
        with patch('src.discord_commander.messaging_controller_views.StatusReader', return_value=mock_status_reader):
            view = SwarmStatusView(mock_messaging_service)
            
            embed = await view._create_status_embed()
            
            assert embed is not None

    @pytest.mark.asyncio
    async def test_create_status_embed_no_data(self, mock_discord, mock_messaging_service):
        """Test creating status embed when no data available."""
        from src.discord_commander.messaging_controller_views import SwarmStatusView
        
        mock_status_reader = MagicMock()
        mock_status_reader.read_all_statuses = MagicMock(return_value={})
        
        with patch('src.discord_commander.messaging_controller_views.StatusReader', return_value=mock_status_reader):
            view = SwarmStatusView(mock_messaging_service)
            
            embed = await view._create_status_embed()
            
            assert embed is not None

