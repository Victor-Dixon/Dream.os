"""
Analytics Models
===============

Data models and classes for the expanded analytics system.
This component contains all the dataclasses and model definitions.

Extracted from expanded_analytics_system.py for better modularity and maintainability.
"""

import json
import logging
from datetime import datetime
from typing import List, Dict, Optional, Any, Tuple, Union
from dataclasses import dataclass, asdict, field
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class AnalyticsReport:
    """Comprehensive analytics report."""
    id: str
    title: str
    report_type: str
    generated_at: datetime
    time_period: str
    data_summary: Dict[str, Any]
    insights: List[Dict[str, Any]]
    recommendations: List[str]
    charts_data: Dict[str, Any]
    export_formats: List[str] = field(default_factory=lambda: ["json", "csv", "html"])
    is_public: bool = False
    author_id: str = ""
    author_name: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert report to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'report_type': self.report_type,
            'generated_at': self.generated_at.isoformat(),
            'time_period': self.time_period,
            'data_summary': self.data_summary,
            'insights': self.insights,
            'recommendations': self.recommendations,
            'charts_data': self.charts_data,
            'export_formats': self.export_formats,
            'is_public': self.is_public,
            'author_id': self.author_id,
            'author_name': self.author_name
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AnalyticsReport':
        """Create AnalyticsReport from dictionary."""
        # Convert string datetime back to datetime object
        if isinstance(data.get('generated_at'), str):
            data['generated_at'] = datetime.fromisoformat(data['generated_at'])
        
        return cls(**data)
    
    def to_json(self) -> str:
        """Convert report to JSON string."""
        return json.dumps(self.to_dict(), indent=2, default=str)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'AnalyticsReport':
        """Create AnalyticsReport from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)


@dataclass
class AnalyticsDashboard:
    """Analytics dashboard configuration."""
    id: str
    name: str
    description: str
    widgets: List[Dict[str, Any]]
    layout: Dict[str, Any]
    refresh_interval: int = 300  # seconds
    is_public: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    owner_id: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert dashboard to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'widgets': self.widgets,
            'layout': self.layout,
            'refresh_interval': self.refresh_interval,
            'is_public': self.is_public,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'owner_id': self.owner_id
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AnalyticsDashboard':
        """Create AnalyticsDashboard from dictionary."""
        # Convert string datetimes back to datetime objects
        for field_name in ['created_at', 'updated_at']:
            if isinstance(data.get(field_name), str):
                data[field_name] = datetime.fromisoformat(data[field_name])
        
        return cls(**data)
    
    def to_json(self) -> str:
        """Convert dashboard to JSON string."""
        return json.dumps(self.to_dict(), indent=2, default=str)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'AnalyticsDashboard':
        """Create AnalyticsDashboard from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)


@dataclass
class AnalyticsWidget:
    """Analytics widget configuration."""
    id: str
    type: str  # chart, metric, table, text
    title: str
    data_source: str
    config: Dict[str, Any]
    position: Dict[str, int]  # x, y, width, height
    refresh_interval: int = 60  # seconds
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert widget to dictionary."""
        return {
            'id': self.id,
            'type': self.type,
            'title': self.title,
            'data_source': self.data_source,
            'config': self.config,
            'position': self.position,
            'refresh_interval': self.refresh_interval
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AnalyticsWidget':
        """Create AnalyticsWidget from dictionary."""
        return cls(**data)
    
    def to_json(self) -> str:
        """Convert widget to JSON string."""
        return json.dumps(self.to_dict(), indent=2, default=str)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'AnalyticsWidget':
        """Create AnalyticsWidget from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)


@dataclass
class TrendAnalysis:
    """Trend analysis result."""
    metric: str
    trend_direction: str  # increasing, decreasing, stable
    trend_strength: float  # 0.0 to 1.0
    change_percentage: float
    confidence: float
    period: str
    data_points: List[Tuple[datetime, float]]
    prediction: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert trend analysis to dictionary."""
        return {
            'metric': self.metric,
            'trend_direction': self.trend_direction,
            'trend_strength': self.trend_strength,
            'change_percentage': self.change_percentage,
            'confidence': self.confidence,
            'period': self.period,
            'data_points': [(dt.isoformat(), value) for dt, value in self.data_points],
            'prediction': self.prediction
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TrendAnalysis':
        """Create TrendAnalysis from dictionary."""
        # Convert data_points back to datetime objects
        if 'data_points' in data:
            data['data_points'] = [
                (datetime.fromisoformat(dt_str), value) 
                for dt_str, value in data['data_points']
            ]
        
        return cls(**data)
    
    def to_json(self) -> str:
        """Convert trend analysis to JSON string."""
        return json.dumps(self.to_dict(), indent=2, default=str)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'TrendAnalysis':
        """Create TrendAnalysis from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)


@dataclass
class PredictiveInsight:
    """Predictive analytics insight."""
    id: str
    insight_type: str
    metric: str
    prediction: float
    confidence: float
    timeframe: str
    factors: List[str]
    impact_score: float
    generated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert predictive insight to dictionary."""
        return {
            'id': self.id,
            'insight_type': self.insight_type,
            'metric': self.metric,
            'prediction': self.prediction,
            'confidence': self.confidence,
            'timeframe': self.timeframe,
            'factors': self.factors,
            'impact_score': self.impact_score,
            'generated_at': self.generated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PredictiveInsight':
        """Create PredictiveInsight from dictionary."""
        # Convert string datetime back to datetime object
        if isinstance(data.get('generated_at'), str):
            data['generated_at'] = datetime.fromisoformat(data['generated_at'])
        
        return cls(**data)
    
    def to_json(self) -> str:
        """Convert predictive insight to JSON string."""
        return json.dumps(self.to_dict(), indent=2, default=str)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'PredictiveInsight':
        """Create PredictiveInsight from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)


