#!/usr/bin/env python3
"""
Thea Commands - Discord Bot Integration
=======================================

Discord bot commands for Thea Manager integration.
Provides GUI-based interaction with Thea MMORPG functionality.

<!-- SSOT Domain: discord -->

V2 Compliance | Author: Agent-2 | Date: 2026-01-11
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

logger = logging.getLogger(__name__)


class TheaCommands(commands.Cog):
    """Discord commands for Thea Manager integration."""

    def __init__(self, bot: "UnifiedDiscordBot", gui_controller):
        """Initialize Thea commands."""
        commands.Cog.__init__(self)
        self.bot = bot
        self.gui_controller = gui_controller
        self.logger = logging.getLogger(__name__)

    @commands.command(name="thea", description="Send a message to Thea Manager")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def thea(self, ctx: commands.Context, *, message: str):
        """Send a message to Thea Manager and display the response."""
        self.logger.info(f"Command 'thea' triggered by {ctx.author}")

        try:
            embed = discord.Embed(
                title="🤖 Thea Manager Query",
                description=f"**Query:** {message}\n\n*Processing...*",
                color=discord.Color.blue(),
                timestamp=discord.utils.utcnow(),
            )
            embed.set_footer(text=f"Requested by {ctx.author.display_name}")

            # Send initial response
            response_msg = await ctx.send(embed=embed)

            # Get Thea service
            thea_service = self.bot._get_thea_service(headless=True)

            # Send message to Thea
            result = thea_service.send_message(message)

            if result and result.success and result.response:
                # Success response
                embed.description = f"**Query:** {message}\n\n**Response:** {result.response.content[:1900]}"
                embed.color = discord.Color.green()
                embed.set_footer(text=f"Requested by {ctx.author.display_name} | Thea Manager")

                if len(result.response.content) > 1900:
                    embed.description += "..."
            else:
                # Error response
                error_msg = result.error_message if result else "Unknown error"
                embed.description = f"**Query:** {message}\n\n**Error:** {error_msg}"
                embed.color = discord.Color.red()

            await response_msg.edit(embed=embed)

        except Exception as e:
            self.logger.error(f"Error in thea command: {e}", exc_info=True)
            embed = discord.Embed(
                title="❌ Thea Manager Error",
                description=f"Failed to process Thea query: {str(e)}",
                color=discord.Color.red(),
                timestamp=discord.utils.utcnow(),
            )
            await ctx.send(embed=embed)

    @commands.command(name="thea-status", description="Check Thea Manager status")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def thea_status(self, ctx: commands.Context):
        """Check the current status of Thea Manager integration."""
        self.logger.info(f"Command 'thea-status' triggered by {ctx.author}")

        try:
            embed = discord.Embed(
                title="📊 Thea Manager Status",
                color=discord.Color.blue(),
                timestamp=discord.utils.utcnow(),
            )

            # Check if Thea service is available
            try:
                thea_service = self.bot._get_thea_service(headless=True)
                embed.add_field(
                    name="🔗 Service Status",
                    value="✅ Thea service initialized",
                    inline=False
                )

                # Try to check authentication status
                is_authenticated = thea_service.check_authentication_status()
                auth_status = "✅ Authenticated" if is_authenticated else "❌ Not authenticated"
                embed.add_field(
                    name="🔐 Authentication",
                    value=auth_status,
                    inline=False
                )

            except Exception as e:
                embed.add_field(
                    name="❌ Service Status",
                    value=f"Error: {str(e)}",
                    inline=False
                )
                embed.color = discord.Color.red()

            embed.set_footer(text=f"Requested by {ctx.author.display_name}")
            await ctx.send(embed=embed)

        except Exception as e:
            self.logger.error(f"Error in thea-status command: {e}", exc_info=True)
            embed = discord.Embed(
                title="❌ Thea Status Error",
                description=f"Failed to check Thea status: {str(e)}",
                color=discord.Color.red(),
                timestamp=discord.utils.utcnow(),
            )
            await ctx.send(embed=embed)

    @commands.command(name="thea-auth", description="Authenticate with Thea Manager")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def thea_auth(self, ctx: commands.Context):
        """Authenticate with Thea Manager."""
        self.logger.info(f"Command 'thea-auth' triggered by {ctx.author}")

        try:
            embed = discord.Embed(
                title="🔐 Thea Manager Authentication",
                description="*Authenticating with Thea Manager...*",
                color=discord.Color.blue(),
                timestamp=discord.utils.utcnow(),
            )

            response_msg = await ctx.send(embed=embed)

            # Get Thea service and attempt authentication
            thea_service = self.bot._get_thea_service(headless=True)
            success = thea_service.ensure_thea_authenticated(allow_manual=False)

            if success:
                embed.description = "✅ Successfully authenticated with Thea Manager"
                embed.color = discord.Color.green()
            else:
                embed.description = "❌ Authentication failed. Manual authentication may be required."
                embed.color = discord.Color.red()

            embed.set_footer(text=f"Requested by {ctx.author.display_name}")
            await response_msg.edit(embed=embed)

        except Exception as e:
            self.logger.error(f"Error in thea-auth command: {e}", exc_info=True)
            embed = discord.Embed(
                title="❌ Thea Authentication Error",
                description=f"Failed to authenticate: {str(e)}",
                color=discord.Color.red(),
                timestamp=discord.utils.utcnow(),
            )
            await ctx.send(embed=embed)


async def setup(bot):
    """Setup function for Discord cog loading."""
    await bot.add_cog(TheaCommands(bot, bot.gui_controller))