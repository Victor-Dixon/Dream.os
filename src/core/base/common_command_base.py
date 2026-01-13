#!/usr/bin/env python3
"""
Common Command Base Classes - Phase 2 Base Init Extraction
========================================================

PHASE 2 EXECUTION: Base init extraction (common __init__ signature)
Consolidates identical initialization patterns across commands/controllers.

This module provides standardized base classes for:
- Discord command cogs with common bot/logger initialization
- Service handlers with unified initialization patterns
- Controllers with consistent setup

V2 Compliance: Standardized initialization, reduced code duplication
SOLID Principles: DRY principle, base class pattern

Author: Agent-1 (Infrastructure & Core Systems)
Date: 2026-01-12
"""

import logging
from abc import ABC
from typing import TYPE_CHECKING, Optional, Any

try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    discord = None
    commands = None
    DISCORD_AVAILABLE = False

if TYPE_CHECKING:
    from ...discord_commander.unified_discord_bot import UnifiedDiscordBot
    from ...discord_commander.gui.discord_gui_controller import DiscordGUIController


class CommonCommandBase(commands.Cog, ABC):
    """
    Common base class for Discord command cogs.

    PHASE 2 EXECUTION: Extracts common __init__ pattern:
    - Bot assignment
    - Logger initialization
    - Common attributes setup

    Usage:
        class MyCommands(CommonCommandBase):
            def __init__(self, bot):
                super().__init__(bot)  # Handles all common initialization
    """

    def __init__(self, bot: "UnifiedDiscordBot"):
        """
        Initialize common command base.

        Args:
            bot: The Discord bot instance
        """
        super().__init__()
        self.bot = bot
        self.logger = logging.getLogger(self.__class__.__module__)

        # Initialize common attributes
        self._setup_common_attributes()

    def _setup_common_attributes(self):
        """Setup common attributes used by most command cogs."""
        # Common command attributes that many cogs need
        self.command_prefix = "!"
        self.embed_color = 0x00ff00  # Default green
        self.error_color = 0xff0000  # Red for errors

    def create_embed(self, title: str, description: str = "",
                    color: Optional[int] = None) -> discord.Embed:
        """
        Create a standardized embed.

        Args:
            title: Embed title
            description: Embed description
            color: Embed color (uses default if None)

        Returns:
            Discord embed object
        """
        if not DISCORD_AVAILABLE:
            return None

        embed = discord.Embed(
            title=title,
            description=description,
            color=color or self.embed_color
        )
        return embed

    def create_error_embed(self, error_message: str) -> discord.Embed:
        """
        Create a standardized error embed.

        Args:
            error_message: The error message to display

        Returns:
            Error embed with red color
        """
        if not DISCORD_AVAILABLE:
            return None

        return discord.Embed(
            title="❌ Error",
            description=error_message,
            color=self.error_color
        )


class CommonHandlerBase(ABC):
    """
    Common base class for service handlers.

    PHASE 2 EXECUTION: Extracts common handler initialization patterns:
    - Service name assignment
    - Logger setup
    - Common handler attributes

    Usage:
        class MyHandler(CommonHandlerBase):
            def __init__(self):
                super().__init__("MyHandler")  # Handles all common initialization
    """

    def __init__(self, handler_name: str):
        """
        Initialize common handler base.

        Args:
            handler_name: Name of the handler for logging
        """
        self.handler_name = handler_name
        self.logger = logging.getLogger(self.__class__.__module__)

        # Initialize common handler attributes
        self._setup_handler_attributes()

    def _setup_handler_attributes(self):
        """Setup common attributes used by most handlers."""
        # Common handler attributes
        self.exit_code = 0
        self.success_count = 0
        self.error_count = 0
        self.last_operation = None

    def can_handle(self, args) -> bool:
        """
        Check if this handler can handle the given arguments.

        This is a common pattern across handlers. Subclasses should override.

        Args:
            args: Command line arguments or similar

        Returns:
            True if this handler can handle the args
        """
        return False

    def handle(self, args) -> dict:
        """
        Handle the command/request.

        This is a common pattern across handlers. Subclasses should override.

        Args:
            args: Command line arguments or similar

        Returns:
            Result dictionary
        """
        return {
            'success': False,
            'error': 'Handler not implemented',
            'handler': self.handler_name
        }

    def log_operation_start(self, operation: str, *args, **kwargs):
        """
        Log the start of an operation.

        Args:
            operation: Name of the operation
            *args: Additional positional arguments to log
            **kwargs: Additional keyword arguments to log
        """
        self.last_operation = operation
        self.logger.info(f"Starting {operation}", extra={
            'operation': operation,
            'args_count': len(args),
            'kwargs_keys': list(kwargs.keys()) if kwargs else []
        })

    def log_operation_complete(self, operation: str, success: bool = True,
                              result: Any = None):
        """
        Log the completion of an operation.

        Args:
            operation: Name of the operation
            success: Whether the operation succeeded
            result: Operation result (if any)
        """
        if success:
            self.success_count += 1
            self.logger.info(f"Completed {operation} successfully")
        else:
            self.error_count += 1
            self.logger.error(f"Failed {operation}", extra={
                'operation': operation,
                'result': str(result) if result else None
            })


