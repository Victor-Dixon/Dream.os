#!/usr/bin/env python3
"""
Devlog Poster - Post devlogs to Agent-Specific Discord Channels
================================================================

Posts devlogs to each agent's dedicated Discord channel using Discord bot.

Usage:
    python tools/devlog_poster.py --agent Agent-X --file <devlog_path>

Example:
    python tools/devlog_poster.py --agent Agent-3 --file devlogs/2025-12-26_status.md
"""

import sys
import argparse
import asyncio
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

load_dotenv(project_root / ".env")

try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    print("❌ discord.py not installed! Run: pip install discord.py")


async def post_devlog_async(agent_id: str, devlog_path: str, title: str = None) -> bool:
    """
    Post devlog to agent-specific Discord channel.
    
    Args:
        agent_id: Agent identifier (e.g., "Agent-3")
        devlog_path: Path to devlog markdown file
        title: Optional title (defaults to devlog filename)
    
    Returns:
        True if successful, False otherwise
    """
    if not DISCORD_AVAILABLE:
        print("❌ discord.py not available")
        return False
    
    devlog_file = Path(devlog_path)
    
    if not devlog_file.exists():
        print(f"❌ Devlog file not found: {devlog_path}")
        return False
    
    # Read devlog content
    try:
        devlog_content = devlog_file.read_text(encoding='utf-8')
    except Exception as e:
        print(f"❌ Failed to read devlog file: {e}")
        return False
    
    # Extract title from devlog if not provided
    if not title:
        if devlog_content.startswith("#"):
            first_line = devlog_content.split("\n")[0]
            title = first_line.replace("#", "").strip()
        else:
            title = devlog_file.stem
    
    # Truncate content if too long (Discord limit 2000 chars total)
    # Account for: header (~100), footer (~50), file reference (~50), truncation msg (~50)
    # Total overhead: ~250 chars, so max content is ~1750 chars
    file_reference = f"\n\n📄 **Full Devlog**: `{devlog_file.name}`"
    truncation_msg = "\n\n... (truncated - see full devlog in workspace)"
    header_footer = f"📢 ## Devlog: {title}\n\n" + f"\n\n*Posted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
    max_content_length = 2000 - len(header_footer) - len(file_reference) - len(truncation_msg) - 50  # Safety margin
    
    if len(devlog_content) > max_content_length:
        truncated_content = devlog_content[:max_content_length] + truncation_msg
        print(f"⚠️  Devlog content truncated ({len(devlog_content)} chars → {max_content_length} chars)")
        message = truncated_content + file_reference
    else:
        message = devlog_content + file_reference
    
    # Get Discord token
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        print("❌ DISCORD_BOT_TOKEN not set in .env")
        return False
    
    # Initialize bot
    intents = discord.Intents.default()
    intents.message_content = True
    intents.guilds = True
    
    bot = commands.Bot(command_prefix="!", intents=intents)
    posted = False
    error_msg = None
    
    @bot.event
    async def on_ready():
        nonlocal posted, error_msg
        try:
            # Find agent-specific channel (format: "agent-3")
            agent_num = agent_id.lower().replace('agent-', '')
            channel_name = f"agent-{agent_num}"
            
            channel = None
            for guild in bot.guilds:
                for ch in guild.text_channels:
                    if ch.name == channel_name:
                        channel = ch
                        break
                if channel:
                    break
            
            if not channel:
                error_msg = f"Channel #{channel_name} not found"
                print(f"❌ {error_msg}")
                available = [ch.name for guild in bot.guilds for ch in guild.text_channels]
                print(f"   Available channels: {available}")
                await bot.close()
                return
            
            # Format message (message already includes file reference and truncation if needed)
            content = f"📢 ## Devlog: {title}\n\n{message}\n\n*Posted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
            
            # Final safety check - Discord limit is 2000 chars
            if len(content) > 2000:
                # Truncate more aggressively
                max_final = 2000 - len(f"📢 ## Devlog: {title}\n\n") - len(f"\n\n*Posted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*") - 100
                message_truncated = message[:max_final] + "\n\n... (message too long - see full devlog in workspace)"
                content = f"📢 ## Devlog: {title}\n\n{message_truncated}\n\n*Posted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
            
            # Post to channel
            await channel.send(content)
            print(f"✅ Devlog posted to #{channel.name}: {title}")
            posted = True
            await bot.close()
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error posting to Discord: {e}")
            await bot.close()
    
    # Run bot
    try:
        async with bot:
            await bot.start(token)
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Failed to connect to Discord: {e}")
        return False
    
    return posted


def post_devlog(agent_id: str, devlog_path: str, title: str = None) -> bool:
    """Synchronous wrapper for async post_devlog."""
    return asyncio.run(post_devlog_async(agent_id, devlog_path, title))


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Post devlog to agent-specific Discord channel",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/devlog_poster.py --agent Agent-3 --file devlogs/2025-12-26_status.md
  python tools/devlog_poster.py --agent Agent-7 --file agent_workspaces/Agent-7/devlogs/status.md --title "Agent-7 Status Update"
        """
    )
    
    parser.add_argument(
        "--agent",
        required=True,
        help="Agent identifier (e.g., Agent-3)"
    )
    
    parser.add_argument(
        "--file",
        required=True,
        help="Path to devlog markdown file"
    )
    
    parser.add_argument(
        "--title",
        help="Optional title (defaults to devlog filename or first # heading)"
    )
    
    args = parser.parse_args()
    
    # Post devlog
    success = post_devlog(
        agent_id=args.agent,
        devlog_path=args.file,
        title=args.title
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
