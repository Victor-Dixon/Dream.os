#!/usr/bin/env python3
"""Profile commands for Discord bot."""

import logging

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class ProfileCommands(commands.Cog):
    """Commands for viewing agent profiles."""

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.logger = logging.getLogger(__name__)

    @commands.command(name="aria", description="✨ View Aria's interactive profile!")
    async def aria_profile(self, ctx: commands.Context) -> None:
        """Show a placeholder Aria profile embed."""
        embed = discord.Embed(title="Aria", description="Aria profile placeholder")
        await ctx.send(embed=embed)

    @commands.command(name="carmyn", aliases=["carymn"], description="🌟 Display Carmyn's profile!")
    async def carmyn_profile(self, ctx: commands.Context) -> None:
        """Show a placeholder Carmyn profile embed."""
        embed = discord.Embed(title="Carmyn", description="Carmyn profile placeholder")
        await ctx.send(embed=embed)


__all__ = ["ProfileCommands"]
