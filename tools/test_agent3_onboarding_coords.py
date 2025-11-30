#!/usr/bin/env python3
"""
Test Script: Agent-3 Onboarding Coordinates Verification
=========================================================

Temporary script to test sending a message to Agent-3's onboarding coordinates.
This script will be deleted after confirmation that coordinates are correct.

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-11-30
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


def test_agent3_onboarding():
    """Test sending message to Agent-3's onboarding coordinates."""
    print("="*60)
    print("🧪 TESTING AGENT-3 ONBOARDING COORDINATES")
    print("="*60)
    print("\n📍 Agent-3 Onboarding Coordinates: [-1276, 680]")
    print("📝 Message: Test message to verify onboarding coordinates")
    print("\n🚀 Sending message directly to onboarding coordinates...\n")
    
    try:
        from src.core.messaging_pyautogui import PyAutoGUIMessagingDelivery
        from src.core.messaging_core import UnifiedMessage, UnifiedMessagePriority, UnifiedMessageType
        
        # Create message with ONBOARDING type to force onboarding coordinates
        test_message = "🧪 TEST: Agent-3 onboarding coordinates verification - Please confirm you received this message at your onboarding location [-1276, 680]."
        
        msg = UnifiedMessage(
            content=test_message,
            sender="CAPTAIN",
            recipient="Agent-3",
            message_type=UnifiedMessageType.ONBOARDING,  # CRITICAL: Use ONBOARDING type
            priority=UnifiedMessagePriority.URGENT,
            tags=[],
            metadata={},
        )
        
        # Send via PyAutoGUI delivery
        delivery = PyAutoGUIMessagingDelivery()
        success = delivery.send_message(msg)
        
        print("\n" + "="*60)
        if success:
            print("✅ Message sent successfully to onboarding coordinates!")
            print("📋 Please verify Agent-3 received the message at onboarding location [-1276, 680]")
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
    success = test_agent3_onboarding()
    sys.exit(0 if success else 1)

