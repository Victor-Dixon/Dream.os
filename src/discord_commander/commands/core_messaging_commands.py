"""Core messaging commands for agent communication."""

import logging

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class CoreMessagingCommands(commands.Cog):
    """Core messaging commands for agent communication."""

    def __init__(self, bot, gui_controller=None):
        super().__init__()
        self.bot = bot
        self.gui_controller = gui_controller
        self.logger = logging.getLogger(__name__)

    @commands.command(name="gui", description="Open messaging GUI")
    async def gui(self, ctx: commands.Context) -> None:
        """Open interactive messaging GUI placeholder."""
        embed = discord.Embed(
            title="🤖 Agent Messaging Control Panel",
            description="Use the controls below to interact with the swarm",
            color=discord.Color.blue(),
            timestamp=discord.utils.utcnow(),
        )
        await ctx.send(embed=embed)

    @commands.command(name="status", description="View swarm status")
    async def status(self, ctx: commands.Context) -> None:
        """View swarm status placeholder."""
        await ctx.send("Swarm status is currently unavailable in this stub.")

    @commands.command(name="monitor", description="Control status change monitor")
    async def monitor(self, ctx: commands.Context, action: str = "status") -> None:
        """Control status change monitor placeholder."""
        await ctx.send(f"Monitor action '{action}' requested.")


__all__ = ["CoreMessagingCommands"]
