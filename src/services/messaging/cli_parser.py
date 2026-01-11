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

from .cli_parser_helpers import (
    add_core_messaging_args,
    add_coordination_flags,
    add_cycle_v2_flags,
    add_infrastructure_flags,
    add_message_options,
    add_onboarding_flags,
    add_task_system_flags,
    add_utility_flags,
)

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

    add_core_messaging_args(parser)
    add_message_options(parser)
    add_coordination_flags(parser)
    add_utility_flags(parser)
    add_task_system_flags(parser)
    add_onboarding_flags(parser)
    add_cycle_v2_flags(parser)
    add_infrastructure_flags(parser)

    return parser





