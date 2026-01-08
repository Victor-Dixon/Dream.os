#!/usr/bin/env python3
"""
<!-- SSOT Domain: messaging -->

Bot Messaging Commands - Main Delegate (Modular V2 Compliance)
============================================================

Main entry point for bot messaging commands.
Uses modular command handlers for maintainability and V2 compliance.

V2 Compliant: <100 lines, modular architecture
Author: Agent-7 (Web Development Specialist)
Date: 2026-01-08
"""

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.discord_commander.unified_discord_bot import UnifiedDiscordBot

try:
    import discord
    from discord.ext import commands
except ImportError:
    discord = None
    commands = None

# Import modular command handlers
from .messaging_monitor_commands import MessagingMonitorCommands
from .messaging_core_commands import MessagingCoreCommands
from .profile_commands import ProfileCommands
from .utility_commands import UtilityCommands
from .system_control_commands import SystemControlCommands

logger = logging.getLogger(__name__)


class MessagingCommands(commands.Cog):
    """Main messaging commands cog that includes all modular handlers."""

    def __init__(self, bot: "UnifiedDiscordBot", gui_controller):
        """Initialize messaging commands with modular handlers."""
        commands.Cog.__init__(self)
        self.bot = bot
        self.gui_controller = gui_controller
        self.logger = logging.getLogger(__name__)

        # Initialize modular command handlers
        self.monitor_commands = MessagingMonitorCommands(bot)
        self.core_commands = MessagingCoreCommands(bot, gui_controller)
        self.profile_commands = ProfileCommands(bot)
        self.utility_commands = UtilityCommands(bot, gui_controller)
        self.system_commands = SystemControlCommands(bot)

        self.logger.info("✅ Messaging Commands initialized with modular architecture")

    # Delegate commands to modular handlers
    @commands.command(name="monitor", description="Control status change monitor")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def monitor(self, ctx: commands.Context, action: str = "status"):
        """Delegate to monitor commands."""
        await self.monitor_commands.monitor(ctx, action)

    @commands.command(name="message", description="Send message to agent")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def message(self, ctx: commands.Context, agent_id: str, *, message: str):
        """Delegate to core commands."""
        await self.core_commands.message(ctx, agent_id, message)

    @commands.command(name="broadcast", description="Broadcast to all agents")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def broadcast(self, ctx: commands.Context, *, message: str):
        """Delegate to core commands."""
        await self.core_commands.broadcast(ctx, message)

    @commands.command(name="mermaid", description="Render Mermaid diagram")
    async def mermaid(self, ctx: commands.Context, *, diagram_code: str):
        """Delegate to utility commands."""
        await self.utility_commands.mermaid(ctx, diagram_code)

    @commands.command(name="help", description="Show help information")
    async def help_cmd(self, ctx: commands.Context):
        """Delegate to utility commands."""
        await self.utility_commands.help_cmd(ctx)

    @commands.command(name="commands", description="List all registered commands")
    async def list_commands(self, ctx: commands.Context):
        """Delegate to utility commands."""
        await self.utility_commands.list_commands(ctx)

    @commands.command(name="aria", description="✨ View Aria's interactive profile!")
    async def aria_profile(self, ctx: commands.Context):
        """Delegate to profile commands."""
        await self.profile_commands.aria_profile(ctx)

    @commands.command(name="carmyn", aliases=["carymn"], description="🌟 Display Carmyn's awesome profile!")
    async def carmyn_profile(self, ctx: commands.Context):
        """Delegate to profile commands."""
        await self.profile_commands.carmyn_profile(ctx)

    @commands.command(name="shutdown", description="Gracefully shutdown the bot")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def shutdown_cmd(self, ctx: commands.Context):
        """Delegate to system commands."""
        await self.system_commands.shutdown_cmd(ctx)

    @commands.command(name="restart", description="Restart the Discord bot")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def restart_cmd(self, ctx: commands.Context):
        """Delegate to system commands."""
        await self.system_commands.restart_cmd(ctx)


__all__ = ["MessagingCommands"]