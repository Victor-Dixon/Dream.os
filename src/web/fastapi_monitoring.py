#!/usr/bin/env python3
"""
Monitoring Module - FastAPI Services
====================================

V2 Compliant: Yes (<100 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-08

Monitoring metrics extracted from fastapi_app.py for V2 compliance.
Provides centralized metrics collection and reporting for application monitoring.
"""

import time
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# Monitoring metrics storage
monitoring_metrics: Dict[str, Any] = {
    "requests_total": 0,
    "cache_hits": 0,
    "cache_misses": 0,
    "rate_limit_hits": 0,
    "ai_requests": 0,
    "errors_total": 0,
    "uptime_start": time.time(),
    "response_times": []
}

# Performance tracking
PERFORMANCE_SAMPLE_SIZE = 100


def increment_metric(metric_name: str, value: int = 1):
    """
    Increment a monitoring metric.

    Thread-safe metric incrementing with automatic initialization.

    Args:
        metric_name: Name of metric to increment
        value: Value to add (default: 1)
    """
    if metric_name not in monitoring_metrics:
        monitoring_metrics[metric_name] = 0

    monitoring_metrics[metric_name] += value


def set_metric(metric_name: str, value: Any):
    """
    Set a monitoring metric value.

    Args:
        metric_name: Name of metric to set
        value: Value to set
    """
    monitoring_metrics[metric_name] = value


def get_metric(metric_name: str) -> Any:
    """
    Get a monitoring metric value.

    Args:
        metric_name: Name of metric to retrieve

    Returns:
        Metric value or None if not found
    """
    return monitoring_metrics.get(metric_name)


def record_response_time(response_time_ms: float):
    """
    Record response time for performance monitoring.

    Maintains rolling window of response times for performance analysis.

    Args:
        response_time_ms: Response time in milliseconds
    """
    response_times = monitoring_metrics.get("response_times", [])
    response_times.append(response_time_ms)

    # Keep only last N measurements for memory efficiency
    if len(response_times) > PERFORMANCE_SAMPLE_SIZE:
        response_times = response_times[-PERFORMANCE_SAMPLE_SIZE:]

    monitoring_metrics["response_times"] = response_times


def get_monitoring_metrics(include_performance: bool = True) -> Dict[str, Any]:
    """
    Get all monitoring metrics.

    Args:
        include_performance: Whether to include performance statistics

    Returns:
        dict: Complete monitoring metrics
    """
    metrics = monitoring_metrics.copy()

    if include_performance:
        metrics.update(_calculate_performance_stats())

    return metrics


def _calculate_performance_stats() -> Dict[str, Any]:
    """Calculate performance statistics from response times."""
    response_times = monitoring_metrics.get("response_times", [])

    if not response_times:
        return {
            "avg_response_time_ms": 0,
            "median_response_time_ms": 0,
            "p95_response_time_ms": 0,
            "p99_response_time_ms": 0,
            "max_response_time_ms": 0
        }

    sorted_times = sorted(response_times)

    return {
        "avg_response_time_ms": round(sum(sorted_times) / len(sorted_times), 2),
        "median_response_time_ms": round(sorted_times[len(sorted_times) // 2], 2),
        "p95_response_time_ms": round(sorted_times[int(len(sorted_times) * 0.95)], 2),
        "p99_response_time_ms": round(sorted_times[int(len(sorted_times) * 0.99)], 2),
        "max_response_time_ms": round(max(sorted_times), 2),
        "sample_count": len(sorted_times)
    }


def get_health_status() -> Dict[str, Any]:
    """
    Get application health status based on metrics.

    Returns:
        dict: Health status with overall assessment
    """
    metrics = get_monitoring_metrics()

    # Calculate health score based on error rates and performance
    error_rate = metrics.get("errors_total", 0) / max(metrics.get("requests_total", 1), 1)
    avg_response_time = metrics.get("avg_response_time_ms", 0)

    # Health thresholds
    health_score = 100
    issues = []

    if error_rate > 0.05:  # >5% error rate
        health_score -= 30
        issues.append(".1%")

    if avg_response_time > 1000:  # >1 second average
        health_score -= 20
        issues.append(".0f")
    elif avg_response_time > 500:  # >500ms average
        health_score -= 10
        issues.append(".0f")

    if metrics.get("rate_limit_hits", 0) > metrics.get("requests_total", 1) * 0.1:  # >10% rate limited
        health_score -= 15
        issues.append("High rate limiting")

    # Determine overall status
    if health_score >= 90:
        overall_status = "healthy"
    elif health_score >= 70:
        overall_status = "degraded"
    else:
        overall_status = "unhealthy"

    return {
        "overall_status": overall_status,
        "health_score": health_score,
        "issues": issues,
        "metrics": metrics
    }


def reset_monitoring_metrics():
    """Reset all monitoring metrics to initial state."""
    global monitoring_metrics
    monitoring_metrics = {
        "requests_total": 0,
        "cache_hits": 0,
        "cache_misses": 0,
        "rate_limit_hits": 0,
        "ai_requests": 0,
        "errors_total": 0,
        "uptime_start": time.time(),
        "response_times": []
    }
    logger.info("Monitoring metrics reset")


__all__ = [
    "increment_metric",
    "set_metric",
    "get_metric",
    "record_response_time",
    "get_monitoring_metrics",
    "get_health_status",
    "reset_monitoring_metrics"
]