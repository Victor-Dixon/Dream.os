#!/usr/bin/env python3
"""
Template Processors
==================

Analytics, response management, debugging, and other processing operations.
"""

import json
import logging
import csv
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict

from .template_models import (
    TemplateUsage, TemplateMetrics, PerformanceReport, 
    TemplateCategory, MetricType, _safe_templateusage_from_dict,
    _safe_fromisoformat
)
from .template_engine import PromptTemplateEngine

logger = logging.getLogger(__name__)


class TemplateResponseManager:
    """Manages template response processing and feedback."""
    
    def __init__(self, template_engine: PromptTemplateEngine):
        """Initialize the response manager."""
        self.template_engine = template_engine

    def process_template_response(
        self, template_id: str, response: str, success: bool = True
    ) -> Dict:
        """Process a template response and update metrics."""
        try:
            # Update success rate
            self.template_engine.update_success_rate(template_id, success)
            
            # Get updated template info
            template = self.template_engine.get_template(template_id)
            
            return {
                "template_id": template_id,
                "response": response,
                "success": success,
                "template_name": template.name if template else "Unknown",
                "success_rate": template.success_rate if template else 0.0,
                "usage_count": template.usage_count if template else 0,
                "processed_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to process template response: {e}")
            return {
                "template_id": template_id,
                "response": response,
                "success": False,
                "error": str(e),
                "processed_at": datetime.now().isoformat()
            }

    def get_template_performance(self, template_id: str) -> Dict:
        """Get performance metrics for a template."""
        try:
            template = self.template_engine.get_template(template_id)
            if not template:
                return {"error": "Template not found"}
            
            versions = self.template_engine.get_template_versions(template_id)
            
            return {
                "template_id": template_id,
                "name": template.name,
                "success_rate": template.success_rate,
                "usage_count": template.usage_count,
                "version": template.version,
                "is_active": template.is_active,
                "versions_count": len(versions),
                "last_updated": template.updated_at.isoformat() if template.updated_at else None,
                "created_at": template.created_at.isoformat() if template.created_at else None
            }
        except Exception as e:
            logger.error(f"Failed to get template performance: {e}")
            return {"error": str(e)}


