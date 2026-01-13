#!/usr/bin/env python3
"""
Test Discord Configuration - Verify all required environment variables are set
"""

import os
from pathlib import Path

def load_env_file(filepath):
    """Load environment variables from a .env file"""
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    os.environ[key] = value
        return True
    return False

def test_discord_config():
    # Try to load from .env.discord if it exists
    env_discord_file = Path('.env.discord')
    if env_discord_file.exists():
        print("📁 Loading configuration from .env.discord...")
        load_env_file(env_discord_file)
    else:
        print("⚠️  .env.discord file not found, checking current environment...")
    """Test that all Discord configuration variables are properly set"""
    print("🤖 DISCORD BOT CONFIGURATION TEST")
    print("=" * 60)

    # Required environment variables for Discord bot
    required_vars = [
        'DISCORD_BOT_TOKEN',
        'DISCORD_INFRASTRUCTURE_CHANNEL_ID',
        'DISCORD_ARCHITECTURE_CHANNEL_ID',
        'DISCORD_COORDINATION_CHANNEL_ID',
        'DISCORD_A2A_COORDINATION_CHANNEL_ID',
        'DISCORD_AGENT1_WEBHOOK_URL',
        'DISCORD_AGENT2_WEBHOOK_URL',
        'DISCORD_AGENT3_WEBHOOK_URL',
        'DISCORD_AGENT4_WEBHOOK_URL'
    ]

    print("📋 CHECKING REQUIRED ENVIRONMENT VARIABLES:")
    print("-" * 50)

    all_configured = True
    configured_count = 0

    for var in required_vars:
        value = os.getenv(var)
        if value and value.strip():
            status = "✅"
            configured_count += 1
            # Mask sensitive values
            if 'TOKEN' in var:
                display_value = value[:10] + "..." + value[-5:] if len(value) > 15 else value
            elif 'WEBHOOK' in var:
                display_value = value[:30] + "..." if len(value) > 35 else value
            else:
                display_value = value
        else:
            status = "❌"
            display_value = "MISSING"
            all_configured = False

        print("15")

    print(f"\n📊 CONFIGURATION STATUS: {configured_count}/{len(required_vars)} variables configured")

    if all_configured:
        print("\n🎉 SUCCESS: All Discord bot configuration variables are properly set!")
        print("🤖 Discord bot should now work correctly with full agent coordination.")

        # Additional validation
        print("\n🔍 ADDITIONAL VALIDATION:")

        # Check token format
        token = os.getenv('DISCORD_BOT_TOKEN', '')
        if len(token) >= 50 and token.startswith(('M', 'N', 'O')):
            print("✅ Bot token format appears valid")
        else:
            print("⚠️  Bot token format may be invalid")

        # Check channel IDs (should be numeric)
        channel_vars = [v for v in required_vars if 'CHANNEL_ID' in v]
        valid_channels = 0
        for var in channel_vars:
            channel_id = os.getenv(var, '')
            if channel_id.isdigit() and len(channel_id) > 15:
                valid_channels += 1

        print(f"✅ Channel IDs: {valid_channels}/{len(channel_vars)} appear valid")

        # Check webhook URLs
        webhook_vars = [v for v in required_vars if 'WEBHOOK_URL' in v]
        valid_webhooks = 0
        for var in webhook_vars:
            webhook_url = os.getenv(var, '')
            if webhook_url.startswith('https://discord.com/api/webhooks/'):
                valid_webhooks += 1

        print(f"✅ Webhook URLs: {valid_webhooks}/{len(webhook_vars)} appear valid")

        print("\n🚀 READY FOR DISCORD BOT DEPLOYMENT!")

    else:
        print("\n❌ FAILURE: Some Discord configuration variables are missing.")
        print("🔧 Run the following to fix:")
        print("   python tools/discord_manager.py --setup")
        print("   # Or manually set the missing environment variables")

    return all_configured

if __name__ == "__main__":
    success = test_discord_config()
    exit(0 if success else 1)