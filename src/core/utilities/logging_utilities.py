"""
<!-- SSOT Domain: core -->

Logging Utilities - Logging Manager
====================================

Manages logging for manager components.
Part of shared_utilities.py modular refactoring.

**CONSOLIDATED**: Now uses unified_logging_system.
Maintained for backward compatibility.

Author: Agent-1 (Integration & Core Systems Specialist) - V2 Refactor
Original: Agent-6 (Coordination & Communication Specialist)
License: MIT
"""

import logging

# Redirect to unified logging system
try:
    from ...core.unified_logging_system import get_logger, configure_logging
    UNIFIED_AVAILABLE = True
except ImportError:
    UNIFIED_AVAILABLE = False

from .base_utilities import BaseUtility


class LoggingManager(BaseUtility):
    """
    Manages logging for managers.
    
    **CONSOLIDATED**: Now uses unified_logging_system.
    Maintained for backward compatibility.
    """

    def __init__(self):
        super().__init__()
        self.log_level = logging.INFO
        
        # Use unified logging system if available
        if UNIFIED_AVAILABLE:
            configure_logging(level="INFO")
            self.logger = get_logger(self.name)
        else:
            self.logger = logging.getLogger(self.name)

    def initialize(self) -> bool:
        """Initialize logging manager."""
        if UNIFIED_AVAILABLE:
            configure_logging(level=logging.getLevelName(self.log_level))
        else:
            logging.basicConfig(level=self.log_level)
        self.logger.info("LoggingManager initialized")
        return True

    def cleanup(self) -> bool:
        """Clean up logging resources."""
        return True

    def set_log_level(self, level: int) -> None:
        """Set logging level."""
        self.log_level = level
        if UNIFIED_AVAILABLE:
            level_str = logging.getLevelName(level)
            if level_str.startswith("Level "):
                level_str = "INFO"
            configure_logging(level=level_str)
            self.logger = get_logger(self.name)
        else:
            logging.getLogger().setLevel(level)

    def log_info(self, message: str) -> None:
        """Log info message."""
        self.logger.info(message)

    def log_error(self, message: str) -> None:
        """Log error message."""
        self.logger.error(message)


def create_logging_manager() -> LoggingManager:
    """Create a new logging manager instance."""
    return LoggingManager()


__all__ = ["LoggingManager", "create_logging_manager"]
