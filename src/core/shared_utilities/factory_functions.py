"""
<!-- SSOT Domain: core -->

Factory Functions - Utility Instance Creation
=============================================

Convenience functions for creating utility instances.

Author: Agent-6 (Coordination & Communication Specialist)
Refactored: Agent-1 (Integration & Core Systems Specialist) - 2025-12-04
License: MIT
"""

from .cleanup_manager import CleanupManager
from .configuration_manager_util import ConfigurationManagerUtil
from .error_handler import ErrorHandler
from .initialization_manager import InitializationManager
from .logging_manager import LoggingManager
from .result_manager import ResultManager
from .status_manager import StatusManager
from .validation_manager import ValidationManager


def create_cleanup_manager() -> CleanupManager:
    """Create a new cleanup manager instance."""
    return CleanupManager()


def create_configuration_manager() -> ConfigurationManagerUtil:
    """Create a new configuration manager instance."""
    return ConfigurationManagerUtil()


def create_error_handler() -> ErrorHandler:
    """Create a new error handler instance."""
    return ErrorHandler()


def create_initialization_manager() -> InitializationManager:
    """Create a new initialization manager instance."""
    return InitializationManager()


def create_logging_manager() -> LoggingManager:
    """Create a new logging manager instance."""
    return LoggingManager()


def create_result_manager() -> ResultManager:
    """Create a new result manager instance."""
    return ResultManager()


def create_status_manager() -> StatusManager:
    """Create a new status manager instance."""
    return StatusManager()


def create_validation_manager() -> ValidationManager:
    """Create a new validation manager instance."""
    return ValidationManager()


