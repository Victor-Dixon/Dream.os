#!/usr/bin/env python3
"""
Error Utilities Module
=====================

Standardized error handling and logging for tools consolidation.
Provides unified exception handling, logging patterns, and error reporting.

Part of Phase 2A: Foundation Consolidation
Consolidates error handling patterns used across 15+ tools.

Author: Agent-7 (Tools Consolidation & Architecture Lead)
Date: 2026-01-13
"""

import logging
import traceback
import sys
from typing import Any, Optional, Callable, Dict, List
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

class ErrorUtils:
    """Unified error handling utilities for tools consolidation."""

    @staticmethod
    def safe_execute(func: Callable, *args, error_msg: str = "Operation failed",
                    log_level: str = "error", **kwargs) -> Any:
        """Safely execute a function with error handling.

        Args:
            func: Function to execute
            *args: Positional arguments for function
            error_msg: Error message to log on failure
            log_level: Logging level ('debug', 'info', 'warning', 'error', 'critical')
            **kwargs: Keyword arguments for function

        Returns:
            Function result or None on error
        """
        try:
            return func(*args, **kwargs)
        except Exception as e:
            ErrorUtils.log_error(e, error_msg, log_level)
            return None

    @staticmethod
    def log_error(error: Exception, context: str = "",
                 log_level: str = "error", include_traceback: bool = True) -> None:
        """Log an error with consistent formatting.

        Args:
            error: Exception object
            context: Additional context information
            log_level: Logging level
            include_traceback: Whether to include full traceback
        """
        error_msg = f"{context}: {str(error)}" if context else str(error)

        # Get the appropriate logger method
        log_method = getattr(logger, log_level.lower(), logger.error)

        log_method(error_msg)

        if include_traceback and log_level in ('error', 'critical'):
            logger.debug(f"Traceback for {error.__class__.__name__}: {traceback.format_exc()}")

    @staticmethod
    def create_error_report(error: Exception, operation: str = "",
                           additional_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a structured error report.

        Args:
            error: Exception that occurred
            operation: Operation being performed when error occurred
            additional_data: Additional context data

        Returns:
            Structured error report dictionary
        """
        return {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "error_type": error.__class__.__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc(),
            "python_version": sys.version,
            "platform": sys.platform,
            "additional_data": additional_data or {}
        }

    @staticmethod
    def handle_file_operation_error(error: Exception, file_path: str,
                                   operation: str = "file operation") -> None:
        """Handle file operation errors with appropriate messaging.

        Args:
            error: Exception that occurred
            file_path: Path that caused the error
            operation: Type of file operation
        """
        error_type = error.__class__.__name__

        if "PermissionError" in error_type:
            logger.error(f"Permission denied for {operation}: {file_path}")
        elif "FileNotFoundError" in error_type:
            logger.error(f"File not found for {operation}: {file_path}")
        elif "IsADirectoryError" in error_type:
            logger.error(f"Expected file but found directory: {file_path}")
        elif "OSError" in error_type:
            logger.error(f"OS error during {operation}: {file_path} - {str(error)}")
        else:
            ErrorUtils.log_error(error, f"Unexpected error during {operation}: {file_path}")

    @staticmethod
    def validate_function_args(func_name: str, required_args: List[str],
                             provided_kwargs: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate that required function arguments are provided.

        Args:
            func_name: Name of function being validated
            required_args: List of required argument names
            provided_kwargs: Dictionary of provided keyword arguments

        Returns:
            Tuple of (is_valid, missing_args_list)
        """
        missing_args = []
        for arg in required_args:
            if arg not in provided_kwargs:
                missing_args.append(arg)

        if missing_args:
            logger.error(f"{func_name}: Missing required arguments: {', '.join(missing_args)}")
            return False, missing_args

        return True, []

    @staticmethod
    def retry_operation(func: Callable, max_retries: int = 3,
                       delay: float = 1.0, backoff: float = 2.0,
                       *args, **kwargs) -> Any:
        """Retry an operation with exponential backoff.

        Args:
            func: Function to retry
            max_retries: Maximum number of retry attempts
            delay: Initial delay between retries
            backoff: Backoff multiplier for delay
            *args: Positional arguments for function
            **kwargs: Keyword arguments for function

        Returns:
            Function result or None on all failures
        """
        current_delay = delay

        for attempt in range(max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == max_retries:
                    logger.error(f"Operation failed after {max_retries} retries: {str(e)}")
                    return None

                logger.warning(f"Attempt {attempt + 1} failed, retrying in {current_delay}s: {str(e)}")
                import time
                time.sleep(current_delay)
                current_delay *= backoff

        return None

    @staticmethod
    def graceful_shutdown(signal_received: str = "", cleanup_funcs: Optional[List[Callable]] = None) -> None:
        """Perform graceful shutdown with cleanup.

        Args:
            signal_received: Signal that triggered shutdown
            cleanup_funcs: List of cleanup functions to call
        """
        logger.info(f"Initiating graceful shutdown{f' (signal: {signal_received})' if signal_received else ''}")

        if cleanup_funcs:
            for cleanup_func in cleanup_funcs:
                try:
                    cleanup_func()
                    logger.debug("Cleanup function executed successfully")
                except Exception as e:
                    logger.error(f"Error during cleanup: {str(e)}")

        logger.info("Shutdown complete")
        sys.exit(0)

# Convenience functions for backward compatibility
def safe_call(func: Callable, *args, error_msg: str = "Operation failed", **kwargs) -> Any:
    """Legacy function for safe_execute."""
    return ErrorUtils.safe_execute(func, *args, error_msg=error_msg, **kwargs)

def log_exception(error: Exception, context: str = "") -> None:
    """Legacy function for log_error."""
    ErrorUtils.log_error(error, context)