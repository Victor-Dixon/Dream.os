#!/usr/bin/env python3
"""
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

from datetime import datetime
from typing import Any


# Infrastructure SSOT: RetryConfig and CircuitBreakerConfig moved to config_dataclasses.py
# Import from Infrastructure SSOT for backward compatibility
from dataclasses import dataclass, field


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
        """Convert to dictionary."""
        return {
            "total_errors": self.total_errors,
            "error_types": self.error_types,
            "operations": self.operations,
            "timestamp": self.timestamp,
        }


__all__ = [
    "RetryConfig",  # Re-exported from Infrastructure SSOT
    "CircuitBreakerConfig",  # Re-exported from Infrastructure SSOT
    "RecoverableErrors",
    "ErrorSeverityMapping",
    "ErrorSummary",
]
