#!/usr/bin/env python3
"""
Discord Bot Status Verification Tool
====================================

Verifies Discord bot is running and functional.

Author: Agent-7 (Web Development Specialist)
"""

import sys
import os
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    print("❌ discord.py not installed")
    sys.exit(1)

async def check_bot_connection(token: str):
    """Check if bot can connect to Discord."""
    print("=" * 60)
    print("🔍 Testing Discord Bot Connection")
    print("=" * 60)
    print()
    
    try:
        # Create a simple bot client to test connection
        intents = discord.Intents.default()
        intents.message_content = True
        
        client = discord.Client(intents=intents)
        
        @client.event
        async def on_ready():
            print(f"✅ Bot connected successfully!")
            print(f"   Bot Name: {client.user.name}")
            print(f"   Bot ID: {client.user.id}")
            print(f"   Guilds: {len(client.guilds)}")
            print()
            await client.close()
        
        @client.event
        async def on_error(event, *args, **kwargs):
            print(f"⚠️  Error in {event}: {args}")
        
        print("📡 Attempting to connect to Discord...")
        await client.start(token)
        
        return True
        
    except discord.LoginFailure:
        print("❌ Invalid Discord token")
        return False
    except discord.PrivilegedIntentsRequired as e:
        print(f"❌ Missing required intents: {e}")
        return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def check_bot_process():
    """Check if bot process is running."""
    print("=" * 60)
    print("🔍 Checking Bot Process")
    print("=" * 60)
    print()
    
    import psutil
    
    bot_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info.get('cmdline', [])
            if cmdline and any('unified_discord_bot' in str(arg) for arg in cmdline):
                bot_processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    if bot_processes:
        print(f"✅ Found {len(bot_processes)} bot process(es):")
        for proc in bot_processes:
            print(f"   PID: {proc['pid']}, Name: {proc['name']}")
        return True
    else:
        print("⚠️  No bot process found running")
        print("   Bot may not be started or may have crashed")
        return False

def main():
    """Main verification function."""
    print("=" * 60)
    print("🐛 Discord Bot Status Verification")
    print("=" * 60)
    print()
    
    # Load environment
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except:
        pass
    
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        print("❌ DISCORD_BOT_TOKEN not set")
        return 1
    
    # Check process
    try:
        import psutil
        process_running = check_bot_process()
    except ImportError:
        print("⚠️  psutil not installed - skipping process check")
        print("   Install with: pip install psutil")
        process_running = None
        print()
    
    # Test connection
    print()
    connection_ok = asyncio.run(check_bot_connection(token))
    
    # Summary
    print("=" * 60)
    print("📊 Verification Summary")
    print("=" * 60)
    print()
    
    if process_running is not None:
        print(f"Process Running: {'✅ YES' if process_running else '❌ NO'}")
    print(f"Connection Test: {'✅ PASS' if connection_ok else '❌ FAIL'}")
    print()
    
    if connection_ok:
        print("✅ Bot can connect to Discord successfully!")
        if process_running:
            print("✅ Bot process is running")
            print()
            print("🎯 Bot Status: OPERATIONAL")
        else:
            print("⚠️  Bot process not found, but connection test passed")
            print("   Bot may need to be started")
            print()
            print("💡 Start bot with: python tools/run_unified_discord_bot_with_restart.py")
        return 0
    else:
        print("❌ Bot connection test failed")
        print("   Check token and intents configuration")
        return 1

if __name__ == "__main__":
    sys.exit(main())

