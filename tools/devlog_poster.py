#!/usr/bin/env python3
"""
Devlog Poster Tool - Agent Cellphone V2
======================================

Posts complete devlogs to Discord agent-specific channels using smart pagination.

Features:
    - Smart pagination: Splits long devlogs into multiple beautifully formatted messages
    - Complete content preservation: Posts the entire devlog, not truncated versions
    - Page indicators: Shows "Page X/Y" for multi-page devlogs
    - Rate limiting protection: Adds delays between pages to avoid Discord rate limits

Usage:
    python tools/devlog_poster.py --agent Agent-X --file <devlog_path>

Requirements:
    - DISCORD_WEBHOOK_AGENT_X environment variables in .env
    - Each webhook configured to post to agent's devlog channel

Author: AI Assistant - Created to resolve missing tool issue with smart pagination
Date: 2026-01-08
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def split_content_into_pages(content: str, max_length: int = 1900) -> list[str]:
    """
    Split content into pages that fit within Discord's message limits.

    Args:
        content: The full content to split
        max_length: Maximum characters per page (default 1900 for safety)

    Returns:
        List of content pages
    """
    if len(content) <= max_length:
        return [content]

    pages = []
    lines = content.split('\n')
    current_page = ""
    current_length = 0

    for line in lines:
        line_length = len(line) + 1  # +1 for newline

        # If adding this line would exceed the limit, start a new page
        if current_length + line_length > max_length and current_page:
            pages.append(current_page.rstrip())
            current_page = line + '\n'
            current_length = line_length
        else:
            current_page += line + '\n'
            current_length += line_length

    # Add the last page if it has content
    if current_page.strip():
        pages.append(current_page.rstrip())

    return pages

def post_devlog_to_discord(agent_id: str, devlog_path: str) -> bool:
    """
    Post complete devlog to Discord using agent-specific webhook with smart pagination.

    Features:
        - Splits long devlogs into multiple messages to preserve complete content
        - Adds page indicators (Page X/Y) for multi-page devlogs
        - Includes continuation markers for readability
        - Rate limiting protection between pages

    Args:
        agent_id: Agent identifier (e.g., 'Agent-1', 'Agent-2')
        devlog_path: Path to devlog file

    Returns:
        bool: Success status (all pages posted successfully)
    """
    try:
        # Load environment variables
        from dotenv import load_dotenv
        env_path = project_root / ".env"
        if env_path.exists():
            load_dotenv(env_path)

        # Construct webhook environment variable name
        webhook_env_var = f"DISCORD_WEBHOOK_{agent_id.replace('-', '_').upper()}"

        webhook_url = os.getenv(webhook_env_var)
        if not webhook_url:
            print(f"❌ ERROR: {webhook_env_var} not found in environment variables")
            return False

        # Read devlog content
        devlog_file = Path(devlog_path)
        if not devlog_file.exists():
            print(f"❌ ERROR: Devlog file not found: {devlog_path}")
            return False

        content = devlog_file.read_text(encoding='utf-8')

        # Split content into pages
        pages = split_content_into_pages(content)

        # Post to Discord webhook with pagination
        import requests
        import time

        total_pages = len(pages)
        success_count = 0

        for page_num, page_content in enumerate(pages, 1):
            # Create pagination header
            if total_pages == 1:
                header = f"**{agent_id} Devlog Update**"
            else:
                header = f"**{agent_id} Devlog Update** (Page {page_num}/{total_pages})"
                # Add continuation marker for multi-page
                if page_num > 1:
                    header += " *(continued)*"

            payload = {
                "username": f"{agent_id} Devlog",
                "content": f"{header}\n\n{page_content}"
            }

            # Add small delay between pages to avoid rate limiting
            if page_num > 1:
                time.sleep(1)

            response = requests.post(webhook_url, json=payload, timeout=10)

            if response.status_code == 204:
                success_count += 1
                print(f"✅ Posted page {page_num}/{total_pages} to {agent_id} Discord channel")
            else:
                print(f"❌ Failed to post page {page_num}/{total_pages}: HTTP {response.status_code}")
                return False

        if success_count == total_pages:
            print(f"✅ Successfully posted complete devlog ({total_pages} page{'s' if total_pages > 1 else ''}) to {agent_id} Discord channel")
            return True
        else:
            print(f"❌ Only posted {success_count}/{total_pages} pages")
            return False

    except Exception as e:
        print(f"❌ Error posting devlog: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Post devlog to Discord agent channel")
    parser.add_argument("--agent", required=True, help="Agent ID (e.g., Agent-1, Agent-2)")
    parser.add_argument("--file", required=True, help="Path to devlog file")

    args = parser.parse_args()

    success = post_devlog_to_discord(args.agent, args.file)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()