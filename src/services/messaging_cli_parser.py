"""
Messaging CLI Parser Module
Handles argument parsing for messaging CLI

<!-- SSOT Domain: communication -->
"""

import argparse

CLI_HELP_EPILOG = """
🐝 SWARM MESSAGING CLI - COMMAND YOUR AGENTS!
==============================================

EXAMPLES:
--------
# Send message to specific agent
python -m src.services.messaging_cli --message "Start survey" --agent Agent-1
# Broadcast to all agents
python -m src.services.messaging_cli --message "SWARM ALERT!" --broadcast
# Send with priority and tags
python -m src.services.messaging_cli --message "URGENT: Fix issue" \\
    --agent Agent-2 --priority urgent --tags bug critical

# V3 Enhanced Features
python -m src.services.messaging_cli --verify-delivery    # Check all deliveries
python -m src.services.messaging_cli --clean-queue        # Remove system messages
python -m src.services.messaging_cli --reset-stuck        # Reset stuck messages
python -m src.services.messaging_cli --queue-stats        # Show statistics
python -m src.services.messaging_cli --health-check       # System health check
python -m src.services.messaging_cli --process-workspaces # Clean all workspaces

🐝 WE. ARE. SWARM - COORDINATE THROUGH PYAUTOGUI!
"""


def create_messaging_parser() -> argparse.ArgumentParser:
    """Create the argument parser for messaging CLI."""
    parser = argparse.ArgumentParser(
        description="🐝 SWARM Messaging CLI - Command the swarm through PyAutoGUI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=CLI_HELP_EPILOG,
    )

    # Core messaging arguments
    parser.add_argument("--message", "-m", type=str, help="Message content to send")

    parser.add_argument("--agent", "-a", type=str, help="Target agent ID (e.g., Agent-1, Agent-2)")

    parser.add_argument(
        "--broadcast", "-b", action="store_true", help="Broadcast message to all agents"
    )

    # Message options
    parser.add_argument(
        "--priority",
        "-p",
        choices=["normal", "regular", "urgent"],
        default="regular",
        help="Message priority (default: regular). Accepts 'normal' or 'regular' (both are equivalent). Urgent adds 'URGENT MESSAGE' prefix but uses regular enter.",
    )

    parser.add_argument(
        "--stalled",
        action="store_true",
        help="Use Ctrl+Enter to send (for stalled agents). Overrides normal enter behavior.",
    )

    parser.add_argument("--tags", "-t", nargs="+", help="Message tags for categorization")

    # PyAutoGUI options
    parser.add_argument(
        "--pyautogui", "--gui", action="store_true", help="Use PyAutoGUI for message delivery"
    )

    # Survey coordination flags
    parser.add_argument(
        "--survey-coordination", action="store_true", help="Initiate survey coordination mode"
    )

    parser.add_argument(
        "--consolidation-coordination",
        action="store_true",
        help="Initiate consolidation coordination mode",
    )

    parser.add_argument("--consolidation-batch", type=str, help="Specify consolidation batch ID")

    parser.add_argument(
        "--consolidation-status", type=str, help="Specify consolidation status update"
    )

    # Coordinate display
    parser.add_argument(
        "--coordinates", action="store_true", help="Display agent coordinates and configuration"
    )

    # Agent start flag
    parser.add_argument(
        "--start",
        nargs="+",
        type=int,
        metavar="N",
        help="Start agents (1-8, e.g., --start 1 2 3) - sends to onboarding coordinates",
    )

    # V3 Enhanced Features
    parser.add_argument(
        "--verify-delivery",
        action="store_true",
        help="Verify delivery status for all agents (V3)",
    )

    parser.add_argument(
        "--clean-queue",
        action="store_true",
        help="Clean system messages from queue (V3)",
    )

    parser.add_argument(
        "--reset-stuck",
        action="store_true",
        help="Reset stuck messages to PENDING (V3)",
    )

    parser.add_argument(
        "--queue-stats",
        action="store_true",
        help="Show comprehensive queue statistics (V3)",
    )

    parser.add_argument(
        "--health-check",
        action="store_true",
        help="Perform full messaging system health check (V3)",
    )

    parser.add_argument(
        "--process-workspaces",
        action="store_true",
        help="Process all agent workspaces for cleanup (V3)",
    )

    parser.add_argument(
        "--archive-old",
        type=int,
        metavar="DAYS",
        help="Archive messages older than DAYS (default: 30)",
    )

    parser.add_argument(
        "--save",
        action="store_true",
        help="Send message to all agents' chat input coords and press Ctrl+Enter to save",
    )

    parser.add_argument(
        "--leaderboard",
        action="store_true",
        help="Display the autonomous competition leaderboard",
    )

    # Task system flags (SSOT Blocker Resolution - Agent-8)
    parser.add_argument(
        "--get-next-task",
        action="store_true",
        help="Claim next available assigned task (requires --agent)",
    )

    parser.add_argument(
        "--list-tasks",
        action="store_true",
        help="List all available tasks in queue",
    )

    parser.add_argument(
        "--task-status",
        type=str,
        metavar="TASK_ID",
        help="Check status of specific task",
    )

    parser.add_argument(
        "--complete-task",
        type=str,
        metavar="TASK_ID",
        help="Mark task as complete",
    )

    # Hard onboarding flag
    parser.add_argument(
        "--hard-onboarding",
        action="store_true",
        help="Execute hard onboarding protocol (5-step reset) for agent",
    )

    parser.add_argument(
        "--onboarding-file",
        type=str,
        help="Path to file containing onboarding message (for hard onboarding)",
    )

    parser.add_argument(
        "--role",
        type=str,
        help="Agent role assignment (for hard onboarding with template)",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Dry run mode - show what would be done without executing",
    )

    return parser
