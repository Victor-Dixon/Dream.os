#!/usr/bin/env python3
"""
Multi-Agent Request Helpers - Messaging Infrastructure
=======================================================

<!-- SSOT Domain: integration -->

Helper functions for multi-agent request handling.
Extracted from multi_agent_request_handler.py for V2 compliance.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from src.core.messaging_core import (
    UnifiedMessagePriority,
    UnifiedMessageTag,
    UnifiedMessageType,
)

logger = logging.getLogger(__name__)


def create_request_collector(
    responder: Any,
    request_id: str,
    sender: str,
    recipients: List[str],
    message: str,
    timeout_seconds: int,
    wait_for_all: bool,
) -> str:
    """Create response collector and return collector ID."""
    return responder.create_request(
        request_id=request_id,
        sender=sender,
        recipients=recipients,
        content=message,
        timeout_seconds=timeout_seconds,
        wait_for_all=wait_for_all
    )


def build_multi_agent_metadata(
    stalled: bool,
    collector_id: str,
    request_id: str,
) -> Dict[str, Any]:
    """Build metadata for multi-agent request."""
    return {
        "stalled": stalled,
        "use_pyautogui": True,
        "collector_id": collector_id,
        "request_id": request_id,
        "is_multi_agent_request": True
    }


def enqueue_multi_agent_message(
    queue_repository: Any,
    sender: str,
    recipient: str,
    formatted_message: str,
    priority_value: str,
    metadata: Dict[str, Any],
) -> str:
    """Enqueue multi-agent request message via repository and return queue ID."""
    message_dict = {
        "type": "multi_agent_request",
        "sender": sender,
        "recipient": recipient,
        "content": formatted_message,
        "priority": priority_value,
        "message_type": UnifiedMessageType.MULTI_AGENT_REQUEST.value,
        "tags": [UnifiedMessageTag.COORDINATION.value],
        "metadata": metadata,
    }
    # Use repository pattern - queue_repository implements IQueueRepository
    return queue_repository.enqueue(message_dict)


def send_multi_agent_messages(
    queue_repository: Any,
    sender: str,
    recipients: List[str],
    formatted_message: str,
    priority_value: str,
    metadata: Dict[str, Any],
) -> List[str]:
    """Send multi-agent messages to all recipients via repository and return queue IDs."""
    queue_ids = []
    for recipient in recipients:
        queue_id = enqueue_multi_agent_message(
            queue_repository, sender, recipient, formatted_message, priority_value, metadata
        )
        queue_ids.append(queue_id)
    return queue_ids


def process_multi_agent_request(
    queue_repository: Any,
    sender: str,
    recipients: List[str],
    message: str,
    collector_id: str,
    request_id: str,
    priority: Any,
    stalled: bool,
    timeout_seconds: int,
) -> str:
    """Process multi-agent request via repository and return collector ID."""
    import logging
    from .message_formatters import _format_multi_agent_request_message
    logger = logging.getLogger(__name__)

    if queue_repository:
        metadata = build_multi_agent_metadata(stalled, collector_id, request_id)
        priority_value = priority.value if hasattr(priority, "value") else str(priority)
        formatted_message = _format_multi_agent_request_message(
            message, collector_id, request_id, len(recipients), timeout_seconds
        )
        queue_ids = send_multi_agent_messages(
            queue_repository, sender, recipients, formatted_message, priority_value, metadata
        )
        logger.info(f"✅ Multi-agent request {collector_id} queued for {len(recipients)} agents")
        return collector_id
    else:
        logger.error("Queue repository unavailable for multi-agent request")
        return ""

