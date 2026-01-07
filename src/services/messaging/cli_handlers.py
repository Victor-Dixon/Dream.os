#!/usr/bin/env python3
"""
CLI Handlers Module - Messaging Infrastructure
==============================================

<!-- SSOT Domain: integration -->

CLI command handlers extracted from messaging_infrastructure.py for V2 compliance.
Handles all CLI command execution logic.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

from __future__ import annotations

import logging
import time
from datetime import datetime
from typing import Any

from src.core.constants.agent_constants import AGENT_LIST as SWARM_AGENTS
from src.core.coordinate_loader import get_coordinate_loader
from src.core.gamification.autonomous_competition_system import get_competition_system
from src.core.messaging_core import UnifiedMessagePriority
from src.core.messaging_models_core import MessageCategory, MESSAGE_TEMPLATES

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    pyautogui = None


from .coordination_handlers import MessageCoordinator
from .delivery_handlers import send_message_to_onboarding_coords

logger = logging.getLogger(__name__)


def handle_robinhood_stats() -> int:
    """Handle Robinhood statistics command."""
    try:
        # Import here to avoid circular imports
        import subprocess
        import sys
        from pathlib import Path

        # Path to the robinhood stats tool
        tool_path = Path(__file__).parent.parent.parent.parent / "tools" / "robinhood_stats_2026.py"

        if not tool_path.exists():
            print(f"❌ Robinhood stats tool not found at: {tool_path}")
            return 1

        # Run the tool
        result = subprocess.run([sys.executable, str(tool_path)], cwd=Path.cwd())

        return result.returncode

    except Exception as e:
        logger.error(f"Error handling Robinhood stats: {e}")
        print(f"❌ Error accessing Robinhood statistics: {e}")
        return 1


def handle_cycle_v2_message(args, parser) -> int:
    """Handle CYCLE_V2 message sending with template."""
    try:
        from .cli_handler_helpers import (
            send_cycle_v2_message,
            validate_cycle_v2_fields,
        )

        if not args.agent:
            print("❌ ERROR: --agent required for --cycle-v2")
            parser.print_help()
            return 1
        is_valid, missing = validate_cycle_v2_fields(args)
        if not is_valid:
            print(f"❌ ERROR: Missing required CYCLE_V2 fields: {', '.join(missing)}")
            print("Required: --mission, --dod, --ssot-constraint, --v2-constraint, --touch-surface, --validation, --handoff")
            return 1
        return send_cycle_v2_message(args)

    except Exception as e:
        logger.error(f"CYCLE_V2 message handling error: {e}")
        import traceback
        traceback.print_exc()
        return 1


def handle_message(args, parser) -> int:
    """Handle message sending."""
    try:
        from .cli_handler_helpers import (
            normalize_priority,
            route_message_delivery,
        )

        if getattr(args, "cycle_v2", False):
            return handle_cycle_v2_message(args, parser)
        if not args.agent and not args.broadcast:
            print("❌ ERROR: Either --agent or --broadcast must be specified")
            parser.print_help()
            return 1
        priority = normalize_priority(args.priority)
        stalled = getattr(args, "stalled", False)
        return route_message_delivery(args, priority, stalled)

    except Exception as e:
        logger.error(f"Message handling error: {e}")
        return 1


def handle_survey() -> int:
    """Handle survey coordination initiation."""
    try:
        if MessageCoordinator.coordinate_survey():
            print("✅ Survey coordination initiated successfully")
            return 0
        else:
            print("❌ Survey coordination failed")
            return 1
    except Exception as e:
        logger.error(f"Survey coordination error: {e}")
        return 1


def handle_consolidation(args) -> int:
    """Handle consolidation coordination."""
    try:
        if MessageCoordinator.coordinate_consolidation(
            args.consolidation_batch, args.consolidation_status
        ):
            print("✅ Consolidation coordination successful")
            return 0
        else:
            print("❌ Consolidation coordination failed")
            return 1
    except Exception as e:
        logger.error(f"Consolidation coordination error: {e}")
        return 1


def handle_coordinates() -> int:
    """Display agent coordinates."""
    try:
        coord_loader = get_coordinate_loader()
        print("\n🐝 SWARM AGENT COORDINATES")
        print("=" * 50)
        for agent in SWARM_AGENTS:
            chat_coords = coord_loader.get_chat_coordinates(agent)
            onboard_coords = coord_loader.get_onboarding_coordinates(agent)
            print(f"\n{agent}:")
            print(f"  Chat:      {chat_coords}")
            print(f"  Onboarding: {onboard_coords}")
        print("\n" + "=" * 50)
        return 0
    except Exception as e:
        logger.error(f"Coordinates display error: {e}")
        return 1


def handle_start_agents(args) -> int:
    """Handle starting agents via onboarding coordinates (mode-aware)."""
    try:
        from src.core.agent_mode_manager import get_active_agents, is_agent_active
        
        agent_numbers = args.start
        message = args.message if hasattr(
            args, "message") and args.message else "START"
        
        # Get active agents for current mode
        active_agents = get_active_agents()
        print(f"📋 Mode-aware: Active agents: {', '.join(active_agents)}")

        for num in agent_numbers:
            agent_id = f"Agent-{num}"
            # Check if agent is active in current mode
            if not is_agent_active(agent_id):
                print(f"⚠️  Agent {agent_id} is not active in current mode (skipping)")
                continue

            if send_message_to_onboarding_coords(agent_id, message):
                print(f"✅ Started {agent_id}")
            else:
                print(f"❌ Failed to start {agent_id}")

        return 0
    except Exception as e:
        logger.error(f"Start agents error: {e}")
        return 1


def handle_save(args, parser) -> int:
    """Handle save operation (Ctrl+Enter to all agents)."""
    try:
        if not PYAUTOGUI_AVAILABLE:
            print("❌ ERROR: PyAutoGUI not available - cannot execute save operation")
            return 1

        if not args.message:
            print("❌ ERROR: --message required for save operation")
            return 1

        coord_loader = get_coordinate_loader()
        for agent in SWARM_AGENTS:
            try:
                chat_coords = coord_loader.get_chat_coordinates(agent)
                pyautogui.click(chat_coords[0], chat_coords[1])
                time.sleep(0.2)
                pyautogui.write(args.message, interval=0.01)
                pyautogui.hotkey("ctrl", "enter")
                print(f"✅ Saved to {agent}")
                time.sleep(0.5)
            except Exception as e:
                print(f"❌ Failed to save to {agent}: {e}")

        return 0
    except Exception as e:
        logger.error(f"Save operation error: {e}")
        return 1


def handle_leaderboard() -> int:
    """Display the autonomous competition leaderboard."""
    try:
        competition_system = get_competition_system()
        leaderboard = competition_system.get_leaderboard()

        print("\n🏆 AUTONOMOUS COMPETITION LEADERBOARD")
        print("=" * 60)
        for rank, entry in enumerate(leaderboard, start=1):
            agent = entry["agent_id"]
            score = entry["score"]
            completed = entry.get("contracts_completed", 0)
            print(f"{rank}. {agent:10s} - {score:5d} pts ({completed} contracts)")
        print("=" * 60)
        return 0
    except Exception as e:
        logger.error(f"Leaderboard error: {e}")
        print("❌ Failed to display leaderboard")
        return 1

