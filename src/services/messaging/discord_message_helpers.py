#!/usr/bin/env python3
"""
Discord Message Helpers - Messaging Infrastructure
=================================================

<!-- SSOT Domain: integration -->

Helper functions for Discord message handling.
Extracted from discord_message_handler.py for V2 compliance.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

from __future__ import annotations

import logging
import re
import subprocess
import uuid
from pathlib import Path
from typing import Any

from src.core.config.timeout_constants import TimeoutConstants
from src.core.messaging_core import UnifiedMessagePriority, UnifiedMessageType
from src.core.messaging_models_core import MessageCategory

from .message_formatters import _apply_template

logger = logging.getLogger(__name__)


def resolve_priority_and_sender(
    priority: str,
    sender: str | None,
    discord_user_id: str | None,
    resolve_discord_sender_func=None,
) -> tuple[UnifiedMessagePriority, str]:
    """Resolve priority enum and sender name."""
    priority_value = (priority or "regular").lower()
    priority_enum = (
        UnifiedMessagePriority.URGENT
        if priority_value == "urgent"
        else UnifiedMessagePriority.REGULAR
    )

    resolved_sender = sender or (
        resolve_discord_sender_func(discord_user_id)
        if discord_user_id and resolve_discord_sender_func
        else "DISCORD"
    )

    return priority_enum, resolved_sender


def apply_message_template(
    message: str,
    agent: str,
    resolved_sender: str,
    priority_enum: UnifiedMessagePriority,
    apply_template: bool,
    message_category: MessageCategory | None,
) -> str:
    """Apply message template if requested."""
    if not apply_template:
        return message

    category = message_category or MessageCategory.D2A
    
    # Populate extra metadata based on category
    extra_meta = {}
    if category == MessageCategory.A2A:
        extra_meta = {
            "ask": message,  # Map message content to 'ask' field in A2A template
            "context": "",  # Empty context by default, can be extended later
        }
    
    templated_message = _apply_template(
        category=category,
        message=message,
        sender=resolved_sender,
        recipient=agent,
        priority=priority_enum,
        message_id=str(uuid.uuid4()),
        extra=extra_meta,
    )

    # CRITICAL FIX: If templated message ends with original message, it was appended incorrectly
    message_count = templated_message.count(message)
    if templated_message.endswith(message) and message_count > 1:
        templated_message = templated_message[:-len(message)].rstrip()

    return templated_message


def validate_agent_can_receive(agent: str, message: str) -> tuple[bool, str | None, dict | None]:
    """Validate agent can receive messages (check for pending multi-agent requests)."""
    from ...core.multi_agent_request_validator import get_multi_agent_validator

    validator = get_multi_agent_validator()
    can_send, error_message, pending_info = validator.validate_agent_can_send_message(
        agent_id=agent,
        target_recipient=None,
        message_content=message
    )

    return can_send, error_message, pending_info


def determine_discord_message_type(message: str) -> str:
    """Determine message type for Discord messages (ONBOARDING vs HUMAN_TO_AGENT)."""
    message_lower = message.lower().strip()

    is_onboarding_command = (
        "hard onboard" in message_lower or
        "soft onboard" in message_lower or
        message_lower.startswith("!start") or
        bool(re.match(r'^start\s+(agent-)?[1-8](\s|$)', message_lower, re.IGNORECASE))
    )

    if is_onboarding_command:
        return UnifiedMessageType.ONBOARDING.value
    else:
        return UnifiedMessageType.HUMAN_TO_AGENT.value


def build_queue_metadata(
    resolved_sender: str,
    discord_username: str | None,
    discord_user_id: str | None,
    stalled: bool,
    message: str,
    message_category: MessageCategory | None,
    apply_template: bool,
) -> dict[str, Any]:
    """Build metadata dictionary for queue message."""
    return {
        "source": "discord",
        "sender": resolved_sender,
        "discord_username": discord_username,
        "discord_user_id": discord_user_id if discord_user_id else None,
        "use_pyautogui": True,
        "stalled": stalled,
        "raw_message": message,
        "message_category": (message_category or MessageCategory.D2A).value if apply_template else None,
    }


def build_queue_message(
    agent: str,
    templated_message: str,
    resolved_sender: str,
    priority: str,
    explicit_message_type: str,
    discord_user_id: str | None,
    discord_username: str | None,
    stalled: bool,
    message: str,
    message_category: MessageCategory | None,
    apply_template: bool,
) -> dict[str, Any]:
    """Build message dictionary for queue enqueue."""
    return {
        "type": "agent_message",
        "sender": resolved_sender,
        "discord_username": discord_username,
        "discord_user_id": discord_user_id if discord_user_id else None,
        "recipient": agent,
        "content": templated_message,
        "priority": priority,
        "source": "discord",
        "message_type": explicit_message_type,
        "tags": [],
        "metadata": build_queue_metadata(
            resolved_sender, discord_username, discord_user_id,
            stalled, message, message_category, apply_template
        ),
    }


def wait_for_message_delivery(
    queue_repository,
    queue_id: str,
    agent: str,
    timeout: float,
) -> dict[str, Any]:
    """Wait for message delivery via repository and return result."""
    import time
    logger.debug(f"⏳ Waiting for message {queue_id} delivery...")
    start_time = time.time()
    
    # Poll repository for delivery status
    while time.time() - start_time < timeout:
        status = queue_repository.get_status(queue_id)
        if status:
            status_value = status.get("status") if isinstance(status, dict) else getattr(status, "status", None)
            if status_value == "DELIVERED":
                logger.info(f"✅ Message {queue_id} delivered successfully")
                return {
                    "success": True,
                    "message": f"Message delivered to {agent}",
                    "agent": agent,
                    "queue_id": queue_id,
                    "delivered": True,
                }
            elif status_value == "FAILED":
                logger.warning(f"⚠️ Message {queue_id} delivery failed")
                return {
                    "success": False,
                    "message": f"Message delivery failed for {agent}",
                    "agent": agent,
                    "queue_id": queue_id,
                    "delivered": False,
                }
        time.sleep(0.5)  # Poll every 500ms
    
    logger.warning(f"⚠️ Message {queue_id} delivery timeout")
    return {
        "success": False,
        "message": f"Message delivery timeout for {agent}",
        "agent": agent,
        "queue_id": queue_id,
        "delivered": False,
    }


def build_subprocess_command(
    messaging_cli_path: Path,
    agent: str,
    templated_message: str,
    priority: str,
    use_pyautogui: bool,
) -> list[str]:
    """Build subprocess command for fallback delivery."""
    cmd = [
        "python",
        str(messaging_cli_path),
        "--agent",
        agent,
        "--message",
        templated_message,
        "--priority",
        priority,
    ]
    if use_pyautogui:
        cmd.append("--pyautogui")
    return cmd


def execute_subprocess_delivery(
    cmd: list[str],
    project_root: Path,
    agent: str,
    message: str,
) -> dict[str, Any]:
    """Execute subprocess delivery and return result."""
    env = {"PYTHONPATH": str(project_root)}

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True,
            timeout=TimeoutConstants.HTTP_DEFAULT, env=env, cwd=str(project_root)
        )

        if result.returncode == 0:
            logger.info(f"Message sent to {agent}: {message[:50]}...")
            return {"success": True, "message": f"Message sent to {agent}", "agent": agent}
        else:
            error_msg = result.stderr or "Unknown error"
            logger.error(f"Failed to send message to {agent}: {error_msg}")
            return {
                "success": False,
                "message": f"Failed to send message: {error_msg}",
                "agent": agent,
            }
    except subprocess.TimeoutExpired:
        logger.error(f"Timeout sending message to {agent}")
        return {"success": False, "message": "Message timeout", "agent": agent}


def fallback_subprocess_delivery(
    agent: str,
    templated_message: str,
    priority: str,
    use_pyautogui: bool,
    messaging_cli_path: Path,
    project_root: Path,
    message: str,
) -> dict[str, Any]:
    """Fallback to subprocess delivery if queue unavailable."""
    cmd = build_subprocess_command(
        messaging_cli_path, agent, templated_message, priority, use_pyautogui
    )
    return execute_subprocess_delivery(cmd, project_root, agent, message)


def prepare_discord_message(
    message: str,
    agent: str,
    priority: str,
    sender: str | None,
    discord_user_id: str | None,
    apply_template: bool,
    message_category: MessageCategory | None,
    resolve_discord_sender_func,
) -> tuple[UnifiedMessagePriority, str, str]:
    """Prepare Discord message: resolve priority, sender, and apply template."""
    priority_enum, resolved_sender = resolve_priority_and_sender(
        priority, sender, discord_user_id, resolve_discord_sender_func
    )
    templated_message = apply_message_template(
        message, agent, resolved_sender, priority_enum,
        apply_template, message_category
    )
    return priority_enum, resolved_sender, templated_message


def build_and_enqueue_discord_message(
    queue_repository,
    agent: str,
    templated_message: str,
    resolved_sender: str,
    priority: str,
    explicit_message_type: str,
    discord_user_id: str | None,
    discord_username: str | None,
    stalled: bool,
    message: str,
    message_category: MessageCategory | None,
    apply_template: bool,
) -> str:
    """Build and enqueue Discord message via repository, return queue ID."""
    queue_message = build_queue_message(
        agent, templated_message, resolved_sender, priority,
        explicit_message_type, discord_user_id, discord_username,
        stalled, message, message_category, apply_template
    )
    # Use repository pattern - queue_repository implements IQueueRepository
    queue_id = queue_repository.enqueue(queue_message)
    logger.info(f"✅ Message queued for {agent} (ID: {queue_id}): {message[:50]}...")
    return queue_id


def route_discord_delivery(
    queue_repository: Any, agent: str, message: str, templated_message: str, resolved_sender: str,
    priority_enum: UnifiedMessagePriority, stalled: bool, messaging_cli_path: Path | None,
    project_root: Path | None, use_pyautogui: bool, message_category: MessageCategory | None,
    apply_template: bool, wait_for_delivery: bool, timeout: float, discord_user_id: str | None,
) -> dict[str, Any]:
    """
    Route Discord message delivery via queue repository or fallback.
    
    If queue_repository is None, falls back to subprocess delivery (bypassing queue).
    This handles cases where queue processor isn't started or queue initialization failed.
    """
    if queue_repository:
        try:
            return send_discord_via_queue(
                queue_repository=queue_repository, agent=agent, templated_message=templated_message,
                resolved_sender=resolved_sender, priority=priority_enum.value,
                explicit_message_type=determine_discord_message_type(message),
                discord_user_id=discord_user_id, discord_username=None, stalled=stalled,
                message=message, message_category=message_category, apply_template=apply_template,
                wait_for_delivery=wait_for_delivery, timeout=timeout,
            )
        except Exception as e:
            logger.warning(
                f"⚠️ Failed to enqueue Discord message for {agent}: {e}. "
                "Falling back to subprocess delivery.")
            return fallback_subprocess_delivery(
                agent=agent, message=templated_message, priority=priority_enum,
                messaging_cli_path=messaging_cli_path, project_root=project_root,
                use_pyautogui=use_pyautogui, stalled=stalled,
            )
    logger.info(
        f"📤 Queue repository unavailable - using subprocess delivery for {agent} "
        "(queue processor not required for subprocess delivery)")
    return fallback_subprocess_delivery(
        agent=agent, message=templated_message, priority=priority_enum,
        messaging_cli_path=messaging_cli_path, project_root=project_root,
        use_pyautogui=use_pyautogui, stalled=stalled,
    )


def send_discord_via_queue(
    queue_repository,
    agent: str,
    templated_message: str,
    resolved_sender: str,
    priority: str,
    explicit_message_type: str,
    discord_user_id: str | None,
    discord_username: str | None,
    stalled: bool,
    message: str,
    message_category: MessageCategory | None,
    apply_template: bool,
    wait_for_delivery: bool,
    timeout: float,
) -> dict[str, Any]:
    """Send Discord message via queue repository and return result."""
    queue_id = build_and_enqueue_discord_message(
        queue_repository, agent, templated_message, resolved_sender, priority,
        explicit_message_type, discord_user_id, discord_username,
        stalled, message, message_category, apply_template
    )
    if wait_for_delivery:
        return wait_for_message_delivery(queue_repository, queue_id, agent, timeout)
    return {"success": True, "message": f"Message queued for {agent}", "agent": agent, "queue_id": queue_id}


def queue_message_for_agent_by_number(
    agent_number: int,
    message: str,
    priority: str = "regular",
    sender: str | None = None,
    discord_user_id: str | None = None,
    stalled: bool = False,
    apply_template: bool = False,
    message_category: Any = None,
    wait_for_delivery: bool = False,
    timeout: float = 30.0,
    queue_repository = None,
    **kwargs
) -> dict[str, Any]:
    """
    Queue message for agent by number.
    
    Restored helper function for agent bumping.
    
    Args:
        agent_number: Agent number (1-8)
        message: Message content
        priority: Priority (regular/urgent)
        sender: Sender name
        
    Returns:
        Result dictionary
    """
    agent = f"Agent-{agent_number}"
    
    # If repo not provided, create default
    if queue_repository is None:
        try:
            from .repositories.queue_repository import QueueRepository
            queue_repository = QueueRepository()
        except ImportError:
            logger.warning("Could not import QueueRepository, forcing subprocess delivery")
            queue_repository = None

    # Resolve paths if not provided
    project_root = Path(__file__).resolve().parents[3] # src/services/messaging/helpers.py -> /workspace
    messaging_cli_path = project_root / "src" / "services" / "messaging_cli.py"

    # Prepare message
    priority_enum, resolved_sender, templated_message = prepare_discord_message(
        message, agent, priority, sender, discord_user_id, apply_template, message_category, None
    )
    
    # Route delivery
    return route_discord_delivery(
        queue_repository=queue_repository,
        agent=agent,
        message=message,
        templated_message=templated_message,
        resolved_sender=resolved_sender,
        priority_enum=priority_enum,
        stalled=stalled,
        messaging_cli_path=messaging_cli_path,
        project_root=project_root,
        use_pyautogui=True,
        message_category=message_category,
        apply_template=apply_template,
        wait_for_delivery=wait_for_delivery,
        timeout=timeout,
        discord_user_id=discord_user_id
    )
