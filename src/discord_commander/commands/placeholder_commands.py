"""Placeholder commands for Discord bot."""

import logging

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class PlaceholderCommands(commands.Cog):
    """Misc placeholder commands."""

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.logger = logging.getLogger(__name__)

    @commands.command(name="sftp", aliases=["sftp_creds", "ftp"], description="Get SFTP credentials guide")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def sftp(self, ctx: commands.Context) -> None:
        """Get SFTP credentials - streamlined guide."""
        embed = discord.Embed(
            title="🔑 How to Get SFTP Credentials (30 seconds)",
            description="Quick guide to get your SFTP credentials from Hostinger",
            color=discord.Color.green(),
        )
        embed.add_field(
            name="Step 1: Log into Hostinger",
            value="👉 https://hpanel.hostinger.com/",
            inline=False,
        )
        await ctx.send(embed=embed)


__all__ = ["PlaceholderCommands"]
