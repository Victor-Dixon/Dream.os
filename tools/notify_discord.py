#!/usr/bin/env python3
"""
Unified Discord Notification Tool
=================================

Sends notifications to agent-specific Discord channels.
Agents always post to their own channels.

Usage:
    python tools/notify_discord.py "Message" --agent Agent-7
    python tools/notify_discord.py "Update" --agent Agent-1

Author: Agent-7 (Web Development Specialist)
"""

import os
import sys
import requests
import json
import argparse
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv, dotenv_values

# Load environment variables
try:
    env_vars = dotenv_values(".env")
    for key, value in env_vars.items():
        if value and key not in os.environ:
            os.environ[key] = value
except Exception:
    load_dotenv()


def get_agent_webhook(agent: str) -> Optional[str]:
    """Get Discord webhook URL for specific agent."""
    # Normalize agent ID - extract number
    agent_lower = agent.lower().strip()
    
    # Extract number from "agent-7", "Agent-7", "agent7", etc.
    if "agent-" in agent_lower:
        agent_num = agent_lower.split("agent-")[-1].strip()
    elif agent_lower.startswith("agent"):
        agent_num = agent_lower.replace("agent", "").strip()
    else:
        # Assume it's just the number
        agent_num = agent_lower
    
    # Try multiple env var formats
    webhook = (
        os.getenv(f"DISCORD_WEBHOOK_AGENT_{agent_num}") or
        os.getenv(f"DISCORD_AGENT{agent_num}_WEBHOOK") or
        (os.getenv("DISCORD_CAPTAIN_WEBHOOK") if agent_num == "4" else None)
    )
    
    return webhook


def send_discord_notification(message: str, agent: Optional[str] = None, 
                              webhook_url: Optional[str] = None) -> bool:
    """
    Send a notification to Discord via webhook.
    
    Args:
        message: Message content
        agent: Agent ID (e.g., "Agent-7") - routes to agent's channel
        webhook_url: Direct webhook URL (overrides agent routing)
    """
    # If agent specified, use agent-specific webhook
    if agent and not webhook_url:
        webhook_url = get_agent_webhook(agent)
        if not webhook_url:
            print(f"⚠️  No Discord webhook found for {agent}")
            print(f"   Check environment variables:")
            print(f"   - DISCORD_WEBHOOK_AGENT_X")
            print(f"   - DISCORD_AGENTX_WEBHOOK")
            return False
    
    # Fallback to config file
    if not webhook_url:
        config_file = Path("config/discord_webhooks.json")
        if config_file.exists():
            with open(config_file) as f:
                webhooks = json.load(f)
                for key, webhook_data in webhooks.items():
                    if 'webhook_url' in webhook_data:
                        webhook_url = webhook_data['webhook_url']
                        break
    
    # Fallback to general webhook (last resort)
    if not webhook_url:
        webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    
    if not webhook_url:
        print("⚠️  No Discord webhook URL found. Skipping notification.")
        if agent:
            print(f"   Agent: {agent}")
            print(f"   Try setting DISCORD_WEBHOOK_AGENT_X environment variable")
        return False
    
    # Determine username
    username = agent if agent else "Agent-7"
    
    try:
        payload = {
            "content": message,
            "username": username
        }
        response = requests.post(webhook_url, json=payload, timeout=10)
        if response.status_code in [200, 204]:
            channel_info = f" ({agent}'s channel)" if agent else ""
            print(f"✅ Discord notification sent{channel_info}!")
            return True
        else:
            print(f"⚠️  Discord webhook returned {response.status_code}")
            return False
    except Exception as e:
        print(f"⚠️  Error sending Discord notification: {e}")
        return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Send Discord notification to agent's channel"
    )
    parser.add_argument('message', nargs='?', default="Task completed!",
                       help='Message to send')
    parser.add_argument('--agent', '-a',
                       help='Agent ID (e.g., Agent-7) - routes to agent\'s channel')
    
    args = parser.parse_args()
    
    # If message is first positional arg and no --agent, try to detect from script context
    # Default to Agent-7 if running from Agent-7 context
    agent = args.agent or "Agent-7"
    
    success = send_discord_notification(args.message, agent=agent)
    sys.exit(0 if success else 1)

