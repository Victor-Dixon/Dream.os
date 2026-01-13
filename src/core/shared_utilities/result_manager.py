"""
<!-- SSOT Domain: core -->

Result Manager - Result Management
==================================

Manages results for operations.

Author: Agent-6 (Coordination & Communication Specialist)
Refactored: Agent-1 (Integration & Core Systems Specialist) - 2025-12-04
License: MIT
"""

from typing import Generic, Optional, TypeVar

from .base_utility import BaseUtility

T = TypeVar('T')


class ResultManager(BaseUtility, Generic[T]):
    """Manages results for operations."""

    def __init__(self):
        super().__init__()
        self.results = []
        self.last_result = None

    def initialize(self) -> bool:
        """Initialize result manager."""
        self.logger.info("ResultManager initialized")
        return True

    def cleanup(self) -> bool:
        """Clean up result resources."""
        self.results.clear()
        self.last_result = None
        return True

    def add_result(self, result: T) -> None:
        """Add a result."""
        self.results.append(result)
        self.last_result = result

    def get_results(self) -> list[T]:
        """Get all results."""
        return self.results.copy()

    def get_last_result(self) -> Optional[T]:
        """Get last result."""
        return self.last_result

    def clear_results(self) -> None:
        """Clear all results."""
        self.results.clear()
        self.last_result = None


