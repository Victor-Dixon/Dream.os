#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

Error Handling Enums - V2 Compliant
===================================

Error handling enums extracted from error_handling_core.py for V2 compliance.

Author: Agent-3 (Infrastructure & DevOps Specialist)
V2 Compliant: <400 lines, ≤5 classes
"""

from enum import Enum


class ErrorSeverity(Enum):
    """Error severity levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Error category types."""

    OPERATION = "operation"
    FILE = "file"
    NETWORK = "network"
    DATABASE = "database"
    VALIDATION = "validation"
    CONFIGURATION = "configuration"
    AGENT = "agent"
    COORDINATION = "coordination"


class CircuitState(Enum):
    """Circuit breaker states."""

    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


__all__ = ["ErrorSeverity", "ErrorCategory", "CircuitState"]

