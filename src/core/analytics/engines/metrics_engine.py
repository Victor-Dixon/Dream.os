#!/usr/bin/env python3
"""
Metrics Engine - KISS Compliant
===============================

<!-- SSOT Domain: analytics -->

Simple metrics collection and monitoring.

Author: Agent-5 - Business Intelligence Specialist
License: MIT
"""

import logging
import time
from collections import defaultdict, deque
from datetime import datetime
from typing import Any, Optional

logger = logging.getLogger(__name__)

# Optional persistence integration
try:
    from src.repositories.metrics_repository import MetricsRepository
    METRICS_REPOSITORY_AVAILABLE = True
except ImportError:
    METRICS_REPOSITORY_AVAILABLE = False
    MetricsRepository = None


class MetricsEngine:
    """Simple metrics collection and monitoring engine."""

    def __init__(self, config=None, metrics_repository: Optional[MetricsRepository] = None):
        """
        Initialize metrics engine.
        
        Args:
            config: Optional configuration dictionary
            metrics_repository: Optional MetricsRepository for persistence
        """
        self.config = config or {}
        self.logger = logger

        # Simple metrics storage
        self.metrics = defaultdict(int)
        self.performance_history = deque(maxlen=100)
        self.error_history = deque(maxlen=50)
        self.start_time = time.time()
        
        # Optional persistence
        self.metrics_repository = metrics_repository
        if metrics_repository is None and METRICS_REPOSITORY_AVAILABLE:
            try:
                self.metrics_repository = MetricsRepository()
                self.logger.debug("MetricsRepository initialized for persistence")
            except Exception as e:
                self.logger.warning(f"Could not initialize MetricsRepository: {e}")
                self.metrics_repository = None

    def record_metric(self, name: str, value: Any) -> None:
        """Record a metric value."""
        try:
            if isinstance(value, (int, float)):
                self.metrics[name] = value
            else:
                self.metrics[f"{name}_count"] += 1
            self.logger.debug(f"Recorded metric: {name} = {value}")
        except Exception as e:
            self.logger.error(f"Error recording metric: {e}")

    def increment_metric(self, name: str, amount: int = 1) -> None:
        """Increment a metric value."""
        try:
            self.metrics[name] += amount
            self.logger.debug(f"Incremented metric: {name} by {amount}")
        except Exception as e:
            self.logger.error(f"Error incrementing metric: {e}")

    def get_metric(self, name: str) -> Any:
        """Get a metric value."""
        return self.metrics.get(name, 0)

    def get_all_metrics(self) -> dict[str, Any]:
        """Get all metrics."""
        return dict(self.metrics)

    def record_performance(self, operation: str, duration: float) -> None:
        """Record performance data."""
        try:
            self.performance_history.append(
                {
                    "operation": operation,
                    "duration": duration,
                    "timestamp": datetime.now().isoformat(),
                }
            )
            self.logger.debug(f"Recorded performance: {operation} took {duration}s")
        except Exception as e:
            self.logger.error(f"Error recording performance: {e}")

    def record_error(self, error_type: str, message: str) -> None:
        """Record error data."""
        try:
            self.error_history.append(
                {
                    "error_type": error_type,
                    "message": message,
                    "timestamp": datetime.now().isoformat(),
                }
            )
            self.logger.debug(f"Recorded error: {error_type} - {message}")
        except Exception as e:
            self.logger.error(f"Error recording error: {e}")

    def get_performance_summary(self) -> dict[str, Any]:
        """Get performance summary."""
        try:
            if not self.performance_history:
                return {"message": "No performance data available"}

            durations = [p["duration"] for p in self.performance_history]
            avg_duration = sum(durations) / len(durations)
            max_duration = max(durations)
            min_duration = min(durations)

            return {
                "total_operations": len(self.performance_history),
                "avg_duration": round(avg_duration, 3),
                "max_duration": round(max_duration, 3),
                "min_duration": round(min_duration, 3),
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            self.logger.error(f"Error getting performance summary: {e}")
            return {"error": str(e)}

    def get_error_summary(self) -> dict[str, Any]:
        """Get error summary."""
        try:
            if not self.error_history:
                return {"message": "No error data available"}

            error_types = defaultdict(int)
            for error in self.error_history:
                error_types[error["error_type"]] += 1

            return {
                "total_errors": len(self.error_history),
                "error_types": dict(error_types),
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            self.logger.error(f"Error getting error summary: {e}")
            return {"error": str(e)}

    def clear_metrics(self) -> None:
        """Clear all metrics."""
        self.metrics.clear()
        self.performance_history.clear()
        self.error_history.clear()
        self.logger.info("All metrics cleared")

    def get_status(self) -> dict[str, Any]:
        """Get engine status."""
        uptime = time.time() - self.start_time
        return {
            "active": True,
            "uptime": round(uptime, 2),
            "metrics_count": len(self.metrics),
            "performance_records": len(self.performance_history),
            "error_records": len(self.error_history),
            "persistence_enabled": self.metrics_repository is not None,
            "timestamp": datetime.now().isoformat(),
        }
    
    def save_snapshot(self, source: str = "metrics_engine") -> bool:
        """
        Save current metrics snapshot to repository.
        
        Args:
            source: Source identifier for the snapshot
            
        Returns:
            True if saved successfully, False otherwise
        """
        if not self.metrics_repository:
            self.logger.debug("MetricsRepository not available, skipping snapshot")
            return False
        
        try:
            all_metrics = self.get_all_metrics()
            success = self.metrics_repository.save_metrics_snapshot(all_metrics, source=source)
            if success:
                self.logger.debug(f"Metrics snapshot saved: {source} ({len(all_metrics)} metrics)")
            return success
        except Exception as e:
            self.logger.error(f"Error saving metrics snapshot: {e}")
            return False
    
    def get_metrics_history(self, source: Optional[str] = None, limit: Optional[int] = None) -> list[dict[str, Any]]:
        """
        Get metrics history from repository.
        
        Args:
            source: Optional source filter
            limit: Optional limit on number of snapshots
            
        Returns:
            List of metrics snapshot dictionaries
        """
        if not self.metrics_repository:
            return []
        
        try:
            return self.metrics_repository.get_metrics_history(source=source, limit=limit)
        except Exception as e:
            self.logger.error(f"Error getting metrics history: {e}")
            return []
    
    def get_metrics_trend(self, metric_name: str, source: Optional[str] = None, limit: int = 100) -> list[float]:
        """
        Get trend data for a specific metric over time.
        
        Args:
            metric_name: Name of metric to track
            source: Optional source filter
            limit: Maximum snapshots to analyze
            
        Returns:
            List of metric values over time
        """
        if not self.metrics_repository:
            return []
        
        try:
            return self.metrics_repository.get_metrics_trend(metric_name, source=source, limit=limit)
        except Exception as e:
            self.logger.error(f"Error getting metrics trend: {e}")
            return []


# Simple factory function
def create_metrics_engine(config=None) -> MetricsEngine:
    """Create metrics engine."""
    return MetricsEngine(config)


__all__ = ["MetricsEngine", "create_metrics_engine"]
