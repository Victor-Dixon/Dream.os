"""
<!-- SSOT Domain: core -->

Recovery Strategies Module
===========================

Concrete recovery strategy implementations extracted for V2 compliance.

Author: Agent-2 - Architecture & Design Specialist (V2 Refactor)
License: MIT
"""

import logging
from collections.abc import Callable
from datetime import datetime, timedelta

from .error_handling_core import ErrorContext, ErrorSeverity
from typing import Dict, List, Callable, Any, Optional, Union, Tuple, Set


logger = logging.getLogger(__name__)


class RecoveryStrategy:
    """Base class for error recovery strategies."""

    def __init__(self, name: str, description: str = ""):
        """Initialize recovery strategy."""
        self.name = name
        self.description = description or name

    def can_recover(self, error_context: ErrorContext) -> bool:
        """Check if this strategy can recover from the error."""
        raise NotImplementedError("Subclasses must implement can_recover")

    def execute_recovery(self, error_context: ErrorContext) -> bool:
        """Execute the recovery strategy."""
        raise NotImplementedError("Subclasses must implement execute_recovery")


class ServiceRestartStrategy(RecoveryStrategy):
    """Strategy for restarting failed services."""

    def __init__(self, service_manager: Callable):
        """Initialize service restart strategy."""
        super().__init__("service_restart", "Restart failed service components")
        self.service_manager = service_manager
        self.last_restart = None
        self.restart_cooldown = timedelta(minutes=5)

    def can_recover(self, error_context: ErrorContext) -> bool:
        """Check if service restart is appropriate."""
        if self.last_restart and datetime.now() - self.last_restart < self.restart_cooldown:
            return False
        return error_context.severity in [ErrorSeverity.HIGH, ErrorSeverity.CRITICAL]

    def execute_recovery(self, error_context: ErrorContext) -> bool:
        """Execute service restart."""
        try:
            logger.info(f"Executing service restart for {error_context.operation}")
            success = self.service_manager()
            if success:
                self.last_restart = datetime.now()
                logger.info(f"Service restart successful for {error_context.operation}")
            return success
        except Exception as e:
            logger.error(f"Service restart failed: {e}")
            return False


class ConfigurationResetStrategy(RecoveryStrategy):
    """Strategy for resetting configuration to defaults."""

    def __init__(self, config_reset_func: Callable):
        """Initialize configuration reset strategy."""
        super().__init__("config_reset", "Reset configuration to safe defaults")
        self.config_reset_func = config_reset_func

    def can_recover(self, error_context: ErrorContext) -> bool:
        """Check if configuration reset is appropriate."""
        return (
            "config" in error_context.operation.lower()
            or error_context.severity == ErrorSeverity.CRITICAL
        )

    def execute_recovery(self, error_context: ErrorContext) -> bool:
        """Execute configuration reset."""
        try:
            logger.info(f"Executing configuration reset for {error_context.operation}")
            success = self.config_reset_func()
            if success:
                logger.info(f"Configuration reset successful for {error_context.operation}")
            return success
        except Exception as e:
            logger.error(f"Configuration reset failed: {e}")
            return False


class ResourceCleanupStrategy(RecoveryStrategy):
    """Strategy for cleaning up stuck resources."""

    def __init__(self, cleanup_func: Callable):
        """Initialize resource cleanup strategy."""
        super().__init__("resource_cleanup", "Clean up stuck resources and locks")
        self.cleanup_func = cleanup_func

    def can_recover(self, error_context: ErrorContext) -> bool:
        """Check if resource cleanup is appropriate."""
        error_data = str(error_context.additional_data).lower()
        return "resource" in error_data or "lock" in error_data

    def execute_recovery(self, error_context: ErrorContext) -> bool:
        """Execute resource cleanup."""
        try:
            logger.info(f"Executing resource cleanup for {error_context.operation}")
            success = self.cleanup_func()
            if success:
                logger.info(f"Resource cleanup successful for {error_context.operation}")
            return success
        except Exception as e:
            logger.error(f"Resource cleanup failed: {e}")
            return False


