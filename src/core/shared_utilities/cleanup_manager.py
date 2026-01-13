"""
<!-- SSOT Domain: core -->

Cleanup Manager - Cleanup Operations
=====================================

Manages cleanup operations for managers.

Author: Agent-6 (Coordination & Communication Specialist)
Refactored: Agent-1 (Integration & Core Systems Specialist) - 2025-12-04
License: MIT
"""

from .base_utility import BaseUtility


class CleanupManager(BaseUtility):
    """Manages cleanup operations for managers."""

    def __init__(self):
        super().__init__()
        self.cleanup_handlers = []

    def initialize(self) -> bool:
        """Initialize cleanup manager."""
        self.logger.info("CleanupManager initialized")
        return True

    def cleanup(self) -> bool:
        """Execute all registered cleanup handlers."""
        success = True
        for handler in reversed(self.cleanup_handlers):
            try:
                handler()
            except Exception as e:
                self.logger.error(f"Cleanup handler failed: {e}")
                success = False
        self.cleanup_handlers.clear()
        return success

    def register_handler(self, handler: callable) -> None:
        """Register a cleanup handler."""
        self.cleanup_handlers.append(handler)


