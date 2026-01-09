"""
Template Analytics Module - Unified Template Analysis
===================================================

This module consolidates template analytics functionality including:
- Template performance tracking
- Template usage analytics
- Template optimization recommendations
- Template category analysis
- Template trend analysis
"""

import json
import logging
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import statistics
import sqlite3
from dataclasses_json import dataclass_json
from collections import defaultdict

logger = logging.getLogger(__name__)


class TemplateCategory(Enum):
    """Template categories for analysis."""
    GENERAL = "general"
    CREATIVE = "creative"
    TECHNICAL = "technical"
    BUSINESS = "business"
    EDUCATIONAL = "educational"
    MARKETING = "marketing"
    SOCIAL = "social"
    CUSTOM = "custom"


class PerformanceMetric(Enum):
    """Template performance metrics."""
    SUCCESS_RATE = "success_rate"
    COMPLETION_RATE = "completion_rate"
    USER_SATISFACTION = "user_satisfaction"
    RESPONSE_TIME = "response_time"
    USAGE_FREQUENCY = "usage_frequency"
    ERROR_RATE = "error_rate"


@dataclass_json
@dataclass
class TemplateUsage:
    """Template usage data."""
    template_id: str
    template_name: str
    category: TemplateCategory
    usage_count: int
    success_count: int
    completion_count: int
    avg_satisfaction: float
    avg_response_time: float
    error_count: int
    first_used: datetime
    last_used: datetime
    metadata: Dict[str, Any]


@dataclass_json
@dataclass
class TemplateMetrics:
    """Template performance metrics."""
    template_id: str
    template_name: str
    category: TemplateCategory
    success_rate: float
    completion_rate: float
    user_satisfaction: float
    avg_response_time: float
    usage_frequency: float
    error_rate: float
    performance_score: float
    timestamp: datetime
    metadata: Dict[str, Any]


@dataclass_json
@dataclass
class TemplatePerformanceReport:
    """Template performance report."""
    report_id: str
    generated_at: datetime
    time_period: str
    total_templates: int
    active_templates: int
    avg_performance_score: float
    top_performing_templates: List[TemplateMetrics]
    needs_optimization: List[TemplateMetrics]
    category_performance: Dict[TemplateCategory, Dict[str, float]]
    usage_trends: Dict[str, List[Tuple[datetime, float]]]
    insights: List[str]
    recommendations: List[str]


