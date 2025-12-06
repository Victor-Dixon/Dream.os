"""
Unified RetryConfig and CircuitBreakerConfig for Infrastructure SSOT Migration
============================================================================

Phase 1: Consolidated definitions combining best features from all 4 duplicates.

This file will be moved to src/core/config/config_dataclasses.py by Agent-3.

Author: Agent-7 (Web Development Specialist) - C-024 Priority 2 Phase 1
Date: 2025-12-03
License: MIT

NOTE: This file should NOT be imported directly due to hyphen in filename.
      It should be executed with: python -m exec(open('path').read())
      Or the classes should be copied to the target location.
"""

from dataclasses import dataclass, field
from typing import Any

# RetryStrategy will be imported from error_models_enums
# For Infrastructure SSOT, we may need to move RetryStrategy enum as well
try:
    from src.core.error_handling.error_models_enums import RetryStrategy
except ImportError:
    # Fallback: Define minimal RetryStrategy if enum not available
    from enum import Enum
    class RetryStrategy(Enum):
        FIXED = "fixed"
        EXPONENTIAL = "exponential"
        LINEAR = "linear"
        CUSTOM = "custom"


@dataclass
class RetryConfig:
    """
    Unified retry configuration for infrastructure SSOT.
    
    Combines best features from:
    - error_config.py: calculate_delay() method, exceptions tuple
    - error_models_core.py: RetryStrategy enum, enabled flag, metadata, validation
    - error_decision_models.py: exponential_backoff flag, retry_exceptions tuple
    
    This will be moved to Infrastructure SSOT (config_dataclasses.py).
    """

    max_attempts: int = 3
    base_delay: float = 1.0
    backoff_factor: float = 2.0  # Same as backoff_multiplier
    max_delay: float = 60.0
    strategy: RetryStrategy = RetryStrategy.EXPONENTIAL
    jitter: bool = True
    enabled: bool = True
    exceptions: tuple[type[Exception], ...] = field(
        default_factory=lambda: (Exception,)
    )
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Post-initialization validation."""
        if self.max_attempts <= 0:
            raise ValueError("max_attempts must be positive")
        if self.base_delay <= 0:
            raise ValueError("base_delay must be positive")
        if self.max_delay <= 0:
            raise ValueError("max_delay must be positive")
        if self.backoff_factor <= 0:
            raise ValueError("backoff_factor must be positive")

    def calculate_delay(self, attempt: int) -> float:
        """
        Calculate delay for given attempt with exponential backoff and jitter.
        
        Args:
            attempt: Current attempt number (0-indexed)
            
        Returns:
            Calculated delay in seconds
        """
        import random
        
        # Calculate base delay based on strategy
        if self.strategy == RetryStrategy.EXPONENTIAL:
            delay = self.base_delay * (self.backoff_factor ** attempt)
        elif self.strategy == RetryStrategy.LINEAR:
            delay = self.base_delay * (1 + attempt * self.backoff_factor)
        elif self.strategy == RetryStrategy.FIXED:
            delay = self.base_delay
        else:  # CUSTOM
            delay = self.base_delay * (self.backoff_factor ** attempt)

        # Apply maximum delay limit
        delay = min(delay, self.max_delay)

        # Apply jitter if enabled
        if self.jitter:
            jitter_range = delay * 0.1  # 10% jitter
            delay += random.uniform(-jitter_range, jitter_range)
            delay = max(0.1, delay)  # Minimum 100ms delay

        return delay

    def should_retry(self, error: Exception, attempt: int) -> bool:
        """
        Determine if operation should be retried.
        
        Args:
            error: Exception that occurred
            attempt: Current attempt number (0-indexed)
            
        Returns:
            True if should retry, False otherwise
        """
        if not self.enabled:
            return False
        
        if attempt >= self.max_attempts:
            return False
        
        # Check if error type is in retry exceptions
        if not isinstance(error, self.exceptions):
            return False
        
        return True


@dataclass
class CircuitBreakerConfig:
    """
    Unified circuit breaker configuration for infrastructure SSOT.
    
    Combines best features from:
    - error_config.py: name, failure_threshold, recovery_timeout
    - error_models_core.py: expected_exception, success_threshold, enabled, metadata, validation
    - circuit_breaker/core.py: timeout_seconds (mapped to recovery_timeout)
    
    This will be moved to Infrastructure SSOT (config_dataclasses.py).
    """

    name: str
    failure_threshold: int = 5
    recovery_timeout: float = 60.0
    expected_exception: type[Exception] = Exception
    success_threshold: int = 3
    enabled: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Post-initialization validation."""
        if not self.name:
            raise ValueError("name is required")
        if self.failure_threshold <= 0:
            raise ValueError("failure_threshold must be positive")
        if self.recovery_timeout <= 0:
            raise ValueError("recovery_timeout must be positive")
        if self.success_threshold <= 0:
            raise ValueError("success_threshold must be positive")

    @property
    def timeout_seconds(self) -> int:
        """
        Compatibility property for circuit_breaker/core.py usage.
        Maps recovery_timeout to timeout_seconds.
        """
        return int(self.recovery_timeout)

