"""
Trading Robot Plugin System
===========================

Plugin system for loading and managing trading robot strategies.
Supports dynamic loading, performance tracking, and marketplace integration.

Author: Agent-1 (Integration & Core Systems Specialist)
Created: 2025-12-15
"""

from .plugin_manager import PluginManager
from .plugin_base import PluginBase
from .plugin_metadata import PluginMetadata

__all__ = ["PluginManager", "PluginBase", "PluginMetadata"]

