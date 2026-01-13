#!/usr/bin/env python3
"""
Standardized Logging Mixin - Phase 1 Refactoring
===============================================

PHASE 1 EXECUTION: Logging standardization across all services
Implements consistent logger acquisition and logging patterns.

This mixin provides:
- Standardized logger naming using __name__
- Consistent log level handling
- Structured logging methods
- Performance-optimized logging

V2 Compliance: Standardized logging infrastructure
SOLID Principles: Single Responsibility (logging only)
SSOT: Centralized logging configuration

Author: Agent-1 (Infrastructure & Core Systems)
Date: 2026-01-12
"""

import logging
import sys
from typing import Any, Optional
from pathlib import Path


class LoggingMixin:
    """
    Standardized logging mixin for consistent logger acquisition and usage.

    PHASE 1 EXECUTION: Replaces inconsistent logging patterns across ~492 service files.

    Usage:
        class MyService(LoggingMixin):
            def __init__(self):
                super().__init__()
                # Logger automatically available as self.logger

            def some_method(self):
                self.logger.info("Operation started")
                self.logger.error("Error occurred", exc_info=True)
    """

    def __init__(self, logger_name: Optional[str] = None):
        """
        Initialize standardized logging.

        Args:
            logger_name: Optional custom logger name. Defaults to __name__ of the class.
        """
        # Use class __name__ for consistent logger naming
        if logger_name is None:
            logger_name = self.__class__.__module__

        self.logger = logging.getLogger(logger_name)

        # Ensure logger has handlers (fallback to basic config)
        if not self.logger.handlers:
            self._setup_basic_logging()

    def _setup_basic_logging(self):
        """Setup basic logging configuration as fallback."""
        # Only setup if no handlers exist anywhere in the hierarchy
        root_logger = logging.getLogger()
        if not root_logger.handlers:
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                stream=sys.stdout
            )

    def log_method_entry(self, method_name: str, *args, **kwargs):
        """
        Log method entry with parameters (for debugging).

        Args:
            method_name: Name of the method being entered
            *args: Positional arguments (sensitive data will be masked)
            **kwargs: Keyword arguments (sensitive data will be masked)
        """
        # Mask sensitive information
        safe_args = self._mask_sensitive_data(args)
        safe_kwargs = self._mask_sensitive_data(kwargs)

        self.logger.debug(
            f"Entering {method_name}",
            extra={
                'method': method_name,
                'args_count': len(safe_args),
                'kwargs_keys': list(safe_kwargs.keys()) if safe_kwargs else []
            }
        )

    def log_method_exit(self, method_name: str, result: Any = None, duration_ms: Optional[float] = None):
        """
        Log method exit with optional result and duration.

        Args:
            method_name: Name of the method exiting
            result: Method result (will be masked if sensitive)
            duration_ms: Execution duration in milliseconds
        """
        safe_result = self._mask_sensitive_data(result)

        log_data = {
            'method': method_name,
            'has_result': result is not None
        }

        if duration_ms is not None:
            log_data['duration_ms'] = duration_ms

        self.logger.debug(f"Exiting {method_name}", extra=log_data)

    def log_performance(self, operation: str, duration_ms: float, metadata: Optional[dict] = None):
        """
        Log performance metrics.

        Args:
            operation: Name of the operation
            duration_ms: Duration in milliseconds
            metadata: Additional performance metadata
        """
        log_data = {
            'operation': operation,
            'duration_ms': duration_ms,
            'performance_threshold': 1000  # 1 second threshold
        }

        if metadata:
            log_data.update(metadata)

        if duration_ms > 1000:  # Log as warning if slow
            self.logger.warning(f"Slow operation: {operation}", extra=log_data)
        else:
            self.logger.info(f"Operation completed: {operation}", extra=log_data)

    def log_error_with_context(self, error: Exception, context: Optional[dict] = None,
                              operation: Optional[str] = None):
        """
        Log error with full context and stack trace.

        Args:
            error: The exception that occurred
            context: Additional context information
            operation: Name of the operation where error occurred
        """
        log_data = {
            'error_type': type(error).__name__,
            'error_message': str(error),
            'operation': operation or 'unknown'
        }

        if context:
            # Filter out sensitive context keys
            safe_context = {k: v for k, v in context.items()
                           if not self._is_sensitive_key(k)}
            log_data['context'] = safe_context

        self.logger.error(
            f"Error in {operation or 'operation'}: {error}",
            exc_info=True,
            extra=log_data
        )

    def _mask_sensitive_data(self, data: Any) -> Any:
        """
        Mask sensitive data in logs.

        Args:
            data: Data to mask

        Returns:
            Masked data safe for logging
        """
        if isinstance(data, dict):
            return {k: self._mask_value(k, v) for k, v in data.items()}
        elif isinstance(data, (list, tuple)):
            return [self._mask_sensitive_data(item) for item in data]
        else:
            return self._mask_value(None, data)

    def _mask_value(self, key: Optional[str], value: Any) -> Any:
        """
        Mask individual values if they appear sensitive.

        Args:
            key: Dictionary key (if applicable)
            value: Value to potentially mask

        Returns:
            Masked value or original value
        """
        if self._is_sensitive_key(key) or self._is_sensitive_value(value):
            return "***MASKED***"
        return value

    def _is_sensitive_key(self, key: Optional[str]) -> bool:
        """
        Check if a key represents sensitive information.

        Args:
            key: Key to check

        Returns:
            True if key is sensitive
        """
        if not key:
            return False

        sensitive_keys = {
            'password', 'token', 'secret', 'key', 'auth',
            'credential', 'private', 'sensitive', 'api_key',
            'access_token', 'refresh_token', 'session_key'
        }

        key_lower = key.lower()
        return any(sensitive in key_lower for sensitive in sensitive_keys)

    def _is_sensitive_value(self, value: Any) -> bool:
        """
        Check if a value appears to be sensitive data.

        Args:
            value: Value to check

        Returns:
            True if value appears sensitive
        """
        if not isinstance(value, str):
            return False

        # Check for patterns that indicate sensitive data
        sensitive_patterns = [
            r'Bearer\s+[A-Za-z0-9\-_\.]+',  # Bearer tokens
            r'eyJ[A-Za-z0-9\-_\.]+',        # JWT tokens
            r'[A-Za-z0-9]{32,}',           # Long alphanumeric strings (potential keys)
        ]

        import re
        for pattern in sensitive_patterns:
            if re.search(pattern, value):
                return True

        return False


# Utility functions for standardized logging setup
def setup_service_logging(service_name: str, log_level: str = "INFO",
                         log_file: Optional[Path] = None) -> logging.Logger:
    """
    Setup standardized logging for a service.

    Args:
        service_name: Name of the service
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(service_name)

    # Clear existing handlers to avoid duplication
    logger.handlers.clear()

    # Set log level
    level_map = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    logger.setLevel(level_map.get(log_level.upper(), logging.INFO))

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Add file handler if specified
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a standardized logger instance.

    This is the recommended way to get loggers throughout the codebase.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


# Export convenience functions
__all__ = [
    'LoggingMixin',
    'setup_service_logging',
    'get_logger'
]