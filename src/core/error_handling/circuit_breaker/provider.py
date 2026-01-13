"""
Circuit Breaker Provider - Dependency Injection Factory
=========================================================

<!-- SSOT Domain: integration -->

Factory/provider for creating Circuit Breaker instances.
Uses dependency injection to break circular imports.

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-12-03
V2 Compliant: Yes (<300 lines)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.config.config_dataclasses import CircuitBreakerConfig
    from .protocol import ICircuitBreaker


class CircuitBreakerProvider:
    """
    Provider for Circuit Breaker instances (Dependency Injection).
    
    Uses lazy imports to avoid circular dependencies.
    All Circuit Breaker creation should go through this provider.
    """

    @staticmethod
    def create(config: CircuitBreakerConfig) -> ICircuitBreaker:
        """
        Create a Circuit Breaker instance.
        
        Args:
            config: Circuit Breaker configuration
            
        Returns:
            Circuit Breaker instance conforming to ICircuitBreaker protocol
        """
        # Import from within directory (resolves file/directory conflict)
        from .implementation import CircuitBreaker
        return CircuitBreaker(config)

    @staticmethod
    def get_default() -> ICircuitBreaker:
        """
        Get default Circuit Breaker instance.
        
        Returns:
            Default Circuit Breaker instance
        """
        from src.core.config.config_dataclasses import CircuitBreakerConfig
        from src.core.config.timeout_constants import TimeoutConstants
        
        config = CircuitBreakerConfig(
            name="default",
            failure_threshold=5,
            recovery_timeout=TimeoutConstants.HTTP_MEDIUM
        )
        return CircuitBreakerProvider.create(config)

    @staticmethod
    def create_with_config(
        name: str,
        failure_threshold: int = 5,
        recovery_timeout: float = None
    ) -> ICircuitBreaker:
        """
        Create Circuit Breaker with inline configuration.
        
        Args:
            name: Circuit breaker name
            failure_threshold: Number of failures before opening
            recovery_timeout: Timeout before attempting recovery (seconds)
            
        Returns:
            Circuit Breaker instance
        """
        from src.core.config.config_dataclasses import CircuitBreakerConfig
        from src.core.config.timeout_constants import TimeoutConstants
        
        # Use SSOT timeout if not provided
        if recovery_timeout is None:
            recovery_timeout = TimeoutConstants.HTTP_MEDIUM
        
        config = CircuitBreakerConfig(
            name=name,
            failure_threshold=failure_threshold,
            recovery_timeout=recovery_timeout
        )
        return CircuitBreakerProvider.create(config)

