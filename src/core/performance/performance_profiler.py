#!/usr/bin/env python3
"""
Performance Profiler - Advanced Analytics & Optimization
=======================================================

Comprehensive performance profiling system for agent orchestration and coordination.
Provides detailed metrics, bottleneck detection, and optimization recommendations.

FEATURES:
- Real-time performance monitoring
- Bottleneck detection and analysis
- Memory usage tracking
- Execution time profiling
- Scalability metrics
- Performance trend analysis
- Optimization recommendations

Author: Agent-5 (Infrastructure Automation Specialist - Phase 2 Lead)
Date: 2026-01-13
Phase: Phase 2 - Scalability & Performance Optimization
"""

import asyncio
import functools
import logging
import psutil
import threading
import time
from collections import defaultdict, deque
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable, Union
import tracemalloc

logger = logging.getLogger(__name__)


@dataclass
class PerformanceMetrics:
    """Comprehensive performance metrics collection."""
    operation_name: str
    start_time: float
    end_time: Optional[float] = None
    duration: Optional[float] = None
    memory_start: Optional[int] = None
    memory_end: Optional[int] = None
    memory_delta: Optional[int] = None
    cpu_percent: Optional[float] = None
    thread_count: Optional[int] = None
    context_switches: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)

    @property
    def memory_delta_mb(self) -> Optional[float]:
        """Memory delta in MB."""
        return self.memory_delta / (1024 * 1024) if self.memory_delta else None

    @property
    def duration_ms(self) -> Optional[float]:
        """Duration in milliseconds."""
        return self.duration * 1000 if self.duration else None


@dataclass
class PerformanceSnapshot:
    """System performance snapshot."""
    timestamp: float
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    memory_available_mb: float
    disk_usage_percent: float
    network_connections: int
    thread_count: int
    active_operations: int


