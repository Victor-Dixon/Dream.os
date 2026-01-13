#!/usr/bin/env python3
"""
🔌 Plugin Manager MVP
====================

Basic plugin lifecycle management for Phase 3 MVP.
Demonstrates plugin loading, initialization, and execution.

<!-- SSOT Domain: plugins -->
"""

from __future__ import annotations

import logging
import importlib
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

from .plugin_interface import PluginInterface, PluginInfo, PluginStatus, PluginContext
from .plugin_registry import PluginRegistry


logger = logging.getLogger(__name__)


@dataclass
class PluginInstance:
    """Container for loaded plugin instance."""
    plugin: PluginInterface
    info: PluginInfo
    context: PluginContext
    status: PluginStatus


class PluginManager:
    """
    Basic Plugin Manager - Phase 3 MVP

    Manages plugin lifecycle: discovery, loading, initialization, execution.
    """

    def __init__(self, plugins_dir: Path = None):
        """
        Initialize plugin manager.

        Args:
            plugins_dir: Directory containing plugin packages
        """
        self.plugins_dir = plugins_dir or Path(__file__).parent / "packages"
        self.registry = PluginRegistry(self.plugins_dir)
        self.active_plugins: Dict[str, PluginInstance] = {}

        logger.info("Plugin manager initialized")

    def discover_and_register_plugins(self) -> int:
        """
        Discover and register all available plugins.

        Returns:
            int: Number of plugins registered
        """
        discovered = self.registry.discover_plugins()
        registered_count = 0

        for plugin_info in discovered:
            if self.registry.register_plugin(plugin_info):
                registered_count += 1
                logger.info(f"Registered plugin: {plugin_info.name}")
            else:
                logger.warning(f"Failed to register plugin: {plugin_info.name}")

        logger.info(f"Plugin discovery complete: {registered_count}/{len(discovered)} registered")
        return registered_count

    def load_plugin(self, plugin_id: str, config: dict = None) -> bool:
        """
        Load and initialize a plugin.

        Args:
            plugin_id: Plugin ID to load
            config: Plugin-specific configuration

        Returns:
            bool: True if loading successful
        """
        try:
            # Get plugin info
            plugin_info = self.registry.get_plugin_info(plugin_id)
            if not plugin_info:
                logger.error(f"Plugin not found: {plugin_id}")
                return False

            # Check if already loaded
            if plugin_id in self.active_plugins:
                logger.warning(f"Plugin already loaded: {plugin_id}")
                return True

            # Resolve dependencies (MVP: just check they exist)
            for dep in plugin_info.dependencies:
                if dep not in self.active_plugins and dep != plugin_id:
                    logger.warning(f"Missing dependency for {plugin_id}: {dep}")
                    # For MVP, we'll allow loading with missing dependencies

            # Load plugin module
            module_path = f"src.plugins.packages.{plugin_id}.{plugin_info.entry_point.split(':')[0]}"
            plugin_module = importlib.import_module(module_path)

            # Get plugin class
            plugin_class_name = plugin_info.entry_point.split(':')[1]
            plugin_class = getattr(plugin_module, plugin_class_name)

            # Create plugin instance
            plugin_instance = plugin_class()

            # Create plugin context
            context = PluginContext(
                plugin_id=plugin_id,
                config=config or {},
                logger=logging.getLogger(f"plugin.{plugin_id}"),
                event_bus=None,  # MVP: no event bus yet
                resource_limits={
                    "max_memory_mb": 100,
                    "max_cpu_percent": 10,
                    "max_execution_time_sec": 30
                },
                permissions=plugin_info.permissions
            )

            # Initialize plugin
            if plugin_instance.initialize(config or {}, context):
                # Store plugin instance
                plugin_wrapper = PluginInstance(
                    plugin=plugin_instance,
                    info=plugin_info,
                    context=context,
                    status=PluginStatus.ACTIVE
                )

                self.active_plugins[plugin_id] = plugin_wrapper
                logger.info(f"Plugin loaded successfully: {plugin_id}")
                return True
            else:
                logger.error(f"Plugin initialization failed: {plugin_id}")
                return False

        except Exception as e:
            logger.error(f"Failed to load plugin {plugin_id}: {e}")
            return False

    def unload_plugin(self, plugin_id: str) -> bool:
        """
        Unload a plugin.

        Args:
            plugin_id: Plugin ID to unload

        Returns:
            bool: True if unloading successful
        """
        if plugin_id not in self.active_plugins:
            logger.warning(f"Plugin not loaded: {plugin_id}")
            return False

        try:
            plugin_instance = self.active_plugins[plugin_id]

            # Cleanup plugin
            if plugin_instance.plugin.cleanup():
                del self.active_plugins[plugin_id]
                logger.info(f"Plugin unloaded successfully: {plugin_id}")
                return True
            else:
                logger.error(f"Plugin cleanup failed: {plugin_id}")
                return False

        except Exception as e:
            logger.error(f"Failed to unload plugin {plugin_id}: {e}")
            return False

    def execute_plugin(self, plugin_id: str, input_data: Any) -> Any:
        """
        Execute a plugin with input data.

        Args:
            plugin_id: Plugin ID to execute
            input_data: Input data for plugin

        Returns:
            Any: Plugin execution result
        """
        if plugin_id not in self.active_plugins:
            return {"error": f"Plugin not loaded: {plugin_id}"}

        try:
            plugin_instance = self.active_plugins[plugin_id]
            return plugin_instance.plugin.execute(input_data)

        except Exception as e:
            logger.error(f"Plugin execution failed: {plugin_id} - {e}")
            return {"error": str(e)}

    def get_plugin_status(self, plugin_id: str) -> Optional[PluginStatus]:
        """
        Get status of a specific plugin.

        Args:
            plugin_id: Plugin ID to check

        Returns:
            Optional[PluginStatus]: Plugin status or None if not found
        """
        if plugin_id in self.active_plugins:
            return self.active_plugins[plugin_id].plugin.get_status()
        return None

    def get_loaded_plugins(self) -> List[str]:
        """
        Get list of loaded plugin IDs.

        Returns:
            List[str]: List of loaded plugin IDs
        """
        return list(self.active_plugins.keys())

    def get_registered_plugins(self) -> List[PluginInfo]:
        """
        Get all registered plugins.

        Returns:
            List[PluginInfo]: List of all registered plugin metadata
        """
        return self.registry.get_all_plugins()

    def shutdown(self) -> bool:
        """
        Shutdown plugin manager and unload all plugins.

        Returns:
            bool: True if shutdown successful
        """
        logger.info("Shutting down plugin manager...")

        success = True
        for plugin_id in list(self.active_plugins.keys()):
            if not self.unload_plugin(plugin_id):
                success = False

        logger.info("Plugin manager shutdown complete")
        return success


