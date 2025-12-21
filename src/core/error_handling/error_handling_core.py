#!/usr/bin/env python3
"""
Error Handling Core - V2 Compliant Facade

<!-- SSOT Domain: infrastructure -->

==========================================

Facade module for backward compatibility after V2 refactoring.
All classes and functions are now in separate modules.

Refactored: 2025-12-02 (Agent-3)
- Split 19 classes into 5 modules for V2 compliance
- Maintains backward compatibility via facade pattern

Author: Agent-3 - Infrastructure & DevOps Specialist
V2 Compliant: <400 lines, ≤5 classes (facade only)
"""

# Import all from refactored modules
# Infrastructure SSOT: RetryConfig and CircuitBreakerConfig moved to config_dataclasses.py
from src.core.config.config_dataclasses import CircuitBreakerConfig, RetryConfig
# ErrorSummary moved to error_response_models_specialized.py (SSOT)
from .error_response_models_specialized import ErrorSummary
from .error_enums import CircuitState, ErrorCategory, ErrorSeverity
from .error_exceptions_core import CircuitBreakerError, RetryException
from .error_response_models_core import (
    DatabaseErrorResponse,
    ErrorContext,
    FileErrorResponse,
    NetworkErrorResponse,
    StandardErrorResponse,
)
from .error_response_models_specialized import (
    AgentErrorResponse,
    ConfigurationErrorResponse,
    CoordinationErrorResponse,
    ValidationErrorResponse,
)
from .error_utilities_core import (
    ErrorSeverityMapping,
    RecoverableErrors,
    get_log_level_for_severity,
    log_exception_with_severity,
)

# Backward compatibility exports
__all__ = [
    # Enums
    "ErrorSeverity",
    "ErrorCategory",
    "CircuitState",
    # Context and Response Models
    "ErrorContext",
    "StandardErrorResponse",
    "FileErrorResponse",
    "NetworkErrorResponse",
    "DatabaseErrorResponse",
    "ValidationErrorResponse",
    "ConfigurationErrorResponse",
    "AgentErrorResponse",
    "CoordinationErrorResponse",
    # Config Models
    "ErrorSummary",
    "RetryConfig",
    "CircuitBreakerConfig",
    # Exceptions
    "RetryException",
    "CircuitBreakerError",
    # Utilities
    "RecoverableErrors",
    "ErrorSeverityMapping",
    "get_log_level_for_severity",
    "log_exception_with_severity",
]
