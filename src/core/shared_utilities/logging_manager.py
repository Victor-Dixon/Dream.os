"""
<!-- SSOT Domain: core -->

Logging Manager - Logging Operations
=====================================

Manages logging for managers.

Author: Agent-6 (Coordination & Communication Specialist)
Refactored: Agent-1 (Integration & Core Systems Specialist) - 2025-12-04
License: MIT
"""

import logging

from .base_utility import BaseUtility


class LoggingManager(BaseUtility):
    """Manages logging for managers."""

    def __init__(self, name: str = None):
        super().__init__(name)
        self.log_level = logging.INFO

    def initialize(self) -> bool:
        """Initialize logging manager."""
        logging.basicConfig(level=self.log_level)
        self.logger.info("LoggingManager initialized")
        return True

    def cleanup(self) -> bool:
        """Clean up logging resources."""
        return True

    def set_log_level(self, level: int) -> None:
        """Set logging level."""
        self.log_level = level
        logging.getLogger().setLevel(level)

    def log_info(self, message: str) -> None:
        """Log info message."""
        self.logger.info(message)

    def log_error(self, message: str) -> None:
        """Log error message."""
        self.logger.error(message)

    def get_logger(self) -> logging.Logger:
        """Get logger instance."""
        if self._logger is None:
            self._logger = logging.getLogger(self.name)
        return self._logger

