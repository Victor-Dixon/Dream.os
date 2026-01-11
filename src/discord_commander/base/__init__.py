"""
Base Classes for Discord Commands
=================================

Base classes and mixins to eliminate repetitive code in Discord command cogs.

<!-- SSOT Domain: discord -->
"""

from .command_base import (
    BaseCommandCog,
    LoggingMixin,
    EmbedMixin,
    ErrorHandlingMixin,
    RoleRequiredMixin,
)

from .command_registry import (
    CommandRegistry,
    CommandMetrics,
)

__all__ = [
    "BaseCommandCog",
    "LoggingMixin",
    "EmbedMixin",
    "ErrorHandlingMixin",
    "RoleRequiredMixin",
    "CommandRegistry",
    "CommandMetrics",
]