#!/usr/bin/env python3
"""
Example Unified Command - Code Deduplication Migration
======================================================

<!-- SSOT Domain: discord -->

Example showing how to migrate Discord commands to use UnifiedCommand base class.
Demonstrates the consolidated patterns for initialization, error handling, and metrics.

V2 Compliance: Shows migration pattern from BaseCommandCog to UnifiedCommand

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-11
"""

import logging
from typing import TYPE_CHECKING

from ..base.unified_command import UnifiedCommand

if TYPE_CHECKING:
    from src.discord_commander.unified_discord_bot import UnifiedDiscordBot
    from src.discord_commander.discord_gui_controller import DiscordGUIController

try:
    import discord
    from discord.ext import commands
except ImportError:
    discord = None
    commands = None

logger = logging.getLogger(__name__)


class ExampleUnifiedCommands(UnifiedCommand):
    """
    Example command class migrated to UnifiedCommand base class.

    Demonstrates:
    - Automatic metrics tracking
    - Standardized permission checking
    - Context manager for command execution
    - Consolidated error handling
    """

    def __init__(self, bot: "UnifiedDiscordBot", gui_controller: "DiscordGUIController"):
        """Initialize example unified commands."""
        super().__init__(bot, gui_controller, "ExampleUnifiedCommands")

    @commands.command(name="example", description="Example unified command")
    async def example_command(self, ctx: commands.Context):
        """Example command using unified execution pattern."""
        # Check permissions using unified method
        if not await self.require_permissions(ctx):
            return

        # Use unified command execution with automatic tracking
        async with self.execute_command(ctx, "example_command"):
            # Command logic here - any exceptions will be handled automatically
            embed = self.create_success_embed(
                title="Example Command",
                description="This command uses the unified execution pattern!"
            )
            embed.add_field(
                name="Features",
                value="• Automatic metrics tracking\n• Standardized error handling\n• Permission checking",
                inline=False
            )

            await ctx.send(embed=embed)

    @commands.command(name="metrics", description="Show command metrics")
    async def show_metrics(self, ctx: commands.Context):
        """Show command execution metrics."""
        if not await self.require_permissions(ctx, ["Admin"]):
            return

        async with self.execute_command(ctx, "show_metrics"):
            metrics = self.get_metrics()

            embed = self.create_info_embed(
                title="Command Metrics",
                description=f"Metrics for {metrics['cog_name']}"
            )

            embed.add_field(
                name="Execution Stats",
                value=f"Total: {metrics['total_commands']}\nSuccessful: {metrics['successful_commands']}\nFailed: {metrics['failed_commands']}",
                inline=True
            )

            embed.add_field(
                name="Performance",
                value=f"Success Rate: {metrics['success_rate']:.1%}\nHistory Size: {metrics['history_size']}",
                inline=True
            )

            await ctx.send(embed=embed)

    @commands.command(name="history", description="Show recent command history")
    async def show_history(self, ctx: commands.Context, limit: int = 5):
        """Show recent command execution history."""
        if not await self.require_permissions(ctx, ["Admin"]):
            return

        async with self.execute_command(ctx, "show_history", limit=limit):
            history = self.get_command_history(limit)

            embed = self.create_info_embed(
                title="Command History",
                description=f"Recent {len(history)} commands"
            )

            for i, entry in enumerate(history, 1):
                status_emoji = "✅" if entry['success'] else "❌"
                embed.add_field(
                    name=f"{i}. {entry['command']} {status_emoji}",
                    value=f"User: {entry['user']}\nDuration: {entry['execution_time']:.3f}s\nTime: {entry['timestamp']:.0f}",
                    inline=True
                )

            await ctx.send(embed=embed)


async def setup(bot):
    """Setup function for Discord cog loading."""
    await bot.add_cog(ExampleUnifiedCommands(bot, bot.gui_controller))