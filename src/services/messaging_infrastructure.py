#!/usr/bin/env python3
"""
UNIFIED MESSAGING INFRASTRUCTURE - Backward Compatibility Shim
==============================================================

<!-- SSOT Domain: integration -->

Backward compatibility shim for messaging_infrastructure.py.
All functionality has been extracted to src/services/messaging/ modules.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

from __future__ import annotations

<<<<<<< HEAD
# Temporarily disable imports to avoid circular import issues
# TODO: Re-enable these imports once circular import is resolved
# from .messaging import (
#     create_messaging_parser,
#     _apply_template,
#     _format_multi_agent_request_message,
#     _format_normal_message_with_instructions,
#     _is_ack_text,
#     _load_last_inbound_categories,
#     _map_category_from_type,
#     _save_last_inbound_categories,
#     send_message_pyautogui,
#     send_message_to_onboarding_coords,
#     handle_cycle_v2_message,
#     handle_message,
#     handle_survey,
#     handle_consolidation,
#     handle_coordinates,
#     handle_start_agents,
#     handle_save,
#     handle_leaderboard,
# )

# Placeholder functions for backward compatibility
def create_messaging_parser():
    """Placeholder - import disabled due to circular import."""
    return None

def _apply_template(*args, **kwargs):
    """Placeholder - import disabled due to circular import."""
    return None

def _format_multi_agent_request_message(*args, **kwargs):
    """Placeholder - import disabled due to circular import."""
    return None

def _format_normal_message_with_instructions(*args, **kwargs):
    """Placeholder - import disabled due to circular import."""
    return None

def _is_ack_text(*args, **kwargs):
    """Placeholder - import disabled due to circular import."""
    return False

def _load_last_inbound_categories(*args, **kwargs):
    """Placeholder - import disabled due to circular import."""
    return {}

def _map_category_from_type(*args, **kwargs):
    """Placeholder - import disabled due to circular import."""
    return None

def _save_last_inbound_categories(*args, **kwargs):
    """Placeholder - import disabled due to circular import."""
    pass

def send_message_pyautogui(*args, **kwargs):
    """Placeholder - import disabled due to circular import."""
    return {"success": False, "error": "Circular import issue - function disabled"}

def send_message_to_onboarding_coords(*args, **kwargs):
    """Placeholder - import disabled due to circular import."""
    return {"success": False, "error": "Circular import issue - function disabled"}

def handle_cycle_v2_message(*args, **kwargs):
    """Placeholder - import disabled due to circular import."""
    return None

def handle_message(*args, **kwargs):
    """Placeholder - import disabled due to circular import."""
    return None

def handle_survey(*args, **kwargs):
    """Placeholder - import disabled due to circular import."""
    return None

def handle_consolidation(*args, **kwargs):
    """Placeholder - import disabled due to circular import."""
    return None

def handle_coordinates(*args, **kwargs):
    """Placeholder - import disabled due to circular import."""
    return None

def handle_start_agents(*args, **kwargs):
    """Placeholder - import disabled due to circular import."""
    return None

def handle_save(*args, **kwargs):
    """Placeholder - import disabled due to circular import."""
    return None

def handle_leaderboard(*args, **kwargs):
    """Placeholder - import disabled due to circular import."""
    return None

# Lazy import MessageCoordinator to avoid circular imports
def _get_message_coordinator():
    """Lazy import MessageCoordinator to avoid circular imports."""
    from .messaging import MessageCoordinator
    return MessageCoordinator


# ConsolidatedMessagingService - Moved here to avoid circular imports
class ConsolidatedMessagingService:
    """Consolidated messaging service for backward compatibility."""

    def __init__(self):
        """Initialize consolidated messaging service."""
        import logging
        self.logger = logging.getLogger(__name__)

    def send_message(self, agent: str, message: str, priority: str = "regular",
                    use_pyautogui: bool = True, wait_for_delivery: bool = False,
                    timeout: float = 30.0, discord_user_id: str = None,
                    stalled: bool = False, apply_template: bool = False,
                    message_category=None, sender: str = None):
        """Send message to agent."""
        try:
            coordinator_class = _get_message_coordinator()
            coordinator = coordinator_class()
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
            coordinator_class = _get_message_coordinator()
            coordinator = coordinator_class()
            return coordinator.broadcast_message(message, priority)
        except Exception as e:
            self.logger.error(f"Failed to broadcast message: {e}")
            return {"success": False, "error": str(e)}
=======
# Import all public APIs from messaging module for backward compatibility
from .messaging import (
    # CLI Parser
    create_messaging_parser,
    # Message Formatters
    _apply_template,
    _format_multi_agent_request_message,
    _format_normal_message_with_instructions,
    _is_ack_text,
    _load_last_inbound_categories,
    _map_category_from_type,
    _save_last_inbound_categories,
    # Delivery Handlers
    send_message_pyautogui,
    send_message_to_onboarding_coords,
    # Coordination Handlers
    MessageCoordinator,
    # Service Adapters
    ConsolidatedMessagingService,
    send_discord_message,
    broadcast_discord_message,
    # CLI Handlers
    handle_cycle_v2_message,
    handle_message,
    handle_survey,
    handle_consolidation,
    handle_coordinates,
    handle_start_agents,
    handle_save,
    handle_leaderboard,
)
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console

# Message templates (kept for backward compatibility)
from src.core.constants.agent_constants import AGENT_LIST as SWARM_AGENTS
from src.utils.swarm_time import get_swarm_time_display

CLI_HELP_EPILOG = """
🐝 SWARM MESSAGING CLI - COMMAND YOUR AGENTS!
==============================================

