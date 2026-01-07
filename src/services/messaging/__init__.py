#!/usr/bin/env python3
"""
Messaging Module - Public API Exports
======================================

<!-- SSOT Domain: integration -->

Public API exports for messaging infrastructure.
Extracted from messaging_infrastructure.py for V2 compliance.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

from __future__ import annotations

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

# Service Adapters
from .service_adapters import (
    ConsolidatedMessagingService,
    send_discord_message,
    broadcast_discord_message,
)

# CLI Handlers
from .cli_handlers import (
    handle_cycle_v2_message,
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
    # Service Adapters
    "ConsolidatedMessagingService",
    "send_discord_message",
    "broadcast_discord_message",
    # CLI Handlers
    "handle_cycle_v2_message",
    "handle_message",
    "handle_survey",
    "handle_consolidation",
    "handle_coordinates",
    "handle_start_agents",
    "handle_save",
    "handle_leaderboard",
]
