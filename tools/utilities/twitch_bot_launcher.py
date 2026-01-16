#!/usr/bin/env python3
"""
DEPRECATED: Twitch Bot Launcher - Agent Cellphone V2
====================================================

⚠️  THIS LAUNCHER HAS BEEN DEPRECATED ⚠️

This launcher has been consolidated into the single source of truth:
    scripts/start_twitch.py

Please use the consolidated launcher instead:
    python scripts/start_twitch.py

Old functionality:
- Started Twitch bot in background
- Created PID file for process tracking
- Ensured proper logging setup
- Validated environment before launch

Author: Agent-2 (Architecture & Integration Specialist)
Date: 2026-01-08
Deprecated: 2026-01-15 (Consolidated into scripts/start_twitch.py)
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
    """DEPRECATED: Redirect to consolidated launcher."""
    print("⚠️  DEPRECATED LAUNCHER DETECTED ⚠️")
    print("=" * 50)
    print("This Twitch bot launcher has been DEPRECATED.")
    print()
    print("🎯 Please use the consolidated launcher instead:")
    print("   python scripts/start_twitch.py")
    print()
    print("This ensures:")
    print("   • Single source of truth for Twitch launching")
    print("   • Correct PID file management (twitch_bot.pid)")
    print("   • Service manager compatibility")
    print("   • Consolidated features from all launchers")
    print()
    print("🚀 Redirecting to consolidated launcher...")

    # Import and run the consolidated launcher
    try:
        import subprocess
        import sys
        from pathlib import Path

        # Get the path to the consolidated launcher
        consolidated_launcher = Path(__file__).resolve().parents[2] / "scripts" / "start_twitch.py"

        # Run the consolidated launcher with same arguments
        result = subprocess.run([sys.executable, str(consolidated_launcher)] + sys.argv[1:])
        return result.returncode

    except Exception as e:
        print(f"❌ Failed to redirect to consolidated launcher: {e}")
        print("Please run: python scripts/start_twitch.py")
        return 1

if __name__ == "__main__":
    sys.exit(main())