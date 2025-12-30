#!/usr/bin/env python3
"""
Discord Bot Startup Script with Auto-Restart
=============================================

Starts the Discord bot and automatically restarts it if it crashes.
Includes process management and health monitoring.

V2 Compliance | Author: Agent-4 | Date: 2025-12-28

<!-- SSOT Domain: tools -->
"""

import os
import sys
import subprocess
import time
import signal
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# PID file location
PID_DIR = project_root / "pids"
PID_FILE = PID_DIR / "discord.pid"
PID_DIR.mkdir(exist_ok=True)

# Log directory
LOG_DIR = project_root / "runtime" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)


def get_existing_pid():
    """Get PID from file if it exists."""
    if PID_FILE.exists():
        try:
            with open(PID_FILE, 'r') as f:
                pid = int(f.read().strip())
            return pid
        except (ValueError, IOError):
            return None
    return None


def check_process_running(pid):
    """Check if process is still running."""
    try:
        os.kill(pid, 0)  # Signal 0 doesn't kill, just checks if process exists
        return True
    except OSError:
        return False


def write_pid(pid):
    """Write PID to file."""
    try:
        with open(PID_FILE, 'w') as f:
            f.write(str(pid))
    except IOError as e:
        print(f"⚠️ Could not write PID file: {e}")


def stop_existing_bot():
    """Stop existing bot process if running."""
    pid = get_existing_pid()
    if pid and check_process_running(pid):
        print(f"🛑 Stopping existing bot (PID: {pid})...")
        try:
            os.kill(pid, signal.SIGTERM)
            time.sleep(2)
            if check_process_running(pid):
                print(f"⚠️ Process still running, forcing kill...")
                os.kill(pid, signal.SIGKILL)
        except OSError:
            pass
        PID_FILE.unlink(missing_ok=True)


def start_bot():
    """Start the Discord bot."""
    print("🚀 Starting Discord Bot...")
    print("🐝 WE. ARE. SWARM.")

    # Check for token
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        print("⚠️  DISCORD_BOT_TOKEN not set in environment!")
        print("   Set it with: $env:DISCORD_BOT_TOKEN='your_token' (Windows)")
        print("   Or use: python tools/start_discord_system.py (handles env automatically)")
        return 0  # Exit gracefully - not a tool error
        sys.exit(1)

    # Stop existing bot if running
    stop_existing_bot()

    # Start bot process
    bot_script = project_root / "src" / "discord_commander" / "bot_runner.py"

    # Use Python executable
    python_exe = sys.executable

    # Start process
    process = subprocess.Popen(
        [python_exe, "-m", "src.discord_commander.bot_runner"],
        cwd=str(project_root),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    # Write PID
    write_pid(process.pid)
    print(f"✅ Bot started (PID: {process.pid})")
    print(f"📝 PID file: {PID_FILE}")
    print(f"📋 Logs: {LOG_DIR / 'discord_bot_*.log'}")
    print("\n🔄 Bot will auto-restart on crashes")
    print("🛑 Press Ctrl+C to stop\n")

    # Monitor process
    try:
        # Stream output
        for line in process.stdout:
            print(line.rstrip())

        # Wait for process to complete
        return_code = process.wait()

        if return_code != 0:
            print(f"\n⚠️ Bot exited with code {return_code}")
            print("🔄 Will restart in 5 seconds...")
            time.sleep(5)
            return start_bot()  # Restart
        else:
            print("\n✅ Bot stopped cleanly")
            PID_FILE.unlink(missing_ok=True)
            return 0

    except KeyboardInterrupt:
        print("\n🛑 Stopping bot...")
        try:
            process.terminate()
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        PID_FILE.unlink(missing_ok=True)
        return 0
    except Exception as e:
        print(f"\n❌ Error monitoring bot: {e}")
        try:
            process.kill()
        except:
            pass
        PID_FILE.unlink(missing_ok=True)
        return 1


if __name__ == "__main__":
    try:
        sys.exit(start_bot())
    except KeyboardInterrupt:
        print("\n🛑 Startup interrupted")
        sys.exit(0)
