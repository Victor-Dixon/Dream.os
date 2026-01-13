#!/usr/bin/env python3
"""
🔌 Plugin Interface Definition - Phase 3 Architecture Specification
===================================================================

Comprehensive plugin interfaces implementing the Phase 3 Plugin Architecture Specification.
Includes IPlugin, IMessageHandler, and supporting data structures.

<!-- SSOT Domain: plugins -->
"""

from __future__ import annotations

import abc
from typing import Any, Dict, List, Optional, Protocol
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


# ===== DATA STRUCTURES =====

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
    SUSPENDED = "suspended"
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
    dependencies: List[str] = field(default_factory=list)
    permissions: List[str] = field(default_factory=list)
    entry_point: str = ""
    config_schema: Dict[str, Any] = field(default_factory=dict)
    min_core_version: str = "2.0.0"
    max_core_version: Optional[str] = None
    homepage: Optional[str] = None
    repository: Optional[str] = None
    license: str = "MIT"
    tags: List[str] = field(default_factory=list)


@dataclass
class PluginContext:
    """Runtime context provided to plugins."""
    plugin_id: str
    config: Dict[str, Any] = field(default_factory=dict)
    logger: Any = None  # Logger instance
    event_bus: Any = None  # Event bus for inter-plugin communication
    resource_limits: Dict[str, Any] = field(default_factory=dict)
    permissions: List[str] = field(default_factory=list)
    plugin_registry: Any = None  # Plugin registry access
    messaging_service: Any = None  # Messaging service access


