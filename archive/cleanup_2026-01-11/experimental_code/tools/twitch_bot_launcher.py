#!/usr/bin/env python3
"""
Twitch Bot Launcher - Agent Cellphone V2
========================================

SSOT Domain: chat_presence

Simple launcher script to start the Twitch bot and manage PID files.

Features:
- Starts Twitch bot in background
- Creates PID file for process tracking
- Ensures proper logging setup
- Validates environment before launch

Author: Agent-2 (Architecture & Integration Specialist)
Date: 2026-01-08
"""

import os
import subprocess
import sys
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    # Load from repo root
    repo_root = Path(__file__).resolve().parents[1]
    load_dotenv(dotenv_path=repo_root / ".env")
    print("✅ Loaded environment variables from .env")
except ImportError:
    print("⚠️  python-dotenv not installed. Using existing environment variables.")

def create_pid_file(pid: int) -> None:
    """Create the twitch_bot.pid file with the process ID."""
    pid_dir = Path("pids")
    pid_dir.mkdir(exist_ok=True)
    pid_file = pid_dir / "twitch_bot.pid"

    with open(pid_file, 'w') as f:
        f.write(str(pid))

    print(f"✅ Created twitch_bot.pid with PID: {pid}")

def validate_environment() -> bool:
    """Validate that required Twitch environment variables are set."""
    required_vars = ['TWITCH_ACCESS_TOKEN', 'TWITCH_CHANNEL']

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        return False

    print("✅ Twitch environment validation passed")
    return True

def main():
    """Launch the Twitch bot."""
    print("🎮 Starting Twitch Bot Launcher...")

    # Validate environment
    if not validate_environment():
        sys.exit(1)

    # Ensure runtime/logs directory exists
    log_dir = Path("runtime/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ Log directory ready: {log_dir}")

    try:
        # Start the Twitch bot in background
        print("🚀 Launching Twitch bot...")

        # Use subprocess to run the Twitch eventsub server in background
        process = subprocess.Popen(
            [sys.executable, "-m", "src.services.chat_presence.twitch_eventsub_server"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=Path.cwd()
        )

        # Create PID file
        create_pid_file(process.pid)

        print("✅ Twitch bot launched successfully!")
        print(f"📝 Process ID: {process.pid}")
        print(f"📝 Logs: {log_dir}/twitch_bot_*.log")
        print(f"📝 PID file: pids/twitch_bot.pid")

        return 0

    except Exception as e:
        print(f"❌ Failed to launch Twitch bot: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())