@dataclass
class AnalyticsShare:
    """Analytics sharing configuration."""
    id: str
    resource_id: str  # report_id or dashboard_id
    resource_type: str  # 'report' or 'dashboard'
    shared_with: str
    shared_at: datetime = field(default_factory=datetime.now)
    permissions: Dict[str, bool] = field(default_factory=lambda: {
        'view': True,
        'edit': False,
        'share': False,
        'delete': False
    })
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert share to dictionary."""
        return {
            'id': self.id,
            'resource_id': self.resource_id,
            'resource_type': self.resource_type,
            'shared_with': self.shared_with,
            'shared_at': self.shared_at.isoformat(),
            'permissions': self.permissions
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AnalyticsShare':
        """Create AnalyticsShare from dictionary."""
        # Convert string datetime back to datetime object
        if isinstance(data.get('shared_at'), str):
            data['shared_at'] = datetime.fromisoformat(data['shared_at'])
        
        return cls(**data)
    
    def to_json(self) -> str:
        """Convert share to JSON string."""
        return json.dumps(self.to_dict(), indent=2, default=str)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'AnalyticsShare':
        """Create AnalyticsShare from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)


@dataclass
class AnalyticsExport:
    """Analytics export configuration."""
    id: str
    resource_id: str
    resource_type: str  # 'report' or 'dashboard'
    format_type: str  # 'json', 'csv', 'html', 'pdf'
    export_path: str
    exported_at: datetime = field(default_factory=datetime.now)
    file_size: Optional[int] = None
    checksum: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert export to dictionary."""
        return {
            'id': self.id,
            'resource_id': self.resource_id,
            'resource_type': self.resource_type,
            'format_type': self.format_type,
            'export_path': self.export_path,
            'exported_at': self.exported_at.isoformat(),
            'file_size': self.file_size,
            'checksum': self.checksum
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AnalyticsExport':
        """Create AnalyticsExport from dictionary."""
        # Convert string datetime back to datetime object
        if isinstance(data.get('exported_at'), str):
            data['exported_at'] = datetime.fromisoformat(data['exported_at'])
        
        return cls(**data)
    
    def to_json(self) -> str:
        """Convert export to JSON string."""
        return json.dumps(self.to_dict(), indent=2, default=str)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'AnalyticsExport':
        """Create AnalyticsExport from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)


# Convenience functions for model creation
def create_analytics_report(
    title: str,
    report_type: str = "comprehensive",
    time_period: str = "30d",
    author_id: str = "",
    author_name: str = ""
) -> AnalyticsReport:
    """Create a new analytics report."""
    import uuid
    
    return AnalyticsReport(
        id=str(uuid.uuid4()),
        title=title,
        report_type=report_type,
        generated_at=datetime.now(),
        time_period=time_period,
        data_summary={},
        insights=[],
        recommendations=[],
        charts_data={},
        author_id=author_id,
        author_name=author_name
    )


def create_analytics_dashboard(
    name: str,
    description: str = "",
    owner_id: str = "",
    widgets: List[Dict[str, Any]] = None
) -> AnalyticsDashboard:
    """Create a new analytics dashboard."""
    import uuid
    
    if widgets is None:
        widgets = []
    
    return AnalyticsDashboard(
        id=str(uuid.uuid4()),
        name=name,
        description=description,
        widgets=widgets,
        layout={},
        owner_id=owner_id
    )


def create_analytics_widget(
    widget_type: str,
    title: str,
    data_source: str,
    config: Dict[str, Any] = None,
    position: Dict[str, int] = None
) -> AnalyticsWidget:
    """Create a new analytics widget."""
    import uuid
    
    if config is None:
        config = {}
    
    if position is None:
        position = {'x': 0, 'y': 0, 'width': 6, 'height': 4}
    
    return AnalyticsWidget(
        id=str(uuid.uuid4()),
        type=widget_type,
        title=title,
        data_source=data_source,
        config=config,
        position=position
    )


def create_trend_analysis(
    metric: str,
    trend_direction: str,
    trend_strength: float,
    change_percentage: float,
    confidence: float,
    period: str,
    data_points: List[Tuple[datetime, float]]
) -> TrendAnalysis:
    """Create a new trend analysis."""
    return TrendAnalysis(
        metric=metric,
        trend_direction=trend_direction,
        trend_strength=trend_strength,
        change_percentage=change_percentage,
        confidence=confidence,
        period=period,
        data_points=data_points
    )


def create_predictive_insight(
    insight_type: str,
    metric: str,
    prediction: float,
    confidence: float,
    timeframe: str,
    factors: List[str],
    impact_score: float
) -> PredictiveInsight:
    """Create a new predictive insight."""
    import uuid
    
    return PredictiveInsight(
        id=str(uuid.uuid4()),
        insight_type=insight_type,
        metric=metric,
        prediction=prediction,
        confidence=confidence,
        timeframe=timeframe,
        factors=factors,
        impact_score=impact_score
    ) 