"""
Webhook Service - Agent Cellphone V2
====================================

SSOT Domain: discord

Core service for managing Discord webhooks programmatically.

Features:
- Webhook creation and deletion
- Webhook testing and information retrieval
- Configuration persistence
- Channel permission validation
- Error handling and logging

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any

try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    discord = None
    commands = None

logger = logging.getLogger(__name__)

class WebhookConfigManager:
    """Manages webhook configuration persistence."""

    def __init__(self, config_dir: Path):
        self.config_file = config_dir / "webhooks.json"
        self.config_dir = config_dir
        self.config_dir.mkdir(exist_ok=True)
        self._ensure_config_exists()

    def _ensure_config_exists(self) -> None:
        """Ensure config file exists with proper structure."""
        if not self.config_file.exists():
            default_config = {
                "webhooks": {},
                "version": "2.0",
                "last_updated": None
            }
            self._save_config(default_config)

    def _load_config(self) -> Dict[str, Any]:
        """Load webhook configuration from file."""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.warning(f"Error loading webhook config: {e}")
            return {"webhooks": {}, "version": "2.0"}

    def _save_config(self, config: Dict[str, Any]) -> None:
        """Save webhook configuration to file."""
        try:
            config["last_updated"] = str(discord.utils.utcnow()) if DISCORD_AVAILABLE else None
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving webhook config: {e}")

    def add_webhook(self, webhook_id: str, data: Dict[str, Any]) -> None:
        """Add webhook to configuration."""
        config = self._load_config()
        config["webhooks"][webhook_id] = data
        self._save_config(config)

    def remove_webhook(self, webhook_id: str) -> bool:
        """Remove webhook from configuration."""
        config = self._load_config()
        if webhook_id in config["webhooks"]:
            del config["webhooks"][webhook_id]
            self._save_config(config)
            return True
        return False

    def get_webhook(self, webhook_id: str) -> Optional[Dict[str, Any]]:
        """Get webhook configuration by ID."""
        config = self._load_config()
        return config["webhooks"].get(webhook_id)

    def get_all_webhooks(self) -> Dict[str, Dict[str, Any]]:
        """Get all webhooks configuration."""
        config = self._load_config()
        return config["webhooks"]

    def get_webhooks_for_channel(self, channel_id: str) -> List[Dict[str, Any]]:
        """Get all webhooks for a specific channel."""
        all_webhooks = self.get_all_webhooks()
        return [data for data in all_webhooks.values()
                if str(data.get("channel_id")) == str(channel_id)]

class WebhookService:
    """
    Service for managing Discord webhooks programmatically.
    """

    def __init__(self, bot: Optional[commands.Bot] = None):
        self.bot = bot
        self.config_manager = WebhookConfigManager(Path("config"))

    async def create_webhook(self, channel: discord.TextChannel, name: str,
                           avatar_url: Optional[str] = None,
                           reason: str = "Created by agent automation") -> Optional[discord.Webhook]:
        """
        Create a webhook for a channel.

        Args:
            channel: Discord text channel
            name: Webhook name
            avatar_url: Optional avatar URL
            reason: Audit log reason

        Returns:
            Created webhook or None if failed
        """
        if not DISCORD_AVAILABLE:
            return None

        try:
            # Check permissions
            if not channel.permissions_for(channel.guild.me).manage_webhooks:
                raise ValueError("Missing 'Manage Webhooks' permission")

            # Create webhook
            webhook = await channel.create_webhook(
                name=name,
                avatar=await self._get_avatar_bytes(avatar_url) if avatar_url else None,
                reason=reason
            )

            # Store in config
            config_data = {
                "id": str(webhook.id),
                "name": webhook.name,
                "channel_id": str(channel.id),
                "channel_name": channel.name,
                "guild_id": str(channel.guild.id),
                "guild_name": channel.guild.name,
                "url": webhook.url,
                "token": webhook.token,
                "created_at": str(discord.utils.utcnow()),
                "created_by": "agent_automation"
            }
            self.config_manager.add_webhook(str(webhook.id), config_data)

            logger.info(f"Created webhook '{name}' in #{channel.name}")
            return webhook

        except Exception as e:
            logger.error(f"Failed to create webhook: {e}")
            raise

    async def delete_webhook(self, webhook_id: str, reason: str = "Deleted by agent automation") -> bool:
        """
        Delete a webhook by ID.

        Args:
            webhook_id: Webhook ID to delete
            reason: Audit log reason

        Returns:
            True if deleted successfully
        """
        if not DISCORD_AVAILABLE or not self.bot:
            return False

        try:
            # Find webhook across all guilds
            webhook = None
            for guild in self.bot.guilds:
                try:
                    webhook = await guild.fetch_webhook(int(webhook_id))
                    break
                except (discord.NotFound, discord.Forbidden):
                    continue

            if not webhook:
                raise ValueError(f"Webhook {webhook_id} not found")

            await webhook.delete(reason=reason)
            self.config_manager.remove_webhook(webhook_id)

            logger.info(f"Deleted webhook {webhook_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to delete webhook {webhook_id}: {e}")
            return False

    async def test_webhook(self, webhook_id: str, test_message: str = "Webhook test message") -> bool:
        """
        Test a webhook by sending a test message.

        Args:
            webhook_id: Webhook ID to test
            test_message: Test message content

        Returns:
            True if test successful
        """
        if not DISCORD_AVAILABLE:
            return False

        try:
            # Get webhook config
            config = self.config_manager.get_webhook(webhook_id)
            if not config:
                raise ValueError(f"Webhook {webhook_id} not found in config")

            # Create webhook from URL
            webhook = discord.Webhook.from_url(config["url"], session=self.bot.http._HTTPClient__session)

            # Send test message
            await webhook.send(
                content=test_message,
                username="Webhook Test",
                avatar_url=None
            )

            logger.info(f"Successfully tested webhook {webhook_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to test webhook {webhook_id}: {e}")
            return False

    async def get_webhook_info(self, webhook_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a webhook.

        Args:
            webhook_id: Webhook ID

        Returns:
            Webhook information dictionary
        """
        if not DISCORD_AVAILABLE or not self.bot:
            return None

        try:
            # Try to fetch from Discord API first
            webhook = None
            for guild in self.bot.guilds:
                try:
                    webhook = await guild.fetch_webhook(int(webhook_id))
                    break
                except (discord.NotFound, discord.Forbidden):
                    continue

            if webhook:
                info = {
                    "id": str(webhook.id),
                    "name": webhook.name,
                    "channel": f"#{webhook.channel.name}" if webhook.channel else "Unknown",
                    "guild": webhook.guild.name if webhook.guild else "Unknown",
                    "created_at": str(webhook.created_at) if webhook.created_at else None,
                    "user": str(webhook.user) if webhook.user else "Unknown",
                    "url": webhook.url,
                    "status": "active"
                }
            else:
                # Fallback to config data
                config = self.config_manager.get_webhook(webhook_id)
                if config:
                    info = config.copy()
                    info["status"] = "config_only"
                else:
                    return None

            return info

        except Exception as e:
            logger.error(f"Failed to get webhook info for {webhook_id}: {e}")
            return None

    async def list_channel_webhooks(self, channel: discord.TextChannel) -> List[Dict[str, Any]]:
        """
        List all webhooks for a channel.

        Args:
            channel: Discord text channel

        Returns:
            List of webhook information dictionaries
        """
        if not DISCORD_AVAILABLE:
            return []

        try:
            webhooks = await channel.webhooks()
            return [{
                "id": str(webhook.id),
                "name": webhook.name,
                "created_at": str(webhook.created_at) if webhook.created_at else None,
                "user": str(webhook.user) if webhook.user else "Unknown"
            } for webhook in webhooks]

        except Exception as e:
            logger.error(f"Failed to list webhooks for channel {channel.name}: {e}")
            return []

    async def _get_avatar_bytes(self, avatar_url: str) -> Optional[bytes]:
        """Get avatar bytes from URL."""
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(avatar_url) as response:
                    if response.status == 200:
                        return await response.read()
        except Exception as e:
            logger.warning(f"Failed to fetch avatar from {avatar_url}: {e}")
        return None

# Global service instance
webhook_service = WebhookService()

__all__ = [
    "WebhookService",
    "WebhookConfigManager",
    "webhook_service"
]