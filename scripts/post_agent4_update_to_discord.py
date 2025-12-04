#!/usr/bin/env python3
"""
Post Agent-4 (Captain) Update to Discord Router
==============================================

Posts Captain updates to Discord via router.

Author: Agent-4 (Captain - Strategic Oversight)
Date: 2025-12-02
"""

import os
import sys
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Get Discord router webhook (prefer router, fallback to Agent-4 specific)
webhook_url = (
    os.getenv("DISCORD_ROUTER_WEBHOOK_URL") or
    os.getenv("DISCORD_AGENT4_WEBHOOK") or
    os.getenv("DISCORD_WEBHOOK_URL")
)

if not webhook_url:
    print("❌ No Discord webhook configured for Agent-4")
    sys.exit(1)


def post_update_to_discord(message: str, title: str = "Agent-4 Captain Update"):
    """Post update to Discord via router."""
    # Format message for Discord
    content = f"## {title}\n\n{message}\n\n*Posted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
    
    # Discord message payload
    payload = {
        "content": content,
        "username": "Agent-4 (Captain - Strategic Oversight)",
        "avatar_url": None
    }
    
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        print(f"✅ Posted update to Discord: {title}")
        return True
    except Exception as e:
        print(f"❌ Failed to post to Discord: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/post_agent4_update_to_discord.py <message> [title]")
        sys.exit(1)
    
    message = sys.argv[1]
    title = sys.argv[2] if len(sys.argv) > 2 else "Agent-4 Captain Update"
    
    post_update_to_discord(message, title)



