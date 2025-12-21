"""
Plugin Manager
==============

Manages loading, registration, and execution of trading robot plugins.
"""

import importlib
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from loguru import logger

from .plugin_base import PluginBase
from .plugin_metadata import PluginMetadata


class PluginManager:
    """Manages trading robot plugins."""

    def __init__(self, plugins_directory: str = "plugins/robots"):
        """Initialize plugin manager."""
        self.plugins_directory = Path(plugins_directory)
        self.plugins: Dict[str, PluginBase] = {}
        self.metadata_cache: Dict[str, PluginMetadata] = {}
        self.plugins_directory.mkdir(parents=True, exist_ok=True)
        self.performance_tracker = None  # Will be set if performance tracking is available

    def load_plugin(self, plugin_id: str, parameters: Dict[str, Any] = None) -> Optional[PluginBase]:
        """Load a plugin by ID."""
        try:
            # Try to load from cache first
            if plugin_id in self.plugins:
                logger.info(f"Plugin {plugin_id} already loaded")
                return self.plugins[plugin_id]

            # Load metadata
            metadata = self.load_metadata(plugin_id)
            if not metadata:
                logger.error(f"Failed to load metadata for plugin {plugin_id}")
                return None

            # Import plugin module
            module_path = f"plugins.robots.{plugin_id}"
            try:
                module = importlib.import_module(module_path)
            except ImportError:
                logger.error(f"Failed to import plugin module: {module_path}")
                return None

            # Get plugin class (convention: Plugin class name matches plugin_id in PascalCase)
            class_name = "".join(word.capitalize()
                                 for word in plugin_id.split("_"))
            plugin_class = getattr(module, class_name, None)

            if not plugin_class:
                logger.error(
                    f"Plugin class {class_name} not found in {module_path}")
                return None

            # Instantiate plugin
            plugin = plugin_class(
                metadata, parameters or metadata.default_parameters)
            self.plugins[plugin_id] = plugin
            logger.info(f"✅ Loaded plugin: {plugin_id} ({metadata.name})")
            
            # Capture plugin load metrics for performance tracking (if available)
            if self.performance_tracker:
                try:
                    # Get user_id from context (default to 'system' if not available)
                    user_id = getattr(self, 'user_id', 'system')
                    
                    self.performance_tracker.collector.capture_plugin_metrics(
                        user_id=user_id,
                        plugin_id=plugin_id,
                        plugin_metrics={
                            "action": "plugin_loaded",
                            "plugin_name": metadata.name,
                            "plugin_version": metadata.version,
                            "is_for_sale": metadata.is_for_sale,
                            "price": metadata.price,
                            "timestamp": __import__('datetime').datetime.now().isoformat()
                        }
                    )
                except Exception as e:
                    logger.warning(f"⚠️ Failed to capture plugin load metrics: {e}")

            return plugin

        except Exception as e:
            logger.error(f"Error loading plugin {plugin_id}: {e}")
            return None

    def load_metadata(self, plugin_id: str) -> Optional[PluginMetadata]:
        """Load plugin metadata."""
        if plugin_id in self.metadata_cache:
            return self.metadata_cache[plugin_id]

        metadata_file = self.plugins_directory / plugin_id / "metadata.json"
        if not metadata_file.exists():
            logger.error(f"Metadata file not found: {metadata_file}")
            return None

        try:
            with open(metadata_file, "r") as f:
                data = json.load(f)
            metadata = PluginMetadata.from_dict(data)
            self.metadata_cache[plugin_id] = metadata
            return metadata

        except Exception as e:
            logger.error(f"Error loading metadata for {plugin_id}: {e}")
            return None

    def list_plugins(self) -> List[PluginMetadata]:
        """List all available plugins."""
        plugins = []
        if not self.plugins_directory.exists():
            return plugins

        for plugin_dir in self.plugins_directory.iterdir():
            if plugin_dir.is_dir():
                metadata_file = plugin_dir / "metadata.json"
                if metadata_file.exists():
                    try:
                        metadata = self.load_metadata(plugin_dir.name)
                        if metadata:
                            plugins.append(metadata)
                    except Exception as e:
                        logger.warning(
                            f"Error loading plugin {plugin_dir.name}: {e}")

        return plugins

    def get_plugin(self, plugin_id: str) -> Optional[PluginBase]:
        """Get a loaded plugin."""
        return self.plugins.get(plugin_id)

    def unload_plugin(self, plugin_id: str):
        """Unload a plugin."""
        if plugin_id in self.plugins:
            del self.plugins[plugin_id]
            logger.info(f"Unloaded plugin: {plugin_id}")

    def get_plugins_for_sale(self) -> List[PluginMetadata]:
        """Get all plugins available for sale."""
        all_plugins = self.list_plugins()
        return [p for p in all_plugins if p.is_for_sale]
    
    def set_performance_tracker(self, performance_tracker):
        """
        Set performance tracker for plugin-specific metrics.
        
        Args:
            performance_tracker: PerformanceTracker instance
        """
        self.performance_tracker = performance_tracker
        logger.info("✅ Performance tracker set for plugin manager")
    
    def capture_plugin_performance(self, plugin_id: str, user_id: str = 'system', metrics: Dict[str, Any] = None):
        """
        Capture plugin-specific performance metrics.
        
        Args:
            plugin_id: Plugin identifier
            user_id: User identifier (default: 'system')
            metrics: Plugin-specific metrics dictionary
        """
        if not self.performance_tracker:
            return False
        
        try:
            plugin_metrics = metrics or {}
            plugin_metrics["timestamp"] = __import__('datetime').datetime.now().isoformat()
            
            return self.performance_tracker.collector.capture_plugin_metrics(
                user_id=user_id,
                plugin_id=plugin_id,
                plugin_metrics=plugin_metrics
            )
        except Exception as e:
            logger.warning(f"⚠️ Failed to capture plugin performance: {e}")
            return False
    
    def get_plugin_performance_summary(self, plugin_id: str, user_id: str = 'system') -> Dict[str, Any]:
        """
        Get performance summary for a plugin.
        
        Args:
            plugin_id: Plugin identifier
            user_id: User identifier (default: 'system')
            
        Returns:
            Performance summary dictionary
        """
        if not self.performance_tracker:
            return {}
        
        try:
            plugin = self.get_plugin(plugin_id)
            if plugin and hasattr(plugin, 'get_performance_summary'):
                return plugin.get_performance_summary()
            
            # Fallback: get from performance tracker
            return self.performance_tracker.get_performance_metrics(
                user_id=user_id,
                plugin_id=plugin_id,
                metric_type="all_time"
            )
        except Exception as e:
            logger.warning(f"⚠️ Failed to get plugin performance summary: {e}")
            return {}