class TemplatePerformanceAnalytics:
    """Analytics for template performance and optimization."""
    
    def __init__(
        self,
        template_engine: PromptTemplateEngine,
        data_dir: str = "data/template_analytics",
    ):
        """Initialize the analytics system."""
        self.template_engine = template_engine
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Data storage files
        self.usage_file = self.data_dir / "template_usage.jsonl"
        self.metrics_file = self.data_dir / "template_metrics.json"
        self.reports_file = self.data_dir / "performance_reports.json"
        
        # In-memory storage
        self.usage_records: List[TemplateUsage] = []
        self.template_metrics: Dict[str, TemplateMetrics] = {}
        
        # Load existing data
        self._load_existing_data()

    def _load_existing_data(self):
        """Load existing analytics data from files."""
        try:
            # Load usage records
            if self.usage_file.exists():
                with open(self.usage_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            try:
                                data = json.loads(line)
                                usage = _safe_templateusage_from_dict(data)
                                self.usage_records.append(usage)
                            except Exception as e:
                                logger.warning(f"Failed to load usage record: {e}")
            
            # Load template metrics
            if self.metrics_file.exists():
                with open(self.metrics_file, 'r', encoding='utf-8') as f:
                    metrics_data = json.load(f)
                    for template_id, data in metrics_data.items():
                        try:
                            metrics = TemplateMetrics.schema().load(data)
                            self.template_metrics[template_id] = metrics
                        except Exception as e:
                            logger.warning(f"Failed to load metrics for {template_id}: {e}")
            
            logger.info(f"Loaded {len(self.usage_records)} usage records and {len(self.template_metrics)} metrics")
            
        except Exception as e:
            logger.error(f"Failed to load existing analytics data: {e}")

    def record_template_usage(self, usage: TemplateUsage):
        """Record a template usage event."""
        try:
            # Add to memory
            self.usage_records.append(usage)
            
            # Save to file
            with open(self.usage_file, 'a', encoding='utf-8') as f:
                f.write(usage.to_json() + '\n')
            
            # Update metrics
            self._update_template_metrics(usage)
            
        except Exception as e:
            logger.error(f"Failed to record template usage: {e}")

    def _update_template_metrics(self, usage: TemplateUsage):
        """Update aggregated metrics for a template."""
        template_id = usage.template_id
        
        if template_id not in self.template_metrics:
            # Create new metrics
            self.template_metrics[template_id] = TemplateMetrics(
                template_id=template_id,
                template_name=usage.template_name,
                category=usage.category,
                total_usage=0,
                success_count=0,
                error_count=0,
                avg_execution_time=0.0,
                avg_user_feedback=0.0,
                avg_output_quality=0.0,
                success_rate=0.0,
                error_rate=0.0,
                last_used=usage.timestamp,
                first_used=usage.timestamp,
                usage_trend=[],
                performance_score=0.0,
                optimization_priority="low"
            )
        
        metrics = self.template_metrics[template_id]
        
        # Update basic counts
        metrics.total_usage += 1
        if usage.success:
            metrics.success_count += 1
        else:
            metrics.error_count += 1
        
        # Update averages
        metrics.avg_execution_time = (
            (metrics.avg_execution_time * (metrics.total_usage - 1) + usage.execution_time) 
            / metrics.total_usage
        )
        
        if usage.user_feedback is not None:
            current_feedback_count = sum(1 for u in self.usage_records 
                                       if u.template_id == template_id and u.user_feedback is not None)
            metrics.avg_user_feedback = (
                (metrics.avg_user_feedback * (current_feedback_count - 1) + usage.user_feedback)
                / current_feedback_count
            )
        
        if usage.output_quality_score is not None:
            current_quality_count = sum(1 for u in self.usage_records 
                                      if u.template_id == template_id and u.output_quality_score is not None)
            metrics.avg_output_quality = (
                (metrics.avg_output_quality * (current_quality_count - 1) + usage.output_quality_score)
                / current_quality_count
            )
        
        # Update rates
        metrics.success_rate = metrics.success_count / metrics.total_usage
        metrics.error_rate = metrics.error_count / metrics.total_usage
        
        # Update timestamps
        metrics.last_used = usage.timestamp
        if metrics.first_used is None:
            metrics.first_used = usage.timestamp
        
        # Update usage trend
        self._update_usage_trend(metrics, usage.timestamp)
        
        # Update performance score and priority
        metrics.performance_score = self._calculate_performance_score(metrics)
        metrics.optimization_priority = self._determine_optimization_priority(metrics)
        
        # Save updated metrics
        self._save_metrics()

    def _update_usage_trend(self, metrics: TemplateMetrics, timestamp: datetime):
        """Update usage trend data."""
        # Group usage by date
        date_str = timestamp.strftime("%Y-%m-%d")
        
        # Find existing entry for this date
        for i, (trend_date, count) in enumerate(metrics.usage_trend):
            if trend_date.strftime("%Y-%m-%d") == date_str:
                metrics.usage_trend[i] = (trend_date, count + 1)
                return
        
        # Add new date entry
        metrics.usage_trend.append((timestamp, 1))
        
        # Keep only last 30 days
        cutoff_date = datetime.now() - timedelta(days=30)
        metrics.usage_trend = [
            (date, count) for date, count in metrics.usage_trend 
            if date >= cutoff_date
        ]

    def _calculate_performance_score(self, metrics: TemplateMetrics) -> float:
        """Calculate overall performance score for a template."""
        score = 0.0
        
        # Success rate weight: 40%
        score += metrics.success_rate * 0.4
        
        # User feedback weight: 25%
        if metrics.avg_user_feedback > 0:
            score += min(metrics.avg_user_feedback / 5.0, 1.0) * 0.25
        
        # Output quality weight: 20%
        if metrics.avg_output_quality > 0:
            score += min(metrics.avg_output_quality / 5.0, 1.0) * 0.2
        
        # Usage frequency weight: 15%
        if metrics.total_usage > 0:
            # Normalize usage count (0-100 uses = 0-1 score)
            usage_score = min(metrics.total_usage / 100.0, 1.0)
            score += usage_score * 0.15
        
        return min(score, 1.0)  # Cap at 1.0

    def _determine_optimization_priority(self, metrics: TemplateMetrics) -> str:
        """Determine optimization priority based on metrics."""
        if metrics.success_rate < 0.5 or metrics.error_rate > 0.3:
            return "high"
        elif metrics.success_rate < 0.7 or metrics.performance_score < 0.6:
            return "medium"
        else:
            return "low"

    def _save_metrics(self):
        """Save metrics to file."""
        try:
            metrics_data = {
                template_id: metrics.to_dict() 
                for template_id, metrics in self.template_metrics.items()
            }
            
            with open(self.metrics_file, 'w', encoding='utf-8') as f:
                json.dump(metrics_data, f, indent=2, default=str)
                
        except Exception as e:
            logger.error(f"Failed to save metrics: {e}")

    def get_template_metrics(self, template_id: str) -> Optional[TemplateMetrics]:
        """Get metrics for a specific template."""
        return self.template_metrics.get(template_id)

    def get_category_metrics(self, category: TemplateCategory) -> List[TemplateMetrics]:
        """Get metrics for all templates in a category."""
        return [
            metrics for metrics in self.template_metrics.values()
            if metrics.category == category
        ]

    def get_top_performers(self, limit: int = 10) -> List[TemplateMetrics]:
        """Get top performing templates."""
        sorted_metrics = sorted(
            self.template_metrics.values(),
            key=lambda m: m.performance_score,
            reverse=True
        )
        return sorted_metrics[:limit]

    def get_needs_optimization(self, priority: str = "high") -> List[TemplateMetrics]:
        """Get templates that need optimization."""
        return [
            metrics for metrics in self.template_metrics.values()
            if metrics.optimization_priority == priority
        ]

    def generate_performance_report(
        self, time_period: str = "30d"
    ) -> PerformanceReport:
        """Generate comprehensive performance report."""
        try:
            # Calculate time period
            if time_period.endswith('d'):
                days = int(time_period[:-1])
                cutoff_date = datetime.now() - timedelta(days=days)
            else:
                cutoff_date = datetime.now() - timedelta(days=30)
            
            # Filter usage records by time period
            recent_usage = [
                usage for usage in self.usage_records
                if usage.timestamp >= cutoff_date
            ]
            
            # Calculate overall statistics
            total_templates = len(self.template_metrics)
            total_usage = len(recent_usage)
            overall_success_rate = (
                sum(1 for u in recent_usage if u.success) / total_usage 
                if total_usage > 0 else 0.0
            )
            avg_execution_time = (
                sum(u.execution_time for u in recent_usage) / total_usage
                if total_usage > 0 else 0.0
            )
            
            # Get top performers and needs optimization
            top_performers = self.get_top_performers(10)
            needs_optimization = self.get_needs_optimization("high")
            
            # Calculate category breakdown
            category_breakdown = self._calculate_category_breakdown(recent_usage)
            
            # Calculate trends
            trends = self._calculate_trends(recent_usage)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                recent_usage, top_performers, needs_optimization
            )
            
            report = PerformanceReport(
                report_id=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                generated_at=datetime.now(),
                time_period=time_period,
                total_templates=total_templates,
                total_usage=total_usage,
                overall_success_rate=overall_success_rate,
                avg_execution_time=avg_execution_time,
                top_performers=top_performers,
                needs_optimization=needs_optimization,
                category_breakdown=category_breakdown,
                trends=trends,
                recommendations=recommendations
            )
            
            # Save report
            self._save_report(report)
            
            return report
            
        except Exception as e:
            logger.error(f"Failed to generate performance report: {e}")
            raise

    def _calculate_category_breakdown(
        self, usage_records: List[TemplateUsage]
    ) -> Dict[TemplateCategory, Dict[str, float]]:
        """Calculate breakdown by category."""
        breakdown = defaultdict(lambda: {
            'count': 0, 'success_rate': 0.0, 'avg_execution_time': 0.0
        })
        
        for usage in usage_records:
            category = usage.category
            breakdown[category]['count'] += 1
            
            if usage.success:
                breakdown[category]['success_rate'] += 1
            breakdown[category]['avg_execution_time'] += usage.execution_time
        
        # Calculate averages
        for category in breakdown:
            count = breakdown[category]['count']
            if count > 0:
                breakdown[category]['success_rate'] /= count
                breakdown[category]['avg_execution_time'] /= count
        
        return dict(breakdown)

    def _calculate_trends(
        self, usage_records: List[TemplateUsage]
    ) -> Dict[str, List[Tuple[datetime, float]]]:
        """Calculate usage trends over time."""
        trends = {
            'success_rate': [],
            'execution_time': [],
            'usage_count': []
        }
        
        # Group by date
        daily_data = defaultdict(lambda: {
            'success_count': 0, 'total_count': 0, 'execution_times': []
        })
        
        for usage in usage_records:
            date_str = usage.timestamp.strftime("%Y-%m-%d")
            daily_data[date_str]['total_count'] += 1
            daily_data[date_str]['execution_times'].append(usage.execution_time)
            if usage.success:
                daily_data[date_str]['success_count'] += 1
        
        # Calculate daily metrics
        for date_str, data in sorted(daily_data.items()):
            date = datetime.strptime(date_str, "%Y-%m-%d")
            
            success_rate = data['success_count'] / data['total_count']
            avg_execution_time = sum(data['execution_times']) / len(data['execution_times'])
            
            trends['success_rate'].append((date, success_rate))
            trends['execution_time'].append((date, avg_execution_time))
            trends['usage_count'].append((date, data['total_count']))
        
        return trends

    def _generate_recommendations(
        self,
        usage_records: List[TemplateUsage],
        top_performers: List[TemplateMetrics],
        needs_optimization: List[TemplateMetrics],
    ) -> List[str]:
        """Generate optimization recommendations."""
        recommendations = []
        
        # Recommendations based on low-performing templates
        if needs_optimization:
            recommendations.append(
                f"Optimize {len(needs_optimization)} templates with high priority issues"
            )
            
            for metrics in needs_optimization[:3]:  # Top 3 issues
                if metrics.success_rate < 0.5:
                    recommendations.append(
                        f"Template '{metrics.template_name}' has low success rate "
                        f"({metrics.success_rate:.1%}) - consider revision"
                    )
        
        # Recommendations based on usage patterns
        if usage_records:
            avg_execution_time = sum(u.execution_time for u in usage_records) / len(usage_records)
            if avg_execution_time > 5.0:  # More than 5 seconds
                recommendations.append(
                    f"Average execution time is {avg_execution_time:.1f}s - "
                    "consider optimizing template complexity"
                )
        
        # Recommendations based on top performers
        if top_performers:
            recommendations.append(
                f"Study top {len(top_performers[:3])} performing templates for best practices"
            )
        
        # General recommendations
        if len(usage_records) < 10:
            recommendations.append("Collect more usage data for better insights")
        
        return recommendations

    def _save_report(self, report: PerformanceReport):
        """Save performance report to file."""
        try:
            reports = []
            if self.reports_file.exists():
                with open(self.reports_file, 'r', encoding='utf-8') as f:
                    reports = json.load(f)
            
            reports.append(report.to_dict())
            
            # Keep only last 10 reports
            if len(reports) > 10:
                reports = reports[-10:]
            
            with open(self.reports_file, 'w', encoding='utf-8') as f:
                json.dump(reports, f, indent=2, default=str)
                
        except Exception as e:
            logger.error(f"Failed to save performance report: {e}")

    def get_usage_statistics(self) -> Dict[str, Any]:
        """Get overall usage statistics."""
        if not self.usage_records:
            return {"error": "No usage data available"}
        
        total_usage = len(self.usage_records)
        success_count = sum(1 for u in self.usage_records if u.success)
        avg_execution_time = sum(u.execution_time for u in self.usage_records) / total_usage
        
        return {
            "total_usage": total_usage,
            "success_count": success_count,
            "error_count": total_usage - success_count,
            "success_rate": success_count / total_usage,
            "avg_execution_time": avg_execution_time,
            "unique_templates": len(set(u.template_id for u in self.usage_records)),
            "date_range": {
                "start": min(u.timestamp for u in self.usage_records).isoformat(),
                "end": max(u.timestamp for u in self.usage_records).isoformat()
            }
        }

    def export_metrics(self, output_file: str = None) -> str:
        """Export metrics to CSV file."""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.data_dir / f"template_metrics_export_{timestamp}.csv"
        
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'template_id', 'template_name', 'category', 'total_usage',
                    'success_count', 'error_count', 'success_rate', 'error_rate',
                    'avg_execution_time', 'avg_user_feedback', 'avg_output_quality',
                    'performance_score', 'optimization_priority', 'first_used', 'last_used'
                ]
                
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for metrics in self.template_metrics.values():
                    writer.writerow({
                        'template_id': metrics.template_id,
                        'template_name': metrics.template_name,
                        'category': metrics.category.value,
                        'total_usage': metrics.total_usage,
                        'success_count': metrics.success_count,
                        'error_count': metrics.error_count,
                        'success_rate': f"{metrics.success_rate:.3f}",
                        'error_rate': f"{metrics.error_rate:.3f}",
                        'avg_execution_time': f"{metrics.avg_execution_time:.3f}",
                        'avg_user_feedback': f"{metrics.avg_user_feedback:.3f}",
                        'avg_output_quality': f"{metrics.avg_output_quality:.3f}",
                        'performance_score': f"{metrics.performance_score:.3f}",
                        'optimization_priority': metrics.optimization_priority,
                        'first_used': metrics.first_used.isoformat() if metrics.first_used else '',
                        'last_used': metrics.last_used.isoformat() if metrics.last_used else ''
                    })
            
            logger.info(f"Exported metrics to {output_file}")
            return str(output_file)
            
        except Exception as e:
            logger.error(f"Failed to export metrics: {e}")
            raise


