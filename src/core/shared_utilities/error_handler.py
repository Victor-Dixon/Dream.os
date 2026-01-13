"""
<!-- SSOT Domain: core -->

Error Handler - Error Management
=================================

Handles errors for managers.

Author: Agent-6 (Coordination & Communication Specialist)
Refactored: Agent-1 (Integration & Core Systems Specialist) - 2025-12-04
License: MIT
"""

from typing import Any, Dict

from .base_utility import BaseUtility


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

    def get_error_summary(self) -> Dict[str, Any]:
        """Get error summary."""
        return {
            'error_count': self.error_count,
            'last_error': str(self.last_error) if self.last_error else None
        }


