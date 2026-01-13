#!/usr/bin/env python3
"""
Error Handling Standardization - SSOT Implementation
=====================================

Single Source of Truth for error handling patterns.

<!-- SSOT Domain: error-management -->

Eliminates inconsistent exception patterns through:
- Standardized exception hierarchy
- Context-aware error messages
- Retry mechanisms
- Error classification and reporting

V2 Compliant: Unified error handling across all services
Author: Agent-8 (SSOT & System Integration)
Date: 2026-01-12
"""

import logging
import time
import traceback
from typing import Any, Dict, List, Optional, Callable, Type, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum
from functools import wraps
from contextlib import contextmanager


class ErrorSeverity(Enum):
    """Standardized error severity levels."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Standardized error categories for classification."""
    CONFIGURATION = "configuration"
    NETWORK = "network"
    DATABASE = "database"
    FILESYSTEM = "filesystem"
    VALIDATION = "validation"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    BUSINESS_LOGIC = "business_logic"
    EXTERNAL_SERVICE = "external_service"
    INTERNAL_ERROR = "internal_error"


@dataclass
class ErrorContext:
    """Context information for errors."""
    component: str
    operation: str
    user_id: Optional[str] = None
    request_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


@dataclass
class StandardizedError:
    """Standardized error representation."""
    message: str
    category: ErrorCategory
    severity: ErrorSeverity
    context: ErrorContext
    original_exception: Optional[Exception] = None
    stack_trace: Optional[str] = None
    retryable: bool = False
    suggested_action: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary representation."""
        return {
            'message': self.message,
            'category': self.category.value,
            'severity': self.severity.value,
            'component': self.context.component,
            'operation': self.context.operation,
            'user_id': self.context.user_id,
            'request_id': self.context.request_id,
            'timestamp': self.context.timestamp,
            'metadata': self.context.metadata,
            'retryable': self.retryable,
            'suggested_action': self.suggested_action,
            'has_stack_trace': self.stack_trace is not None,
        }


class SwarmError(Exception):
    """Base exception for all swarm operations."""

    def __init__(
        self,
        message: str,
        category: ErrorCategory,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        context: Optional[ErrorContext] = None,
        original_exception: Optional[Exception] = None,
        retryable: bool = False,
        suggested_action: Optional[str] = None
    ):
        self.standardized_error = StandardizedError(
            message=message,
            category=category,
            severity=severity,
            context=context or ErrorContext("unknown", "unknown"),
            original_exception=original_exception,
            stack_trace=traceback.format_exc() if original_exception else None,
            retryable=retryable,
            suggested_action=suggested_action,
        )

        super().__init__(message)
        self.category = category
        self.severity = severity
        self.context = self.standardized_error.context


class ConfigurationError(SwarmError):
    """Configuration-related errors."""
    def __init__(self, message: str, context: ErrorContext, **kwargs):
        super().__init__(
            message,
            ErrorCategory.CONFIGURATION,
            ErrorSeverity.ERROR,
            context,
            **kwargs
        )


class NetworkError(SwarmError):
    """Network-related errors."""
    def __init__(self, message: str, context: ErrorContext, **kwargs):
        super().__init__(
            message,
            ErrorCategory.NETWORK,
            ErrorSeverity.WARNING,
            context,
            retryable=True,
            **kwargs
        )


class DatabaseError(SwarmError):
    """Database-related errors."""
    def __init__(self, message: str, context: ErrorContext, **kwargs):
        super().__init__(
            message,
            ErrorCategory.DATABASE,
            ErrorSeverity.ERROR,
            context,
            retryable=True,
            **kwargs
        )


class ValidationError(SwarmError):
    """Data validation errors."""
    def __init__(self, message: str, context: ErrorContext, **kwargs):
        super().__init__(
            message,
            ErrorCategory.VALIDATION,
            ErrorSeverity.WARNING,
            context,
            **kwargs
        )


class AuthenticationError(SwarmError):
    """Authentication-related errors."""
    def __init__(self, message: str, context: ErrorContext, **kwargs):
        super().__init__(
            message,
            ErrorCategory.AUTHENTICATION,
            ErrorSeverity.ERROR,
            context,
            **kwargs
        )


class AuthorizationError(SwarmError):
    """Authorization-related errors."""
    def __init__(self, message: str, context: ErrorContext, **kwargs):
        super().__init__(
            message,
            ErrorCategory.AUTHORIZATION,
            ErrorSeverity.ERROR,
            context,
            **kwargs
        )


class BusinessLogicError(SwarmError):
    """Business logic errors."""
    def __init__(self, message: str, context: ErrorContext, **kwargs):
        super().__init__(
            message,
            ErrorCategory.BUSINESS_LOGIC,
            ErrorSeverity.ERROR,
            context,
            **kwargs
        )


class ExternalServiceError(SwarmError):
    """External service errors."""
    def __init__(self, message: str, context: ErrorContext, **kwargs):
        super().__init__(
            message,
            ErrorCategory.EXTERNAL_SERVICE,
            ErrorSeverity.WARNING,
            context,
            retryable=True,
            **kwargs
        )


class ErrorHandler:
    """
    Centralized error handling and reporting.

    Provides:
    - Standardized error logging
    - Error classification
    - Retry mechanisms
    - Error aggregation and reporting
    """

    def __init__(self, component_name: str):
        self.component_name = component_name
        self.logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")
        self.errors: List[StandardizedError] = []
        self.error_counts = {}

    def handle_error(
        self,
        error: Exception,
        operation: str,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        user_id: Optional[str] = None,
        request_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        retryable: bool = False,
        suggested_action: Optional[str] = None
    ) -> StandardizedError:
        """
        Handle and standardize an error.

        Args:
            error: The original exception
            operation: The operation that failed
            severity: Error severity level
            user_id: Optional user identifier
            request_id: Optional request identifier
            metadata: Additional error metadata
            retryable: Whether the operation can be retried
            suggested_action: Suggested recovery action

        Returns:
            Standardized error representation
        """

        # Classify error category
        category = self._classify_error(error)

        # Create error context
        context = ErrorContext(
            component=self.component_name,
            operation=operation,
            user_id=user_id,
            request_id=request_id,
            metadata=metadata or {},
        )

        # Create standardized error
        std_error = StandardizedError(
            message=str(error),
            category=category,
            severity=severity,
            context=context,
            original_exception=error,
            stack_trace=traceback.format_exc(),
            retryable=retryable,
            suggested_action=suggested_action,
        )

        # Log error
        self._log_error(std_error)

        # Track error
        self.errors.append(std_error)
        self.error_counts[category] = self.error_counts.get(category, 0) + 1

        return std_error

    def _classify_error(self, error: Exception) -> ErrorCategory:
        """Classify an error into a category."""
        error_type = type(error).__name__
        error_message = str(error).lower()

        # Network-related errors
        if any(keyword in error_message for keyword in ['connection', 'timeout', 'network', 'http', 'dns']):
            return ErrorCategory.NETWORK

        # Database-related errors
        if any(keyword in error_message for keyword in ['database', 'sql', 'query', 'cursor']):
            return ErrorCategory.DATABASE

        # File system errors
        if any(keyword in error_message for keyword in ['file', 'directory', 'path', 'permission']):
            return ErrorCategory.FILESYSTEM

        # Authentication/Authorization
        if any(keyword in error_message for keyword in ['auth', 'login', 'permission', 'access']):
            if 'auth' in error_message:
                return ErrorCategory.AUTHENTICATION
            else:
                return ErrorCategory.AUTHORIZATION

        # Validation errors
        if any(keyword in error_message for keyword in ['invalid', 'validation', 'required', 'format']):
            return ErrorCategory.VALIDATION

        # Configuration errors
        if any(keyword in error_message for keyword in ['config', 'setting', 'parameter']):
            return ErrorCategory.CONFIGURATION

        # Default to internal error
        return ErrorCategory.INTERNAL_ERROR

    def _log_error(self, error: StandardizedError) -> None:
        """Log an error with appropriate level."""
        log_message = (
            f"[{error.category.value.upper()}] {error.context.component}.{error.context.operation}: "
            f"{error.message}"
        )

        if error.context.user_id:
            log_message += f" (user: {error.context.user_id})"
        if error.context.request_id:
            log_message += f" (request: {error.context.request_id})"
        if error.suggested_action:
            log_message += f" | Suggested: {error.suggested_action}"

        if error.severity == ErrorSeverity.DEBUG:
            self.logger.debug(log_message)
        elif error.severity == ErrorSeverity.INFO:
            self.logger.info(log_message)
        elif error.severity == ErrorSeverity.WARNING:
            self.logger.warning(log_message)
        elif error.severity == ErrorSeverity.ERROR:
            self.logger.error(log_message)
        elif error.severity == ErrorSeverity.CRITICAL:
            self.logger.critical(log_message)

        # Log stack trace for ERROR and above
        if error.severity in [ErrorSeverity.ERROR, ErrorSeverity.CRITICAL] and error.stack_trace:
            self.logger.debug(f"Stack trace:\n{error.stack_trace}")

    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of errors handled."""
        return {
            'total_errors': len(self.errors),
            'error_counts_by_category': self.error_counts.copy(),
            'recent_errors': [
                error.to_dict() for error in self.errors[-10:]  # Last 10 errors
            ],
        }