class CommonControllerBase(ABC):
    """
    Common base class for controllers.

    PHASE 2 EXECUTION: Extracts common controller initialization patterns:
    - Controller name assignment
    - Logger setup
    - Common controller attributes

    Usage:
        class MyController(CommonControllerBase):
            def __init__(self, config):
                super().__init__("MyController")  # Handles common initialization
                self.config = config  # Custom initialization
    """

    def __init__(self, controller_name: str):
        """
        Initialize common controller base.

        Args:
            controller_name: Name of the controller for logging
        """
        self.controller_name = controller_name
        self.logger = logging.getLogger(self.__class__.__module__)

        # Initialize common controller attributes
        self._setup_controller_attributes()

    def _setup_controller_attributes(self):
        """Setup common attributes used by most controllers."""
        # Common controller attributes
        self.is_initialized = False
        self.start_time = None
        self.operation_count = 0
        self.error_count = 0

    def initialize(self) -> bool:
        """
        Initialize the controller.

        Returns:
            True if initialization successful
        """
        try:
            self.start_time = __import__('time').time()
            self.is_initialized = True
            self.logger.info(f"Controller {self.controller_name} initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize controller {self.controller_name}: {e}")
            return False

    def get_status(self) -> dict:
        """
        Get controller status information.

        Returns:
            Status dictionary
        """
        uptime = 0
        if self.start_time:
            uptime = __import__('time').time() - self.start_time

        return {
            'controller_name': self.controller_name,
            'is_initialized': self.is_initialized,
            'uptime_seconds': uptime,
            'operation_count': self.operation_count,
            'error_count': self.error_count,
            'error_rate': self.error_count / max(self.operation_count, 1)
        }


# Convenience functions for creating standardized instances
def create_command_cog(bot: "UnifiedDiscordBot", cog_class):
    """
    Create a command cog with standardized initialization.

    Args:
        bot: The Discord bot instance
        cog_class: The cog class to instantiate

    Returns:
        Instantiated cog
    """
    return cog_class(bot)


def create_handler(handler_class, *args, **kwargs):
    """
    Create a handler with standardized initialization.

    Args:
        handler_class: The handler class to instantiate
        *args: Positional arguments for handler
        **kwargs: Keyword arguments for handler

    Returns:
        Instantiated handler
    """
    return handler_class(*args, **kwargs)


def create_controller(controller_class, controller_name: str, *args, **kwargs):
    """
    Create a controller with standardized initialization.

    Args:
        controller_class: The controller class to instantiate
        controller_name: Name for the controller
        *args: Additional positional arguments
        **kwargs: Additional keyword arguments

    Returns:
        Instantiated controller
    """
    instance = controller_class(controller_name, *args, **kwargs)
    instance.initialize()
    return instance


# Export all classes and functions
__all__ = [
    'CommonCommandBase',
    'CommonHandlerBase',
    'CommonControllerBase',
    'create_command_cog',
    'create_handler',
    'create_controller'
]