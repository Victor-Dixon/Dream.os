"""
Swarm Showcase Commands V2 - Agent Cellphone V2
==============================================

SSOT Domain: discord

Refactored Discord commands for swarm showcase displays.

Features:
- Simplified command handling using modular components
- Professional embed displays for swarm capabilities
- Task tracking and agent excellence showcases

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

import logging
from typing import Any

try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    from .test_utils import get_mock_discord
    mock_discord, mock_commands = get_mock_discord()
    discord = mock_discord
    commands = mock_commands

from .swarm_showcase_data import SwarmShowcaseData
from .swarm_showcase_embeds import SwarmShowcaseEmbeds

logger = logging.getLogger(__name__)

class SwarmShowcaseCommands(commands.Cog if DISCORD_AVAILABLE else object):
    """
    Professional Discord showcase for swarm capabilities using modular components.
    """

    def __init__(self, bot):
        self.bot = bot
        self.data_loader = SwarmShowcaseData()
        self.embed_factory = SwarmShowcaseEmbeds(self.data_loader)

    @commands.command(name="swarm_tasks", aliases=["tasks"])
    async def show_swarm_tasks(self, ctx: commands.Context):
        """Display all active tasks and directives."""
        try:
            embed = self.embed_factory.create_tasks_embed()
            await ctx.send(embed=embed)
        except Exception as e:
            logger.error(f"Failed to show swarm tasks: {e}")
            await ctx.send("❌ Failed to load swarm tasks. Please try again later.")

    @commands.command(name="swarm_roadmap", aliases=["roadmap"])
    async def show_swarm_roadmap(self, ctx: commands.Context):
        """Show integration roadmap and progress."""
        try:
            embed = self.embed_factory.create_roadmap_embed()
            await ctx.send(embed=embed)
        except Exception as e:
            logger.error(f"Failed to show swarm roadmap: {e}")
            await ctx.send("❌ Failed to load swarm roadmap. Please try again later.")

    @commands.command(name="swarm_excellence", aliases=["excellence"])
    async def show_swarm_excellence(self, ctx: commands.Context):
        """Showcase agent achievements and excellence."""
        try:
            embed = self.embed_factory.create_excellence_embed()
            await ctx.send(embed=embed)
        except Exception as e:
            logger.error(f"Failed to show swarm excellence: {e}")
            await ctx.send("❌ Failed to load swarm excellence showcase. Please try again later.")

    @commands.command(name="swarm_overview", aliases=["overview", "status"])
    async def show_swarm_overview(self, ctx: commands.Context):
        """Complete swarm status and missions overview."""
        try:
            embed = self.embed_factory.create_overview_embed()
            await ctx.send(embed=embed)
        except Exception as e:
            logger.error(f"Failed to show swarm overview: {e}")
            await ctx.send("❌ Failed to load swarm overview. Please try again later.")

    @commands.command(name="swarm_profile", aliases=["profile"])
    async def show_swarm_profile(self, ctx: commands.Context, agent_id: str = None):
        """Show detailed profile for specific agent."""
        if not agent_id:
            await ctx.send("❌ Please specify an agent ID. Usage: `!swarm_profile Agent-1`")
            return

        try:
            embed = self.embed_factory.create_profile_embed(agent_id)
            await ctx.send(embed=embed)
        except Exception as e:
            logger.error(f"Failed to show agent profile for {agent_id}: {e}")
            await ctx.send(f"❌ Failed to load profile for {agent_id}. Please check the agent ID and try again.")

    @commands.command(name="swarm_refresh", aliases=["refresh"])
    async def refresh_swarm_data(self, ctx: commands.Context):
        """Refresh all swarm showcase data."""
        try:
            self.data_loader.refresh_data()
            await ctx.send("✅ Swarm showcase data has been refreshed!")
        except Exception as e:
            logger.error(f"Failed to refresh swarm data: {e}")
            await ctx.send("❌ Failed to refresh swarm data. Please try again later.")

async def setup(bot):
    """Setup function for Discord cog."""
    await bot.add_cog(SwarmShowcaseCommands(bot))