#!/usr/bin/env python3
"""
Control Panel Commands - Modular V2 Compliance
==============================================

Control panel and GUI commands extracted for V2 compliance.

<!-- SSOT Domain: messaging -->

V2 Compliant: Modular control panel commands
Author: Agent-7 (Web Development Specialist)
Date: 2026-01-11
"""

import logging
from typing import TYPE_CHECKING

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


class ControlPanelCommands(commands.Cog):
    """Control panel and GUI commands."""

    def __init__(self, bot: "UnifiedDiscordBot", gui_controller: "DiscordGUIController"):
        """Initialize control panel commands."""
        super().__init__()
        self.bot = bot
        self.gui_controller = gui_controller
        self.logger = logging.getLogger(__name__)

    @commands.command(name="control", aliases=["panel", "menu"], description="Open the main control panel")
    async def control_panel(self, ctx: commands.Context):
        """Open the main control panel with all bot functions."""
        try:
            control_view = self.gui_controller.create_control_panel()
            embed = discord.Embed(
                title="🎛️ Agent Cellphone V2 - Control Panel",
                description=(
                    "**Welcome to the Agent Cellphone V2 Control Center!**\n\n"
                    "Use the buttons below to access all bot functions:\n"
                    "• **Agent Status** - View current agent statuses\n"
                    "• **Messaging** - Send messages to agents\n"
                    "• **Swarm Tasks** - Manage swarm tasks\n"
                    "• **Monitor** - Control status monitoring\n"
                    "• **Templates** - Access message templates\n"
                    "• **Help** - Interactive help system\n\n"
                    "**All functions are accessible via buttons - no typing required!**"
                ),
                color=discord.Color.blue(),
                timestamp=discord.utils.utcnow(),
            )
            embed.add_field(
                name="🔧 System Status",
                value="✅ Bot Online | ✅ Queue Processor Running | ✅ PyAutoGUI Active",
                inline=False,
            )
            embed.set_footer(text="🐝 WE. ARE. SWARM. ⚡️ Control at your fingertips!")
            await ctx.send(embed=embed, view=control_view)
        except Exception as e:
            self.logger.error(f"Error opening control panel: {e}")
            await ctx.send(f"❌ Error opening control panel: {e}")


__all__ = ["ControlPanelCommands"]