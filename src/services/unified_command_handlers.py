"""
Unified Command Handlers V2 - Phase 4 Consolidation
====================================================

PHASE 4 CONSOLIDATION: Consolidated command handler modules
Merged from: handlers/command_handler.py, overnight_command_handler.py, role_command_handler.py
Reduced from 3 separate files (~500 lines) to 1 consolidated module

Consolidated command handlers for messaging CLI operations:
- MessageCommandHandler: Core messaging commands (coordinates, list_agents, send_message, etc.)
- OvernightCommandHandler: Autonomous overnight operations
- RoleCommandHandler: Role-based command operations

Features:
- Unified command processing interface
- Consolidated error handling and logging
- Single responsibility principle maintained
- V2 compliance and SSOT integration

V2 Compliance: <400 lines, modular imports
Author: Agent-7 (Modularization)
<!-- SSOT Domain: integration -->
"""

# Import all handlers from modular structure
from .command_handlers.message_command_handler import MessageCommandHandler
from .command_handlers.overnight_command_handler import OvernightCommandHandler
from .command_handlers.role_command_handler import RoleCommandHandler
from .command_handlers.task_command_handler import TaskCommandHandler
from .command_handlers.batch_message_command_handler import BatchMessageCommandHandler

# Backward compatibility aliases
CommandHandler = MessageCommandHandler

# Export all handlers
__all__ = [
    "MessageCommandHandler",
    "OvernightCommandHandler",
    "RoleCommandHandler",
    "TaskCommandHandler",
    "BatchMessageCommandHandler",
    "CommandHandler",  # Backward compatibility
]