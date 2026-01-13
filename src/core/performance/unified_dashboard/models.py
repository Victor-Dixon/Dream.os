"""
<!-- SSOT Domain: core -->

Dashboard Models - V2 Compliance
================================

Data models for unified dashboard system.

V2 Compliance: < 300 lines, single responsibility, data models.

Author: Agent-3 (Infrastructure & DevOps Specialist) - Blocker Fix
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional


class MetricType(Enum):
    """Metric type enumeration."""
    GAUGE = "gauge"
    COUNTER = "counter"
    TIMER = "timer"
    HISTOGRAM = "histogram"


@dataclass
class PerformanceMetric:
    """Performance metric data structure for dashboard."""
    
    metric_id: str
    name: str
    metric_type: MetricType
    value: float
    timestamp: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    tags: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DashboardConfig:
    """Dashboard configuration."""
    
    config_id: str
    name: str
    settings: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None


@dataclass
class DashboardWidget:
    """Dashboard widget."""
    
    widget_id: str
    name: str
    widget_type: str
    config: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None


class AlertLevel(Enum):
    """Alert level enumeration."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class PerformanceAlert:
    """Performance alert."""
    
    alert_id: str
    message: str
    level: AlertLevel
    metric_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class PerformanceReport:
    """Performance report."""
    
    report_id: str
    report_type: str
    data: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

