#!/usr/bin/env python3
"""
Discord Bot Health Check Utility
=================================

Quick utility to verify Discord bot process status and configuration.
Checks for running process, PID file, and environment configuration.

Usage:
    python tools/discord_bot_health_check.py
"""

import os
import sys
from pathlib import Path

def check_bot_process():
    """Check if Discord bot process is running."""
    pid_file = Path("discord.pid")
    if pid_file.exists():
        try:
            pid = int(pid_file.read_text().strip())
            # Check if process exists (Windows-compatible check)
            if sys.platform == "win32":
                import subprocess
                result = subprocess.run(
                    ["tasklist", "/FI", f"PID eq {pid}"],
                    capture_output=True,
                    text=True
                )
                return "python" in result.stdout.lower()
            else:
                os.kill(pid, 0)  # Signal 0 just checks if process exists
                return True
        except (ValueError, OSError, ProcessLookupError):
            return False
    return False

def check_env_config():
    """Check if DISCORD_BOT_TOKEN is configured."""
    env_file = Path(".env")
    if not env_file.exists():
        return False, "❌ .env file not found"
    
    try:
        content = env_file.read_text()
        if "DISCORD_BOT_TOKEN" in content:
            # Check if token is not empty
            for line in content.split("\n"):
                if line.startswith("DISCORD_BOT_TOKEN="):
                    token = line.split("=", 1)[1].strip()
                    if token and token != "":
                        return True, "✅ DISCORD_BOT_TOKEN configured"
            return False, "⚠️ DISCORD_BOT_TOKEN is empty"
        return False, "❌ DISCORD_BOT_TOKEN not found in .env"
    except Exception as e:
        return False, f"❌ Error reading .env: {e}"

def main():
    """Run health check."""
    print("🔍 Discord Bot Health Check\n")
    
    # Check process
    process_running = check_bot_process()
    print(f"Process Status: {'✅ Running' if process_running else '❌ Not running'}")
    
    # Check environment
    env_ok, env_msg = check_env_config()
    print(f"Environment: {env_msg}")
    
    # Summary
    if process_running and env_ok:
        print("\n✅ Bot is healthy")
        return 0
    else:
        print("\n⚠️ Bot health issues detected")
        return 1

if __name__ == "__main__":
    sys.exit(main())

