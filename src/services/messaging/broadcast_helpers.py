#!/usr/bin/env python3
"""
Broadcast Helpers - Messaging Infrastructure
===========================================

<!-- SSOT Domain: integration -->

Helper functions for broadcast message handling.
Extracted from broadcast_handler.py for V2 compliance.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

from __future__ import annotations

import logging
import time
from typing import Any, Dict, List

# Mode-aware: Use get_active_agents() instead of AGENT_LIST
try:
    from src.core.agent_mode_manager import get_active_agents
    # Will be set dynamically per mode
    def get_swarm_agents():
        return get_active_agents()
except Exception:
    # Fallback if mode manager unavailable
    from src.core.constants.agent_constants import AGENT_LIST
    def get_swarm_agents():
        return AGENT_LIST
from src.core.messaging_core import (
    UnifiedMessagePriority,
    UnifiedMessageTag,
    UnifiedMessageType,
    send_message,
)

logger = logging.getLogger(__name__)

# Inter-agent delay for broadcast fallback to prevent routing race conditions
INTER_AGENT_DELAY_BROADCAST = 3.0  # Delay between agents in broadcast fallback (increased from 1.0s)


def validate_agent_for_broadcast(
    validator,
    agent: str,
    message: str,
) -> tuple[bool, str | None, dict | None]:
    """Validate agent can receive broadcast message."""
    return validator.validate_agent_can_send_message(
        agent_id=agent,
        target_recipient=None,
        message_content=message
    )


def build_broadcast_metadata(stalled: bool) -> Dict[str, Any]:
    """Build metadata for broadcast message."""
    return {
        "stalled": stalled,
        "use_pyautogui": True,
    }


def enqueue_broadcast_message(
    queue,
    agent: str,
    formatted_message: str,
    priority_value: str,
    metadata: Dict[str, Any],
) -> str:
    """Enqueue broadcast message for agent and return queue ID."""
    return queue.enqueue(
        message={
            "type": "agent_message",
            "sender": "CAPTAIN",
            "recipient": agent,
            "content": formatted_message,
            "priority": priority_value,
            "message_type": UnifiedMessageType.BROADCAST.value,
            "tags": [
                UnifiedMessageTag.SYSTEM.value,
                UnifiedMessageTag.COORDINATION.value,
            ],
            "metadata": metadata,
        }
    )


def process_broadcast_agents(
    queue,
    formatted_message: str,
    priority_value: str,
    metadata: Dict[str, Any],
    validator,
    message: str,
) -> tuple[List[str], List[Dict[str, Any]]]:
    """Process all agents for broadcast, returning queue_ids and skipped_agents (mode-aware)."""
    queue_ids = []
    skipped_agents = []
    swarm_agents = get_swarm_agents()  # Mode-aware agent list
    for agent in swarm_agents:
        can_send, error_message, pending_info = validate_agent_for_broadcast(validator, agent, message)
        if not can_send:
            logger.warning(f"⏭️  Skipping {agent} in broadcast - has pending multi-agent request")
            skipped_agents.append({
                "agent": agent,
                "reason": "pending_multi_agent_request",
                "error_message": error_message,
                "pending_info": pending_info
            })
            continue
        queue_id = enqueue_broadcast_message(queue, agent, formatted_message, priority_value, metadata)
        queue_ids.append(queue_id)
    return queue_ids, skipped_agents


def execute_broadcast_delivery(
    queue: Any,
    message: str,
    priority: UnifiedMessagePriority,
    stalled: bool,
    validator: Any,
) -> int:
    """Execute broadcast delivery via queue or fallback."""
    if queue:
        metadata = build_broadcast_metadata(stalled)
        priority_value = priority.value if hasattr(priority, "value") else str(priority)
        from .message_formatters import _format_normal_message_with_instructions
        formatted_message = _format_normal_message_with_instructions(message, "BROADCAST")
        queue_ids, skipped_agents = process_broadcast_agents(
            queue, formatted_message, priority_value, metadata, validator, message
        )
        if skipped_agents:
            logger.warning(f"⏭️  Broadcast skipped {len(skipped_agents)} agents with pending requests: {[a['agent'] for a in skipped_agents]}")
        logger.info(f"✅ Broadcast queued for {len(queue_ids)} agents (skipped {len(skipped_agents)}): {message[:50]}...")
        return len(queue_ids)
    else:
        logger.warning("⚠️ Queue unavailable, falling back to direct broadcast")
        return send_broadcast_fallback(message, priority, stalled)


def send_broadcast_fallback(
    message: str,
    priority: UnifiedMessagePriority,
    stalled: bool,
) -> int:
    """Send broadcast via fallback (direct send with keyboard lock)."""
    from ...core.keyboard_control_lock import keyboard_control

    with keyboard_control("broadcast_all_agents"):
        metadata = {"stalled": stalled} if stalled else {}
        success_count = 0
        swarm_agents = get_swarm_agents()  # Mode-aware agent list
        for agent in swarm_agents:
            ok = send_message(
                content=message,
                sender="CAPTAIN",
                recipient=agent,
                message_type=UnifiedMessageType.BROADCAST,
                priority=priority,
                tags=[UnifiedMessageTag.SYSTEM, UnifiedMessageTag.COORDINATION],
                metadata=metadata,
            )
            if ok:
                success_count += 1
            # #region agent log
            import json
            from pathlib import Path
            log_path = Path("d:\\Agent_Cellphone_V2_Repository\\.cursor\\debug.log")
            delay_start = time.time()
            try:
                with open(log_path, 'a', encoding='utf-8') as f:
                    f.write(json.dumps({"sessionId": "debug-session", "runId": "run1", "hypothesisId": "C", "location": "broadcast_helpers.py:164", "message": "Before broadcast inter-agent delay", "data": {"agent": agent, "success": ok, "delay_seconds": INTER_AGENT_DELAY_BROADCAST}, "timestamp": int(time.time() * 1000)}) + "\n")
            except: pass
            # #endregion
            time.sleep(INTER_AGENT_DELAY_BROADCAST)
            # #region agent log
            delay_end = time.time()
            actual_delay = delay_end - delay_start
            try:
                with open(log_path, 'a', encoding='utf-8') as f:
                    f.write(json.dumps({"sessionId": "debug-session", "runId": "run1", "hypothesisId": "C", "location": "broadcast_helpers.py:170", "message": "After broadcast inter-agent delay", "data": {"agent": agent, "expected_delay": INTER_AGENT_DELAY_BROADCAST, "actual_delay": round(actual_delay, 2)}, "timestamp": int(time.time() * 1000)}) + "\n")
            except: pass
            # #endregion
        return success_count





