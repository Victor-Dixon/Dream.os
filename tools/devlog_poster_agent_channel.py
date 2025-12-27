#!/usr/bin/env python3
"""
Devlog Poster - Post to Agent-Specific Discord Channels
========================================================

Posts devlogs to each agent's dedicated devlog channel using Discord bot.

Usage:
    python tools/devlog_poster_agent_channel.py --agent Agent-X --file <devlog_path>

Example:
    python tools/devlog_poster_agent_channel.py --agent Agent-5 --file devlogs/2025-12-26_agent5_status_update.md
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


async def post_to_agent_channel(agent_id: str, devlog_path: str, title: str = None):
    """
    Post devlog to agent-specific Discord channel.
    
    Args:
        agent_id: Agent identifier (e.g., "Agent-5")
        devlog_path: Path to devlog markdown file
        title: Optional title (defaults to devlog filename)
    
    Returns:
        True if successful, False otherwise
    """
    if not DISCORD_AVAILABLE:
        print("❌ Discord.py not available")
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
    
    # Truncate content if too long (Discord limit 2000 chars)
    # Account for: title (~50 chars), file reference (~50 chars), timestamp (~50 chars), truncation msg (~50 chars)
    # Total overhead: ~200 chars, so max content is ~1800 chars
    file_reference = f"\n\n📄 **Full Devlog**: `{devlog_file.name}`"
    truncation_msg = "\n\n... (truncated - see full devlog in workspace)"
    max_content_length = 1800 - len(file_reference) - len(truncation_msg)
    
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
    
    @bot.event
    async def on_ready():
        """Bot ready - find channel and post."""
        try:
            # Find agent-specific devlog channel
            # Channel format: "agent-5" or "agent-5-devlogs"
            agent_num = agent_id.lower().replace('agent-', '')
            channel_name = f"agent-{agent_num}"
            fallback_channel_name = f"agent-{agent_num}-devlogs"
            
            channel = None
            for guild in bot.guilds:
                for ch in guild.text_channels:
                    if ch.name == channel_name or ch.name == fallback_channel_name:
                        channel = ch
                        break
                if channel:
                    break
            
            if not channel:
                print(f"❌ Channel #{channel_name} or #{fallback_channel_name} not found")
                print(f"   Available channels: {[ch.name for guild in bot.guilds for ch in guild.text_channels]}")
                await bot.close()
                return
            
            # Format message (ensure total length is under 2000 chars)
            timestamp = f"*Posted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
            header = f"📢 ## {title}\n\n"
            
            # Calculate remaining space for message content
            overhead = len(header) + len(timestamp) + 4  # +4 for newlines
            max_message_length = 2000 - overhead
            
            # Use a local variable to avoid closure issues
            final_message = message
            if len(final_message) > max_message_length:
                # Further truncate if needed
                truncate_at = max_message_length - 50  # Leave room for truncation note
                final_message = final_message[:truncate_at] + "\n\n... (further truncated)"
            
            content = f"{header}{final_message}\n\n{timestamp}"
            
            # Post to channel
            await channel.send(content)
            print(f"✅ Devlog posted to #{channel.name}: {title}")
            await bot.close()
            
        except Exception as e:
            print(f"❌ Error posting to Discord: {e}")
            await bot.close()
    
    # Run bot
    try:
        await bot.start(token)
    except Exception as e:
        print(f"❌ Failed to connect to Discord: {e}")
        return False
    
    return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Post devlog to agent-specific Discord channel",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/devlog_poster_agent_channel.py --agent Agent-5 --file devlogs/2025-12-26_status.md
  python tools/devlog_poster_agent_channel.py --agent Agent-7 --file agent_workspaces/Agent-7/devlogs/status.md --title "Agent-7 Status Update"
        """
    )
    
    parser.add_argument(
        "--agent",
        required=True,
        help="Agent identifier (e.g., Agent-5)"
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
    success = asyncio.run(post_to_agent_channel(
        agent_id=args.agent,
        devlog_path=args.file,
        title=args.title
    ))
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
