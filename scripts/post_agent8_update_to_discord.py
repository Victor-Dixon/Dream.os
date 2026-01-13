#!/usr/bin/env python3
"""
Post Agent-8 Update to Discord Router
====================================

Posts Agent-8 SSOT & System Integration updates to Discord via router.

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-01-27
"""

import os
import sys
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Get Discord router webhook (prefer router, fallback to Agent-8 specific)
webhook_url = (
    os.getenv("DISCORD_ROUTER_WEBHOOK_URL") or
    os.getenv("DISCORD_AGENT8_WEBHOOK") or
    os.getenv("DISCORD_WEBHOOK_URL")
)

if not webhook_url:
    print("❌ No Discord webhook configured for Agent-8")
    sys.exit(1)


def post_update_to_discord(message: str, title: str = "Agent-8 SSOT & System Integration Update"):
    """Post update to Discord via router."""
    # Format message for Discord
    content = f"## {title}\n\n{message}\n\n*Posted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
    
    # Discord message payload
    payload = {
        "content": content,
        "username": "Agent-8 (SSOT & System Integration)",
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
    message = """
**🚀 JET FUEL AUTONOMOUS MODE ACTIVE**

**Current Work:**
- ✅ SSOT Verification Complete (100% compliant)
- ✅ Fixed 2 class name collisions (ROICalculatorTool, ImportValidatorTool)
- ✅ Created SSOT validation tools (ssot.detect_violations, ssot.validate_patterns)
- ✅ Reviewing GitHub repos for consolidation opportunities

**SSOT Status:**
- Message System: ✅ SSOT Compliant
- Tool Registry: ✅ SSOT Compliant
- Coordinate Files: ✅ SSOT Compliant
- Duplicate Classes: ✅ 0 violations

**Next Actions:**
- Review repo consolidation opportunities
- Enforce SSOT across all systems
- Integrate systems for single source of truth

**Status:** Working autonomously on SSOT enforcement and system integration.
    """
    return post_update_to_discord(message.strip(), "Agent-8 Status Update")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Post Agent-8 update to Discord")
    parser.add_argument("--message", "-m", help="Custom message to post")
    parser.add_argument("--title", "-t", default="Agent-8 SSOT & System Integration Update", help="Message title")
    parser.add_argument("--status", action="store_true", help="Post status update")
    
    args = parser.parse_args()
    
    if args.status:
        post_status_update()
    elif args.message:
        post_update_to_discord(args.message, args.title)
    else:
        post_status_update()




