"""
Content Analytics Module - Unified Content Analysis
=================================================

This module consolidates content analytics functionality including:
- Content quality scoring and analysis
- Content performance metrics
- Content optimization recommendations
- Content type classification
- Content trend analysis
"""

import json
import logging
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import statistics
import re
from dataclasses_json import dataclass_json
from collections import defaultdict

logger = logging.getLogger(__name__)


class ContentType(Enum):
    """Content types for analysis."""
    GENERAL = "general"
    SOCIAL = "social"
    BLOG = "blog"
    QUEST = "quest"
    TECHNICAL = "technical"
    CREATIVE = "creative"
    EDUCATIONAL = "educational"
    MARKETING = "marketing"


class QualityDimension(Enum):
    """Quality dimensions for content analysis."""
    READABILITY = "readability"
    ENGAGEMENT = "engagement"
    RELEVANCE = "relevance"
    ORIGINALITY = "originality"
    ACCURACY = "accuracy"
    COMPLETENESS = "completeness"
    STRUCTURE = "structure"
    TONE = "tone"


class QualityLevel(Enum):
    """Quality levels for content classification."""
    EXCELLENT = "excellent"
    GOOD = "good"
    AVERAGE = "average"
    POOR = "poor"
    UNACCEPTABLE = "unacceptable"


@dataclass_json
@dataclass
class ContentQualityMetrics:
    """Content quality metrics."""
    content_id: str
    content_type: ContentType
    overall_score: float
    dimension_scores: Dict[QualityDimension, float]
    quality_level: QualityLevel
    word_count: int
    sentence_count: int
    paragraph_count: int
    readability_score: float
    engagement_score: float
    relevance_score: float
    originality_score: float
    accuracy_score: float
    completeness_score: float
    structure_score: float
    tone_score: float
    timestamp: datetime
    metadata: Dict[str, Any]


@dataclass_json
@dataclass
class ContentPerformanceMetrics:
    """Content performance metrics."""
    content_id: str
    content_type: ContentType
    views: int
    engagement_rate: float
    time_on_content: float
    bounce_rate: float
    conversion_rate: float
    social_shares: int
    comments: int
    likes: int
    timestamp: datetime
    metadata: Dict[str, Any]


@dataclass_json
@dataclass
class ContentAnalyticsResult:
    """Combined content analytics result."""
    content_id: str
    content_type: ContentType
    quality_metrics: ContentQualityMetrics
    performance_metrics: Optional[ContentPerformanceMetrics]
    combined_score: float
    optimization_priority: str
    recommendations: List[str]
    insights: List[str]
    timestamp: datetime
    metadata: Dict[str, Any]


