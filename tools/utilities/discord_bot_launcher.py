<<<<<<< HEAD
#!/usr/bin/env python3
"""
Discord Bot Launcher - Agent Cellphone V2
=========================================

SSOT Domain: discord

Simple launcher script to start the Discord bot and manage PID files.

USAGE:
    python tools/discord_bot_launcher.py    # Start the bot
    python check_discord_bot.py             # Check if bot is running
    python tools/discord_bot_launcher.py stop  # Stop the bot (future feature)

REQUIRED ENVIRONMENT VARIABLES:
    DISCORD_BOT_TOKEN - Your Discord bot token from https://discord.com/developers/applications
    DISCORD_GUILD_ID - Your Discord server ID

SETUP:
    1. Copy env.example to .env
    2. Add your DISCORD_BOT_TOKEN and DISCORD_GUILD_ID to .env
    3. Run: python tools/discord_bot_launcher.py

Features:
- Starts Discord bot in background
- Creates PID file for process tracking
- Ensures proper logging setup
- Validates environment before launch

Author: Agent-6 (Coordination & Communication Specialist)
Date: 2026-01-08
"""

import asyncio
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
    """Create the discord.pid file with the process ID."""
    pid_dir = Path("pids")
    pid_dir.mkdir(exist_ok=True)
    pid_file = pid_dir / "discord.pid"

    with open(pid_file, 'w') as f:
        f.write(str(pid))

    print(f"✅ Created discord.pid with PID: {pid}")

def validate_environment() -> bool:
    """Validate that required Discord environment variables are set."""
    required_vars = ['DISCORD_BOT_TOKEN', 'DISCORD_GUILD_ID']

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        return False

    print("✅ Environment validation passed")
    return True

def main():
    """Launch the Discord bot."""
    print("🤖 Starting Discord Bot Launcher...")

    # Validate environment
    if not validate_environment():
        sys.exit(1)

    # Ensure runtime/logs directory exists
    log_dir = Path("runtime/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ Log directory ready: {log_dir}")

    try:
        # Start the bot runner in background
        print("🚀 Launching Discord bot...")

        # Use subprocess to run the bot in background
        process = subprocess.Popen(
            [sys.executable, "-m", "src.discord_commander.unified_discord_bot"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=Path.cwd()
        )

        # Create PID file
        create_pid_file(process.pid)

        print("✅ Discord bot launched successfully!")
        print(f"📝 Process ID: {process.pid}")
        print(f"📝 Logs: {log_dir}/discord_bot_*.log")
        print(f"📝 PID file: pids/discord.pid")

        return 0

    except Exception as e:
        print(f"❌ Failed to launch Discord bot: {e}")
        return 1

if __name__ == "__main__":
=======
#!/usr/bin/env python3
"""
Discord Bot Launcher - Agent Cellphone V2
=========================================

SSOT Domain: discord

Simple launcher script to start the Discord bot and manage PID files.

Features:
- Starts Discord bot in background
- Creates PID file for process tracking
- Ensures proper logging setup
- Validates environment before launch

Author: Agent-6 (Coordination & Communication Specialist)
Date: 2026-01-08
"""

import asyncio
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
    """Create the discord.pid file with the process ID."""
    pid_dir = Path("pids")
    pid_dir.mkdir(exist_ok=True)
    pid_file = pid_dir / "discord.pid"

    with open(pid_file, 'w') as f:
        f.write(str(pid))

    print(f"✅ Created discord.pid with PID: {pid}")

def validate_environment() -> bool:
    """Validate that required Discord environment variables are set."""
    required_vars = ['DISCORD_BOT_TOKEN', 'DISCORD_GUILD_ID']

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        return False

    print("✅ Environment validation passed")
    return True

def main():
    """Launch the Discord bot."""
    print("🤖 Starting Discord Bot Launcher...")

    # Validate environment
    if not validate_environment():
        sys.exit(1)

    # Ensure runtime/logs directory exists
    log_dir = Path("runtime/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ Log directory ready: {log_dir}")

    try:
        # Start the bot runner in background
        print("🚀 Launching Discord bot...")

        # Use subprocess to run the bot in background
        process = subprocess.Popen(
            [sys.executable, "-m", "src.discord_commander.bot_runner_v2"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=Path.cwd()
        )

        # Create PID file
        create_pid_file(process.pid)

        print("✅ Discord bot launched successfully!")
        print(f"📝 Process ID: {process.pid}")
        print(f"📝 Logs: {log_dir}/discord_bot_*.log")
        print(f"📝 PID file: pids/discord.pid")

        return 0

    except Exception as e:
        print(f"❌ Failed to launch Discord bot: {e}")
        return 1

if __name__ == "__main__":
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
    sys.exit(main())