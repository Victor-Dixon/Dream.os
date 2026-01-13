"""
<!-- SSOT Domain: core -->

Circuit Breaker Core - V2 Compliance Module
==========================================

Core circuit breaker functionality.

V2 Compliance: < 300 lines, single responsibility, circuit breaker core.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import logging
from datetime import datetime, timedelta
from enum import Enum

logger = logging.getLogger(__name__)


class CircuitState(Enum):
    """Circuit breaker states."""

    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


# Infrastructure SSOT: CircuitBreakerConfig moved to config_dataclasses.py
from src.core.config.config_dataclasses import CircuitBreakerConfig

# Note: SSOT CircuitBreakerConfig has timeout_seconds property for backward compatibility


class CircuitBreakerCore:
    """Core circuit breaker functionality."""

    def __init__(self, config: CircuitBreakerConfig):
        """Initialize circuit breaker core."""
        self.config = config
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time: datetime | None = None
        self.next_attempt_time: datetime | None = None

    def _should_attempt_reset(self) -> bool:
        """Check if we should attempt to reset the circuit."""
        if self.state != CircuitState.OPEN:
            return False

        if self.next_attempt_time is None:
            return True

        return datetime.now() >= self.next_attempt_time

    def _record_success(self) -> None:
        """Record successful operation."""
        self.failure_count = 0
        self.state = CircuitState.CLOSED
        self.next_attempt_time = None
        logger.info(f"Circuit breaker '{self.config.name}' reset to CLOSED")

    def _record_failure(self, exception: Exception) -> None:
        """Record failed operation."""
        self.failure_count += 1
        self.last_failure_time = datetime.now()

        if self.failure_count >= self.config.failure_threshold:
            self.state = CircuitState.OPEN
            # Use timeout_seconds property (backward compatibility)
            timeout = self.config.timeout_seconds if hasattr(self.config, 'timeout_seconds') else self.config.recovery_timeout
            self.next_attempt_time = datetime.now() + timedelta(seconds=timeout)
            logger.warning(
                f"Circuit breaker '{self.config.name}' opened after {self.failure_count} failures"
            )

    def get_status(self) -> dict:
        """Get current circuit breaker status."""
        return {
            "name": self.config.name,
            "state": self.state.value,
            "failure_count": self.failure_count,
            "failure_threshold": self.config.failure_threshold,
            "timeout_seconds": self.config.timeout_seconds if hasattr(self.config, 'timeout_seconds') else int(self.config.recovery_timeout),
            "last_failure_time": (
                self.last_failure_time.isoformat() if self.last_failure_time else None
            ),
            "next_attempt_time": (
                self.next_attempt_time.isoformat() if self.next_attempt_time else None
            ),
        }
