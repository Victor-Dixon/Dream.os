# <!-- SSOT Domain: core -->
# AUTO-GENERATED __init__.py
# DO NOT EDIT MANUALLY - changes may be overwritten

from . import engine
from . import metric_manager
from . import reporter
from . import widget_manager

# Export classes for backward compatibility
from .engine import DashboardEngine
from .models import (
    DashboardConfig,
    DashboardWidget,
    MetricType,
    PerformanceAlert,
    PerformanceMetric,
    PerformanceReport,
)

# Create orchestrator alias
try:
    from .engine import DashboardEngine as PerformanceDashboardOrchestrator
except ImportError:
    PerformanceDashboardOrchestrator = DashboardEngine

# Export for performance_dashboard.py
DashboardModels = type('DashboardModels', (), {
    'DashboardConfig': DashboardConfig,
    'DashboardWidget': DashboardWidget,
    'MetricType': MetricType,
    'PerformanceAlert': PerformanceAlert,
    'PerformanceMetric': PerformanceMetric,
    'PerformanceReport': PerformanceReport,
})

DashboardReporter = reporter  # Module reference

__all__ = [
    'engine',
    'metric_manager',
    'reporter',
    'widget_manager',
    'DashboardEngine',
    'PerformanceDashboardOrchestrator',
    'DashboardModels',
    'DashboardReporter',
    'DashboardConfig',
    'DashboardWidget',
    'MetricType',
    'PerformanceAlert',
    'PerformanceMetric',
    'PerformanceReport',
]
