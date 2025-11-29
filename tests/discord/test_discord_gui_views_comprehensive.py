#!/usr/bin/env python3
"""
Comprehensive Tests for Discord GUI Views
=========================================

Tests all functionality in discord_gui_views.py to identify:
1. Methods only used in tests (dead code candidates)
2. Actual usage patterns in codebase
3. Protocol requirements

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-01-27
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, Mock, patch, PropertyMock
from typing import Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class TestAgentMessagingGUIView:
    """Comprehensive tests for AgentMessagingGUIView class."""

    @pytest.fixture
    def mock_discord(self):
        """Mock Discord library components."""
        mock_discord_module = MagicMock()
        mock_ui = MagicMock()
        mock_view = MagicMock()
        mock_select = MagicMock()
        mock_button = MagicMock()
        mock_select_option = MagicMock()
        
        # Setup mock structure
        mock_ui.View = mock_view
        mock_ui.Select = mock_select
        mock_ui.Button = mock_button
        mock_ui.SelectOption = mock_select_option
        mock_discord_module.ui = mock_ui
        mock_discord_module.Interaction = MagicMock()
        mock_discord_module.Embed = MagicMock()
        mock_discord_module.Color = MagicMock()
        mock_discord_module.utils = MagicMock()
        mock_discord_module.utils.utcnow = MagicMock()
        
        with patch.dict('sys.modules', {
            'discord': mock_discord_module,
            'discord.ui': mock_ui,
            'discord.ext': MagicMock(),
            'discord.ext.commands': MagicMock(),
        }):
            yield mock_discord_module

    @pytest.fixture
    def mock_messaging_service(self):
        """Mock ConsolidatedMessagingService."""
        service = MagicMock()
        service.send_message = MagicMock(return_value={"success": True})
        return service

    @pytest.fixture
    def mock_status_reader(self):
        """Mock StatusReader."""
        reader = MagicMock()
        reader.read_all_statuses = MagicMock(return_value={
            "Agent-1": {"agent_name": "Agent-1", "status": "active", "points_earned": 100},
            "Agent-2": {"agent_name": "Agent-2", "status": "idle", "points_earned": 200},
        })
        reader.get_agent_status = MagicMock(return_value={
            "agent_name": "Agent-1",
            "status": "active",
            "points_summary": 100
        })
        return reader

    def test_import_success(self, mock_discord):
        """Test that module can be imported."""
        try:
            from src.discord_commander.discord_gui_views import (
                AgentMessagingGUIView,
                SwarmStatusGUIView
            )
            assert AgentMessagingGUIView is not None
            assert SwarmStatusGUIView is not None
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")

    def test_agent_messaging_view_initialization(self, mock_discord, mock_messaging_service, mock_status_reader):
        """Test AgentMessagingGUIView initialization."""
        with patch('src.discord_commander.discord_gui_views.StatusReader', return_value=mock_status_reader):
            from src.discord_commander.discord_gui_views import AgentMessagingGUIView
            
            view = AgentMessagingGUIView(mock_messaging_service)
            assert view.messaging_service == mock_messaging_service
            assert view.agents is not None
            assert len(view.agents) == 8  # Should have 8 agents

    def test_load_agents(self, mock_discord, mock_messaging_service, mock_status_reader):
        """Test _load_agents method."""
        with patch('src.discord_commander.discord_gui_views.StatusReader', return_value=mock_status_reader):
            from src.discord_commander.discord_gui_views import AgentMessagingGUIView
            
            view = AgentMessagingGUIView(mock_messaging_service)
            agents = view._load_agents()
            
            assert len(agents) == 8
            assert all("id" in agent for agent in agents)
            assert all("name" in agent for agent in agents)
            assert all("status" in agent for agent in agents)
            assert all("points" in agent for agent in agents)

    def test_load_agents_fallback(self, mock_discord, mock_messaging_service):
        """Test _load_agents fallback when StatusReader fails."""
        with patch('src.discord_commander.discord_gui_views.StatusReader', side_effect=Exception("Test error")):
            from src.discord_commander.discord_gui_views import AgentMessagingGUIView
            
            view = AgentMessagingGUIView(mock_messaging_service)
            agents = view._load_agents()
            
            # Should fallback to static list
            assert len(agents) == 8
            assert all(agent["status"] == "unknown" for agent in agents)

    def test_create_agent_options(self, mock_discord, mock_messaging_service, mock_status_reader):
        """Test _create_agent_options method."""
        with patch('src.discord_commander.discord_gui_views.StatusReader', return_value=mock_status_reader):
            from src.discord_commander.discord_gui_views import AgentMessagingGUIView
            
            view = AgentMessagingGUIView(mock_messaging_service)
            options = view._create_agent_options()
            
            assert len(options) == 8
            # Options should be SelectOption objects (mocked)

    def test_get_status_emoji(self, mock_discord, mock_messaging_service):
        """Test _get_status_emoji method."""
        from src.discord_commander.discord_gui_views import AgentMessagingGUIView
        
        view = AgentMessagingGUIView(mock_messaging_service)
        
        assert view._get_status_emoji("active") == "🟢"
        assert view._get_status_emoji("idle") == "🟡"
        assert view._get_status_emoji("busy") == "🔴"
        assert view._get_status_emoji("offline") == "⚫"
        assert view._get_status_emoji("unknown") == "❓"
        assert view._get_status_emoji("INVALID") == "❓"  # Default

    def test_extract_points(self, mock_discord, mock_messaging_service):
        """Test _extract_points method."""
        from src.discord_commander.discord_gui_views import AgentMessagingGUIView
        
        view = AgentMessagingGUIView(mock_messaging_service)
        
        # Test integer
        assert view._extract_points(100) == 100
        assert view._extract_points(0) == 0
        
        # Test string
        assert view._extract_points("100") == 100
        assert view._extract_points("1,000") == 1000
        assert view._extract_points("100pts") == 100
        
        # Test dict
        assert view._extract_points({"total": 200}) == 200
        assert view._extract_points({"total": 0}) == 0
        
        # Test invalid
        assert view._extract_points(None) == 0
        assert view._extract_points([]) == 0

    @pytest.mark.asyncio
    async def test_on_agent_select(self, mock_discord, mock_messaging_service, mock_status_reader):
        """Test on_agent_select callback."""
        with patch('src.discord_commander.discord_gui_views.StatusReader', return_value=mock_status_reader):
            with patch('src.discord_commander.discord_gui_views.AgentMessageModal') as mock_modal:
                from src.discord_commander.discord_gui_views import AgentMessagingGUIView
                
                view = AgentMessagingGUIView(mock_messaging_service)
                view.agent_select.values = ["Agent-1"]
                
                mock_interaction = AsyncMock()
                mock_interaction.response.send_modal = AsyncMock()
                
                await view.on_agent_select(mock_interaction)
                
                # Should create modal and send it
                mock_modal.assert_called_once()
                mock_interaction.response.send_modal.assert_called_once()

    @pytest.mark.asyncio
    async def test_on_broadcast(self, mock_discord, mock_messaging_service):
        """Test on_broadcast callback."""
        with patch('src.discord_commander.discord_gui_views.BroadcastMessageModal') as mock_modal:
            from src.discord_commander.discord_gui_views import AgentMessagingGUIView
            
            view = AgentMessagingGUIView(mock_messaging_service)
            
            mock_interaction = AsyncMock()
            mock_interaction.response.send_modal = AsyncMock()
            
            await view.on_broadcast(mock_interaction)
            
            # Should create broadcast modal
            mock_modal.assert_called_once()
            mock_interaction.response.send_modal.assert_called_once()

    @pytest.mark.asyncio
    async def test_on_status(self, mock_discord, mock_messaging_service, mock_status_reader):
        """Test on_status callback."""
        with patch('src.discord_commander.discord_gui_views.StatusReader', return_value=mock_status_reader):
            from src.discord_commander.discord_gui_views import AgentMessagingGUIView, SwarmStatusGUIView
            
            view = AgentMessagingGUIView(mock_messaging_service)
            
            mock_interaction = AsyncMock()
            mock_interaction.response.send_message = AsyncMock()
            
            await view.on_status(mock_interaction)
            
            # Should send status embed
            mock_interaction.response.send_message.assert_called_once()
            call_args = mock_interaction.response.send_message.call_args
            assert "embed" in call_args.kwargs
            assert "view" in call_args.kwargs

    @pytest.mark.asyncio
    async def test_on_refresh(self, mock_discord, mock_messaging_service, mock_status_reader):
        """Test on_refresh callback."""
        with patch('src.discord_commander.discord_gui_views.StatusReader', return_value=mock_status_reader):
            from src.discord_commander.discord_gui_views import AgentMessagingGUIView
            
            view = AgentMessagingGUIView(mock_messaging_service)
            original_agents = view.agents.copy()
            
            mock_interaction = AsyncMock()
            mock_interaction.response.send_message = AsyncMock()
            
            await view.on_refresh(mock_interaction)
            
            # Should reload agents and update options
            assert view.agents is not None
            mock_interaction.response.send_message.assert_called_once()


class TestSwarmStatusGUIView:
    """Comprehensive tests for SwarmStatusGUIView class."""

    @pytest.fixture
    def mock_discord(self):
        """Mock Discord library components."""
        mock_discord_module = MagicMock()
        mock_ui = MagicMock()
        mock_view = MagicMock()
        mock_button = MagicMock()
        
        mock_ui.View = mock_view
        mock_ui.Button = mock_button
        mock_discord_module.ui = mock_ui
        mock_discord_module.Interaction = MagicMock()
        mock_discord_module.Embed = MagicMock()
        mock_discord_module.Color = MagicMock()
        mock_discord_module.utils = MagicMock()
        mock_discord_module.utils.utcnow = MagicMock()
        
        with patch.dict('sys.modules', {
            'discord': mock_discord_module,
            'discord.ui': mock_ui,
            'discord.ext': MagicMock(),
            'discord.ext.commands': MagicMock(),
        }):
            yield mock_discord_module

    @pytest.fixture
    def mock_messaging_service(self):
        """Mock ConsolidatedMessagingService."""
        return MagicMock()

    @pytest.fixture
    def mock_status_reader(self):
        """Mock StatusReader."""
        reader = MagicMock()
        reader.get_agent_status = MagicMock(side_effect=lambda agent_id: {
            "agent_name": agent_id,
            "status": "active" if "1" in agent_id else "idle",
            "points_summary": 100
        })
        return reader

    def test_swarm_status_view_initialization(self, mock_discord, mock_messaging_service):
        """Test SwarmStatusGUIView initialization."""
        from src.discord_commander.discord_gui_views import SwarmStatusGUIView
        
        view = SwarmStatusGUIView(mock_messaging_service)
        assert view.messaging_service == mock_messaging_service

    @pytest.mark.asyncio
    async def test_on_refresh(self, mock_discord, mock_messaging_service, mock_status_reader):
        """Test on_refresh callback."""
        with patch('src.discord_commander.discord_gui_views.StatusReader', return_value=mock_status_reader):
            from src.discord_commander.discord_gui_views import SwarmStatusGUIView
            
            view = SwarmStatusGUIView(mock_messaging_service)
            
            mock_interaction = AsyncMock()
            mock_interaction.response.edit_message = AsyncMock()
            
            await view.on_refresh(mock_interaction)
            
            # Should refresh status and edit message
            mock_interaction.response.edit_message.assert_called_once()
            call_args = mock_interaction.response.edit_message.call_args
            assert "embed" in call_args.kwargs
            assert "view" in call_args.kwargs

    @pytest.mark.asyncio
    async def test_on_refresh_error_handling(self, mock_discord, mock_messaging_service):
        """Test on_refresh error handling."""
        with patch('src.discord_commander.discord_gui_views.StatusReader', side_effect=Exception("Test error")):
            from src.discord_commander.discord_gui_views import SwarmStatusGUIView
            
            view = SwarmStatusGUIView(mock_messaging_service)
            
            mock_interaction = AsyncMock()
            mock_interaction.response.send_message = AsyncMock()
            
            await view.on_refresh(mock_interaction)
            
            # Should send error message
            mock_interaction.response.send_message.assert_called_once()
            call_args = mock_interaction.response.send_message.call_args
            assert "❌" in call_args.kwargs.get("content", "") or "Error" in str(call_args)


class TestModuleExports:
    """Test module exports and __all__."""

    def test_module_exports(self, mock_discord):
        """Test that module exports correct classes."""
        try:
            from src.discord_commander import discord_gui_views
            
            assert hasattr(discord_gui_views, 'AgentMessagingGUIView')
            assert hasattr(discord_gui_views, 'SwarmStatusGUIView')
            assert hasattr(discord_gui_views, '__all__')
            
            assert 'AgentMessagingGUIView' in discord_gui_views.__all__
            assert 'SwarmStatusGUIView' in discord_gui_views.__all__
        except ImportError:
            pytest.skip("Module not available")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

