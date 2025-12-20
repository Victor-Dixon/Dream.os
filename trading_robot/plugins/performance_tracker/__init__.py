"""
Performance Tracker Plugin
==========================

Plugin for tracking and aggregating trading performance metrics.
Provides comprehensive performance tracking for users and plugins.

V2 Compliant: Modular structure
"""

from .performance_tracker import PerformanceTracker
from .metrics_collector import MetricsCollector
from .metrics_storage import MetricsStorage
from .metrics_aggregator import MetricsAggregator
from .performance_dashboard import PerformanceDashboard

__all__ = [
    "PerformanceTracker",
    "MetricsCollector",
    "MetricsStorage",
    "MetricsAggregator",
    "PerformanceDashboard",
]

