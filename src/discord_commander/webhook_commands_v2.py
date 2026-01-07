"""
Webhook Commands V2 - Agent Cellphone V2
=======================================

SSOT Domain: discord

Refactored Discord webhook management commands using service architecture.

Features:
- Webhook creation, deletion, and testing
- Webhook information and listing
- Interactive confirmation dialogs
- Error handling and validation

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

import logging
from typing import Optional

try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    from .test_utils import get_mock_discord
    mock_discord, mock_commands = get_mock_discord()
    discord = mock_discord
    commands = mock_commands

from .webhook_service import webhook_service

logger = logging.getLogger(__name__)

class WebhookCommands(commands.Cog if DISCORD_AVAILABLE else object):
    """
    Discord commands for webhook management.
    """

    def __init__(self, bot):
        self.bot = bot
        self.webhook_service = webhook_service

    @commands.command(name="create_webhook", aliases=["webhook_create", "make_webhook"])
    @commands.has_permissions(administrator=True)
    async def create_webhook_command(
        self,
        ctx: commands.Context,
        channel: Optional[discord.TextChannel] = None,
        webhook_name: str = "Agent Webhook",
        *,
        reason: str = "Created by agent automation"
    ):
        """
        Create a webhook for a channel.

        Usage:
        !create_webhook #channel-name "Webhook Name"
        !create_webhook 1234567890 "Custom Webhook" reason: For agent notifications

        Examples:
        !create_webhook #general "Agent Updates"
        !webhook_create #logs "System Logs" reason: Monitoring system events
        """
        try:
            # Determine target channel
            if channel is None:
                channel = ctx.channel

            # Validate permissions
            if not channel.permissions_for(ctx.guild.me).manage_webhooks:
                embed = discord.Embed(
                    title="❌ Permission Denied",
                    description="I need 'Manage Webhooks' permission to create webhooks.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return

            # Create webhook using service
            webhook = await self.webhook_service.create_webhook(
                channel=channel,
                name=webhook_name,
                reason=reason
            )

            if webhook:
                embed = discord.Embed(
                    title="✅ Webhook Created",
                    description=f"Successfully created webhook in {channel.mention}",
                    color=discord.Color.green()
                )
                embed.add_field(name="Name", value=webhook.name, inline=True)
                embed.add_field(name="ID", value=str(webhook.id), inline=True)
                embed.add_field(name="Channel", value=channel.name, inline=True)

                # Show URL privately
                url_embed = discord.Embed(
                    title="🔒 Webhook URL (Private)",
                    description="Keep this URL secure!",
                    color=discord.Color.orange()
                )
                url_embed.add_field(name="URL", value=f"||{webhook.url}||", inline=False)

                await ctx.send(embed=embed)
                try:
                    await ctx.author.send(embed=url_embed)
                except discord.Forbidden:
                    await ctx.send("⚠️ Could not DM you the webhook URL. Please enable DMs from server members.")

        except Exception as e:
            logger.error(f"Error creating webhook: {e}")
            embed = discord.Embed(
                title="❌ Creation Failed",
                description=f"Failed to create webhook: {str(e)}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @commands.command(name="list_webhooks", aliases=["webhooks", "show_webhooks"])
    @commands.has_permissions(administrator=True)
    async def list_webhooks_command(self, ctx: commands.Context):
        """
        List all webhooks in the current channel or server.

        Usage: !list_webhooks

        Shows webhook ID, name, and creation info for easy management.
        """
        try:
            # Get webhooks for current channel
            channel_webhooks = await self.webhook_service.list_channel_webhooks(ctx.channel)

            if not channel_webhooks:
                embed = discord.Embed(
                    title="📋 No Webhooks Found",
                    description=f"No webhooks found in {ctx.channel.mention}",
                    color=discord.Color.blue()
                )
                embed.add_field(
                    name="Create One",
                    value="Use `!create_webhook` to create a webhook",
                    inline=False
                )
                await ctx.send(embed=embed)
                return

            embed = discord.Embed(
                title=f"📋 Webhooks in #{ctx.channel.name}",
                description=f"Found {len(channel_webhooks)} webhook(s)",
                color=discord.Color.blue()
            )

            for webhook in channel_webhooks[:10]:  # Limit to 10
                created = webhook.get('created_at', 'Unknown')
                user = webhook.get('user', 'Unknown')
                embed.add_field(
                    name=f"🔗 {webhook['name']}",
                    value=f"ID: `{webhook['id']}`\nCreated: {created[:10] if created != 'Unknown' else 'Unknown'}\nBy: {user}",
                    inline=False
                )

            if len(channel_webhooks) > 10:
                embed.set_footer(text=f"Showing 10 of {len(channel_webhooks)} webhooks")

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error listing webhooks: {e}")
            await ctx.send(f"❌ Error listing webhooks: {e}")

    @commands.command(name="delete_webhook", aliases=["webhook_delete", "remove_webhook"])
    @commands.has_permissions(administrator=True)
    async def delete_webhook_command(self, ctx: commands.Context, webhook_id: str):
        """
        Delete a webhook by ID.

        Usage: !delete_webhook <webhook_id>

        Example: !delete_webhook 1234567890123456789
        """
        try:
            # Show confirmation dialog
            embed = discord.Embed(
                title="⚠️ Confirm Deletion",
                description=f"Are you sure you want to delete webhook `{webhook_id}`?",
                color=discord.Color.orange()
            )
            embed.add_field(
                name="⚠️ Warning",
                value="This action cannot be undone!",
                inline=False
            )

            view = WebhookDeletionView(webhook_id, self.webhook_service)
            await ctx.send(embed=embed, view=view)

        except Exception as e:
            logger.error(f"Error initiating webhook deletion: {e}")
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="test_webhook", aliases=["webhook_test", "ping_webhook"])
    @commands.has_permissions(administrator=True)
    async def test_webhook_command(self, ctx: commands.Context, webhook_id: str):
        """
        Test a webhook by sending a test message.

        Usage: !test_webhook <webhook_id>

        Example: !test_webhook 1234567890123456789
        """
        try:
            # Test the webhook
            success = await self.webhook_service.test_webhook(
                webhook_id=webhook_id,
                test_message=f"🧪 Webhook test from {ctx.author.display_name}"
            )

            if success:
                embed = discord.Embed(
                    title="✅ Webhook Test Successful",
                    description=f"Webhook `{webhook_id}` is working correctly!",
                    color=discord.Color.green()
                )
                embed.add_field(
                    name="Test Message",
                    value="Check if a test message appeared in the configured channel",
                    inline=False
                )
            else:
                embed = discord.Embed(
                    title="❌ Webhook Test Failed",
                    description=f"Webhook `{webhook_id}` failed to send test message",
                    color=discord.Color.red()
                )

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error testing webhook: {e}")
            await ctx.send(f"❌ Error testing webhook: {e}")

    @commands.command(name="webhook_info", aliases=["webhook_details", "info_webhook"])
    @commands.has_permissions(administrator=True)
    async def webhook_info_command(self, ctx: commands.Context, webhook_id: str):
        """
        Get detailed information about a webhook.

        Usage: !webhook_info <webhook_id>

        Shows webhook details, creation info, and status.
        """
        try:
            info = await self.webhook_service.get_webhook_info(webhook_id)

            if not info:
                embed = discord.Embed(
                    title="❌ Webhook Not Found",
                    description=f"Could not find webhook `{webhook_id}`",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return

            embed = discord.Embed(
                title=f"ℹ️ Webhook Information",
                description=f"Details for webhook `{webhook_id}`",
                color=discord.Color.blue()
            )

            embed.add_field(name="Name", value=info.get("name", "Unknown"), inline=True)
            embed.add_field(name="ID", value=info.get("id", "Unknown"), inline=True)
            embed.add_field(name="Status", value=info.get("status", "Unknown"), inline=True)

            channel = info.get("channel", "Unknown")
            guild = info.get("guild", "Unknown")
            embed.add_field(name="Channel", value=channel, inline=True)
            embed.add_field(name="Server", value=guild, inline=True)

            created = info.get("created_at", "Unknown")
            if created and created != "Unknown":
                embed.add_field(name="Created", value=created[:19], inline=True)

            user = info.get("user", "Unknown")
            embed.add_field(name="Created By", value=user, inline=False)

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error getting webhook info: {e}")
            await ctx.send(f"❌ Error getting webhook info: {e}")

class WebhookDeletionView(discord.ui.View if DISCORD_AVAILABLE else object):
    """Interactive view for webhook deletion confirmation."""

    def __init__(self, webhook_id: str, webhook_service):
        super().__init__(timeout=60)
        self.webhook_id = webhook_id
        self.webhook_service = webhook_service

    @discord.ui.button(label="Confirm Delete", style=discord.ButtonStyle.danger, emoji="🗑️")
    async def confirm_delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Confirm webhook deletion."""
        try:
            success = await self.webhook_service.delete_webhook(
                webhook_id=self.webhook_id,
                reason=f"Deleted by {interaction.user.display_name}"
            )

            if success:
                embed = discord.Embed(
                    title="✅ Webhook Deleted",
                    description=f"Successfully deleted webhook `{self.webhook_id}`",
                    color=discord.Color.green()
                )
            else:
                embed = discord.Embed(
                    title="❌ Deletion Failed",
                    description=f"Failed to delete webhook `{self.webhook_id}`",
                    color=discord.Color.red()
                )

            await interaction.response.edit_message(embed=embed, view=None)

        except Exception as e:
            logger.error(f"Error deleting webhook: {e}")
            embed = discord.Embed(
                title="❌ Error",
                description=f"Error deleting webhook: {str(e)}",
                color=discord.Color.red()
            )
            await interaction.response.edit_message(embed=embed, view=None)

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary, emoji="❌")
    async def cancel_delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Cancel webhook deletion."""
        embed = discord.Embed(
            title="❌ Deletion Cancelled",
            description="Webhook deletion has been cancelled.",
            color=discord.Color.blue()
        )
        await interaction.response.edit_message(embed=embed, view=None)

async def setup(bot):
    """Setup function for Discord cog."""
    await bot.add_cog(WebhookCommands(bot))