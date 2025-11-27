#!/usr/bin/env python3
"""
Discord Status Updater
======================

Posts infrastructure status updates to Discord channel.
Uses Discord bot to send updates to Agent-3's channel.

Author: Agent-3 (Infrastructure & DevOps) - JET FUEL AUTONOMOUS MODE
Created: 2025-01-27
Priority: CRITICAL
"""

import asyncio
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    discord = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DiscordStatusUpdater:
    """Update Discord channel with infrastructure status."""

    def __init__(self, channel_id: int | None = None):
        """Initialize status updater."""
        self.channel_id = channel_id or int(os.getenv("DISCORD_CHANNEL_ID", "0"))
        self.token = os.getenv("DISCORD_BOT_TOKEN")
        
        if not self.token:
            logger.warning("DISCORD_BOT_TOKEN not set - Discord updates disabled")
            self.bot = None
        else:
            intents = discord.Intents.default()
            intents.message_content = True
            self.bot = commands.Bot(command_prefix="!", intents=intents) if DISCORD_AVAILABLE else None

    async def post_status_update(self, title: str, content: str, status: str = "info") -> bool:
        """
        Post status update to Discord channel.
        
        Args:
            title: Update title
            content: Update content
            status: Status type (info, success, warning, error)
            
        Returns:
            True if posted successfully
        """
        if not self.bot or not self.token:
            logger.warning("Discord bot not available - skipping update")
            return False
        
        try:
            await self.bot.login(self.token)
            channel = await self.bot.fetch_channel(self.channel_id)
            
            # Color based on status
            colors = {
                "info": discord.Color.blue(),
                "success": discord.Color.green(),
                "warning": discord.Color.orange(),
                "error": discord.Color.red(),
            }
            
            embed = discord.Embed(
                title=f"🔧 {title}",
                description=content,
                color=colors.get(status, discord.Color.blue()),
                timestamp=datetime.utcnow(),
            )
            
            embed.set_footer(text="Agent-3 | Infrastructure & DevOps")
            
            await channel.send(embed=embed)
            await self.bot.close()
            
            logger.info(f"✅ Status update posted to Discord: {title}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to post Discord update: {e}")
            return False

    def post_update_sync(self, title: str, content: str, status: str = "info") -> bool:
        """Synchronous wrapper for posting updates."""
        if not DISCORD_AVAILABLE or not self.bot:
            logger.warning("Discord not available - update not posted")
            return False
        
        try:
            asyncio.run(self.post_status_update(title, content, status))
            return True
        except Exception as e:
            logger.error(f"Failed to post update: {e}")
            return False


def post_infrastructure_update(title: str, content: str, status: str = "info") -> bool:
    """Convenience function to post infrastructure updates."""
    updater = DiscordStatusUpdater()
    return updater.post_update_sync(title, content, status)


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Discord Status Updater")
    parser.add_argument("--title", required=True, help="Update title")
    parser.add_argument("--content", required=True, help="Update content")
    parser.add_argument("--status", default="info", choices=["info", "success", "warning", "error"], help="Status type")
    
    args = parser.parse_args()
    
    updater = DiscordStatusUpdater()
    success = updater.post_update_sync(args.title, args.content, args.status)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()




