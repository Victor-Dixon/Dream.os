#!/usr/bin/env python3
"""
<<<<<<< HEAD
Webhook Commands - Agent Cellphone V2
=====================================

SSOT Domain: discord

Refactored entry point for Discord webhook management commands.
All core logic has been extracted into service architecture for V2 compliance.

Features:
- Webhook creation, deletion, testing, and information
- Interactive confirmation dialogs
- Configuration persistence
- Error handling and validation (webhook_commands_v2.py)

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""


# === V2 FEATURES MERGED ===

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
=======
<!-- SSOT Domain: discord -->

Discord Webhook Management Commands
===================================

Bot commands for creating and managing Discord webhooks programmatically.
Enables agents to fully control Discord server webhook infrastructure.

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import json
import logging
from pathlib import Path

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class WebhookCommands(commands.Cog):
    """Discord bot commands for webhook management."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config_dir = Path("config")
        self.config_dir.mkdir(exist_ok=True)

    @commands.command(name="create_webhook")
    @commands.has_permissions(administrator=True)
    async def create_webhook(
        self,
        ctx: commands.Context,
        channel: discord.TextChannel,
        webhook_name: str = "Agent Webhook",
        *,
        reason: str = "Created by agent automation",
    ):
        """
        Create a webhook for a specific channel.

        Usage:
            !create_webhook #channel-name Webhook-Name
            !create_webhook 1234567890 Custom-Webhook

        Examples:
            !create_webhook #devlogs Agent-8-Devlog-Webhook
            !create_webhook #status Status-Update-Webhook
        """
        try:
            # Create webhook
            webhook = await channel.create_webhook(name=webhook_name, reason=reason)

            # Save to config
            config_file = self.config_dir / "discord_webhooks.json"
            webhooks_config = {}

            if config_file.exists():
                with open(config_file) as f:
                    webhooks_config = json.load(f)

            # Add new webhook
            webhook_key = f"{channel.name}_webhook"
            webhooks_config[webhook_key] = {
                "webhook_url": webhook.url,
                "webhook_id": str(webhook.id),
                "channel_id": str(channel.id),
                "channel_name": channel.name,
                "webhook_name": webhook_name,
                "created_by": str(ctx.author),
                "created_at": discord.utils.utcnow().isoformat(),
            }

            # Save config
            with open(config_file, "w") as f:
                json.dump(webhooks_config, f, indent=2)

            # Create success embed
            embed = discord.Embed(
                title="✅ Webhook Created Successfully!",
                description=f"Created webhook for {channel.mention}",
                color=discord.Color.green(),
            )

            embed.add_field(name="Webhook Name", value=webhook_name, inline=True)
            embed.add_field(name="Channel", value=channel.mention, inline=True)
            embed.add_field(name="Webhook ID", value=str(webhook.id), inline=False)
            embed.add_field(
                name="⚠️ Webhook URL",
                value="Saved to config/discord_webhooks.json (DO NOT share publicly!)",
                inline=False,
            )
            embed.add_field(name="Usage", value=f"Use config key: `{webhook_key}`", inline=False)

            await ctx.send(embed=embed)

            # Send webhook URL in DM for security
            try:
                dm_embed = discord.Embed(
                    title="🔐 Webhook URL (Private)",
                    description=f"Webhook URL for {channel.name}",
                    color=discord.Color.blue(),
                )
                dm_embed.add_field(name="URL", value=webhook.url, inline=False)
                dm_embed.add_field(
                    name="Security",
                    value="⚠️ Keep this URL private! Anyone with this URL can post to your channel.",
                    inline=False,
                )
                await ctx.author.send(embed=dm_embed)
            except discord.Forbidden:
                await ctx.send("⚠️ Couldn't DM you the webhook URL. Check config file.")

            logger.info(f"Created webhook '{webhook_name}' for {channel.name}")

        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to create webhooks in that channel!")
        except Exception as e:
            logger.error(f"Failed to create webhook: {e}")
            await ctx.send(f"❌ Failed to create webhook: {str(e)}")

    @commands.command(name="list_webhooks")
    @commands.has_permissions(administrator=True)
    async def list_webhooks(
        self, ctx: commands.Context, channel: discord.TextChannel | None = None
    ):
        """
        List all webhooks in the server or specific channel.

        Usage:
            !list_webhooks              # List all server webhooks
            !list_webhooks #channel     # List webhooks for specific channel
        """
        try:
            if channel:
                # List webhooks for specific channel
                webhooks = await channel.webhooks()
                title = f"Webhooks in #{channel.name}"
            else:
                # List all server webhooks
                webhooks = await ctx.guild.webhooks()
                title = f"All Webhooks in {ctx.guild.name}"

            if not webhooks:
                await ctx.send("No webhooks found.")
                return

            embed = discord.Embed(
                title=title,
                description=f"Found {len(webhooks)} webhook(s)",
                color=discord.Color.blue(),
            )

            for webhook in webhooks[:25]:  # Discord embed limit
                channel_info = f"<#{webhook.channel_id}>" if webhook.channel_id else "Unknown"
                creator = webhook.user.mention if webhook.user else "Unknown"

                embed.add_field(
                    name=f"📌 {webhook.name}",
                    value=f"**Channel:** {channel_info}\n"
                    f"**Created by:** {creator}\n"
                    f"**ID:** `{webhook.id}`",
                    inline=False,
                )

            if len(webhooks) > 25:
                embed.set_footer(text=f"Showing first 25 of {len(webhooks)} webhooks")

            await ctx.send(embed=embed)

        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to view webhooks!")
        except Exception as e:
            logger.error(f"Failed to list webhooks: {e}")
            await ctx.send(f"❌ Failed to list webhooks: {str(e)}")

    @commands.command(name="delete_webhook")
    @commands.has_permissions(administrator=True)
    async def delete_webhook(self, ctx: commands.Context, webhook_id: str):
        """
        Delete a webhook by ID.

        Usage:
            !delete_webhook <webhook_id>

        Example:
            !delete_webhook 1234567890123456789
        """
        try:
            # Get webhook
            webhook = await self.bot.fetch_webhook(int(webhook_id))

            # Confirm deletion
            confirm_embed = discord.Embed(
                title="⚠️ Confirm Webhook Deletion",
                description="Are you sure you want to delete this webhook?",
                color=discord.Color.orange(),
            )
            confirm_embed.add_field(name="Webhook Name", value=webhook.name, inline=True)
            confirm_embed.add_field(name="Channel", value=f"<#{webhook.channel_id}>", inline=True)

            # Add confirmation buttons
            view = WebhookDeleteConfirmView(webhook, ctx.author)
            message = await ctx.send(embed=confirm_embed, view=view)

            # Wait for confirmation
            await view.wait()

            if view.confirmed:
                await webhook.delete(reason=f"Deleted by {ctx.author}")

                # Update config
                self._remove_from_config(webhook_id)

                success_embed = discord.Embed(
                    title="✅ Webhook Deleted",
                    description=f"Successfully deleted webhook '{webhook.name}'",
                    color=discord.Color.green(),
                )
                await message.edit(embed=success_embed, view=None)
                logger.info(f"Deleted webhook '{webhook.name}' (ID: {webhook_id})")
            else:
                await message.edit(content="❌ Webhook deletion cancelled.", embed=None, view=None)

        except discord.NotFound:
            await ctx.send(f"❌ Webhook with ID `{webhook_id}` not found!")
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to delete that webhook!")
        except ValueError:
            await ctx.send(f"❌ Invalid webhook ID: `{webhook_id}`")
        except Exception as e:
            logger.error(f"Failed to delete webhook: {e}")
            await ctx.send(f"❌ Failed to delete webhook: {str(e)}")

    @commands.command(name="test_webhook")
    @commands.has_permissions(administrator=True)
    async def test_webhook(self, ctx: commands.Context, webhook_id: str):
        """
        Test a webhook by sending a test message.

        Usage:
            !test_webhook <webhook_id>
        """
        try:
            webhook = await self.bot.fetch_webhook(int(webhook_id))

            # Send test message
            await webhook.send(
                content="✅ **Webhook Test Successful!**\n"
                f"This webhook is working correctly.\n"
                f"Tested by: {ctx.author.mention}",
                username="Webhook Test Bot",
            )

            embed = discord.Embed(
                title="✅ Webhook Test Sent",
                description=f"Test message sent to webhook '{webhook.name}'",
                color=discord.Color.green(),
            )
            embed.add_field(name="Channel", value=f"<#{webhook.channel_id}>", inline=True)

            await ctx.send(embed=embed)

        except discord.NotFound:
            await ctx.send(f"❌ Webhook with ID `{webhook_id}` not found!")
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to use that webhook!")
        except ValueError:
            await ctx.send(f"❌ Invalid webhook ID: `{webhook_id}`")
        except Exception as e:
            logger.error(f"Failed to test webhook: {e}")
            await ctx.send(f"❌ Failed to test webhook: {str(e)}")

    @commands.command(name="webhook_info")
    @commands.has_permissions(administrator=True)
    async def webhook_info(self, ctx: commands.Context, webhook_id: str):
        """
        Get detailed information about a webhook.

        Usage:
            !webhook_info <webhook_id>
        """
        try:
            webhook = await self.bot.fetch_webhook(int(webhook_id))

            embed = discord.Embed(
                title="📋 Webhook Information",
                description=f"Details for webhook '{webhook.name}'",
                color=discord.Color.blue(),
            )

            embed.add_field(name="Name", value=webhook.name, inline=True)
            embed.add_field(name="ID", value=str(webhook.id), inline=True)
            embed.add_field(name="Channel", value=f"<#{webhook.channel_id}>", inline=True)

            if webhook.user:
                embed.add_field(name="Created By", value=webhook.user.mention, inline=True)

            if webhook.avatar:
                embed.set_thumbnail(url=webhook.avatar.url)

            # Send webhook URL in DM
            try:
                dm_embed = discord.Embed(
                    title="🔐 Webhook URL (Private)",
                    description=f"URL for webhook '{webhook.name}'",
                    color=discord.Color.blue(),
                )
                dm_embed.add_field(name="URL", value=webhook.url, inline=False)
                await ctx.author.send(embed=dm_embed)

                embed.add_field(
                    name="Webhook URL", value="Sent to your DMs (keep it private!)", inline=False
                )
            except discord.Forbidden:
                embed.add_field(
                    name="Webhook URL", value="Enable DMs to receive the webhook URL", inline=False
                )

            await ctx.send(embed=embed)

        except discord.NotFound:
            await ctx.send(f"❌ Webhook with ID `{webhook_id}` not found!")
        except ValueError:
            await ctx.send(f"❌ Invalid webhook ID: `{webhook_id}`")
        except Exception as e:
            logger.error(f"Failed to get webhook info: {e}")
            await ctx.send(f"❌ Failed to get webhook info: {str(e)}")

    def _remove_from_config(self, webhook_id: str):
        """Remove webhook from config file."""
        config_file = self.config_dir / "discord_webhooks.json"

        if not config_file.exists():
            return

        try:
            with open(config_file) as f:
                config = json.load(f)

            # Find and remove webhook
            for key, value in list(config.items()):
                if isinstance(value, dict) and value.get("webhook_id") == webhook_id:
                    del config[key]

            # Save updated config
            with open(config_file, "w") as f:
                json.dump(config, f, indent=2)

        except Exception as e:
            logger.error(f"Failed to update config: {e}")


