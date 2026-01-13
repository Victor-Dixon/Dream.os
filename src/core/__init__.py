"""
Core Module

<!-- SSOT Domain: core -->
"""
# Core Module - Essential Exports Only
# ====================================
#
# This module exports only the most commonly used symbols from core modules.
# For other symbols, use direct imports: from src.core.<module> import <symbol>
#
# Refactored: Agent-8 (2025-01-27) - Reduced from 50+ module exports to essential symbols only
# Rationale: Most code uses direct imports, module-level exports were mostly unused
# Performance: Faster imports, no circular import risk, clearer API surface

# Messaging System (Most Used - 12+ imports)
from .messaging_core import (
    send_message,
    send_message_object,
    broadcast_message,
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
    get_messaging_core,
)

# Logging System (Most Used - 16+ imports)
from .unified_logging_system import (
    get_logger,
    get_logging_system,
    configure_logging,
)

# Configuration System (Most Used - 5+ imports)
from .config_ssot import (
    get_config,
    get_agent_config,
    get_timeout_config,
    get_browser_config,
    get_threshold_config,
    UnifiedConfigManager,
)

# Coordinate System (Most Used - 5+ imports)
from .coordinate_loader import (
    get_coordinate_loader,
    CoordinateLoader,
)

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> origin/codex/build-tsla-morning-report-system
# Message Queue (Used - 3+ imports) - Registry pattern available
# Import from message_queue_registry as needed to avoid circular imports
MessageQueue = None
IMessageQueue = None
<<<<<<< HEAD
=======
# Message Queue (Used - 3+ imports)
from .message_queue import (
    MessageQueue,
    IMessageQueue,
)
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
>>>>>>> origin/codex/build-tsla-morning-report-system

# Agent Activity Tracker (Used - 2+ imports)
from .agent_activity_tracker import (
    get_activity_tracker,
    AgentActivityTracker,
)

# Keyboard Control (Used - 5+ imports)
from .keyboard_control_lock import (
    keyboard_control,
    is_locked,
)

# Backward Compatibility Aliases
from .agent_documentation_service import (
    AgentDocumentationService as AgentDocs,
    create_agent_docs,
)

__all__ = [
    # Messaging
    'send_message',
    'send_message_object',
    'broadcast_message',
    'UnifiedMessage',
    'UnifiedMessageType',
    'UnifiedMessagePriority',
    'UnifiedMessageTag',
    'get_messaging_core',
    # Logging
    'get_logger',
    'get_logging_system',
    'configure_logging',
    # Config
    'get_config',
    'get_agent_config',
    'get_timeout_config',
    'get_browser_config',
    'get_threshold_config',
    'UnifiedConfigManager',
    # Coordinates
    'get_coordinate_loader',
    'CoordinateLoader',
    # Message Queue
    'MessageQueue',
    'IMessageQueue',
    # Agent Activity
    'get_activity_tracker',
    'AgentActivityTracker',
    # Keyboard Control
    'keyboard_control',
    'is_locked',
    # Backward Compatibility
    'AgentDocs',
    'create_agent_docs',
]
