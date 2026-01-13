#!/usr/bin/env python3
"""
Core Services Launcher - Agent Cellphone V2
==========================================

Minimal launcher for the essential messaging services.
Bypasses all the broken launcher infrastructure and starts services directly.

Services Started:
- Message Queue Processor (handles agent-to-agent messaging)
- Discord Commander (optional - start separately if needed)

Usage:
  python start_core_services.py          # Start message queue only
  python start_core_services.py --discord # Start message queue + Discord

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-09
"""

import argparse
import asyncio
import subprocess
import sys
import time
from pathlib import Path

def start_message_queue():
    """Start the message queue processor."""
    print("📨 Starting Message Queue Processor...")

    try:
        # Start message queue directly
        from tools.utilities.start_message_queue import main
        # Run in background process
        proc = subprocess.Popen([
            sys.executable, "-c",
            "from tools.utilities.start_message_queue import main; main()"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        print(f"✅ Message Queue started (PID: {proc.pid})")
        return True

    except Exception as e:
        print(f"❌ Failed to start Message Queue: {e}")
        return False

async def start_discord_bot():
    """Start the Discord bot."""
    print("🤖 Starting Discord Bot...")

    try:
        # Start Discord bot directly
        from src.discord_commander.bot_runner_v2 import main
        # This will run indefinitely
        await main()
        return True

    except Exception as e:
        print(f"❌ Failed to start Discord Bot: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Start core messaging services")
    parser.add_argument('--discord', action='store_true',
                       help='Also start Discord bot (runs indefinitely)')
    args = parser.parse_args()

    print("🚀 Agent Cellphone V2 - Core Services Launcher")
    print("=" * 50)

    # Start message queue (always)
    mq_started = start_message_queue()

    if not mq_started:
        print("❌ Core services failed to start")
        sys.exit(1)

    # Start Discord if requested
    if args.discord:
        print("\n🤖 Starting Discord Commander...")
        print("Note: Discord bot will run indefinitely. Use Ctrl+C to stop.")
        try:
            asyncio.run(start_discord_bot())
        except KeyboardInterrupt:
            print("\n🛑 Discord bot stopped")
    else:
        print("\n💡 Message queue is running in background")
        print("   To start Discord bot: python start_core_services.py --discord")
        print("   To check status: python main.py --status")

    print("\n✅ Core services operational!")

if __name__ == "__main__":
    main()