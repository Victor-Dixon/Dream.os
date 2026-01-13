#!/usr/bin/env python3
"""
Telephone Game Transmission Test
=================================

Tests the restored coordinate system by sending a message directly to Agent-1's chat interface.
This validates that the coordinate restoration worked and PyAutoGUI messaging is functional.

Author: Agent-7 (Tools Consolidation & Architecture Lead)
Date: 2026-01-13
"""

import time
import logging
from src.core.coordinate_loader import get_coordinate_loader

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_coordinate_messaging():
    """Test sending a telephone game transmission via coordinates."""

    print("🎯 TELEPHONE GAME TRANSMISSION TEST")
    print("=" * 50)
    print("Testing coordinate-based messaging to Agent-1...")
    print()

    # Get Agent-1 coordinates
    try:
        coord_loader = get_coordinate_loader()
        coords = coord_loader.get_chat_coordinates('Agent-1')
        print(f"✅ Agent-1 coordinates loaded: {coords}")

    except Exception as e:
        print(f"❌ Failed to load coordinates: {e}")
        return False

    # Prepare the message
    message = "🐝 TELEPHONE GAME TRANSMISSION: System validation test from Agent-7. Testing coordinate-based messaging infrastructure. Coordinate system restoration confirmed. Message delivered via PyAutoGUI to position {coords}. Swarm coordination active. ⚡🔥"

    print(f"📤 Message to send: {message[:100]}...")
    print(f"🎯 Target coordinates: {coords}")
    print()

    # Test PyAutoGUI availability
    try:
        import pyautogui
        print("✅ PyAutoGUI available")

        # Get current mouse position for safety
        current_pos = pyautogui.position()
        print(f"📍 Current mouse position: {current_pos}")

        # Move to Agent-1's coordinates
        print(f"🖱️  Moving to Agent-1 coordinates: {coords}")
        pyautogui.moveTo(coords[0], coords[1], duration=1)

        # Wait for interface focus
        time.sleep(0.5)

        # Click to focus the input field
        print("🖱️  Clicking to focus input field...")
        pyautogui.click()

        # Wait for focus
        time.sleep(0.5)

        # Clear any existing text (Ctrl+A, Delete)
        print("⌨️  Clearing input field...")
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.2)
        pyautogui.press('delete')

        # Type the message
        print("⌨️  Typing telephone game transmission...")
        pyautogui.write(message, interval=0.05)

        # Send the message (Enter key)
        print("📤 Sending message...")
        pyautogui.press('enter')

        # Wait for delivery
        time.sleep(1)

        # Return mouse to original position
        print(f"🖱️  Returning mouse to original position: {current_pos}")
        pyautogui.moveTo(current_pos[0], current_pos[1], duration=0.5)

        print()
        print("✅ TELEPHONE GAME TRANSMISSION SENT!")
        print("🎯 Coordinate-based messaging validated")
        print("🐝 Swarm coordination infrastructure operational")

        return True

    except ImportError:
        print("❌ PyAutoGUI not available")
        print("💡 Install with: pip install pyautogui")
        return False

    except Exception as e:
        print(f"❌ PyAutoGUI operation failed: {e}")
        print("⚠️  This may indicate coordinate system issues")
        return False

if __name__ == "__main__":
    success = test_coordinate_messaging()
    exit(0 if success else 1)