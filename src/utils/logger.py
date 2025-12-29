#!/usr/bin/env python3

"""
Enhanced Logging System - Agent Cellphone V2
===========================================

V2 compliant logging infrastructure with structured logging,
performance monitoring, and configurable outputs.

**CONSOLIDATED**: This module now redirects to unified_logging_system.
Maintained for backward compatibility.

Author: V2 SWARM CAPTAIN
License: MIT
""""

import logging
from pathlib import Path
from typing import Dict, Any, Optional

# Redirect to unified logging system
try:
    from src.core.unified_logging_system import get_logger as unified_get_logger, configure_logging
    UNIFIED_AVAILABLE = True
except ImportError:
    UNIFIED_AVAILABLE = False
    unified_get_logger = None


class V2Logger:
    """
    V2 compliant logger - Redirects to unified logging system.
    
    Maintained for backward compatibility. All functionality
    now delegates to src.core.unified_logging_system.
    """

    def __init__(self, name: str, log_level: str = "INFO", log_to_file: bool = True):
        """Initialize V2 logger (redirects to unified system).

        Args:
            name: Logger name
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_to_file: Whether to log to file in addition to console
        """
        self.name = name
        self.log_level = log_level
        self.log_to_file = log_to_file
        
        # Use unified logging system
        if UNIFIED_AVAILABLE:
            # Configure logging if needed
            if log_to_file:
                log_dir = Path("logs")
                log_dir.mkdir(exist_ok=True)
                log_file = log_dir / f"{name}.log"
                configure_logging(level=log_level, log_file=log_file)
            else:
                configure_logging(level=log_level)
            
            # Get logger from unified system (use unified_get_logger to avoid circular import)
            self.logger = unified_get_logger(name)
        else:
            # Fallback to standard logging
            self.logger = logging.getLogger(name)
            self.logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    def debug(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log debug message."""
        if extra:
            self.logger.debug(message, extra=extra)
        else:
            self.logger.debug(message)

    def info(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log info message."""
        if extra:
            self.logger.info(message, extra=extra)
        else:
            self.logger.info(message)

    def warning(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log warning message."""
        if extra:
            self.logger.warning(message, extra=extra)
        else:
            self.logger.warning(message)

    def error(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log error message."""
        if extra:
            self.logger.error(message, extra=extra)
        else:
            self.logger.error(message)

    def critical(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log critical message."""
        if extra:
            self.logger.critical(message, extra=extra)
        else:
            self.logger.critical(message)


# Global logger instances for different components
_messaging_logger = None
_contract_logger = None
_core_logger = None


def get_messaging_logger() -> V2Logger:
    """Get messaging system logger."""
    global _messaging_logger
    if _messaging_logger is None:
        _messaging_logger = V2Logger("messaging", log_level="INFO")
    return _messaging_logger


def get_contract_logger() -> V2Logger:
    """Get contract system logger."""
    global _contract_logger
    if _contract_logger is None:
        _contract_logger = V2Logger("contract", log_level="INFO")
    return _contract_logger


def get_core_logger() -> V2Logger:
    """Get core system logger."""
    global _core_logger
    if _core_logger is None:
        _core_logger = V2Logger("core", log_level="INFO")
    return _core_logger


def get_logger(name: str, log_level: str = "INFO") -> V2Logger:
    """Get a configured V2 logger with the given name.

    Args:
        name: Logger name
        log_level: Logging level

    Returns:
        V2Logger: Configured logger instance
    """
    return V2Logger(name, log_level)
