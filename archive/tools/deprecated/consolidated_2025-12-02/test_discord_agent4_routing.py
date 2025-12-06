#!/usr/bin/env python3
"""
Test Script: Discord Message Routing to Agent-4
================================================

Test script to verify Discord messages route to chat coordinates, not onboarding.
This will help diagnose the routing issue.

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-11-30
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


def test_discord_routing():
    """Test Discord message routing to Agent-4."""
    print("="*60)
    print("🧪 TESTING DISCORD MESSAGE ROUTING TO AGENT-4")
    print("="*60)
    print("\n📍 Agent-4 Coordinates:")
    print("   - Chat: (-308, 1000)")
    print("   - Onboarding: (-304, 680)")
    print("\n🚀 Creating test message with Discord metadata...\n")
    
    try:
        from src.core.messaging_pyautogui import PyAutoGUIMessagingDelivery
        from src.core.messaging_core import UnifiedMessage, UnifiedMessagePriority, UnifiedMessageType
        
        # Create message with Discord metadata (simulating Discord message)
        test_message = "🧪 TEST: Discord message routing test - This should go to CHAT coordinates (-308, 1000), NOT onboarding (-304, 680)."
        
        msg = UnifiedMessage(
            content=test_message,
            sender="CAPTAIN",
            recipient="Agent-4",
            message_type=UnifiedMessageType.CAPTAIN_TO_AGENT,  # Normal message type
            priority=UnifiedMessagePriority.REGULAR,
            tags=[],
            metadata={
                "source": "discord",  # Discord metadata
                "discord_user_id": "123456789",
                "discord_username": "TestUser"
            },
        )
        
        print("📋 Message Details:")
        print(f"   - Recipient: {msg.recipient}")
        print(f"   - Message Type: {msg.message_type}")
        print(f"   - Metadata source: {msg.metadata.get('source')}")
        print(f"   - Has discord_user_id: {msg.metadata.get('discord_user_id') is not None}")
        print("\n🚀 Sending message...\n")
        
        # Send via PyAutoGUI delivery
        delivery = PyAutoGUIMessagingDelivery()
        success = delivery.send_message(msg)
        
        print("\n" + "="*60)
        if success:
            print("✅ Message sent successfully!")
            print("📋 Please verify Agent-4 received the message at:")
            print("   ✅ EXPECTED: Chat coordinates (-308, 1000)")
            print("   ❌ NOT: Onboarding coordinates (-304, 680)")
            print("\n💡 Check the logs above to see which coordinates were used")
        else:
            print("❌ Message send failed")
        print("="*60)
        
        return success
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_discord_routing()
    sys.exit(0 if success else 1)

