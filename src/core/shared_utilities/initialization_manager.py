"""
<!-- SSOT Domain: core -->

Initialization Manager - Initialization Operations
===================================================

Manages initialization operations.

Author: Agent-6 (Coordination & Communication Specialist)
Refactored: Agent-1 (Integration & Core Systems Specialist) - 2025-12-04
License: MIT
"""

from datetime import datetime
from typing import Optional

from .base_utility import BaseUtility


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

    def get_init_time(self) -> Optional[datetime]:
        """Get initialization time."""
        return self.init_time


