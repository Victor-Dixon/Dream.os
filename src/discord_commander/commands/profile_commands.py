<<<<<<< HEAD
#!/usr/bin/env python3
"""
Profile Commands - Modular V2 Compliance
========================================

Profile display commands (Aria, Carmyn) extracted from bot_messaging_commands.py.

<!-- SSOT Domain: messaging -->

V2 Compliant: Modular profile commands
Author: Agent-7 (Web Development Specialist)
Date: 2026-01-08
=======
"""
<!-- SSOT Domain: discord -->

Profile Commands
================

Profile commands extracted from unified_discord_bot.py for V2 compliance.
Handles: Agent profile displays (Aria, Carmyn).

V2 Compliance: <300 lines, <5 classes, <10 functions
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
"""

import logging

import discord
from discord.ext import commands

<<<<<<< HEAD
from ...core.base.common_command_base import CommonCommandBase

logger = logging.getLogger(__name__)


class ProfileCommands(CommonCommandBase):
    """Profile display commands for team members."""

    def __init__(self, bot):
        """Initialize profile commands."""
        super().__init__(bot)  # Uses CommonCommandBase for standardized initialization

    @commands.command(name="aria", description="✨ View Aria's interactive profile!")
    async def aria_profile(self, ctx: commands.Context):
        """Display Aria's interactive profile with buttons!"""
        try:
            from src.discord_commander.views.aria_profile_view import AriaProfileView
=======
logger = logging.getLogger(__name__)


class ProfileCommands(commands.Cog):
    """Profile commands for displaying agent profiles."""

    def __init__(self, bot, gui_controller):
        """Initialize profile commands."""
        self.bot = bot
        self.gui_controller = gui_controller
        self.logger = logging.getLogger(__name__)

    @commands.command(name="aria", description="✨ View Aria's interactive profile!")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def aria_profile(self, ctx: commands.Context):
        """Display Aria's interactive profile with buttons!"""
        self.logger.info(f"Command 'aria_profile' triggered by {ctx.author}")
        try:
            from src.discord_commander.views.aria_profile_view import AriaProfileView

>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
            view = AriaProfileView()
            embed = view._create_main_embed()
            await ctx.send(embed=embed, view=view)
        except Exception as e:
            self.logger.error(f"Error in !aria command: {e}", exc_info=True)
            await ctx.send(f"❌ Oops! Something went wrong: {e}")

    @commands.command(name="carmyn", aliases=["carymn"], description="🌟 Display Carmyn's awesome profile!")
<<<<<<< HEAD
    async def carmyn_profile(self, ctx: commands.Context):
        """Display Carmyn's interactive profile with buttons!"""
        try:
            from src.discord_commander.views.carmyn_profile_view import CarmynProfileView
=======
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def carmyn_profile(self, ctx: commands.Context):
        """Display Carmyn's interactive profile with buttons!"""
        self.logger.info(f"Command 'carmyn_profile' triggered by {ctx.author}")
        try:
            from ..views.carmyn_profile_view import CarmynProfileView

>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
            view = CarmynProfileView()
            embed = view._create_main_embed()
            await ctx.send(embed=embed, view=view)
        except Exception as e:
            self.logger.error(f"Error in !carmyn command: {e}", exc_info=True)
            await ctx.send(f"❌ Oops! Something went wrong: {e}")

<<<<<<< HEAD

__all__ = ["ProfileCommands"]
=======
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
