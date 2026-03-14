#!/usr/bin/env python3
"""
Test Discord messaging functionality
"""

import asyncio
import os
import discord
from pathlib import Path

async def test_discord_messaging():
    """Test if Discord bot can send messages"""

    print("🧪 TESTING DISCORD MESSAGING FUNCTIONALITY")
    print("=" * 60)

    # Get token from environment or .env.discord file
    token = os.getenv('DISCORD_BOT_TOKEN') or os.getenv('DISCORD_TOKEN')

    if not token:
        # Try to load from .env.discord
        env_file = Path('.env.discord')
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    if line.startswith('DISCORD_BOT_TOKEN=') or line.startswith('DISCORD_TOKEN='):
                        token = line.split('=', 1)[1].strip().strip('"').strip("'")
                        break

    if not token:
        print("❌ No Discord token found!")
        print("💡 Set DISCORD_BOT_TOKEN environment variable or create .env.discord file")
        return False

    # Get channel ID from environment or .env.discord
    channel_id = os.getenv('DISCORD_INFRASTRUCTURE_CHANNEL_ID')

    if not channel_id:
        # Try to load from .env.discord
        env_file = Path('.env.discord')
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    if line.startswith('DISCORD_INFRASTRUCTURE_CHANNEL_ID='):
                        channel_id = line.split('=', 1)[1].strip().strip('"').strip("'")
                        break

    if not channel_id:
        print("❌ No channel ID found!")
        print("💡 Set DISCORD_INFRASTRUCTURE_CHANNEL_ID environment variable")
        return False

    try:
        # Create minimal bot for testing
        intents = discord.Intents.default()
        intents.message_content = True

        bot = discord.Client(intents=intents)
        sent_message = False

        @bot.event
        async def on_ready():
            nonlocal sent_message
            print(f"✅ Bot connected as {bot.user}")

            try:
                channel = bot.get_channel(int(channel_id))
                if channel:
                    test_message = f"🧪 **Discord Messaging Test**\nTimestamp: {discord.utils.utcnow()}\nStatus: Bot messaging functional!"
                    await channel.send(test_message)
                    print(f"✅ Test message sent to {channel.name} (#{channel.name})")
                    sent_message = True
                else:
                    print(f"❌ Could not find channel with ID {channel_id}")
            except Exception as e:
                print(f"❌ Failed to send test message: {e}")

            await bot.close()

        print("🔗 Connecting to Discord for messaging test...")
        await bot.start(token)

        if sent_message:
            print("🎉 MESSAGING TEST PASSED - Bot can send messages!")
            return True
        else:
            print("❌ MESSAGING TEST FAILED - Bot cannot send messages")
            return False

    except discord.LoginFailure:
        print("❌ Invalid Discord token")
        return False
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_discord_messaging())
    exit(0 if success else 1)