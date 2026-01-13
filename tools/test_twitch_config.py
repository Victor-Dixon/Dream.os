#!/usr/bin/env python3
"""
Twitch Configuration Validator
==============================

Validates Twitch bot configuration before starting the bot.
Checks environment variables, format, and optionally tests connection.

Usage:
    python tools/test_twitch_config.py          # Validate config only
    python tools/test_twitch_config.py --test   # Validate + test connection

Author: Agent-7 (Web Development Specialist)
V2 Compliant: <150 lines
"""

import os
import sys
import argparse
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()


def validate_channel(channel: str) -> tuple[bool, str, str]:
    """
    Validate and normalize Twitch channel name.
    
    Returns:
        (is_valid, normalized_channel, error_message)
    """
    if not channel:
        return False, "", "Channel is empty"
    
    # Remove # prefix if present
    if channel.startswith("#"):
        channel = channel[1:]
    
    # Extract from URL if present
    if "twitch.tv/" in channel.lower():
        parts = channel.lower().split("twitch.tv/")
        if len(parts) > 1:
            channel = parts[-1].split("/")[0].split("?")[0].rstrip("/")
    
    # Normalize
    channel = channel.lower().strip()
    
    # Validate format (alphanumeric, underscores, hyphens)
    if not channel:
        return False, "", "Channel name is empty after normalization"
    
    if not all(c.isalnum() or c in ['_', '-'] for c in channel):
        return False, channel, f"Invalid channel format: '{channel}' (must be alphanumeric with _ or -)"
    
    if len(channel) < 1 or len(channel) > 25:
        return False, channel, f"Channel name length invalid: {len(channel)} (must be 1-25 chars)"
    
    return True, channel, ""


def validate_token(token: str) -> tuple[bool, str, str]:
    """
    Validate Twitch OAuth token format.
    
    Returns:
        (is_valid, normalized_token, error_message)
    """
    if not token:
        return False, "", "Token is empty"
    
    # Clean token
    token_clean = token.strip().strip('"').strip("'").replace('\n', '').replace('\r', '')
    
    # Check format
    if not token_clean.startswith("oauth:"):
        # Try adding prefix
        if len(token_clean) > 10:  # Reasonable token length
            token_clean = f"oauth:{token_clean}"
        else:
            return False, "", "Token too short or invalid format (should be 'oauth:xxxxx')"
    
    # Basic length check (OAuth tokens are typically 30+ chars)
    if len(token_clean) < 20:
        return False, token_clean, f"Token too short: {len(token_clean)} chars (expected 20+)"
    
    return True, token_clean, ""


def test_connection(channel: str, token: str, username: str) -> tuple[bool, str]:
    """
    Test Twitch IRC connection (optional).
    
    Returns:
        (success, error_message)
    """
    try:
        # Import here to avoid dependency if not testing
        from src.services.chat_presence.twitch_bridge import TwitchChatBridge
        import asyncio
        
        print("   🔌 Testing connection...")
        
        # Create bridge
        bridge = TwitchChatBridge(
            username=username,
            oauth_token=token,
            channel=channel,
            on_message=None,  # No message handler for test
        )
        
        # Try to connect (with timeout)
        async def test_connect():
            try:
                result = await asyncio.wait_for(bridge.connect(), timeout=10.0)
                if result:
                    # Give it a moment to establish connection
                    await asyncio.sleep(2)
                    bridge.stop()
                    return True, "Connection successful"
                else:
                    bridge.stop()
                    return False, "Connection returned False"
            except asyncio.TimeoutError:
                bridge.stop()
                return False, "Connection timeout (10s)"
            except Exception as e:
                bridge.stop()
                return False, f"Connection error: {str(e)}"
        
        success, message = asyncio.run(test_connect())
        return success, message
        
    except ImportError as e:
        return False, f"Import error: {e}"
    except Exception as e:
        return False, f"Test error: {str(e)}"


def main():
    """Main validation function."""
    parser = argparse.ArgumentParser(description="Validate Twitch bot configuration")
    parser.add_argument(
        '--test',
        action='store_true',
        help='Test connection after validation'
    )
    args = parser.parse_args()
    
    print("🔍 Twitch Configuration Validator")
    print("=" * 50)
    print()
    
    # Get environment variables
    channel = os.getenv("TWITCH_CHANNEL", "").strip()
    token = os.getenv("TWITCH_ACCESS_TOKEN", "").strip()
    username = os.getenv("TWITCH_BOT_USERNAME", "").strip() or channel
    
    errors = []
    warnings = []
    
    # Validate channel
    print("📺 Validating TWITCH_CHANNEL...")
    if not channel:
        errors.append("TWITCH_CHANNEL is not set")
        print("   ❌ NOT SET")
    else:
        is_valid, normalized, error = validate_channel(channel)
        if is_valid:
            print(f"   ✅ Valid: {normalized}")
            channel = normalized
        else:
            errors.append(f"TWITCH_CHANNEL: {error}")
            print(f"   ❌ Invalid: {error}")
    print()
    
    # Validate token
    print("🔐 Validating TWITCH_ACCESS_TOKEN...")
    if not token:
        errors.append("TWITCH_ACCESS_TOKEN is not set")
        print("   ❌ NOT SET")
    else:
        is_valid, normalized, error = validate_token(token)
        if is_valid:
            masked = normalized[:15] + "..." + normalized[-4:] if len(normalized) > 19 else "***"
            print(f"   ✅ Valid format: {masked}")
            token = normalized
        else:
            errors.append(f"TWITCH_ACCESS_TOKEN: {error}")
            print(f"   ❌ Invalid: {error}")
    print()
    
    # Validate username
    print("👤 Validating TWITCH_BOT_USERNAME...")
    if not username:
        warnings.append("TWITCH_BOT_USERNAME not set, will use channel name")
        username = channel
        print(f"   ⚠️  Not set, will use: {username}")
    else:
        is_valid, normalized, error = validate_channel(username)
        if is_valid:
            print(f"   ✅ Valid: {normalized}")
            username = normalized
        else:
            warnings.append(f"TWITCH_BOT_USERNAME: {error}, will use channel name")
            username = channel
            print(f"   ⚠️  Invalid, using channel: {username}")
    print()
    
    # Summary
    print("=" * 50)
    if errors:
        print("❌ VALIDATION FAILED")
        print()
        print("Errors:")
        for error in errors:
            print(f"  • {error}")
        print()
        print("Fix these errors and run again.")
        return 1
    else:
        print("✅ VALIDATION PASSED")
        if warnings:
            print()
            print("Warnings:")
            for warning in warnings:
                print(f"  ⚠️  {warning}")
    
    # Test connection if requested
    if args.test:
        print()
        print("=" * 50)
        print("🧪 Testing Connection...")
        print()
        success, message = test_connection(channel, token, username)
        if success:
            print(f"   ✅ {message}")
            print()
            print("✅ Configuration is valid and connection test passed!")
            return 0
        else:
            print(f"   ❌ {message}")
            print()
            print("⚠️  Configuration is valid but connection test failed.")
            print("   This might be due to:")
            print("   • Invalid or expired OAuth token")
            print("   • Network connectivity issues")
            print("   • Bot username doesn't match token")
            return 1
    
    print()
    print("💡 Tip: Run with --test to verify connection")
    return 0


if __name__ == "__main__":
    sys.exit(main())

