"""
Captain's Tool: Message All Agents
===================================

⚠️ DEPRECATED: This tool has been migrated to tools_v2.
Use 'python -m tools_v2.toolbelt captain.message_all' instead.
This file will be removed in future version.

Migrated to: tools_v2/categories/captain_tools_extension.py → MessageAllAgentsTool
Registry: captain.message_all

Sends messages to all 8 agents (including self!) with one command.
Prevents forgetting to message Captain (Agent-4).

Usage: python tools/captain_message_all_agents.py --message "Check INBOX!" --priority regular

Author: Agent-4 (Captain)
Date: 2025-10-13
Deprecated: 2025-01-27 (Agent-6 - V2 Tools Flattening)
"""

import warnings

warnings.warn(
    "⚠️ DEPRECATED: This tool has been migrated to tools_v2. "
    "Use 'python -m tools_v2.toolbelt msg.broadcast' instead. "
    "This file will be removed in future version.",
    DeprecationWarning,
    stacklevel=2
)

# Legacy compatibility - delegate to tools_v2
# For migration path, use: python -m tools_v2.toolbelt msg.broadcast

import subprocess
import sys

SWARM_AGENTS = [
    "Agent-1",
    "Agent-2",
    "Agent-3",
    "Agent-4",
    "Agent-5",
    "Agent-6",
    "Agent-7",
    "Agent-8",
]


def message_all_agents(message: str, priority: str = "regular", include_captain: bool = True):
    """Send message to all agents including Captain."""
    # Delegate to tools_v2 adapter
    try:
        from tools_v2.categories.messaging_tools import BroadcastTool
        
        tool = BroadcastTool()
        result = tool.execute({
            "message": message,
            "priority": priority,
            "include_captain": include_captain
        }, None)
        
        if result.success:
            print(f"✅ Message broadcast to {len(SWARM_AGENTS)} agents")
            print(f"   Priority: {priority}")
            print(f"   Message: {message[:80]}...")
        else:
            print(f"❌ Error: {result.error_message}")
        
        return result.success
    except ImportError:
        # Fallback to original implementation
        agents_to_message = (
            SWARM_AGENTS if include_captain else [a for a in SWARM_AGENTS if a != "Agent-4"]
        )

        print(f"\n🚀 Messaging {len(agents_to_message)} agents...")
        print(f"Priority: {priority}")
        print(f"Message: {message[:80]}...\n")

        results = {}
        for agent in agents_to_message:
            cmd = [
                "python",
                "src/services/messaging_cli.py",
                "--agent",
                agent,
                "--message",
                message,
                "--priority",
                priority,
                "--pyautogui",
            ]

            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

                if result.returncode == 0:
                    results[agent] = "✅ Sent"
                    print(f"✅ {agent}: Message sent")
                else:
                    results[agent] = f"❌ Failed: {result.stderr[:50]}"
                    print(f"❌ {agent}: Failed - {result.stderr[:50]}")

            except Exception as e:
                results[agent] = f"❌ Error: {str(e)[:50]}"
                print(f"❌ {agent}: Error - {str(e)[:50]}")

        success_count = sum(1 for r in results.values() if r.startswith("✅"))

        print(f"\n{'='*80}")
        print(f"SUMMARY: {success_count}/{len(agents_to_message)} messages sent")
        print(f"{'='*80}\n")

        if success_count == len(agents_to_message):
            print("✅ ALL AGENTS MESSAGED - Swarm activated! 🐝")
        else:
            print(f"⚠️  {len(agents_to_message) - success_count} messages failed")

        return success_count == len(agents_to_message)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Message all agents")
    parser.add_argument("--message", "-m", required=True, help="Message content")
    parser.add_argument("--priority", "-p", default="regular", help="Priority (regular/urgent)")
    parser.add_argument("--no-captain", action="store_true", help="Exclude Captain (Agent-4)")

    args = parser.parse_args()

    message_all_agents(args.message, args.priority, not args.no_captain)
