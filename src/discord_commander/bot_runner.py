#!/usr/bin/env python3
"""
Bot Runner - Agent Cellphone V2
==============================

SSOT Domain: discord

Refactored entry point for Discord bot runner.
All core logic has been extracted into service architecture for V2 compliance.

Features:
- Bot lifecycle management
- Automatic reconnection with backoff
- Environment validation
- Logging and error handling (bot_runner_v2.py)

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Discord imports
try:
    import discord
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False

def main():
    """Main entry point for Discord bot."""
    if not DISCORD_AVAILABLE:
        print("❌ discord.py not available. Install with: pip install discord.py")
        return 1

    # Import and run the bot
    try:
        from src.discord_commander.unified_discord_bot import UnifiedDiscordBot

        # Get token from environment
        token = os.getenv('DISCORD_BOT_TOKEN')
        if not token:
            print("❌ DISCORD_BOT_TOKEN environment variable not set")
            print("💡 Set it in your .env file or environment")
            return 1

        # Create and run bot
        bot = UnifiedDiscordBot(token=token)
        bot.run(token)

    except Exception as e:
        print(f"❌ Failed to start Discord bot: {e}")
        return 1

    return 0