class TemplateDebugger:
    """Debugging utilities for template rendering."""
    
    def __init__(self, template_engine: PromptTemplateEngine):
        """Initialize the template debugger."""
        self.template_engine = template_engine

    def debug_template_rendering(self, template_id: str, variables: Dict) -> Dict:
        """Debug template rendering with detailed analysis."""
        try:
            # Get template
            template = self.template_engine.get_template(template_id)
            if not template:
                return {"error": f"Template {template_id} not found"}
            
            # Analyze variables
            required_vars = set(template.variables or [])
            provided_vars = set(variables.keys())
            missing_vars = required_vars - provided_vars
            extra_vars = provided_vars - required_vars
            
            # Test rendering
            try:
                rendered = self.template_engine.render_template(template_id, variables)
                render_success = True
                render_error = None
            except Exception as e:
                rendered = None
                render_success = False
                render_error = str(e)
            
            # Analyze template complexity
            content_length = len(template.content)
            variable_count = len(required_vars)
            jinja_blocks = template.content.count('{{') + template.content.count('{%')
            
            return {
                "template_id": template_id,
                "template_name": template.name,
                "template_type": template.type,
                "analysis": {
                    "content_length": content_length,
                    "variable_count": variable_count,
                    "jinja_blocks": jinja_blocks,
                    "complexity_score": content_length * variable_count * jinja_blocks
                },
                "variables": {
                    "required": list(required_vars),
                    "provided": list(provided_vars),
                    "missing": list(missing_vars),
                    "extra": list(extra_vars),
                    "coverage": len(provided_vars & required_vars) / len(required_vars) if required_vars else 1.0
                },
                "rendering": {
                    "success": render_success,
                    "error": render_error,
                    "rendered_content": rendered,
                    "rendered_length": len(rendered) if rendered else 0
                },
                "performance": {
                    "success_rate": template.success_rate,
                    "usage_count": template.usage_count,
                    "version": template.version
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to debug template: {e}")
            return {"error": str(e)}


class ContextualTemplateSender:
    """Sends templates with contextual information."""
    
    def __init__(self, template_engine: PromptTemplateEngine):
        """Initialize the contextual sender."""
        self.template_engine = template_engine

    def send_with_context(
        self, template_id: str, context: Dict, additional_vars: Dict = None
    ) -> str:
        """Send a template with contextual information."""
        try:
            # Merge context with additional variables
            variables = context.copy()
            if additional_vars:
                variables.update(additional_vars)
            
            # Add contextual metadata
            variables['_context_timestamp'] = datetime.now().isoformat()
            variables['_context_source'] = 'contextual_sender'
            
            # Render template
            return self.template_engine.render_template(template_id, variables)
            
        except Exception as e:
            logger.error(f"Failed to send contextual template: {e}")
            raise 