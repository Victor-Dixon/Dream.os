#!/usr/bin/env python3
"""
Manual PyAutoGUI Delivery Test - Agent-7
=========================================

Test manual PyAutoGUI message delivery to Agent-7 coordinates.
This script will actually move the mouse and control the keyboard.

WARNING: This will control your mouse and keyboard!
Make sure agent windows are positioned correctly before running.

Agent-7 Coordinates: (653, 940)

Author: Agent-7 (Web Development Specialist)
Date: 2026-01-10
"""

import sys
import time
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)

def test_manual_pyautogui_delivery():
    """Test manual PyAutoGUI delivery to Agent-7 coordinates."""
    print("🚨 MANUAL PYAUTOGUI DELIVERY TEST")
    print("⚠️  This will control your mouse and keyboard!")
    print("Agent-7 coordinates: (653, 940)")
    print()

    try:
        import pyautogui
        import pyperclip
        print("✅ PyAutoGUI and pyperclip imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import required modules: {e}")
        return False

    # Agent-7 coordinates
    agent7_coords = (653, 940)
    test_message = "MANUAL PYAUTOGUI TEST: This message was delivered via actual mouse/keyboard control to Agent-7 coordinates!"

    print(f"🎯 Target coordinates: {agent7_coords}")
    print(f"📝 Test message: {test_message}")
    print()

    # Confirm before proceeding (skip if --full flag used)
    if len(sys.argv) <= 1 or sys.argv[1] != "--full":
        try:
            response = input("Continue with manual PyAutoGUI delivery? (yes/no): ").strip().lower()
        except KeyboardInterrupt:
            print("\n❌ Test cancelled by user")
            return False

        if response != 'yes':
            print("❌ Test cancelled by user")
            return False
    else:
        print("⚠️  Skipping confirmation due to --full flag")

    print("🚀 Executing manual PyAutoGUI delivery sequence...")

    try:
        # Step 1: Move to Agent-7 coordinates
        print("   1. Moving mouse to Agent-7 coordinates...")
        pyautogui.moveTo(agent7_coords[0], agent7_coords[1], duration=1.0)
        time.sleep(0.5)

        # Step 2: Click to focus the input field
        print("   2. Clicking to focus input field...")
        pyautogui.click()
        time.sleep(0.5)

        # Step 3: Clear existing content (Ctrl+A, Delete)
        print("   3. Clearing existing content...")
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyautogui.press('delete')
        time.sleep(0.5)

        # Step 4: Create new tab/window (Ctrl+T)
        print("   4. Creating new tab/window...")
        pyautogui.hotkey('ctrl', 't')
        time.sleep(1.0)  # Wait for tab to load

        # Step 5: Copy message to clipboard and paste
        print("   5. Pasting test message...")
        pyperclip.copy(test_message)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)

        # Step 6: Send message (Enter)
        print("   6. Sending message...")
        pyautogui.press('enter')

        print("✅ Manual PyAutoGUI delivery completed successfully!")
        print("   Mouse moved to Agent-7 coordinates and message was pasted.")
        print("   Check Agent-7's chat interface for the test message.")

        return True

    except Exception as e:
        print(f"❌ Manual PyAutoGUI delivery failed: {e}")
        return False

def test_coordinate_validation():
    """Test coordinate validation without actual mouse movement."""
    print("🧪 Testing coordinate validation (no mouse movement)...")

    try:
        from src.core.messaging_pyautogui import PyAutoGUIMessagingDelivery

        delivery = PyAutoGUIMessagingDelivery()

        # Test Agent-7 coordinates
        agent7_coords = (653, 940)
        is_valid = delivery.validate_coordinates("Agent-7", agent7_coords)

        if is_valid:
            print("✅ Agent-7 coordinates validated successfully")
            return True
        else:
            print("❌ Agent-7 coordinates validation failed")
            return False

    except Exception as e:
        print(f"❌ Coordinate validation test failed: {e}")
        return False

def main():
    """Main test execution."""
    import sys

    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--full":
        print("🚨 Running FULL MANUAL PYAUTOGUI DELIVERY TEST")
        print("⚠️  This will control your mouse and keyboard!")
        success = test_manual_pyautogui_delivery()
    else:
        print("🧪 Running COORDINATE VALIDATION TEST (safe)")
        success = test_coordinate_validation()

    print("\n" + "="*60)
    if success:
        print("🎉 TEST PASSED")
    else:
        print("💥 TEST FAILED")
    print("="*60)

    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)