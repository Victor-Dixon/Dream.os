"""
Status Reader V2 - Agent Cellphone V2
====================================

SSOT Domain: discord

Refactored status reader using service architecture for Discord commands.

Features:
- Async/sync status reading with caching
- Discord embed formatting
- Error handling and fallbacks
- Command-based interface

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
        !status              - Show all agents' status overview
        !status Agent-1      - Show specific agent status
        !agent Agent-2       - Show Agent-2 status

        Examples:
        !status
        !status Agent-1
        !agent_status Agent-3
        """
        if agent_id:
            await self._show_single_agent_status(ctx, agent_id)
        else:
            await self._show_all_agents_overview(ctx)

    async def _show_single_agent_status(self, ctx: commands.Context, agent_id: str):
        """Show detailed status for a specific agent."""
        # Normalize agent ID format
        if not agent_id.startswith("Agent-"):
            agent_id = f"Agent-{agent_id}"

        # Read status
        status_data = await self.status_service.read_agent_status_async(agent_id)

        if not status_data:
            embed = discord.Embed(
                title="❌ Agent Not Found",
                description=f"Could not read status for {agent_id}",
                color=discord.Color.red()
            )
            embed.add_field(
                name="Possible Issues",
                value="• Agent workspace doesn't exist\n• Status file is missing or corrupted\n• Agent is offline",
                inline=False
            )
            await ctx.send(embed=embed)
            return

        # Create embed using factory
        embed = agent_status_factory.create_embed(status_data)

        # Add additional context
        embed.add_field(
            name="Requested by",
            value=ctx.author.display_name,
            inline=True
        )

        embed.set_footer(text=f"Status Reader V2 | Agent Cellphone Swarm")

        await ctx.send(embed=embed)

    async def _show_all_agents_overview(self, ctx: commands.Context):
        """Show overview of all agents' status."""
        embed = discord.Embed(
            title="🐝 Swarm Status Overview",
            description="Current status of all swarm agents",
            color=discord.Color.blue()
        )

        # Read all statuses
        all_statuses = await self.status_service.read_all_statuses_async()

        if not all_statuses:
            embed.add_field(
                name="❌ No Agents Found",
                value="Unable to read status for any agents",
                inline=False
            )
        else:
            # Group by status
            active_agents = []
            inactive_agents = []
            unknown_agents = []

            for agent_id, status in all_statuses.items():
                agent_status = status.get("status", "UNKNOWN")
                mission = status.get("current_mission", "No mission")[:30]

                display_text = f"{agent_id}: {mission}"

                if agent_status == "ACTIVE_AGENT_MODE":
                    active_agents.append(display_text)
                elif agent_status == "INACTIVE":
                    inactive_agents.append(display_text)
                else:
                    unknown_agents.append(display_text)

            # Add fields for each status group
            if active_agents:
                embed.add_field(
                    name="🟢 Active Agents",
                    value="\n".join(active_agents[:8]),  # Discord limit
                    inline=False
                )

            if inactive_agents:
                embed.add_field(
                    name="🔴 Inactive Agents",
                    value="\n".join(inactive_agents[:8]),
                    inline=False
                )

            if unknown_agents:
                embed.add_field(
                    name="❓ Unknown Status",
                    value="\n".join(unknown_agents[:8]),
                    inline=False
                )

            # Summary stats
            total_agents = len(all_statuses)
            active_count = len(active_agents)

            embed.add_field(
                name="📊 Summary",
                value=f"Total: {total_agents} | Active: {active_count} | Inactive: {len(inactive_agents)}",
                inline=False
            )

        embed.set_footer(text=f"Use !status Agent-X for detailed view | Cache TTL: 30s")
        await ctx.send(embed=embed)

    @commands.command(name="status_refresh", aliases=["refresh_status", "clear_status_cache"])
    async def refresh_status_cache(self, ctx: commands.Context):
        """
        Refresh status cache and force reload all agent statuses.

        Usage: !status_refresh
        """
        try:
            # Clear cache
            self.status_service.clear_cache()

            # Get fresh stats
            cache_stats = self.status_service.get_cache_stats()

            embed = discord.Embed(
                title="🔄 Status Cache Refreshed",
                description="All agent status caches have been cleared and will reload on next request",
                color=discord.Color.green()
            )

            embed.add_field(
                name="Cache Stats",
                value=f"Max Size: {cache_stats['max_size']}\nTTL: {cache_stats['ttl_seconds']}s",
                inline=True
            )

            embed.add_field(
                name="Requested by",
                value=ctx.author.display_name,
                inline=True
            )

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error refreshing status cache: {e}")
            await ctx.send(f"❌ Error refreshing cache: {e}")

    @commands.command(name="status_stats", aliases=["status_info", "cache_stats"])
    async def show_status_stats(self, ctx: commands.Context):
        """
        Show status reader statistics and cache information.

        Usage: !status_stats
        """
        try:
            cache_stats = self.status_service.get_cache_stats()

            embed = discord.Embed(
                title="📊 Status Reader Stats",
                description="Cache and performance statistics",
                color=discord.Color.purple()
            )

            embed.add_field(
                name="Cache Information",
                value=f"Cached Agents: {cache_stats['cached_agents']}\nMax Size: {cache_stats['max_size']}\nTTL: {cache_stats['ttl_seconds']}s",
                inline=True
            )

            oldest_age = cache_stats.get('oldest_cache_age')
            if oldest_age:
                embed.add_field(
                    name="Cache Age",
                    value=f"Oldest: {oldest_age:.1f}s ago",
                    inline=True
                )
            else:
                embed.add_field(
                    name="Cache Age",
                    value="No cached data",
                    inline=True
                )

            # Add workspace info
            embed.add_field(
                name="Configuration",
                value="Workspace: agent_workspaces\nFormat: JSON status files",
                inline=False
            )

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error showing status stats: {e}")
            await ctx.send(f"❌ Error getting stats: {e}")

async def setup(bot):
    """Setup function for Discord cog."""
    await bot.add_cog(StatusReaderCommands(bot))