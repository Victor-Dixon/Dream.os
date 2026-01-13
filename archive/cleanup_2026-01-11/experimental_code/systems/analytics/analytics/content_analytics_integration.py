"""
Content Analytics Integration System

This module provides unified integration for template performance analytics
and content quality scoring, offering comprehensive content insights and optimization.
"""

import json
import logging
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses_json import dataclass_json

from dreamscape.core.templates.template_system import (
    TemplatePerformanceAnalytics,
    TemplateUsage,
    TemplateMetrics,
    PerformanceReport,
    TemplateCategory,
)
from ..content.content_quality_scoring import ContentQualityScorer
from ..content.content_generation_system import ContentQualityReport, ContentType, QualityDimension
from dreamscape.core.utils.common_utils import parse_date_safe

logger = logging.getLogger(__name__)


@dataclass_json
@dataclass
class ContentAnalyticsResult:
    """Combined result from template performance and quality scoring"""
    content_id: str
    content_type: ContentType
    template_id: str
    timestamp: datetime
    quality_report: ContentQualityReport
    template_metrics: Optional[TemplateMetrics]
    combined_score: float
    optimization_priority: str
    recommendations: List[str]
    metadata: Dict[str, Any]


@dataclass_json
@dataclass
class ContentAnalyticsSummary:
    """Summary of content analytics across multiple pieces of content"""
    summary_id: str
    generated_at: datetime
    time_period: str
    total_content_analyzed: int
    avg_quality_score: float
    avg_template_performance: float
    top_quality_content: List[ContentAnalyticsResult]
    needs_optimization: List[ContentAnalyticsResult]
    category_performance: Dict[ContentType, Dict[str, float]]
    template_performance: Dict[str, float]
    trends: Dict[str, List[Tuple[datetime, float]]]
    insights: List[str]
    recommendations: List[str]


