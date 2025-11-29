#!/usr/bin/env python3
"""
Tests for Swarm Showcase Commands
==================================

Comprehensive test suite for Discord showcase embeds and command functionality.

Author: Agent-7
Date: 2025-11-28
"""

import json
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, Mock, patch


class TestSwarmShowcaseCommands(unittest.IsolatedAsyncioTestCase):
    """Test swarm showcase Discord commands."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_bot = MagicMock()
        
        # Mock Discord
        self.discord_patch = patch.dict('sys.modules', {
            'discord': MagicMock(),
            'discord.ext': MagicMock(),
            'discord.ext.commands': MagicMock(),
            'discord.utils': MagicMock()
        })
        self.discord_patch.start()
        
        # Mock discord.utils.utcnow
        import discord
        discord.utils.utcnow = MagicMock(return_value=MagicMock())

    def tearDown(self):
        """Clean up."""
        self.discord_patch.stop()

    def test_showcase_initialization(self):
        """Test showcase initialization."""
        from src.discord_commander.swarm_showcase_commands import SwarmShowcaseCommands
        
        showcase = SwarmShowcaseCommands(self.mock_bot)
        
        assert showcase.bot == self.mock_bot
        assert showcase.workspace_path == Path("agent_workspaces")
        assert showcase.docs_path == Path("docs")
        assert showcase.logger is not None

    async def test_show_swarm_tasks_success(self):
        """Test successful swarm tasks command."""
        from src.discord_commander.swarm_showcase_commands import SwarmShowcaseCommands
        
        showcase = SwarmShowcaseCommands(self.mock_bot)
        mock_ctx = AsyncMock()
        
        # Mock controller view
        with patch('src.discord_commander.swarm_showcase_commands.SwarmTasksControllerView') as mock_view_class:
            mock_view = MagicMock()
            mock_embed = MagicMock()
            mock_view.create_initial_embed.return_value = mock_embed
            mock_view_class.return_value = mock_view
            
            await showcase.show_swarm_tasks(mock_ctx)
            
            mock_ctx.send.assert_called_once()
            assert mock_view_class.called

    async def test_show_swarm_tasks_fallback(self):
        """Test swarm tasks command with fallback."""
        from src.discord_commander.swarm_showcase_commands import SwarmShowcaseCommands
        
        showcase = SwarmShowcaseCommands(self.mock_bot)
        mock_ctx = AsyncMock()
        
        # Mock controller failure, should fallback
        with patch('src.discord_commander.swarm_showcase_commands.SwarmTasksControllerView', side_effect=Exception("Test error")):
            showcase._load_all_agent_statuses = MagicMock(return_value=[
                {
                    "agent_id": "Agent-1",
                    "current_mission": "Test Mission",
                    "current_tasks": ["Task 1"],
                    "mission_priority": "HIGH",
                    "status": "ACTIVE_AGENT_MODE"
                }
            ])
            
            await showcase.show_swarm_tasks(mock_ctx)
            
            # Should call send (fallback)
            assert mock_ctx.send.called

    async def test_show_swarm_tasks_double_failure(self):
        """Test swarm tasks command with both controller and fallback failure."""
        from src.discord_commander.swarm_showcase_commands import SwarmShowcaseCommands
        
        showcase = SwarmShowcaseCommands(self.mock_bot)
        mock_ctx = AsyncMock()
        
        with patch('src.discord_commander.swarm_showcase_commands.SwarmTasksControllerView', side_effect=Exception("Test error")):
            showcase._create_tasks_embed = AsyncMock(side_effect=Exception("Fallback error"))
            
            await showcase.show_swarm_tasks(mock_ctx)
            
            # Should send error message
            assert mock_ctx.send.called
            assert "Error" in str(mock_ctx.send.call_args)

    async def test_create_tasks_embed(self):
        """Test tasks embed creation."""
        from src.discord_commander.swarm_showcase_commands import SwarmShowcaseCommands
        
        showcase = SwarmShowcaseCommands(self.mock_bot)
        showcase._load_all_agent_statuses = MagicMock(return_value=[
            {
                "agent_id": "Agent-1",
                "current_mission": "Test Mission",
                "current_tasks": ["Task 1", "Task 2"],
                "mission_priority": "HIGH",
                "status": "ACTIVE_AGENT_MODE"
            },
            {
                "agent_id": "Agent-2",
                "current_mission": "Test Mission 2",
                "current_tasks": [],
                "mission_priority": "MEDIUM",
                "status": "ACTIVE_AGENT_MODE"
            }
        ])
        
        # Mock chunk_field_value
        with patch('src.discord_commander.swarm_showcase_commands.chunk_field_value', return_value=["Test value"]):
            embed = await showcase._create_tasks_embed()
            
            assert embed is not None
            assert "SWARM TASKS" in embed.title

    async def test_create_tasks_embed_priority_sorting(self):
        """Test tasks embed priority sorting."""
        from src.discord_commander.swarm_showcase_commands import SwarmShowcaseCommands
        
        showcase = SwarmShowcaseCommands(self.mock_bot)
        showcase._load_all_agent_statuses = MagicMock(return_value=[
            {"agent_id": "Agent-1", "mission_priority": "LOW", "current_mission": "Low", "current_tasks": [], "status": "ACTIVE"},
            {"agent_id": "Agent-2", "mission_priority": "CRITICAL", "current_mission": "Critical", "current_tasks": [], "status": "ACTIVE"},
            {"agent_id": "Agent-3", "mission_priority": "HIGH", "current_mission": "High", "current_tasks": [], "status": "ACTIVE"},
        ])
        
        with patch('src.discord_commander.swarm_showcase_commands.chunk_field_value', return_value=["Test"]):
            embed = await showcase._create_tasks_embed()
            
            assert embed is not None

    async def test_show_swarm_roadmap_success(self):
        """Test successful roadmap command."""
        from src.discord_commander.swarm_showcase_commands import SwarmShowcaseCommands
        
        showcase = SwarmShowcaseCommands(self.mock_bot)
        mock_ctx = AsyncMock()
        
        await showcase.show_swarm_roadmap(mock_ctx)
        
        mock_ctx.send.assert_called_once()

    async def test_show_swarm_roadmap_exception(self):
        """Test roadmap command with exception."""
        from src.discord_commander.swarm_showcase_commands import SwarmShowcaseCommands
        
        showcase = SwarmShowcaseCommands(self.mock_bot)
        mock_ctx = AsyncMock()
        showcase._create_roadmap_embed = AsyncMock(side_effect=Exception("Test error"))
        
        await showcase.show_swarm_roadmap(mock_ctx)
        
        assert "Error" in str(mock_ctx.send.call_args)

    async def test_create_roadmap_embed(self):
        """Test roadmap embed creation."""
        from src.discord_commander.swarm_showcase_commands import SwarmShowcaseCommands
        
        showcase = SwarmShowcaseCommands(self.mock_bot)
        
        embed = await showcase._create_roadmap_embed()
        
        assert embed is not None
        assert "ROADMAP" in embed.title
        assert embed.footer is not None

    async def test_show_swarm_excellence_success(self):
        """Test successful excellence command."""
        from src.discord_commander.swarm_showcase_commands import SwarmShowcaseCommands
        
        showcase = SwarmShowcaseCommands(self.mock_bot)
        mock_ctx = AsyncMock()
        
        await showcase.show_swarm_excellence(mock_ctx)
        
        mock_ctx.send.assert_called_once()

    async def test_show_swarm_excellence_exception(self):
        """Test excellence command with exception."""
        from src.discord_commander.swarm_showcase_commands import SwarmShowcaseCommands
        
        showcase = SwarmShowcaseCommands(self.mock_bot)
        mock_ctx = AsyncMock()
        showcase._create_excellence_embed = AsyncMock(side_effect=Exception("Test error"))
        
        await showcase.show_swarm_excellence(mock_ctx)
        
        assert "Error" in str(mock_ctx.send.call_args)

    async def test_create_excellence_embed(self):
        """Test excellence embed creation."""
        from src.discord_commander.swarm_showcase_commands import SwarmShowcaseCommands
        
        showcase = SwarmShowcaseCommands(self.mock_bot)
        
        embed = await showcase._create_excellence_embed()
        
        assert embed is not None
        assert "EXCELLENCE" in embed.title
        assert embed.footer is not None

    async def test_show_swarm_overview_success(self):
        """Test successful overview command."""
        from src.discord_commander.swarm_showcase_commands import SwarmShowcaseCommands
        
        showcase = SwarmShowcaseCommands(self.mock_bot)
        mock_ctx = AsyncMock()
        showcase._load_all_agent_statuses = MagicMock(return_value=[
            {"agent_id": f"Agent-{i}", "status": "ACTIVE_AGENT_MODE", "current_tasks": ["Task"], "completed_tasks": []}
            for i in range(1, 9)
        ])
        
        await showcase.show_swarm_overview(mock_ctx)
        
        mock_ctx.send.assert_called_once()

    async def test_show_swarm_overview_exception(self):
        """Test overview command with exception."""
        from src.discord_commander.swarm_showcase_commands import SwarmShowcaseCommands
        
        showcase = SwarmShowcaseCommands(self.mock_bot)
        mock_ctx = AsyncMock()
        showcase._create_overview_embed = AsyncMock(side_effect=Exception("Test error"))
        
        await showcase.show_swarm_overview(mock_ctx)
        
        assert "Error" in str(mock_ctx.send.call_args)

    async def test_create_overview_embed(self):
        """Test overview embed creation."""
        from src.discord_commander.swarm_showcase_commands import SwarmShowcaseCommands
        
        showcase = SwarmShowcaseCommands(self.mock_bot)
        showcase._load_all_agent_statuses = MagicMock(return_value=[
            {"agent_id": f"Agent-{i}", "status": "ACTIVE_AGENT_MODE", "current_tasks": ["Task"], "completed_tasks": []}
            for i in range(1, 9)
        ])
        
        embed = await showcase._create_overview_embed()
        
        assert embed is not None
        assert "DASHBOARD" in embed.title

    def test_load_all_agent_statuses_success(self):
        """Test loading all agent statuses successfully."""
        from src.discord_commander.swarm_showcase_commands import SwarmShowcaseCommands
        
        showcase = SwarmShowcaseCommands(self.mock_bot)
        
        # Mock status files
        mock_status = {"agent_id": "Agent-1", "status": "ACTIVE"}
        
        with patch('pathlib.Path.exists', return_value=True), \
             patch('builtins.open', unittest.mock.mock_open(read_data=json.dumps(mock_status))):
            statuses = showcase._load_all_agent_statuses()
            
            assert isinstance(statuses, list)

    def test_load_all_agent_statuses_missing_file(self):
        """Test loading statuses when file doesn't exist."""
        from src.discord_commander.swarm_showcase_commands import SwarmShowcaseCommands
        
        showcase = SwarmShowcaseCommands(self.mock_bot)
        
        with patch('pathlib.Path.exists', return_value=False):
            statuses = showcase._load_all_agent_statuses()
            
            assert isinstance(statuses, list)
            assert len(statuses) == 0

    def test_load_all_agent_statuses_exception(self):
        """Test loading statuses with exception."""
        from src.discord_commander.swarm_showcase_commands import SwarmShowcaseCommands
        
        showcase = SwarmShowcaseCommands(self.mock_bot)
        
        with patch('pathlib.Path.exists', return_value=True), \
             patch('builtins.open', side_effect=Exception("Test error")):
            statuses = showcase._load_all_agent_statuses()
            
            assert isinstance(statuses, list)

    def test_load_roadmap_data_exists(self):
        """Test loading roadmap data when file exists."""
        from src.discord_commander.swarm_showcase_commands import SwarmShowcaseCommands
        
        showcase = SwarmShowcaseCommands(self.mock_bot)
        
        with patch('pathlib.Path.exists', return_value=True):
            data = showcase._load_roadmap_data()
            
            assert isinstance(data, dict)
            assert "phases" in data or "goldmines" in data

    def test_load_roadmap_data_not_exists(self):
        """Test loading roadmap data when file doesn't exist."""
        from src.discord_commander.swarm_showcase_commands import SwarmShowcaseCommands
        
        showcase = SwarmShowcaseCommands(self.mock_bot)
        
        with patch('pathlib.Path.exists', return_value=False):
            data = showcase._load_roadmap_data()
            
            assert isinstance(data, dict)
            assert "phases" in data

    def test_command_aliases(self):
        """Test that command aliases are properly defined."""
        from src.discord_commander.swarm_showcase_commands import SwarmShowcaseCommands
        
        showcase = SwarmShowcaseCommands(self.mock_bot)
        
        # Verify command methods exist
        self.assertTrue(hasattr(showcase, 'show_swarm_tasks'))
        self.assertTrue(hasattr(showcase, 'show_swarm_roadmap'))
        self.assertTrue(hasattr(showcase, 'show_swarm_excellence'))
        self.assertTrue(hasattr(showcase, 'show_swarm_overview'))

    def test_load_all_agent_statuses_malformed_json(self):
        """Test loading statuses with malformed JSON."""
        from src.discord_commander.swarm_showcase_commands import SwarmShowcaseCommands
        
        showcase = SwarmShowcaseCommands(self.mock_bot)
        
        with patch('pathlib.Path.exists', return_value=True), \
             patch('builtins.open', unittest.mock.mock_open(read_data="invalid json")):
            statuses = showcase._load_all_agent_statuses()
            
            # Should handle gracefully
            assert isinstance(statuses, list)

    def test_load_all_agent_statuses_missing_fields(self):
        """Test loading statuses with missing fields."""
        from src.discord_commander.swarm_showcase_commands import SwarmShowcaseCommands
        
        showcase = SwarmShowcaseCommands(self.mock_bot)
        
        # Status with missing fields
        mock_status = {"agent_id": "Agent-1"}  # Missing other fields
        
        with patch('pathlib.Path.exists', return_value=True), \
             patch('builtins.open', unittest.mock.mock_open(read_data=json.dumps(mock_status))):
            statuses = showcase._load_all_agent_statuses()
            
            assert isinstance(statuses, list)
            assert len(statuses) > 0

    async def test_create_tasks_embed_empty_agents(self):
        """Test tasks embed creation with no agents."""
        from src.discord_commander.swarm_showcase_commands import SwarmShowcaseCommands
        
        showcase = SwarmShowcaseCommands(self.mock_bot)
        showcase._load_all_agent_statuses = MagicMock(return_value=[])
        
        with patch('src.discord_commander.swarm_showcase_commands.chunk_field_value', return_value=["Test"]):
            embed = await showcase._create_tasks_embed()
            
            assert embed is not None
            assert "SWARM TASKS" in embed.title

    async def test_create_tasks_embed_many_agents(self):
        """Test tasks embed creation with many agents (limit to 8)."""
        from src.discord_commander.swarm_showcase_commands import SwarmShowcaseCommands
        
        showcase = SwarmShowcaseCommands(self.mock_bot)
        # Create 10 agents (should limit to 8)
        showcase._load_all_agent_statuses = MagicMock(return_value=[
            {
                "agent_id": f"Agent-{i}",
                "current_mission": f"Mission {i}",
                "current_tasks": [f"Task {i}"],
                "mission_priority": "HIGH",
                "status": "ACTIVE_AGENT_MODE"
            }
            for i in range(1, 11)
        ])
        
        with patch('src.discord_commander.swarm_showcase_commands.chunk_field_value', return_value=["Test"]):
            embed = await showcase._create_tasks_embed()
            
            assert embed is not None
            # Should limit to 8 agents
            assert len(embed.fields) <= 8

    async def test_create_overview_embed_empty_statuses(self):
        """Test overview embed creation with empty agent statuses."""
        from src.discord_commander.swarm_showcase_commands import SwarmShowcaseCommands
        
        showcase = SwarmShowcaseCommands(self.mock_bot)
        showcase._load_all_agent_statuses = MagicMock(return_value=[])
        
        embed = await showcase._create_overview_embed()
        
        assert embed is not None
        assert "DASHBOARD" in embed.title

    def test_load_all_agent_statuses_permission_error(self):
        """Test loading statuses with permission error."""
        from src.discord_commander.swarm_showcase_commands import SwarmShowcaseCommands
        
        showcase = SwarmShowcaseCommands(self.mock_bot)
        
        with patch('pathlib.Path.exists', return_value=True), \
             patch('builtins.open', side_effect=PermissionError("Permission denied")):
            statuses = showcase._load_all_agent_statuses()
            
            # Should handle gracefully
            assert isinstance(statuses, list)


class TestSetupFunction:
    """Test setup function."""

    @patch('src.discord_commander.swarm_showcase_commands.DISCORD_AVAILABLE', True)
    async def test_setup_with_discord(self):
        """Test setup function with Discord available."""
        from src.discord_commander.swarm_showcase_commands import setup
        
        mock_bot = AsyncMock()
        
        await setup(mock_bot)
        
        mock_bot.add_cog.assert_called_once()

    @patch('src.discord_commander.swarm_showcase_commands.DISCORD_AVAILABLE', False)
    async def test_setup_without_discord(self):
        """Test setup function without Discord."""
        from src.discord_commander.swarm_showcase_commands import setup
        
        mock_bot = AsyncMock()
        
        await setup(mock_bot)
        
        # Should not add cog
        mock_bot.add_cog.assert_not_called()


if __name__ == "__main__":
    unittest.main()