EXAMPLES:
--------
# Send message to specific agent
python -m src.services.messaging_cli --message "Start survey" --agent Agent-1
# Broadcast to all agents
python -m src.services.messaging_cli --message "SWARM ALERT!" --broadcast
# Send with priority and tags
python -m src.services.messaging_cli --message "URGENT: Fix issue" \\
    --agent Agent-2 --priority urgent --tags bug critical

🐝 WE. ARE. SWARM - COORDINATE THROUGH PYAUTOGUI!
"""

SURVEY_MESSAGE_TEMPLATE = """
🐝 SWARM SURVEY INITIATED - SRC/ DIRECTORY ANALYSIS
================================================

**OBJECTIVE:** Comprehensive analysis of src/ directory for consolidation planning
**TARGET:** 683 → ~250 files with full functionality preservation

**PHASES:**
1. Structural Analysis (Directories, files, dependencies)
2. Functional Analysis (Services, capabilities, relationships)
3. Quality Assessment (V2 compliance, violations, anti-patterns)
4. Consolidation Planning (Opportunities, risks, rollback strategies)

**COORDINATION:** Real-time via PyAutoGUI messaging system
**COMMANDER:** Captain Agent-4 (Quality Assurance Specialist)

🐝 WE ARE SWARM - UNITED IN ANALYSIS!
"""

CONSOLIDATION_MESSAGE_TEMPLATE = """🔧 CONSOLIDATION UPDATE
======================

**BATCH:** {batch}
**STATUS:** {status}
**TIMESTAMP:** {timestamp}

**COORDINATION:** Real-time swarm coordination active
**COMMANDER:** Captain Agent-4

🔧 CONSOLIDATION PROGRESS CONTINUES...
"""

AGENT_ASSIGNMENTS = {
    "Agent-1": "Service Layer Specialist - Analyze src/services/",
    "Agent-2": "Core Systems Architect - Analyze src/core/",
    "Agent-3": "Web & API Integration - Analyze src/web/ and src/infrastructure/",
    "Agent-4": "Domain & Quality Assurance - Cross-cutting analysis + coordination",
    "Agent-5": "Trading & Gaming Systems - Analyze specialized systems",
    "Agent-6": "Testing & Infrastructure - Analyze tests/ and tools/",
    "Agent-7": "Performance & Monitoring - Analyze monitoring components",
    "Agent-8": "Integration & Coordination - Analyze integration points",
}

# SendMode enum (kept for backward compatibility)
class SendMode:
    ENTER = "enter"
    CTRL_ENTER = "ctrl_enter"

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
<<<<<<< HEAD
    # Coordination Handlers - Lazy import to avoid circular imports
    "_get_message_coordinator",
    # Service Adapters
    "ConsolidatedMessagingService",
=======
    # Coordination Handlers
    "MessageCoordinator",
    # Service Adapters
    "ConsolidatedMessagingService",
    "send_discord_message",
    "broadcast_discord_message",
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
    # CLI Handlers
    "handle_cycle_v2_message",
    "handle_message",
    "handle_survey",
    "handle_consolidation",
    "handle_coordinates",
    "handle_start_agents",
    "handle_save",
    "handle_leaderboard",
    # Templates and Constants
    "CLI_HELP_EPILOG",
    "SURVEY_MESSAGE_TEMPLATE",
    "CONSOLIDATION_MESSAGE_TEMPLATE",
    "AGENT_ASSIGNMENTS",
    "SendMode",
    "SWARM_AGENTS",
]