class ContentAnalyticsModule:
    """
    Unified content analytics module.
    
    This module provides comprehensive content analysis including:
    - Quality scoring across multiple dimensions
    - Performance tracking and metrics
    - Content optimization recommendations
    - Trend analysis and insights
    """
    
    def __init__(self, data_dir: str = "data/content_analytics"):
        """Initialize the content analytics module."""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Data storage
        self.quality_metrics_file = self.data_dir / "quality_metrics.jsonl"
        self.performance_metrics_file = self.data_dir / "performance_metrics.jsonl"
        self.analytics_results_file = self.data_dir / "analytics_results.jsonl"
        
        # Load existing data
        self.quality_metrics: List[ContentQualityMetrics] = []
        self.performance_metrics: List[ContentPerformanceMetrics] = []
        self.analytics_results: List[ContentAnalyticsResult] = []
        self._load_existing_data()
        
        logger.info(f"Content Analytics Module initialized at {self.data_dir}")
    
    def _load_existing_data(self):
        """Load existing analytics data."""
        # Load quality metrics
        if self.quality_metrics_file.exists():
            with open(self.quality_metrics_file, 'r') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        metric = ContentQualityMetrics.from_dict(data)
                        metric.timestamp = datetime.fromisoformat(data['timestamp'])
                        self.quality_metrics.append(metric)
        
        # Load performance metrics
        if self.performance_metrics_file.exists():
            with open(self.performance_metrics_file, 'r') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        metric = ContentPerformanceMetrics.from_dict(data)
                        metric.timestamp = datetime.fromisoformat(data['timestamp'])
                        self.performance_metrics.append(metric)
        
        # Load analytics results
        if self.analytics_results_file.exists():
            with open(self.analytics_results_file, 'r') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        result = ContentAnalyticsResult.from_dict(data)
                        result.timestamp = datetime.fromisoformat(data['timestamp'])
                        self.analytics_results.append(result)
        
        logger.info(f"Loaded {len(self.quality_metrics)} quality metrics, {len(self.performance_metrics)} performance metrics, {len(self.analytics_results)} analytics results")
    
    def analyze_content(self, content: str, content_type: ContentType = ContentType.GENERAL, 
                       content_id: str = None, metadata: Dict[str, Any] = None) -> ContentAnalyticsResult:
        """Analyze content and generate comprehensive analytics result."""
        if content_id is None:
            content_id = f"content_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if metadata is None:
            metadata = {}
        
        # Generate quality metrics
        quality_metrics = self._generate_quality_metrics(content, content_type, content_id, metadata)
        
        # Generate performance metrics (simulated for now)
        performance_metrics = self._generate_performance_metrics(content_id, content_type, metadata)
        
        # Calculate combined score
        combined_score = self._calculate_combined_score(quality_metrics, performance_metrics)
        
        # Determine optimization priority
        optimization_priority = self._determine_optimization_priority(quality_metrics, performance_metrics)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(quality_metrics, performance_metrics)
        
        # Generate insights
        insights = self._generate_insights(quality_metrics, performance_metrics)
        
        # Create analytics result
        result = ContentAnalyticsResult(
            content_id=content_id,
            content_type=content_type,
            quality_metrics=quality_metrics,
            performance_metrics=performance_metrics,
            combined_score=combined_score,
            optimization_priority=optimization_priority,
            recommendations=recommendations,
            insights=insights,
            timestamp=datetime.now(),
            metadata=metadata
        )
        
        # Save result
        self._save_analytics_result(result)
        
        return result
    
    def _generate_quality_metrics(self, content: str, content_type: ContentType, 
                                 content_id: str, metadata: Dict[str, Any]) -> ContentQualityMetrics:
        """Generate quality metrics for content."""
        # Basic text statistics
        words = content.split()
        sentences = re.split(r'[.!?]+', content)
        paragraphs = content.split('\n\n')
        
        word_count = len(words)
        sentence_count = len([s for s in sentences if s.strip()])
        paragraph_count = len([p for p in paragraphs if p.strip()])
        
        # Calculate dimension scores
        dimension_scores = {
            QualityDimension.READABILITY: self._calculate_readability_score(content, word_count, sentence_count),
            QualityDimension.ENGAGEMENT: self._calculate_engagement_score(content, content_type),
            QualityDimension.RELEVANCE: self._calculate_relevance_score(content, content_type),
            QualityDimension.ORIGINALITY: self._calculate_originality_score(content),
            QualityDimension.ACCURACY: self._calculate_accuracy_score(content),
            QualityDimension.COMPLETENESS: self._calculate_completeness_score(content),
            QualityDimension.STRUCTURE: self._calculate_structure_score(content, paragraph_count),
            QualityDimension.TONE: self._calculate_tone_score(content, content_type)
        }
        
        # Calculate overall score
        overall_score = statistics.mean(dimension_scores.values())
        
        # Determine quality level
        quality_level = self._determine_quality_level(overall_score)
        
        # Create quality metrics
        metrics = ContentQualityMetrics(
            content_id=content_id,
            content_type=content_type,
            overall_score=overall_score,
            dimension_scores=dimension_scores,
            quality_level=quality_level,
            word_count=word_count,
            sentence_count=sentence_count,
            paragraph_count=paragraph_count,
            readability_score=dimension_scores[QualityDimension.READABILITY],
            engagement_score=dimension_scores[QualityDimension.ENGAGEMENT],
            relevance_score=dimension_scores[QualityDimension.RELEVANCE],
            originality_score=dimension_scores[QualityDimension.ORIGINALITY],
            accuracy_score=dimension_scores[QualityDimension.ACCURACY],
            completeness_score=dimension_scores[QualityDimension.COMPLETENESS],
            structure_score=dimension_scores[QualityDimension.STRUCTURE],
            tone_score=dimension_scores[QualityDimension.TONE],
            timestamp=datetime.now(),
            metadata=metadata
        )
        
        # Save quality metrics
        self._save_quality_metrics(metrics)
        
        return metrics
    
    def _calculate_readability_score(self, content: str, word_count: int, sentence_count: int) -> float:
        """Calculate readability score using Flesch Reading Ease."""
        if sentence_count == 0 or word_count == 0:
            return 0.0
        
        # Count syllables (simplified)
        syllables = sum(1 for char in content.lower() if char in 'aeiou')
        
        # Flesch Reading Ease formula
        flesch_score = 206.835 - (1.015 * (word_count / sentence_count)) - (84.6 * (syllables / word_count))
        
        # Normalize to 0-1 scale
        return max(0.0, min(1.0, flesch_score / 100.0))
    
    def _calculate_engagement_score(self, content: str, content_type: ContentType) -> float:
        """Calculate engagement score based on content characteristics."""
        score = 0.5  # Base score
        
        # Factors that increase engagement
        if '?' in content:  # Questions
            score += 0.1
        if '!' in content:  # Exclamations
            score += 0.05
        if len(content.split()) > 100:  # Substantial content
            score += 0.1
        if any(word in content.lower() for word in ['you', 'your', 'we', 'our']):  # Personal pronouns
            score += 0.1
        
        # Content type adjustments
        if content_type == ContentType.SOCIAL:
            score += 0.1
        elif content_type == ContentType.CREATIVE:
            score += 0.05
        
        return min(1.0, score)
    
    def _calculate_relevance_score(self, content: str, content_type: ContentType) -> float:
        """Calculate relevance score based on content type alignment."""
        # This would typically use NLP to determine topic relevance
        # For now, return a base score with some variation
        base_score = 0.7
        
        # Add some variation based on content characteristics
        if content_type == ContentType.TECHNICAL and any(word in content.lower() for word in ['code', 'function', 'algorithm']):
            base_score += 0.2
        elif content_type == ContentType.CREATIVE and any(word in content.lower() for word in ['story', 'creative', 'imagine']):
            base_score += 0.2
        
        return min(1.0, base_score)
    
    def _calculate_originality_score(self, content: str) -> float:
        """Calculate originality score."""
        # This would typically use plagiarism detection or uniqueness analysis
        # For now, return a base score with some variation
        base_score = 0.8
        
        # Add variation based on content length and complexity
        if len(content.split()) > 200:
            base_score += 0.1
        
        return min(1.0, base_score)
    
    def _calculate_accuracy_score(self, content: str) -> float:
        """Calculate accuracy score."""
        # This would typically use fact-checking or verification
        # For now, return a base score
        return 0.75
    
    def _calculate_completeness_score(self, content: str) -> float:
        """Calculate completeness score."""
        # Check for common completeness indicators
        score = 0.5  # Base score
        
        if len(content.split()) > 50:  # Substantial content
            score += 0.2
        if content.count('.') > 3:  # Multiple sentences
            score += 0.1
        if '\n\n' in content:  # Multiple paragraphs
            score += 0.1
        if any(word in content.lower() for word in ['conclusion', 'summary', 'finally']):
            score += 0.1
        
        return min(1.0, score)
    
    def _calculate_structure_score(self, content: str, paragraph_count: int) -> float:
        """Calculate structure score."""
        score = 0.5  # Base score
        
        if paragraph_count > 1:
            score += 0.2
        if any(word in content.lower() for word in ['first', 'second', 'third', 'finally']):
            score += 0.1
        if any(word in content.lower() for word in ['introduction', 'conclusion']):
            score += 0.1
        if len(content.split()) > 100:
            score += 0.1
        
        return min(1.0, score)
    
    def _calculate_tone_score(self, content: str, content_type: ContentType) -> float:
        """Calculate tone appropriateness score."""
        score = 0.7  # Base score
        
        # Adjust based on content type
        if content_type == ContentType.TECHNICAL:
            if any(word in content.lower() for word in ['technical', 'function', 'algorithm']):
                score += 0.2
        elif content_type == ContentType.CREATIVE:
            if any(word in content.lower() for word in ['creative', 'imagine', 'story']):
                score += 0.2
        
        return min(1.0, score)
    
    def _determine_quality_level(self, overall_score: float) -> QualityLevel:
        """Determine quality level based on overall score."""
        if overall_score >= 0.9:
            return QualityLevel.EXCELLENT
        elif overall_score >= 0.8:
            return QualityLevel.GOOD
        elif overall_score >= 0.6:
            return QualityLevel.AVERAGE
        elif overall_score >= 0.4:
            return QualityLevel.POOR
        else:
            return QualityLevel.UNACCEPTABLE
    
    def _generate_performance_metrics(self, content_id: str, content_type: ContentType, 
                                    metadata: Dict[str, Any]) -> ContentPerformanceMetrics:
        """Generate performance metrics for content."""
        # This would typically come from actual performance data
        # For now, generate simulated metrics
        import random
        
        metrics = ContentPerformanceMetrics(
            content_id=content_id,
            content_type=content_type,
            views=random.randint(10, 1000),
            engagement_rate=random.uniform(0.1, 0.8),
            time_on_content=random.uniform(30, 300),
            bounce_rate=random.uniform(0.1, 0.6),
            conversion_rate=random.uniform(0.01, 0.1),
            social_shares=random.randint(0, 50),
            comments=random.randint(0, 20),
            likes=random.randint(0, 100),
            timestamp=datetime.now(),
            metadata=metadata
        )
        
        # Save performance metrics
        self._save_performance_metrics(metrics)
        
        return metrics
    
    def _calculate_combined_score(self, quality_metrics: ContentQualityMetrics, 
                                performance_metrics: Optional[ContentPerformanceMetrics]) -> float:
        """Calculate combined score from quality and performance metrics."""
        quality_score = quality_metrics.overall_score
        
        if performance_metrics:
            # Normalize performance metrics to 0-1 scale
            performance_score = (
                performance_metrics.engagement_rate * 0.4 +
                (1 - performance_metrics.bounce_rate) * 0.3 +
                min(performance_metrics.conversion_rate * 10, 1.0) * 0.3
            )
            
            # Combine scores (70% quality, 30% performance)
            combined_score = quality_score * 0.7 + performance_score * 0.3
        else:
            combined_score = quality_score
        
        return combined_score
    
    def _determine_optimization_priority(self, quality_metrics: ContentQualityMetrics,
                                       performance_metrics: Optional[ContentPerformanceMetrics]) -> str:
        """Determine optimization priority."""
        if quality_metrics.overall_score < 0.6:
            return "high"
        elif quality_metrics.overall_score < 0.8:
            return "medium"
        else:
            return "low"
    
    def _generate_recommendations(self, quality_metrics: ContentQualityMetrics,
                                performance_metrics: Optional[ContentPerformanceMetrics]) -> List[str]:
        """Generate optimization recommendations."""
        recommendations = []
        
        # Quality-based recommendations
        if quality_metrics.readability_score < 0.6:
            recommendations.append("Improve readability by using shorter sentences and simpler language.")
        
        if quality_metrics.engagement_score < 0.6:
            recommendations.append("Increase engagement by adding questions, examples, or interactive elements.")
        
        if quality_metrics.structure_score < 0.6:
            recommendations.append("Improve structure by adding clear headings and organizing content into logical sections.")
        
        if quality_metrics.completeness_score < 0.6:
            recommendations.append("Add more detail and ensure all key points are covered.")
        
        # Performance-based recommendations
        if performance_metrics and performance_metrics.engagement_rate < 0.3:
            recommendations.append("Low engagement detected. Consider adding more interactive elements or improving content relevance.")
        
        if performance_metrics and performance_metrics.bounce_rate > 0.7:
            recommendations.append("High bounce rate. Improve content introduction and ensure it meets user expectations.")
        
        if not recommendations:
            recommendations.append("Content is performing well. Continue monitoring and consider A/B testing for further optimization.")
        
        return recommendations
    
    def _generate_insights(self, quality_metrics: ContentQualityMetrics,
                          performance_metrics: Optional[ContentPerformanceMetrics]) -> List[str]:
        """Generate insights about the content."""
        insights = []
        
        # Quality insights
        if quality_metrics.overall_score > 0.9:
            insights.append("Content quality is excellent across all dimensions.")
        elif quality_metrics.overall_score > 0.8:
            insights.append("Content quality is good with room for minor improvements.")
        
        # Dimension-specific insights
        best_dimension = max(quality_metrics.dimension_scores.items(), key=lambda x: x[1])
        worst_dimension = min(quality_metrics.dimension_scores.items(), key=lambda x: x[1])
        
        insights.append(f"Strongest quality dimension: {best_dimension[0].value} ({best_dimension[1]:.2f})")
        insights.append(f"Area for improvement: {worst_dimension[0].value} ({worst_dimension[1]:.2f})")
        
        # Performance insights
        if performance_metrics:
            if performance_metrics.engagement_rate > 0.6:
                insights.append("Content shows high user engagement.")
            if performance_metrics.conversion_rate > 0.05:
                insights.append("Content has good conversion performance.")
        
        return insights
    
    def _save_quality_metrics(self, metrics: ContentQualityMetrics):
        """Save quality metrics to file."""
        with open(self.quality_metrics_file, 'a') as f:
            f.write(json.dumps(asdict(metrics)) + '\n')
        self.quality_metrics.append(metrics)
    
    def _save_performance_metrics(self, metrics: ContentPerformanceMetrics):
        """Save performance metrics to file."""
        with open(self.performance_metrics_file, 'a') as f:
            f.write(json.dumps(asdict(metrics)) + '\n')
        self.performance_metrics.append(metrics)
    
    def _save_analytics_result(self, result: ContentAnalyticsResult):
        """Save analytics result to file."""
        with open(self.analytics_results_file, 'a') as f:
            f.write(json.dumps(asdict(result)) + '\n')
        self.analytics_results.append(result)
    
    def get_insights(self, time_period: str = "30d") -> List[Dict[str, Any]]:
        """Get insights for the specified time period."""
        cutoff_date = datetime.now() - timedelta(days=int(time_period[:-1]))
        
        recent_results = [
            result for result in self.analytics_results
            if result.timestamp >= cutoff_date
        ]
        
        insights = []
        for result in recent_results:
            insights.extend([
                {
                    "insight_id": f"content_{result.content_id}_{i}",
                    "insight_type": "content_quality",
                    "title": insight,
                    "description": f"Content quality insight for {result.content_id}",
                    "confidence": 0.8,
                    "impact_score": 0.6,
                    "recommendations": result.recommendations,
                    "metadata": result.metadata,
                    "timestamp": result.timestamp,
                    "source_data": {"content_id": result.content_id},
                    "analytics_type": "content_quality",
                    "tags": [result.content_type.value]
                }
                for i, insight in enumerate(result.insights)
            ])
        
        return insights
    
    def get_metrics(self, time_period: str = "30d") -> List[Dict[str, Any]]:
        """Get metrics for the specified time period."""
        cutoff_date = datetime.now() - timedelta(days=int(time_period[:-1]))
        
        recent_metrics = [
            metric for metric in self.quality_metrics
            if metric.timestamp >= cutoff_date
        ]
        
        return [
            {
                "metric_id": metric.content_id,
                "metric_name": "content_quality_score",
                "value": metric.overall_score,
                "unit": "score",
                "timestamp": metric.timestamp,
                "metadata": metric.metadata,
                "analytics_type": "content_quality",
                "confidence": 0.9,
                "trend": "stable"
            }
            for metric in recent_metrics
        ]
    
    def get_summary(self, time_period: str = "30d") -> Dict[str, Any]:
        """Get summary for the specified time period."""
        cutoff_date = datetime.now() - timedelta(days=int(time_period[:-1]))
        
        recent_results = [
            result for result in self.analytics_results
            if result.timestamp >= cutoff_date
        ]
        
        if not recent_results:
            return {"total_content": 0, "avg_quality_score": 0.0}
        
        return {
            "total_content": len(recent_results),
            "avg_quality_score": statistics.mean(r.quality_metrics.overall_score for r in recent_results),
            "avg_combined_score": statistics.mean(r.combined_score for r in recent_results),
            "quality_distribution": self._get_quality_distribution(recent_results),
            "content_type_distribution": self._get_content_type_distribution(recent_results)
        }
    
    def _get_quality_distribution(self, results: List[ContentAnalyticsResult]) -> Dict[str, int]:
        """Get distribution of quality levels."""
        distribution = defaultdict(int)
        for result in results:
            distribution[result.quality_metrics.quality_level.value] += 1
        return dict(distribution)
    
    def _get_content_type_distribution(self, results: List[ContentAnalyticsResult]) -> Dict[str, int]:
        """Get distribution of content types."""
        distribution = defaultdict(int)
        for result in results:
            distribution[result.content_type.value] += 1
        return dict(distribution) 