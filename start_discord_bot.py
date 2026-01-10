#!/usr/bin/env python3
"""
Direct Discord Bot Launcher - Agent Cellphone V2
===============================================

Simple, direct launcher for the Discord bot that bypasses all the broken launcher infrastructure.

Features:
- Starts Discord bot directly using bot_runner_v2.py
- No complex PID management or broken paths
- Simple and reliable startup

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-09
"""

import asyncio
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

async def start_discord_bot():
    """Start the Discord bot directly."""
    try:
        print("🤖 Starting Discord Bot (Direct)...")
        print("=" * 50)

        # Import and run the bot
        from discord_commander.bot_runner_v2 import main

        # Run the bot
        exit_code = await main()
        return exit_code

    except KeyboardInterrupt:
        print("\n🛑 Discord bot stopped by user")
        return 0
    except Exception as e:
        print(f"❌ Discord bot failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    # Run the bot
    exit_code = asyncio.run(start_discord_bot())
    sys.exit(exit_code)