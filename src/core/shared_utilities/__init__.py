"""
<!-- SSOT Domain: core -->

Shared Utilities - Core Manager Utilities (Refactored)
=======================================================

Shared utility classes for manager components implementing SSOT principles.
Refactored for V2 compliance: Split into modular files.

Author: Agent-6 (Coordination & Communication Specialist)
Refactored: Agent-1 (Integration & Core Systems Specialist) - 2025-12-04
License: MIT
"""

# Import all utility classes from modular files
from .base_utility import BaseUtility
from .cleanup_manager import CleanupManager
from .configuration_manager_util import ConfigurationManagerUtil
from .error_handler import ErrorHandler
from .initialization_manager import InitializationManager
from .logging_manager import LoggingManager
from .result_manager import ResultManager
from .status_manager import StatusManager
from .validation_manager import ValidationManager

# Import factory functions
from .factory_functions import (
    create_cleanup_manager,
    create_configuration_manager,
    create_error_handler,
    create_initialization_manager,
    create_logging_manager,
    create_result_manager,
    create_status_manager,
    create_validation_manager,
)

# Backward compatibility alias
ConfigurationManager = ConfigurationManagerUtil

__all__ = [
    'BaseUtility',
    'CleanupManager',
    'ConfigurationManagerUtil',
    'ConfigurationManager',  # Backward compatibility alias
    'ErrorHandler',
    'InitializationManager',
    'LoggingManager',
    'ResultManager',
    'StatusManager',
    'ValidationManager',
    # Factory functions
    'create_cleanup_manager',
    'create_configuration_manager',
    'create_error_handler',
    'create_initialization_manager',
    'create_logging_manager',
    'create_result_manager',
    'create_status_manager',
    'create_validation_manager',
]

