#!/usr/bin/env python3
"""
Discord Message Handler - Messaging Infrastructure
=================================================

<!-- SSOT Domain: integration -->

Handles Discord message delivery via message queue.
Extracted from service_adapters.py for V2 compliance.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from src.core.messaging_models_core import MessageCategory

from .discord_message_helpers import (
    prepare_discord_message,
)

logger = logging.getLogger(__name__)


def send_discord_message_to_agent(
    agent: str, message: str, priority: str = "regular", use_pyautogui: bool = True,
    wait_for_delivery: bool = False, timeout: float = 30.0, discord_user_id: str | None = None,
    stalled: bool = False, apply_template: bool = False, message_category: MessageCategory | None = None,
    sender: str | None = None, queue_repository=None, messaging_cli_path: Path | None = None,
    project_root: Path | None = None, resolve_discord_sender_func=None, get_discord_username_func=None,
) -> dict[str, Any]:
    """Send Discord message to agent via message queue (synchronized delivery)."""
    try:
        from .discord_message_helpers import route_discord_delivery
        priority_enum, resolved_sender, templated_message = prepare_discord_message(
            message, agent, priority, sender, discord_user_id, apply_template, message_category, resolve_discord_sender_func
        )
        return route_discord_delivery(
            queue_repository, agent, message, templated_message, resolved_sender, priority_enum,
            stalled, messaging_cli_path, project_root, use_pyautogui, message_category, apply_template, wait_for_delivery, timeout, discord_user_id
        )
    except Exception as e:
        logger.error(f"Error sending message to {agent}: {e}")
        return {"success": False, "message": str(e), "agent": agent}

