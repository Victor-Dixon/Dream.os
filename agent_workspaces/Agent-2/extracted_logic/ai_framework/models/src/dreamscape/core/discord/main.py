"""
Discord Main Module
==================

Main entry point for Discord integration testing.
"""

import os
import sys
from pathlib import Path

# Add the src directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

# EDIT START
# Refactored to use centralized discord import logic from utils.py to avoid circular imports and duplicate logic.
from .utils import DISCORD_AVAILABLE, discord, commands

# Removed any local discord.py import logic.
# EDIT END


def main():
    """Test the Discord manager."""
    dm = DiscordManager()

    print("Discord Manager Test:")
    print(f"Enabled: {dm.config['enabled']}")
    print(f"Bot Token: {'Set' if dm.config['bot_token'] else 'Not Set'}")
    print(f"Application ID: {dm.config.get('application_id', 'Not Set')}")
    print(f"Guild ID: {dm.config['guild_id']}")
    print(f"Channel ID: {dm.config['channel_id']}")
    print(f"Features: {dm.config['features']}")
    print(
        f"Environment Token: {'Available' if os.getenv('DISCORD_BOT_TOKEN') else 'Not Set'}"
    )
    print(
        f"Environment App ID: {'Available' if os.getenv('DISCORD_APPLICATION_ID') else 'Not Set'}"
    )

    if not dm.bot:
        print("\n⚠️  Discord.py not installed. Install with: pip install discord.py")


if __name__ == "__main__":
    main()
