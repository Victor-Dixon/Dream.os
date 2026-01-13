"""Performance Analytics for Gaming System.
<!-- SSOT Domain: gaming -->

Comprehensive performance analytics and insights for the gaming ecosystem.

Author: Agent-6 - Gaming & Entertainment Specialist
V2 Compliance: SOLID principles, comprehensive metrics, predictive analytics
"""

import logging
import statistics
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class PerformanceAnalytics:
    """Performance analytics engine for gaming system metrics."""

    def __init__(self):
        """Initialize performance analytics."""
        self.metrics_history: Dict[str, List[Dict[str, Any]]] = {}
        self.baseline_metrics: Dict[str, Any] = {}
        self.performance_thresholds = {
            "response_time": {"good": 100, "warning": 200, "critical": 500},
            "engagement_rate": {"good": 80, "warning": 50, "critical": 20},
            "completion_rate": {"good": 90, "warning": 70, "critical": 50},
            "social_interaction_rate": {"good": 5, "warning": 2, "critical": 0.5},
            "error_rate": {"good": 1, "warning": 5, "critical": 10}
        }

    def record_metric(self, metric_name: str, value: Any, timestamp: Optional[datetime] = None,
                     metadata: Optional[Dict[str, Any]] = None):
        """Record a performance metric."""
        if timestamp is None:
            timestamp = datetime.now()

        metric_entry = {
            "timestamp": timestamp,
            "value": value,
            "metadata": metadata or {}
        }

        if metric_name not in self.metrics_history:
            self.metrics_history[metric_name] = []

        self.metrics_history[metric_name].append(metric_entry)

        # Keep only last 1000 entries per metric
        if len(self.metrics_history[metric_name]) > 1000:
            self.metrics_history[metric_name] = self.metrics_history[metric_name][-1000:]

    def get_metric_history(self, metric_name: str, hours: int = 24) -> List[Dict[str, Any]]:
        """Get metric history for the specified time period."""
        if metric_name not in self.metrics_history:
            return []

        cutoff_time = datetime.now() - timedelta(hours=hours)
        return [m for m in self.metrics_history[metric_name]
                if m["timestamp"] > cutoff_time]

    def calculate_metric_stats(self, metric_name: str, hours: int = 24) -> Dict[str, Any]:
        """Calculate statistical metrics for a given metric."""
        history = self.get_metric_history(metric_name, hours)
        if not history:
            return {"metric": metric_name, "status": "no_data"}

        values = [m["value"] for m in history if isinstance(m["value"], (int, float))]

        if not values:
            return {"metric": metric_name, "status": "no_numeric_data"}

        stats = {
            "metric": metric_name,
            "count": len(values),
            "current": values[-1] if values else None,
            "min": min(values),
            "max": max(values),
            "avg": statistics.mean(values),
            "median": statistics.median(values),
            "std_dev": statistics.stdev(values) if len(values) > 1 else 0,
            "time_range": f"{hours}h",
            "trend": self._calculate_trend(values)
        }

        # Add performance assessment
        stats.update(self._assess_performance(metric_name, stats))

        return stats

    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction from values."""
        if len(values) < 2:
            return "insufficient_data"

        # Compare first half vs second half
        midpoint = len(values) // 2
        first_half = values[:midpoint]
        second_half = values[midpoint:]

        if not first_half or not second_half:
            return "insufficient_data"

        first_avg = statistics.mean(first_half)
        second_avg = statistics.mean(second_half)

        diff_percent = ((second_avg - first_avg) / first_avg) * 100 if first_avg != 0 else 0

        if diff_percent > 5:
            return "increasing"
        elif diff_percent < -5:
            return "decreasing"
        else:
            return "stable"

    def _assess_performance(self, metric_name: str, stats: Dict[str, Any]) -> Dict[str, Any]:
        """Assess performance against thresholds."""
        if metric_name not in self.performance_thresholds:
            return {"assessment": "unknown", "status": "unknown"}

        thresholds = self.performance_thresholds[metric_name]
        current_value = stats.get("current")

        if current_value is None:
            return {"assessment": "no_data", "status": "unknown"}

        if metric_name in ["error_rate"]:  # Lower is better
            if current_value <= thresholds["good"]:
                status = "good"
            elif current_value <= thresholds["warning"]:
                status = "warning"
            else:
                status = "critical"
        else:  # Higher is better
            if current_value >= thresholds["good"]:
                status = "good"
            elif current_value >= thresholds["warning"]:
                status = "warning"
            else:
                status = "critical"

        assessment = {
            "assessment": status,
            "status": status,
            "thresholds": thresholds,
            "current_vs_threshold": self._compare_to_threshold(current_value, thresholds, metric_name)
        }

        return assessment

    def _compare_to_threshold(self, value: float, thresholds: Dict[str, float], metric_name: str) -> str:
        """Compare value to performance thresholds."""
        if metric_name in ["error_rate"]:  # Lower is better
            if value <= thresholds["good"]:
                return "excellent"
            elif value <= thresholds["warning"]:
                return "acceptable"
            else:
                return "needs_attention"
        else:  # Higher is better
            if value >= thresholds["good"]:
                return "excellent"
            elif value >= thresholds["warning"]:
                return "acceptable"
            else:
                return "needs_attention"

    def get_system_health_score(self) -> Dict[str, Any]:
        """Calculate overall system health score."""
        key_metrics = [
            "response_time",
            "engagement_rate",
            "completion_rate",
            "social_interaction_rate",
            "error_rate"
        ]

        health_components = {}
        total_score = 0
        valid_metrics = 0

        for metric in key_metrics:
            stats = self.calculate_metric_stats(metric, hours=1)  # Last hour
            if stats.get("status") != "no_data":
                assessment_score = {"good": 100, "warning": 50, "critical": 0}.get(
                    stats.get("assessment", "unknown"), 25
                )
                health_components[metric] = {
                    "score": assessment_score,
                    "assessment": stats.get("assessment", "unknown"),
                    "current": stats.get("current")
                }
                total_score += assessment_score
                valid_metrics += 1

        overall_score = total_score / valid_metrics if valid_metrics > 0 else 0

        health_status = "unknown"
        if overall_score >= 80:
            health_status = "excellent"
        elif overall_score >= 60:
            health_status = "good"
        elif overall_score >= 40:
            health_status = "warning"
        else:
            health_status = "critical"

        return {
            "overall_score": round(overall_score, 1),
            "health_status": health_status,
            "components": health_components,
            "valid_metrics": valid_metrics,
            "recommendations": self._generate_health_recommendations(health_components)
        }

    def _generate_health_recommendations(self, components: Dict[str, Any]) -> List[str]:
        """Generate health improvement recommendations."""
        recommendations = []

        for metric_name, data in components.items():
            assessment = data.get("assessment", "unknown")
            if assessment in ["critical", "warning"]:
                metric_display = metric_name.replace("_", " ").title()
                recommendations.append(f"Improve {metric_display} (currently {assessment})")

        if not recommendations:
            recommendations.append("System health is excellent - maintain current performance")

        # Add predictive recommendations
        trend_issues = self._analyze_trends_for_recommendations()
        recommendations.extend(trend_issues)

        return recommendations[:5]  # Limit to top 5

    def _analyze_trends_for_recommendations(self) -> List[str]:
        """Analyze trends to generate predictive recommendations."""
        recommendations = []

        # Check for declining trends
        declining_metrics = []
        for metric_name in self.metrics_history.keys():
            stats = self.calculate_metric_stats(metric_name, hours=6)
            if stats.get("trend") == "decreasing":
                declining_metrics.append(metric_name)

        if declining_metrics:
            recommendations.append(f"Address declining trends in: {', '.join(declining_metrics[:3])}")

        # Check for high variability
        variable_metrics = []
        for metric_name in self.metrics_history.keys():
            stats = self.calculate_metric_stats(metric_name, hours=24)
            std_dev = stats.get("std_dev", 0)
            avg = stats.get("avg", 1)
            if avg > 0 and (std_dev / avg) > 0.5:  # High variability
                variable_metrics.append(metric_name)

        if variable_metrics:
            recommendations.append(f"Stabilize performance for: {', '.join(variable_metrics[:3])}")

        return recommendations

    def generate_performance_report(self, hours: int = 24) -> Dict[str, Any]:
        """Generate comprehensive performance report."""
        report = {
            "generated_at": datetime.now().isoformat(),
            "time_range": f"{hours} hours",
            "system_health": self.get_system_health_score(),
            "metrics_summary": {},
            "insights": [],
            "recommendations": []
        }

        # Collect all available metrics
        all_metrics = list(self.metrics_history.keys())
        for metric in all_metrics:
            report["metrics_summary"][metric] = self.calculate_metric_stats(metric, hours)

        # Generate insights
        report["insights"] = self._generate_performance_insights(report["metrics_summary"])

        # Collect all recommendations
        all_recommendations = set()
        for metric_data in report["metrics_summary"].values():
            if "recommendations" in metric_data:
                all_recommendations.update(metric_data["recommendations"])

        health_recs = report["system_health"].get("recommendations", [])
        all_recommendations.update(health_recs)

        report["recommendations"] = list(all_recommendations)[:10]  # Top 10 unique recommendations

        return report

    def _generate_performance_insights(self, metrics_summary: Dict[str, Any]) -> List[str]:
        """Generate performance insights from metrics data."""
        insights = []

        # Analyze engagement patterns
        engagement = metrics_summary.get("engagement_rate", {})
        if engagement.get("trend") == "increasing":
            insights.append("User engagement is trending upward - excellent momentum")
        elif engagement.get("trend") == "decreasing":
            insights.append("User engagement is declining - investigate recent changes")

        # Analyze error patterns
        error_rate = metrics_summary.get("error_rate", {})
        if error_rate.get("assessment") == "good":
            insights.append("Error rates are within acceptable ranges")
        elif error_rate.get("assessment") == "critical":
            insights.append("High error rates detected - immediate attention required")

        # Analyze social interaction trends
        social_rate = metrics_summary.get("social_interaction_rate", {})
        if social_rate.get("trend") == "increasing":
            insights.append("Social interactions are increasing - community engagement growing")
        elif social_rate.get("current", 0) < 1:
            insights.append("Low social interaction rates - consider community building initiatives")

        # Performance vs expectations
        completion_rate = metrics_summary.get("completion_rate", {})
        if completion_rate.get("current", 0) > 85:
            insights.append("Task completion rates are excellent")
        elif completion_rate.get("current", 0) < 50:
            insights.append("Task completion rates need improvement")

        return insights

    def set_baseline(self, metric_name: str, baseline_value: Any):
        """Set baseline value for performance comparison."""
        self.baseline_metrics[metric_name] = {
            "value": baseline_value,
            "timestamp": datetime.now()
        }

    def get_baseline_comparison(self, metric_name: str) -> Dict[str, Any]:
        """Compare current performance to baseline."""
        if metric_name not in self.baseline_metrics:
            return {"status": "no_baseline"}

        baseline = self.baseline_metrics[metric_name]
        current_stats = self.calculate_metric_stats(metric_name, hours=1)

        if current_stats.get("status") == "no_data":
            return {"status": "no_current_data"}

        current_value = current_stats.get("current")
        baseline_value = baseline["value"]

        if not isinstance(current_value, (int, float)) or not isinstance(baseline_value, (int, float)):
            return {"status": "non_comparable"}

        difference = current_value - baseline_value
        percent_change = ((difference / baseline_value) * 100) if baseline_value != 0 else 0

        return {
            "baseline_value": baseline_value,
            "current_value": current_value,
            "difference": difference,
            "percent_change": round(percent_change, 2),
            "direction": "improvement" if percent_change > 0 else "decline" if percent_change < 0 else "unchanged",
            "baseline_timestamp": baseline["timestamp"].isoformat()
        }