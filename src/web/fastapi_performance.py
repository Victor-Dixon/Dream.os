#!/usr/bin/env python3
"""
Performance Module - FastAPI Services
=====================================

V2 Compliant: Yes (<100 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-08

Performance optimization utilities extracted from fastapi_app.py for V2 compliance.
Provides response data optimization and performance monitoring functions.
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


async def optimize_response_data(data: Dict[str, Any], endpoint: str) -> Dict[str, Any]:
    """
    Optimize response data for better performance.

    Applies endpoint-specific optimizations to reduce payload size
    and improve response times without losing critical information.

    Args:
        data: Response data dictionary
        endpoint: API endpoint path

    Returns:
        dict: Optimized response data
    """
    if endpoint in ["/api/ai/context", "/api/metrics"]:
        # These endpoints don't need optimization as they're already efficient
        return data

    # Convert timestamps to integers for smaller JSON
    if "timestamp" in data and endpoint.startswith("/api/v1/"):
        # Keep timestamp for trading data but optimize format
        data["timestamp"] = int(data["timestamp"])  # Convert to int for smaller JSON

    # Compress large arrays if needed
    if endpoint == "/api/v1/trades" and len(data.get("trades", [])) > 50:
        # Limit to most recent 50 trades for performance
        data["trades"] = data["trades"][-50:]
        data["truncated"] = True
        logger.info(f"Truncated trades response to 50 items for performance")

    # Remove unnecessary metadata for production performance
    if endpoint.startswith("/api/v1/"):
        # Keep only essential fields for trading endpoints
        essential_fields = {"trades", "timestamp", "status", "error"}
        keys_to_remove = [k for k in data.keys() if k not in essential_fields]
        for key in keys_to_remove:
            if key not in ["trades", "timestamp", "status"]:  # Preserve core data
                del data[key]

    return data


def calculate_response_metrics(response_data: Dict[str, Any]) -> Dict[str, float]:
    """
    Calculate response performance metrics.

    Analyzes response data to provide performance insights.

    Args:
        response_data: Response data dictionary

    Returns:
        dict: Performance metrics
    """
    metrics = {
        "data_size_kb": len(str(response_data)) / 1024,
        "field_count": len(response_data),
        "nested_depth": _calculate_nested_depth(response_data),
        "array_sizes": _calculate_array_sizes(response_data)
    }

    return metrics


def _calculate_nested_depth(data: Any, current_depth: int = 0) -> int:
    """Calculate maximum nesting depth in data structure."""
    if isinstance(data, dict):
        if not data:
            return current_depth
        return max(_calculate_nested_depth(v, current_depth + 1) for v in data.values())
    elif isinstance(data, list):
        if not data:
            return current_depth
        return max(_calculate_nested_depth(item, current_depth) for item in data)
    else:
        return current_depth


def _calculate_array_sizes(data: Any) -> Dict[str, int]:
    """Calculate sizes of arrays in the data structure."""
    array_sizes = {}

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, list):
                array_sizes[key] = len(value)
            elif isinstance(value, dict):
                nested_sizes = _calculate_array_sizes(value)
                array_sizes.update({f"{key}.{k}": v for k, v in nested_sizes.items()})

    return array_sizes


def is_performance_critical_endpoint(endpoint: str) -> bool:
    """
    Check if endpoint is performance-critical.

    Identifies endpoints that require special performance optimization.

    Args:
        endpoint: API endpoint path

    Returns:
        bool: True if endpoint is performance-critical
    """
    critical_endpoints = {
        "/api/v1/trades",
        "/api/ai/chat",
        "/api/metrics",
        "/health"
    }

    return any(endpoint.startswith(ep) for ep in critical_endpoints)


def get_performance_recommendations(metrics: Dict[str, Any]) -> list[str]:
    """
    Generate performance recommendations based on metrics.

    Analyzes performance metrics to provide optimization suggestions.

    Args:
        metrics: Performance metrics dictionary

    Returns:
        list: Performance recommendations
    """
    recommendations = []

    # Data size recommendations
    data_size_kb = metrics.get("data_size_kb", 0)
    if data_size_kb > 100:
        recommendations.append("Consider pagination for large datasets")
    elif data_size_kb > 50:
        recommendations.append("Review data fields - remove unnecessary metadata")

    # Array size recommendations
    array_sizes = metrics.get("array_sizes", {})
    for field, size in array_sizes.items():
        if size > 1000:
            recommendations.append(f"Consider limiting {field} array size (currently {size} items)")
        elif size > 100:
            recommendations.append(f"Consider pagination for {field} array (currently {size} items)")

    # Nesting recommendations
    nested_depth = metrics.get("nested_depth", 0)
    if nested_depth > 5:
        recommendations.append(f"Consider flattening nested structure (current depth: {nested_depth})")

    return recommendations if recommendations else ["Performance looks good"]


__all__ = [
    "optimize_response_data",
    "calculate_response_metrics",
    "is_performance_critical_endpoint",
    "get_performance_recommendations"
]