#!/usr/bin/env python3
"""
Unified Discord Bot Startup Script
===================================

Single entry point for Discord bot startup with comprehensive error handling.
V2 Compliant: <400 lines

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
Priority: CRITICAL
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)

# Discord imports
try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    logger.error("❌ discord.py not installed! Install with: pip install discord.py")
    sys.exit(1)


def validate_environment() -> tuple[bool, list[str]]:
    """Validate environment before bot startup."""
    issues = []
    
    # Check Discord token
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        issues.append("DISCORD_BOT_TOKEN not set in environment")
    elif len(token) < 50:  # Basic validation
        issues.append("DISCORD_BOT_TOKEN appears invalid (too short)")
    
    # Check Discord library
    if not DISCORD_AVAILABLE:
        issues.append("discord.py library not available")
    
    # Check workspace directories
    workspace_root = Path("agent_workspaces")
    if not workspace_root.exists():
        issues.append(f"Workspace root not found: {workspace_root}")
    
    return (len(issues) == 0, issues)


def print_startup_info():
    """Print startup information."""
    print("\n" + "="*70)
    print("🚀 DISCORD BOT STARTUP")
    print("="*70)
    print(f"Python: {sys.version.split()[0]}")
    print(f"Discord.py: {discord.__version__ if DISCORD_AVAILABLE else 'NOT AVAILABLE'}")
    print(f"Workspace: {Path('agent_workspaces').absolute()}")
    print("="*70 + "\n")


async def start_bot():
    """Start the Discord bot with error handling."""
    # Pre-flight validation
    is_valid, issues = validate_environment()
    if not is_valid:
        logger.error("❌ Pre-flight validation failed:")
        for issue in issues:
            logger.error(f"   • {issue}")
        logger.error("\n💡 Fix these issues before starting the bot:")
        logger.error("   1. Set DISCORD_BOT_TOKEN in .env file or environment")
        logger.error("   2. Install discord.py: pip install discord.py")
        logger.error("   3. Ensure agent_workspaces directory exists")
        sys.exit(1)
    
    print_startup_info()
    
    # Import bot setup
    try:
        from src.discord_commander.discord_commander_bot import setup_unified_bot
    except ImportError as e:
        logger.error(f"❌ Failed to import bot setup: {e}")
        logger.error("   Ensure src/discord_commander/discord_commander_bot.py exists")
        sys.exit(1)
    
    # Start bot
    try:
        logger.info("🚀 Starting Unified Discord Bot...")
        logger.info("🐝 WE. ARE. SWARM.")
        await setup_unified_bot()
    except discord.LoginFailure:
        logger.error("❌ Invalid Discord bot token!")
        logger.error("   Check your DISCORD_BOT_TOKEN in .env file")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("\n👋 Bot shutdown requested by user")
    except Exception as e:
        logger.error(f"❌ Bot startup error: {e}", exc_info=True)
        logger.error("\n💡 Troubleshooting:")
        logger.error("   1. Verify DISCORD_BOT_TOKEN is correct")
        logger.error("   2. Check bot has proper permissions in Discord")
        logger.error("   3. Ensure all dependencies are installed")
        logger.error("   4. Check network connectivity")
        sys.exit(1)


def main():
    """Main entry point."""
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        logger.info("\n👋 Startup script interrupted")
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

