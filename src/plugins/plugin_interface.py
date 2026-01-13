#!/usr/bin/env python3
"""
🔌 Plugin Interface Definition
=============================

Abstract base classes and interfaces for plugin system.
Phase 3 MVP Implementation

<!-- SSOT Domain: plugins -->
"""

from __future__ import annotations

import abc
from typing import Any, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class PluginCategory(Enum):
    """Plugin categories for ecosystem organization."""
    ANALYTICS = "analytics"
    COLLABORATION = "collaboration"
    INTEGRATION = "integration"
    DOCUMENTATION = "documentation"
    AI_ENHANCEMENT = "ai_enhancement"
    WORKFLOW_AUTOMATION = "workflow_automation"
    SECURITY = "security"
    PERFORMANCE = "performance"
    CUSTOM = "custom"


class PluginStatus(Enum):
    """Plugin lifecycle status."""
    UNLOADED = "unloaded"
    LOADING = "loading"
    LOADED = "loaded"
    INITIALIZING = "initializing"
    ACTIVE = "active"
    ERROR = "error"
    UNLOADING = "unloading"


@dataclass
class PluginInfo:
    """Plugin metadata and configuration."""
    plugin_id: str
    name: str
    version: str
    author: str
    description: str
    category: PluginCategory
    dependencies: list[str]
    permissions: list[str]
    entry_point: str
    config_schema: dict
    min_core_version: str
    max_core_version: Optional[str] = None


@dataclass
class PluginContext:
    """Runtime context provided to plugins."""
    plugin_id: str
    config: dict
    logger: Any  # Logger instance
    event_bus: Any  # Event bus for inter-plugin communication
    resource_limits: dict
    permissions: list[str]


class PluginEvent:
    """Base class for plugin events."""
    def __init__(self, event_type: str, source_plugin: str, data: dict = None):
        self.event_type = event_type
        self.source_plugin = source_plugin
        self.data = data or {}
        self.timestamp = __import__('datetime').datetime.now()


class PluginInterface(abc.ABC):
    """
    Abstract base class for all plugins.

    This defines the contract that all plugins must implement.
    """

    @abc.abstractmethod
    def initialize(self, config: dict, context: PluginContext) -> bool:
        """
        Initialize the plugin.

        Args:
            config: Plugin-specific configuration
            context: Runtime context with services and limits

        Returns:
            bool: True if initialization successful
        """
        pass

    @abc.abstractmethod
    def execute(self, input_data: Any) -> Any:
        """
        Execute plugin functionality.

        Args:
            input_data: Input data for plugin processing

        Returns:
            Any: Plugin execution result
        """
        pass

    @abc.abstractmethod
    def cleanup(self) -> bool:
        """
        Clean up plugin resources.

        Returns:
            bool: True if cleanup successful
        """
        pass

    @abc.abstractmethod
    def get_status(self) -> PluginStatus:
        """
        Get current plugin status.

        Returns:
            PluginStatus: Current plugin state
        """
        pass

    @abc.abstractmethod
    def handle_event(self, event: PluginEvent) -> None:
        """
        Handle incoming plugin events.

        Args:
            event: Plugin event to process
        """
        pass

    @property
    @abc.abstractmethod
    def plugin_info(self) -> PluginInfo:
        """
        Get plugin metadata.

        Returns:
            PluginInfo: Plugin metadata and configuration
        """
        pass