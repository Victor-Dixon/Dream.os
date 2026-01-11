#!/usr/bin/env python3
"""
Template Models
==============

Data models, enums, and dataclasses for the template system.
"""

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses_json import dataclass_json

from dreamscape.core.utils.database_mixin import DatabaseCleanupMixin

logger = logging.getLogger(__name__)


class MetricType(Enum):
    """Types of performance metrics"""

    USAGE_COUNT = "usage_count"
    SUCCESS_RATE = "success_rate"
    RESPONSE_TIME = "response_time"
    USER_SATISFACTION = "user_satisfaction"
    CONVERSION_RATE = "conversion_rate"
    ENGAGEMENT_SCORE = "engagement_score"
    ERROR_RATE = "error_rate"
    COMPLETION_RATE = "completion_rate"


class TemplateCategory(Enum):
    """Template categories for analysis"""
    QUEST_GENERATION = "quest_generation"
    CONTENT_CREATION = "content_creation"
    RESPONSE_ANALYSIS = "response_analysis"
    BREAKTHROUGH_DETECTION = "breakthrough_detection"
    SOCIAL_MEDIA = "social_media"
    BLOG_POSTS = "blog_posts"
    NOTIFICATION = "notification"
    SYSTEM = "system"
    # Legacy/alternate aliases for backward compatibility
    REVIEW = "response_analysis"  # alias for RESPONSE_ANALYSIS
    ANALYSIS = "response_analysis"  # alias for RESPONSE_ANALYSIS
    PLANNING = "quest_generation"  # alias for QUEST_GENERATION
    REPORTING = "content_creation"  # alias for CONTENT_CREATION
    OPTIMIZATION = "system"  # alias for SYSTEM
    GENERATION = "quest_generation"  # alias for QUEST_GENERATION


@dataclass_json
@dataclass
class TemplateUsage:
    """Individual template usage record"""

    template_id: str
    template_name: str
    category: TemplateCategory
    timestamp: datetime
    execution_time: float
    success: bool
    error_message: Optional[str] = None
    user_feedback: Optional[float] = None
    context_size: int = 0
    output_quality_score: Optional[float] = None
    parameters_used: Dict[str, Any] = None

    def __post_init__(self):
        # Ensure parameters_used is always a dict
        if self.parameters_used is None:
            self.parameters_used = {}
        # Ensure context_size is always an int
        if self.context_size is None:
            self.context_size = 0
        # Ensure error_message is a string or None
        if self.error_message is not None and not isinstance(self.error_message, str):
            self.error_message = str(self.error_message)
        # Ensure user_feedback and output_quality_score are floats or None
        if self.user_feedback is not None and not isinstance(self.user_feedback, float):
            try:
                self.user_feedback = float(self.user_feedback)
            except Exception:
                self.user_feedback = None
        if self.output_quality_score is not None and not isinstance(
            self.output_quality_score, float
        ):
            try:
                self.output_quality_score = float(self.output_quality_score)
            except Exception:
                self.output_quality_score = None

    @classmethod
    def from_dict(cls, data: dict):
        # Always set parameters_used to {} if missing or None
        if "parameters_used" not in data or data["parameters_used"] is None:
            data = dict(data)  # copy to avoid mutating input
            data["parameters_used"] = {}
        
        # Handle legacy category mapping silently
        if "category" in data and data["category"] == "OPTIMIZATION":
            data["category"] = "SYSTEM"
            # Don't log warning for this common mapping
        
        # Ensure error_message field is always present
        if "error_message" not in data:
            data["error_message"] = None
        
        return cls.schema().load(data)


def _safe_templateusage_from_dict(data):
    """Safely create TemplateUsage from dict with error handling."""
    try:
        return TemplateUsage.from_dict(data)
    except Exception as e:
        logger.warning(f"Failed to parse TemplateUsage from dict: {e}")
        # Return a minimal valid TemplateUsage
        return TemplateUsage(
            template_id=data.get("template_id", "unknown"),
            template_name=data.get("template_name", "Unknown"),
            category=TemplateCategory.SYSTEM,
            timestamp=datetime.now(),
            execution_time=0.0,
            success=False,
            error_message=f"Parse error: {e}",
            parameters_used=data.get("parameters_used", {})
        )


def _safe_fromisoformat(val):
    """Safely parse ISO format datetime string."""
    if isinstance(val, str):
        try:
            return datetime.fromisoformat(val)
        except ValueError:
            logger.warning(f"Failed to parse datetime: {val}")
            return datetime.now()
    return val


@dataclass_json
@dataclass
class TemplateMetrics:
    """Aggregated metrics for a template"""

    template_id: str
    template_name: str
    category: TemplateCategory
    total_usage: int
    success_count: int
    error_count: int
    avg_execution_time: float
    avg_user_feedback: float
    avg_output_quality: float
    success_rate: float
    error_rate: float
    last_used: datetime
    first_used: datetime
    usage_trend: List[Tuple[datetime, int]]  # (date, count)
    performance_score: float
    optimization_priority: str  # "high", "medium", "low"


@dataclass_json
@dataclass
class PerformanceReport:
    """Comprehensive performance report"""

    report_id: str
    generated_at: datetime
    time_period: str
    total_templates: int
    total_usage: int
    overall_success_rate: float
    avg_execution_time: float
    top_performers: List[TemplateMetrics]
    needs_optimization: List[TemplateMetrics]
    category_breakdown: Dict[TemplateCategory, Dict[str, float]]
    trends: Dict[str, List[Tuple[datetime, float]]]
    recommendations: List[str]


@dataclass
class PromptTemplate(DatabaseCleanupMixin):
    """Core template data model"""
    
    id: str
    type: str
    name: str
    content: str
    parent_id: Optional[str] = None
    description: Optional[str] = None
    variables: List[str] = None
    metadata: Dict = None
    version: str = "1.0.0"
    created_at: datetime = None
    updated_at: datetime = None
    is_active: bool = True
    success_rate: float = 0.0
    usage_count: int = 0

    def __post_init__(self):
        if self.variables is None:
            self.variables = []
        if self.metadata is None:
            self.metadata = {}
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()


@dataclass
class TemplateVersion(DatabaseCleanupMixin):
    """Template version data model"""
    
    template_id: str
    version: str
    content: str
    changes: Optional[str] = None
    performance_data: Dict = None
    created_at: datetime = None
    created_by: Optional[str] = None
    is_active: bool = True

    def __post_init__(self):
        if self.performance_data is None:
            self.performance_data = {}
        if self.created_at is None:
            self.created_at = datetime.now() 