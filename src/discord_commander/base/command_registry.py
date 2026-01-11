#!/usr/bin/env python3
"""
Command Registry - Auto-Discovery System
========================================

Automatically discovers and registers Discord command cogs.

<!-- SSOT Domain: discord -->

Features:
- Auto-discovery of command modules
- Automatic cog registration
- Dependency injection for all commands
- Error isolation for failed commands

V2 Compliant: Eliminates repetitive command loading code
Author: Agent-7 (Code Quality Specialist)
Date: 2026-01-11
"""

import importlib
import inspect
import logging
from pathlib import Path
from typing import TYPE_CHECKING, List, Dict, Any, Type

if TYPE_CHECKING:
    from src.discord_commander.unified_discord_bot import UnifiedDiscordBot
    from src.discord_commander.discord_gui_controller import DiscordGUIController

logger = logging.getLogger(__name__)


class CommandRegistry:
    """
    Registry for automatic command discovery and registration.

    Eliminates repetitive command loading code by auto-discovering
    all command cogs and registering them with proper dependencies.
    """

    def __init__(self, bot: "UnifiedDiscordBot", gui_controller: "DiscordGUIController"):
        """Initialize command registry."""
        self.bot = bot
        self.gui_controller = gui_controller
        self.logger = logging.getLogger(__name__)

        # Command modules to auto-discover
        self.command_modules = [
            "src.discord_commander.commands.control_panel_commands",
            "src.discord_commander.commands.core_messaging_commands",
            "src.discord_commander.commands.messaging_core_commands",
            "src.discord_commander.commands.utility_commands",
            "src.discord_commander.commands.system_control_commands",
            "src.discord_commander.commands.agent_management_commands",
            "src.discord_commander.commands.onboarding_commands",
            "src.discord_commander.commands.profile_commands",
            "src.discord_commander.commands.placeholder_commands",
            "src.discord_commander.commands.messaging_monitor_commands",
            "src.discord_commander.commands.bot_messaging_commands",
            "src.discord_commander.commands.thea_commands",
        ]

    async def discover_and_register_all(self) -> Dict[str, bool]:
        """
        Auto-discover and register all command cogs.

        Returns dict mapping cog names to registration success.
        """
        results = {}

        for module_name in self.command_modules:
            try:
                success = await self._register_command_module(module_name)
                results[module_name.split('.')[-1]] = success

                if success:
                    self.logger.info(f"✅ Registered command module: {module_name}")
                else:
                    self.logger.warning(f"⚠️ Failed to register command module: {module_name}")

            except Exception as e:
                self.logger.error(f"❌ Error registering {module_name}: {e}")
                results[module_name.split('.')[-1]] = False

        return results

    async def _register_command_module(self, module_name: str) -> bool:
        """Register a single command module."""
        try:
            # Import the module
            module = importlib.import_module(module_name)

            # Find all command cog classes
            cog_classes = self._find_command_cogs(module)

            if not cog_classes:
                self.logger.warning(f"No command cogs found in {module_name}")
                return False

            # Register each cog
            for cog_class in cog_classes:
                try:
                    await self._register_cog(cog_class)
                except Exception as e:
                    self.logger.error(f"Failed to register cog {cog_class.__name__}: {e}")
                    continue

            return True

        except ImportError as e:
            self.logger.error(f"Failed to import {module_name}: {e}")
            return False

    def _find_command_cogs(self, module) -> List[Type]:
        """Find all command cog classes in a module."""
        cog_classes = []

        for name, obj in inspect.getmembers(module):
            if (inspect.isclass(obj) and
                hasattr(obj, '__bases__') and
                any('commands.Cog' in str(base) for base in obj.__bases__) and
                not name.startswith('_')):
                cog_classes.append(obj)

        return cog_classes

    async def _register_cog(self, cog_class: Type) -> None:
        """Register a single cog with dependency injection."""
        # Create cog instance with dependencies
        try:
            cog_instance = cog_class(self.bot, self.gui_controller)
            await self.bot.add_cog(cog_instance)
            self.logger.debug(f"Registered cog: {cog_class.__name__}")
        except Exception as e:
            raise RuntimeError(f"Failed to instantiate {cog_class.__name__}: {e}")


class CommandMetrics:
    """Collect metrics about registered commands."""

    def __init__(self, bot: "UnifiedDiscordBot"):
        self.bot = bot
        self.metrics = {
            'total_cogs': 0,
            'total_commands': 0,
            'command_types': {},
            'role_required_commands': 0,
        }

    def collect_metrics(self) -> Dict[str, Any]:
        """Collect comprehensive command metrics."""
        self.metrics = {
            'total_cogs': len(self.bot.cogs),
            'total_commands': 0,
            'command_types': {},
            'role_required_commands': 0,
        }

        for cog_name, cog in self.bot.cogs.items():
            cog_commands = len([attr for attr in dir(cog) if hasattr(getattr(cog, attr), 'name')])
            self.metrics['total_commands'] += cog_commands

            # Analyze command types and requirements
            for attr_name in dir(cog):
                attr = getattr(cog, attr_name)
                if hasattr(attr, 'name') and hasattr(attr, 'has_any_role'):
                    command_name = attr.name
                    self.metrics['command_types'][command_name] = {
                        'cog': cog_name,
                        'has_role_requirement': bool(attr.has_any_role),
                        'aliases': getattr(attr, 'aliases', []),
                    }
                    if attr.has_any_role:
                        self.metrics['role_required_commands'] += 1

        return self.metrics

    def print_report(self) -> None:
        """Print a formatted metrics report."""
        metrics = self.collect_metrics()

        print("📊 COMMAND REGISTRY METRICS")
        print("=" * 40)
        print(f"Total Cogs: {metrics['total_cogs']}")
        print(f"Total Commands: {metrics['total_commands']}")
        print(f"Role-Required Commands: {metrics['role_required_commands']}")
        print(f"Public Commands: {metrics['total_commands'] - metrics['role_required_commands']}")
        print()
        print("🔒 Commands by Role Requirement:")
        print(f"   Admin/Captain/Swarm Commander: {metrics['role_required_commands']}")
        print(f"   Public Access: {metrics['total_commands'] - metrics['role_required_commands']}")


__all__ = [
    "CommandRegistry",
    "CommandMetrics",
]