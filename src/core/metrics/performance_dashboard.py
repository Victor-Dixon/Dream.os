#!/usr/bin/env python3
"""
Performance Dashboard - Real-Time Metrics Visualization
======================================================

Interactive dashboard for monitoring agent orchestration performance,
scalability metrics, and system health in real-time.

FEATURES:
- Real-time performance metrics
- Scalability trend analysis
- Load balancing visualization
- Cache performance monitoring
- Orchestration efficiency tracking
- Interactive web-based dashboard

Author: Agent-5 (Infrastructure Automation Specialist - Phase 2 Lead)
Date: 2026-01-13
Phase: Phase 2 - Scalability & Performance Optimization
"""

import asyncio
import json
import logging
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

from ..performance.performance_profiler import get_performance_profiler
from ..caching.intelligent_cache import get_orchestration_cache
from ..load_balancing.intelligent_load_balancer import get_load_balancer

logger = logging.getLogger(__name__)


@dataclass
class DashboardMetrics:
    """Comprehensive dashboard metrics."""
    timestamp: float

    # Performance metrics
    orchestration_throughput: float = 0.0  # operations per second
    avg_response_time: float = 0.0  # milliseconds
    error_rate: float = 0.0  # percentage
    memory_usage: float = 0.0  # MB
    cpu_usage: float = 0.0  # percentage

    # Scalability metrics
    active_agents: int = 0
    concurrent_operations: int = 0
    scalability_score: float = 0.0  # 0-100
    load_distribution_score: float = 0.0  # 0-100

    # Cache metrics
    cache_hit_rate: float = 0.0
    cache_size_mb: float = 0.0
    cache_entries: int = 0
    predictive_cache_hits: int = 0

    # Load balancing metrics
    agent_utilization_avg: float = 0.0
    task_distribution_balance: float = 0.0
    assignment_confidence_avg: float = 0.0

    # Historical trends
    trends_1h: Dict[str, float] = field(default_factory=dict)
    trends_24h: Dict[str, float] = field(default_factory=dict)

    alerts: List[str] = field(default_factory=list)


