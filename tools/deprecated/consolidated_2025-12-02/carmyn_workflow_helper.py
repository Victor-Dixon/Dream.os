#!/usr/bin/env python3
"""
Carmyn Workflow Helper - Discord-First Communication Assistant
Agent-7 (Web Development Specialist)

Purpose: Streamline Carmyn workflow (action → deploy → Discord post)
V2 Compliant: <400 lines
"""

import argparse
import subprocess
import sys
from pathlib import Path
from datetime import datetime


CARMYN_DISCORD_ID = "<@1437922284554686565>"
CARMYN_WORKSPACE = "agent_workspaces/Agent-7/profiles/carmyn/website/"


def post_to_discord(message: str) -> bool:
    """Post message to Discord devlog."""
    try:
        # Try discord_router first
        cmd = [
            sys.executable,
            "-m",
            "tools.discord_router",
            "--agent",
            "Agent-7",
            "--devlog",
            "--message",
            message
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return True
    except Exception:
        pass
    
    # Fallback: Try devlog_manager
    try:
        devlog_file = Path("agent_workspaces/Agent-7/devlogs/CARMYN_UPDATE.md")
        devlog_file.write_text(f"# Carmyn Update\n\n{message}\n\n*Posted: {datetime.now()}*\n")
        cmd = [sys.executable, "tools/devlog_manager.py", "post", str(devlog_file)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.returncode == 0
    except Exception as e:
        print(f"⚠️  Discord post failed: {e}")
        print(f"⚠️  Message to post manually: {message}")
        return False


def create_discord_message(action: str, status: str, url: str = None, next_steps: str = None) -> str:
    """Create formatted Discord message for Carmyn."""
    message = f"{CARMYN_DISCORD_ID} {status} {action}!\n\n"
    
    if url:
        message += f"🔗 LIVE LINK: {url}\n\n"
    
    if next_steps:
        message += f"📋 Next: {next_steps}\n\n"
    
    message += "What would you like to work on next? 💖✨"
    return message


def workflow_action(action_name: str, status: str, url: str = None, next_steps: str = None):
    """Complete Carmyn workflow: create message and post to Discord."""
    message = create_discord_message(action_name, status, url, next_steps)
    success = post_to_discord(message)
    
    if success:
        print(f"✅ Discord post successful!")
    else:
        print(f"⚠️  Discord post may have failed - check manually")
        print(f"\nMessage:\n{message}")
    
    return success


def main():
    """CLI interface."""
    parser = argparse.ArgumentParser(
        description="Carmyn Workflow Helper - Discord-first communication",
        epilog=f"Example: python {sys.argv[0]} --action 'Website Updated' --status '✅' --url 'https://prismblossom.online'"
    )
    parser.add_argument("--action", required=True, help="Action description")
    parser.add_argument("--status", default="✅", help="Status emoji/text")
    parser.add_argument("--url", help="Live URL (optional)")
    parser.add_argument("--next", dest="next_steps", help="Next steps (optional)")
    
    args = parser.parse_args()
    
    workflow_action(args.action, args.status, args.url, args.next_steps)
    return 0


if __name__ == "__main__":
    sys.exit(main())