class WebhookDeleteConfirmView(discord.ui.View):
    """Confirmation view for webhook deletion."""

    def __init__(self, webhook: discord.Webhook, user: discord.User):
        from src.core.config.timeout_constants import TimeoutConstants
        super().__init__(timeout=TimeoutConstants.HTTP_DEFAULT)
        self.webhook = webhook
        self.user = user
        self.confirmed = False

    @discord.ui.button(label="✅ Confirm Delete", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Confirm deletion."""
        try:
            if interaction.user.id != self.user.id:
                await interaction.response.send_message(
                    "❌ Only the command issuer can confirm this action.", ephemeral=True
                )
                return

            self.confirmed = True
            await interaction.response.send_message("✅ Confirmed", ephemeral=True)
            self.stop()
        except Exception as e:
            logger.error(f"Error in webhook delete confirm: {e}", exc_info=True)
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"❌ Error: {e}", ephemeral=True
                )

    @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Cancel deletion."""
        try:
            if interaction.user.id != self.user.id:
                await interaction.response.send_message(
                    "❌ Only the command issuer can cancel this action.", ephemeral=True
                )
                return

            self.confirmed = False
            await interaction.response.send_message("❌ Cancelled", ephemeral=True)
            self.stop()
        except Exception as e:
            logger.error(f"Error in webhook delete cancel: {e}", exc_info=True)
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"❌ Error: {e}", ephemeral=True
                )


async def setup(bot: commands.Bot):
    """Setup function for loading as extension."""
    await bot.add_cog(WebhookCommands(bot))
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
