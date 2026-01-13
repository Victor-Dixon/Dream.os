#!/usr/bin/env python3
"""
Agent Message Helpers - Messaging Infrastructure
================================================

<!-- SSOT Domain: integration -->

Helper functions for agent message handling.
Extracted from agent_message_handler.py for V2 compliance.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from src.core.messaging_core import UnifiedMessageTag
from src.core.messaging_models_core import MessageCategory

from .message_formatters import (
    _apply_template,
    _format_normal_message_with_instructions,
    _is_ack_text,
    _load_last_inbound_categories,
    _save_last_inbound_categories,
)

logger = logging.getLogger(__name__)


def check_ack_blocked(sender: str, message: str) -> Optional[Dict[str, Any]]:
    """Check if message should be blocked due to ack policy."""
    if sender.upper().startswith("AGENT-"):
        last_inbound = _load_last_inbound_categories()
        if last_inbound.get(sender) == MessageCategory.S2A.value and _is_ack_text(message):
            logger.warning(
                f"❌ Message blocked: ack/noise reply after S2A inbound for {sender}")
            return {
                "success": False,
                "blocked": True,
                "reason": "ack_blocked_after_s2a",
                "agent": None,  # Will be set by caller
            }
    return None


def validate_recipient_can_receive(agent: str, message: str) -> tuple[bool, str | None, dict | None]:
    """Validate recipient can receive messages (check for pending multi-agent requests)."""
    from ...core.multi_agent_request_validator import get_multi_agent_validator

    validator = get_multi_agent_validator()
    can_send, error_message, pending_info = validator.validate_agent_can_send_message(
        agent_id=agent,
        target_recipient=None,
        message_content=message
    )
    return can_send, error_message, pending_info


def build_queue_metadata(
    stalled: bool,
    use_pyautogui: bool,
    send_mode: Optional[str],
    category: Optional[MessageCategory],
) -> Dict[str, Any]:
    """Build metadata dictionary for queue message."""
    metadata = {
        "stalled": stalled,
        "use_pyautogui": use_pyautogui,
        "send_mode": send_mode,
    }
    if category:
        metadata["message_category"] = category.value
    return metadata


def format_message_for_queue(
    message: Any,
    category: Optional[MessageCategory],
) -> str:
    """Format message for queue enqueue."""
    if category:
        return str(message)
    if isinstance(message, str):
        return _format_normal_message_with_instructions(message, "NORMAL")
    return str(message)


def enqueue_message(
    queue_repository,
    sender: str,
    agent: str,
    formatted_message: str,
    priority: Any,
    message_type: Any,
    metadata: Dict[str, Any],
) -> str:
    """Enqueue message via repository and return queue ID."""
    message_dict = {
        "type": "agent_message",
        "sender": sender,
        "recipient": agent,
        "content": formatted_message,
        "priority": priority.value if hasattr(priority, "value") else str(priority),
        "message_type": message_type.value,
        "tags": [UnifiedMessageTag.SYSTEM.value],
        "metadata": metadata,
    }
    
    # Use repository pattern - queue_repository implements IQueueRepository
    queue_id = queue_repository.enqueue(message_dict)
    return queue_id


def update_last_inbound_category(agent: str, category: Optional[MessageCategory]) -> None:
    """Update last inbound category for agent."""
    if category and agent.upper().startswith("AGENT-"):
        last_inbound = _load_last_inbound_categories()
        last_inbound[agent] = category.value
        _save_last_inbound_categories(last_inbound)


def send_message_with_fallback(
    queue_repository,
    sender_final: str,
    agent: str,
    formatted_message: str,
    priority: Any,
    message_type: Any,
    metadata: Dict[str, Any],
) -> Any:
    """
    Send message via queue repository or fallback, return result.
    
    If queue_repository is None, falls back to direct send (bypassing queue).
    This handles cases where queue processor isn't started or queue initialization failed.
    """
    if queue_repository:
        try:
            return send_via_queue(queue_repository, sender_final, agent, formatted_message, priority, message_type, metadata)
        except Exception as e:
            logger.warning(
                f"⚠️ Failed to enqueue message for {agent}: {e}. "
                "Falling back to direct send.")
            return send_via_fallback(sender_final, agent, formatted_message, priority, message_type, metadata)
    logger.info(
        f"📤 Queue repository unavailable - sending directly to {agent} "
        "(queue processor not required for direct delivery)")
    return send_via_fallback(sender_final, agent, formatted_message, priority, message_type, metadata)


def detect_and_determine_sender(
    sender: Optional[str],
    agent: str,
    detect_sender_func,
    determine_message_type_func,
):
    """Detect sender and determine message type."""
    if sender is None and detect_sender_func:
        sender = detect_sender_func()

    if determine_message_type_func:
        message_type, sender_final = determine_message_type_func(sender, agent)
    else:
        from src.core.messaging_core import UnifiedMessageType
        message_type = UnifiedMessageType.TEXT
        # Default to Agent-4 (CAPTAIN) for clarity in templates
        sender_final = sender or "Agent-4"

    return message_type, sender_final


def send_via_queue(
    queue_repository,
    sender: str,
    agent: str,
    formatted_message: str,
    priority: Any,
    message_type: Any,
    metadata: Dict[str, Any],
) -> Dict[str, Any]:
    """Send message via queue repository and return result."""
    queue_id = enqueue_message(
        queue_repository, sender, agent, formatted_message, priority, message_type, metadata)
    logger.info(
        f"✅ Message queued for {agent} (ID: {queue_id}): {formatted_message[:50]}...")
    return {"success": True, "queue_id": queue_id, "agent": agent}


def send_via_fallback(
    sender: str,
    agent: str,
    formatted_message: str,
    priority: Any,
    message_type: Any,
    metadata: Dict[str, Any],
<<<<<<< HEAD
) -> Dict[str, Any]:
    """Send message via fallback (direct send) and return result."""
    from src.core.messaging_core import send_message, UnifiedMessageTag

    # Send the message directly
    result = send_message(
=======
) -> Any:
    """Send message via fallback (direct send) and return result."""
    from src.core.messaging_core import send_message, UnifiedMessageTag
    return send_message(
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
        content=formatted_message,
        sender=sender,
        recipient=agent,
        message_type=message_type,
        priority=priority,
        tags=[UnifiedMessageTag.SYSTEM],
        metadata=metadata,
    )

<<<<<<< HEAD
    # Return a dict indicating this was a direct send, not queued
    if result:
        return {"success": True, "direct_send": True, "agent": agent}
    else:
        return {"success": False, "direct_send": True, "agent": agent}

=======
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console

def handle_blocked_message(block_result: Dict[str, Any], agent: str) -> None:
    """Handle blocked message logging."""
    import logging
    logger = logging.getLogger(__name__)
    if block_result.get("reason") == "pending_multi_agent_request":
        logger.warning(
            f"❌ Message blocked - recipient {agent} has pending multi-agent request")


def send_validated_message(
    queue_repository: Any,
    sender_final: str,
    agent: str,
    message: Any,
    category: Optional[MessageCategory],
    stalled: bool,
    use_pyautogui: bool,
    send_mode: Optional[str],
    priority: Any,
    message_type: Any,
) -> Any:
    """Send validated message via queue repository with fallback."""
    metadata = build_queue_metadata(
        stalled, use_pyautogui, send_mode, category)

    # Apply A2A coordination template for Agent-to-Agent messages sent via CLI/queue.
    # Discord and other integrations that already apply templates pass fully-rendered
    # content and/or their own metadata; here we only template when:
    # - We have an explicit A2A category, and
    # - The message is a plain string (raw coordination ask).
    templated_message = message
    try:
        if category == MessageCategory.A2A and isinstance(message, str):
            import uuid

            # Populate extra metadata with message content for template
            extra_meta = {
                "ask": message,  # Map message content to 'ask' field in A2A template
                "context": "",  # Empty context by default, can be extended later
            }

            templated_message = _apply_template(
                category=MessageCategory.A2A,
                message=message,
                sender=sender_final,
                recipient=agent,
                priority=priority,
                message_id=str(uuid.uuid4()),
                extra=extra_meta,
            )
    except Exception as e:
        # Safety: never block delivery if template application fails
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"A2A template application failed: {e}, using raw message")
        templated_message = message

    formatted_message = format_message_for_queue(templated_message, category)
    result = send_message_with_fallback(
        queue_repository,
        sender_final,
        agent,
        formatted_message,
        priority,
        message_type,
        metadata,
    )
    update_last_inbound_category(agent, category)
    return result


def validate_and_prepare_message(
    sender_final: str,
    agent: str,
    message: Any,
    category: Optional[MessageCategory],
) -> tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """Validate message and return blocking result if needed, or None if valid."""
    # Heuristic safeguard: detect likely A2A misuse when template/category don't match.
    # If a message looks like an A2A coordination ping but the category is not A2A,
    # this usually means AGENT_CONTEXT/sender detection wasn't set correctly.
    try:
        if isinstance(message, str):
            text = message.strip().lower()
            if text.startswith("a2a:") and category != MessageCategory.A2A:
                logger.warning(
                    "⚠️ Message to %s starts with 'A2A:' but category=%s "
                    "- check AGENT_CONTEXT / sender detection for proper A2A routing",
                    agent,
                    getattr(category, "value", str(category)),
                )
    except Exception:
        # Never block on safeguard heuristics
        pass

    ack_block = check_ack_blocked(sender_final, message)
    if ack_block:
        ack_block["agent"] = agent
        return ack_block, None
    can_send, error_message, pending_info = validate_recipient_can_receive(
        agent, message)
    if not can_send:
        return {
            "success": False,
            "blocked": True,
            "reason": "pending_multi_agent_request",
            "error_message": error_message,
            "agent": agent,
            "pending_info": pending_info
        }, None
    return None, None
