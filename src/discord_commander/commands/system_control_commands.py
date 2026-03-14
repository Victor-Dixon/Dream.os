#!/usr/bin/env python3
"""System control commands for the Discord bot."""

import logging
from discord.ext import commands

logger = logging.getLogger(__name__)


class SystemControlCommands(commands.Cog):
    """Minimal system control commands."""

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.logger = logging.getLogger(__name__)

    @commands.command(name="shutdown", description="Gracefully shutdown the bot")
    async def shutdown_cmd(self, ctx: commands.Context) -> None:
        """Shutdown command placeholder."""
        await ctx.send("Shutting down...")
        await self.bot.close()

    @commands.command(name="restart", description="Restart the Discord bot")
    async def restart_cmd(self, ctx: commands.Context) -> None:
        """Restart command placeholder."""
        await ctx.send("Restart requested (not implemented in this stub).")


__all__ = ["SystemControlCommands"]
