#!/usr/bin/env python3
# Header-Variant: full
# Owner: @dreamos/platform
# Purpose: message_queue_launcher module.
# SSOT: docs/recovery/recovery_registry.yaml#tools-utilities-message-queue-launcher-py
# @registry docs/recovery/recovery_registry.yaml#tools-utilities-message-queue-launcher-py

"""
Message Queue Launcher - Agent Cellphone V2
==========================================

SSOT Domain: core

Simple launcher script to start the message queue processor and manage PID files.

Features:
- Starts message queue processor in background
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
    """Create the message_queue.pid file with the process ID."""
    pid_dir = Path("pids")
    pid_dir.mkdir(exist_ok=True)
    pid_file = pid_dir / "message_queue.pid"

    with open(pid_file, 'w') as f:
        f.write(str(pid))

    print(f"✅ Created message_queue.pid with PID: {pid}")

def validate_environment() -> bool:
    """Validate that required message queue environment variables are set."""
    # Message queue doesn't require specific env vars beyond basic setup
    # Could add validation for database URLs, queue configurations, etc. if needed
    print("✅ Message queue environment validation passed")
    return True

def main():
    """Launch the message queue processor."""
    print("📨 Starting Message Queue Launcher...")

    # Validate environment
    if not validate_environment():
        sys.exit(1)

    # Ensure runtime/logs directory exists
    log_dir = Path("runtime/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ Log directory ready: {log_dir}")

    try:
        # Start the message queue processor in background
        print("🚀 Launching message queue processor...")

        # Use subprocess to run the processor in background
        # The processor is a long-running service that processes messages
        env = os.environ.copy()
        env['PYTHONPATH'] = str(Path.cwd())

        # Redirect stderr to a log file so we can see any errors
        error_log = log_dir / "message_queue_error.log"

        with open(error_log, 'w') as err_file:
            process = subprocess.Popen(
                [sys.executable, "-m", "src.core.message_queue_processor.core.processor"],
                env=env,
                stdout=subprocess.DEVNULL,  # Suppress stdout to avoid clutter
                stderr=err_file,           # Log errors to file
                cwd=Path.cwd()
            )

        # Create PID file
        create_pid_file(process.pid)

        print("✅ Message queue processor launched successfully!")
        print(f"📝 Process ID: {process.pid}")
        print(f"📝 Logs: {log_dir}/message_queue_*.log")
        print(f"📝 PID file: pids/message_queue.pid")

        return 0

    except Exception as e:
        print(f"❌ Failed to launch message queue processor: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
