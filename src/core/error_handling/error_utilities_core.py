#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

Error Utilities - V2 Compliant
===============================

Error utility functions and helper classes extracted from error_handling_core.py.

Author: Agent-3 (Infrastructure & DevOps Specialist)
V2 Compliant: <400 lines, ≤5 classes
"""

from typing import Any

from .error_enums import ErrorSeverity

# DUP-006/007 Coordination: Import Agent-2's standardized logging
try:
    from ..utilities.standardized_logging import LogLevel

    _LOGGING_AVAILABLE = True
except ImportError:
    _LOGGING_AVAILABLE = False


class RecoverableErrors:
    """Recoverable error types."""

    TYPES = (ConnectionError, TimeoutError, OSError, FileNotFoundError, PermissionError)


class ErrorSeverityMapping:
    """Error severity mapping."""

    CRITICAL = (SystemError, MemoryError, KeyboardInterrupt)
    HIGH = (ValueError, TypeError, AttributeError, KeyError)
    MEDIUM = (FileNotFoundError, PermissionError, ConnectionError)
    # All others are LOW severity


def get_log_level_for_severity(severity: ErrorSeverity) -> int:
    """Map ErrorSeverity to LogLevel for coordinated error/logging.

    DUP-006/007 Coordination: Integrates error handling with Agent-2's standardized logging.

    Args:
        severity: Error severity level

    Returns:
        Logging level (int) compatible with logging module
    """
    if _LOGGING_AVAILABLE:
        mapping = {
            ErrorSeverity.CRITICAL: LogLevel.CRITICAL.value,
            ErrorSeverity.HIGH: LogLevel.ERROR.value,
            ErrorSeverity.MEDIUM: LogLevel.WARNING.value,
            ErrorSeverity.LOW: LogLevel.INFO.value,
        }
        return mapping.get(severity, LogLevel.ERROR.value)
    else:
        # Fallback to standard logging levels
        import logging

        mapping = {
            ErrorSeverity.CRITICAL: logging.CRITICAL,
            ErrorSeverity.HIGH: logging.ERROR,
            ErrorSeverity.MEDIUM: logging.WARNING,
            ErrorSeverity.LOW: logging.INFO,
        }
        return mapping.get(severity, logging.ERROR)


def log_exception_with_severity(
    logger, severity: ErrorSeverity, exception: Exception, context: dict[str, Any] = None
) -> None:
    """Log exception with appropriate severity level.

    DUP-006/007 Coordination: Unified exception logging using Agent-2's standardized logging.

    Args:
        logger: Logger instance (from standardized_logging.get_logger)
        severity: Error severity level
        exception: Exception to log
        context: Additional context dictionary
    """
    log_level = get_log_level_for_severity(severity)
    context_str = f" | Context: {context}" if context else ""
    logger.log(
        log_level, f"Exception: {type(exception).__name__}: {exception}{context_str}", exc_info=True
    )


__all__ = [
    "RecoverableErrors",
    "ErrorSeverityMapping",
    "get_log_level_for_severity",
    "log_exception_with_severity",
]

