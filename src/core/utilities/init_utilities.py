
"""
⚠️ DEPRECATED - This module is deprecated.

This utility has been consolidated into shared_utilities/ as SSOT.
Please update imports to use shared_utilities instead.

Migration:
  OLD: from src.core.utilities.{old_module} import ...
  NEW: from src.core.shared_utilities.{new_module} import ...

This module will be removed in a future release.
"""

import warnings
warnings.warn(
    "utilities/ modules are deprecated. Use shared_utilities/ instead.",
    DeprecationWarning,
    stacklevel=2
)

"""
Initialization Utilities - Initialization Manager
==================================================

Manages initialization operations for manager components.
Part of shared_utilities.py modular refactoring.

Author: Agent-1 (Integration & Core Systems Specialist) - V2 Refactor
Original: Agent-6 (Coordination & Communication Specialist)
License: MIT
"""

from datetime import datetime

from .base_utilities import BaseUtility


class InitializationManager(BaseUtility):
    """Manages initialization operations."""

    def __init__(self):
        super().__init__()
        self.initialized = False
        self.init_time = None

    def initialize(self) -> bool:
        """Initialize the initialization manager."""
        if not self.initialized:
            self.initialized = True
            self.init_time = datetime.now()
            self.logger.info("InitializationManager initialized")
        return True

    def cleanup(self) -> bool:
        """Clean up initialization resources."""
        self.initialized = False
        self.init_time = None
        return True

    def is_initialized(self) -> bool:
        """Check if initialized."""
        return self.initialized

    def get_init_time(self) -> datetime | None:
        """Get initialization time."""
        return self.init_time


def create_initialization_manager() -> InitializationManager:
    """Create a new initialization manager instance."""
    return InitializationManager()


__all__ = ["InitializationManager", "create_initialization_manager"]