class RetryStrategy(RecoveryStrategy):
    """Strategy for retrying failed operations with exponential backoff."""

    def __init__(self, operation_func: Callable, max_retries: int = 3, base_delay: float = 1.0):
        """Initialize retry strategy."""
        super().__init__("retry", "Retry failed operation with exponential backoff")
        self.operation_func = operation_func
        self.max_retries = max_retries
        self.base_delay = base_delay

    def can_recover(self, error_context: ErrorContext) -> bool:
        """Check if retry is appropriate."""
        import time
        # Retry for transient errors (network, timeout, temporary failures)
        error_type = error_context.error_type.lower()
        transient_errors = ["timeout", "connection", "network", "temporary", "retryable"]
        return any(err in error_type for err in transient_errors) or error_context.severity in [
            ErrorSeverity.LOW,
            ErrorSeverity.MEDIUM,
        ]

    def execute_recovery(self, error_context: ErrorContext) -> bool:
        """Execute retry with exponential backoff."""
        import time
        try:
            logger.info(f"Executing retry strategy for {error_context.operation}")
            for attempt in range(self.max_retries):
                delay = self.base_delay * (2 ** attempt)
                if attempt > 0:
                    logger.info(f"Retry attempt {attempt + 1}/{self.max_retries} after {delay:.1f}s delay")
                    time.sleep(delay)
                try:
                    result = self.operation_func()
                    logger.info(f"Retry successful on attempt {attempt + 1} for {error_context.operation}")
                    return True
                except Exception as retry_error:
                    logger.warning(f"Retry attempt {attempt + 1} failed: {retry_error}")
                    if attempt == self.max_retries - 1:
                        logger.error(f"All retry attempts exhausted for {error_context.operation}")
            return False
        except Exception as e:
            logger.error(f"Retry strategy failed: {e}")
            return False


class FallbackStrategy(RecoveryStrategy):
    """Strategy for falling back to alternative operation."""

    def __init__(self, primary_func: Callable, fallback_func: Callable):
        """Initialize fallback strategy."""
        super().__init__("fallback", "Fall back to alternative operation")
        self.primary_func = primary_func
        self.fallback_func = fallback_func

    def can_recover(self, error_context: ErrorContext) -> bool:
        """Check if fallback is appropriate."""
        # Fallback is appropriate for most errors if alternative exists
        return error_context.severity != ErrorSeverity.CRITICAL

    def execute_recovery(self, error_context: ErrorContext) -> bool:
        """Execute fallback operation."""
        try:
            logger.info(f"Executing fallback strategy for {error_context.operation}")
            result = self.fallback_func()
            logger.info(f"Fallback successful for {error_context.operation}")
            return True
        except Exception as e:
            logger.error(f"Fallback also failed for {error_context.operation}: {e}")
            return False


class TimeoutStrategy(RecoveryStrategy):
    """Strategy for handling timeout errors."""

    def __init__(self, operation_func: Callable, extended_timeout: float = 60.0):
        """Initialize timeout strategy."""
        super().__init__("timeout", "Retry with extended timeout")
        self.operation_func = operation_func
        self.extended_timeout = extended_timeout

    def can_recover(self, error_context: ErrorContext) -> bool:
        """Check if timeout strategy is appropriate."""
        error_type = error_context.error_type.lower()
        error_data = str(error_context.additional_data).lower()
        return "timeout" in error_type or "timeout" in error_data

    def execute_recovery(self, error_context: ErrorContext) -> bool:
        """Execute operation with extended timeout."""
        import signal
        import time

        def timeout_handler(signum, frame):
            raise TimeoutError(f"Operation timed out after {self.extended_timeout}s")

        try:
            logger.info(f"Executing timeout strategy for {error_context.operation} (timeout: {self.extended_timeout}s)")
            # Set up timeout
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(int(self.extended_timeout))

            try:
                result = self.operation_func()
                signal.alarm(0)  # Cancel timeout
                logger.info(f"Timeout strategy successful for {error_context.operation}")
                return True
            except TimeoutError:
                logger.error(f"Operation still timed out with extended timeout for {error_context.operation}")
                return False
            finally:
                signal.alarm(0)  # Always cancel timeout
        except Exception as e:
            logger.error(f"Timeout strategy failed for {error_context.operation}: {e}")
            return False


class GracefulDegradationStrategy(RecoveryStrategy):
    """Strategy for graceful degradation when full functionality unavailable."""

    def __init__(self, degraded_func: Callable):
        """Initialize graceful degradation strategy."""
        super().__init__("graceful_degradation", "Degrade to reduced functionality")
        self.degraded_func = degraded_func

    def can_recover(self, error_context: ErrorContext) -> bool:
        """Check if graceful degradation is appropriate."""
        # Degradation is appropriate when full functionality fails but reduced functionality is available
        return error_context.severity in [ErrorSeverity.MEDIUM, ErrorSeverity.HIGH]

    def execute_recovery(self, error_context: ErrorContext) -> bool:
        """Execute degraded operation."""
        try:
            logger.info(f"Executing graceful degradation for {error_context.operation}")
            result = self.degraded_func()
            logger.info(f"Graceful degradation successful for {error_context.operation}")
            return True
        except Exception as e:
            logger.error(f"Graceful degradation failed for {error_context.operation}: {e}")
            return False