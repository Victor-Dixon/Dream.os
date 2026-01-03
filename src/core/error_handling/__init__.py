# V2 Compliance Error Handling Framework
# ======================================
#
# Centralized error handling with comprehensive logging, recovery, and monitoring.
# This module provides the core error handling infrastructure for the Agent Cellphone V2 system.

from .error_handling import (
    # Core classes
    ErrorHandler, ErrorSeverity, ErrorCategory, ErrorContext, ErrorReport,

    # Global functions
    get_error_handler,

    # Decorators and context managers
    handle_errors, error_context,

    # Utility functions
    safe_dict_access, safe_list_access, validate_json_data,
    validate_python_syntax, validate_project_syntax,
)

# Import circuit breaker from existing implementation
try:
    from .circuit_breaker.implementation import CircuitBreaker
    from .circuit_breaker.protocol import ICircuitBreaker
    from .circuit_breaker.provider import CircuitBreakerProvider
except ImportError:
    # Fallback for missing circuit breaker
    CircuitBreaker = None
    ICircuitBreaker = None
    CircuitBreakerProvider = None

# SSOT Domain: core
# V2 Error Handling Framework

__all__ = [
    # Core classes
    'ErrorHandler', 'ErrorSeverity', 'ErrorCategory', 'ErrorContext', 'ErrorReport',

    # Global functions
    'get_error_handler',

    # Decorators and context managers
    'handle_errors', 'error_context',

    # Utility functions
    'safe_dict_access', 'safe_list_access', 'validate_json_data',
    'validate_python_syntax', 'validate_project_syntax',

    # Circuit breaker (backward compatibility)
    'CircuitBreaker', 'ICircuitBreaker', 'CircuitBreakerProvider',
]
