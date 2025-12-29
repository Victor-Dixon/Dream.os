#!/usr/bin/env python3
<!-- SSOT Domain: core -->
"""
Stress Test Metrics Analyzer
=============================

Advanced analysis and insights generation for stress test metrics:
- Latency pattern analysis (p50, p95, p99)
- Bottleneck identification
- Optimization opportunities
- Performance recommendations
- Dashboard visualization data

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-11-29
License: MIT
"""

import json
import logging
import statistics
from pathlib import Path
from typing import Any, Optional

from .stress_test_metrics import StressTestAnalyzer

logger = logging.getLogger(__name__)


class StressTestMetricsAnalyzer:
    """Advanced analyzer for stress test metrics and insights generation."""

    def __init__(self, dashboard_data: Optional[dict[str, Any]] = None):
        """Initialize metrics analyzer."""
        self.dashboard_data = dashboard_data or {}
        self.logger = logger
        self.base_analyzer = StressTestAnalyzer()

    def load_dashboard_from_file(self, file_path: Path) -> dict[str, Any]:
        """Load dashboard JSON from file."""
        try:
            with open(file_path, "r") as f:
                self.dashboard_data = json.load(f)
            self.logger.info(f"Loaded dashboard from {file_path}")
            return self.dashboard_data
        except Exception as e:
            self.logger.error(f"Error loading dashboard: {e}")
            return {}

    def analyze_latency_patterns(self) -> dict[str, Any]:
        """Analyze latency patterns and trends."""
        try:
            overall = self.dashboard_data.get("overall_metrics", {})
            latency = overall.get("latency_percentiles", {})

            patterns = {
                "p50": latency.get("p50", 0),
                "p95": latency.get("p95", 0),
                "p99": latency.get("p99", 0),
                "p95_to_p50_ratio": (
                    latency.get("p95", 0) / latency.get("p50", 1)
                    if latency.get("p50", 0) > 0
                    else 0
                ),
                "p99_to_p50_ratio": (
                    latency.get("p99", 0) / latency.get("p50", 1)
                    if latency.get("p50", 0) > 0
                    else 0
                ),
                "tail_latency_severity": self._assess_tail_latency(latency),
                "latency_distribution": self._analyze_latency_distribution(),
            }

            # Identify latency anomalies
            patterns["anomalies"] = self._detect_latency_anomalies(latency)
            patterns["trends"] = self._analyze_latency_trends()

            return patterns
        except Exception as e:
            self.logger.error(f"Error analyzing latency patterns: {e}")
            return {}

    def identify_bottlenecks(self) -> list[dict[str, Any]]:
        """Identify performance bottlenecks."""
        try:
            bottlenecks = []

            # Analyze overall metrics
            overall = self.dashboard_data.get("overall_metrics", {})
            latency = overall.get("latency_percentiles", {})

            # High latency bottleneck
            if latency.get("p99", 0) > 500:  # 500ms threshold
                bottlenecks.append({
                    "type": "high_latency",
                    "severity": "high" if latency.get("p99", 0) > 1000 else "medium",
                    "metric": "p99_latency",
                    "value": latency.get("p99", 0),
                    "threshold": 500,
                    "description": f"P99 latency ({latency.get('p99', 0):.2f}ms) exceeds threshold",
                })

            # Low throughput bottleneck
            throughput = overall.get("throughput_msg_per_sec", 0)
            if throughput < 50:  # 50 msg/sec threshold
                bottlenecks.append({
                    "type": "low_throughput",
                    "severity": "high" if throughput < 20 else "medium",
                    "metric": "throughput",
                    "value": throughput,
                    "threshold": 50,
                    "description": f"Throughput ({throughput:.2f} msg/sec) below threshold",
                })

            # High failure rate bottleneck
            failure_rate = overall.get("failure_rate_percent", 0)
            if failure_rate > 1.0:  # 1% threshold
                bottlenecks.append({
                    "type": "high_failure_rate",
                    "severity": "high" if failure_rate > 5.0 else "medium",
                    "metric": "failure_rate",
                    "value": failure_rate,
                    "threshold": 1.0,
                    "description": f"Failure rate ({failure_rate:.2f}%) exceeds threshold",
                })

            # Queue depth bottleneck
            queue = overall.get("queue_depth", {})
            max_queue = queue.get("max", 0)
            if max_queue > 100:  # 100 items threshold
                bottlenecks.append({
                    "type": "queue_depth",
                    "severity": "high" if max_queue > 500 else "medium",
                    "metric": "queue_depth_max",
                    "value": max_queue,
                    "threshold": 100,
                    "description": f"Max queue depth ({max_queue}) exceeds threshold",
                })

            # Per-agent bottlenecks
            per_agent = self.dashboard_data.get("per_agent_metrics", {})
            for agent_id, agent_metrics in per_agent.items():
                agent_latency = agent_metrics.get("latency_percentiles", {})
                if agent_latency.get("p99", 0) > 500:
                    bottlenecks.append({
                        "type": "agent_latency",
                        "severity": "medium",
                        "agent": agent_id,
                        "metric": "p99_latency",
                        "value": agent_latency.get("p99", 0),
                        "description": f"{agent_id}: High latency detected",
                    })

            return bottlenecks
        except Exception as e:
            self.logger.error(f"Error identifying bottlenecks: {e}")
            return []

    def generate_optimization_opportunities(self) -> list[dict[str, Any]]:
        """Generate optimization opportunities based on analysis."""
        try:
            opportunities = []
            bottlenecks = self.identify_bottlenecks()

            for bottleneck in bottlenecks:
                if bottleneck["type"] == "high_latency":
                    opportunities.append({
                        "category": "latency_optimization",
                        "priority": "high" if bottleneck["severity"] == "high" else "medium",
                        "recommendation": "Optimize message processing pipeline",
                        "actions": [
                            "Review message queue processing logic",
                            "Consider batch processing for high-volume scenarios",
                            "Evaluate database query optimization",
                            "Check for unnecessary serialization/deserialization",
                        ],
                        "expected_impact": "20-40% latency reduction",
                    })

                elif bottleneck["type"] == "low_throughput":
                    opportunities.append({
                        "category": "throughput_optimization",
                        "priority": "high" if bottleneck["severity"] == "high" else "medium",
                        "recommendation": "Increase message processing throughput",
                        "actions": [
                            "Implement parallel processing",
                            "Optimize I/O operations",
                            "Consider connection pooling",
                            "Review resource allocation",
                        ],
                        "expected_impact": "50-100% throughput improvement",
                    })

                elif bottleneck["type"] == "high_failure_rate":
                    opportunities.append({
                        "category": "reliability_optimization",
                        "priority": "high",
                        "recommendation": "Reduce failure rate",
                        "actions": [
                            "Implement retry mechanisms with exponential backoff",
                            "Add circuit breaker pattern",
                            "Improve error handling and recovery",
                            "Monitor and fix root causes",
                        ],
                        "expected_impact": "Failure rate reduction to <1%",
                    })

                elif bottleneck["type"] == "queue_depth":
                    opportunities.append({
                        "category": "queue_optimization",
                        "priority": "medium",
                        "recommendation": "Optimize queue management",
                        "actions": [
                            "Increase consumer processing rate",
                            "Implement queue prioritization",
                            "Add queue depth alerts",
                            "Consider horizontal scaling",
                        ],
                        "expected_impact": "Queue depth reduction by 50%",
                    })

            return opportunities
        except Exception as e:
            self.logger.error(f"Error generating opportunities: {e}")
            return []

    def generate_performance_recommendations(self) -> dict[str, Any]:
        """Generate comprehensive performance recommendations."""
        try:
            latency_patterns = self.analyze_latency_patterns()
            bottlenecks = self.identify_bottlenecks()
            opportunities = self.generate_optimization_opportunities()

            recommendations = {
                "summary": {
                    "total_bottlenecks": len(bottlenecks),
                    "high_severity": sum(1 for b in bottlenecks if b["severity"] == "high"),
                    "medium_severity": sum(1 for b in bottlenecks if b["severity"] == "medium"),
                    "optimization_opportunities": len(opportunities),
                },
                "critical_actions": [
                    opp for opp in opportunities if opp["priority"] == "high"
                ],
                "recommended_actions": [
                    opp for opp in opportunities if opp["priority"] == "medium"
                ],
                "latency_insights": {
                    "current_state": {
                        "p50": latency_patterns.get("p50", 0),
                        "p95": latency_patterns.get("p95", 0),
                        "p99": latency_patterns.get("p99", 0),
                    },
                    "tail_latency_concern": (
                        latency_patterns.get("tail_latency_severity", "none") != "none"
                    ),
                    "recommendations": self._generate_latency_recommendations(latency_patterns),
                },
                "bottlenecks": bottlenecks,
                "optimization_opportunities": opportunities,
            }

            return recommendations
        except Exception as e:
            self.logger.error(f"Error generating recommendations: {e}")
            return {}

    def generate_dashboard_visualization_data(self) -> dict[str, Any]:
        """Generate data structure for dashboard visualization."""
        try:
            visualization_data = {
                "charts": {
                    "latency_distribution": self._generate_latency_chart_data(),
                    "throughput_timeline": self._generate_throughput_chart_data(),
                    "failure_rate_timeline": self._generate_failure_rate_chart_data(),
                    "queue_depth_timeline": self._generate_queue_depth_chart_data(),
                    "per_agent_comparison": self._generate_agent_comparison_data(),
                    "message_type_analysis": self._generate_message_type_analysis(),
                },
                "summary_metrics": self.dashboard_data.get("overall_metrics", {}),
                "key_insights": self._generate_key_insights(),
            }

            return visualization_data
        except Exception as e:
            self.logger.error(f"Error generating visualization data: {e}")
            return {}

    def _assess_tail_latency(self, latency: dict[str, Any]) -> str:
        """Assess tail latency severity."""
        p50 = latency.get("p50", 0)
        p99 = latency.get("p99", 0)

        if p50 == 0:
            return "none"

        ratio = p99 / p50
        if ratio > 10:
            return "severe"
        elif ratio > 5:
            return "high"
        elif ratio > 3:
            return "medium"
        else:
            return "low"

    def _analyze_latency_distribution(self) -> dict[str, Any]:
        """Analyze latency distribution characteristics."""
        overall = self.dashboard_data.get("overall_metrics", {})
        latency = overall.get("latency_percentiles", {})

        return {
            "spread": latency.get("p99", 0) - latency.get("p50", 0),
            "consistency": "high" if (latency.get("p95", 0) - latency.get("p50", 0)) < 50 else "low",
        }

    def _detect_latency_anomalies(self, latency: dict[str, Any]) -> list[str]:
        """Detect latency anomalies."""
        anomalies = []

        if latency.get("p99", 0) > 1000:
            anomalies.append("Extremely high tail latency (>1s)")
        if latency.get("p95", 0) > 500:
            anomalies.append("High 95th percentile latency (>500ms)")

        return anomalies

    def _analyze_latency_trends(self) -> dict[str, Any]:
        """Analyze latency trends over time."""
        # Placeholder - would analyze time-series data if available
        return {"trend": "stable", "notes": "Time-series analysis requires historical data"}

    def _generate_latency_recommendations(self, patterns: dict[str, Any]) -> list[str]:
        """Generate latency-specific recommendations."""
        recommendations = []

        if patterns.get("tail_latency_severity") in ["high", "severe"]:
            recommendations.append("Focus on optimizing tail latency - investigate slow operations")
        if patterns.get("p95_to_p50_ratio", 0) > 5:
            recommendations.append("High variance in latency - consider load balancing improvements")

        return recommendations

    def _generate_latency_chart_data(self) -> dict[str, Any]:
        """Generate latency distribution chart data."""
        overall = self.dashboard_data.get("overall_metrics", {})
        latency = overall.get("latency_percentiles", {})

        return {
            "p50": latency.get("p50", 0),
            "p95": latency.get("p95", 0),
            "p99": latency.get("p99", 0),
            "labels": ["p50", "p95", "p99"],
        }

    def _generate_throughput_chart_data(self) -> dict[str, Any]:
        """Generate throughput timeline chart data."""
        overall = self.dashboard_data.get("overall_metrics", {})
        return {
            "current": overall.get("throughput_msg_per_sec", 0),
            "target": 100,  # Example target
        }

    def _generate_failure_rate_chart_data(self) -> dict[str, Any]:
        """Generate failure rate chart data."""
        overall = self.dashboard_data.get("overall_metrics", {})
        return {"current": overall.get("failure_rate_percent", 0), "target": 1.0}

    def _generate_queue_depth_chart_data(self) -> dict[str, Any]:
        """Generate queue depth chart data."""
        overall = self.dashboard_data.get("overall_metrics", {})
        queue = overall.get("queue_depth", {})
        return {
            "max": queue.get("max", 0),
            "avg": queue.get("avg", 0),
            "current": queue.get("current", 0),
        }

    def _generate_agent_comparison_data(self) -> dict[str, Any]:
        """Generate per-agent comparison data."""
        per_agent = self.dashboard_data.get("per_agent_metrics", {})
        return {
            "agents": list(per_agent.keys()),
            "metrics": {
                agent: {
                    "latency_p99": metrics.get("latency_percentiles", {}).get("p99", 0),
                    "failure_rate": metrics.get("failure_rate_percent", 0),
                }
                for agent, metrics in per_agent.items()
            },
        }

    def _generate_message_type_analysis(self) -> dict[str, Any]:
        """Generate message type analysis data."""
        per_type = self.dashboard_data.get("per_message_type_metrics", {})
        return per_type

    def _generate_key_insights(self) -> list[str]:
        """Generate key insights summary."""
        insights = []
        bottlenecks = self.identify_bottlenecks()

        if any(b["severity"] == "high" for b in bottlenecks):
            insights.append("High severity bottlenecks detected - immediate action required")

        overall = self.dashboard_data.get("overall_metrics", {})
        if overall.get("failure_rate_percent", 0) > 1.0:
            insights.append("Failure rate exceeds acceptable threshold")

        latency = overall.get("latency_percentiles", {})
        if latency.get("p99", 0) > 500:
            insights.append("Tail latency requires optimization")

        return insights


__all__ = ["StressTestMetricsAnalyzer"]

