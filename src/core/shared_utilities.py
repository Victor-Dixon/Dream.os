"""
Shared Utilities - Core Manager Utilities (Refactored)

<!-- SSOT Domain: infrastructure -->

=======================================================

Shared utility classes for manager components implementing SSOT principles.
Refactored for V2 compliance: Split into modular files.

This file maintains backward compatibility by re-exporting from the modular structure.

Author: Agent-6 (Coordination & Communication Specialist)
Refactored: Agent-1 (Integration & Core Systems Specialist) - 2025-12-04
License: MIT
"""

# Re-export all from modular structure for backward compatibility
from .shared_utilities.base_utility import BaseUtility
from .shared_utilities.cleanup_manager import CleanupManager
from .shared_utilities.configuration_manager_util import ConfigurationManagerUtil
from .shared_utilities.error_handler import ErrorHandler
from .shared_utilities.initialization_manager import InitializationManager
from .shared_utilities.logging_manager import LoggingManager
from .shared_utilities.result_manager import ResultManager
from .shared_utilities.status_manager import StatusManager
from .shared_utilities.validation_manager import ValidationManager
from .shared_utilities.factory_functions import (
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