def error_handler(
    component: str,
    operation: Optional[str] = None,
    severity: ErrorSeverity = ErrorSeverity.ERROR,
    retryable: bool = False,
    suggested_action: Optional[str] = None
):
    """
    Decorator for standardized error handling.

    Args:
        component: Component name for error context
        operation: Operation name (defaults to function name)
        severity: Error severity level
        retryable: Whether operation can be retried
        suggested_action: Suggested recovery action
    """
    def decorator(func: Callable):
        op_name = operation or func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            handler = ErrorHandler(component)
            try:
                return func(*args, **kwargs)
            except Exception as e:
                std_error = handler.handle_error(
                    error=e,
                    operation=op_name,
                    severity=severity,
                    retryable=retryable,
                    suggested_action=suggested_action,
                )
                raise SwarmError(
                    std_error.message,
                    std_error.category,
                    std_error.severity,
                    std_error.context,
                    std_error.original_exception,
                    std_error.retryable,
                    std_error.suggested_action,
                ) from e

        return wrapper
    return decorator


@contextmanager
def error_context(component: str, operation: str, **metadata):
    """
    Context manager for error handling.

    Usage:
        with error_context("messaging", "send_message", user_id="agent-1"):
            # Risky operation
            pass
    """
    handler = ErrorHandler(component)
    try:
        yield
    except Exception as e:
        handler.handle_error(
            error=e,
            operation=operation,
            metadata=metadata,
        )
        raise


