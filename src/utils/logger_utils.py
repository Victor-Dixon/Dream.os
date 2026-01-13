"""
<!-- SSOT Domain: logging -->


Logger Utilities - Wrapper for Unified Logging System
======================================================

Provides backward compatibility for logger utilities.
Delegates to unified logging system.

V2 Compliance: Wrapper pattern, <400 lines
"""

import logging

# Import from unified logging system
# Verified: get_logger and configure_logging are exported
try:
    from ..core.unified_logging_system import get_logger as unified_get_logger
    from ..core.unified_logging_system import configure_logging

    UNIFIED_AVAILABLE = True
except ImportError:
    UNIFIED_AVAILABLE = False
    configure_logging = None


def setup_logger(name: str, level: str = "INFO", log_file: str = None):
    """

    Set up logger with specified configuration.

    Args:
        name: Logger name
        level: Log level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional log file path

    Returns:
        Configured logger instance
    """
    if UNIFIED_AVAILABLE and configure_logging:
        # Configure unified logging system if not already configured
        from pathlib import Path
        log_path = Path(log_file) if log_file else None
        configure_logging(level=level, log_file=log_path)
        return unified_get_logger(name)

    # Fallback implementation
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    return logger


def get_logger(name: str):
    """

    Get logger instance by name.

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    if UNIFIED_AVAILABLE:
        return unified_get_logger(name)

    return logging.getLogger(name)


def create_logger(name: str, level: str = "INFO"):
    """Create logger (backward compatible)."""

    return setup_logger(name, level)


# Export commonly used items
__all__ = ["setup_logger", "get_logger", "create_logger"]
