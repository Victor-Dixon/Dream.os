#!/usr/bin/env python3
"""Messaging command aggregator for Discord bot."""

import logging
from typing import TYPE_CHECKING

from discord.ext import commands

from .messaging_core_commands import MessagingCoreCommands
from .messaging_monitor_commands import MessagingMonitorCommands
from .profile_commands import ProfileCommands
from .system_control_commands import SystemControlCommands
from .utility_commands import UtilityCommands

if TYPE_CHECKING:
    from ..unified_discord_bot import UnifiedDiscordBot

logger = logging.getLogger(__name__)


class MessagingCommands(commands.Cog):
    """Main messaging commands cog that includes all modular handlers."""

    def __init__(self, bot: "UnifiedDiscordBot", gui_controller=None):
        super().__init__()
        self.bot = bot
        self.gui_controller = gui_controller
        self.monitor_commands = MessagingMonitorCommands(bot)
        self.core_commands = MessagingCoreCommands(bot)
        self.profile_commands = ProfileCommands(bot)
        self.utility_commands = UtilityCommands(bot)
        self.system_commands = SystemControlCommands(bot)
        self.logger = logging.getLogger(__name__)

    @commands.command(name="monitor", description="Monitor messaging status")
    async def monitor(self, ctx: commands.Context, action: str = "status") -> None:
        """Delegate to monitor commands."""
        await self.monitor_commands.monitor(ctx, action)

    @commands.command(name="message", description="Send message to agent")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def message(self, ctx: commands.Context, agent_id: str, *, message: str) -> None:
        """Delegate to core commands."""
        await self.core_commands.message(ctx, agent_id, message)

    @commands.command(name="broadcast", description="Broadcast to all agents")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def broadcast(self, ctx: commands.Context, *, message: str) -> None:
        """Delegate to utility commands."""
        await self.utility_commands.broadcast(ctx, message)

    @commands.command(name="aria", description="✨ View Aria's interactive profile!")
    async def aria_profile(self, ctx: commands.Context) -> None:
        """Delegate to profile commands."""
        await self.profile_commands.aria_profile(ctx)

    @commands.command(name="carmyn", aliases=["carymn"], description="🌟 Display Carmyn's profile!")
    async def carmyn_profile(self, ctx: commands.Context) -> None:
        """Delegate to profile commands."""
        await self.profile_commands.carmyn_profile(ctx)

    @commands.command(name="shutdown", description="Gracefully shutdown the bot")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def shutdown_cmd(self, ctx: commands.Context) -> None:
        """Delegate to system commands."""
        await self.system_commands.shutdown_cmd(ctx)

    @commands.command(name="restart", description="Restart the Discord bot")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def restart_cmd(self, ctx: commands.Context) -> None:
        """Delegate to system commands."""
        await self.system_commands.restart_cmd(ctx)


__all__ = ["MessagingCommands"]
