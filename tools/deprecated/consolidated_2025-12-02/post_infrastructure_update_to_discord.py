#!/usr/bin/env python3
"""
Post Infrastructure Update to Discord
=====================================

Posts infrastructure status updates to Discord using the bot.
Can be called from automation scripts or manually.

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


async def post_update_to_discord(
    title: str,
    content: str,
    status: str = "info",
    channel_id: int | None = None,
) -> bool:
    """
    Post infrastructure update to Discord channel.
    
    Args:
        title: Update title
        content: Update content
        status: Status type (info, success, warning, error)
        channel_id: Optional channel ID (uses DISCORD_CHANNEL_ID env var if not provided)
        
    Returns:
        True if posted successfully
    """
    if not DISCORD_AVAILABLE:
        logger.warning("Discord not available - update not posted")
        return False
    
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        logger.warning("DISCORD_BOT_TOKEN not set - update not posted")
        return False
    
    if not channel_id:
        channel_id_str = os.getenv("DISCORD_CHANNEL_ID")
        if channel_id_str:
            try:
                channel_id = int(channel_id_str)
            except ValueError:
                logger.warning(f"Invalid DISCORD_CHANNEL_ID: {channel_id_str}")
                return False
        else:
            logger.warning("No channel ID provided and DISCORD_CHANNEL_ID not set")
            return False
    
    try:
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        
        bot = commands.Bot(command_prefix="!", intents=intents)
        
        @bot.event
        async def on_ready():
            try:
                channel = await bot.fetch_channel(channel_id)
                
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
                logger.info(f"✅ Infrastructure update posted to Discord: {title}")
                
                await bot.close()
            except Exception as e:
                logger.error(f"❌ Failed to post update: {e}")
                await bot.close()
        
        await bot.start(token)
        return True
        
    except Exception as e:
        logger.error(f"❌ Discord update error: {e}")
        return False


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Post Infrastructure Update to Discord")
    parser.add_argument("--title", required=True, help="Update title")
    parser.add_argument("--content", required=True, help="Update content")
    parser.add_argument("--status", default="info", choices=["info", "success", "warning", "error"], help="Status type")
    parser.add_argument("--channel-id", type=int, help="Discord channel ID (or use DISCORD_CHANNEL_ID env var)")
    
    args = parser.parse_args()
    
    success = asyncio.run(
        post_update_to_discord(
            title=args.title,
            content=args.content,
            status=args.status,
            channel_id=args.channel_id,
        )
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()




