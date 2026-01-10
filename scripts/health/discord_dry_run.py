#!/usr/bin/env python3
"""
Discord Dry Run Test - Agent Cellphone V2
=========================================

Tests Discord bot connection without posting messages.
Used for smoke testing during recovery.

Exit codes:
0 = Connection successful (dry-run)
1 = Connection failed

Author: Agent-6 (Discord Messaging Recovery Specialist)
Date: 2026-01-09
"""

import os
import sys
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Discord imports
try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False

class DiscordDryRunBot(commands.Bot):
    """Minimal bot for dry-run testing."""

    def __init__(self, token: str):
        """Initialize bot with required intents for dry-run."""
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True  # Privileged intent
        intents.voice_states = True

        super().__init__(command_prefix="!", intents=intents, help_command=None)
        self.token = token
        self.test_passed = False

    async def on_ready(self):
        """Handle successful connection."""
        print(f"✅ Connected as {self.user}")
        print(f"   Guilds: {len(self.guilds)}")
        print(f"   Users: {len(self.users) if self.intents.members else 'N/A'}")
        self.test_passed = True

        # Disconnect immediately after successful connection
        await self.close()

    async def test_connection(self) -> bool:
        """Test Discord connection and return result."""
        try:
            print("🔍 Testing Discord connection (dry-run)...")

            # Attempt login (this will validate token and intents)
            await self.login(self.token)
            print("✅ Token validation successful")

            # Start the bot briefly to test full connection
            await self.start(self.token)

        except discord.PrivilegedIntentsRequired as e:
            print("❌ Privileged intents required but not enabled")
            print("   Required intents: members, message_content")
            print("   Enable at: https://discord.com/developers/applications/")
            print("   Bot Settings → Privileged Gateway Intents")
            return False

        except discord.LoginFailure as e:
            print(f"❌ Invalid Discord token: {e}")
            return False

        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            return False

        return self.test_passed

async def main():
    """Main dry-run test function."""
    if not DISCORD_AVAILABLE:
        print("❌ discord.py not available. Install with: pip install discord.py")
        return 1

    # Get token from environment
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        print("❌ DISCORD_BOT_TOKEN environment variable not set")
        return 1

    # Create and test bot
    bot = DiscordDryRunBot(token)
    success = await bot.test_connection()

    if success:
        print("✅ Discord dry-run test PASSED")
        return 0
    else:
        print("❌ Discord dry-run test FAILED")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)