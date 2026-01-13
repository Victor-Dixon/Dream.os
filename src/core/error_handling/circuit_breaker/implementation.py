"""
Circuit Breaker Implementation - SSOT
======================================

Circuit breaker pattern implementation - SSOT for Circuit Breaker.

<!-- SSOT Domain: integration -->

Moved from circuit_breaker.py to resolve file/directory conflict.
Consolidated with main implementation to eliminate duplicates.

Author: Agent-2 - Architecture & Design Specialist (V2 Refactor)
Refactored: Agent-1 - Integration & Core Systems Specialist (Dependency Injection)
License: MIT
"""

import logging
from datetime import datetime, timedelta
from typing import Any

# Infrastructure SSOT: CircuitBreakerConfig moved to config_dataclasses.py
from src.core.config.config_dataclasses import CircuitBreakerConfig
from ..error_handling_core import CircuitBreakerError, CircuitState

logger = logging.getLogger(__name__)


class CircuitBreaker:
    """
    Circuit breaker pattern for preventing cascading failures.
    
    Implements ICircuitBreaker protocol for dependency injection.
    SSOT for Circuit Breaker implementation.
    """

    def __init__(self, config: CircuitBreakerConfig):
        """Initialize circuit breaker."""
        self.config = config
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None
        self.opened_at = None

    def get_state(self) -> str:
        """Get current circuit breaker state."""
        return self.state.value

    def call(self, func, *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection."""
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
                logger.info(f"Circuit breaker entering half-open state for {self.config.name}")
            else:
                raise CircuitBreakerError(f"Circuit breaker is OPEN for {self.config.name}")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e

    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset."""
        if not self.opened_at:
            return False
        # Support both 'timeout' and 'recovery_timeout' for backward compatibility
        timeout = getattr(self.config, 'timeout', None) or getattr(self.config, 'recovery_timeout', 60.0)
        return datetime.now() - self.opened_at >= timedelta(seconds=timeout)

    def _on_success(self):
        """Handle successful call."""
        if self.state == CircuitState.HALF_OPEN:
            logger.info(f"Circuit breaker reset to CLOSED for {self.config.name}")
            self.state = CircuitState.CLOSED
        self.failure_count = 0

    def _on_failure(self):
        """Handle failed call."""
        self.failure_count += 1
        self.last_failure_time = datetime.now()

        if self.failure_count >= self.config.failure_threshold:
            self.state = CircuitState.OPEN
            self.opened_at = datetime.now()
            logger.warning(
                f"Circuit breaker opened after {self.failure_count} failures for {self.config.name}"
            )

    def get_state(self) -> str:
        """Get current circuit breaker state."""
        return self.state.value

    def get_status(self) -> dict[str, Any]:
        """Get current circuit breaker status."""
        # Support both 'timeout' and 'recovery_timeout' for backward compatibility
        timeout = getattr(self.config, 'timeout', None) or getattr(self.config, 'recovery_timeout', 60.0)
        timeout_seconds = getattr(self.config, 'timeout_seconds', None) or timeout
        
        return {
            "name": self.config.name,
            "state": self.state.value,
            "failure_count": self.failure_count,
            "failure_threshold": self.config.failure_threshold,
            "timeout_seconds": timeout_seconds,
            "last_failure_time": (
                self.last_failure_time.isoformat() if self.last_failure_time else None
            ),
            "opened_at": (
                self.opened_at.isoformat() if self.opened_at else None
            ),
        }

