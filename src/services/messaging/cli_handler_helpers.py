#!/usr/bin/env python3
"""
CLI Handler Helpers - Messaging Infrastructure
===============================================

<!-- SSOT Domain: integration -->

Helper functions for CLI message handling.
Extracted from cli_handlers.py for V2 compliance.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

from __future__ import annotations

import time
from datetime import datetime
from typing import Any

from src.core.messaging_core import UnifiedMessagePriority

from .message_formatters import MessageCategory, MESSAGE_TEMPLATES


def normalize_priority(priority: str) -> UnifiedMessagePriority:
    """Normalize priority string to enum."""
    normalized = "regular" if priority == "normal" else priority
    return (
        UnifiedMessagePriority.URGENT
        if normalized == "urgent"
        else UnifiedMessagePriority.REGULAR
    )


def validate_cycle_v2_fields(args: Any) -> tuple[bool, list[str]]:
    """Validate required CYCLE_V2 fields and return (is_valid, missing_fields)."""
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
    return len(missing) == 0, missing


def format_cycle_v2_template(
    template: str,
    args: Any,
    priority: UnifiedMessagePriority,
    message_id: str,
    timestamp: str,
) -> str:
    """Format CYCLE_V2 template with arguments."""
    dod = args.dod.replace("\\n", "\n") if args.dod else ""
    return template.format(
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


def prepare_cycle_v2_message(args: Any) -> tuple[str, UnifiedMessagePriority]:
    """Prepare CYCLE_V2 message and return (rendered_message, priority)."""
    cycle_v2_template = MESSAGE_TEMPLATES.get(
        MessageCategory.S2A, {}).get("CYCLE_V2")
    if not cycle_v2_template:
        raise ValueError("CYCLE_V2 template not found")
    priority = normalize_priority(args.priority)
    message_id = f"msg_{int(time.time() * 1000)}"
    timestamp = datetime.now().isoformat()
    rendered = format_cycle_v2_template(
        cycle_v2_template, args, priority, message_id, timestamp)
    return rendered, priority


def send_broadcast_message(
    message: str,
    priority: UnifiedMessagePriority,
    stalled: bool,

) -> int:
    """Send broadcast message and return exit code."""
    from .coordination_handlers import MessageCoordinator
    success_count = MessageCoordinator.broadcast_to_all()

    if success_count > 0:
        print(f"✅ Broadcast to {success_count} agents successful")
        return 0
    else:
        print("❌ Broadcast failed")
        return 1


def send_single_agent_message(
    agent: str,
    message: str,
    priority: UnifiedMessagePriority,
    stalled: bool,
    sender: str | None = None,
    category: str | None = None,

) -> int:
    """Send single agent message and return exit code."""
    from .coordination_handlers import MessageCoordinator
    from .sender_validation import validate_a2a_sender_identification, log_agent_activity

    # Map CLI category string (if provided) to MessageCategory enum
    message_category = None
    if category:
        try:
            message_category = MessageCategory(category.lower())
        except ValueError:
            # Should not happen due to argparse choices, but guard just in case
            print(
                f"❌ ERROR: Invalid category '{category}'. "
                "Valid options: s2a, d2a, c2a, a2a, a2c."
            )
            return 1

    # Validate sender identification for A2A messages (enforce proper routing)
    detected_sender = None
    if message_category == MessageCategory.A2A:
        # Detect sender for comparison
        from .coordination_helpers import detect_sender
        detected_sender = detect_sender()
        
        is_valid, validated_sender, error_msg = validate_a2a_sender_identification(
            sender=sender,
            category=message_category,
            detected_sender=detected_sender,
        )
        
        if not is_valid:
            print(error_msg)
            print(f"\n💡 Tip: Use --sender Agent-X to identify yourself (e.g., --sender Agent-2)")
            return 1
        
        # Use validated sender
        sender = validated_sender

    result = MessageCoordinator.send_to_agent(
        agent=agent,
        message=message,
        priority=priority,

        stalled=stalled,
        sender=sender,
        message_category=message_category,
    )
    
    # Log agent activity for tracking (tied to status monitoring)
    if result and isinstance(result, dict) and result.get("success"):
        final_sender = sender or detected_sender or "SYSTEM"
        if message_category:
            log_agent_activity(
                sender=final_sender,
                recipient=agent,
                category=message_category,
                message_id=result.get("queue_id"),
            )
    
    success, msg = handle_message_result(result, agent)
    print(msg)
    return 0 if success else 1


def handle_message_result(result: Any, agent: str) -> tuple[bool, str]:
    """Handle message send result and return (success, message)."""
    if isinstance(result, dict):
        if result.get("success"):
            return True, f"✅ Message sent to {agent}"
        elif result.get("blocked"):
            error_msg = result.get(
                "error_message", "Pending request details unavailable")
            return False, f"❌ MESSAGE BLOCKED - Pending Multi-Agent Request\n\n{error_msg}"
        else:
            return False, f"❌ Failed to send message to {agent}"
    elif result:
        return True, f"✅ Message sent to {agent}"
    else:
        return False, f"❌ Failed to send message to {agent}"


def route_message_delivery(
    args: Any,
    priority: UnifiedMessagePriority,
    stalled: bool,
) -> int:
    """
    Route message delivery based on args (broadcast or single agent).

    Args:
        args: Parsed CLI arguments
        priority: Message priority
        stalled: Whether this is a stalled agent recovery message

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    if args.broadcast:

        return send_single_agent_message(
            args.agent,
            args.message,
            priority,
            stalled,
            sender=sender,
            category=category,

        )
    else:
        print("❌ ERROR: Either --agent or --broadcast must be specified")
        return 1
