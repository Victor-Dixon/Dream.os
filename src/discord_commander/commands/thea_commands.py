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

from .command_base import DiscordCommandMixin, RoleDecorators

if TYPE_CHECKING:
    from src.discord_commander.unified_discord_bot import UnifiedDiscordBot

try:
    import discord
    from discord.ext import commands
except ImportError:
    discord = None
    commands = None

logger = logging.getLogger(__name__)


class TheaCommands(commands.Cog, DiscordCommandMixin):
    """Discord commands for Thea Manager integration."""

    def __init__(self, bot: "UnifiedDiscordBot", gui_controller):
        """Initialize Thea commands."""
        commands.Cog.__init__(self)
        DiscordCommandMixin.__init__(self)
        self.bot = bot
        self.gui_controller = gui_controller

    @commands.command(name="thea", description="Send a message to Thea Manager")
    @RoleDecorators.admin_only()
    async def thea(self, ctx: commands.Context, *, message: str):
        """Send a message to Thea Manager and display the response."""
        self.log_command_trigger(ctx, "thea")

        try:
            embed = self.create_base_embed(
                "🤖 Thea Manager Query",
                f"**Query:** {message}\n\n*Processing...*"
            )
            self.add_user_footer(embed, ctx)

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
            await self.handle_command_error(ctx, e, "thea")

    @commands.command(name="thea-status", description="Check Thea Manager status")
    @RoleDecorators.admin_only()
    async def thea_status(self, ctx: commands.Context):
        """Check the current status of Thea Manager integration."""
        self.log_command_trigger(ctx, "thea-status")

        try:
            embed = self.create_base_embed("📊 Thea Manager Status")

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

            self.add_user_footer(embed, ctx)
            await ctx.send(embed=embed)

        except Exception as e:
            await self.handle_command_error(ctx, e, "thea-status")

    @commands.command(name="thea-auth", description="Authenticate with Thea Manager")
    @RoleDecorators.admin_only()
    async def thea_auth(self, ctx: commands.Context):
        """Authenticate with Thea Manager."""
        self.log_command_trigger(ctx, "thea-auth")

        try:
            embed = self.create_base_embed(
                "🔐 Thea Manager Authentication",
                "*Authenticating with Thea Manager...*"
            )
            self.add_user_footer(embed, ctx)

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

            self.add_user_footer(embed, ctx)
            await response_msg.edit(embed=embed)

        except Exception as e:
            await self.handle_command_error(ctx, e, "thea-auth")


async def setup(bot):
    """Setup function for Discord cog loading."""
    await bot.add_cog(TheaCommands(bot, bot.gui_controller))
