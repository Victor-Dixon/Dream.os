#!/usr/bin/env python3
"""
Verbose PyAutoGUI Delivery Test
================================

Tests message delivery with detailed logging to see what's actually happening.
"""
import sys
import time
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pyautogui
import pyperclip

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_delivery():
    """Test delivery with verbose logging."""
    coords = (-1269, 496)
    message = "VERBOSE TEST - Check if this appears in Agent-1 chat input"
    
    print("=" * 60)
    print("Verbose PyAutoGUI Delivery Test")
    print("=" * 60)
    print(f"Coordinates: {coords}")
    print(f"Message: {message}")
    print()
    
    try:
        # Check screen
        screen = pyautogui.size()
        print(f"Screen size: {screen}")
        print(f"Coordinates on primary screen: {coords[0] >= 0 and coords[0] <= screen.width}")
        print()
        
        # Step 1: Move to coordinates
        print("Step 1: Moving to coordinates...")
        pyautogui.moveTo(coords[0], coords[1], duration=0.5)
        current_pos = pyautogui.position()
        print(f"  Current position: {current_pos}")
        print(f"  Target: {coords}")
        print(f"  Match: {abs(current_pos.x - coords[0]) < 5 and abs(current_pos.y - coords[1]) < 5}")
        print()
        
        # Step 2: Click to focus
        print("Step 2: Clicking to focus...")
        pyautogui.click()
        time.sleep(1.0)
        print("  Clicked")
        print()
        
        # Step 3: Clear text
        print("Step 3: Clearing existing text...")
        pyautogui.hotkey("ctrl", "a")
        time.sleep(0.2)
        pyautogui.press("delete")
        time.sleep(0.3)
        print("  Cleared")
        print()
        
        # Step 4: Copy to clipboard
        print("Step 4: Copying to clipboard...")
        pyperclip.copy(message)
        time.sleep(0.5)
        clipboard_check = pyperclip.paste()
        print(f"  Clipboard contains: {clipboard_check[:50]}...")
        print(f"  Match: {clipboard_check == message}")
        print()
        
        # Step 5: Paste
        print("Step 5: Pasting message...")
        pyautogui.hotkey("ctrl", "v")
        time.sleep(1.0)
        print("  Pasted")
        print()
        
        # Step 6: Send
        print("Step 6: Sending message (pressing Enter)...")
        pyautogui.press("enter")
        time.sleep(1.0)
        print("  Enter pressed")
        print()
        
        print("=" * 60)
        print("✅ Test complete!")
        print("=" * 60)
        print("CHECK: Did the message appear in Agent-1's chat input?")
        print("If not, the coordinates might be wrong or window not focused.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_delivery()
    sys.exit(0 if success else 1)

