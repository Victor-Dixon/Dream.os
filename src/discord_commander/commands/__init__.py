"""
Discord Command Handlers
========================

Modular command handlers extracted from unified_discord_bot.py for V2 compliance.
Each module contains related commands grouped by functionality.

V2 Compliance: Each module <300 lines, <5 classes, <10 functions
"""

# Import all command cogs for easy registration
from .core_messaging_commands import CoreMessagingCommands
from .system_control_commands import SystemControlCommands
# TODO: Add remaining command modules as they are extracted
# from .onboarding_commands import OnboardingCommands
# from .utility_commands import UtilityCommands
# from .profile_commands import ProfileCommands
# from .agent_management_commands import AgentManagementCommands
# from .placeholder_commands import PlaceholderCommands

__all__ = [
    "CoreMessagingCommands",
    "SystemControlCommands",
    # TODO: Add remaining command modules as they are extracted
    # "OnboardingCommands",
    # "UtilityCommands",
    # "ProfileCommands",
    # "AgentManagementCommands",
    # "PlaceholderCommands",
]