class ContentAnalyticsIntegration:
    """Unified content analytics system combining performance and quality analysis"""
    
    def __init__(self, data_dir: str = "data/content_analytics"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize subsystems
        self.template_analytics = TemplatePerformanceAnalytics(
            str(self.data_dir / "template_analytics")
        )
        self.quality_scorer = ContentQualityScorer()
        
        # Results storage
        self.results_file = self.data_dir / "analytics_results.jsonl"
        self.summaries_file = self.data_dir / "analytics_summaries.json"
        
        self.analytics_results: List[ContentAnalyticsResult] = []
        self._load_existing_results()
    
    def _load_existing_results(self):
        """Load existing analytics results"""
        try:
            if self.results_file.exists():
                with open(self.results_file, 'r') as f:
                    for line in f:
                        if line.strip():
                            result_data = json.loads(line)
                            # Use parse_date_safe and default if invalid
                            ts = result_data.get('timestamp')
                            parsed_ts = parse_date_safe(ts)
                            if not parsed_ts:
                                parsed_ts = datetime.fromisoformat('2025-07-08T00:00:00')
                            result_data['timestamp'] = parsed_ts
                            qr_ts = result_data.get('quality_report', {}).get('timestamp')
                            parsed_qr_ts = parse_date_safe(qr_ts)
                            if not parsed_qr_ts:
                                parsed_qr_ts = datetime.fromisoformat('2025-07-08T00:00:00')
                            if 'quality_report' in result_data:
                                result_data['quality_report']['timestamp'] = parsed_qr_ts
                            result = ContentAnalyticsResult.from_dict(result_data)
                            self.analytics_results.append(result)
        except Exception as e:
            logger.error(f"Error loading analytics results: {e}")
    
    def analyze_content(self, content: str, content_type: ContentType, 
                       template_id: str, content_id: str = None, 
                       metadata: Dict[str, Any] = None) -> ContentAnalyticsResult:
        """Perform comprehensive content analysis"""
        import time
        start_time = time.time()
        
        if content_id is None:
            content_id = f"content_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if metadata is None:
            metadata = {}
        
        try:
            # Perform quality scoring
            quality_report = self.quality_scorer.score_content(
                content, content_type, content_id, metadata
            )
            
            # Get template metrics (if available)
            template_metrics = self.template_analytics.get_template_metrics(template_id)
            
            # Calculate combined score
            combined_score = self._calculate_combined_score(quality_report, template_metrics)
            
            # Determine optimization priority
            optimization_priority = self._determine_optimization_priority(
                quality_report, template_metrics
            )
            
            # Generate unified recommendations
            recommendations = self._generate_unified_recommendations(
                quality_report, template_metrics
            )
            
            # Create result
            result = ContentAnalyticsResult(
                content_id=content_id,
                content_type=content_type,
                template_id=template_id,
                timestamp=datetime.now(),
                quality_report=quality_report,
                template_metrics=template_metrics,
                combined_score=combined_score,
                optimization_priority=optimization_priority,
                recommendations=recommendations,
                metadata=metadata
            )
            
            # Save result
            self._save_result(result)
            self.analytics_results.append(result)
            
            processing_time = time.time() - start_time
            logger.info(f"Content analysis completed for {content_id} in {processing_time:.2f}s")
            
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing content: {e}")
            raise
    
    def _calculate_combined_score(self, quality_report: ContentQualityReport, 
                                template_metrics: Optional[TemplateMetrics]) -> float:
        """Calculate combined score from quality and performance"""
        quality_weight = 0.7
        performance_weight = 0.3
        
        quality_score = quality_report.overall_score
        
        if template_metrics:
            performance_score = template_metrics.performance_score
        else:
            performance_score = 50.0  # Default score for unknown templates
        
        combined_score = (quality_score * quality_weight) + (performance_score * performance_weight)
        return min(100.0, max(0.0, combined_score))
    
    def _determine_optimization_priority(self, quality_report: ContentQualityReport,
                                       template_metrics: Optional[TemplateMetrics]) -> str:
        """Determine overall optimization priority"""
        # Quality-based priority
        if quality_report.overall_score < 50:
            quality_priority = "high"
        elif quality_report.overall_score < 70:
            quality_priority = "medium"
        else:
            quality_priority = "low"
        
        # Performance-based priority
        if template_metrics:
            performance_priority = template_metrics.optimization_priority
        else:
            performance_priority = "medium"  # Unknown template
        
        # Combine priorities
        if quality_priority == "high" or performance_priority == "high":
            return "high"
        elif quality_priority == "medium" or performance_priority == "medium":
            return "medium"
        else:
            return "low"
    
    def _generate_unified_recommendations(self, quality_report: ContentQualityReport,
                                        template_metrics: Optional[TemplateMetrics]) -> List[str]:
        """Generate unified recommendations from both systems"""
        recommendations = []
        
        # Quality-based recommendations
        recommendations.extend(quality_report.recommendations[:3])
        
        # Performance-based recommendations
        if template_metrics and template_metrics.optimization_priority == "high":
            if template_metrics.error_rate > 0.2:
                recommendations.append(f"Template '{template_metrics.template_name}' has high error rate - investigate issues")
            if template_metrics.avg_execution_time > 3.0:
                recommendations.append(f"Template '{template_metrics.template_name}' is slow - optimize performance")
        
        return list(set(recommendations))[:5]  # Remove duplicates, limit to 5
    
    def _save_result(self, result: ContentAnalyticsResult):
        """Save analytics result to file"""
        try:
            result_dict = result.to_dict()
            result_dict['timestamp'] = result.timestamp.isoformat()
            result_dict['quality_report']['timestamp'] = result.quality_report.timestamp.isoformat()
            # Convert enums to strings for JSON serialization
            result_dict['content_type'] = result.content_type.value
            result_dict['quality_report']['content_type'] = result.quality_report.content_type.value
            result_dict['quality_report']['overall_level'] = result.quality_report.overall_level.value
            
            # Convert dimension scores
            dimension_scores = {}
            for dimension, score in result.quality_report.dimension_scores.items():
                dimension_scores[dimension.value] = {
                    'dimension': score.dimension.value,
                    'score': score.score,
                    'level': score.level.value,
                    'reasoning': score.reasoning,
                    'suggestions': score.suggestions,
                    'confidence': score.confidence
                }
            result_dict['quality_report']['dimension_scores'] = dimension_scores
            
            with open(self.results_file, 'a') as f:
                f.write(json.dumps(result_dict) + '\n')
                
        except Exception as e:
            logger.error(f"Error saving analytics result: {e}")
    
    def generate_analytics_summary(self, time_period: str = "30d") -> ContentAnalyticsSummary:
        """Generate comprehensive analytics summary"""
        try:
            # Calculate time range
            end_date = datetime.now()
            if time_period == "7d":
                start_date = end_date - timedelta(days=7)
            elif time_period == "30d":
                start_date = end_date - timedelta(days=30)
            elif time_period == "90d":
                start_date = end_date - timedelta(days=90)
            else:
                start_date = datetime.min
            
            # Filter results for time period
            period_results = [r for r in self.analytics_results 
                            if start_date <= r.timestamp <= end_date]
            
            if not period_results:
                return self._create_empty_summary(time_period)
            
            # Calculate overall metrics
            total_content = len(period_results)
            avg_quality_score = sum(r.quality_report.overall_score for r in period_results) / total_content
            avg_template_performance = sum(r.template_metrics.performance_score for r in period_results 
                                         if r.template_metrics) / total_content
            
            # Get top performers and optimization candidates
            top_quality = sorted(period_results, key=lambda x: x.combined_score, reverse=True)[:10]
            needs_optimization = [r for r in period_results if r.optimization_priority == "high"]
            
            # Calculate category performance
            category_performance = self._calculate_category_performance(period_results)
            
            # Calculate template performance
            template_performance = self._calculate_template_performance(period_results)
            
            # Calculate trends
            trends = self._calculate_analytics_trends(period_results)
            
            # Generate insights and recommendations
            insights = self._generate_insights(period_results, top_quality, needs_optimization)
            recommendations = self._generate_summary_recommendations(
                period_results, top_quality, needs_optimization
            )
            
            summary = ContentAnalyticsSummary(
                summary_id=f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                generated_at=datetime.now(),
                time_period=time_period,
                total_content_analyzed=total_content,
                avg_quality_score=avg_quality_score,
                avg_template_performance=avg_template_performance,
                top_quality_content=top_quality,
                needs_optimization=needs_optimization,
                category_performance=category_performance,
                template_performance=template_performance,
                trends=trends,
                insights=insights,
                recommendations=recommendations
            )
            
            # Save summary
            self._save_summary(summary)
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating analytics summary: {e}")
            raise
    
    def _create_empty_summary(self, time_period: str) -> ContentAnalyticsSummary:
        """Create empty summary when no data is available"""
        return ContentAnalyticsSummary(
            summary_id=f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            generated_at=datetime.now(),
            time_period=time_period,
            total_content_analyzed=0,
            avg_quality_score=0.0,
            avg_template_performance=0.0,
            top_quality_content=[],
            needs_optimization=[],
            category_performance={},
            template_performance={},
            trends={},
            insights=["No content analyzed in the specified time period"],
            recommendations=["Start analyzing content to generate insights"]
        )
    
    def _calculate_category_performance(self, results: List[ContentAnalyticsResult]) -> Dict[ContentType, Dict[str, float]]:
        """Calculate performance metrics by content category"""
        category_data = {}
        
        for content_type in ContentType:
            type_results = [r for r in results if r.content_type == content_type]
            
            if not type_results:
                category_data[content_type] = {
                    'count': 0,
                    'avg_quality': 0.0,
                    'avg_performance': 0.0,
                    'avg_combined': 0.0
                }
                continue
            
            avg_quality = sum(r.quality_report.overall_score for r in type_results) / len(type_results)
            avg_performance = sum(r.template_metrics.performance_score for r in type_results 
                                if r.template_metrics) / len(type_results)
            avg_combined = sum(r.combined_score for r in type_results) / len(type_results)
            
            category_data[content_type] = {
                'count': len(type_results),
                'avg_quality': avg_quality,
                'avg_performance': avg_performance,
                'avg_combined': avg_combined
            }
        
        return category_data
    
    def _calculate_template_performance(self, results: List[ContentAnalyticsResult]) -> Dict[str, float]:
        """Calculate performance metrics by template"""
        template_data = {}
        
        for result in results:
            template_id = result.template_id
            if template_id not in template_data:
                template_data[template_id] = []
            
            template_data[template_id].append(result.combined_score)
        
        # Calculate averages
        template_performance = {}
        for template_id, scores in template_data.items():
            template_performance[template_id] = sum(scores) / len(scores)
        
        return template_performance
    
    def _calculate_analytics_trends(self, results: List[ContentAnalyticsResult]) -> Dict[str, List[Tuple[datetime, float]]]:
        """Calculate trends over time"""
        trends = {
            'quality_score': [],
            'combined_score': [],
            'content_volume': []
        }
        
        if not results:
            return trends
        
        # Group by day
        daily_data = {}
        for result in results:
            date_key = result.timestamp.date()
            if date_key not in daily_data:
                daily_data[date_key] = []
            daily_data[date_key].append(result)
        
        # Calculate daily metrics
        for date, day_results in sorted(daily_data.items()):
            avg_quality = sum(r.quality_report.overall_score for r in day_results) / len(day_results)
            avg_combined = sum(r.combined_score for r in day_results) / len(day_results)
            
            trends['quality_score'].append((datetime.combine(date, datetime.min.time()), avg_quality))
            trends['combined_score'].append((datetime.combine(date, datetime.min.time()), avg_combined))
            trends['content_volume'].append((datetime.combine(date, datetime.min.time()), len(day_results)))
        
        return trends
    
    def _generate_insights(self, results: List[ContentAnalyticsResult], 
                          top_quality: List[ContentAnalyticsResult],
                          needs_optimization: List[ContentAnalyticsResult]) -> List[str]:
        """Generate insights from analytics data"""
        insights = []
        
        # Quality insights
        avg_quality = sum(r.quality_report.overall_score for r in results) / len(results)
        if avg_quality < 70:
            insights.append(f"Overall content quality is below target ({avg_quality:.1f}/100)")
        elif avg_quality > 85:
            insights.append(f"Excellent overall content quality ({avg_quality:.1f}/100)")
        
        # Performance insights
        if needs_optimization:
            insights.append(f"{len(needs_optimization)} pieces of content need optimization")
        
        # Category insights
        category_counts = {}
        for result in results:
            category = result.content_type
            category_counts[category] = category_counts.get(category, 0) + 1
        
        most_common_category = max(category_counts.items(), key=lambda x: x[1])
        insights.append(f"Most analyzed content type: {most_common_category[0].value} ({most_common_category[1]} items)")
        
        # Template insights
        template_counts = {}
        for result in results:
            template_id = result.template_id
            template_counts[template_id] = template_counts.get(template_id, 0) + 1
        
        if template_counts:
            most_used_template = max(template_counts.items(), key=lambda x: x[1])
            insights.append(f"Most used template: {most_used_template[0]} ({most_used_template[1]} times)")
        
        return insights
    
    def _generate_summary_recommendations(self, results: List[ContentAnalyticsResult],
                                        top_quality: List[ContentAnalyticsResult],
                                        needs_optimization: List[ContentAnalyticsResult]) -> List[str]:
        """Generate summary-level recommendations"""
        recommendations = []
        
        # Quality-based recommendations
        avg_quality = sum(r.quality_report.overall_score for r in results) / len(results)
        if avg_quality < 70:
            recommendations.append("Focus on improving content quality across all types")
        
        # Optimization recommendations
        if needs_optimization:
            recommendations.append(f"Prioritize optimization of {len(needs_optimization)} low-performing content pieces")
        
        # Category recommendations
        category_quality = {}
        for result in results:
            category = result.content_type
            if category not in category_quality:
                category_quality[category] = []
            category_quality[category].append(result.quality_report.overall_score)
        
        for category, scores in category_quality.items():
            avg_score = sum(scores) / len(scores)
            if avg_score < 65:
                recommendations.append(f"Improve {category.value} content quality (current avg: {avg_score:.1f})")
        
        # Template recommendations
        template_quality = {}
        for result in results:
            template_id = result.template_id
            if template_id not in template_quality:
                template_quality[template_id] = []
            template_quality[template_id].append(result.combined_score)
        
        for template_id, scores in template_quality.items():
            avg_score = sum(scores) / len(scores)
            if avg_score < 60:
                recommendations.append(f"Optimize template '{template_id}' (current avg: {avg_score:.1f})")
        
        return recommendations[:5]  # Limit to top 5
    
    def _save_summary(self, summary: ContentAnalyticsSummary):
        """Save analytics summary"""
        try:
            summaries = []
            if self.summaries_file.exists():
                with open(self.summaries_file, 'r') as f:
                    summaries = json.load(f)
            
            summary_dict = summary.to_dict()
            summary_dict['generated_at'] = summary.generated_at.isoformat()
            # Convert enum keys to strings for JSON serialization
            category_performance = {}
            for category, data in summary.category_performance.items():
                category_performance[category.value] = data
            summary_dict['category_performance'] = category_performance
            summaries.append(summary_dict)
            
            # Keep only last 10 summaries
            summaries = summaries[-10:]
            
            with open(self.summaries_file, 'w') as f:
                json.dump(summaries, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error saving analytics summary: {e}")
    
    def get_content_analytics(self, content_id: str) -> Optional[ContentAnalyticsResult]:
        """Get analytics for a specific content piece"""
        for result in self.analytics_results:
            if result.content_id == content_id:
                return result
        return None
    
    def get_template_analytics(self, template_id: str) -> List[ContentAnalyticsResult]:
        """Get all analytics for a specific template"""
        return [r for r in self.analytics_results if r.template_id == template_id]
    
    def get_category_analytics(self, content_type: ContentType) -> List[ContentAnalyticsResult]:
        """Get all analytics for a specific content type"""
        return [r for r in self.analytics_results if r.content_type == content_type]
    
    def export_analytics(self, output_file: str = None) -> str:
        """Export analytics data to JSON file"""
        if output_file is None:
            output_file = self.data_dir / f"content_analytics_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            # Convert results to JSON-serializable format
            serializable_results = []
            for result in self.analytics_results:
                result_dict = result.to_dict()
                result_dict['content_type'] = result.content_type.value
                result_dict['quality_report']['content_type'] = result.quality_report.content_type.value
                result_dict['quality_report']['overall_level'] = result.quality_report.overall_level.value
                
                # Convert template metrics if present
                if result.template_metrics:
                    result_dict['template_metrics']['category'] = result.template_metrics.category.value
                    # Convert datetime fields in template metrics
                    if 'last_used' in result_dict['template_metrics']:
                        result_dict['template_metrics']['last_used'] = result.template_metrics.last_used.isoformat()
                    if 'first_used' in result_dict['template_metrics']:
                        result_dict['template_metrics']['first_used'] = result.template_metrics.first_used.isoformat()
                    # Convert usage trend
                    if 'usage_trend' in result_dict['template_metrics']:
                        result_dict['template_metrics']['usage_trend'] = [
                            (d.isoformat(), c) for d, c in result.template_metrics.usage_trend
                        ]
                
                # Convert dimension scores
                dimension_scores = {}
                for dimension, score in result.quality_report.dimension_scores.items():
                    dimension_scores[dimension.value] = {
                        'dimension': score.dimension.value,
                        'score': score.score,
                        'level': score.level.value,
                        'reasoning': score.reasoning,
                        'suggestions': score.suggestions,
                        'confidence': score.confidence
                    }
                result_dict['quality_report']['dimension_scores'] = dimension_scores
                serializable_results.append(result_dict)
            
            export_data = {
                'export_date': datetime.now().isoformat(),
                'total_results': len(self.analytics_results),
                'analytics_results': serializable_results
            }
            
            # Convert datetime objects to strings in the results
            for result in serializable_results:
                if isinstance(result['timestamp'], datetime):
                    result['timestamp'] = result['timestamp'].isoformat()
                if isinstance(result['quality_report']['timestamp'], datetime):
                    result['quality_report']['timestamp'] = result['quality_report']['timestamp'].isoformat()
            
            with open(output_file, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            logger.info(f"Exported content analytics to {output_file}")
            return str(output_file)
            
        except Exception as e:
            logger.error(f"Error exporting content analytics: {e}")
            raise
    
    def get_analytics_statistics(self) -> Dict[str, Any]:
        """Get overall analytics statistics"""
        if not self.analytics_results:
            return {
                'total_analyzed': 0,
                'avg_quality_score': 0.0,
                'avg_combined_score': 0.0,
                'optimization_needed': 0
            }
        
        total_analyzed = len(self.analytics_results)
        avg_quality_score = sum(r.quality_report.overall_score for r in self.analytics_results) / total_analyzed
        avg_combined_score = sum(r.combined_score for r in self.analytics_results) / total_analyzed
        optimization_needed = sum(1 for r in self.analytics_results if r.optimization_priority == "high")
        
        return {
            'total_analyzed': total_analyzed,
            'avg_quality_score': avg_quality_score,
            'avg_combined_score': avg_combined_score,
            'optimization_needed': optimization_needed,
            'date_range': {
                'earliest': min(r.timestamp for r in self.analytics_results).isoformat(),
                'latest': max(r.timestamp for r in self.analytics_results).isoformat()
            }
        }
    
    def get_analytics_summary(self) -> Dict[str, Any]:
        """Get a summary of analytics data for GUI display"""
        try:
            # Get basic statistics
            stats = self.get_analytics_statistics()
            
            # Get recent results for recommendations
            recent_results = sorted(
                self.analytics_results, 
                key=lambda x: x.timestamp, 
                reverse=True
            )[:10]
            
            # Generate recommendations
            recommendations = []
            if recent_results:
                # Quality-based recommendations
                low_quality = [r for r in recent_results if r.quality_report.overall_score < 60]
                if low_quality:
                    recommendations.append({
                        "type": "quality_improvement",
                        "priority": "high",
                        "description": f"Improve content quality for {len(low_quality)} items",
                        "impact": "high",
                        "effort": "medium"
                    })
                
                # Performance-based recommendations
                high_priority = [r for r in recent_results if r.optimization_priority == "high"]
                if high_priority:
                    recommendations.append({
                        "type": "optimization",
                        "priority": "high", 
                        "description": f"Optimize {len(high_priority)} high-priority items",
                        "impact": "high",
                        "effort": "medium"
                    })
                
                # Template performance recommendations
                template_performance = {}
                for result in recent_results:
                    template_id = result.template_id
                    if template_id not in template_performance:
                        template_performance[template_id] = []
                    template_performance[template_id].append(result.combined_score)
                
                for template_id, scores in template_performance.items():
                    avg_score = sum(scores) / len(scores)
                    if avg_score < 70:
                        recommendations.append({
                            "type": "template_optimization",
                            "priority": "medium",
                            "description": f"Optimize template '{template_id}' (avg score: {avg_score:.1f})",
                            "impact": "medium",
                            "effort": "low"
                        })
            
            # Category performance
            category_performance = {}
            for result in recent_results:
                content_type = result.content_type.value
                if content_type not in category_performance:
                    category_performance[content_type] = []
                category_performance[content_type].append(result.quality_report.overall_score)
            
            for content_type, scores in category_performance.items():
                category_performance[content_type] = sum(scores) / len(scores)
            
            return {
                "statistics": stats,
                "recommendations": recommendations,
                "category_performance": category_performance,
                "recent_activity": len(recent_results),
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating analytics summary: {e}")
            return {
                "statistics": {
                    "total_analyzed": 0,
                    "avg_quality_score": 0.0,
                    "avg_combined_score": 0.0,
                    "optimization_needed": 0
                },
                "recommendations": [],
                "category_performance": {},
                "recent_activity": 0,
                "last_updated": datetime.now().isoformat(),
                "error": str(e)
            } 