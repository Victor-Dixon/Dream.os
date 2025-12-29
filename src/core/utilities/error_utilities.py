
"""
<!-- SSOT Domain: core -->

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
Error Utilities - Error Handler
================================

Handles errors for manager components.
Part of shared_utilities.py modular refactoring.

Author: Agent-1 (Integration & Core Systems Specialist) - V2 Refactor
Original: Agent-6 (Coordination & Communication Specialist)
License: MIT
"""

from typing import Any

from .base_utilities import BaseUtility


class ErrorHandler(BaseUtility):
    """Handles errors for managers."""

    def __init__(self):
        super().__init__()
        self.error_count = 0
        self.last_error = None

    def initialize(self) -> bool:
        """Initialize error handler."""
        self.logger.info("ErrorHandler initialized")
        return True

    def cleanup(self) -> bool:
        """Clean up error handler resources."""
        self.error_count = 0
        self.last_error = None
        return True

    def handle_error(self, error: Exception, context: str = None) -> bool:
        """Handle an error."""
        self.error_count += 1
        self.last_error = error
        self.logger.error(f"Error in {context or 'unknown'}: {error}")
        return True

    def get_error_summary(self) -> dict[str, Any]:
        """Get error summary."""
        return {
            "error_count": self.error_count,
            "last_error": str(self.last_error) if self.last_error else None,
        }


def create_error_handler() -> ErrorHandler:
    """Create a new error handler instance."""
    return ErrorHandler()


__all__ = ["ErrorHandler", "create_error_handler"]