class RetryMechanism:
    """
    Standardized retry mechanism for operations.
    """

    def __init__(
        self,
        max_attempts: int = 3,
        backoff_factor: float = 1.0,
        max_delay: float = 60.0,
        jitter: bool = True
    ):
        self.max_attempts = max_attempts
        self.backoff_factor = backoff_factor
        self.max_delay = max_delay
        self.jitter = jitter
        self.logger = logging.getLogger(__name__)

    def retry(
        self,
        func: Callable,
        *args,
        retryable_errors: Tuple[Type[Exception], ...] = (Exception,),
        **kwargs
    ) -> Any:
        """
        Retry a function with exponential backoff.

        Args:
            func: Function to retry
            retryable_errors: Exception types that should trigger retry
            *args, **kwargs: Arguments to pass to function

        Returns:
            Function result

        Raises:
            Last exception if all retries exhausted
        """
        last_exception = None

        for attempt in range(self.max_attempts):
            try:
                return func(*args, **kwargs)
            except retryable_errors as e:
                last_exception = e
                if attempt < self.max_attempts - 1:
                    delay = min(
                        self.backoff_factor * (2 ** attempt),
                        self.max_delay
                    )
                    self.logger.warning(
                        f"Attempt {attempt + 1} failed, retrying in {delay:.2f}s: {e}"
                    )
                    time.sleep(delay)
                else:
                    self.logger.error(
                        f"All {self.max_attempts} attempts failed: {e}"
                    )

        raise last_exception


# Global error handler instances
default_error_handler = ErrorHandler("swarm_system")
retry_mechanism = RetryMechanism()


__all__ = [
    "ErrorSeverity",
    "ErrorCategory",
    "ErrorContext",
    "StandardizedError",
    "SwarmError",
    "ConfigurationError",
    "NetworkError",
    "DatabaseError",
    "ValidationError",
    "AuthenticationError",
    "AuthorizationError",
    "BusinessLogicError",
    "ExternalServiceError",
    "ErrorHandler",
    "error_handler",
    "error_context",
    "RetryMechanism",
    "default_error_handler",
    "retry_mechanism",
]