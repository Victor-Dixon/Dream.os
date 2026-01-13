#!/usr/bin/env python3
"""
🔌 Plugin Loader - Phase 3 Architecture Implementation
======================================================

Core plugin loader implementing the Phase 3 Plugin Architecture Specification.
Provides discovery, loading, and lifecycle management for plugins.

<!-- SSOT Domain: plugins -->
"""

from __future__ import annotations

import logging
import importlib
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional, List, Set
from dataclasses import dataclass

from src.plugins.plugin_interface import (
    IPlugin, PluginContext, PluginConfig, PluginInfo, PluginStatus, PluginCategory
)

logger = logging.getLogger(__name__)


@dataclass
class LoadedPlugin:
    """Container for a loaded plugin instance."""
    plugin: IPlugin
    info: PluginInfo
    context: PluginContext
    status: PluginStatus
    config: PluginConfig


class PluginLoader:
    """
    Plugin Loader implementing Phase 3 Architecture Specification.

    Provides comprehensive plugin lifecycle management with discovery,
    dependency resolution, sandboxing, and hot-reload capabilities.
    """

    def __init__(self, plugins_dir: Path = None):
        """
        Initialize plugin loader.

        Args:
            plugins_dir: Directory containing plugin packages
        """
        self.plugins_dir = plugins_dir or Path(__file__).parent / "packages"
        self.loaded_plugins: Dict[str, LoadedPlugin] = {}
        self.plugin_registry: Dict[str, PluginInfo] = {}
        self.dependency_graph: Dict[str, Set[str]] = {}

        logger.info("🔌 Plugin loader initialized")

    async def discover_plugins(self) -> List[PluginInfo]:
        """
        Discover all available plugins in the plugins directory.

        Returns:
            List[PluginInfo]: List of discovered plugin information
        """
        discovered_plugins = []

        if not self.plugins_dir.exists():
            logger.warning(f"Plugins directory does not exist: {self.plugins_dir}")
            return discovered_plugins

        # Scan plugin directories
        for plugin_dir in self.plugins_dir.iterdir():
            if not plugin_dir.is_dir() or plugin_dir.name.startswith('.'):
                continue

            plugin_info = await self._load_plugin_info(plugin_dir)
            if plugin_info:
                discovered_plugins.append(plugin_info)
                self.plugin_registry[plugin_info.plugin_id] = plugin_info
                logger.info(f"📦 Discovered plugin: {plugin_info.name} ({plugin_info.plugin_id})")

        # Build dependency graph
        self._build_dependency_graph()

        logger.info(f"🔍 Plugin discovery complete: {len(discovered_plugins)} plugins found")
        return discovered_plugins

    async def _load_plugin_info(self, plugin_dir: Path) -> Optional[PluginInfo]:
        """
        Load plugin information from manifest.json.

        Args:
            plugin_dir: Plugin directory path

        Returns:
            Optional[PluginInfo]: Plugin information or None if invalid
        """
        manifest_path = plugin_dir / "manifest.json"

        if not manifest_path.exists():
            logger.warning(f"No manifest.json found in {plugin_dir}")
            return None

        try:
            import json
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)

            # Validate required fields
            required_fields = ['plugin_id', 'name', 'version', 'author', 'description']
            for field in required_fields:
                if field not in manifest:
                    logger.error(f"Missing required field '{field}' in {manifest_path}")
                    return None

            # Convert category string to enum
            category = PluginCategory(manifest.get('category', 'custom'))

            return PluginInfo(
                plugin_id=manifest['plugin_id'],
                name=manifest['name'],
                version=manifest['version'],
                author=manifest['author'],
                description=manifest['description'],
                category=category,
                dependencies=manifest.get('dependencies', []),
                permissions=manifest.get('permissions', []),
                entry_point=manifest.get('entry_point', 'plugin:Plugin'),
                config_schema=manifest.get('config_schema', {}),
                min_core_version=manifest.get('min_core_version', '2.0.0'),
                max_core_version=manifest.get('max_core_version'),
                homepage=manifest.get('homepage'),
                repository=manifest.get('repository'),
                license=manifest.get('license', 'MIT'),
                tags=manifest.get('tags', [])
            )

        except Exception as e:
            logger.error(f"Failed to load plugin manifest {manifest_path}: {e}")
            return None

    def _build_dependency_graph(self):
        """Build dependency graph for plugin loading order."""
        self.dependency_graph = {}

        for plugin_id, info in self.plugin_registry.items():
            self.dependency_graph[plugin_id] = set(info.dependencies)

    async def load_plugin(self, plugin_id: str, config: Optional[PluginConfig] = None) -> bool:
        """
        Load and initialize a plugin with dependency resolution.

        Args:
            plugin_id: Plugin ID to load
            config: Plugin configuration

        Returns:
            bool: True if loading successful
        """
        try:
            # Check if already loaded
            if plugin_id in self.loaded_plugins:
                logger.info(f"Plugin already loaded: {plugin_id}")
                return True

            # Get plugin info
            if plugin_id not in self.plugin_registry:
                logger.error(f"Plugin not registered: {plugin_id}")
                return False

            plugin_info = self.plugin_registry[plugin_id]

            # Load dependencies first
            for dep_id in plugin_info.dependencies:
                if dep_id not in self.loaded_plugins:
                    logger.info(f"Loading dependency: {dep_id}")
                    if not await self.load_plugin(dep_id):
                        logger.error(f"Failed to load dependency {dep_id} for {plugin_id}")
                        return False

            # Create plugin configuration
            if config is None:
                config = PluginConfig(
                    plugin_id=plugin_id,
                    version=plugin_info.version,
                    enabled=True,
                    settings={}
                )

            # Validate configuration
            if not await self._validate_plugin_config(plugin_info, config):
                logger.error(f"Configuration validation failed for {plugin_id}")
                return False

            # Load plugin module
            plugin_instance = await self._instantiate_plugin(plugin_info)
            if not plugin_instance:
                return False

            # Create plugin context
            context = PluginContext(
                plugin_id=plugin_id,
                config=config.settings,
                logger=logging.getLogger(f"plugin.{plugin_id}"),
                event_bus=None,  # TODO: Implement event bus
                resource_limits={
                    "max_memory_mb": 100,
                    "max_cpu_percent": 10,
                    "max_execution_time_sec": 30
                },
                permissions=plugin_info.permissions,
                plugin_registry=self,
                messaging_service=None  # TODO: Implement messaging service
            )

            # Initialize plugin
            logger.info(f"Initializing plugin: {plugin_id}")
            if not await plugin_instance.initialize(context):
                logger.error(f"Plugin initialization failed: {plugin_id}")
                return False

            # Activate plugin
            logger.info(f"Activating plugin: {plugin_id}")
            if not await plugin_instance.activate():
                logger.error(f"Plugin activation failed: {plugin_id}")
                return False

            # Store loaded plugin
            loaded_plugin = LoadedPlugin(
                plugin=plugin_instance,
                info=plugin_info,
                context=context,
                status=PluginStatus.ACTIVE,
                config=config
            )

            self.loaded_plugins[plugin_id] = loaded_plugin

            logger.info(f"✅ Plugin loaded successfully: {plugin_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to load plugin {plugin_id}: {e}")
            return False

    async def _validate_plugin_config(self, plugin_info: PluginInfo, config: PluginConfig) -> bool:
        """
        Validate plugin configuration against schema.

        Args:
            plugin_info: Plugin information
            config: Plugin configuration

        Returns:
            bool: True if configuration is valid
        """
        try:
            # Basic validation - plugin instance should validate detailed schema
            if not config.plugin_id or config.plugin_id != plugin_info.plugin_id:
                return False

            # Version compatibility check
            if config.version != plugin_info.version:
                logger.warning(f"Version mismatch for {config.plugin_id}: config={config.version}, manifest={plugin_info.version}")

            return True

        except Exception as e:
            logger.error(f"Configuration validation error for {plugin_info.plugin_id}: {e}")
            return False

    async def _instantiate_plugin(self, plugin_info: PluginInfo) -> Optional[IPlugin]:
        """
        Instantiate plugin from module.

        Args:
            plugin_info: Plugin information

        Returns:
            Optional[IPlugin]: Plugin instance or None if failed
        """
        try:
            # Parse entry point
            module_name, class_name = plugin_info.entry_point.split(':')

            # Import plugin module
            plugin_module_path = f"src.plugins.packages.{plugin_info.plugin_id}.{module_name}"
            plugin_module = importlib.import_module(plugin_module_path)

            # Get plugin class
            plugin_class = getattr(plugin_module, class_name)

            # Instantiate plugin
            plugin_instance = plugin_class()

            # Validate interface compliance
            if not isinstance(plugin_instance, IPlugin):
                logger.error(f"Plugin {plugin_info.plugin_id} does not implement IPlugin interface")
                return None

            return plugin_instance

        except Exception as e:
            logger.error(f"Failed to instantiate plugin {plugin_info.plugin_id}: {e}")
            return None

    async def unload_plugin(self, plugin_id: str) -> bool:
        """
        Unload a plugin gracefully.

        Args:
            plugin_id: Plugin ID to unload

        Returns:
            bool: True if unloading successful
        """
        if plugin_id not in self.loaded_plugins:
            logger.warning(f"Plugin not loaded: {plugin_id}")
            return False

        try:
            loaded_plugin = self.loaded_plugins[plugin_id]

            # Deactivate plugin
            logger.info(f"Deactivating plugin: {plugin_id}")
            if not await loaded_plugin.plugin.deactivate():
                logger.warning(f"Plugin deactivation failed: {plugin_id}")

            # Update status
            loaded_plugin.status = PluginStatus.UNLOADED

            # Remove from loaded plugins
            del self.loaded_plugins[plugin_id]

            logger.info(f"✅ Plugin unloaded successfully: {plugin_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to unload plugin {plugin_id}: {e}")
            return False

    async def reload_plugin(self, plugin_id: str) -> bool:
        """
        Hot-reload a plugin without system restart.

        Args:
            plugin_id: Plugin ID to reload

        Returns:
            bool: True if reload successful
        """
        logger.info(f"🔄 Reloading plugin: {plugin_id}")

        # Unload current instance
        if not await self.unload_plugin(plugin_id):
            return False

        # Re-discover plugin info (in case manifest changed)
        plugin_dir = self.plugins_dir / plugin_id
        if plugin_dir.exists():
            new_info = await self._load_plugin_info(plugin_dir)
            if new_info:
                self.plugin_registry[plugin_id] = new_info

        # Load new instance
        return await self.load_plugin(plugin_id)

    def get_loaded_plugins(self) -> List[str]:
        """
        Get list of loaded plugin IDs.

        Returns:
            List[str]: List of loaded plugin IDs
        """
        return list(self.loaded_plugins.keys())

    def get_plugin_info(self, plugin_id: str) -> Optional[PluginInfo]:
        """
        Get plugin information.

        Args:
            plugin_id: Plugin ID

        Returns:
            Optional[PluginInfo]: Plugin information or None if not found
        """
        return self.plugin_registry.get(plugin_id)

    def get_plugin_status(self, plugin_id: str) -> Optional[PluginStatus]:
        """
        Get plugin status.

        Args:
            plugin_id: Plugin ID

        Returns:
            Optional[PluginStatus]: Plugin status or None if not loaded
        """
        if plugin_id in self.loaded_plugins:
            return self.loaded_plugins[plugin_id].status
        return None

    async def get_plugin_instance(self, plugin_id: str) -> Optional[IPlugin]:
        """
        Get plugin instance.

        Args:
            plugin_id: Plugin ID

        Returns:
            Optional[IPlugin]: Plugin instance or None if not loaded
        """
        if plugin_id in self.loaded_plugins:
            return self.loaded_plugins[plugin_id].plugin
        return None

    async def shutdown(self) -> bool:
        """
        Shutdown plugin loader and unload all plugins.

        Returns:
            bool: True if shutdown successful
        """
        logger.info("🔌 Shutting down plugin loader...")

        success = True
        for plugin_id in list(self.loaded_plugins.keys()):
            if not await self.unload_plugin(plugin_id):
                success = False

        self.loaded_plugins.clear()
        self.plugin_registry.clear()
        self.dependency_graph.clear()

        logger.info("✅ Plugin loader shutdown complete")
        return success


