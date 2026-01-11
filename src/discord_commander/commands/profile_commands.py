#!/usr/bin/env python3
"""
Profile Commands - Modular V2 Compliance
========================================

Profile display commands (Aria, Carmyn) extracted from bot_messaging_commands.py.

<!-- SSOT Domain: messaging -->

V2 Compliant: Modular profile commands
Author: Agent-7 (Web Development Specialist)
Date: 2026-01-08
"""

import logging

try:
    import discord
    from discord.ext import commands
except ImportError:
    discord = None
    commands = None

logger = logging.getLogger(__name__)


class ProfileCommands(commands.Cog):
    """Profile display commands for team members."""

    def __init__(self, bot):
        """Initialize profile commands."""
        super().__init__()
        self.bot = bot
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
            from src.discord_commander.views.carmyn_profile_view import CarmynProfileView
            view = CarmynProfileView()
            embed = view._create_main_embed()
            await ctx.send(embed=embed, view=view)
        except Exception as e:
            self.logger.error(f"Error in !carmyn command: {e}", exc_info=True)
            await ctx.send(f"❌ Oops! Something went wrong: {e}")


__all__ = ["ProfileCommands"]