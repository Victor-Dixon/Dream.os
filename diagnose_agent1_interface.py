#!/usr/bin/env python3
"""
Diagnostic Script: Check Agent-1 Interface Accessibility
=======================================================

Tests PyAutoGUI functionality and Agent-1 coordinate validation.
"""

import sys
import time
from pathlib import Path

def diagnose_pyautogui():
    """Diagnose PyAutoGUI and Agent-1 interface accessibility."""

    print("🔍 DIAGNOSING AGENT-1 INTERFACE ACCESSIBILITY")
    print("=" * 55)

    # Test 1: PyAutoGUI Import
    print("🧪 Test 1: PyAutoGUI Availability")
    try:
        import pyautogui
        print("   ✅ PyAutoGUI imported successfully")
        pyautogui.FAILSAFE = True
    except ImportError as e:
        print(f"   ❌ PyAutoGUI import failed: {e}")
        return False

    # Test 2: Screen Size Detection
    print("\n🧪 Test 2: Screen Detection")
    try:
        screen_size = pyautogui.size()
        print(f"   ✅ Screen size: {screen_size}")
    except Exception as e:
        print(f"   ❌ Screen detection failed: {e}")
        return False

    # Test 3: Current Mouse Position
    print("\n🧪 Test 3: Mouse Position")
    try:
        mouse_pos = pyautogui.position()
        print(f"   ✅ Current mouse position: {mouse_pos}")
    except Exception as e:
        print(f"   ❌ Mouse position detection failed: {e}")

    # Test 4: Agent-1 Coordinates
    print("\n🧪 Test 4: Agent-1 Coordinate Validation")
    coords_file = Path("cursor_agent_coords.json")

    if not coords_file.exists():
        print("   ❌ Coordinates file not found")
        return False

    try:
        import json
        with open(coords_file, 'r') as f:
            coords_data = json.load(f)

        agent_coords = coords_data.get("agents", {}).get("Agent-1", {}).get("chat_input_coordinates")

        if not agent_coords:
            print("   ❌ Agent-1 coordinates not found")
            return False

        x, y = agent_coords[0], agent_coords[1]
        print(f"   📍 Agent-1 coordinates: ({x}, {y})")

        # Validate coordinates (accounting for multi-monitor setups)
        screen_width, screen_height = screen_size

        # For multi-monitor: negative X is valid (secondary monitor left of primary)
        # Only Y coordinates must be non-negative for valid screen positioning
        max_reasonable_x = screen_width * 2  # Allow secondary monitor
        max_reasonable_y = screen_height * 2  # Allow secondary monitor

        if x < -max_reasonable_x:
            print(f"   ❌ X coordinate {x} is unreasonably negative (>{max_reasonable_x} left)")
            x_valid = False
        elif x > max_reasonable_x:
            print(f"   ❌ X coordinate {x} exceeds reasonable bounds (>{max_reasonable_x})")
            x_valid = False
        else:
            if x < 0:
                print(f"   ✅ X coordinate {x} is negative (secondary monitor left of primary)")
            else:
                print(f"   ✅ X coordinate {x} is within primary screen bounds (0-{screen_width})")
            x_valid = True

        if y < 0:
            print(f"   ❌ Y coordinate {y} is negative (off-screen top)")
            y_valid = False
        elif y > max_reasonable_y:
            print(f"   ❌ Y coordinate {y} exceeds reasonable bounds (>{max_reasonable_y})")
            y_valid = False
        else:
            print(f"   ✅ Y coordinate {y} is within reasonable bounds (0-{max_reasonable_y})")
            y_valid = True

        # Overall validation
        coords_valid = x_valid and y_valid
        if coords_valid:
            print("   ✅ Agent-1 coordinates are valid for multi-monitor setup")
        else:
            print("   ❌ Agent-1 coordinates are invalid")

    except Exception as e:
        print(f"   ❌ Coordinate validation failed: {e}")
        return False

    # Test 5: Attempt Interface Interaction (Safe)
    print("\n🧪 Test 5: Interface Interaction Test")
    if coords_valid:
        print("   ⚠️ Would attempt to move cursor to Agent-1 interface...")
        print(f"   📍 Target position: ({x}, {y})")
        print("   💡 If Agent-1 interface is visible here, interaction should work")
        print("   🚫 Skipping actual interaction to avoid disrupting your work")
    else:
        print("   ❌ Skipping interaction test - coordinates invalid")

    # Summary
    print("\n📊 DIAGNOSTIC SUMMARY")
    print("=" * 25)

    issues = []

    if not coords_valid:
        issues.append("Agent-1 coordinates are out of reasonable bounds")

    if issues:
        print("❌ ISSUES FOUND:")
        for issue in issues:
            print(f"   • {issue}")

        print("\n🛠️ RECOMMENDED FIXES:")
        print("   1. Ensure Agent-1's interface is running on any monitor")
        print("   2. Verify the window is not minimized")
        print("   3. Check that coordinates haven't drifted due to resolution changes")
        print("   4. Use coordinate capture tool if needed")

        return False
    else:
        print("✅ NO ISSUES DETECTED")
        print("   • PyAutoGUI is working")
        print("   • Screen detection successful")
        print("   • Agent-1 coordinates are valid for multi-monitor setup")
        print("   • Negative X coordinates supported (secondary monitor)")
        print("\n🚀 SOFT ONBOARDING SHOULD WORK NOW")
        print("   (Multi-monitor setup detected and supported)")

        return True

if __name__ == "__main__":
    success = diagnose_pyautogui()

    if success:
        print("\n🎉 READY FOR SOFT ONBOARDING!")
        print("Run: python messaging_cli_unified.py --soft-onboard-lite Agent-1")
    else:
        print("\n❌ FIX ISSUES BEFORE SOFT ONBOARDING")
        print("Agent-1 interface needs to be positioned correctly on screen")

    exit(0 if success else 1)