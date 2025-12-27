"""
Communication Tools - Discord Router Integration
================================================

Unified Discord posting for all agents via router.

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-11-24
Priority: CRITICAL - Agents not posting to Discord
"""

import os
import sys
import requests
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, Optional
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Load .env from project root explicitly
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)


class DiscordRouterPoster:
    """Unified Discord router posting for all agents."""
    
    def __init__(self, agent_id: Optional[str] = None):
        """Initialize Discord router poster.
        
        Args:
            agent_id: Optional agent ID to use agent-specific webhook (e.g., "Agent-2")
        """
        # For devlogs, prefer agent-specific webhook, then router, then fallback
        if agent_id:
            # Convert "Agent-2" to "AGENT_2" for env var lookup
            agent_env_key = agent_id.replace("-", "_").upper()
            agent_webhook = os.getenv(f"DISCORD_WEBHOOK_{agent_env_key}")
            if agent_webhook:
                self.webhook_url = agent_webhook
                return
        
        # Fallback to router or general webhook
        self.webhook_url = (
            os.getenv("DISCORD_ROUTER_WEBHOOK_URL") or
            os.getenv("DISCORD_WEBHOOK_URL")
        )
        
        if not self.webhook_url:
            print("⚠️  WARNING: No Discord webhook configured")
            if agent_id:
                agent_env_key = agent_id.replace("-", "_").upper()
                print(f"   Set DISCORD_WEBHOOK_{agent_env_key} for agent-specific channel")
            print("   Or set DISCORD_ROUTER_WEBHOOK_URL or DISCORD_WEBHOOK_URL in .env")
    
    def post_update(
        self,
        agent_id: str,
        message: str,
        title: Optional[str] = None,
        priority: str = "normal"
    ) -> Dict[str, Any]:
        """
        Post update to Discord via router.
        
        Args:
            agent_id: Agent identifier (e.g., "Agent-8")
            message: Message content
            title: Optional title (defaults to agent update)
            priority: Priority level (normal, high, urgent)
        
        Returns:
            Result dict with success status
        """
        if not self.webhook_url:
            return {
                "success": False,
                "error": "No Discord webhook configured",
            }
        
        # Format title
        if not title:
            title = f"{agent_id} Update"
        
        # Add priority indicator
        priority_icons = {
            "urgent": "🚨",
            "high": "⚡",
            "normal": "📢",
        }
        icon = priority_icons.get(priority, "📢")
        
        # Format message for Discord
        content = f"{icon} ## {title}\n\n{message}\n\n*Posted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
        
        # Discord has a 2000 character limit for message content
        # If content is too long, truncate with a note
        max_discord_length = 2000
        if len(content) > max_discord_length:
            truncate_at = max_discord_length - 100  # Leave room for truncation message
            content = content[:truncate_at] + "\n\n... (message truncated - see full content in workspace)"
            print(f"⚠️  Message truncated for Discord ({len(content)} chars → {max_discord_length} chars)")
        
        # Discord message payload
        # Note: Discord API restriction - webhook usernames cannot contain "discord"
        # Using "(Router)" instead of "(Discord Router)" to comply with API restrictions
        payload = {
            "content": content,
            "username": f"{agent_id} (Router)"
        }
        
        # Validate payload size
        import json
        payload_size = len(json.dumps(payload))
        if payload_size > 2000:
            return {
                "success": False,
                "error": f"Payload too large ({payload_size} bytes, Discord limit: 2000 bytes)",
            }
        
        try:
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            return {
                "success": True,
                "message": f"Posted update to Discord: {title}",
            }
        except requests.exceptions.HTTPError as e:
            # Capture detailed error information for debugging
            error_details = {
                "status_code": response.status_code,
                "response_text": response.text[:500] if hasattr(response, 'text') else "No response text",
                "error": str(e)
            }
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {error_details['response_text']}",
                "details": error_details
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Request failed: {str(e)}",
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
            }


class DiscordPostTool:
    """Tool adapter for Discord posting."""
    
    def __init__(self):
        """Initialize Discord post tool."""
        self.poster = DiscordRouterPoster()
    
    def execute(self, params: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
        """
        Execute Discord post.
        
        Args:
            params: {
                "agent_id": "Agent-8",
                "message": "Update message",
                "title": "Optional title",
                "priority": "normal|high|urgent"
            }
        
        Returns:
            Result dict
        """
        agent_id = params.get("agent_id", "Agent-8")
        message = params.get("message", "")
        title = params.get("title")
        priority = params.get("priority", "normal")
        
        if not message:
            return {
                "success": False,
                "error": "Message is required",
            }
        
        result = self.poster.post_update(agent_id, message, title, priority)
        
        if result["success"]:
            print(f"✅ {result['message']}")
        else:
            print(f"❌ Failed to post to Discord: {result.get('error')}")
        
        return result


# Tool registration
def get_tools():
    """Get communication tools."""
    return {
        "discord.post": DiscordPostTool(),
    }


