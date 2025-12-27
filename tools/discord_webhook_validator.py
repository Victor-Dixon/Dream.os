#!/usr/bin/env python3
"""
Discord Webhook Validator Tool

Validates Discord webhook configuration (username, URL, permissions) and tests posting
with detailed diagnostics.

Usage:
    python tools/discord_webhook_validator.py [--agent Agent-X] [--webhook-url URL] [--test-post]
"""

import os
import sys
import argparse
import requests
from pathlib import Path
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
from datetime import datetime

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Load .env from project root
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)


class DiscordWebhookValidator:
    """Validates Discord webhook configuration and tests posting."""
    
    def __init__(self, webhook_url: Optional[str] = None, agent_id: Optional[str] = None):
        """Initialize validator.
        
        Args:
            webhook_url: Optional webhook URL to validate (if not provided, uses agent-specific or router)
            agent_id: Optional agent ID to use agent-specific webhook
        """
        self.agent_id = agent_id
        self.webhook_url = webhook_url
        
        if not self.webhook_url:
            # Try agent-specific webhook first
            if agent_id:
                agent_env_key = agent_id.replace("-", "_").upper()
                self.webhook_url = os.getenv(f"DISCORD_WEBHOOK_{agent_env_key}")
            
            # Fallback to router or general webhook
            if not self.webhook_url:
                self.webhook_url = (
                    os.getenv("DISCORD_ROUTER_WEBHOOK_URL") or
                    os.getenv("DISCORD_WEBHOOK_URL")
                )
    
    def validate_webhook_url(self) -> Dict[str, Any]:
        """Validate webhook URL format and accessibility.
        
        Returns:
            Validation result dict
        """
        result = {
            "valid": False,
            "url": self.webhook_url,
            "errors": [],
            "warnings": [],
            "info": []
        }
        
        if not self.webhook_url:
            result["errors"].append("No webhook URL configured")
            return result
        
        # Check URL format (accept both discord.com and discordapp.com)
        if not (self.webhook_url.startswith("https://discord.com/api/webhooks/") or 
                self.webhook_url.startswith("https://discordapp.com/api/webhooks/")):
            result["errors"].append("Invalid webhook URL format (must start with https://discord.com/api/webhooks/ or https://discordapp.com/api/webhooks/)")
            return result
        
        # Check URL structure
        parts = self.webhook_url.split("/")
        if len(parts) < 6:
            result["errors"].append("Invalid webhook URL structure")
            return result
        
        webhook_id = parts[5] if len(parts) > 5 else None
        webhook_token = parts[6] if len(parts) > 6 else None
        
        if not webhook_id or not webhook_token:
            result["errors"].append("Missing webhook ID or token in URL")
            return result
        
        result["info"].append(f"Webhook ID: {webhook_id[:8]}...")
        result["info"].append(f"Webhook token: {webhook_token[:8]}...")
        
        # Test webhook accessibility
        try:
            response = requests.get(self.webhook_url, timeout=5)
            if response.status_code == 401:
                result["errors"].append("Webhook token is invalid or expired")
            elif response.status_code == 404:
                result["errors"].append("Webhook not found (may have been deleted)")
            elif response.status_code == 200:
                result["valid"] = True
                result["info"].append("Webhook is accessible")
            else:
                result["warnings"].append(f"Unexpected response code: {response.status_code}")
        except requests.exceptions.Timeout:
            result["errors"].append("Webhook URL timeout (check network connectivity)")
        except requests.exceptions.RequestException as e:
            result["errors"].append(f"Webhook URL error: {str(e)}")
        
        return result
    
    def validate_username(self, username: Optional[str] = None) -> Dict[str, Any]:
        """Validate webhook username (check for forbidden words).
        
        Args:
            username: Optional username to check (if not provided, tests with default)
        
        Returns:
            Validation result dict
        """
        result = {
            "valid": False,
            "username": username,
            "errors": [],
            "warnings": [],
            "info": []
        }
        
        if not username:
            # Test with default username format
            if self.agent_id:
                username = f"{self.agent_id} (Router)"
            else:
                username = "Discord Router"
        
        result["username"] = username
        
        # Check for forbidden words
        forbidden_words = ["discord"]
        username_lower = username.lower()
        
        for word in forbidden_words:
            if word in username_lower:
                result["errors"].append(f"Username contains forbidden word: '{word}' (Discord API restriction)")
                result["warnings"].append(f"Update username in Discord settings: Server Settings → Integrations → Webhooks → Edit → Change username")
                return result
        
        # Check length
        if len(username) > 80:
            result["warnings"].append(f"Username is long ({len(username)} chars, Discord limit: 80)")
        
        result["valid"] = True
        result["info"].append("Username format is valid")
        
        return result
    
    def test_post(self, test_message: Optional[str] = None) -> Dict[str, Any]:
        """Test posting to webhook.
        
        Args:
            test_message: Optional test message (defaults to validation test message)
        
        Returns:
            Test result dict
        """
        result = {
            "success": False,
            "webhook_url": self.webhook_url,
            "errors": [],
            "warnings": [],
            "info": []
        }
        
        if not self.webhook_url:
            result["errors"].append("No webhook URL configured")
            return result
        
        if not test_message:
            test_message = f"✅ Discord Webhook Validation Test - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # Prepare payload
        payload = {
            "content": test_message,
            "username": f"{self.agent_id} (Router)" if self.agent_id else "Webhook Validator"
        }
        
        # Remove "discord" from username if present
        if "discord" in payload["username"].lower():
            payload["username"] = payload["username"].replace("discord", "").replace("Discord", "").strip()
            result["warnings"].append("Removed 'discord' from username (Discord API restriction)")
        
        try:
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            
            result["status_code"] = response.status_code
            result["response_text"] = response.text[:200]  # First 200 chars
            
            if response.status_code in [200, 204]:
                result["success"] = True
                result["info"].append("✅ Test post successful - message posted to Discord")
                if response.status_code == 204:
                    result["info"].append("Status 204 (No Content) - Discord accepted the message")
            elif response.status_code == 400:
                result["errors"].append("400 Bad Request - Check payload format and username")
                if "username" in response.text.lower():
                    result["errors"].append("Username issue detected - may contain forbidden word 'discord'")
            elif response.status_code == 401:
                result["errors"].append("401 Unauthorized - Webhook token is invalid or expired")
            elif response.status_code == 404:
                result["errors"].append("404 Not Found - Webhook may have been deleted")
            elif response.status_code == 429:
                result["warnings"].append("429 Rate Limited - Too many requests, wait before retrying")
            else:
                result["errors"].append(f"Unexpected status code: {response.status_code}")
                
        except requests.exceptions.Timeout:
            result["errors"].append("Request timeout - Check network connectivity")
        except requests.exceptions.RequestException as e:
            result["errors"].append(f"Request error: {str(e)}")
        
        return result
    
    def validate_all(self, test_post: bool = False) -> Dict[str, Any]:
        """Run all validation checks.
        
        Args:
            test_post: Whether to test posting to webhook
        
        Returns:
            Complete validation result dict
        """
        result = {
            "agent_id": self.agent_id,
            "webhook_url": self.webhook_url,
            "validations": {},
            "overall_valid": False,
            "errors": [],
            "warnings": [],
            "info": []
        }
        
        # Validate URL
        url_result = self.validate_webhook_url()
        result["validations"]["url"] = url_result
        result["errors"].extend(url_result["errors"])
        result["warnings"].extend(url_result["warnings"])
        result["info"].extend(url_result["info"])
        
        # Validate username
        username_result = self.validate_username()
        result["validations"]["username"] = username_result
        result["errors"].extend(username_result["errors"])
        result["warnings"].extend(username_result["warnings"])
        result["info"].extend(username_result["info"])
        
        # Test post if requested
        if test_post:
            post_result = self.test_post()
            result["validations"]["test_post"] = post_result
            result["errors"].extend(post_result["errors"])
            result["warnings"].extend(post_result["warnings"])
            result["info"].extend(post_result["info"])
            result["overall_valid"] = post_result["success"]
        else:
            # Overall valid if URL and username are valid
            result["overall_valid"] = url_result["valid"] and username_result["valid"]
        
        return result


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Validate Discord webhook configuration and test posting"
    )
    parser.add_argument(
        "--agent",
        type=str,
        help="Agent ID to validate agent-specific webhook (e.g., Agent-1)"
    )
    parser.add_argument(
        "--webhook-url",
        type=str,
        help="Webhook URL to validate (overrides agent-specific and router webhooks)"
    )
    parser.add_argument(
        "--test-post",
        action="store_true",
        help="Test posting to webhook"
    )
    parser.add_argument(
        "--username",
        type=str,
        help="Username to validate (defaults to agent-specific or 'Discord Router')"
    )
    
    args = parser.parse_args()
    
    # Initialize validator
    validator = DiscordWebhookValidator(
        webhook_url=args.webhook_url,
        agent_id=args.agent
    )
    
    # Run validation
    result = validator.validate_all(test_post=args.test_post)
    
    # Print results
    print("\n" + "="*60)
    print("Discord Webhook Validation Results")
    print("="*60)
    
    if args.agent:
        print(f"\nAgent: {args.agent}")
    if result["webhook_url"]:
        print(f"Webhook URL: {result['webhook_url'][:50]}...")
    else:
        print("\n⚠️  No webhook URL configured")
    
    # URL validation
    if "url" in result["validations"]:
        url_result = result["validations"]["url"]
        print(f"\n📋 URL Validation: {'✅ Valid' if url_result['valid'] else '❌ Invalid'}")
        for error in url_result["errors"]:
            print(f"   ❌ {error}")
        for warning in url_result["warnings"]:
            print(f"   ⚠️  {warning}")
        for info in url_result["info"]:
            print(f"   ℹ️  {info}")
    
    # Username validation
    if "username" in result["validations"]:
        username_result = result["validations"]["username"]
        print(f"\n👤 Username Validation: {'✅ Valid' if username_result['valid'] else '❌ Invalid'}")
        if username_result["username"]:
            print(f"   Username: {username_result['username']}")
        for error in username_result["errors"]:
            print(f"   ❌ {error}")
        for warning in username_result["warnings"]:
            print(f"   ⚠️  {warning}")
        for info in username_result["info"]:
            print(f"   ℹ️  {info}")
    
    # Test post
    if "test_post" in result["validations"]:
        post_result = result["validations"]["test_post"]
        print(f"\n📤 Test Post: {'✅ Success' if post_result['success'] else '❌ Failed'}")
        if "status_code" in post_result:
            print(f"   Status Code: {post_result['status_code']}")
        for error in post_result["errors"]:
            print(f"   ❌ {error}")
        for warning in post_result["warnings"]:
            print(f"   ⚠️  {warning}")
        for info in post_result["info"]:
            print(f"   ℹ️  {info}")
    
    # Overall result
    print("\n" + "="*60)
    if result["overall_valid"]:
        print("✅ Overall: VALID - Webhook configuration is correct")
    else:
        print("❌ Overall: INVALID - Issues found, see above")
    print("="*60 + "\n")
    
    # Exit code
    sys.exit(0 if result["overall_valid"] else 1)


if __name__ == "__main__":
    main()
