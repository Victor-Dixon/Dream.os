#!/usr/bin/env python3
"""
Unified Tools Usage Metrics Tracker
===================================

Tracks usage metrics for unified tools (unified_validator, unified_analyzer, etc.)
Provides analytics for tool usage patterns, category distribution, and performance.

<!-- SSOT Domain: analytics -->

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-07
V2 Compliant: Yes (<300 lines)
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class UnifiedToolsMetricsTracker:
    """Tracks usage metrics for unified tools."""

    def __init__(self, data_dir: Optional[Path] = None):
        """
        Initialize metrics tracker.
        
        Args:
            data_dir: Directory for storing metrics data (defaults to systems/output_flywheel/data/)
        """
        if data_dir is None:
            project_root = Path(__file__).parent.parent.parent
            data_dir = project_root / "systems" / "output_flywheel" / "data"
        
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.metrics_file = self.data_dir / "unified_tools_metrics.json"
        self._load_metrics()

    def _load_metrics(self) -> Dict[str, Any]:
        """Load metrics from file."""
        if self.metrics_file.exists():
            try:
                with open(self.metrics_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading metrics: {e}")
                return self._default_metrics()
        return self._default_metrics()

    def _default_metrics(self) -> Dict[str, Any]:
        """Return default metrics structure."""
        return {
            "tool_usage": {},
            "category_usage": {},
            "performance_metrics": {},
            "error_rates": {},
            "last_updated": datetime.now().isoformat(),
        }

    def _save_metrics(self, metrics: Dict[str, Any]) -> None:
        """Save metrics to file."""
        try:
            metrics["last_updated"] = datetime.now().isoformat()
            with open(self.metrics_file, "w", encoding="utf-8") as f:
                json.dump(metrics, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving metrics: {e}")

    def track_tool_usage(
        self,
        tool_name: str,
        category: Optional[str] = None,
        success: bool = True,
        execution_time: Optional[float] = None,
    ) -> None:
        """
        Track tool usage.
        
        Args:
            tool_name: Name of the tool (e.g., "unified_validator", "unified_analyzer")
            category: Category used (e.g., "validation", "analysis")
            success: Whether execution was successful
            execution_time: Execution time in seconds
        """
        metrics = self._load_metrics()
        
        # Track tool usage
        if tool_name not in metrics["tool_usage"]:
            metrics["tool_usage"][tool_name] = {
                "total_calls": 0,
                "successful_calls": 0,
                "failed_calls": 0,
                "categories": {},
            }
        
        tool_metrics = metrics["tool_usage"][tool_name]
        tool_metrics["total_calls"] += 1
        
        if success:
            tool_metrics["successful_calls"] += 1
        else:
            tool_metrics["failed_calls"] += 1
        
        # Track category usage
        if category:
            if category not in tool_metrics["categories"]:
                tool_metrics["categories"][category] = 0
            tool_metrics["categories"][category] += 1
            
            # Global category tracking
            if category not in metrics["category_usage"]:
                metrics["category_usage"][category] = 0
            metrics["category_usage"][category] += 1
        
        # Track performance
        if execution_time is not None:
            if tool_name not in metrics["performance_metrics"]:
                metrics["performance_metrics"][tool_name] = {
                    "execution_times": [],
                    "avg_execution_time": 0.0,
                    "min_execution_time": float("inf"),
                    "max_execution_time": 0.0,
                }
            
            perf = metrics["performance_metrics"][tool_name]
            perf["execution_times"].append(execution_time)
            
            # Keep only last 100 execution times
            if len(perf["execution_times"]) > 100:
                perf["execution_times"] = perf["execution_times"][-100:]
            
            # Update statistics
            perf["avg_execution_time"] = sum(perf["execution_times"]) / len(perf["execution_times"])
            perf["min_execution_time"] = min(perf["execution_times"])
            perf["max_execution_time"] = max(perf["execution_times"])
        
        # Track error rates
        if tool_name not in metrics["error_rates"]:
            metrics["error_rates"][tool_name] = {
                "total": 0,
                "errors": 0,
                "rate": 0.0,
            }
        
        error_metrics = metrics["error_rates"][tool_name]
        error_metrics["total"] += 1
        if not success:
            error_metrics["errors"] += 1
        error_metrics["rate"] = error_metrics["errors"] / error_metrics["total"] if error_metrics["total"] > 0 else 0.0
        
        self._save_metrics(metrics)

    def get_tool_metrics(self, tool_name: str) -> Dict[str, Any]:
        """Get metrics for a specific tool."""
        metrics = self._load_metrics()
        return metrics["tool_usage"].get(tool_name, {})

    def get_category_distribution(self) -> Dict[str, int]:
        """Get category usage distribution."""
        metrics = self._load_metrics()
        return metrics.get("category_usage", {})

    def get_performance_metrics(self, tool_name: Optional[str] = None) -> Dict[str, Any]:
        """Get performance metrics for a tool or all tools."""
        metrics = self._load_metrics()
        perf_metrics = metrics.get("performance_metrics", {})
        
        if tool_name:
            return perf_metrics.get(tool_name, {})
        return perf_metrics

    def get_error_rates(self) -> Dict[str, Dict[str, Any]]:
        """Get error rates for all tools."""
        metrics = self._load_metrics()
        return metrics.get("error_rates", {})

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of all metrics."""
        metrics = self._load_metrics()
        
        total_tool_calls = sum(
            tool["total_calls"] for tool in metrics["tool_usage"].values()
        )
        
        total_category_usage = sum(metrics["category_usage"].values())
        
        avg_error_rate = 0.0
        if metrics["error_rates"]:
            error_rates = [rate["rate"] for rate in metrics["error_rates"].values()]
            avg_error_rate = sum(error_rates) / len(error_rates) if error_rates else 0.0
        
        return {
            "total_tool_calls": total_tool_calls,
            "total_category_usage": total_category_usage,
            "tools_tracked": len(metrics["tool_usage"]),
            "categories_tracked": len(metrics["category_usage"]),
            "average_error_rate": avg_error_rate,
            "last_updated": metrics.get("last_updated"),
        }


# Global instance
_tracker_instance: Optional[UnifiedToolsMetricsTracker] = None


def get_tracker() -> UnifiedToolsMetricsTracker:
    """Get global metrics tracker instance."""
    global _tracker_instance
    if _tracker_instance is None:
        _tracker_instance = UnifiedToolsMetricsTracker()
    return _tracker_instance


def track_tool_usage(
    tool_name: str,
    category: Optional[str] = None,
    success: bool = True,
    execution_time: Optional[float] = None,
) -> None:
    """Convenience function to track tool usage."""
    tracker = get_tracker()
    tracker.track_tool_usage(tool_name, category, success, execution_time)


__all__ = [
    "UnifiedToolsMetricsTracker",
    "get_tracker",
    "track_tool_usage",
]

