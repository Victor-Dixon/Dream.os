#!/usr/bin/env python3
"""
Twitch EventSub Launcher - Agent Cellphone V2
=============================================

Simple launcher script to start the Twitch EventSub webhook server and manage PID files.

Features:
- Starts Twitch EventSub server in background
- Creates PID file for process tracking
- Ensures proper logging setup
- Validates environment before launch

Author: Agent-2 (Architecture & Integration Specialist)
Date: 2026-01-09
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
    """Create the twitch_eventsub.pid file with the process ID."""
    pid_dir = Path("pids")
    pid_dir.mkdir(exist_ok=True)
    pid_file = pid_dir / "twitch_eventsub.pid"

    with open(pid_file, 'w') as f:
        f.write(str(pid))

    print(f"✅ Created twitch_eventsub.pid with PID: {pid}")

def validate_environment() -> bool:
    """Validate that required Twitch environment variables are set."""
    # For development/testing, use default values if not set
    if not os.getenv('TWITCH_EVENTSUB_WEBHOOK_SECRET'):
        os.environ['TWITCH_EVENTSUB_WEBHOOK_SECRET'] = 'dev-webhook-secret-12345'
        print("⚠️ Using default development webhook secret")

    print("✅ Twitch EventSub environment validation passed")
    return True

def main():
    """Launch the Twitch EventSub server."""
    print("🎮 Starting Twitch EventSub Launcher...")

    # Validate environment
    if not validate_environment():
        sys.exit(1)

    # Ensure runtime/logs directory exists
    log_dir = Path("runtime/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ Log directory ready: {log_dir}")

    try:
        # Start the Twitch EventSub server in background
        print("🚀 Launching Twitch EventSub webhook server...")

        # Use subprocess to run the server in background
        env = os.environ.copy()
        env['PYTHONPATH'] = str(Path.cwd())

        # Launch as detached process so it doesn't depend on parent
        if os.name == 'nt':  # Windows
            process = subprocess.Popen(
                [sys.executable, "-m", "src.services.chat_presence.twitch_eventsub_server"],
                env=env,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                cwd=Path.cwd(),
                creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
            )
        else:  # Unix-like systems
            process = subprocess.Popen(
                [sys.executable, "-m", "src.services.chat_presence.twitch_eventsub_server"],
                env=env,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                cwd=Path.cwd(),
                start_new_session=True
            )

        # Create PID file
        create_pid_file(process.pid)

        print("✅ Twitch EventSub server launched successfully!")
        print(f"📝 Process ID: {process.pid}")
        print(f"📝 Logs: {log_dir}/twitch_eventsub_*.log")
        print(f"📝 PID file: pids/twitch_eventsub.pid")
        print("🌐 Server should be available at http://localhost:5000")

        return 0

    except Exception as e:
        print(f"❌ Failed to launch Twitch EventSub server: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())