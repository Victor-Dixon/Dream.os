#!/usr/bin/env python3
"""
Twitch EventSub Server Launcher Script
======================================

Launcher for Twitch EventSub webhook server that runs as a background daemon.
"""

import os
import subprocess
import sys
from pathlib import Path

def create_pid_file(pid: int) -> None:
    """Create the twitch.pid file with the process ID."""
    pid_dir = Path("pids")
    pid_dir.mkdir(exist_ok=True)
    pid_file = pid_dir / "twitch.pid"

    with open(pid_file, 'w') as f:
        f.write(str(pid))

    print(f"✅ Created twitch.pid with PID: {pid}")

def main():
    """Launch the Twitch EventSub server as a background daemon."""
    print("📺 Starting Twitch EventSub Server Launcher...")

    try:
        # Set up environment
        env = os.environ.copy()
        env['PYTHONPATH'] = str(Path.cwd())

        # Launch the Twitch server in background
        print("🚀 Launching Twitch EventSub server daemon...")

        process = subprocess.Popen(
            [sys.executable, "-m", "src.services.chat_presence.twitch_eventsub_server"],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=Path.cwd()
        )

        # Create PID file
        create_pid_file(process.pid)

        print("✅ Twitch EventSub server daemon launched successfully!")
        print(f"📝 Process ID: {process.pid}")
        print(f"📝 PID file: pids/twitch.pid")

        return 0

    except Exception as e:
        print(f"❌ Failed to launch Twitch EventSub server: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())