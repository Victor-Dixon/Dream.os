#!/usr/bin/env python3
"""
Two Agent Setup Example
=======================

This example demonstrates how to set up and coordinate two agents in the swarm.
It shows basic agent initialization, messaging, and coordination patterns.

Usage:
    python examples/two_agent_setup.py

Requirements:
    - .env file with DISCORD_BOT_TOKEN and DISCORD_GUILD_ID
    - Two agent workspaces (Agent-1 and Agent-2)
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.services.messaging_cli import MessagingCLI
from src.core.messaging_core import send_message, UnifiedMessageType, UnifiedMessagePriority
from src.services.unified_messaging_service import UnifiedMessagingService


async def setup_two_agents():
    """
    Demonstrate setting up and coordinating two agents.

    This example shows:
    1. Agent initialization verification
    2. Basic messaging between agents
    3. Status coordination
    4. Task assignment and completion
    """
    print("🐝 TWO AGENT SETUP EXAMPLE")
    print("=" * 50)

    # Initialize messaging service
    messaging_service = UnifiedMessagingService()
    print("✅ Messaging service initialized")

    # Verify agent workspaces exist
    agent1_workspace = Path("agent_workspaces/Agent-1")
    agent2_workspace = Path("agent_workspaces/Agent-2")

    if not agent1_workspace.exists():
        print(f"❌ Agent-1 workspace not found at {agent1_workspace}")
        return

    if not agent2_workspace.exists():
        print(f"❌ Agent-2 workspace not found at {agent2_workspace}")
        return

    print("✅ Agent workspaces verified")

    # Send initialization messages
    print("\n📨 Sending initialization messages...")

    # Agent-1 initialization
    init_msg_1 = await messaging_service.send_message(
        agent="Agent-1",
        message="SYSTEM: Agent-1 initialized for two-agent coordination demo. Ready for task assignment.",
        priority="regular",
        use_pyautogui=True,
        message_category="c2a"
    )
    print(f"✅ Agent-1 initialization: {'Success' if init_msg_1 else 'Failed'}")

    # Agent-2 initialization
    init_msg_2 = await messaging_service.send_message(
        agent="Agent-2",
        message="SYSTEM: Agent-2 initialized for two-agent coordination demo. Ready for task assignment.",
        priority="regular",
        use_pyautogui=True,
        message_category="c2a"
    )
    print(f"✅ Agent-2 initialization: {'Success' if init_msg_2 else 'Failed'}")

    # Demonstrate agent-to-agent communication
    print("\n🤝 Demonstrating agent-to-agent communication...")

    # Agent-1 to Agent-2
    a2a_msg_1 = await messaging_service.send_message(
        agent="Agent-2",
        message="[A2A] Agent-1: Hello Agent-2! Let's coordinate on this task.",
        priority="regular",
        use_pyautogui=True,
        message_category="a2a"
    )
    print(f"✅ Agent-1 → Agent-2 message: {'Success' if a2a_msg_1 else 'Failed'}")

    # Agent-2 to Agent-1
    a2a_msg_2 = await messaging_service.send_message(
        agent="Agent-1",
        message="[A2A] Agent-2: Acknowledged Agent-1! I'm ready to collaborate.",
        priority="regular",
        use_pyautogui=True,
        message_category="a2a"
    )
    print(f"✅ Agent-2 → Agent-1 message: {'Success' if a2a_msg_2 else 'Failed'}")

    # Demonstrate task assignment
    print("\n📋 Demonstrating task assignment...")

    task_assignment = await messaging_service.send_message(
        agent="Agent-1",
        message="""TASK ASSIGNMENT: Code Review Lead
Assigned tasks: Review Agent-2's recent commits, provide feedback, suggest improvements
Timeline: Complete by end of day
Priority: P1 - High for code quality
Capabilities required: Code review, Python expertise, constructive feedback
Coordinate with: Agent-2 for clarification questions""",
        priority="high",
        use_pyautogui=True,
        message_category="c2a"
    )
    print(f"✅ Task assignment to Agent-1: {'Success' if task_assignment else 'Failed'}")

    # Demonstrate status check
    print("\n📊 Demonstrating status coordination...")

    status_request = await messaging_service.send_message(
        agent="Agent-1",
        message="STATUS REQUEST: Please provide current task status and any blockers.",
        priority="regular",
        use_pyautogui=True,
        message_category="c2a"
    )
    print(f"✅ Status request to Agent-1: {'Success' if status_request else 'Failed'}")

    print("\n🎉 Two-agent setup demonstration complete!")
    print("\n💡 Next steps:")
    print("   1. Check agent inboxes for received messages")
    print("   2. Agents will respond through the messaging system")
    print("   3. Monitor agent_workspaces/*/inbox/ for responses")
    print("   4. Use 'python -m src.services.messaging_cli --queue-stats' to monitor")

    return True


async def main():
    """Main entry point."""
    try:
        success = await setup_two_agents()
        if success:
            print("\n✅ EXAMPLE COMPLETED SUCCESSFULLY")
            return 0
        else:
            print("\n❌ EXAMPLE FAILED")
            return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    print("\n🐝 WE. ARE. SWARM. ⚡️🔥")
    sys.exit(exit_code)