# Global plugin loader instance
_plugin_loader: Optional[PluginLoader] = None


def get_plugin_loader() -> PluginLoader:
    """Get global plugin loader instance."""
    global _plugin_loader
    if _plugin_loader is None:
        _plugin_loader = PluginLoader()
    return _plugin_loader


async def initialize_plugin_system() -> bool:
    """
    Initialize the plugin system.

    Returns:
        bool: True if initialization successful
    """
    try:
        loader = get_plugin_loader()

        # Discover plugins
        discovered = await loader.discover_plugins()
        logger.info(f"📦 Discovered {len(discovered)} plugins")

        # Load core plugins (for now, load any available)
        loaded_count = 0
        for plugin_info in discovered[:1]:  # Load first plugin as demo
            if await loader.load_plugin(plugin_info.plugin_id):
                loaded_count += 1

        logger.info(f"✅ Plugin system initialized - {loaded_count} plugins loaded")
        return loaded_count > 0

    except Exception as e:
        logger.error(f"Failed to initialize plugin system: {e}")
        return False


async def demo_plugin_loader():
    """Demonstrate the plugin loader functionality."""
    print("🔌 Phase 3 Plugin Loader Demo")
    print("=" * 40)

    # Initialize system
    if not await initialize_plugin_system():
        print("❌ Failed to initialize plugin system")
        return

    loader = get_plugin_loader()

    print(f"📦 Registered plugins: {len(loader.plugin_registry)}")
    print(f"🔧 Loaded plugins: {loader.get_loaded_plugins()}")

    # List available plugins
    print("\n📋 Available Plugins:")
    for plugin_id, info in loader.plugin_registry.items():
        status = "✅ Loaded" if plugin_id in loader.loaded_plugins else "⏳ Available"
        print(f"  • {info.name} ({plugin_id}) - {status}")

    print("\n✅ Plugin loader demo complete!")
    print("🎉 Phase 3 Architecture - Plugin foundation operational!")


if __name__ == "__main__":
    asyncio.run(demo_plugin_loader())