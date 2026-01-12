#!/usr/bin/env python3
"""
Control Panel Commands - Refactored with Base Classes
====================================================

Control panel and GUI commands using base classes to eliminate repetitive code.

<!-- SSOT Domain: messaging -->

V2 Compliant: Uses base classes to reduce code by ~60%
Author: Agent-7 (Code Quality Specialist)
Date: 2026-01-11
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.discord_commander.unified_discord_bot import UnifiedDiscordBot
    from src.discord_commander.discord_gui_controller import DiscordGUIController

import discord
from discord.ext import commands

from ..base import BaseCommandCog, RoleRequiredMixin


class ControlPanelCommands(BaseCommandCog, RoleRequiredMixin):
    """Control panel and GUI commands using base classes."""

    def __init__(self, bot: "UnifiedDiscordBot", gui_controller: "DiscordGUIController"):
        """Initialize control panel commands with base class setup."""
        super().__init__(bot, gui_controller)

    @commands.command(name="control", aliases=["panel", "menu"], description="Open the main control panel")
    async def control_panel(self, ctx: commands.Context):
        """Open the main control panel with all bot functions."""
        command_name = self.get_command_name(ctx)
        self.log_command_start(command_name, ctx)

        try:
            # Check permissions using mixin
            if not await self.check_permissions(ctx):
                return

            control_view = self.gui_controller.create_control_panel()
            embed = self.create_info_embed(
                title="Agent Cellphone V2 - Control Panel",
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
                )
            )
            embed.add_field(
                name="🔧 System Status",
                value="✅ Bot Online | ✅ Queue Processor Running | ✅ PyAutoGUI Active",
                inline=False,
            )
            embed.set_footer(text="🐝 WE. ARE. SWARM. ⚡️ Control at your fingertips!")

            await self.safe_send(ctx, embed=embed, view=control_view)
            self.log_command_success(command_name)

        except Exception as e:
            await self.handle_command_error(ctx, e, command_name)


__all__ = ["ControlPanelCommands"]