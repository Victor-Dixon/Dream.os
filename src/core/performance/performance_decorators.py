#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

Performance Decorators - Agent Cellphone V2
==========================================

Performance monitoring decorators and utilities.

Author: Agent-8 (SSOT Maintenance & System Integration Specialist)
License: MIT
"""

import time
from functools import wraps
from typing import Callable

# Import get_performance_monitor from coordination_performance_monitor
try:
    from .coordination_performance_monitor import get_performance_monitor
except ImportError:
    # Fallback if import fails
    def get_performance_monitor():
        """Fallback performance monitor getter."""
        from .coordination_performance_monitor import CoordinationPerformanceMonitor
        return CoordinationPerformanceMonitor()


def monitor_performance(operation_name: str = None):
    """Decorator for automatic performance monitoring."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            monitor = get_performance_monitor()
            op_name = operation_name or f"{func.__module__}.{func.__name__}"

            start_time = time.time()
            monitor.record_operation_start(op_name)

            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                monitor.record_operation_completion(op_name, duration, success=True)
                return result
            except Exception as e:
                duration = time.time() - start_time
                monitor.record_operation_completion(op_name, duration, success=False)
                raise e

        return wrapper

    return decorator
