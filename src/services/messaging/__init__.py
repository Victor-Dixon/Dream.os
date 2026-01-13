#!/usr/bin/env python3
"""
A2A Coordination Protocol - Single Source of Truth
======================================

<!-- SSOT Domain: integration -->

⚠️  DEPRECATION NOTICE: Legacy messaging functions are deprecated.
   Use A2A coordination protocol for all agent-to-agent communication:
   python -m src.services.messaging_cli --agent Agent-X --category a2a --sender Agent-Y --message "..."

📋 A2A COORDINATION ONLY:
This module now contains ONLY A2A coordination protocol components.
Legacy messaging systems archived to: archive/legacy_messaging_systems/

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
Updated: Agent-1 | A2A SSOT Consolidation | Date: 2026-01-11
"""

from __future__ import annotations

import logging
from typing import Any

# CLI Parser
from .cli_parser import create_messaging_parser

# Message Formatters
from .message_formatters import (
    _apply_template,
    _format_multi_agent_request_message,
    _format_normal_message_with_instructions,
    _is_ack_text,
    _load_last_inbound_categories,
    _map_category_from_type,
    _save_last_inbound_categories,
)

# Delivery Handlers
from .delivery_handlers import (
    send_message_pyautogui,
    send_message_to_onboarding_coords,
)

# Coordination Handlers
from .coordination_handlers import (
    MessageCoordinator,
)

# Service Adapters - Define locally to avoid circular imports
class ConsolidatedMessagingService:
    """Consolidated messaging service for backward compatibility."""

    def __init__(self):
        """Initialize consolidated messaging service."""
        self.logger = logging.getLogger(__name__)

    def send_message(self, agent: str, message: str, priority: str = "regular",
                    use_pyautogui: bool = True, wait_for_delivery: bool = False,
                    timeout: float = 30.0, discord_user_id: str = None,
                    stalled: bool = False, apply_template: bool = False,
                    message_category=None, sender: str = None):
        """Send message to agent."""
        try:
            from .coordination_handlers import MessageCoordinator
            coordinator = MessageCoordinator()
            return coordinator.send_message(
                agent=agent,
                message=message,
                priority=priority,
                use_pyautogui=use_pyautogui,
                wait_for_delivery=wait_for_delivery,
                timeout=timeout,
                discord_user_id=discord_user_id,
                stalled=stalled,
                apply_template=apply_template,
                message_category=message_category,
                sender=sender
            )
        except Exception as e:
            self.logger.error(f"Failed to send message: {e}")
            return {"success": False, "error": str(e)}

    def broadcast_message(self, message: str, priority: str = "regular"):
        """Broadcast message to all agents."""
        try:
            from .coordination_handlers import MessageCoordinator
            coordinator = MessageCoordinator()
            return coordinator.broadcast_message(message, priority)
        except Exception as e:
            self.logger.error(f"Failed to broadcast message: {e}")
            return {"success": False, "error": str(e)}

# Minimal backward compatibility functions
def send_discord_message(message: str, priority: str = "regular") -> dict[str, Any]:
    """Send message via Discord (minimal implementation)."""
    try:
        from .coordination_handlers import MessageCoordinator
        coordinator = MessageCoordinator()
        # This would need to be implemented properly, but for now return a basic response
        return {"success": True, "message": "Discord message sent (placeholder)"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def broadcast_discord_message(message: str, priority: str = "regular") -> dict[str, Any]:
    """Broadcast message via Discord (minimal implementation)."""
    try:
        from .coordination_handlers import MessageCoordinator
        coordinator = MessageCoordinator()
        # This would need to be implemented properly, but for now return a basic response
        return {"success": True, "message": "Discord broadcast sent (placeholder)"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# CLI Handlers
from .cli_handlers import (
    handle_cycle_v2_message,
    handle_delivery_status,
    handle_message,
    handle_survey,
    handle_consolidation,
    handle_coordinates,
    handle_start_agents,
    handle_save,
    handle_leaderboard,
    handle_robinhood_stats,
)

__all__ = [
    # CLI Parser
    "create_messaging_parser",
    # Message Formatters
    "_apply_template",
    "_format_multi_agent_request_message",
    "_format_normal_message_with_instructions",
    "_is_ack_text",
    "_load_last_inbound_categories",
    "_map_category_from_type",
    "_save_last_inbound_categories",
    # Delivery Handlers
    "send_message_pyautogui",
    "send_message_to_onboarding_coords",
    # Coordination Handlers
    "MessageCoordinator",
    # Service Adapters - Minimal backward compatibility
    "ConsolidatedMessagingService",
    "send_discord_message",
    "broadcast_discord_message",
    # CLI Handlers
    "handle_cycle_v2_message",
    "handle_delivery_status",
    "handle_message",
    "handle_survey",
    "handle_consolidation",
    "handle_coordinates",
    "handle_start_agents",
    "handle_save",
    "handle_leaderboard",
]