# Global plugin manager instance
_plugin_manager: Optional[PluginManager] = None


def get_plugin_manager() -> PluginManager:
    """Get global plugin manager instance."""
    global _plugin_manager
    if _plugin_manager is None:
        _plugin_manager = PluginManager()
    return _plugin_manager


def initialize_plugin_system() -> bool:
    """
    Initialize the plugin system.

    Returns:
        bool: True if initialization successful
    """
    try:
        manager = get_plugin_manager()

        # Discover and register plugins
        registered_count = manager.discover_and_register_plugins()

        # Load the analytics plugin as MVP demonstration
        if manager.load_plugin("analytics_plugin"):
            logger.info("✅ Plugin system initialized - Analytics plugin loaded")
            return True
        else:
            logger.error("❌ Failed to load analytics plugin")
            return False

    except Exception as e:
        logger.error(f"Failed to initialize plugin system: {e}")
        return False


def demo_plugin_system() -> None:
    """Demonstrate the plugin system working."""
    print("🔌 Agent Cellphone V2 Plugin System Demo")
    print("=" * 50)

    # Initialize system
    if not initialize_plugin_system():
        print("❌ Failed to initialize plugin system")
        return

    manager = get_plugin_manager()

    print(f"📦 Registered plugins: {len(manager.get_registered_plugins())}")
    print(f"🔧 Loaded plugins: {manager.get_loaded_plugins()}")

    # Execute analytics plugin
    print("\n📊 Testing Analytics Plugin...")

    # Get current metrics
    result = manager.execute_plugin("analytics_plugin", {"command": "get_metrics"})
    print(f"📈 Current metrics: {result}")

    # Get system health
    result = manager.execute_plugin("analytics_plugin", {"command": "get_health"})
    print(f"❤️ System health: {result}")

    print("\n✅ Plugin system demo complete!")
    print("🎉 Phase 3 MVP - Plugin framework operational!")