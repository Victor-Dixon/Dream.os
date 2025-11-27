#!/usr/bin/env python3
"""
Quick Twitch Bot Setup Script
==============================

Interactive setup to get your Twitch bot running RIGHT NOW.

Usage:
    python tools/setup_twitch_bot_now.py
"""

import json
import os
from pathlib import Path

def main():
    print("=" * 60)
    print("🚀 QUICK TWITCH BOT SETUP")
    print("=" * 60)
    print()
    
    print("Step 1: Get OAuth Token")
    print("-" * 60)
    print("1. Open: https://twitchapps.com/tmi/")
    print("2. Click 'Connect with Twitch'")
    print("3. Authorize and copy your OAuth token")
    print()
    
    oauth_token = input("Paste your OAuth token here (starts with oauth:): ").strip()
    if not oauth_token.startswith("oauth:"):
        print("⚠️ Warning: Token should start with 'oauth:'")
        confirm = input("Continue anyway? (y/n): ")
        if confirm.lower() != 'y':
            return
    
    print()
    print("Step 2: Bot Configuration")
    print("-" * 60)
    username = input("Enter your Twitch username (bot account or yours): ").strip().lower()
    channel = input("Enter your channel name (without #): ").strip().lower()
    
    if not username or not channel:
        print("❌ Username and channel are required!")
        return
    
    print()
    print("Step 3: Creating Config File")
    print("-" * 60)
    
    config = {
        "twitch": {
            "username": username,
            "oauth_token": oauth_token,
            "channel": channel
        }
    }
    
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)
    config_file = config_dir / "chat_presence.json"
    
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Config file created: {config_file}")
    print()
    
    print("Step 4: Install Dependencies")
    print("-" * 60)
    print("Checking dependencies...")
    
    try:
        import websockets
        import irc
        print("✅ All dependencies installed!")
    except ImportError:
        print("⚠️ Missing dependencies. Installing...")
        os.system("pip install websockets irc")
        print("✅ Dependencies installed!")
    
    print()
    print("=" * 60)
    print("✅ SETUP COMPLETE!")
    print("=" * 60)
    print()
    print("To start the bot, run:")
    print(f"  python tools/chat_presence_cli.py --twitch-only")
    print()
    print("The bot will connect to your channel automatically!")
    print()
    print("Test commands in chat:")
    print("  !agent7 hello")
    print("  !team status")
    print("  !swarm hello")
    print()

if __name__ == "__main__":
    main()

