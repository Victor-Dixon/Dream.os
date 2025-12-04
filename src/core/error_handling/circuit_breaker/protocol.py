"""
Circuit Breaker Protocol - SSOT for Circuit Breaker Interface
============================================================

<!-- SSOT Domain: integration -->

Protocol defining the Circuit Breaker interface contract.
All Circuit Breaker implementations must conform to this protocol.

Uses Dependency Injection pattern to break circular imports.

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-12-03
V2 Compliant: Yes (<300 lines)
"""

from __future__ import annotations

from typing import Any, Callable, Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.config.config_dataclasses import CircuitBreakerConfig


class ICircuitBreaker(Protocol):
    """
    Circuit Breaker protocol - defines the interface contract.
    
    All Circuit Breaker implementations must provide these methods.
    This protocol enables dependency injection and breaks circular imports.
    """

    def call(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """
        Execute function with circuit breaker protection.
        
        Args:
            func: Function to execute
            *args: Positional arguments for function
            **kwargs: Keyword arguments for function
            
        Returns:
            Function result
            
        Raises:
            CircuitBreakerError: If circuit is open and not ready for reset
            Exception: Any exception raised by the function
        """
        ...

    def get_state(self) -> str:
        """
        Get current circuit breaker state.
        
        Returns:
            State string: "closed", "open", or "half_open"
        """
        ...

    def get_status(self) -> dict[str, Any]:
        """
        Get current circuit breaker status.
        
        Returns:
            Dictionary with status information:
            - name: Circuit breaker name
            - state: Current state
            - failure_count: Number of failures
            - failure_threshold: Threshold for opening
            - timeout_seconds: Recovery timeout
            - last_failure_time: Timestamp of last failure
            - next_attempt_time: Timestamp for next reset attempt
        """
        ...

