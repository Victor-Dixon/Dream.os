#!/usr/bin/env python3
"""
Post to Discord Router - Unified Agent Communication
====================================================

Easy-to-use script for all agents to post updates to Discord via router.

Usage:
    python tools/post_to_discord_router.py --agent Agent-8 --message "Update text"
    python tools/post_to_discord_router.py --agent Agent-1 --message "Update" --title "Custom Title"
    python tools/post_to_discord_router.py --agent Agent-2 --message "Update" --priority urgent

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-11-24
Priority: CRITICAL - Agents not posting to Discord
"""

import sys
import argparse
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from tools_v2.categories.communication_tools import DiscordRouterPoster


def main():
    """Main execution."""
    parser = argparse.ArgumentParser(
        description="Post update to Discord via router",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/post_to_discord_router.py --agent Agent-8 --message "Status update"
  python tools/post_to_discord_router.py --agent Agent-1 --message "Update" --title "Custom Title"
  python tools/post_to_discord_router.py --agent Agent-2 --message "Urgent!" --priority urgent
        """
    )
    
    parser.add_argument(
        "--agent", "-a",
        required=True,
        help="Agent ID (e.g., Agent-8)"
    )
    
    parser.add_argument(
        "--message", "-m",
        required=True,
        help="Message content to post"
    )
    
    parser.add_argument(
        "--title", "-t",
        help="Optional title (defaults to '{Agent} Update')"
    )
    
    parser.add_argument(
        "--priority", "-p",
        choices=["normal", "high", "urgent"],
        default="normal",
        help="Priority level (default: normal)"
    )
    
    args = parser.parse_args()
    
    # Post to Discord
    poster = DiscordRouterPoster()
    result = poster.post_update(
        agent_id=args.agent,
        message=args.message,
        title=args.title,
        priority=args.priority
    )
    
    if result["success"]:
        print(f"✅ {result['message']}")
        print("🐝 WE. ARE. SWARM. ⚡🔥")
        sys.exit(0)
    else:
        print(f"❌ Failed to post to Discord: {result.get('error')}")
        print("\n💡 TIP: Make sure DISCORD_ROUTER_WEBHOOK_URL or DISCORD_WEBHOOK_URL is set in .env")
        sys.exit(1)


if __name__ == "__main__":
    main()


