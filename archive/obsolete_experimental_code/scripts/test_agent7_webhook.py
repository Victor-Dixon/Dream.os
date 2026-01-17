#!/usr/bin/env python3
"""Test Agent-7 webhook integration"""

import os
import requests
import json
from datetime import datetime

def test_agent_webhook(agent_number):
    """Test a specific agent webhook"""

    webhook_env_var = f'DISCORD_AGENT{agent_number}_WEBHOOK_URL'
    webhook_url = os.getenv(webhook_env_var)

    if not webhook_url:
        print(f"❌ {webhook_env_var} not found")
        return False

    try:
        # Create test message
        test_message = {
            "content": f"🤖 Agent-{agent_number} Webhook Test",
            "embeds": [{
                "title": f"Agent {agent_number} Integration Test",
                "description": f"Testing webhook connectivity for Agent-{agent_number}",
                "color": 0x00ff00,
                "fields": [
                    {
                        "name": "Timestamp",
                        "value": datetime.now().isoformat(),
                        "inline": True
                    },
                    {
                        "name": "Status",
                        "value": "✅ Webhook Connected",
                        "inline": True
                    }
                ],
                "footer": {
                    "text": "Agent Cellphone V2 - Discord Integration"
                }
            }]
        }

        # Send webhook request
        response = requests.post(
            webhook_url,
            json=test_message,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )

        if response.status_code == 204:
            print(f"✅ Agent-{agent_number} webhook test successful!")
            print(f"   📨 Message sent to Discord channel")
            return True
        else:
            print(f"❌ Agent-{agent_number} webhook failed: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Agent-{agent_number} webhook error: {e}")
        return False

def main():
    print("🧪 TESTING AGENT WEBHOOK INTEGRATION")
    print("=" * 50)

    # Load environment variables
    from pathlib import Path
    if Path('.env').exists():
        import dotenv
        dotenv.load_dotenv()

    # Test Agent-7 specifically (as mentioned by user)
    print("🎯 Testing Agent-7 Webhook")
    print("-" * 30)

    agent7_success = test_agent_webhook(7)

    if agent7_success:
        print("\n✅ Agent-7 webhook is working correctly!")
        print("🐝 Agent-7 can now participate in swarm coordination")
    else:
        print("\n❌ Agent-7 webhook test failed")
        print("💡 Check webhook URL and Discord permissions")

    # Test other agents briefly
    print("\n🔍 Testing Other Agent Webhooks")
    print("-" * 30)

    other_agents = [1, 2, 3, 4]
    working_agents = []

    for agent_num in other_agents:
        if test_agent_webhook(agent_num):
            working_agents.append(agent_num)

    print(f"\n📊 Agent webhook status: {len(working_agents)}/{len(other_agents)} working")
    print(f"🤖 Total functional agents: {len(working_agents) + (1 if agent7_success else 0)}/5")

    if agent7_success and len(working_agents) >= 3:  # At least agents 1,2,3,4,7 working
        print("\n🎉 SWARM COORDINATION READY!")
        print("   ✅ Multiple agents can communicate via Discord")
        print("   ✅ Agent-7 is integrated and operational")
        print("   🚀 Ready for multi-agent collaboration")
        return True
    else:
        print("\n⚠️ Limited agent connectivity detected")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)