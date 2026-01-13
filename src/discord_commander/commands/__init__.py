"""
<!-- SSOT Domain: discord -->

Discord Command Handlers
========================

Modular command handlers extracted from unified_discord_bot.py for V2 compliance.
Each module contains related commands grouped by functionality.

V2 Compliance: Each module <300 lines, <5 classes, <10 functions
"""

# Import all command cogs for easy registration
from .core_messaging_commands import CoreMessagingCommands
from .system_control_commands import SystemControlCommands
from .onboarding_commands import OnboardingCommands
from .utility_commands import UtilityCommands
from .agent_management_commands import AgentManagementCommands
from .profile_commands import ProfileCommands
from .placeholder_commands import PlaceholderCommands
from .control_panel_commands import ControlPanelCommands
from .thea_commands import TheaCommands
from .bot_messaging_commands import MessagingCommands

# Auto-register cogs with the registry for reduced boilerplate
from .command_base import command_registry

# Register all command cogs for automatic instantiation
command_registry.register_cog_class(CoreMessagingCommands)
command_registry.register_cog_class(SystemControlCommands)
command_registry.register_cog_class(OnboardingCommands)
command_registry.register_cog_class(UtilityCommands)
command_registry.register_cog_class(AgentManagementCommands)
command_registry.register_cog_class(ProfileCommands)
command_registry.register_cog_class(PlaceholderCommands)
command_registry.register_cog_class(ControlPanelCommands)
command_registry.register_cog_class(MessagingCommands)
command_registry.register_cog_class(TheaCommands)

__all__ = [
    "CoreMessagingCommands",
    "SystemControlCommands",
    "OnboardingCommands",
    "UtilityCommands",
    "AgentManagementCommands",
    "ProfileCommands",
    "PlaceholderCommands",
    "ControlPanelCommands",
    "TheaCommands",
    "MessagingCommands",
    "command_registry",
]

