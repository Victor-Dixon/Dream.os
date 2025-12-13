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

import pyautogui

from .coordination_handlers import MessageCoordinator
from .delivery_handlers import send_message_to_onboarding_coords

logger = logging.getLogger(__name__)


def handle_cycle_v2_message(args, parser) -> int:
    """Handle CYCLE_V2 message sending with template."""
    try:
        if not args.agent:
            print("❌ ERROR: --agent required for --cycle-v2")
            parser.print_help()
            return 1

        # Validate required fields
        required_fields = {
            "mission": args.mission,
            "dod": args.dod,
            "ssot_constraint": args.ssot_constraint,
            "v2_constraint": args.v2_constraint,
            "touch_surface": args.touch_surface,
            "validation": args.validation,
            "handoff": args.handoff,
        }

        missing = [k for k, v in required_fields.items() if not v]
        if missing:
            print(
                f"❌ ERROR: Missing required CYCLE_V2 fields: {', '.join(missing)}")
            print("Required: --mission, --dod, --ssot-constraint, --v2-constraint, --touch-surface, --validation, --handoff")
            return 1

        # Normalize priority
        normalized_priority = "regular" if args.priority == "normal" else args.priority
        priority = (
            UnifiedMessagePriority.URGENT
            if normalized_priority == "urgent"
            else UnifiedMessagePriority.REGULAR
        )

        # Get CYCLE_V2 template from S2A templates
        cycle_v2_template = MESSAGE_TEMPLATES.get(
            MessageCategory.S2A, {}).get("CYCLE_V2")

        if not cycle_v2_template:
            print("❌ ERROR: CYCLE_V2 template not found")
            return 1

        # Format template directly
        message_id = f"msg_{int(time.time() * 1000)}"
        timestamp = datetime.now().isoformat()

        # Replace \n in dod with actual newlines
        dod = args.dod.replace("\\n", "\n") if args.dod else ""

        rendered = cycle_v2_template.format(
            sender="Captain Agent-4",
            recipient=args.agent,
            priority=priority.value if hasattr(
                priority, "value") else str(priority),
            message_id=message_id,
            timestamp=timestamp,
            mission=args.mission,
            dod=dod,
            ssot_constraint=args.ssot_constraint,
            v2_constraint=args.v2_constraint,
            touch_surface=args.touch_surface,
            validation_required=args.validation,
            priority_level=args.priority_level or "P1",
            handoff_expectation=args.handoff,
            fallback="Escalate to Captain if blocked with proposed fix"
        )

        # Send via MessageCoordinator
        result = MessageCoordinator.send_to_agent(
            args.agent,
            rendered,
            priority,
            stalled=getattr(args, "stalled", False),
            message_category=MessageCategory.C2A
        )

        if isinstance(result, dict) and result.get("success"):
            print(f"✅ CYCLE_V2 message sent to {args.agent}")
            print(f"   Mission: {args.mission[:50]}...")
            return 0
        else:
            print(f"❌ Failed to send CYCLE_V2 message to {args.agent}")
            return 1

    except Exception as e:
        logger.error(f"CYCLE_V2 message handling error: {e}")
        import traceback
        traceback.print_exc()
        return 1


def handle_message(args, parser) -> int:
    """Handle message sending."""
    try:
        # Check for cycle-v2 flag first
        if getattr(args, "cycle_v2", False):
            return handle_cycle_v2_message(args, parser)

        if not args.agent and not args.broadcast:
            print("❌ ERROR: Either --agent or --broadcast must be specified")
            parser.print_help()
            return 1

        # Normalize "normal" to "regular" for consistency
        normalized_priority = "regular" if args.priority == "normal" else args.priority
        priority = (
            UnifiedMessagePriority.URGENT
            if normalized_priority == "urgent"
            else UnifiedMessagePriority.REGULAR
        )

        # Get stalled flag from args (defaults to False if not present)
        stalled = getattr(args, "stalled", False)

        if args.broadcast:
            success_count = MessageCoordinator.broadcast_to_all(
                args.message, priority, stalled=stalled
            )
            if success_count > 0:
                print(f"✅ Broadcast to {success_count} agents successful")
                return 0
            else:
                print("❌ Broadcast failed")
                return 1
        else:
            result = MessageCoordinator.send_to_agent(
                args.agent, args.message, priority, use_pyautogui=True, stalled=stalled
            )

            # Check if result is dict (new format) or bool (old format)
            if isinstance(result, dict):
                if result.get("success"):
                    print(f"✅ Message sent to {args.agent}")
                    return 0
                elif result.get("blocked"):
                    # Message blocked - show pending request
                    print("❌ MESSAGE BLOCKED - Pending Multi-Agent Request")
                    print()
                    print(result.get("error_message",
                          "Pending request details unavailable"))
                    return 1
                else:
                    print(f"❌ Failed to send message to {args.agent}")
                    return 1
            elif result:
                # Old format (bool) - success
                print(f"✅ Message sent to {args.agent}")
                return 0
            else:
                print(f"❌ Failed to send message to {args.agent}")
                return 1

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
    """Handle starting agents via onboarding coordinates."""
    try:
        agent_numbers = args.start
        message = args.message if hasattr(
            args, "message") and args.message else "START"

        for num in agent_numbers:
            agent_id = f"Agent-{num}"
            if agent_id not in SWARM_AGENTS:
                print(f"⚠️  Invalid agent: {agent_id}")
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

