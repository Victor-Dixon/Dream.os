#!/usr/bin/env python3
"""
Twitch Chat Bot Launcher
========================

Starts the Twitch chat bot (ChatPresenceOrchestrator) for the SWARM agent system.

This script:
- Loads Twitch credentials from environment variables
- Creates and starts the ChatPresenceOrchestrator
- Maintains the connection with automatic reconnection
- Handles graceful shutdown on Ctrl+C

Usage:
    python tools/START_CHAT_BOT_NOW.py

Environment Variables Required:
    TWITCH_CHANNEL       - Twitch channel name (without #)
    TWITCH_ACCESS_TOKEN  - OAuth token for the bot account
    TWITCH_BOT_USERNAME  - Bot's Twitch username (defaults to channel name)

Author: Agent-7 (Web Development Specialist)
V2 Compliant: <100 lines
"""

import asyncio
import os
import sys
import signal
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()


async def main():
    """Main entry point for Twitch chat bot."""
    # Import after path setup
    from src.services.chat_presence.chat_presence_orchestrator import ChatPresenceOrchestrator

    # Get configuration from environment
    channel = os.getenv("TWITCH_CHANNEL", "").strip()
    oauth_token = os.getenv("TWITCH_ACCESS_TOKEN", "").strip()

    # Validate configuration exists
    if not channel:
        print("❌ ERROR: TWITCH_CHANNEL environment variable not set")
        print("   Set it in your .env file: TWITCH_CHANNEL=yourchannel")
        print("   Example: TWITCH_CHANNEL=digital_dreamscape")
        sys.exit(1)

    if not oauth_token:
        print("❌ ERROR: TWITCH_ACCESS_TOKEN environment variable not set")
        print("   Set it in your .env file: TWITCH_ACCESS_TOKEN=oauth:xxxxx")
        print("   Get token from: https://twitchtokengenerator.com/")
        sys.exit(1)

    # Validate channel format (remove # if present, remove URL if present)
    if channel.startswith("#"):
        channel = channel[1:]
        print(f"   ⚠️  Removed # prefix from channel: {channel}")

    if "twitch.tv/" in channel.lower():
        # Extract channel name from URL
        parts = channel.lower().split("twitch.tv/")
        if len(parts) > 1:
            channel = parts[-1].split("/")[0].split("?")[0].rstrip("/")
            print(f"   ⚠️  Extracted channel name from URL: {channel}")

    # Normalize channel (lowercase, no spaces)
    channel = channel.lower().strip()

    # Set username after channel parsing (use channel name, not full URL)
    username = os.getenv("TWITCH_BOT_USERNAME", "").strip() or channel

    # Validate token format
    token_clean = oauth_token.strip().strip('"').strip("'")
    if not token_clean.startswith("oauth:"):
        print("   ⚠️  Token doesn't start with 'oauth:' - adding prefix")
        oauth_token = f"oauth:{token_clean}"
    else:
        oauth_token = token_clean

    # Username should already be set above, but ensure it's lowercase
    username = username.lower().strip()

    print("🐺 SWARM Twitch Chat Bot Starting...")
    print(f"   Channel: #{channel}")
    print(f"   Username: {username}")
    print(f"   Token: {'SET' if oauth_token else 'NOT SET'}")
    print()

    # Create orchestrator with Twitch config
    twitch_config = {
        "channel": channel,
        "oauth_token": oauth_token,
        "username": username,
        "admin_users": os.getenv("TWITCH_ADMIN_USERS", "").strip(),
    }

    orchestrator = ChatPresenceOrchestrator(twitch_config=twitch_config)

    # Handle shutdown signals
    shutdown_event = asyncio.Event()

    def signal_handler():
        print("\n🛑 Shutdown signal received...")
        shutdown_event.set()

    # Register signal handlers
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, signal_handler)
        except NotImplementedError:
            # Windows doesn't support add_signal_handler
            signal.signal(sig, lambda s, f: signal_handler())

    try:
        # Start the orchestrator
        success = await orchestrator.start()
        
        if success:
            print("✅ Twitch Chat Bot is running!")
            print("   Use !status in chat to check agent status")
            print("   Press Ctrl+C to stop")
            print()
            
            # Keep running until shutdown
            await shutdown_event.wait()
        else:
            print("❌ Failed to start Twitch Chat Bot")
            print("   Check logs for details: logs/chat_presence_orchestrator.log")
            sys.exit(1)

    finally:
        # Graceful shutdown
        print("🔌 Disconnecting from Twitch...")
        await orchestrator.stop()
        print("👋 Twitch Chat Bot stopped. Goodbye!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Interrupted. Goodbye!")

