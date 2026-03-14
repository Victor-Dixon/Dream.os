#!/usr/bin/env python3
"""Utility commands for Discord bot."""

import logging
from typing import TYPE_CHECKING

import discord
from discord.ext import commands

if TYPE_CHECKING:
    from ..unified_discord_bot import UnifiedDiscordBot
    from ..discord_gui_controller import DiscordGUIController

logger = logging.getLogger(__name__)


class UtilityCommands(commands.Cog):
    """Utility and help commands."""

    def __init__(self, bot: "UnifiedDiscordBot", gui_controller: "DiscordGUIController" | None = None):
        super().__init__()
        self.bot = bot
        self.gui_controller = gui_controller
        self.logger = logging.getLogger(__name__)

    @commands.command(name="broadcast", description="Broadcast to all agents")
    async def broadcast(self, ctx: commands.Context, *, message: str) -> None:
        """Broadcast a message in the current channel."""
        await ctx.send(f"📣 Broadcast: {message}")

    @commands.command(name="help", description="Show help info")
    async def list_commands(self, ctx: commands.Context) -> None:
        """Show a basic help embed."""
        embed = discord.Embed(title="Command Help", description="Utility commands")
        await ctx.send(embed=embed)


__all__ = ["UtilityCommands"]
