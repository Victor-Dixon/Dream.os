"""
<!-- SSOT Domain: core -->

Minimal unified logging system stub for trading_robot tests.
"""

import logging


class UnifiedLoggingSystem:
    """Unified logging system for trading robot components."""

    def __init__(self):
        """Initialize the logging system."""
        self.logger = logging.getLogger("trading_robot")

    def get_logger(self, name: str = __name__) -> logging.Logger:
        """Get a logger instance."""
        return logging.getLogger(name)


def get_logger(name: str = __name__) -> logging.Logger:
    """Legacy function for backward compatibility."""
    return logging.getLogger(name)


__all__ = ["UnifiedLoggingSystem", "get_logger"]








