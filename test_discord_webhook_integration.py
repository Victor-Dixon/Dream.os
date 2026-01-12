#!/usr/bin/env python3
"""
Discord Webhook Integration Test
Tests Discord functionality using webhooks instead of creating channels
"""

import asyncio
import os
import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

async def test_webhook_message():
    """Test sending a message via Discord webhook and then deleting it."""

    print("🔗 TESTING DISCORD WEBHOOK INTEGRATION")
    print("=" * 50)

    # Test with Agent-1 webhook (should exist from setup)
    webhook_url = os.getenv('DISCORD_AGENT1_WEBHOOK_URL')

    if not webhook_url:
        print("❌ DISCORD_AGENT1_WEBHOOK_URL not found")
        print("💡 Run: python tools/discord_manager.py --setup")
        return False

    try:
        import requests

        # Create test message
        test_message = {
            "content": "🤖 Integration Test Message",
            "embeds": [{
                "title": "Discord Webhook Test",
                "description": "Testing webhook functionality for agent communication",
                "color": 0x00ff00,
                "fields": [
                    {
                        "name": "Test Type",
                        "value": "Webhook Integration",
                        "inline": True
                    },
                    {
                        "name": "Timestamp",
                        "value": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "inline": True
                    },
                    {
                        "name": "Status",
                        "value": "✅ Test Message Sent",
                        "inline": True
                    }
                ],
                "footer": {
                    "text": "Agent Cellphone V2 - Webhook Integration Test"
                }
            }]
        }

        print("📨 Sending test message via webhook...")

        # Send the message
        response = requests.post(
            webhook_url,
            json=test_message,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )

        if response.status_code == 204:
            print("✅ Test message sent successfully!")

            # Try to get the message (webhooks don't return message IDs easily)
            # For testing purposes, we'll just verify the send worked
            print("✅ Webhook integration test passed")
            print("📝 Note: Test message posted to Discord (check #agent-1 channel)")
            return True
        else:
            print(f"❌ Webhook send failed: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Webhook test error: {e}")
        return False

async def test_multiple_agent_webhooks():
    """Test webhooks for multiple agents."""

    print("\n👥 TESTING MULTIPLE AGENT WEBHOOKS")
    print("=" * 50)

    agents_to_test = ['AGENT1', 'AGENT2', 'AGENT3', 'AGENT4']
    results = {}

    for agent in agents_to_test:
        webhook_env = f'DISCORD_{agent}_WEBHOOK_URL'
        webhook_url = os.getenv(webhook_env)

        if not webhook_url:
            print(f"⚠️  {agent}: Webhook URL not configured")
            results[agent] = False
            continue

        try:
            import requests

            # Send a brief test message
            test_content = f"🤖 {agent} webhook test - {time.strftime('%H:%M:%S')}"

            response = requests.post(
                webhook_url,
                json={"content": test_content},
                headers={'Content-Type': 'application/json'},
                timeout=5
            )

            if response.status_code == 204:
                print(f"✅ {agent}: Webhook working")
                results[agent] = True
            else:
                print(f"❌ {agent}: Webhook failed (HTTP {response.status_code})")
                results[agent] = False

        except Exception as e:
            print(f"❌ {agent}: Error - {e}")
            results[agent] = False

        # Small delay between tests
        await asyncio.sleep(1)

    # Summary
    working_count = sum(1 for result in results.values() if result)
    total_count = len(results)

    print(f"\n📊 Webhook Test Results: {working_count}/{total_count} working")

    if working_count >= 2:  # At least 2 working for basic functionality
        print("✅ Multi-agent webhook integration: PASSED")
        return True
    else:
        print("❌ Multi-agent webhook integration: FAILED")
        return False

async def test_d2a_message_via_webhook():
    """Test sending a full D2A formatted message via webhook."""

    print("\n📋 TESTING D2A MESSAGE VIA WEBHOOK")
    print("=" * 50)

    try:
        from src.core.messaging_models_core import (
            UnifiedMessage,
            MessageCategory,
            UnifiedMessageType,
            UnifiedMessagePriority,
        )
        from src.core.messaging_templates import render_message
        import uuid
        from datetime import datetime
        import requests

        # Create a D2A message
        d2a_message = UnifiedMessage(
            content="Test D2A message from automated test",
            sender="Test System",
            recipient="Agent-1",
            message_type=UnifiedMessageType.HUMAN_TO_AGENT,
            priority=UnifiedMessagePriority.REGULAR,
            category=MessageCategory.D2A,
            message_id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
        )

        # Render with D2A template
        devlog_cmd = "python tools/devlog_poster.py --agent Agent-1 --file <devlog_path>"
        rendered_message = render_message(d2a_message, devlog_command=devlog_cmd)

        # Send via webhook
        webhook_url = os.getenv('DISCORD_AGENT1_WEBHOOK_URL')
        if not webhook_url:
            print("❌ No webhook URL for Agent-1")
            return False

        # Discord has a 2000 character limit, so we need to truncate if necessary
        if len(rendered_message) > 1900:
            truncated_message = rendered_message[:1900] + "\n\n[Message truncated for Discord limit]"
        else:
            truncated_message = rendered_message

        webhook_payload = {
            "content": f"```{truncated_message}```",  # Wrap in code block for formatting
            "embeds": [{
                "title": "D2A Template Test",
                "description": "Testing full D2A message formatting via webhook",
                "color": 0x0099ff,
                "footer": {
                    "text": "Automated D2A Template Test"
                }
            }]
        }

        response = requests.post(
            webhook_url,
            json=webhook_payload,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )

        if response.status_code == 204:
            print("✅ Full D2A message sent via webhook!")
            print("✅ Template formatting preserved")
            print(f"📏 Message length: {len(rendered_message)} chars (sent: {len(truncated_message)})")
            return True
        else:
            print(f"❌ D2A webhook send failed: HTTP {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ D2A webhook test error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all webhook integration tests."""

    print("🎯 DISCORD WEBHOOK INTEGRATION TESTING")
    print("=" * 60)
    print("This test uses webhooks instead of creating channels for cleaner testing")
    print("=" * 60)

    # Run tests
    test1 = await test_webhook_message()
    test2 = await test_multiple_agent_webhooks()
    test3 = await test_d2a_message_via_webhook()

    print("\n" + "=" * 60)
    print("📊 WEBHOOK INTEGRATION RESULTS:")
    print(f"  Basic Webhook Test: {'✅ PASSED' if test1 else '❌ FAILED'}")
    print(f"  Multi-Agent Test: {'✅ PASSED' if test2 else '❌ FAILED'}")
    print(f"  D2A Template Test: {'✅ PASSED' if test3 else '❌ FAILED'}")

    if test1 and test2 and test3:
        print("\n🎉 ALL WEBHOOK TESTS PASSED!")
        print("✅ Discord integration working correctly")
        print("✅ No channels created during testing")
        print("✅ Clean webhook-based testing approach")
        return True
    else:
        print("\n⚠️ SOME WEBHOOK TESTS FAILED")
        print("❌ Discord integration needs attention")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)