"""
Profile Commands
================

Profile commands extracted from unified_discord_bot.py for V2 compliance.
Handles: Agent profile displays (Aria, Carmyn).

V2 Compliance: <300 lines, <5 classes, <10 functions
"""

import logging

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class ProfileCommands(commands.Cog):
    """Profile commands for displaying agent profiles."""

    def __init__(self, bot, gui_controller):
        """Initialize profile commands."""
        self.bot = bot
        self.gui_controller = gui_controller
        self.logger = logging.getLogger(__name__)

    @commands.command(name="aria", description="✨ View Aria's interactive profile!")
    async def aria_profile(self, ctx: commands.Context):
        """Display Aria's interactive profile with buttons!"""
        try:
            from src.discord_commander.views.aria_profile_view import AriaProfileView

            view = AriaProfileView()
            embed = view._create_main_embed()
            await ctx.send(embed=embed, view=view)
        except Exception as e:
            self.logger.error(f"Error in !aria command: {e}", exc_info=True)
            await ctx.send(f"❌ Oops! Something went wrong: {e}")

    @commands.command(name="carmyn", aliases=["carymn"], description="🌟 Display Carmyn's awesome profile!")
    async def carmyn_profile(self, ctx: commands.Context):
        """Display Carmyn's interactive profile with buttons!"""
        try:
            from ..views.carmyn_profile_view import CarmynProfileView

            view = CarmynProfileView()
            embed = view._create_main_embed()
            await ctx.send(embed=embed, view=view)
        except Exception as e:
            self.logger.error(f"Error in !carmyn command: {e}", exc_info=True)
            await ctx.send(f"❌ Oops! Something went wrong: {e}")