class PerformanceDashboard:
    """
    Real-time performance dashboard for agent orchestration.

    Provides comprehensive monitoring, alerting, and trend analysis.
    """

    def __init__(self, history_size: int = 1000):
        self.history_size = history_size
        self.metrics_history: deque = deque(maxlen=history_size)
        self.alerts_history: deque = deque(maxlen=500)

        # Component references
        self.performance_profiler = get_performance_profiler()
        self.cache = get_orchestration_cache()
        self.load_balancer = get_load_balancer()

        # Dashboard state
        self.is_monitoring = False
        self.monitoring_task: Optional[asyncio.Task] = None
        self.alert_thresholds = self._get_default_thresholds()

    def _get_default_thresholds(self) -> Dict[str, Tuple[float, str]]:
        """Get default alert thresholds."""
        return {
            'cpu_usage': (80.0, 'high'),
            'memory_usage': (85.0, 'high'),
            'error_rate': (5.0, 'high'),
            'response_time': (5000.0, 'high'),  # 5 seconds
            'cache_hit_rate': (50.0, 'low'),
            'scalability_score': (70.0, 'low'),
        }

    def start_monitoring(self, interval: float = 10.0):
        """Start real-time monitoring."""
        if self.is_monitoring:
            return

        self.is_monitoring = True
        self.monitoring_task = asyncio.create_task(self._monitoring_loop(interval))
        self.performance_profiler.start_monitoring(interval)
        logger.info("📊 Performance dashboard monitoring started")

    def stop_monitoring(self):
        """Stop monitoring."""
        self.is_monitoring = False
        if self.monitoring_task and not self.monitoring_task.done():
            self.monitoring_task.cancel()

        self.performance_profiler.stop_monitoring()
        logger.info("📊 Performance dashboard monitoring stopped")

    async def _monitoring_loop(self, interval: float):
        """Main monitoring loop."""
        while self.is_monitoring:
            try:
                # Collect metrics
                metrics = await self._collect_metrics()

                # Check alerts
                alerts = self._check_alerts(metrics)
                metrics.alerts = alerts

                # Store in history
                self.metrics_history.append(metrics)

                # Log alerts
                for alert in alerts:
                    logger.warning(f"🚨 {alert}")
                    self.alerts_history.append({
                        'timestamp': time.time(),
                        'alert': alert,
                        'metrics': metrics.__dict__
                    })

                await asyncio.sleep(interval)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Dashboard monitoring error: {e}")
                await asyncio.sleep(interval)

    async def _collect_metrics(self) -> DashboardMetrics:
        """Collect comprehensive metrics from all components."""
        timestamp = time.time()
        metrics = DashboardMetrics(timestamp=timestamp)

        try:
            # Performance metrics
            perf_report = self.performance_profiler.get_performance_report()
            if perf_report and 'performance_stats' in perf_report:
                stats = perf_report['performance_stats']
                metrics.avg_response_time = stats.get('avg_duration_ms', 0.0)
                metrics.orchestration_throughput = len(self.performance_profiler.metrics_history) / max(1, (time.time() - self.performance_profiler.metrics_history[0].start_time if self.performance_profiler.metrics_history else 1))

            # System resource metrics
            import psutil
            if psutil:
                metrics.cpu_usage = psutil.cpu_percent(interval=0.1)
                memory = psutil.virtual_memory()
                metrics.memory_usage = memory.used / (1024 * 1024)  # MB

            # Cache metrics
            cache_stats = self.cache.get_cache_stats()
            metrics.cache_hit_rate = cache_stats.get('hit_rate', 0.0) * 100
            metrics.cache_size_mb = cache_stats.get('total_size_mb', 0.0)
            metrics.cache_entries = cache_stats.get('total_entries', 0)

            # Load balancing metrics
            lb_stats = self.load_balancer.get_load_balancing_stats()
            metrics.active_agents = lb_stats.get('total_agents', 0)
            metrics.concurrent_operations = lb_stats.get('used_capacity', 0)

            if lb_stats.get('agent_stats'):
                utilizations = [agent['utilization'] for agent in lb_stats['agent_stats']]
                if utilizations:
                    metrics.agent_utilization_avg = sum(utilizations) / len(utilizations)

            # Scalability score (placeholder - would be calculated based on system capacity)
            metrics.scalability_score = min(100.0, metrics.active_agents * 10 + (100 - metrics.cpu_usage))

            # Calculate trends
            metrics.trends_1h = self._calculate_trends(3600)  # 1 hour
            metrics.trends_24h = self._calculate_trends(86400)  # 24 hours

        except Exception as e:
            logger.error(f"Error collecting metrics: {e}")

        return metrics

    def _check_alerts(self, metrics: DashboardMetrics) -> List[str]:
        """Check metrics against thresholds and generate alerts."""
        alerts = []

        # CPU usage alert
        if metrics.cpu_usage > self.alert_thresholds['cpu_usage'][0]:
            alerts.append(f"High CPU usage: {metrics.cpu_usage:.1f}% (threshold: {self.alert_thresholds['cpu_usage'][0]}%)")

        # Memory usage alert
        if metrics.memory_usage > 500:  # 500MB threshold for memory
            alerts.append(f"High memory usage: {metrics.memory_usage:.0f}MB")

        # Response time alert
        if metrics.avg_response_time > self.alert_thresholds['response_time'][0]:
            alerts.append(f"Slow response time: {metrics.avg_response_time:.0f}ms (threshold: {self.alert_thresholds['response_time'][0]}ms)")

        # Cache hit rate alert
        if metrics.cache_hit_rate < self.alert_thresholds['cache_hit_rate'][0]:
            alerts.append(f"Low cache hit rate: {metrics.cache_hit_rate:.1f}% (threshold: {self.alert_thresholds['cache_hit_rate'][0]}%)")

        # Scalability alert
        if metrics.scalability_score < self.alert_thresholds['scalability_score'][0]:
            alerts.append(f"Low scalability score: {metrics.scalability_score:.1f} (threshold: {self.alert_thresholds['scalability_score'][0]})")

        return alerts

    def _calculate_trends(self, time_window: float) -> Dict[str, float]:
        """Calculate metric trends over specified time window."""
        cutoff_time = time.time() - time_window
        recent_metrics = [m for m in self.metrics_history if m.timestamp >= cutoff_time]

        if len(recent_metrics) < 2:
            return {}

        trends = {}

        # CPU trend
        cpu_values = [m.cpu_usage for m in recent_metrics if m.cpu_usage > 0]
        if len(cpu_values) >= 2:
            trends['cpu_change'] = cpu_values[-1] - cpu_values[0]

        # Memory trend
        memory_values = [m.memory_usage for m in recent_metrics if m.memory_usage > 0]
        if len(memory_values) >= 2:
            trends['memory_change'] = memory_values[-1] - memory_values[0]

        # Response time trend
        response_times = [m.avg_response_time for m in recent_metrics if m.avg_response_time > 0]
        if len(response_times) >= 2:
            trends['response_time_change'] = response_times[-1] - response_times[0]

        # Throughput trend
        throughputs = [m.orchestration_throughput for m in recent_metrics if m.orchestration_throughput > 0]
        if len(throughputs) >= 2:
            trends['throughput_change'] = throughputs[-1] - throughputs[0]

        return trends

    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get complete dashboard data for display."""
        if not self.metrics_history:
            return {"error": "No metrics available. Start monitoring first."}

        latest_metrics = self.metrics_history[-1]
        recent_alerts = list(self.alerts_history)[-10:]  # Last 10 alerts

        # Performance summary
        performance_summary = {
            "status": "healthy" if not latest_metrics.alerts else "warning",
            "uptime_seconds": time.time() - (self.metrics_history[0].timestamp if self.metrics_history else time.time()),
            "total_operations": len(self.performance_profiler.metrics_history),
            "active_monitoring": self.is_monitoring
        }

        # Component health
        component_health = {
            "orchestration": {
                "status": "operational",
                "throughput": latest_metrics.orchestration_throughput,
                "avg_response_time": latest_metrics.avg_response_time
            },
            "cache": {
                "status": "operational" if latest_metrics.cache_entries > 0 else "idle",
                "hit_rate": latest_metrics.cache_hit_rate,
                "size_mb": latest_metrics.cache_size_mb,
                "entries": latest_metrics.cache_entries
            },
            "load_balancer": {
                "status": "operational",
                "active_agents": latest_metrics.active_agents,
                "utilization": latest_metrics.agent_utilization_avg,
                "balance_score": latest_metrics.load_distribution_score
            }
        }

        # Recommendations
        recommendations = self._generate_recommendations(latest_metrics)

        return {
            "timestamp": time.time(),
            "performance_summary": performance_summary,
            "current_metrics": latest_metrics.__dict__,
            "component_health": component_health,
            "recent_alerts": recent_alerts,
            "recommendations": recommendations,
            "trends": {
                "1_hour": latest_metrics.trends_1h,
                "24_hours": latest_metrics.trends_24h
            }
        }

    def _generate_recommendations(self, metrics: DashboardMetrics) -> List[str]:
        """Generate optimization recommendations based on current metrics."""
        recommendations = []

        # CPU recommendations
        if metrics.cpu_usage > 75:
            recommendations.append("Consider async processing for CPU-intensive operations")

        # Memory recommendations
        if metrics.memory_usage > 400:  # 400MB
            recommendations.append("Implement memory-efficient caching strategies")

        # Cache recommendations
        if metrics.cache_hit_rate < 60:
            recommendations.append("Optimize cache warming and TTL strategies")

        # Load balancing recommendations
        if metrics.agent_utilization_avg > 0.8:
            recommendations.append("Consider horizontal scaling or load redistribution")

        if metrics.load_distribution_score < 0.7:
            recommendations.append("Improve task distribution balance across agents")

        # Performance recommendations
        if metrics.avg_response_time > 2000:  # 2 seconds
            recommendations.append("Profile and optimize slow operations")

        if metrics.orchestration_throughput < 1.0:
            recommendations.append("Consider concurrent processing improvements")

        return recommendations or ["System performance is optimal"]

    def export_metrics_report(self, filepath: str, time_window: Optional[float] = None) -> bool:
        """Export comprehensive metrics report to file."""
        try:
            # Get metrics for specified time window
            if time_window:
                cutoff = time.time() - time_window
                relevant_metrics = [m for m in self.metrics_history if m.timestamp >= cutoff]
            else:
                relevant_metrics = list(self.metrics_history)

            report = {
                "export_timestamp": time.time(),
                "time_window_seconds": time_window,
                "total_metrics": len(relevant_metrics),
                "dashboard_data": self.get_dashboard_data(),
                "raw_metrics": [m.__dict__ for m in relevant_metrics[-100:]],  # Last 100 for detail
                "alerts_summary": self._summarize_alerts(time_window)
            }

            with open(filepath, 'w') as f:
                json.dump(report, f, indent=2, default=str)

            logger.info(f"✅ Metrics report exported to {filepath}")
            return True

        except Exception as e:
            logger.error(f"Failed to export metrics report: {e}")
            return False

    def _summarize_alerts(self, time_window: Optional[float] = None) -> Dict[str, Any]:
        """Summarize alerts for reporting."""
        if time_window:
            cutoff = time.time() - time_window
            relevant_alerts = [a for a in self.alerts_history if a['timestamp'] >= cutoff]
        else:
            relevant_alerts = list(self.alerts_history)

        # Group alerts by type
        alert_types = defaultdict(int)
        for alert in relevant_alerts:
            alert_type = alert['alert'].split(':')[0] if ':' in alert['alert'] else 'other'
            alert_types[alert_type] += 1

        return {
            "total_alerts": len(relevant_alerts),
            "alert_types": dict(alert_types),
            "most_recent": relevant_alerts[-1] if relevant_alerts else None,
            "time_window": time_window
        }


# Global dashboard instance
_performance_dashboard = None

def get_performance_dashboard() -> PerformanceDashboard:
    """Get the global performance dashboard instance."""
    global _performance_dashboard
    if _performance_dashboard is None:
        _performance_dashboard = PerformanceDashboard()
    return _performance_dashboard

def start_dashboard_monitoring(interval: float = 10.0):
    """Start the global performance dashboard monitoring."""
    dashboard = get_performance_dashboard()
    dashboard.start_monitoring(interval)

def stop_dashboard_monitoring():
    """Stop the global performance dashboard monitoring."""
    dashboard = get_performance_dashboard()
    dashboard.stop_monitoring()

def get_dashboard_data() -> Dict[str, Any]:
    """Get current dashboard data."""
    dashboard = get_performance_dashboard()
    return dashboard.get_dashboard_data()