#!/usr/bin/env python3
"""
Direct PyAutoGUI Delivery - Queue Bypass Test
=============================================

Direct PyAutoGUI message delivery that bypasses the queue system entirely.
This will actually move the mouse and paste messages at agent coordinates.

WARNING: This will control your mouse and keyboard!
Make sure agent windows are positioned correctly before running.

Author: Agent-7 (Web Development Specialist)
Date: 2026-01-09
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def test_direct_pyautogui_delivery():
    """Test direct PyAutoGUI delivery bypassing queue."""
    print("🚨 DIRECT PYAUTOGUI DELIVERY TEST")
    print("⚠️  This will control your mouse and keyboard!")
    print("Make sure agent windows are positioned at their coordinates.")
    print()

    # Import the direct delivery function
    try:
        from src.core.messaging_pyautogui import send_message_pyautogui
        print("✅ Direct PyAutoGUI function imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import direct PyAutoGUI function: {e}")
        return False

    # Test message
    test_message = "DIRECT PYAUTOGUI TEST: This message should appear via actual mouse/keyboard control, not through queue!"
    target_agent = "Agent-6"  # Agent-6 coordinates: (1612, 419)

    print(f"🎯 Target: {target_agent} at coordinates (1612, 419)")
    print(f"📝 Message: {test_message}")
    print()

    # Confirm before proceeding
    response = input("Continue with direct PyAutoGUI delivery? (yes/no): ").strip().lower()
    if response != 'yes':
        print("❌ Test cancelled by user")
        return False

    print("🚀 Executing direct PyAutoGUI delivery...")
    try:
        result = send_message_pyautogui(target_agent, test_message, timeout=30)
        if result:
            print("✅ Direct PyAutoGUI delivery completed successfully!")
            print("   Mouse should have moved to Agent-6 coordinates and pasted the message.")
            return True
        else:
            print("❌ Direct PyAutoGUI delivery failed!")
            return False
    except Exception as e:
        print(f"❌ Direct PyAutoGUI delivery crashed: {e}")
        return False

if __name__ == "__main__":
    success = test_direct_pyautogui_delivery()
    sys.exit(0 if success else 1)