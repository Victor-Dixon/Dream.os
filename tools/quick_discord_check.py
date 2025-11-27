#!/usr/bin/env python3
"""
Quick Discord Bot Status Check
==============================
Quick check to see if Discord bot is working.
"""

import os
import sys
from pathlib import Path

# Load .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

print("\n" + "="*70)
print("🔍 QUICK DISCORD BOT CHECK")
print("="*70 + "\n")

# Check token
token = os.getenv("DISCORD_BOT_TOKEN")
if token:
    print(f"✅ Token: SET (length: {len(token)})")
else:
    print("❌ Token: NOT SET")
    print("   Fix: Add DISCORD_BOT_TOKEN to .env file")
    sys.exit(1)

# Check discord.py
try:
    import discord
    print(f"✅ discord.py: INSTALLED (v{discord.__version__})")
except ImportError:
    print("❌ discord.py: NOT INSTALLED")
    print("   Fix: pip install discord.py")
    sys.exit(1)

# Check if bot script exists
bot_script = Path("scripts/run_unified_discord_bot_with_restart.py")
if bot_script.exists():
    print(f"✅ Bot script: EXISTS")
else:
    print(f"❌ Bot script: NOT FOUND")
    sys.exit(1)

# Check processes
try:
    import subprocess
    result = subprocess.run(
        ["powershell", "-Command", "Get-Process python | Where-Object {$_.CommandLine -like '*discord*'} | Measure-Object"],
        capture_output=True,
        text=True,
        timeout=5
    )
    if "Count" in result.stdout:
        print("✅ Bot process: CHECKING...")
    else:
        print("⚠️  Bot process: NOT DETECTED (may still be running)")
except:
    print("⚠️  Bot process: CANNOT CHECK")

print("\n" + "="*70)
print("💡 TO START BOT:")
print("   python tools/start_discord_system.py")
print("="*70 + "\n")

print("💡 TO TEST BOT:")
print("   1. Make sure bot is running")
print("   2. Go to Discord")
print("   3. Type: !status")
print("   4. Bot should respond")
print("\n")

