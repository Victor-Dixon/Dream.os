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
    
    # Parse channel from TWITCH_SWARM_VOICE if present
    if swarm_voice:
        parts = swarm_voice.split("|")
        if len(parts) >= 3:
            # Channel is in TWITCH_SWARM_VOICE, use it
            channel = parts[2].strip()
        elif len(parts) < 3 and not channel:
            # TWITCH_SWARM_VOICE incomplete and no separate channel
            issues.append("⚠️  TWITCH_SWARM_VOICE found but incomplete (need: username|token|channel)")
            issues.append("   Format: TWITCH_SWARM_VOICE=username|oauth:token|channel")
            issues.append("   Or set TWITCH_CHANNEL=your_channel_name in .env")
    
    if not access_token and not swarm_voice:
        issues.append("❌ No Twitch access token found")
        issues.append("   Set TWITCH_ACCESS_TOKEN in .env or run:")
        issues.append("   python tools/twitch_oauth_setup.py")
    elif access_token and not channel:
        issues.append("⚠️  Access token found but no channel specified")
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
    channel = os.getenv("TWITCH_CHANNEL", "").strip()
    swarm_voice = os.getenv("TWITCH_SWARM_VOICE")
    
    # Fix channel name if it's a URL
    if channel:
        # Extract channel name from URL if needed
        if "twitch.tv/" in channel.lower():
            # Extract channel name from URL
            parts = [p for p in channel.split("/") if p.strip()]  # Filter empty parts
            channel = parts[-1].strip() if parts else channel
            # Remove trailing slash or empty string
            channel = channel.rstrip("/").strip()
            if channel.startswith("#"):
                channel = channel[1:]
            print(f"🔧 Extracted channel name from URL: {channel}")
        # Remove any # prefix
        if channel.startswith("#"):
            channel = channel[1:]
    
    # Build config
    twitch_config = None
    
    if access_token and channel:
        username = os.getenv("TWITCH_BOT_USERNAME") or channel
        # Ensure token has oauth: prefix (required by Twitch IRC)
        oauth_token = access_token
        if not oauth_token.startswith("oauth:"):
            oauth_token = f"oauth:{oauth_token}"
        twitch_config = {
            "username": username,
            "oauth_token": oauth_token,
            "channel": channel,
        }
        print(f"✅ Using OAuth token for channel: {channel}")
    elif swarm_voice:
        parts = swarm_voice.split("|")
        if len(parts) == 3:
            # Full format: username|token|channel
            username, oauth_token, channel = [p.strip() for p in parts]
            twitch_config = {
                "username": username,
                "oauth_token": oauth_token,
                "channel": channel,
            }
            print(f"✅ Using TWITCH_SWARM_VOICE for channel: {channel}")
        elif len(parts) == 1 and channel:
            # Only token in TWITCH_SWARM_VOICE, but channel set separately
            username = os.getenv("TWITCH_BOT_USERNAME") or channel
            oauth_token = parts[0].strip()
            # Ensure token has oauth: prefix
            if not oauth_token.startswith("oauth:"):
                oauth_token = f"oauth:{oauth_token}"
            twitch_config = {
                "username": username,
                "oauth_token": oauth_token,
                "channel": channel,
            }
            print(f"✅ Using TWITCH_SWARM_VOICE (token) + TWITCH_CHANNEL: {channel}")
        elif len(parts) == 1:
            # Only token, no channel
            print("❌ TWITCH_SWARM_VOICE has token but no channel")
            print("   Set TWITCH_CHANNEL=your_channel_name in .env")
            return
    
    if not twitch_config:
        print("❌ Could not determine Twitch configuration")
        print()
        print("💡 Setup options:")
        print("   1. Set TWITCH_ACCESS_TOKEN and TWITCH_CHANNEL")
        print("   2. Set TWITCH_SWARM_VOICE=username|oauth:token|channel")
        print("   3. Set TWITCH_SWARM_VOICE=token and TWITCH_CHANNEL=channel")
        print("   4. Run: python tools/twitch_oauth_setup.py")
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



