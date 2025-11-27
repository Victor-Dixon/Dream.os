#!/usr/bin/env python3
"""
Post Agent-2 Update to Discord Router
=====================================

Posts Agent-2 architecture & design updates to Discord via router.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-01-27
"""

import os
import sys
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Get Discord router webhook (prefer router, fallback to Agent-2 specific)
webhook_url = (
    os.getenv("DISCORD_ROUTER_WEBHOOK_URL") or
    os.getenv("DISCORD_AGENT2_WEBHOOK") or
    os.getenv("DISCORD_WEBHOOK_URL")
)

if not webhook_url:
    print("❌ No Discord webhook configured for Agent-2")
    sys.exit(1)


def post_update_to_discord(message: str, title: str = "Agent-2 Architecture Update"):
    """Post update to Discord via router."""
    # Format message for Discord
    content = f"## {title}\n\n{message}\n\n*Posted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
    
    # Discord message payload
    payload = {
        "content": content,
        "username": "Agent-2 (Architecture & Design)",
        "avatar_url": None  # Can add avatar URL if available
    }
    
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        print(f"✅ Posted update to Discord: {title}")
        return True
    except Exception as e:
        print(f"❌ Failed to post to Discord: {e}")
        return False


def post_status_update():
    """Post current status update."""
    from pathlib import Path
    import json
    
    status_file = Path("agent_workspaces/Agent-2/status.json")
    if not status_file.exists():
        print("❌ Status file not found")
        return False
    
    try:
        with open(status_file) as f:
            status = json.load(f)
        
        message = f"""
**Mission:** {status.get('current_mission', 'N/A')}
**Priority:** {status.get('mission_priority', 'N/A')}
**Status:** {status.get('status', 'N/A')}

**Current Tasks:**
{chr(10).join(f"- {task}" for task in status.get('current_tasks', [])[:5])}

**Progress:** {status.get('progress', 'N/A')}

**Next Actions:**
{chr(10).join(f"- {action}" for action in status.get('next_actions', [])[:3])}
"""
        
        return post_update_to_discord(message, "Agent-2 Status Update")
    except Exception as e:
        print(f"❌ Failed to read status: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Custom message provided
        message = " ".join(sys.argv[1:])
        post_update_to_discord(message)
    else:
        # Post status update
        post_status_update()




