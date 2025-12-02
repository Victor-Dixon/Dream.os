#!/usr/bin/env python3
"""
Error Configuration Models - V2 Compliant
==========================================

Error configuration dataclasses extracted from error_handling_core.py.

Author: Agent-3 (Infrastructure & DevOps Specialist)
V2 Compliant: <400 lines, ≤5 classes
"""

import random
from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class ErrorSummary:
    """Error summary statistics."""

    total_errors: int = 0
    error_types: dict[str, int] = None
    operations: dict[str, int] = None
    timestamp: str = ""

    def __post_init__(self):
        if self.error_types is None:
            self.error_types = {}
        if self.operations is None:
            self.operations = {}
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "total_errors": self.total_errors,
            "error_types": self.error_types,
            "operations": self.operations,
            "timestamp": self.timestamp,
        }


@dataclass
class RetryConfig:
    """Unified retry configuration (consolidated from multiple sources)."""

    max_attempts: int = 3
    base_delay: float = 1.0
    backoff_factor: float = 2.0
    max_delay: float = 60.0
    jitter: bool = True
    exceptions: tuple = (Exception,)

    def calculate_delay(self, attempt: int) -> float:
        """Calculate delay for given attempt with exponential backoff and jitter."""
        delay = self.base_delay * (self.backoff_factor**attempt)

        # Apply maximum delay limit
        delay = min(delay, self.max_delay)

        # Apply jitter if enabled
        if self.jitter:
            jitter_range = delay * 0.1  # 10% jitter
            delay += random.uniform(-jitter_range, jitter_range)
            delay = max(0.1, delay)  # Minimum 100ms delay

        return delay


@dataclass
class CircuitBreakerConfig:
    """Circuit breaker configuration."""

    name: str
    failure_threshold: int = 5
    recovery_timeout: float = 60.0


__all__ = ["ErrorSummary", "RetryConfig", "CircuitBreakerConfig"]

