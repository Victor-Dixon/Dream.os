#!/usr/bin/env python3
"""
Post Agent Status Monitor Update to Discord
============================================

Posts updated explanation of agent status monitor to Discord.

Author: Agent-4 (Captain)
Date: 2025-01-27
"""

import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv

# V2 Compliance: Import from tools_v2/utils/ (migrated 2025-01-27)
from tools.utils.discord_mermaid_renderer import DiscordMermaidRenderer

load_dotenv()

# Read the update document
update_file = Path("docs/captain/AGENT_STATUS_MONITOR_DISCORD_UPDATE.md")
content = update_file.read_text(encoding='utf-8')

# Get webhook URL (prefer router, fallback to Agent-4, then general)
webhook_url = (
    os.getenv("DISCORD_ROUTER_WEBHOOK_URL") or
    os.getenv("DISCORD_WEBHOOK_AGENT_4") or
    os.getenv("DISCORD_CAPTAIN_WEBHOOK") or
    os.getenv("DISCORD_WEBHOOK_URL")
)

if not webhook_url:
    print("❌ No Discord webhook configured")
    exit(1)

# Use Mermaid renderer to handle any diagrams
renderer = DiscordMermaidRenderer()

# Check if content has Mermaid diagrams
has_mermaid = bool(renderer.extract_mermaid_diagrams(content))

if has_mermaid:
    # Use renderer to post with Mermaid conversion
    print("🔍 Detected Mermaid diagrams - converting to images...")
    success = renderer.post_to_discord_with_mermaid(
        content,
        webhook_url,
        username="Agent-4 (Captain)",
        temp_dir=Path("temp/discord_images")
    )
    if success:
        print("✅ Posted content with Mermaid diagrams to Discord")
    else:
        print("❌ Failed to post content with Mermaid diagrams")
else:
    # No Mermaid diagrams - post normally
    # Format for Discord (Discord limit: 2000 chars per message)
    # Split into multiple messages if needed
    messages = []
    current_message = ""

    # Split content into chunks
    lines = content.split('\n')
    current_chunk = ""

    for line in lines:
        # Check if adding this line would exceed limit
        if len(current_chunk) + len(line) + 1 > 1900:
            if current_chunk:
                messages.append(current_chunk)
            current_chunk = line + "\n"
        else:
            current_chunk += line + "\n"

    if current_chunk:
        messages.append(current_chunk)

    # Post messages
    for i, message in enumerate(messages):
        payload = {
            "content": f"**Agent Status Monitor - How It Works Now**\n\n{message}",
            "username": "Agent-4 (Captain)"
        }
        
        if i == 0:
            # First message gets title
            payload["content"] = f"🔍 **Agent Status Monitor - How It Works Now**\n\n{message}"
        
        try:
            response = requests.post(webhook_url, json=payload, timeout=10)
            if response.status_code == 204:
                print(f"✅ Posted message {i+1}/{len(messages)} to Discord")
            else:
                print(f"❌ Discord error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Failed to post to Discord: {e}")

    print(f"✅ Posted {len(messages)} message(s) to Discord")

