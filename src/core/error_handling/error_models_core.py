"""
Error Models Core - V2 Compliance Error Handling Core Models

<!-- SSOT Domain: infrastructure -->

============================================================

Core data models for error handling system with V2 compliance standards.

V2 COMPLIANCE: Type-safe error models with validation
DESIGN PATTERN: Dataclass pattern for error model definitions
DEPENDENCY INJECTION: Configuration-driven error handling parameters

Author: Agent-2 (Architecture & Design Specialist)
Mission: V2 Compliance Architecture & Design Optimization
Status: V2 COMPLIANT - Error Models Core Optimized
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .error_models_enums import ErrorSeverity, ErrorType, RetryStrategy


@dataclass
class ErrorContext:
    """Error context with V2 compliance."""

    error_id: str
    error_type: ErrorType
    severity: ErrorSeverity
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = "unknown"
    stack_trace: str | None = None
    user_id: str | None = None
    session_id: str | None = None
    request_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    context_data: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Post-initialization validation."""
        if not self.error_id:
            raise ValueError("error_id is required")
        if not self.message:
            raise ValueError("message is required")


# Infrastructure SSOT: RetryConfig and CircuitBreakerConfig moved to config_dataclasses.py
# Import from Infrastructure SSOT
from src.core.config.config_dataclasses import CircuitBreakerConfig, RetryConfig
