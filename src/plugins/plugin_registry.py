#!/usr/bin/env python3
"""
🔌 Plugin Registry System
========================

Central registry for plugin discovery and management.
Phase 3 MVP Implementation

<!-- SSOT Domain: plugins -->
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import asdict

from .plugin_interface import PluginInfo, PluginCategory


logger = logging.getLogger(__name__)


class PluginRegistry:
    """
    Central registry for plugin discovery and management.

    Handles plugin registration, discovery, dependency resolution,
    and metadata management.
    """

    def __init__(self, plugins_dir: Path = None):
        """
        Initialize plugin registry.

        Args:
            plugins_dir: Directory containing plugin packages
        """
        self.plugins_dir = plugins_dir or Path(__file__).parent / "packages"
        self.plugins: Dict[str, PluginInfo] = {}
        self.categories: Dict[PluginCategory, List[str]] = {}
        self.dependencies: Dict[str, List[str]] = {}

        # Initialize category lists
        for category in PluginCategory:
            self.categories[category] = []

        logger.info("Plugin registry initialized")

    def discover_plugins(self) -> List[PluginInfo]:
        """
        Discover available plugins in the plugins directory.

        Returns:
            List[PluginInfo]: List of discovered plugin metadata
        """
        discovered_plugins = []

        if not self.plugins_dir.exists():
            logger.warning(f"Plugins directory not found: {self.plugins_dir}")
            return discovered_plugins

        for plugin_dir in self.plugins_dir.iterdir():
            if plugin_dir.is_dir() and not plugin_dir.name.startswith('_'):
                plugin_info = self._load_plugin_info(plugin_dir)
                if plugin_info:
                    discovered_plugins.append(plugin_info)
                    logger.info(f"Discovered plugin: {plugin_info.name} ({plugin_info.plugin_id})")

        return discovered_plugins

    def register_plugin(self, plugin_info: PluginInfo) -> bool:
        """
        Register a plugin with the registry.

        Args:
            plugin_info: Plugin metadata to register

        Returns:
            bool: True if registration successful
        """
        try:
            # Validate plugin info
            if not self._validate_plugin_info(plugin_info):
                logger.error(f"Plugin validation failed: {plugin_info.plugin_id}")
                return False

            # Register plugin
            self.plugins[plugin_info.plugin_id] = plugin_info
            self.categories[plugin_info.category].append(plugin_info.plugin_id)

            # Track dependencies
            self.dependencies[plugin_info.plugin_id] = plugin_info.dependencies

            logger.info(f"Registered plugin: {plugin_info.name} ({plugin_info.plugin_id})")
            return True

        except Exception as e:
            logger.error(f"Failed to register plugin {plugin_info.plugin_id}: {e}")
            return False

    def unregister_plugin(self, plugin_id: str) -> bool:
        """
        Unregister a plugin from the registry.

        Args:
            plugin_id: Plugin ID to unregister

        Returns:
            bool: True if unregistration successful
        """
        if plugin_id not in self.plugins:
            logger.warning(f"Plugin not registered: {plugin_id}")
            return False

        plugin_info = self.plugins[plugin_id]

        # Remove from category list
        if plugin_id in self.categories[plugin_info.category]:
            self.categories[plugin_info.category].remove(plugin_id)

        # Remove from registry
        del self.plugins[plugin_id]
        del self.dependencies[plugin_id]

        logger.info(f"Unregistered plugin: {plugin_id}")
        return True

    def get_plugin_info(self, plugin_id: str) -> Optional[PluginInfo]:
        """
        Get plugin metadata by ID.

        Args:
            plugin_id: Plugin ID to retrieve

        Returns:
            Optional[PluginInfo]: Plugin metadata or None if not found
        """
        return self.plugins.get(plugin_id)

    def get_plugins_by_category(self, category: PluginCategory) -> List[PluginInfo]:
        """
        Get all plugins in a specific category.

        Args:
            category: Plugin category to filter by

        Returns:
            List[PluginInfo]: List of plugins in the category
        """
        plugin_ids = self.categories.get(category, [])
        return [self.plugins[pid] for pid in plugin_ids if pid in self.plugins]

    def get_all_plugins(self) -> List[PluginInfo]:
        """
        Get all registered plugins.

        Returns:
            List[PluginInfo]: List of all plugin metadata
        """
        return list(self.plugins.values())

    def resolve_dependencies(self, plugin_id: str) -> List[str]:
        """
        Resolve plugin dependencies in load order.

        Args:
            plugin_id: Plugin ID to resolve dependencies for

        Returns:
            List[str]: Ordered list of plugin IDs including dependencies
        """
        if plugin_id not in self.dependencies:
            return [plugin_id]

        resolved = []
        visited = set()

        def resolve_recursive(pid: str):
            if pid in visited:
                return
            visited.add(pid)

            # Resolve dependencies first
            for dep in self.dependencies.get(pid, []):
                if dep in self.plugins:  # Only resolve known dependencies
                    resolve_recursive(dep)

            resolved.append(pid)

        resolve_recursive(plugin_id)
        return resolved

    def save_registry(self, filepath: Path) -> bool:
        """
        Save registry state to file.

        Args:
            filepath: Path to save registry data

        Returns:
            bool: True if save successful
        """
        try:
            registry_data = {
                "plugins": {pid: asdict(info) for pid, info in self.plugins.items()},
                "categories": {cat.value: pids for cat, pids in self.categories.items()},
                "dependencies": self.dependencies
            }

            with open(filepath, 'w') as f:
                json.dump(registry_data, f, indent=2, default=str)

            logger.info(f"Registry saved to: {filepath}")
            return True

        except Exception as e:
            logger.error(f"Failed to save registry: {e}")
            return False

    def load_registry(self, filepath: Path) -> bool:
        """
        Load registry state from file.

        Args:
            filepath: Path to load registry data from

        Returns:
            bool: True if load successful
        """
        try:
            with open(filepath, 'r') as f:
                registry_data = json.load(f)

            # Reconstruct PluginInfo objects
            self.plugins = {}
            for pid, info_dict in registry_data.get("plugins", {}).items():
                # Convert category string back to enum
                info_dict["category"] = PluginCategory(info_dict["category"])
                self.plugins[pid] = PluginInfo(**info_dict)

            # Reconstruct categories
            self.categories = {}
            for cat_str, pids in registry_data.get("categories", {}).items():
                self.categories[PluginCategory(cat_str)] = pids

            self.dependencies = registry_data.get("dependencies", {})

            logger.info(f"Registry loaded from: {filepath}")
            return True

        except Exception as e:
            logger.error(f"Failed to load registry: {e}")
            return False

    def _load_plugin_info(self, plugin_dir: Path) -> Optional[PluginInfo]:
        """
        Load plugin info from plugin directory.

        Args:
            plugin_dir: Plugin package directory

        Returns:
            Optional[PluginInfo]: Plugin metadata or None if invalid
        """
        plugin_json = plugin_dir / "plugin.json"

        if not plugin_json.exists():
            return None

        try:
            with open(plugin_json, 'r') as f:
                data = json.load(f)

            # Convert category string to enum
            if "category" in data:
                data["category"] = PluginCategory(data["category"])

            return PluginInfo(**data)

        except Exception as e:
            logger.error(f"Failed to load plugin info from {plugin_json}: {e}")
            return None

    def _validate_plugin_info(self, plugin_info: PluginInfo) -> bool:
        """
        Validate plugin metadata.

        Args:
            plugin_info: Plugin info to validate

        Returns:
            bool: True if valid
        """
        # Basic validation checks
        if not plugin_info.plugin_id or not plugin_info.name:
            return False

        if plugin_info.plugin_id in self.plugins:
            logger.warning(f"Plugin ID already registered: {plugin_info.plugin_id}")
            return False

        # Validate dependencies exist (if specified)
        for dep in plugin_info.dependencies:
            if dep not in self.plugins:
                logger.warning(f"Missing dependency for {plugin_info.plugin_id}: {dep}")
                # Don't fail validation for missing dependencies - they might be loaded later

        return True