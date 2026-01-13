"""
Status Reader - Agent Cellphone V2
==================================

SSOT Domain: discord

Refactored entry point for Discord status reading commands.
All core logic has been extracted into service architecture for V2 compliance.

Features:
- Async/sync status reading with caching
- Discord embed formatting
- Error handling and fallbacks
- Command-based interface (status_reader_v2.py)

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

import logging
from typing import Optional

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

from .status_service import status_service
from .embed_factory import agent_status_factory

logger = logging.getLogger(__name__)

class StatusReaderCommands(commands.Cog if DISCORD_AVAILABLE else object):
    """
    Discord commands for reading and displaying agent status information.
    """

    def __init__(self, bot):
        self.bot = bot
        self.status_service = status_service

    @commands.command(name="status", aliases=["agent_status", "agent"])
    async def show_agent_status(self, ctx: commands.Context, agent_id: Optional[str] = None):
        """
        Display status information for agents.

        Usage:
        !status - Show all agent statuses
        !status Agent-1 - Show specific agent status
        !agent_status Agent-2 - Alternative command
        !agent Agent-3 - Short alias
        """
        try:
            embed = await self.status_service.get_status_embed(agent_id)
            await ctx.send(embed=embed)
        except Exception as e:
            logger.error(f"Error in show_agent_status: {e}")
            embed = discord.Embed(
                title="❌ Status Error",
                description=f"Failed to retrieve status information: {str(e)}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @commands.command(name="status_refresh", aliases=["refresh_status"])
    async def refresh_status_cache(self, ctx: commands.Context):
        """
        Refresh the status cache and reload agent information.

        Usage: !status_refresh
        """
        try:
            await self.status_service.refresh_cache()
            embed = discord.Embed(
                title="✅ Status Cache Refreshed",
                description="Agent status cache has been updated with latest information.",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        except Exception as e:
            logger.error(f"Error in refresh_status_cache: {e}")
            embed = discord.Embed(
                title="❌ Cache Refresh Error",
                description=f"Failed to refresh status cache: {str(e)}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @commands.command(name="status_summary", aliases=["status_overview"])
    async def show_status_summary(self, ctx: commands.Context):
        """
        Display a summary overview of all agent statuses.

        Usage: !status_summary
        """
        try:
            embed = await self.status_service.get_status_summary_embed()
            await ctx.send(embed=embed)
        except Exception as e:
            logger.error(f"Error in show_status_summary: {e}")
            embed = discord.Embed(
                title="❌ Summary Error",
                description=f"Failed to generate status summary: {str(e)}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

# Export for backward compatibility
StatusReader = StatusReaderCommands