class TemplateAnalyticsModule:
    """
    Unified template analytics module.
    
    This module provides comprehensive template analysis including:
    - Performance tracking and metrics
    - Usage analytics and trends
    - Template optimization recommendations
    - Category-based analysis
    """
    
    def __init__(self, data_dir: str = "data/template_analytics"):
        """Initialize the template analytics module."""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Database setup
        self.template_db = self.data_dir / "template_analytics.db"
        self._init_database()
        
        # Data storage
        self.usage_file = self.data_dir / "template_usage.jsonl"
        self.metrics_file = self.data_dir / "template_metrics.jsonl"
        self.reports_file = self.data_dir / "template_reports.jsonl"
        
        # Load existing data
        self.template_usage: List[TemplateUsage] = []
        self.template_metrics: List[TemplateMetrics] = []
        self.performance_reports: List[TemplatePerformanceReport] = []
        self._load_existing_data()
        
        logger.info(f"Template Analytics Module initialized at {self.data_dir}")
    
    def _init_database(self):
        """Initialize template analytics database."""
        with sqlite3.connect(self.template_db) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS template_usage (
                    template_id TEXT PRIMARY KEY,
                    template_name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    usage_count INTEGER DEFAULT 0,
                    success_count INTEGER DEFAULT 0,
                    completion_count INTEGER DEFAULT 0,
                    avg_satisfaction REAL DEFAULT 0.0,
                    avg_response_time REAL DEFAULT 0.0,
                    error_count INTEGER DEFAULT 0,
                    first_used TEXT,
                    last_used TEXT,
                    metadata TEXT
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS template_metrics (
                    metric_id TEXT PRIMARY KEY,
                    template_id TEXT NOT NULL,
                    template_name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    success_rate REAL,
                    completion_rate REAL,
                    user_satisfaction REAL,
                    avg_response_time REAL,
                    usage_frequency REAL,
                    error_rate REAL,
                    performance_score REAL,
                    timestamp TEXT,
                    metadata TEXT
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS template_reports (
                    report_id TEXT PRIMARY KEY,
                    generated_at TEXT,
                    time_period TEXT,
                    report_data TEXT
                )
            """)
    
    def _load_existing_data(self):
        """Load existing analytics data."""
        # Load template usage from database
        with sqlite3.connect(self.template_db) as conn:
            cursor = conn.execute("SELECT * FROM template_usage")
            for row in cursor.fetchall():
                usage = TemplateUsage(
                    template_id=row[0],
                    template_name=row[1],
                    category=TemplateCategory(row[2]),
                    usage_count=row[3],
                    success_count=row[4],
                    completion_count=row[5],
                    avg_satisfaction=row[6],
                    avg_response_time=row[7],
                    error_count=row[8],
                    first_used=datetime.fromisoformat(row[9]) if row[9] else datetime.now(),
                    last_used=datetime.fromisoformat(row[10]) if row[10] else datetime.now(),
                    metadata=json.loads(row[11]) if row[11] else {}
                )
                self.template_usage.append(usage)
        
        # Load template metrics from file
        if self.metrics_file.exists():
            with open(self.metrics_file, 'r') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        metric = TemplateMetrics.from_dict(data)
                        metric.timestamp = datetime.fromisoformat(data['timestamp'])
                        self.template_metrics.append(metric)
        
        # Load performance reports from file
        if self.reports_file.exists():
            with open(self.reports_file, 'r') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        report = TemplatePerformanceReport.from_dict(data)
                        report.generated_at = datetime.fromisoformat(data['generated_at'])
                        self.performance_reports.append(report)
        
        logger.info(f"Loaded {len(self.template_usage)} template usage records, {len(self.template_metrics)} metrics, {len(self.performance_reports)} reports")
    
    def record_template_usage(self, template_id: str, template_name: str, category: TemplateCategory,
                            success: bool = True, completion: bool = True, satisfaction: float = 0.0,
                            response_time: float = 0.0, metadata: Dict[str, Any] = None):
        """Record template usage data."""
        if metadata is None:
            metadata = {}
        
        # Update or create usage record
        existing_usage = next((u for u in self.template_usage if u.template_id == template_id), None)
        
        if existing_usage:
            # Update existing record
            existing_usage.usage_count += 1
            if success:
                existing_usage.success_count += 1
            if completion:
                existing_usage.completion_count += 1
            if satisfaction > 0:
                # Update average satisfaction
                total_satisfaction = existing_usage.avg_satisfaction * (existing_usage.usage_count - 1) + satisfaction
                existing_usage.avg_satisfaction = total_satisfaction / existing_usage.usage_count
            if response_time > 0:
                # Update average response time
                total_response_time = existing_usage.avg_response_time * (existing_usage.usage_count - 1) + response_time
                existing_usage.avg_response_time = total_response_time / existing_usage.usage_count
            if not success:
                existing_usage.error_count += 1
            existing_usage.last_used = datetime.now()
            existing_usage.metadata.update(metadata)
        else:
            # Create new record
            usage = TemplateUsage(
                template_id=template_id,
                template_name=template_name,
                category=category,
                usage_count=1,
                success_count=1 if success else 0,
                completion_count=1 if completion else 0,
                avg_satisfaction=satisfaction,
                avg_response_time=response_time,
                error_count=0 if success else 1,
                first_used=datetime.now(),
                last_used=datetime.now(),
                metadata=metadata
            )
            self.template_usage.append(usage)
        
        # Save to database
        self._save_template_usage()
        
        # Generate metrics
        self._generate_template_metrics(template_id)
    
    def _save_template_usage(self):
        """Save template usage to database."""
        with sqlite3.connect(self.template_db) as conn:
            for usage in self.template_usage:
                conn.execute("""
                    INSERT OR REPLACE INTO template_usage 
                    (template_id, template_name, category, usage_count, success_count, completion_count,
                     avg_satisfaction, avg_response_time, error_count, first_used, last_used, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    usage.template_id,
                    usage.template_name,
                    usage.category.value,
                    usage.usage_count,
                    usage.success_count,
                    usage.completion_count,
                    usage.avg_satisfaction,
                    usage.avg_response_time,
                    usage.error_count,
                    usage.first_used.isoformat(),
                    usage.last_used.isoformat(),
                    json.dumps(usage.metadata)
                ))
    
    def _generate_template_metrics(self, template_id: str):
        """Generate performance metrics for a template."""
        usage = next((u for u in self.template_usage if u.template_id == template_id), None)
        if not usage:
            return
        
        # Calculate metrics
        success_rate = usage.success_count / usage.usage_count if usage.usage_count > 0 else 0.0
        completion_rate = usage.completion_count / usage.usage_count if usage.usage_count > 0 else 0.0
        error_rate = usage.error_count / usage.usage_count if usage.usage_count > 0 else 0.0
        
        # Calculate usage frequency (uses per day since first use)
        days_since_first = (datetime.now() - usage.first_used).days
        usage_frequency = usage.usage_count / max(days_since_first, 1)
        
        # Calculate performance score (weighted average)
        performance_score = (
            success_rate * 0.3 +
            completion_rate * 0.2 +
            usage.avg_satisfaction * 0.2 +
            (1 - error_rate) * 0.2 +
            min(usage_frequency / 10, 1.0) * 0.1  # Normalize frequency
        )
        
        # Create metrics
        metrics = TemplateMetrics(
            template_id=usage.template_id,
            template_name=usage.template_name,
            category=usage.category,
            success_rate=success_rate,
            completion_rate=completion_rate,
            user_satisfaction=usage.avg_satisfaction,
            avg_response_time=usage.avg_response_time,
            usage_frequency=usage_frequency,
            error_rate=error_rate,
            performance_score=performance_score,
            timestamp=datetime.now(),
            metadata=usage.metadata
        )
        
        # Save metrics
        self._save_template_metrics(metrics)
    
    def _save_template_metrics(self, metrics: TemplateMetrics):
        """Save template metrics."""
        # Save to file
        with open(self.metrics_file, 'a') as f:
            f.write(json.dumps(asdict(metrics)) + '\n')
        
        # Save to database
        with sqlite3.connect(self.template_db) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO template_metrics 
                (metric_id, template_id, template_name, category, success_rate, completion_rate,
                 user_satisfaction, avg_response_time, usage_frequency, error_rate, performance_score, timestamp, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                f"{metrics.template_id}_{metrics.timestamp.strftime('%Y%m%d_%H%M%S')}",
                metrics.template_id,
                metrics.template_name,
                metrics.category.value,
                metrics.success_rate,
                metrics.completion_rate,
                metrics.user_satisfaction,
                metrics.avg_response_time,
                metrics.usage_frequency,
                metrics.error_rate,
                metrics.performance_score,
                metrics.timestamp.isoformat(),
                json.dumps(metrics.metadata)
            ))
        
        # Update in-memory list
        self.template_metrics.append(metrics)
    
    def generate_performance_report(self, time_period: str = "30d") -> TemplatePerformanceReport:
        """Generate a comprehensive template performance report."""
        cutoff_date = datetime.now() - timedelta(days=int(time_period[:-1]))
        
        # Filter recent metrics
        recent_metrics = [
            metric for metric in self.template_metrics
            if metric.timestamp >= cutoff_date
        ]
        
        if not recent_metrics:
            return self._create_empty_report(time_period)
        
        # Calculate summary statistics
        total_templates = len(set(metric.template_id for metric in recent_metrics))
        active_templates = len([m for m in recent_metrics if m.usage_frequency > 0])
        avg_performance_score = statistics.mean(m.performance_score for m in recent_metrics)
        
        # Get top performing templates
        top_performing = sorted(recent_metrics, key=lambda m: m.performance_score, reverse=True)[:10]
        
        # Get templates needing optimization
        needs_optimization = [m for m in recent_metrics if m.performance_score < 0.6][:10]
        
        # Calculate category performance
        category_performance = self._calculate_category_performance(recent_metrics)
        
        # Calculate usage trends
        usage_trends = self._calculate_usage_trends(recent_metrics, time_period)
        
        # Generate insights
        insights = self._generate_insights(recent_metrics, top_performing, needs_optimization)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(recent_metrics, top_performing, needs_optimization)
        
        # Create report
        report = TemplatePerformanceReport(
            report_id=f"template_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            generated_at=datetime.now(),
            time_period=time_period,
            total_templates=total_templates,
            active_templates=active_templates,
            avg_performance_score=avg_performance_score,
            top_performing_templates=top_performing,
            needs_optimization=needs_optimization,
            category_performance=category_performance,
            usage_trends=usage_trends,
            insights=insights,
            recommendations=recommendations
        )
        
        # Save report
        self._save_performance_report(report)
        
        return report
    
    def _create_empty_report(self, time_period: str) -> TemplatePerformanceReport:
        """Create an empty report when no data is available."""
        return TemplatePerformanceReport(
            report_id=f"template_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            generated_at=datetime.now(),
            time_period=time_period,
            total_templates=0,
            active_templates=0,
            avg_performance_score=0.0,
            top_performing_templates=[],
            needs_optimization=[],
            category_performance={},
            usage_trends={},
            insights=["No template usage data available for the specified time period."],
            recommendations=["Start using templates to generate performance analytics."]
        )
    
    def _calculate_category_performance(self, metrics: List[TemplateMetrics]) -> Dict[TemplateCategory, Dict[str, float]]:
        """Calculate performance by category."""
        category_performance = defaultdict(lambda: defaultdict(list))
        
        for metric in metrics:
            category_performance[metric.category]['performance_scores'].append(metric.performance_score)
            category_performance[metric.category]['success_rates'].append(metric.success_rate)
            category_performance[metric.category]['completion_rates'].append(metric.completion_rate)
            category_performance[metric.category]['satisfaction_scores'].append(metric.user_satisfaction)
        
        # Calculate averages
        result = {}
        for category, data in category_performance.items():
            result[category] = {
                'avg_performance_score': statistics.mean(data['performance_scores']),
                'avg_success_rate': statistics.mean(data['success_rates']),
                'avg_completion_rate': statistics.mean(data['completion_rates']),
                'avg_satisfaction': statistics.mean(data['satisfaction_scores']),
                'template_count': len(data['performance_scores'])
            }
        
        return result
    
    def _calculate_usage_trends(self, metrics: List[TemplateMetrics], time_period: str) -> Dict[str, List[Tuple[datetime, float]]]:
        """Calculate usage trends over time."""
        trends = defaultdict(list)
        
        # Group metrics by template
        template_metrics = defaultdict(list)
        for metric in metrics:
            template_metrics[metric.template_id].append(metric)
        
        # Calculate trends for each template
        for template_id, template_metric_list in template_metrics.items():
            sorted_metrics = sorted(template_metrics[template_id], key=lambda m: m.timestamp)
            
            for metric in sorted_metrics:
                trends[template_id].append((metric.timestamp, metric.usage_frequency))
        
        return dict(trends)
    
    def _generate_insights(self, metrics: List[TemplateMetrics], top_performing: List[TemplateMetrics],
                          needs_optimization: List[TemplateMetrics]) -> List[str]:
        """Generate insights from template analytics."""
        insights = []
        
        if not metrics:
            return ["No template usage data available for analysis."]
        
        # Performance insights
        avg_performance = statistics.mean(m.performance_score for m in metrics)
        if avg_performance > 0.8:
            insights.append("Overall template performance is excellent.")
        elif avg_performance > 0.6:
            insights.append("Overall template performance is good with room for improvement.")
        else:
            insights.append("Overall template performance needs attention.")
        
        # Top performing insights
        if top_performing:
            best_template = top_performing[0]
            insights.append(f"Best performing template: {best_template.template_name} (score: {best_template.performance_score:.2f})")
        
        # Optimization insights
        if needs_optimization:
            insights.append(f"{len(needs_optimization)} templates need optimization.")
        
        # Category insights
        category_performance = self._calculate_category_performance(metrics)
        if category_performance:
            best_category = max(category_performance.items(), key=lambda x: x[1]['avg_performance_score'])
            insights.append(f"Best performing category: {best_category[0].value} (avg score: {best_category[1]['avg_performance_score']:.2f})")
        
        return insights
    
    def _generate_recommendations(self, metrics: List[TemplateMetrics], top_performing: List[TemplateMetrics],
                                needs_optimization: List[TemplateMetrics]) -> List[str]:
        """Generate recommendations based on template analytics."""
        recommendations = []
        
        if not metrics:
            return ["Start using templates to generate recommendations."]
        
        # General recommendations
        avg_performance = statistics.mean(m.performance_score for m in metrics)
        if avg_performance < 0.6:
            recommendations.append("Overall template performance is low. Review and optimize underperforming templates.")
        
        # Optimization recommendations
        if needs_optimization:
            recommendations.append(f"Focus optimization efforts on {len(needs_optimization)} underperforming templates.")
        
        # Success rate recommendations
        low_success_templates = [m for m in metrics if m.success_rate < 0.7]
        if low_success_templates:
            recommendations.append(f"{len(low_success_templates)} templates have low success rates. Investigate and improve error handling.")
        
        # Satisfaction recommendations
        low_satisfaction_templates = [m for m in metrics if m.user_satisfaction < 0.6]
        if low_satisfaction_templates:
            recommendations.append(f"{len(low_satisfaction_templates)} templates have low user satisfaction. Gather feedback and improve user experience.")
        
        # Best practices recommendations
        if top_performing:
            recommendations.append("Study top-performing templates to identify best practices for template design.")
        
        if not recommendations:
            recommendations.append("Template performance is good. Continue monitoring and consider A/B testing for further optimization.")
        
        return recommendations
    
    def _save_performance_report(self, report: TemplatePerformanceReport):
        """Save performance report."""
        with open(self.reports_file, 'a') as f:
            f.write(json.dumps(asdict(report)) + '\n')
        
        # Save to database
        with sqlite3.connect(self.template_db) as conn:
            conn.execute("""
                INSERT INTO template_reports (report_id, generated_at, time_period, report_data)
                VALUES (?, ?, ?, ?)
            """, (
                report.report_id,
                report.generated_at.isoformat(),
                report.time_period,
                json.dumps(asdict(report))
            ))
        
        self.performance_reports.append(report)
    
    def get_insights(self, time_period: str = "30d") -> List[Dict[str, Any]]:
        """Get insights for the specified time period."""
        cutoff_date = datetime.now() - timedelta(days=int(time_period[:-1]))
        
        recent_metrics = [
            metric for metric in self.template_metrics
            if metric.timestamp >= cutoff_date
        ]
        
        insights = []
        for metric in recent_metrics:
            insights.append({
                "insight_id": f"template_{metric.template_id}_{metric.timestamp.strftime('%Y%m%d')}",
                "insight_type": "template_performance",
                "title": f"Template Performance: {metric.template_name}",
                "description": f"Performance score: {metric.performance_score:.2f}, Success rate: {metric.success_rate:.2f}",
                "confidence": 0.9,
                "impact_score": metric.performance_score,
                "recommendations": self._get_template_recommendations(metric),
                "metadata": metric.metadata,
                "timestamp": metric.timestamp,
                "source_data": {"template_id": metric.template_id, "template_name": metric.template_name},
                "analytics_type": "template_performance",
                "tags": [metric.category.value]
            })
        
        return insights
    
    def get_metrics(self, time_period: str = "30d") -> List[Dict[str, Any]]:
        """Get metrics for the specified time period."""
        cutoff_date = datetime.now() - timedelta(days=int(time_period[:-1]))
        
        recent_metrics = [
            metric for metric in self.template_metrics
            if metric.timestamp >= cutoff_date
        ]
        
        return [
            {
                "metric_id": metric.template_id,
                "metric_name": "template_performance_score",
                "value": metric.performance_score,
                "unit": "score",
                "timestamp": metric.timestamp,
                "metadata": metric.metadata,
                "analytics_type": "template_performance",
                "confidence": 0.9,
                "trend": "stable"
            }
            for metric in recent_metrics
        ]
    
    def get_summary(self, time_period: str = "30d") -> Dict[str, Any]:
        """Get summary for the specified time period."""
        cutoff_date = datetime.now() - timedelta(days=int(time_period[:-1]))
        
        recent_metrics = [
            metric for metric in self.template_metrics
            if metric.timestamp >= cutoff_date
        ]
        
        if not recent_metrics:
            return {"total_templates": 0, "avg_performance_score": 0.0}
        
        return {
            "total_templates": len(set(m.template_id for m in recent_metrics)),
            "avg_performance_score": statistics.mean(m.performance_score for m in recent_metrics),
            "avg_success_rate": statistics.mean(m.success_rate for m in recent_metrics),
            "avg_completion_rate": statistics.mean(m.completion_rate for m in recent_metrics),
            "category_distribution": self._get_category_distribution(recent_metrics)
        }
    
    def _get_template_recommendations(self, metric: TemplateMetrics) -> List[str]:
        """Get recommendations for a specific template."""
        recommendations = []
        
        if metric.performance_score < 0.6:
            recommendations.append("Template needs optimization.")
        
        if metric.success_rate < 0.7:
            recommendations.append("Improve error handling and success rate.")
        
        if metric.user_satisfaction < 0.6:
            recommendations.append("Gather user feedback and improve user experience.")
        
        return recommendations
    
    def _get_category_distribution(self, metrics: List[TemplateMetrics]) -> Dict[str, int]:
        """Get distribution of template categories."""
        distribution = defaultdict(int)
        for metric in metrics:
            distribution[metric.category.value] += 1
        return dict(distribution) 