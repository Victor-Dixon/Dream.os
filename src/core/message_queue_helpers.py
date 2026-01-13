#!/usr/bin/env python3
"""
Message Queue Helpers - V2 Compliance Refactor
===============================================

<!-- SSOT Domain: integration -->

Helper functions extracted from MessageQueue for V2 compliance.

V2 Compliance:
- File: <400 lines ✅
- Functions: <30 lines ✅

Author: Agent-6 (Coordination & Communication Specialist)
Date: 2025-01-27
License: MIT
"""

from typing import Any, Dict, Optional
from datetime import datetime

from src.utils.swarm_time import format_swarm_timestamp


def log_message_to_repository(
    message_repository: Optional[Any],
    message: Any,
    queue_id: str,
    now: datetime,
    logger: Optional[Any] = None
) -> None:
    """Log queued message to repository (SSOT enforcement).
    
    Args:
        message_repository: MessageRepository instance
        message: Message data
        queue_id: Queue entry ID
        now: Current timestamp
        logger: Optional logger instance
    """
    if not message_repository:
        return
    
    try:
        msg_data = message if isinstance(message, dict) else {}
        message_repository.save_message({
            "from": msg_data.get("sender", msg_data.get("from", "UNKNOWN")),
            "to": msg_data.get("recipient", msg_data.get("to", "UNKNOWN")),
            "message_type": msg_data.get("type", "text"),
            "priority": msg_data.get("priority", "normal"),
            "content": str(msg_data.get("content", ""))[:500],
            "content_length": len(str(msg_data.get("content", ""))),
            "queue_id": queue_id,
            "source": msg_data.get("source", "queue"),
            "status": "QUEUED",
            "timestamp": format_swarm_timestamp(now),
        })
        if logger:
            logger.debug(f"✅ Queued message logged to history: {queue_id}")
    except Exception as e:
        if logger:
            logger.warning(f"⚠️ Failed to log queued message to history: {e}")


def track_queue_metrics(
    metrics_engine: Optional[Any],
    message: Any,
    queue_size: int,
    logger: Optional[Any] = None
) -> None:
    """Track queue metrics via metrics engine.
    
    Args:
        metrics_engine: MetricsEngine instance
        message: Message data
        queue_size: Current queue size
        logger: Optional logger instance
    """
    if not metrics_engine:
        return
    
    try:
        msg_data = message if isinstance(message, dict) else {}
        metrics_engine.increment_metric("queue.enqueued")
        sender = msg_data.get("sender", "UNKNOWN")
        recipient = msg_data.get("recipient", "UNKNOWN")
        metrics_engine.increment_metric(f"queue.enqueued.by_sender.{sender}")
        metrics_engine.increment_metric(
            f"queue.enqueued.by_recipient.{recipient}"
        )
        metrics_engine.record_metric("queue.size", queue_size)
    except Exception:
        pass  # Metrics failures are non-blocking


def track_agent_activity(
    message: Any,
    logger: Optional[Any] = None
) -> None:
    """Track agent activity when message queued.
    
    Args:
        message: Message data
        logger: Optional logger instance
    """
    try:
        from .agent_activity_tracker import get_activity_tracker
        tracker = get_activity_tracker()
        msg_data = message if isinstance(message, dict) else {}
        sender = msg_data.get("sender", msg_data.get("from", "UNKNOWN"))
        if sender.startswith("Agent-"):
            tracker.mark_active(sender, "message_queuing")
    except Exception as e:
        if logger:
            logger.warning(f"Failed to track agent activity: {e}")


def wait_for_queue_delivery(
    queue: Any,
    queue_id: str,
    timeout: float = 30.0,
    poll_interval: float = 0.5,
    logger: Optional[Any] = None
) -> bool:
    """Wait for message delivery to complete (DELIVERED or FAILED).
    
    CRITICAL: Blocks until message is delivered or failed or timeout.
    Used for synchronous operations that need to wait for completion.
    
    Args:
        queue: MessageQueue instance
        queue_id: Queue entry ID to wait for
        timeout: Maximum time to wait in seconds (default: 30.0)
        poll_interval: How often to check status in seconds (default: 0.5)
        logger: Optional logger instance
        
    Returns:
        True if delivered successfully, False if failed or timeout
    """
    import time
    
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        status = queue.get_entry_status(queue_id)
        
        if status == "DELIVERED":
            if logger:
                logger.debug(f"Message {queue_id} delivered successfully")
            return True
        
        if status == "FAILED":
            if logger:
                logger.debug(f"Message {queue_id} failed")
            return False
        
        if status is None:
            if logger:
                logger.warning(f"Queue entry {queue_id} not found")
            return False
        
        # Still PENDING or PROCESSING, wait and check again
        time.sleep(poll_interval)
    
    # Timeout
    if logger:
        logger.warning(
            f"Timeout waiting for message {queue_id} (timeout: {timeout}s)"
        )
    return False

