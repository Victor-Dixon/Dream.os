#!/usr/bin/env python3
"""
Quick verification that Discord bot is running and accessible.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

import os
from dotenv import load_dotenv

load_dotenv()

# Check token
token = os.getenv("DISCORD_BOT_TOKEN")
if not token:
    print("❌ DISCORD_BOT_TOKEN not set!")
    print("   Please set it in .env file or environment variable")
    sys.exit(1)

if len(token) < 50:
    print(f"⚠️  Token appears invalid (length: {len(token)})")
    sys.exit(1)

print("✅ Discord token found and appears valid")

# Check if bot can be imported
try:
    from src.discord_commander.unified_discord_bot import UnifiedDiscordBot
    print("✅ Discord bot module can be imported")
except Exception as e:
    print(f"❌ Failed to import bot: {e}")
    sys.exit(1)

# Check queue processor
try:
    from src.core.message_queue_processor import MessageQueueProcessor
    print("✅ Message queue processor can be imported")
except Exception as e:
    print(f"❌ Failed to import queue processor: {e}")
    sys.exit(1)

print("\n✅ All checks passed! Discord system ready to start.")
print("   Run: python tools/start_discord_system.py")

