#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

Coordination Error Handling Decorator
======================================

Decorator for applying comprehensive error handling to coordination operations.
Extracted from coordination_error_handler.py for V2 compliance.

Author: Agent-4 (Captain) - V2 Refactoring & Autonomy Enhancement
License: MIT
"""

from collections.abc import Callable
from typing import Any


def _create_operation(func: Callable, args: tuple, kwargs: dict) -> Callable:
    """Create operation callable from function and arguments."""
    def operation() -> Any:
        """Execute the wrapped operation."""
        return func(*args, **kwargs)
    return operation


def _get_operation_name(func: Callable) -> str:
    """Get operation name from function."""
    return f"{func.__module__}.{func.__name__}"


def _execute_with_coordination_handler(
    operation: Callable,
    operation_name: str,
    component: str,
    use_retry: bool,
    use_circuit_breaker: bool,
    use_recovery: bool,
    use_intelligence: bool,
) -> Any:
    """Execute operation with coordination error handler."""
    from .component_management import coordination_handler_core
    return coordination_handler_core.execute_with_error_handling(
        operation,
        operation_name,
        component,
        use_retry,
        use_circuit_breaker,
        use_recovery,
        use_intelligence,
    )


def handle_coordination_errors(
    component: str = "coordination",
    use_retry: bool = True,
    use_circuit_breaker: bool = True,
    use_recovery: bool = True,
    use_intelligence: bool = True,
) -> Callable:
    """Decorator for coordination-specific error handling.

    Args:
        component: Component identifier
        use_retry: Enable retry mechanism
        use_circuit_breaker: Enable circuit breaker
        use_recovery: Enable recovery strategies
        use_intelligence: Enable intelligent error analysis

    Returns:
        Decorated function with error handling
    """
    def decorator(func: Callable) -> Callable:
        """Decorator implementation."""
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Wrapper function that applies error handling."""
            return _create_and_execute_coordination_wrapper(
                func, args, kwargs, component,
                use_retry, use_circuit_breaker, use_recovery, use_intelligence
            )
        return wrapper
    return decorator

def _create_and_execute_coordination_wrapper(
    func: Callable,
    args: tuple,
    kwargs: dict,
    component: str,
    use_retry: bool,
    use_circuit_breaker: bool,
    use_recovery: bool,
    use_intelligence: bool,
) -> Any:
    """Create operation and execute with coordination handler."""
    operation = _create_operation(func, args, kwargs)
    operation_name = _get_operation_name(func)
    return _execute_with_coordination_handler(
        operation, operation_name, component,
        use_retry, use_circuit_breaker, use_recovery, use_intelligence
    )
