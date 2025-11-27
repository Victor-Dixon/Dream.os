#!/usr/bin/env python3
"""
START CHAT BOT NOW
==================

Quick launcher for Twitch chat bot - ready to go immediately.

Usage:
    python tools/START_CHAT_BOT_NOW.py
"""

import asyncio
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load .env
try:
    from dotenv import load_dotenv, dotenv_values
    env_vars = dotenv_values(".env")
    for key, value in env_vars.items():
        if value and key not in os.environ:
            os.environ[key] = value
    load_dotenv()
except ImportError:
    pass

from src.services.chat_presence import ChatPresenceOrchestrator
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def check_config():
    """Check if configuration is ready."""
    issues = []
    
    # Check for OAuth token
    access_token = os.getenv("TWITCH_ACCESS_TOKEN")
    channel = os.getenv("TWITCH_CHANNEL")
    swarm_voice = os.getenv("TWITCH_SWARM_VOICE")
    
    if not access_token and not swarm_voice:
        issues.append("❌ No Twitch access token found")
        issues.append("   Set TWITCH_ACCESS_TOKEN in .env or run:")
        issues.append("   python tools/twitch_oauth_setup.py")
    elif access_token and not channel:
        issues.append("⚠️  Access token found but no channel specified")
        issues.append("   Set TWITCH_CHANNEL=your_channel_name in .env")
    
    if not channel and swarm_voice:
        # Try to parse from TWITCH_SWARM_VOICE
        parts = swarm_voice.split("|")
        if len(parts) >= 3:
            channel = parts[2].strip()
        elif len(parts) == 1:
            # Might just be a token, need channel
            issues.append("⚠️  TWITCH_SWARM_VOICE found but channel missing")
            issues.append("   Set TWITCH_CHANNEL=your_channel_name in .env")
    
    if issues:
        print("\n".join(issues))
        return False
    
    return True


async def main():
    print("=" * 60)
    print("🚀 STARTING TWITCH CHAT BOT")
    print("=" * 60)
    print()
    
    # Check configuration
    if not check_config():
        print()
        print("Please configure your Twitch credentials first.")
        print("See: docs/chat_presence/TWITCH_OAUTH_SETUP.md")
        return
    
    # Load configuration
    access_token = os.getenv("TWITCH_ACCESS_TOKEN")
    channel = os.getenv("TWITCH_CHANNEL")
    swarm_voice = os.getenv("TWITCH_SWARM_VOICE")
    
    # Build config
    twitch_config = None
    
    if access_token and channel:
        username = os.getenv("TWITCH_BOT_USERNAME") or channel
        twitch_config = {
            "username": username,
            "oauth_token": access_token,
            "channel": channel,
        }
        print(f"✅ Using OAuth token for channel: {channel}")
    elif swarm_voice:
        parts = swarm_voice.split("|")
        if len(parts) == 3:
            username, oauth_token, channel = [p.strip() for p in parts]
            twitch_config = {
                "username": username,
                "oauth_token": oauth_token,
                "channel": channel,
            }
            print(f"✅ Using TWITCH_SWARM_VOICE for channel: {channel}")
    
    if not twitch_config:
        print("❌ Could not determine Twitch configuration")
        return
    
    print()
    print("🔌 Connecting to Twitch...")
    print()
    
    # Create orchestrator
    orchestrator = ChatPresenceOrchestrator(
        twitch_config=twitch_config,
        obs_config=None,  # Disable OBS for now
    )
    
    # Start system
    success = await orchestrator.start()
    
    if not success:
        print("❌ Failed to start chat bot")
        return
    
    print()
    print("=" * 60)
    print("✅ CHAT BOT IS LIVE!")
    print("=" * 60)
    print()
    print("The swarm is now active in your Twitch chat!")
    print()
    print("Test commands:")
    print("  !agent7 hello - Agent-7 responds")
    print("  !team status - All agents respond")
    print("  !swarm hello - Broadcast message")
    print()
    print("Press Ctrl+C to stop")
    print()
    
    try:
        # Keep running
        while orchestrator.running:
            await asyncio.sleep(1)
    
    except KeyboardInterrupt:
        print()
        print("🛑 Shutting down...")
        await orchestrator.stop()
        print("✅ Shutdown complete")


if __name__ == "__main__":
    asyncio.run(main())

