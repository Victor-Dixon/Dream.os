#!/usr/bin/env python3
"""
Agent Coordinate Capture Tool
==============================

Interactive tool to capture and update agent coordinates for PyAutoGUI messaging.

Usage:
    python tools/capture_agent_coordinates.py [--agent Agent-X] [--type chat|onboarding|both]

    Without arguments: Interactive mode - guides through capturing coordinates for all agents
    With --agent: Capture coordinates for specific agent
    With --type: Specify coordinate type (chat, onboarding, or both)
"""

import json
import sys
import time
from pathlib import Path

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    print("❌ PyAutoGUI not available. Install with: pip install pyautogui")
    sys.exit(1)

# Agent order for systematic capture
AGENT_ORDER = [
    "Agent-1", "Agent-2", "Agent-3", "Agent-5",
    "Agent-6", "Agent-7", "Agent-8", "Agent-4"
]

COORD_FILE = Path("cursor_agent_coords.json")


def load_coordinates() -> dict:
    """Load current coordinates from SSOT file."""
    if not COORD_FILE.exists():
        print(f"❌ Coordinate file not found: {COORD_FILE}")
        sys.exit(1)

    with open(COORD_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return data.get("agents", {})


def save_coordinates(coords: dict):
    """Save coordinates to SSOT file."""
    data = {
        "agents": coords
    }

    # Create backup
    backup_file = COORD_FILE.with_suffix('.json.backup')
    if COORD_FILE.exists():
        import shutil
        shutil.copy2(COORD_FILE, backup_file)
        print(f"📋 Backup created: {backup_file}")

    with open(COORD_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Coordinates saved to {COORD_FILE}")


def capture_mouse_position(prompt: str) -> tuple[int, int] | None:
    """Capture current mouse position after user confirmation."""
    print(f"\n{prompt}")
    print("Move mouse to target location and press ENTER when ready...")

    try:
        input()  # Wait for user to position mouse and press Enter
        pos = pyautogui.position()
        print(f"📍 Captured: ({pos.x}, {pos.y})")
        return (pos.x, pos.y)
    except KeyboardInterrupt:
        print("\n❌ Cancelled")
        return None


def capture_single_agent(agent_id: str, coord_type: str, current_coords: dict):
    """Capture coordinates for a single agent."""
    print(f"\n{'='*60}")
    print(f"📌 Capturing coordinates for {agent_id}")
    print(f"{'='*60}")

    # Ensure agent exists in dict
    if agent_id not in current_coords:
        current_coords[agent_id] = {
            "chat_input_coordinates": [0, 0],
            "onboarding_input_coords": [0, 0],
            "description": f"{agent_id} coordinates"
        }

    if coord_type in ["chat", "both"]:
        chat_current = current_coords[agent_id].get('chat_input_coordinates', 'N/A')
        chat_prompt = f"CHAT INPUT for {agent_id} (current: {chat_current})"
        chat_coords = capture_mouse_position(chat_prompt)
        if chat_coords:
            current_coords[agent_id]["chat_input_coordinates"] = list(chat_coords)

    if coord_type in ["onboarding", "both"]:
        onboarding_current = current_coords[agent_id].get('onboarding_input_coords', 'N/A')
        onboarding_prompt = f"ONBOARDING INPUT for {agent_id} (current: {onboarding_current})"
        onboarding_coords = capture_mouse_position(onboarding_prompt)
        if onboarding_coords:
            current_coords[agent_id]["onboarding_input_coords"] = list(onboarding_coords)

    return current_coords


def interactive_capture_all():
    """Interactive mode - capture coordinates for all agents."""
    current_coords = load_coordinates()

    print("\n🐝 AGENT COORDINATE CAPTURE TOOL")
    print("="*60)
    print("This tool will guide you through capturing coordinates for all agents.")
    print("For each agent, position your mouse over the input field and press ENTER.")
    print("\nPress Ctrl+C at any time to cancel and save what you've captured so far.")
    print("="*60)

    try:
        for agent_id in AGENT_ORDER:
            if agent_id not in current_coords:
                print(f"\n⚠️  {agent_id} not found in coordinates file, skipping...")
                continue

            print(f"\n\n📍 Next: {agent_id}")
            print(f"   Current chat: {current_coords[agent_id].get('chat_input_coordinates')}")
            print(f"   Current onboarding: {current_coords[agent_id].get('onboarding_input_coords')}")

            # Capture chat coordinates
            chat_coords = capture_mouse_position(f"CHAT INPUT for {agent_id}")
            if chat_coords:
                current_coords[agent_id]["chat_input_coordinates"] = list(chat_coords)

            # Capture onboarding coordinates
            onboarding_coords = capture_mouse_position(f"ONBOARDING INPUT for {agent_id}")
            if onboarding_coords:
                current_coords[agent_id]["onboarding_input_coords"] = list(onboarding_coords)

            print(f"✅ {agent_id} coordinates captured")

        print("\n" + "="*60)
        print("✅ All coordinates captured!")
        save_coordinates(current_coords)

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        response = input("Save captured coordinates so far? (y/n): ")
        if response.lower() == 'y':
            save_coordinates(current_coords)
            print("✅ Partial coordinates saved")
        else:
            print("❌ Changes discarded")


def interactive_capture_onboarding_only():
    """Interactive mode - capture ONLY onboarding coordinates for all agents."""
    current_coords = load_coordinates()

    print("\n🐝 ONBOARDING COORDINATE CAPTURE TOOL")
    print("="*60)
    print("This tool will capture ONLY onboarding coordinates for all agents.")
    print("For each agent, position your mouse over the onboarding input field and press ENTER.")
    print("\nPress Ctrl+C at any time to cancel and save what you've captured so far.")
    print("="*60)

    try:
        for agent_id in AGENT_ORDER:
            if agent_id not in current_coords:
                print(f"\n⚠️  {agent_id} not found in coordinates file, skipping...")
                continue

            print(f"\n\n📍 Next: {agent_id}")
            onboarding_current = current_coords[agent_id].get('onboarding_input_coords', 'N/A')
            print(f"   Current onboarding: {onboarding_current}")

            # Capture onboarding coordinates only
            onboarding_coords = capture_mouse_position(f"ONBOARDING INPUT for {agent_id}")
            if onboarding_coords:
                current_coords[agent_id]["onboarding_input_coords"] = list(onboarding_coords)
                print(f"✅ {agent_id} onboarding coordinates captured")

        print("\n" + "="*60)
        print("✅ All onboarding coordinates captured!")
        save_coordinates(current_coords)

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        response = input("Save captured onboarding coordinates so far? (y/n): ")
        if response.lower() == 'y':
            save_coordinates(current_coords)
            print("✅ Partial onboarding coordinates saved")
        else:
            print("❌ Changes discarded")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Capture and update agent coordinates for PyAutoGUI messaging"
    )
    parser.add_argument(
        "--agent",
        type=str,
        help="Specific agent to update (e.g., Agent-6)"
    )
    parser.add_argument(
        "--type",
        choices=["chat", "onboarding", "both"],
        default="both",
        help="Coordinate type to capture (default: both)"
    )

    args = parser.parse_args()

    if not PYAUTOGUI_AVAILABLE:
        print("❌ PyAutoGUI not available")
        sys.exit(1)

    if args.agent:
        # Single agent mode
        current_coords = load_coordinates()
        if args.agent not in current_coords:
            print(f"❌ Agent {args.agent} not found in coordinates file")
            sys.exit(1)

        capture_single_agent(args.agent, args.type, current_coords)
        save_coordinates(current_coords)
    else:
        # Interactive mode - all agents
        if args.type == "onboarding":
            interactive_capture_onboarding_only()
        elif args.type == "chat":
            # Would need to implement chat-only mode
            print("❌ Chat-only mode not implemented yet. Use --type both or --agent with --type chat")
            sys.exit(1)
        else:
            interactive_capture_all()


if __name__ == "__main__":
    main()