class PerformanceProfiler:
    """
    Advanced performance profiler with analytics and optimization capabilities.

    Features:
    - Real-time monitoring and alerting
    - Historical trend analysis
    - Bottleneck detection
    - Memory leak detection
    - Scalability analysis
    - Performance recommendations
    """

    def __init__(self, max_history: int = 1000, enable_tracing: bool = True):
        self.max_history = max_history
        self.enable_tracing = enable_tracing

        # Metrics storage
        self.metrics_history: deque = deque(maxlen=max_history)
        self.active_operations: Dict[str, PerformanceMetrics] = {}
        self.snapshots: deque = deque(maxlen=100)

        # Performance thresholds
        self.thresholds = {
            'max_operation_time': 30.0,  # seconds
            'max_memory_delta': 100 * 1024 * 1024,  # 100MB
            'cpu_threshold': 80.0,  # percent
            'memory_threshold': 85.0,  # percent
        }

        # Monitoring
        self.monitoring_active = False
        self.monitor_thread: Optional[threading.Thread] = None

        # Initialize tracing if enabled
        if enable_tracing:
            tracemalloc.start()

    def start_monitoring(self, interval: float = 5.0):
        """Start background performance monitoring."""
        if self.monitoring_active:
            return

        self.monitoring_active = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop,
            args=(interval,),
            daemon=True
        )
        self.monitor_thread.start()
        logger.info("🟢 Performance monitoring started")

    def stop_monitoring(self):
        """Stop background performance monitoring."""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5.0)
        logger.info("🔴 Performance monitoring stopped")

    def _monitor_loop(self, interval: float):
        """Background monitoring loop."""
        while self.monitoring_active:
            try:
                snapshot = self._take_snapshot()
                self.snapshots.append(snapshot)

                # Check thresholds and alert if needed
                self._check_alerts(snapshot)

                time.sleep(interval)
            except Exception as e:
                logger.error(f"Monitoring error: {e}")
                time.sleep(interval)

    def _take_snapshot(self) -> PerformanceSnapshot:
        """Take a system performance snapshot."""
        cpu = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        net_connections = len(psutil.net_connections())
        threads = threading.active_count()

        return PerformanceSnapshot(
            timestamp=time.time(),
            cpu_percent=cpu,
            memory_percent=memory.percent,
            memory_used_mb=memory.used / (1024 * 1024),
            memory_available_mb=memory.available / (1024 * 1024),
            disk_usage_percent=disk.percent,
            network_connections=net_connections,
            thread_count=threads,
            active_operations=len(self.active_operations)
        )

    def _check_alerts(self, snapshot: PerformanceSnapshot):
        """Check performance thresholds and generate alerts."""
        alerts = []

        if snapshot.cpu_percent > self.thresholds['cpu_threshold']:
            alerts.append(f"High CPU usage: {snapshot.cpu_percent:.1f}%")

        if snapshot.memory_percent > self.thresholds['memory_threshold']:
            alerts.append(f"High memory usage: {snapshot.memory_percent:.1f}%")

        if snapshot.active_operations > 10:
            alerts.append(f"High active operations: {snapshot.active_operations}")

        for alert in alerts:
            logger.warning(f"🚨 Performance Alert: {alert}")

    @contextmanager
    def profile_operation(self, operation_name: str, **metadata):
        """
        Context manager for profiling operations.

        Usage:
            with profiler.profile_operation("task_execution", task_id="123"):
                # Your code here
                pass
        """
        start_time = time.time()
        memory_start = psutil.Process().memory_info().rss if psutil else None

        metrics = PerformanceMetrics(
            operation_name=operation_name,
            start_time=start_time,
            memory_start=memory_start,
            metadata=metadata
        )

        # Track active operation
        self.active_operations[operation_name] = metrics

        try:
            yield metrics
        finally:
            # Complete profiling
            end_time = time.time()
            memory_end = psutil.Process().memory_info().rss if psutil else None

            metrics.end_time = end_time
            metrics.duration = end_time - start_time
            metrics.memory_end = memory_end
            metrics.memory_delta = (memory_end - memory_start) if memory_start and memory_end else None

            # Additional metrics
            if psutil:
                metrics.cpu_percent = psutil.cpu_percent(interval=0.1)
                metrics.thread_count = threading.active_count()

            # Store in history
            self.metrics_history.append(metrics)

            # Remove from active operations
            self.active_operations.pop(operation_name, None)

            # Log performance
            self._log_performance(metrics)

    def profile_function(self, operation_name: Optional[str] = None):
        """
        Decorator for profiling functions.

        Usage:
            @profiler.profile_function("my_function")
            def my_function():
                pass
        """
        def decorator(func: Callable):
            name = operation_name or f"{func.__module__}.{func.__name__}"

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                with self.profile_operation(name, function=func.__name__, module=func.__module__):
                    return func(*args, **kwargs)
            return wrapper
        return decorator

    def _log_performance(self, metrics: PerformanceMetrics):
        """Log performance metrics with appropriate level."""
        duration_ms = metrics.duration_ms or 0
        memory_mb = metrics.memory_delta_mb or 0

        # Determine log level based on performance
        if duration_ms > 5000:  # 5 seconds
            log_level = logging.WARNING
            emoji = "🐌"
        elif memory_mb > 50:  # 50MB
            log_level = logging.WARNING
            emoji = "🧠"
        else:
            log_level = logging.DEBUG
            emoji = "⚡"

        logger.log(log_level, ".2f"        f"{emoji} {metrics.operation_name} completed in {duration_ms:.2f}ms, "
                 f"memory Δ: {memory_mb:+.2f}MB")

    def get_performance_report(self, operation_filter: Optional[str] = None,
                             time_window: Optional[float] = None) -> Dict[str, Any]:
        """
        Generate comprehensive performance report.

        Args:
            operation_filter: Filter by operation name pattern
            time_window: Only include operations from last N seconds

        Returns:
            Detailed performance analysis report
        """
        # Filter metrics
        metrics = list(self.metrics_history)

        if operation_filter:
            metrics = [m for m in metrics if operation_filter in m.operation_name]

        if time_window:
            cutoff = time.time() - time_window
            metrics = [m for m in metrics if m.start_time >= cutoff]

        if not metrics:
            return {"error": "No metrics found matching criteria"}

        # Calculate statistics
        durations = [m.duration for m in metrics if m.duration]
        memory_deltas = [m.memory_delta for m in metrics if m.memory_delta]

        report = {
            "summary": {
                "total_operations": len(metrics),
                "time_window_seconds": time_window,
                "operation_filter": operation_filter
            },
            "performance_stats": {
                "avg_duration_ms": sum(durations) / len(durations) * 1000 if durations else 0,
                "max_duration_ms": max(durations) * 1000 if durations else 0,
                "min_duration_ms": min(durations) * 1000 if durations else 0,
                "avg_memory_delta_mb": sum(memory_deltas) / len(memory_deltas) / (1024*1024) if memory_deltas else 0,
                "max_memory_delta_mb": max(memory_deltas) / (1024*1024) if memory_deltas else 0,
            },
            "bottlenecks": self._identify_bottlenecks(metrics),
            "recommendations": self._generate_recommendations(metrics),
            "trends": self._analyze_trends(metrics)
        }

        return report

    def _identify_bottlenecks(self, metrics: List[PerformanceMetrics]) -> List[Dict[str, Any]]:
        """Identify performance bottlenecks."""
        bottlenecks = []

        # Duration bottlenecks
        slow_operations = [m for m in metrics if m.duration and m.duration > self.thresholds['max_operation_time']]
        if slow_operations:
            bottlenecks.append({
                "type": "duration",
                "description": f"{len(slow_operations)} operations exceed {self.thresholds['max_operation_time']}s threshold",
                "operations": [m.operation_name for m in slow_operations[:5]],  # Top 5
                "impact": "high"
            })

        # Memory bottlenecks
        memory_hogs = [m for m in metrics if m.memory_delta and m.memory_delta > self.thresholds['max_memory_delta']]
        if memory_hogs:
            bottlenecks.append({
                "type": "memory",
                "description": f"{len(memory_hogs)} operations exceed {self.thresholds['max_memory_delta']/(1024*1024)}MB memory threshold",
                "operations": [m.operation_name for m in memory_hogs[:5]],
                "impact": "high"
            })

        return bottlenecks

    def _generate_recommendations(self, metrics: List[PerformanceMetrics]) -> List[str]:
        """Generate performance optimization recommendations."""
        recommendations = []

        # Analyze patterns
        operation_counts = defaultdict(int)
        for metric in metrics:
            operation_counts[metric.operation_name] += 1

        # Frequent operations
        frequent_ops = [op for op, count in operation_counts.items() if count > 10]
        if frequent_ops:
            recommendations.append(f"Consider caching results for frequently called operations: {', '.join(frequent_ops[:3])}")

        # Memory-intensive operations
        memory_intensive = [m for m in metrics if m.memory_delta and m.memory_delta > 50*1024*1024]  # 50MB
        if memory_intensive:
            recommendations.append("Implement streaming or chunked processing for memory-intensive operations")

        # Slow operations
        slow_ops = [m for m in metrics if m.duration and m.duration > 10]  # 10 seconds
        if slow_ops:
            recommendations.append("Consider async processing or background execution for slow operations")

        # Resource contention
        if len(metrics) > 0:
            avg_threads = sum(m.thread_count or 0 for m in metrics) / len(metrics)
            if avg_threads > 20:
                recommendations.append("High thread count detected - consider thread pool optimization")

        return recommendations or ["Performance is within acceptable parameters"]

    def _analyze_trends(self, metrics: List[PerformanceMetrics]) -> Dict[str, Any]:
        """Analyze performance trends over time."""
        if len(metrics) < 2:
            return {"note": "Insufficient data for trend analysis"}

        # Sort by time
        sorted_metrics = sorted(metrics, key=lambda m: m.start_time)

        # Calculate moving averages
        window_size = min(10, len(sorted_metrics))
        recent_metrics = sorted_metrics[-window_size:]

        recent_avg_duration = sum(m.duration or 0 for m in recent_metrics) / len(recent_metrics)
        overall_avg_duration = sum(m.duration or 0 for m in sorted_metrics) / len(sorted_metrics)

        trend = "stable"
        if recent_avg_duration > overall_avg_duration * 1.2:
            trend = "degrading"
        elif recent_avg_duration < overall_avg_duration * 0.8:
            trend = "improving"

        return {
            "trend": trend,
            "recent_avg_duration": recent_avg_duration,
            "overall_avg_duration": overall_avg_duration,
            "data_points": len(sorted_metrics)
        }

    def get_scalability_analysis(self) -> Dict[str, Any]:
        """Analyze system scalability characteristics."""
        analysis = {
            "current_load": {
                "active_operations": len(self.active_operations),
                "total_operations_tracked": len(self.metrics_history),
                "snapshots_available": len(self.snapshots)
            }
        }

        # Analyze recent snapshots for scalability patterns
        if self.snapshots:
            recent_snapshots = list(self.snapshots)[-10:]  # Last 10 snapshots

            analysis["scalability_metrics"] = {
                "avg_cpu_usage": sum(s.cpu_percent for s in recent_snapshots) / len(recent_snapshots),
                "avg_memory_usage": sum(s.memory_percent for s in recent_snapshots) / len(recent_snapshots),
                "avg_active_operations": sum(s.active_operations for s in recent_snapshots) / len(recent_snapshots),
                "peak_thread_count": max(s.thread_count for s in recent_snapshots),
                "scalability_score": self._calculate_scalability_score(recent_snapshots)
            }

        return analysis

    def _calculate_scalability_score(self, snapshots: List[PerformanceSnapshot]) -> float:
        """Calculate scalability score (0-100, higher is better)."""
        if not snapshots:
            return 0.0

        scores = []

        for snapshot in snapshots:
            # CPU efficiency (lower usage = more scalable)
            cpu_score = max(0, 100 - snapshot.cpu_percent)

            # Memory efficiency (lower usage = more scalable)
            memory_score = max(0, 100 - snapshot.memory_percent)

            # Operation handling (higher = more scalable)
            operation_score = min(100, snapshot.active_operations * 10)

            # Thread efficiency (balanced thread count)
            thread_score = 100 - abs(snapshot.thread_count - 8) * 5  # Optimal around 8 threads
            thread_score = max(0, min(100, thread_score))

            snapshot_score = (cpu_score + memory_score + operation_score + thread_score) / 4
            scores.append(snapshot_score)

        return sum(scores) / len(scores) if scores else 0.0


# Global profiler instance
_performance_profiler = None

def get_performance_profiler() -> PerformanceProfiler:
    """Get the global performance profiler instance."""
    global _performance_profiler
    if _performance_profiler is None:
        _performance_profiler = PerformanceProfiler()
    return _performance_profiler

def start_performance_monitoring(interval: float = 5.0):
    """Start global performance monitoring."""
    profiler = get_performance_profiler()
    profiler.start_monitoring(interval)

def stop_performance_monitoring():
    """Stop global performance monitoring."""
    profiler = get_performance_profiler()
    profiler.stop_monitoring()

# Convenience decorators
def profile_operation(operation_name: str, **metadata):
    """Decorator to profile a function."""
    profiler = get_performance_profiler()
    return profiler.profile_function(operation_name)

def profile_context(operation_name: str, **metadata):
    """Context manager to profile a code block."""
    profiler = get_performance_profiler()
    return profiler.profile_operation(operation_name, **metadata)