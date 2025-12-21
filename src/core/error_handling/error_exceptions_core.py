#!/usr/bin/env python3
"""
Error Exceptions - V2 Compliant

<!-- SSOT Domain: infrastructure -->

================================

Error exception classes extracted from error_handling_core.py.

Author: Agent-3 (Infrastructure & DevOps Specialist)
V2 Compliant: <400 lines, ≤5 classes
"""


class RetryException(Exception):
    """Exception raised to trigger retry mechanism."""

    pass


class CircuitBreakerError(Exception):
    """Exception raised when circuit breaker is OPEN."""

    pass


__all__ = ["RetryException", "CircuitBreakerError"]

