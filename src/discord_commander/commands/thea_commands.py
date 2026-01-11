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
        super().__init__()
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

            # Send message to Thea using correct API
            try:
                response_content = thea_service.send_prompt_and_get_response_text(
                    message)

                if response_content and len(response_content.strip()) > 0:
                    # Success response
                    embed.description = f"**Query:** {message}\n\n**Response:** {str(response_content)[:1900]}"
                    embed.color = discord.Color.green()
                    embed.set_footer(
                        text=f"Requested by {ctx.author.display_name} | Thea Manager")

                    if len(str(response_content)) > 1900:
                        embed.description += "..."
                else:
                    # Empty response
                    embed.description = f"**Query:** {message}\n\n**Response:** *No response from Thea Manager*"
                    embed.color = discord.Color.yellow()

            except Exception as service_error:
                # Error response
                embed.description = f"**Query:** {message}\n\n**Error:** {str(service_error)}"
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
                # Note: TheaBrowserService doesn't have check_authentication_status method
                # We'll assume it's authenticated if service is available
                auth_status = "✅ Service Available (authentication assumed)"
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
            self.logger.error(
                f"Error in thea-status command: {e}", exc_info=True)
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
            success = thea_service.ensure_thea_authenticated(
                allow_manual=False)

            if success:
                embed.description = "✅ Successfully authenticated with Thea Manager"
                embed.color = discord.Color.green()
            else:
                embed.description = "❌ Authentication failed. Manual authentication may be required."
                embed.color = discord.Color.red()

            embed.set_footer(text=f"Requested by {ctx.author.display_name}")
            await response_msg.edit(embed=embed)

        except Exception as e:
            self.logger.error(
                f"Error in thea-auth command: {e}", exc_info=True)
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
