#!/usr/bin/env python3
"""
Service Adapter Helpers - Messaging Infrastructure
==================================================

<!-- SSOT Domain: integration -->

Helper functions for service adapter message handling.
Extracted from service_adapters.py for V2 compliance.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

from __future__ import annotations

import logging
import time
from typing import Any

from src.core.config.timeout_constants import TimeoutConstants
from src.core.constants.agent_constants import AGENT_LIST

logger = logging.getLogger(__name__)


def execute_broadcast_operation(
    send_message_func: Any,
    message: str,
    priority: str,
) -> dict[str, Any]:
    """Execute broadcast operation with keyboard lock."""
    from ..core.keyboard_control_lock import keyboard_control

    agents = AGENT_LIST
    with keyboard_control("broadcast_operation"):
        results = [send_message_func(agent, message, priority, use_pyautogui=True, wait_for_delivery=True, timeout=TimeoutConstants.HTTP_DEFAULT) for agent in agents]
        for _ in agents:
            time.sleep(0.5)
        success_count = sum(1 for r in results if r.get("success"))
        delivered_count = sum(1 for r in results if r.get("delivered", False))
        logger.info(f"✅ Broadcast complete: {success_count}/{len(agents)} queued, {delivered_count}/{len(agents)} delivered (locked during entire operation to prevent conflicts)")
        return {"success": success_count > 0, "message": f"Broadcast to {success_count}/{len(agents)} agents ({delivered_count} delivered)", "results": results}

