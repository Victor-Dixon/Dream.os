#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

Error Handling Configuration
=============================

Configuration classes for retry logic and circuit breakers.
Extracted from error_handling_core.py for V2 compliance.

Consolidated from error_config_models.py to remove duplicates.

Author: Agent-6 - Quality Gates & VSCode Specialist (V2 Refactor)
Original: Agent-3 - Infrastructure & DevOps Specialist (C-055-3)
Consolidation: Agent-7 - Web Development Specialist (C-024)
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from ..config.timeout_constants import TimeoutConstants

from src.core.utils.serialization_utils import to_dict

# Define CircuitBreakerConfig and RetryConfig locally (Infrastructure SSOT may not have them yet)
@dataclass
class CircuitBreakerConfig:
    """Circuit breaker configuration."""
    name: str
    failure_threshold: int = 5
    recovery_timeout: float = TimeoutConstants.HTTP_MEDIUM
    
    @property
    def timeout(self) -> float:
        """Backward compatibility: alias for recovery_timeout."""
        return self.recovery_timeout

@dataclass
class RetryConfig:
    """Retry configuration."""
    max_attempts: int = 3
    initial_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0

class RecoverableErrors:
    """Recoverable error types."""

    TYPES = (ConnectionError, TimeoutError, OSError, FileNotFoundError, PermissionError)


class ErrorSeverityMapping:
    """Error severity mapping."""

    CRITICAL = (SystemError, MemoryError, KeyboardInterrupt)
    HIGH = (ValueError, TypeError, AttributeError, KeyError)
    MEDIUM = (FileNotFoundError, PermissionError, ConnectionError)
    # All others are LOW severity


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
        """Convert to dictionary using SSOT utility."""
        return to_dict(self)


__all__ = [
    "RetryConfig",
    "CircuitBreakerConfig",
    "RecoverableErrors",
    "ErrorSeverityMapping",
    "ErrorSummary",
]
