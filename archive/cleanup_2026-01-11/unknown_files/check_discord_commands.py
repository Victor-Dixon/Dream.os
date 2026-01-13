#!/usr/bin/env python3
"""
Check Discord Bot Commands - Debug Script
=========================================

Checks what commands are registered and their requirements.
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    import discord
    from discord.ext import commands
    print("✅ Discord.py available")
except ImportError as e:
    print(f"❌ Discord.py not available: {e}")
    sys.exit(1)

def check_commands():
    """Check what commands are available and their requirements."""

    # Import the bot
    try:
        from src.discord_commander.unified_discord_bot import UnifiedDiscordBot
        print("✅ Bot module imported successfully")
    except ImportError as e:
        print(f"❌ Bot import failed: {e}")
        return

    # Create a minimal bot instance for inspection
    try:
        bot = UnifiedDiscordBot()
        print("✅ Bot instance created successfully")
    except Exception as e:
        print(f"❌ Bot creation failed: {e}")
        return

    # Check specific commands
    commands_to_check = ['gui', 'control', 'status', 'help', 'commands']

    print("\n📋 COMMAND REGISTRATION STATUS:")
    print("=" * 50)

    for cmd_name in commands_to_check:
        cmd = bot.get_command(cmd_name)
        if cmd:
            print(f"✅ {cmd_name}: REGISTERED")
            if hasattr(cmd, 'checks') and cmd.checks:
                print(f"   📋 Checks: {len(cmd.checks)} check(s)")
                for i, check in enumerate(cmd.checks):
                    print(f"      {i+1}. {check}")
            else:
                print("   📋 Checks: None (no restrictions)")
        else:
            print(f"❌ {cmd_name}: NOT REGISTERED")

    print("\n🔍 TROUBLESHOOTING:")
    print("- If commands show role requirements, ensure user has 'Admin', 'Captain', or 'Swarm Commander' role")
    print("- Check bot logs for registration errors")
    print("- Verify bot has proper permissions in Discord server")

if __name__ == "__main__":
    check_commands()