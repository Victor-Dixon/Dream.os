"""
Dashboard Models - Stub for missing models

This file provides the model classes needed by unified_dashboard modules.
Created to satisfy imports for testing purposes.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Optional


class MetricType(Enum):
    """Metric type enumeration."""
    GAUGE = "gauge"
    COUNTER = "counter"
    TIMER = "timer"
    HISTOGRAM = "histogram"


class PerformanceMetric:
    """Performance metric data structure."""
    
    def __init__(
        self,
        metric_id: str,
        name: str,
        metric_type: MetricType,
        value: float,
        timestamp: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        **kwargs
    ):
        """Initialize performance metric."""
        self.metric_id = metric_id
        self.name = name
        self.metric_type = metric_type
        self.value = value
        self.timestamp = timestamp or datetime.now()
        self.updated_at = updated_at or datetime.now()
        # Allow additional attributes
        for key, value in kwargs.items():
            setattr(self, key, value)


class DashboardConfig:
    """Dashboard configuration."""
    
    def __init__(self, config_id: str, **kwargs):
        """Initialize dashboard config."""
        self.config_id = config_id
        for key, value in kwargs.items():
            setattr(self, key, value)


class DashboardWidget:
    """Dashboard widget."""
    
    def __init__(self, widget_id: str, **kwargs):
        """Initialize dashboard widget."""
        self.widget_id = widget_id
        for key, value in kwargs.items():
            setattr(self, key, value)


class AlertLevel(Enum):
    """Alert level enumeration."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class PerformanceAlert:
    """Performance alert."""
    
    def __init__(self, alert_id: str, level: AlertLevel, message: str, **kwargs):
        """Initialize performance alert."""
        self.alert_id = alert_id
        self.level = level
        self.message = message
        for key, value in kwargs.items():
            setattr(self, key, value)


class PerformanceReport:
    """Performance report."""
    
    def __init__(self, report_id: str, report_type: str = "standard", **kwargs):
        """Initialize performance report."""
        self.report_id = report_id
        self.report_type = report_type
        for key, value in kwargs.items():
            setattr(self, key, value)

