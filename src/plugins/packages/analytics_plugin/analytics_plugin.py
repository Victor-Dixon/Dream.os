#!/usr/bin/env python3
"""
📊 Analytics Plugin Implementation
=================================

Real-time ecosystem analytics for Agent Cellphone V2.
Phase 3 MVP Plugin #1

<!-- SSOT Domain: plugins -->
"""

from __future__ import annotations

import logging
import time
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field

from src.plugins.plugin_interface import (
    PluginInterface,
    PluginInfo,
    PluginCategory,
    PluginStatus,
    PluginContext,
    PluginEvent
)


logger = logging.getLogger(__name__)


@dataclass
class AnalyticsMetrics:
    """Analytics metrics data structure."""
    total_requests: int = 0
    active_users: int = 0
    response_time_avg: float = 0.0
    error_rate: float = 0.0
    uptime_percentage: float = 100.0
    memory_usage_mb: float = 0.0
    cpu_usage_percent: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)


class AnalyticsPlugin(PluginInterface):
    """
    Analytics Plugin - Phase 3 MVP

    Provides real-time ecosystem analytics including:
    - Request/response metrics
    - User activity tracking
    - Performance monitoring
    - Error rate analysis
    """

    def __init__(self):
        self._status = PluginStatus.UNLOADED
        self._context: Optional[PluginContext] = None
        self._config: Dict[str, Any] = {}
        self._metrics: List[AnalyticsMetrics] = []
        self._start_time: Optional[float] = None
        self._event_handlers: Dict[str, callable] = {}

    @property
    def plugin_info(self) -> PluginInfo:
        """Plugin metadata."""
        return PluginInfo(
            plugin_id="analytics_plugin",
            name="Ecosystem Analytics Plugin",
            version="1.0.0",
            author="Agent-6 (Phase 3 Lead)",
            description="Real-time ecosystem analytics and metrics collection",
            category=PluginCategory.ANALYTICS,
            dependencies=[],  # No dependencies for MVP
            permissions=[
                "file_system_read",  # For log analysis
                "system_info"        # For performance metrics
            ],
            entry_point="analytics_plugin:AnalyticsPlugin",
            config_schema={
                "collection_interval": {
                    "type": "integer",
                    "default": 60,
                    "description": "Metrics collection interval in seconds"
                },
                "retention_days": {
                    "type": "integer",
                    "default": 7,
                    "description": "How long to retain metrics data"
                },
                "enable_real_time": {
                    "type": "boolean",
                    "default": True,
                    "description": "Enable real-time metrics collection"
                }
            },
            min_core_version="2.0.0"
        )

    def initialize(self, config: dict, context: PluginContext) -> bool:
        """
        Initialize the analytics plugin.

        Args:
            config: Plugin configuration
            context: Runtime context

        Returns:
            bool: True if initialization successful
        """
        try:
            self._status = PluginStatus.INITIALIZING
            self._context = context
            self._config = config

            # Set up event handlers
            self._setup_event_handlers()

            # Initialize metrics storage
            self._metrics = []

            # Record start time for uptime calculation
            self._start_time = time.time()

            # Start metrics collection if enabled
            if self._config.get("enable_real_time", True):
                self._start_metrics_collection()

            self._status = PluginStatus.ACTIVE
            logger.info("Analytics plugin initialized successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize analytics plugin: {e}")
            self._status = PluginStatus.ERROR
            return False

    def execute(self, input_data: Any) -> Any:
        """
        Execute analytics functionality.

        Args:
            input_data: Input data for analysis

        Returns:
            Any: Analytics results
        """
        if self._status != PluginStatus.ACTIVE:
            return {"error": "Plugin not active", "status": self._status.value}

        try:
            command = input_data.get("command", "get_metrics")

            if command == "get_metrics":
                return self._get_current_metrics()
            elif command == "get_trends":
                return self._get_trends_analysis()
            elif command == "get_health":
                return self._get_system_health()
            else:
                return {"error": f"Unknown command: {command}"}

        except Exception as e:
            logger.error(f"Analytics execution error: {e}")
            return {"error": str(e)}

    def cleanup(self) -> bool:
        """
        Clean up plugin resources.

        Returns:
            bool: True if cleanup successful
        """
        try:
            self._status = PluginStatus.UNLOADING

            # Stop metrics collection
            # (In a real implementation, this would stop background threads/timers)

            # Clear metrics data
            self._metrics.clear()

            # Clean up event handlers
            self._event_handlers.clear()

            self._status = PluginStatus.UNLOADED
            logger.info("Analytics plugin cleaned up successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to cleanup analytics plugin: {e}")
            return False

    def get_status(self) -> PluginStatus:
        """Get current plugin status."""
        return self._status

    def handle_event(self, event: PluginEvent) -> None:
        """
        Handle incoming plugin events.

        Args:
            event: Plugin event to process
        """
        if event.event_type in self._event_handlers:
            try:
                self._event_handlers[event.event_type](event)
            except Exception as e:
                logger.error(f"Error handling event {event.event_type}: {e}")

    def _setup_event_handlers(self) -> None:
        """Set up event handlers for analytics collection."""
        self._event_handlers = {
            "request_processed": self._handle_request_event,
            "user_activity": self._handle_user_activity,
            "error_occurred": self._handle_error_event,
            "system_metrics": self._handle_system_metrics
        }

    def _start_metrics_collection(self) -> None:
        """Start background metrics collection."""
        # In MVP, we'll collect metrics on demand
        # Real implementation would use threading.Timer or asyncio
        logger.info("Metrics collection enabled (on-demand)")

    def _get_current_metrics(self) -> Dict[str, Any]:
        """Get current analytics metrics."""
        if not self._metrics:
            # Return default metrics if no data collected yet
            return {
                "status": "initializing",
                "message": "Metrics collection starting...",
                "timestamp": datetime.now().isoformat()
            }

        latest = self._metrics[-1]
        return {
            "total_requests": latest.total_requests,
            "active_users": latest.active_users,
            "response_time_avg": latest.response_time_avg,
            "error_rate": latest.error_rate,
            "uptime_percentage": self._calculate_uptime(),
            "memory_usage_mb": latest.memory_usage_mb,
            "cpu_usage_percent": latest.cpu_usage_percent,
            "timestamp": latest.timestamp.isoformat()
        }

    def _get_trends_analysis(self) -> Dict[str, Any]:
        """Analyze metrics trends over time."""
        if len(self._metrics) < 2:
            return {"message": "Insufficient data for trend analysis"}

        # Simple trend analysis
        recent = self._metrics[-1]
        previous = self._metrics[-2] if len(self._metrics) > 1 else recent

        trends = {
            "requests_trend": self._calculate_trend(recent.total_requests, previous.total_requests),
            "users_trend": self._calculate_trend(recent.active_users, previous.active_users),
            "response_time_trend": self._calculate_trend(previous.response_time_avg, recent.response_time_avg),  # Lower is better
            "error_rate_trend": self._calculate_trend(recent.error_rate, previous.error_rate)  # Lower is better
        }

        return {
            "trends": trends,
            "period": "last_collection_interval",
            "timestamp": datetime.now().isoformat()
        }

    def _get_system_health(self) -> Dict[str, Any]:
        """Get overall system health assessment."""
        metrics = self._get_current_metrics()

        # Simple health scoring
        health_score = 100
        issues = []

        if metrics.get("error_rate", 0) > 5.0:
            health_score -= 20
            issues.append("High error rate detected")

        if metrics.get("response_time_avg", 0) > 2.0:
            health_score -= 15
            issues.append("Slow response times")

        if metrics.get("uptime_percentage", 100) < 99.5:
            health_score -= 10
            issues.append("Uptime below threshold")

        health_status = "healthy" if health_score >= 80 else "warning" if health_score >= 60 else "critical"

        return {
            "health_score": health_score,
            "status": health_status,
            "issues": issues,
            "timestamp": datetime.now().isoformat()
        }

    def _calculate_uptime(self) -> float:
        """Calculate system uptime percentage."""
        if not self._start_time:
            return 100.0

        uptime_seconds = time.time() - self._start_time
        # Assume 24/7 operation for MVP
        expected_uptime = 24 * 60 * 60  # 24 hours in seconds
        return min(100.0, (uptime_seconds / expected_uptime) * 100)

    def _calculate_trend(self, current: float, previous: float) -> str:
        """Calculate trend direction."""
        if previous == 0:
            return "stable"

        change = ((current - previous) / previous) * 100

        if change > 5:
            return "increasing"
        elif change < -5:
            return "decreasing"
        else:
            return "stable"

    def _handle_request_event(self, event: PluginEvent) -> None:
        """Handle request processing events."""
        if not self._metrics:
            self._metrics.append(AnalyticsMetrics())

        current = self._metrics[-1]
        current.total_requests += 1

        # Update response time if provided
        if "response_time" in event.data:
            # Simple moving average
            current.response_time_avg = (
                current.response_time_avg + event.data["response_time"]
            ) / 2

    def _handle_user_activity(self, event: PluginEvent) -> None:
        """Handle user activity events."""
        if not self._metrics:
            self._metrics.append(AnalyticsMetrics())

        # Update active users (simplified)
        self._metrics[-1].active_users = max(
            self._metrics[-1].active_users,
            event.data.get("active_users", 1)
        )

    def _handle_error_event(self, event: PluginEvent) -> None:
        """Handle error events."""
        if not self._metrics:
            self._metrics.append(AnalyticsMetrics())

        # Increment error count (would need total requests for rate calculation)
        # For MVP, just track that errors occurred
        self._metrics[-1].error_rate += 1  # Simplified

    def _handle_system_metrics(self, event: PluginEvent) -> None:
        """Handle system performance metrics."""
        if not self._metrics:
            self._metrics.append(AnalyticsMetrics())

        current = self._metrics[-1]

        # Update system metrics
        if "memory_usage_mb" in event.data:
            current.memory_usage_mb = event.data["memory_usage_mb"]

        if "cpu_usage_percent" in event.data:
            current.cpu_usage_percent = event.data["cpu_usage_percent"]