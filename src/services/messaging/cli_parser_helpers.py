#!/usr/bin/env python3
"""
CLI Parser Helpers - Messaging Infrastructure
=============================================

<!-- SSOT Domain: integration -->

Helper functions for CLI argument parser construction.
Extracted from cli_parser.py for V2 compliance.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

from __future__ import annotations

import argparse
from typing import Any


def add_core_messaging_args(parser: argparse.ArgumentParser) -> None:
    """Add core messaging arguments to parser."""
    parser.add_argument("--message", "-m", type=str,
                        help="Message content to send")
    parser.add_argument("--agent", "-a", type=str,
                        help="Target agent ID (e.g., Agent-1, Agent-2)")
    parser.add_argument("--broadcast", "-b", action="store_true",
                        help="Broadcast message to all agents")
    parser.add_argument(
        "--sender",
        type=str,
        help="Explicit sender ID (e.g., Agent-1, CAPTAIN). Overrides AGENT_CONTEXT detection.",
    )


def add_message_options(parser: argparse.ArgumentParser) -> None:
    """Add message option arguments to parser."""
    parser.add_argument(
        "--priority", "-p",
        choices=["normal", "regular", "urgent"],
        default="regular",
        help="Message priority (default: regular). Accepts 'normal' or 'regular' (both are equivalent).",
    )
    parser.add_argument("--tags", "-t", nargs="+",
                        help="Message tags for categorization")
    parser.add_argument("--pyautogui", "--gui", action="store_true",
                        help="Use PyAutoGUI for message delivery")
    parser.add_argument(
        "--category",
        choices=["s2a", "d2a", "c2a", "a2a", "a2c"],
        help=(
            "Override high-level message category for templating "
            "(e.g. 'a2a' for Agent-to-Agent coordination). "
            "Defaults to auto-detected based on sender/recipient."
        ),
    )


def add_coordination_flags(parser: argparse.ArgumentParser) -> None:
    """Add coordination flag arguments to parser."""
    parser.add_argument("--survey-coordination", action="store_true",
                        help="Initiate survey coordination mode")
    parser.add_argument("--consolidation-coordination", action="store_true",
                        help="Initiate consolidation coordination mode")
    parser.add_argument("--consolidation-batch", type=str,
                        help="Specify consolidation batch ID")
    parser.add_argument("--consolidation-status", type=str,
                        help="Specify consolidation status update")


def add_utility_flags(parser: argparse.ArgumentParser) -> None:
    """Add utility flag arguments to parser."""
    parser.add_argument("--coordinates", action="store_true",
                        help="Display agent coordinates and configuration")
    parser.add_argument(
        "--start", nargs="+", type=int, metavar="N",
        help="Start agents (1-8, e.g., --start 1 2 3) - sends to onboarding coordinates",
    )
    parser.add_argument(
        "--save", action="store_true",
        help="Send message to all agents' chat input coords and press Ctrl+Enter to save",
    )
    parser.add_argument("--leaderboard", action="store_true",
                        help="Display the autonomous competition leaderboard")


def add_task_system_flags(parser: argparse.ArgumentParser) -> None:
    """Add task system flag arguments to parser."""
    parser.add_argument("--get-next-task", action="store_true",
                        help="Claim next available assigned task (requires --agent)")
    parser.add_argument("--list-tasks", action="store_true",
                        help="List all available tasks in queue")
    parser.add_argument("--task-status", type=str,
                        metavar="TASK_ID", help="Check status of specific task")
    parser.add_argument("--complete-task", type=str,
                        metavar="TASK_ID", help="Mark task as complete")


def add_onboarding_flags(parser: argparse.ArgumentParser) -> None:
    """Add hard onboarding flag arguments to parser."""
    parser.add_argument("--hard-onboarding", action="store_true",
                        help="Execute hard onboarding protocol (5-step reset) for agent")
    parser.add_argument("--onboarding-file", type=str,
                        help="Path to file containing onboarding message (for hard onboarding)")
    parser.add_argument(
        "--role", type=str, help="Agent role assignment (for hard onboarding with template)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Dry run mode - show what would be done without executing")


def add_cycle_v2_flags(parser: argparse.ArgumentParser) -> None:
    """Add Cycle V2 flag arguments to parser."""
    parser.add_argument(
        "--cycle-v2", action="store_true",
        help="Use CYCLE_V2 template for high-throughput cycle (requires --agent and cycle fields)",
    )
    parser.add_argument("--mission", type=str,
                        help="Mission statement (single sentence) for CYCLE_V2")
    parser.add_argument(
        "--dod", type=str, help="Definition of Done (3 bullets max, use \\n for newlines) for CYCLE_V2")
    parser.add_argument("--ssot-constraint", type=str,
                        help="SSOT constraint (domain) for CYCLE_V2")
    parser.add_argument("--v2-constraint", type=str,
                        help="V2 constraint (e.g., 'file <400 lines') for CYCLE_V2")
    parser.add_argument("--touch-surface", type=str,
                        help="Touch surface (files/modules to be changed) for CYCLE_V2")
    parser.add_argument("--validation", type=str,
                        help="Validation required (tests/lint commands) for CYCLE_V2")
    parser.add_argument("--priority-level", type=str, default="P1",
                        help="Priority level (P0/P1) for CYCLE_V2 (default: P1)")
    parser.add_argument("--handoff", type=str,
                        help="Handoff expectation (what 'done' looks like) for CYCLE_V2")


def add_infrastructure_flags(parser: argparse.ArgumentParser) -> None:
    """Add infrastructure flag arguments to parser."""
    parser.add_argument(
        "--resend-failed", action="store_true",
        help="Resend failed messages from queue (resets failed messages to PENDING for retry)",
    )
    parser.add_argument(
        "--infra-health", action="store_true",
        help="Check infrastructure health metrics (disk, memory, CPU, browser automation)",
    )
    parser.add_argument(
        "--generate-work-resume", action="store_true",
        help="Generate comprehensive work resume for an agent (requires --agent)",
    )
    parser.add_argument(
        "--save-resume", action="store_true",
        help="Save generated work resume to file (use with --generate-work-resume)",
    )
