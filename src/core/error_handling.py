#!/usr/bin/env python3
"""
Centralized Error Handling Framework - Agent Cellphone V2
========================================================

Unified error handling patterns to eliminate inconsistent error handling
across 743+ files with 5612+ try/except blocks.

<!-- SSOT Domain: core -->

Author: Agent-1 (Integration & Core Systems)
Date: 2026-01-11

Usage:
    # Replace inconsistent error handling with standardized patterns

    from core.error_handling import ErrorHandler, handle_errors

    # Method 1: Decorator
    @handle_errors(log_errors=True, reraise=True)
    def risky_operation():
        # Your code here
        pass

    # Method 2: Context manager
    with ErrorHandler.handle_errors("operation context"):
        # Your code here
        pass

    # Method 3: Safe execution
    result = ErrorHandler.safe_execute(risky_operation, default_return=None)
"""

import asyncio
import functools
import inspect
import logging
import sys
import time
import traceback
from contextlib import contextmanager
from typing import Any, Callable, Dict, Optional, Type, TypeVar, Union
from dataclasses import dataclass

from .logging_utils import get_logger

T = TypeVar('T')
logger = get_logger(__name__)


@dataclass
class ErrorContext:
    """Context information for error handling."""
    operation: str
    component: str = ""
    user_id: Optional[str] = None
    request_id: Optional[str] = None
    extra_data: Optional[Dict[str, Any]] = None


class ErrorHandler:
    """
    Centralized error handling framework.

    Eliminates 5612+ inconsistent try/except blocks across 743+ files.
    """

    @staticmethod
    def safe_execute(
        func: Callable[..., T],
        *args,
        default_return: T = None,
        log_errors: bool = True,
        reraise: bool = False,
        context: Optional[str] = None,
        **kwargs
    ) -> T:
        """
        Execute a function safely with error handling.

        Replaces the common pattern:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error: {e}")
                return default_return
        """
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if log_errors:
                error_msg = f"Error in {func.__name__}"
                if context:
                    error_msg += f" ({context})"
                error_msg += f": {e}"

                logger.error(error_msg, exc_info=True)

            if reraise:
                raise

            return default_return

    @staticmethod
    async def safe_execute_async(
        coro,
        default_return: Any = None,
        log_errors: bool = True,
        reraise: bool = False,
        context: Optional[str] = None
    ) -> Any:
        """
        Execute an async function safely with error handling.
        """
        try:
            return await coro
        except Exception as e:
            if log_errors:
                error_msg = f"Async error"
                if context:
                    error_msg += f" ({context})"
                error_msg += f": {e}"

                logger.error(error_msg, exc_info=True)

            if reraise:
                raise

            return default_return

    @staticmethod
    @contextmanager
    def handle_errors(
        operation: str = "operation",
        log_errors: bool = True,
        reraise: bool = False,
        component: str = "",
        error_types: Optional[tuple[Type[Exception], ...]] = None
    ):
        """
        Context manager for error handling.

        Usage:
            with ErrorHandler.handle_errors("database operation"):
                # Your code here
                pass
        """
        start_time = time.time()

        try:
            yield
        except error_types or Exception as e:
            duration = time.time() - start_time

            if log_errors:
                error_msg = f"Error in {operation}"
                if component:
                    error_msg += f" ({component})"
                error_msg += f" after {duration:.2f}s: {e}"

                logger.error(error_msg, exc_info=True)

            if reraise:
                raise
        else:
            # Log successful operations if they took long
            duration = time.time() - start_time
            if duration > 5.0:  # Log operations taking more than 5 seconds
                logger.info(f"Operation '{operation}' completed successfully in {duration:.2f}s")

    @staticmethod
    def handle_with_retry(
        max_retries: int = 3,
        backoff_factor: float = 1.0,
        exceptions: tuple[Type[Exception], ...] = (Exception,),
        log_retries: bool = True
    ) -> Callable:
        """
        Decorator for retry logic with exponential backoff.

        Replaces manual retry loops found throughout the codebase.
        """
        def decorator(func: Callable[..., T]) -> Callable[..., T]:
            @functools.wraps(func)
            def wrapper(*args, **kwargs) -> T:
                last_exception = None

                for attempt in range(max_retries + 1):
                    try:
                        return func(*args, **kwargs)
                    except exceptions as e:
                        last_exception = e

                        if attempt < max_retries:
                            delay = backoff_factor * (2 ** attempt)

                            if log_retries:
                                logger.warning(
                                    f"Attempt {attempt + 1}/{max_retries + 1} failed for "
                                    f"{func.__name__}: {e}. Retrying in {delay:.1f}s..."
                                )

                            time.sleep(delay)
                        else:
                            if log_retries:
                                logger.error(
                                    f"All {max_retries + 1} attempts failed for "
                                    f"{func.__name__}: {e}"
                                )
                            raise last_exception

                # This should never be reached, but just in case
                raise last_exception

            return wrapper
        return decorator

    @staticmethod
    def handle_async_with_retry(
        max_retries: int = 3,
        backoff_factor: float = 1.0,
        exceptions: tuple[Type[Exception], ...] = (Exception,),
        log_retries: bool = True
    ) -> Callable:
        """
        Decorator for async retry logic with exponential backoff.
        """
        def decorator(func: Callable[..., T]) -> Callable[..., T]:
            @functools.wraps(func)
            async def wrapper(*args, **kwargs) -> T:
                last_exception = None

                for attempt in range(max_retries + 1):
                    try:
                        return await func(*args, **kwargs)
                    except exceptions as e:
                        last_exception = e

                        if attempt < max_retries:
                            delay = backoff_factor * (2 ** attempt)

                            if log_retries:
                                logger.warning(
                                    f"Async attempt {attempt + 1}/{max_retries + 1} failed for "
                                    f"{func.__name__}: {e}. Retrying in {delay:.1f}s..."
                                )

                            await asyncio.sleep(delay)
                        else:
                            if log_retries:
                                logger.error(
                                    f"All {max_retries + 1} async attempts failed for "
                                    f"{func.__name__}: {e}"
                                )
                            raise last_exception

                # This should never be reached, but just in case
                raise last_exception

            return wrapper
        return decorator

    @staticmethod
    def log_and_raise(
        error: Exception,
        context: str = "",
        level: str = "ERROR",
        include_traceback: bool = True
    ) -> None:
        """
        Standardized error logging before re-raising.

        Ensures consistent error logging across the application.
        """
        log_method = getattr(logger, level.lower(), logger.error)

        error_msg = f"Error"
        if context:
            error_msg += f" in {context}"
        error_msg += f": {error}"

        if include_traceback:
            log_method(error_msg, exc_info=True)
        else:
            log_method(error_msg)

        raise error

    @staticmethod
    def create_error_context(
        operation: str,
        component: str = "",
        user_id: Optional[str] = None,
        request_id: Optional[str] = None,
        extra_data: Optional[Dict[str, Any]] = None
    ) -> ErrorContext:
        """Create an error context for structured error handling."""
        return ErrorContext(
            operation=operation,
            component=component,
            user_id=user_id,
            request_id=request_id,
            extra_data=extra_data or {}
        )

    @staticmethod
    def handle_with_context(
        context: ErrorContext,
        log_errors: bool = True,
        reraise: bool = True
    ) -> Callable:
        """
        Decorator that includes error context in logging.
        """
        def decorator(func: Callable[..., T]) -> Callable[..., T]:
            @functools.wraps(func)
            def wrapper(*args, **kwargs) -> T:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if log_errors:
                        # Create enriched error message with context
                        error_msg = f"Error in {context.operation}"
                        if context.component:
                            error_msg += f" ({context.component})"
                        if context.user_id:
                            error_msg += f" for user {context.user_id}"
                        if context.request_id:
                            error_msg += f" [request {context.request_id}]"
                        error_msg += f": {e}"

                        # Add extra context data to log
                        extra_data = {
                            "operation": context.operation,
                            "component": context.component,
                            "user_id": context.user_id,
                            "request_id": context.request_id,
                            **context.extra_data
                        }

                        logger.error(error_msg, extra=extra_data, exc_info=True)

                    if reraise:
                        raise

                    return None

            return wrapper
        return decorator


