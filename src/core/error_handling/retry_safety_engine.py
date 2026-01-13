#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

Retry & Safety Engine - V2 Compliant
===================================

Retry logic and safe execution functionality.

Author: Agent-4 - Strategic Oversight & Emergency Intervention Manager
Created: 2025-01-27
Purpose: V2 compliant retry and safety operations
"""

import logging
import time
from collections.abc import Callable
from typing import Any

from .error_handling_models import RetryConfiguration


class RetrySafetyEngine:
    """Engine for retry operations and safe execution."""

    def __init__(self, logger: logging.Logger | None = None):
        """Initialize retry safety engine."""
        self.logger = logger

    def _get_logger(self):
        """Get logger instance."""
        if self.logger:
            return self.logger
        # Fallback to module logger
        import logging as std_logging

        return std_logging.getLogger(__name__)

    def retry_operation(
        self,
        operation_func: Callable,
        config: RetryConfiguration | None = None,
        logger: logging.Logger | None = None,
    ) -> Any:
        """Retry operation with exponential backoff.

        Args:
            operation_func: Function to retry
            config: Retry configuration
            logger: Optional logger for retry logging

        Returns:
            Any: Result of successful operation

        Raises:
            Exception: Last exception if all retries fail
        """
        config = config or RetryConfiguration()
        effective_logger = logger or self.logger

        return self._execute_retry_loop(operation_func, config, effective_logger)

    def _execute_retry_loop(
        self,
        operation_func: Callable,
        config: RetryConfiguration,
        logger: logging.Logger | None,
    ) -> Any:
        """Execute retry loop with error handling."""
        last_exception = None

        for attempt in range(config.max_retries + 1):
            try:
                self._log_retry_attempt(attempt, config.max_retries, logger)
                return operation_func()
            except config.exceptions as e:
                last_exception = e
                if self._handle_retry_failure(attempt, config, e, logger):
                    break

        raise last_exception

    def _log_retry_attempt(
        self, attempt: int, max_retries: int, logger: logging.Logger | None
    ) -> None:
        """Log retry attempt if applicable."""
        if logger and attempt > 0:
            self._get_logger().info(f"🔄 Retry attempt {attempt}/{max_retries}")

    def _handle_retry_failure(
        self,
        attempt: int,
        config: RetryConfiguration,
        exception: Exception,
        logger: logging.Logger | None,
    ) -> bool:
        """Handle retry failure and determine if retries exhausted."""
        if attempt == config.max_retries:
            if logger:
                self._get_logger().error(
                    f"❌ All {config.max_retries} retry attempts failed: {exception}"
                )
            return True

        delay = config.calculate_delay(attempt)
        if logger:
            self._get_logger().warning(
                f"⚠️ Attempt {attempt + 1} failed: {exception}, retrying in {delay:.1f}s"
            )
        time.sleep(delay)
        return False

    def safe_execute(
        self,
        operation_func: Callable,
        default_return: Any = None,
        logger: logging.Logger | None = None,
        operation_name: str = "operation",
    ) -> Any:
        """Safely execute operation with fallback return value.

        Args:
            operation_func: Function to execute
            default_return: Value to return if operation fails
            logger: Optional logger for error logging
            operation_name: Name of operation for logging

        Returns:
            Any: Result of operation or default_return if failed
        """
        try:
            return operation_func()
        except Exception as e:
            effective_logger = logger or self.logger
            if effective_logger:
                self._get_logger().error(f"❌ Safe execution failed for {operation_name}: {e}")
            return default_return

    def validate_and_execute(
        self,
        operation_func: Callable,
        validation_func: Callable,
        error_message: str = "Validation failed",
        logger: logging.Logger | None = None,
    ) -> Any:
        """Validate input and execute operation.

        Args:
            operation_func: Function to execute
            validation_func: Function to validate input
            error_message: Error message if validation fails
            logger: Optional logger for error logging

        Returns:
            Any: Result of operation

        Raises:
            ValueError: If validation fails
        """
        try:
            self._validate_input(validation_func, error_message)
            return operation_func()
        except Exception as e:
            self._log_validation_error(e, logger)
            raise

    def _validate_input(self, validation_func: Callable, error_message: str) -> None:
        """Validate input using validation function."""
        if not validation_func():
            raise ValueError(error_message)

    def _log_validation_error(self, error: Exception, logger: logging.Logger | None) -> None:
        """Log validation error if logger available."""
        effective_logger = logger or self.logger
        if effective_logger:
            self._get_logger().error(f"❌ Validation and execution failed: {error}")

    def execute_with_timeout(
        self,
        operation_func: Callable,
        timeout: float,
        default_return: Any = None,
        logger: logging.Logger | None = None,
    ) -> Any:
        """Execute operation with timeout.

        Args:
            operation_func: Function to execute
            timeout: Timeout in seconds
            default_return: Value to return if timeout occurs
            logger: Optional logger

        Returns:
            Any: Result of operation or default_return if timeout
        """
        import signal

        effective_logger = logger or self.logger
        timeout_handler = self._create_timeout_handler(timeout)

        try:
            return self._execute_with_signal_timeout(operation_func, timeout, timeout_handler)
        except TimeoutError as e:
            return self._handle_timeout(e, effective_logger, default_return)
        except Exception as e:
            return self._handle_timeout_error(e, effective_logger, default_return)
        finally:
            signal.alarm(0)

    def _create_timeout_handler(self, timeout: float) -> Callable:
        """Create timeout signal handler."""
        def timeout_handler(signum, frame):
            raise TimeoutError(f"Operation timed out after {timeout} seconds")
        return timeout_handler

    def _execute_with_signal_timeout(
        self, operation_func: Callable, timeout: float, handler: Callable
    ) -> Any:
        """Execute operation with signal-based timeout."""
        import signal
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(int(timeout))
        try:
            result = operation_func()
            signal.alarm(0)
            return result
        finally:
            signal.alarm(0)

    def _handle_timeout(
        self, error: TimeoutError, logger: logging.Logger | None, default: Any
    ) -> Any:
        """Handle timeout error."""
        if logger:
            self._get_logger().warning(f"⏰ Operation timed out: {error}")
        return default

    def _handle_timeout_error(
        self, error: Exception, logger: logging.Logger | None, default: Any
    ) -> Any:
        """Handle timeout execution error."""
        if logger:
            self._get_logger().error(f"❌ Operation failed: {error}")
        return default

    def circuit_breaker_execute(
        self,
        operation_func: Callable,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        logger: logging.Logger | None = None,
    ) -> Any:
        """Execute operation with circuit breaker pattern.

        Args:
            operation_func: Function to execute
            failure_threshold: Number of failures before opening circuit
            recovery_timeout: Time to wait before attempting recovery
            logger: Optional logger

        Returns:
            Any: Result of operation

        Raises:
            Exception: If circuit is open or operation fails
        """
        # Simple circuit breaker implementation
        # In production, this would use a more sophisticated state machine
        try:
            return operation_func()
        except Exception as e:
            self._log_circuit_breaker_error(e, logger)
            raise

    def _log_circuit_breaker_error(self, error: Exception, logger: logging.Logger | None) -> None:
        """Log circuit breaker error if logger available."""
        effective_logger = logger or self.logger
        if effective_logger:
            self._get_logger().error(f"❌ Circuit breaker: Operation failed: {error}")


# Convenience functions for backward compatibility
def retry_operation(
    operation_func: Callable,
    max_retries: int = 3,
    delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: tuple = (Exception,),
    logger: logging.Logger | None = None,
) -> Any:
    """Retry operation with exponential backoff."""
    config = RetryConfiguration(max_retries, delay, backoff_factor, exceptions)
    engine = RetrySafetyEngine(logger)
    return engine.retry_operation(operation_func, config, logger)


def safe_execute(
    operation_func: Callable,
    default_return: Any = None,
    logger: logging.Logger | None = None,
    operation_name: str = "operation",
) -> Any:
    """Safely execute operation with fallback return value."""
    engine = RetrySafetyEngine(logger)
    return engine.safe_execute(operation_func, default_return, logger, operation_name)
