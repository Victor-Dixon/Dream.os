#!/usr/bin/env python3
"""
Devlog Poster - Agent-Specific Channel
======================================
Posts a devlog markdown file to an agent-specific Discord channel.
Uses DiscordRouterPoster for centralized webhook management.
"""

import os
import sys
import argparse
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from tools.categories.communication_tools import DiscordRouterPoster

def post_devlog(agent_id: str, file_path: str, title: str = None):
    """Post devlog to Discord."""
    devlog_path = Path(file_path)
    if not devlog_path.exists():
        print(f"❌ Devlog file not found: {file_path}")
        return False
    
    with open(devlog_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if not title:
        # Try to extract first H1 from markdown
        for line in content.split('\n'):
            if line.startswith('# '):
                title = line.strip('# ').strip()
                break
        if not title:
            title = f"{agent_id} Status Update"
    
    poster = DiscordRouterPoster(agent_id=agent_id)
    result = poster.post_update(
        agent_id=agent_id,
        message=content,
        title=title,
        priority="normal"
    )
    
    if result.get("success"):
        print(f"✅ Devlog posted to Discord for {agent_id}: {title}")
        return True
    else:
        print(f"❌ Failed to post devlog: {result.get('error')}")
        if result.get("details"):
            print(f"   Details: {result['details']}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Post devlog to agent-specific channel")
    parser.add_argument("--agent", required=True, help="Agent ID (e.g., Agent-3)")
    parser.add_argument("--file", required=True, help="Path to devlog file")
    parser.add_argument("--title", help="Optional title override")
    
    args = parser.parse_args()
    
    success = post_devlog(args.agent, args.file, args.title)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

