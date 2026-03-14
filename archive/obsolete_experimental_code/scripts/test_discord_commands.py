#!/usr/bin/env python3
"""
Test Discord bot commands
"""

import asyncio
import discord
import os
from pathlib import Path

async def test_bot_commands():
    """Test Discord bot command processing"""

    print("🧪 TESTING DISCORD BOT COMMANDS")
    print("=" * 50)

    # Load configuration
    token = None
    channel_id = None

    # Try environment variables first
    token = os.getenv('DISCORD_BOT_TOKEN')
    channel_id = os.getenv('DISCORD_INFRASTRUCTURE_CHANNEL_ID')

    # If not found, load from .env.discord
    if not token or not channel_id:
        env_file = Path('.env.discord')
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not token and 'DISCORD_BOT_TOKEN=' in line:
                        token = line.split('=', 1)[1].strip().strip('"').strip("'")
                    elif not channel_id and 'DISCORD_INFRASTRUCTURE_CHANNEL_ID=' in line:
                        channel_id = line.split('=', 1)[1].strip().strip('"').strip("'")

    if not token or not channel_id:
        print("❌ Missing Discord configuration")
        return False

    try:
        # Create test bot
        intents = discord.Intents.default()
        intents.message_content = True

        bot = discord.Client(intents=intents)
        test_results = {
            'connected': False,
            'help_command': False,
            'status_command': False
        }

        @bot.event
        async def on_ready():
            nonlocal test_results
            test_results['connected'] = True
            print(f"✅ Test bot connected as {bot.user}")

            try:
                channel = bot.get_channel(int(channel_id))
                if channel:
                    # Test help command
                    print("🧪 Testing !help command...")
                    await channel.send("!help")

                    # Test status command
                    print("🧪 Testing !status command...")
                    await channel.send("!status")

                    # Wait a bit for responses
                    await asyncio.sleep(3)

                    print("✅ Commands sent - check Discord for responses")
                    test_results['help_command'] = True
                    test_results['status_command'] = True

                else:
                    print(f"❌ Could not find channel {channel_id}")

            except Exception as e:
                print(f"❌ Failed to send test commands: {e}")

            await bot.close()

        print("🔗 Connecting test bot...")
        await bot.start(token)

        # Report results
        print()
        print("📊 TEST RESULTS:")
        print(f"✅ Bot Connection: {'PASSED' if test_results['connected'] else 'FAILED'}")
        print(f"✅ Help Command: {'SENT' if test_results['help_command'] else 'FAILED'}")
        print(f"✅ Status Command: {'SENT' if test_results['status_command'] else 'FAILED'}")

        if all(test_results.values()):
            print()
            print("🎉 COMMAND TESTING COMPLETE!")
            print("💡 Check Discord channel for bot responses")
            print("💡 If no responses, the main bot may not be processing commands")
            return True
        else:
            print()
            print("❌ COMMAND TESTING FAILED")
            return False

    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_bot_commands())
    exit(0 if success else 1)