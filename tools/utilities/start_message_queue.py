#!/usr/bin/env python3
"""
Message Queue Service Launcher
===============================

Launcher script for the message queue processor that runs as a background daemon.
"""

import os
import subprocess
import sys
from pathlib import Path

def create_pid_file(pid: int) -> None:
    """Create the message_queue.pid file with the process ID."""
    pid_dir = Path("pids")
    pid_dir.mkdir(exist_ok=True)
    pid_file = pid_dir / "message_queue.pid"

    with open(pid_file, 'w') as f:
        f.write(str(pid))

    print(f"✅ Created message_queue.pid with PID: {pid}")

def main():
    """Launch the message queue processor as a background daemon."""
    print("📨 Starting Message Queue Service Launcher...")

    try:
        # Set up environment
        env = os.environ.copy()
        env['PYTHONPATH'] = str(Path.cwd())

        # Launch the message queue processor in background
        print("🚀 Launching message queue processor daemon...")

        process = subprocess.Popen(
            [sys.executable, "-m", "src.core.message_queue_processor.core.processor"],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=Path.cwd()
        )

        # Create PID file
        create_pid_file(process.pid)

        print("✅ Message queue processor daemon launched successfully!")
        print(f"📝 Process ID: {process.pid}")
        print(f"📝 PID file: pids/message_queue.pid")

        return 0

    except Exception as e:
        print(f"❌ Failed to launch message queue processor: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())