@dataclass
class PluginConfig:
    """Plugin configuration container."""
    plugin_id: str
    version: str
    enabled: bool = True
    settings: Dict[str, Any] = field(default_factory=dict)
    environment: Dict[str, str] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate configuration against schema."""
        # Basic validation - extend as needed
        return isinstance(self.plugin_id, str) and len(self.plugin_id) > 0

    def merge(self, overrides: Dict[str, Any]) -> 'PluginConfig':
        """Merge configuration overrides."""
        for key, value in overrides.items():
            if key in self.settings:
                self.settings[key] = value
        return self


@dataclass
class Message:
    """Message structure for plugin communication."""
    message_id: str
    sender: str
    recipient: str
    content: str
    message_type: str = "text"
    priority: str = "regular"
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class MessageResponse:
    """Response structure for message handling."""
    response_id: str
    original_message_id: str
    content: Any
    status: str = "success"
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class CommandDefinition:
    """Command definition for CLI plugins."""
    name: str
    description: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    examples: List[str] = field(default_factory=list)


@dataclass
class CommandResult:
    """Result structure for command execution."""
    command: str
    success: bool
    output: Any = None
    error: Optional[str] = None
    execution_time: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DataSourceDefinition:
    """Data source definition for data provider plugins."""
    name: str
    description: str
    schema: Dict[str, Any]
    capabilities: List[str] = field(default_factory=list)


@dataclass
class DataQuery:
    """Query structure for data retrieval."""
    source_id: str
    query_type: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    filters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DataResult:
    """Result structure for data queries."""
    query_id: str
    success: bool
    data: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MetricDefinition:
    """Metric definition for analytics plugins."""
    name: str
    description: str
    data_type: str
    unit: Optional[str] = None
    aggregation: str = "sum"


@dataclass
class MetricsData:
    """Container for metrics data."""
    metrics: Dict[str, Any] = field(default_factory=dict)
    time_range: Optional[Dict[str, datetime]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TimeRange:
    """Time range specification."""
    start: datetime
    end: datetime
    granularity: str = "hour"


@dataclass
class Report:
    """Analytics report structure."""
    report_id: str
    title: str
    format: str
    content: Any
    generated_at: datetime = field(default_factory=datetime.now)
    parameters: Dict[str, Any] = field(default_factory=dict)


class PluginEvent:
    """Base class for plugin events."""
    def __init__(self, event_type: str, source_plugin: str, data: Dict[str, Any] = None):
        self.event_type = event_type
        self.source_plugin = source_plugin
        self.data = data or {}
        self.timestamp = datetime.now()


# ===== CORE INTERFACES =====

class IPlugin(abc.ABC):
    """Core plugin interface that all plugins must implement."""

    @property
    @abc.abstractmethod
    def plugin_id(self) -> str:
        """Unique plugin identifier."""
        pass

    @property
    @abc.abstractmethod
    def version(self) -> str:
        """Plugin version following semantic versioning."""
        pass

    @abc.abstractmethod
    async def initialize(self, context: PluginContext) -> bool:
        """Initialize plugin with context."""
        pass

    @abc.abstractmethod
    async def activate(self) -> bool:
        """Activate plugin for operation."""
        pass

    @abc.abstractmethod
    async def deactivate(self) -> bool:
        """Deactivate plugin gracefully."""
        pass

    @abc.abstractmethod
    async def get_config_schema(self) -> Dict[str, Any]:
        """Return plugin configuration schema."""
        pass

    @abc.abstractmethod
    async def validate_config(self, config: PluginConfig) -> bool:
        """Validate plugin configuration."""
        pass


class IMessageHandler(IPlugin):
    """Interface for plugins that handle messages."""

    @abc.abstractmethod
    async def can_handle(self, message: Message) -> float:
        """Return confidence score (0.0-1.0) for handling message."""
        pass

    @abc.abstractmethod
    async def handle_message(self, message: Message, context: PluginContext) -> MessageResponse:
        """Process and respond to message."""
        pass

    @abc.abstractmethod
    async def get_supported_message_types(self) -> List[str]:
        """Return list of supported message types."""
        pass


class ICommandHandler(IPlugin):
    """Interface for plugins that provide CLI commands."""

    @abc.abstractmethod
    async def get_commands(self) -> Dict[str, CommandDefinition]:
        """Return dictionary of command definitions."""
        pass

    @abc.abstractmethod
    async def execute_command(self, command: str, args: List[str], context: PluginContext) -> CommandResult:
        """Execute plugin command."""
        pass


class IDataProvider(IPlugin):
    """Interface for plugins that provide data sources."""

    @abc.abstractmethod
    async def get_data_sources(self) -> List[DataSourceDefinition]:
        """Return available data sources."""
        pass

    @abc.abstractmethod
    async def query_data(self, source_id: str, query: DataQuery) -> DataResult:
        """Query data from specified source."""
        pass


class IAnalyticsProvider(IPlugin):
    """Interface for plugins that provide analytics capabilities."""

    @abc.abstractmethod
    async def get_metrics(self) -> List[MetricDefinition]:
        """Return available metrics."""
        pass

    @abc.abstractmethod
    async def collect_metrics(self, time_range: TimeRange) -> MetricsData:
        """Collect metrics for specified time range."""
        pass

    @abc.abstractmethod
    async def generate_report(self, metrics: MetricsData, format: str) -> Report:
        """Generate analytics report."""
        pass


# ===== LEGACY COMPATIBILITY =====

class PluginInterface(IPlugin):
    """
    Legacy plugin interface for backward compatibility.
    New plugins should implement specific interfaces above.
    """

    @abc.abstractmethod
    def initialize(self, config: Dict[str, Any], context: PluginContext) -> bool:
        """Initialize the plugin (legacy sync method)."""
        pass

    @abc.abstractmethod
    def execute(self, input_data: Any) -> Any:
        """Execute plugin functionality."""
        pass

    @abc.abstractmethod
    def cleanup(self) -> bool:
        """Clean up plugin resources."""
        pass

    @abc.abstractmethod
    def get_status(self) -> PluginStatus:
        """Get current plugin status."""
        pass

    @abc.abstractmethod
    def handle_event(self, event: PluginEvent) -> None:
        """Handle incoming plugin events."""
        pass

    @property
    @abc.abstractmethod
    def plugin_info(self) -> PluginInfo:
        """Get plugin metadata."""
        pass