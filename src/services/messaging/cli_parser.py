#!/usr/bin/env python3
"""
CLI Parser Module - Messaging Infrastructure
=============================================

<!-- SSOT Domain: integration -->

Extracted from messaging_infrastructure.py for V2 compliance.
Handles argument parsing and validation for messaging CLI.

V2 Compliance | Author: Agent-1 | Date: 2025-12-12
"""

from __future__ import annotations

import argparse
from typing import Any

CLI_HELP_EPILOG = """
🐝 SWARM MESSAGING CLI - COMMAND YOUR AGENTS!
==============================================

EXAMPLES:
---------
# Send message to specific agent
python -m src.services.messaging_cli --message "Start survey" --agent Agent-1
# Broadcast to all agents
python -m src.services.messaging_cli --message "SWARM ALERT!" --broadcast
# Send with priority and tags
python -m src.services.messaging_cli --message "URGENT: Fix issue" \\
    --agent Agent-2 --priority urgent --tags bug critical

🐝 WE. ARE. SWARM - COORDINATE THROUGH PYAUTOGUI!
"""


def create_messaging_parser() -> argparse.ArgumentParser:
    """
    Create the argument parser for messaging CLI.
    
    Returns:
        Configured ArgumentParser instance with all messaging CLI arguments.
    """
    parser = argparse.ArgumentParser(
        description="🐝 SWARM Messaging CLI - Command the swarm through PyAutoGUI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=CLI_HELP_EPILOG,
    )

    # Core messaging arguments
    parser.add_argument("--message", "-m", type=str,
                        help="Message content to send")

    parser.add_argument("--agent", "-a", type=str,
                        help="Target agent ID (e.g., Agent-1, Agent-2)")

    parser.add_argument(
        "--broadcast", "-b", action="store_true", help="Broadcast message to all agents"
    )

    # Message options
    parser.add_argument(
        "--priority",
        "-p",
        choices=["normal", "regular", "urgent"],
        default="regular",
        help="Message priority (default: regular). Accepts 'normal' or 'regular' (both are equivalent).",
    )

    parser.add_argument("--tags", "-t", nargs="+",
                        help="Message tags for categorization")

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

    parser.add_argument("--consolidation-batch", type=str,
                        help="Specify consolidation batch ID")

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

    # Hard onboarding flags
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

    # Cycle V2 flags
    parser.add_argument(
        "--cycle-v2",
        action="store_true",
        help="Use CYCLE_V2 template for high-throughput cycle (requires --agent and cycle fields)",
    )
    parser.add_argument(
        "--mission",
        type=str,
        help="Mission statement (single sentence) for CYCLE_V2",
    )
    parser.add_argument(
        "--dod",
        type=str,
        help="Definition of Done (3 bullets max, use \\n for newlines) for CYCLE_V2",
    )
    parser.add_argument(
        "--ssot-constraint",
        type=str,
        help="SSOT constraint (domain) for CYCLE_V2",
    )
    parser.add_argument(
        "--v2-constraint",
        type=str,
        help="V2 constraint (e.g., 'file <400 lines') for CYCLE_V2",
    )
    parser.add_argument(
        "--touch-surface",
        type=str,
        help="Touch surface (files/modules to be changed) for CYCLE_V2",
    )
    parser.add_argument(
        "--validation",
        type=str,
        help="Validation required (tests/lint commands) for CYCLE_V2",
    )
    parser.add_argument(
        "--priority-level",
        type=str,
        default="P1",
        help="Priority level (P0/P1) for CYCLE_V2 (default: P1)",
    )
    parser.add_argument(
        "--handoff",
        type=str,
        help="Handoff expectation (what 'done' looks like) for CYCLE_V2",
    )

    # Infrastructure health monitoring
    parser.add_argument(
        "--infra-health",
        action="store_true",
        help="Check infrastructure health metrics (disk, memory, CPU, browser automation)",
    )

    return parser