# Convenience decorators for easy importing
def handle_errors(
    operation: str = "operation",
    log_errors: bool = True,
    reraise: bool = False,
    component: str = "",
    error_types: Optional[tuple[Type[Exception], ...]] = None
) -> Callable:
    """
    Convenience decorator for error handling.

    Usage:
        @handle_errors("database query", reraise=True)
        def get_user_data(user_id):
            # Your code here
            pass
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            with ErrorHandler.handle_errors(
                operation=operation,
                log_errors=log_errors,
                reraise=reraise,
                component=component,
                error_types=error_types
            ):
                return func(*args, **kwargs)
        return wrapper
    return decorator


def retry_on_failure(
    max_retries: int = 3,
    backoff_factor: float = 1.0,
    exceptions: tuple[Type[Exception], ...] = (Exception,),
    async_mode: bool = False
) -> Callable:
    """
    Convenience decorator for retry logic.

    Usage:
        @retry_on_failure(max_retries=5)
        def unreliable_api_call():
            # Your code here
            pass

        @retry_on_failure(max_retries=3, async_mode=True)
        async def unreliable_async_call():
            # Your code here
            pass
    """
    if async_mode:
        return ErrorHandler.handle_async_with_retry(
            max_retries=max_retries,
            backoff_factor=backoff_factor,
            exceptions=exceptions
        )
    else:
        return ErrorHandler.handle_with_retry(
            max_retries=max_retries,
            backoff_factor=backoff_factor,
            exceptions=exceptions
        )


# Migration helpers
def migrate_error_handling():
    """
    Helper function to assist with migrating existing error handling code.

    This can be used to find and replace old error handling patterns.
    """
    print("🔍 Error Handling Migration Helper")
    print("Replace these patterns:")
    print()
    print("OLD PATTERN 1:")
    print("  try:")
    print("      result = risky_operation()")
    print("  except Exception as e:")
    print("      logger.error(f'Error: {e}')")
    print("      return None")
    print()
    print("NEW PATTERN 1:")
    print("  from core.error_handling import ErrorHandler")
    print("  result = ErrorHandler.safe_execute(risky_operation, default_return=None)")
    print()
    print("OLD PATTERN 2:")
    print("  try:")
    print("      # multi-line operation")
    print("      pass")
    print("  except Exception as e:")
    print("      logger.error(f'Operation failed: {e}')")
    print("      raise")
    print()
    print("NEW PATTERN 2:")
    print("  from core.error_handling import ErrorHandler")
    print("  with ErrorHandler.handle_errors('operation name', reraise=True):")
    print("      # multi-line operation")
    print("      pass")
    print()
    print("Benefits:")
    print("  ✅ Consistent error handling across all services")
    print("  ✅ Automatic retry logic with backoff")
    print("  ✅ Structured error context")
    print("  ✅ Configurable logging and re-raising")


__all__ = [
    "ErrorHandler",
    "ErrorContext",
    "handle_errors",
    "retry_on_failure",
    "migrate_error_handling",
]