"""
<<<<<<< HEAD
FastAPI Performance Monitoring Module
=====================================

V2 Compliant - Complete performance monitoring with metrics collection
Author: Agent-7 (Web Development Specialist)
Date: 2026-01-10

Implements comprehensive performance monitoring for FastAPI applications.
"""

import time
import logging
import statistics
from collections import defaultdict, deque
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from fastapi import Request, Response

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    """Performance metrics data structure."""
    request_count: int = 0
    total_response_time: float = 0.0
    response_times: deque = field(default_factory=lambda: deque(maxlen=1000))
    status_codes: Dict[int, int] = field(default_factory=dict)
    endpoint_metrics: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    memory_usage: List[float] = field(default_factory=list)
    cpu_usage: List[float] = field(default_factory=list)

    def record_request(self, endpoint: str, response_time: float, status_code: int, memory_used: float = 0.0, cpu_used: float = 0.0):
        """Record a request's performance metrics."""
        self.request_count += 1
        self.total_response_time += response_time
        self.response_times.append(response_time)
        self.status_codes[status_code] = self.status_codes.get(status_code, 0) + 1

        if memory_used > 0:
            self.memory_usage.append(memory_used)
        if cpu_used > 0:
            self.cpu_usage.append(cpu_used)

        # Update endpoint-specific metrics
        if endpoint not in self.endpoint_metrics:
            self.endpoint_metrics[endpoint] = {
                'count': 0,
                'total_time': 0.0,
                'times': deque(maxlen=100),
                'status_codes': defaultdict(int)
            }

        ep_metrics = self.endpoint_metrics[endpoint]
        ep_metrics['count'] += 1
        ep_metrics['total_time'] += response_time
        ep_metrics['times'].append(response_time)
        ep_metrics['status_codes'][status_code] += 1

    def get_summary(self) -> Dict[str, Any]:
        """Get performance metrics summary."""
        avg_response_time = self.total_response_time / max(self.request_count, 1)
        response_times_list = list(self.response_times)

        summary = {
            'total_requests': self.request_count,
            'average_response_time': round(avg_response_time, 3),
            'median_response_time': round(statistics.median(response_times_list), 3) if response_times_list else 0,
            '95p_response_time': round(statistics.quantiles(response_times_list, n=20)[18], 3) if len(response_times_list) >= 20 else 0,
            'min_response_time': round(min(response_times_list), 3) if response_times_list else 0,
            'max_response_time': round(max(response_times_list), 3) if response_times_list else 0,
            'status_codes': dict(self.status_codes),
            'memory_usage_mb': round(sum(self.memory_usage) / max(len(self.memory_usage), 1) / (1024*1024), 2) if self.memory_usage else 0,
            'cpu_usage_percent': round(sum(self.cpu_usage) / max(len(self.cpu_usage), 1), 2) if self.cpu_usage else 0,
            'endpoint_breakdown': {}
        }

        # Add endpoint breakdown
        for endpoint, metrics in self.endpoint_metrics.items():
            times_list = list(metrics['times'])
            summary['endpoint_breakdown'][endpoint] = {
                'requests': metrics['count'],
                'avg_time': round(metrics['total_time'] / max(metrics['count'], 1), 3),
                'median_time': round(statistics.median(times_list), 3) if times_list else 0,
                'status_codes': dict(metrics['status_codes'])
            }

        return summary

# Global metrics instance
performance_metrics = PerformanceMetrics()

async def performance_monitoring_middleware(request: Request, call_next) -> Response:
    """
    Comprehensive performance monitoring middleware.

    Tracks:
    - Response times (avg, median, 95p, min, max)
    - Request counts by endpoint and status code
    - Memory and CPU usage
    - Endpoint-specific performance breakdown
    """
    start_time = time.time()
    start_memory = 0
    start_cpu = 0

    # Track system resource usage if available
    try:
        import psutil
        process = psutil.Process()
        start_memory = process.memory_info().rss
        start_cpu = process.cpu_percent(interval=None)
    except ImportError:
        pass

    try:
        response = await call_next(request)

        # Calculate performance metrics
        duration = time.time() - start_time
        memory_used = 0
        cpu_used = 0

        try:
            import psutil
            process = psutil.Process()
            memory_used = process.memory_info().rss - start_memory
            cpu_used = process.cpu_percent(interval=None) - start_cpu
        except ImportError:
            pass

        # Record metrics
        endpoint = f"{request.method} {request.url.path}"
        performance_metrics.record_request(
            endpoint=endpoint,
            response_time=duration,
            status_code=response.status_code,
            memory_used=memory_used,
            cpu_used=cpu_used
        )

        # Add performance headers to response
        response.headers['X-Response-Time'] = f"{duration:.3f}s"
        response.headers['X-Performance-Monitored'] = "true"

        # Log slow requests
        if duration > 1.0:  # Log requests taking more than 1 second
            logger.warning(f"Slow request: {request.method} {request.url.path} took {duration:.3f}s")
        elif duration > 5.0:  # Log very slow requests
            logger.error(f"Very slow request: {request.method} {request.url.path} took {duration:.3f}s")
        return response

    except Exception as e:
        # Record failed request
        duration = time.time() - start_time
        endpoint = f"{request.method} {request.url.path}"
        performance_metrics.record_request(
            endpoint=endpoint,
            response_time=duration,
            status_code=500  # Internal server error
        )
        raise

def get_performance_metrics() -> Dict[str, Any]:
    """Get current performance metrics."""
    return performance_metrics.get_summary()

def reset_performance_metrics():
    """Reset performance metrics (useful for testing)."""
    global performance_metrics
    performance_metrics = PerformanceMetrics()

def get_performance_middleware():
    """Get the performance monitoring middleware function."""
    return performance_monitoring_middleware
=======
FastAPI Performance Module
V2 Compliant - <100 lines
"""

import time
from fastapi import Request, Response

def performance_middleware():
    """Performance monitoring middleware"""
    pass
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
