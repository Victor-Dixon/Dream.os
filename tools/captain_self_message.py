"""
Captain's Tool: Self-Message Reminder
======================================

⚠️ DEPRECATED: This tool has been migrated to tools_v2.
Use 'python -m tools_v2.toolbelt captain.self_message' instead.
This file will be removed in future version.

Migrated to: tools_v2/categories/captain_tools_extension.py → SelfMessageTool
Registry: captain.self_message

Sends a message to Agent-4 (Captain) as a reminder.
CRITICAL: Captain is an agent too and needs prompts!

Usage: python tools/captain_self_message.py --message "Start your task!" --priority regular

Author: Agent-4 (Captain)
Date: 2025-10-13
Deprecated: 2025-01-27 (Agent-6 - V2 Tools Flattening)
"""

import warnings

warnings.warn(
    "⚠️ DEPRECATED: This tool has been migrated to tools_v2. "
    "Use 'python -m tools_v2.toolbelt msg.send' with agent Agent-4 instead. "
    "This file will be removed in future version.",
    DeprecationWarning,
    stacklevel=2
)

# Legacy compatibility - delegate to tools_v2
# For migration path, use: python -m tools_v2.toolbelt msg.send

import subprocess
import sys


def send_self_message(message: str, priority: str = "regular"):
    """
    Send message to Captain (Agent-4).

    CRITICAL REMINDER: Captain is Agent-4 and needs prompts to run!
    "Prompts are gas - even for Captain!"
    """
    # Delegate to tools_v2 adapter
    try:
        from tools_v2.categories.messaging_tools import SendMessageTool
        
        tool = SendMessageTool()
        result = tool.execute({
            "agent_id": "Agent-4",
            "message": f"[SELF-REMINDER] {message}",
            "priority": priority
        }, None)
        
        if result.success:
            print("\n⛽ CAPTAIN SELF-MESSAGE")
            print("=" * 60)
            print("Reminder: Captain IS Agent-4 - needs prompts too!")
            print(f"Message: {message}")
            print(f"Priority: {priority}")
            print("✅ Self-message sent successfully!")
            print("⛽ Captain activated by own prompt!\n")
        else:
            print(f"❌ Error: {result.error_message}")
        
        return result.success
    except ImportError:
        # Fallback to original implementation
        print("\n⛽ CAPTAIN SELF-MESSAGE")
        print("=" * 60)
        print("Reminder: Captain IS Agent-4 - needs prompts too!")
        print(f"Message: {message}")
        print(f"Priority: {priority}")
        print("=" * 60 + "\n")

        cmd = [
            "python",
            "src/services/messaging_cli.py",
            "--agent",
            "Agent-4",
            "--message",
            f"[SELF-REMINDER] {message}",
            "--priority",
            priority,
            "--pyautogui",
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                print("✅ Self-message sent successfully!")
                print("⛽ Captain activated by own prompt!\n")
                return True
            else:
                print(f"❌ Failed: {result.stderr}")
                return False

        except Exception as e:
            print(f"❌ Error: {e}")
            return False


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Send self-message to Captain")
    parser.add_argument("--message", "-m", required=True, help="Message content")
    parser.add_argument("--priority", "-p", default="regular", help="Priority (regular/urgent)")

    args = parser.parse_args()

    send_self_message(args.message, args.priority)
