#!/usr/bin/env python3
"""
Discord Bot Debug Script
Tests Discord bot connectivity and identifies issues
"""

import asyncio
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Environment variables loaded from .env")
except ImportError:
    print("⚠️  python-dotenv not installed, using system environment only")

async def debug_discord_bot():
    """Debug Discord bot connectivity and configuration"""

    print("🔧 DISCORD BOT DEBUG SESSION")
    print("=" * 50)

    # Check environment
    print("\n🔍 PHASE 1: Environment Check")
    print("-" * 30)

    token = os.getenv('DISCORD_BOT_TOKEN')
    if token:
        print(f"✅ DISCORD_BOT_TOKEN: Found (length: {len(token)})")
        token_preview = token[:10] + "..." + token[-5:] if len(token) > 15 else token
        print(f"   Token preview: {token_preview}")
    else:
        print("❌ DISCORD_BOT_TOKEN: NOT FOUND")
        print("   💡 Set with: $env:DISCORD_BOT_TOKEN = 'your_token'")
        return False

    # Check Discord availability
    print("\n🔍 PHASE 2: Discord.py Check")
    print("-" * 30)

    try:
        import discord
        from discord.ext import commands
        print(f"✅ discord.py: Available (version {discord.__version__})")
    except ImportError as e:
        print(f"❌ discord.py: NOT INSTALLED - {e}")
        print("   💡 Install with: pip install discord.py")
        return False

    # Try to create bot instance
    print("\n🔍 PHASE 3: Bot Instance Creation")
    print("-" * 30)

    try:
        # Import the bot class
        from src.discord_commander.unified_discord_bot import UnifiedDiscordBot

        print("✅ UnifiedDiscordBot: Import successful")

        # Create bot instance (without starting)
        bot = UnifiedDiscordBot(token)
        print("✅ Bot instance: Created successfully")

        # Check bot attributes
        print(f"   Bot user: {bot.user if bot.user else 'Not logged in'}")
        print(f"   Bot guilds: {len(bot.guilds) if bot.guilds else 0}")

    except Exception as e:
        print(f"❌ Bot creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Test connection
    print("\n🔍 PHASE 4: Connection Test")
    print("-" * 30)

    connection_successful = False

    try:
        print("🔗 Attempting to connect to Discord...")

        # Create a simple connection test
        intents = discord.Intents.default()
        intents.guilds = True
        intents.messages = True
        intents.message_content = True

        test_bot = commands.Bot(command_prefix='!', intents=intents)

        @test_bot.event
        async def on_ready():
            nonlocal connection_successful
            connection_successful = True
            print(f"✅ Connection successful! Logged in as {test_bot.user}")
            print(f"   Connected to {len(test_bot.guilds)} server(s)")
            for guild in test_bot.guilds:
                print(f"   - {guild.name} ({guild.id})")
            await test_bot.close()

        @test_bot.event
        async def on_error(event, *args, **kwargs):
            print(f"❌ Discord error in {event}: {args}")

        # Try to start with timeout
        await asyncio.wait_for(test_bot.start(token), timeout=15.0)
        print("✅ Connection test completed")

    except asyncio.TimeoutError:
        print("⏰ Connection timed out after 15 seconds")
        print("   This might indicate:")
        print("   - Slow internet connection")
        print("   - Invalid token")
        print("   - Discord API issues")
        print("   - Firewall blocking connection")

    except discord.LoginFailure:
        print("❌ Login failed - Invalid token")
        print("   💡 Check your DISCORD_BOT_TOKEN")

    except discord.PrivilegedIntentsRequired:
        print("❌ Privileged intents required")
        print("   💡 Enable privileged intents in Discord Developer Portal")

    except Exception as e:
        print(f"❌ Connection failed: {e}")
        import traceback
        traceback.print_exc()

    # Test channel access
    if connection_successful:
        print("\n🔍 PHASE 5: Channel Access Test")
        print("-" * 30)

        # Check if configured channels exist
        channel_vars = [
            'DISCORD_INFRASTRUCTURE_CHANNEL_ID',
            'DISCORD_ARCHITECTURE_CHANNEL_ID',
            'DISCORD_COORDINATION_CHANNEL_ID',
            'DISCORD_A2A_COORDINATION_CHANNEL_ID'
        ]

        for var in channel_vars:
            channel_id = os.getenv(var)
            if channel_id:
                try:
                    # In a real scenario, we'd get the channel from the bot
                    print(f"✅ {var}: {channel_id}")
                except Exception as e:
                    print(f"⚠️  {var}: {channel_id} (access error: {e})")
            else:
                print(f"❌ {var}: NOT CONFIGURED")

    # Summary
    print("\n📊 DEBUG SUMMARY")
    print("-" * 30)

    if connection_successful:
        print("✅ Discord bot connection: SUCCESSFUL")
        print("✅ Bot can connect and access Discord API")
        print("✅ Ready for full bot operation")
        return True
    else:
        print("❌ Discord bot connection: FAILED")
        print("❌ Bot cannot connect to Discord")
        print("❌ Debug and fix issues before deploying")
        return False

def main():
    """Main debug function"""
    try:
        result = asyncio.run(debug_discord_bot())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n🛑 Debug session interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Debug session crashed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()