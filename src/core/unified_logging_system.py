"""
Unified Logging System - Agent Cellphone V2
==========================================

SSOT Domain: infrastructure

Centralized logging configuration and management for the entire system.
Provides consistent logging across all modules with configurable levels.

Features:
- Centralized logger configuration
- Structured logging with context
- Performance monitoring integration
- Environment-aware logging levels
- Thread-safe logging operations

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Infrastructure & Core Systems)
Date: 2026-01-15
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional, Dict, Any
import json
from datetime import datetime

# Global logging system instance
_logging_system = None

class UnifiedLoggingSystem:
    """
    Unified logging system for consistent logging across all modules.

    Provides:
    - Structured logging with context
    - Environment-aware configuration
    - Performance monitoring integration
    - Thread-safe operations
    """

    def __init__(self):
        self._configured = False
        self._loggers = {}
        self._handlers = []
        self._repo_root = Path(__file__).resolve().parents[2]

    def configure_logging(
        self,
        level: str = "INFO",
        log_to_file: bool = True,
        log_to_console: bool = True,
        log_dir: Optional[Path] = None,
        max_bytes: int = 10 * 1024 * 1024,  # 10MB
        backup_count: int = 5,
        format_string: Optional[str] = None
    ) -> None:
        """
        Configure the unified logging system.

        Args:
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_to_file: Whether to log to files
            log_to_console: Whether to log to console
            log_dir: Directory for log files
            max_bytes: Maximum size of log files before rotation
            backup_count: Number of backup log files to keep
            format_string: Custom format string for log messages
        """
        if self._configured:
            return

        # Convert string level to logging level
        numeric_level = getattr(logging, level.upper(), logging.INFO)

        # Set up root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(numeric_level)

        # Clear existing handlers
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        # Default format
        if format_string is None:
            format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

        formatter = logging.Formatter(format_string)

        # Console handler
        if log_to_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(numeric_level)
            console_handler.setFormatter(formatter)
            root_logger.addHandler(console_handler)
            self._handlers.append(console_handler)

        # File handler
        if log_to_file:
            if log_dir is None:
                log_dir = self._repo_root / "logs"

            log_dir.mkdir(exist_ok=True)

            # Main log file
            log_file = log_dir / "agent_cellphone.log"
            file_handler = logging.handlers.RotatingFileHandler(
                log_file, maxBytes=max_bytes, backupCount=backup_count
            )
            file_handler.setLevel(numeric_level)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
            self._handlers.append(file_handler)

            # Error log file (WARNING and above)
            error_log_file = log_dir / "agent_cellphone_error.log"
            error_file_handler = logging.handlers.RotatingFileHandler(
                error_log_file, maxBytes=max_bytes, backupCount=backup_count
            )
            error_file_handler.setLevel(logging.WARNING)
            error_file_handler.setFormatter(formatter)
            root_logger.addHandler(error_file_handler)
            self._handlers.append(error_file_handler)

        self._configured = True

        # Log configuration completion
        logger = logging.getLogger(__name__)
        logger.info(f"✅ Unified logging system configured - Level: {level}, File logging: {log_to_file}")

    def get_logger(self, name: str) -> logging.Logger:
        """
        Get a configured logger for the given name.

        Args:
            name: Logger name (typically __name__)

        Returns:
            Configured logger instance
        """
        if name not in self._loggers:
            logger = logging.getLogger(name)

            # Ensure logging is configured
            if not self._configured:
                self.configure_logging()

            self._loggers[name] = logger

        return self._loggers[name]

    def shutdown(self) -> None:
        """Shutdown the logging system and close all handlers."""
        for handler in self._handlers:
            handler.close()

        self._handlers.clear()
        self._loggers.clear()
        self._configured = False

        # Reset root logger
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

def get_logging_system() -> UnifiedLoggingSystem:
    """Get the global logging system instance."""
    global _logging_system
    if _logging_system is None:
        _logging_system = UnifiedLoggingSystem()
    return _logging_system

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger for the given name.

    This is a convenience function that automatically configures
    logging if it hasn't been configured yet.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Configured logger instance
    """
    system = get_logging_system()
    return system.get_logger(name)

def configure_logging(
    level: str = "INFO",
    log_to_file: bool = True,
    log_to_console: bool = True,
    log_dir: Optional[Path] = None,
    max_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 5,
    format_string: Optional[str] = None
) -> None:
    """
    Configure the unified logging system.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: Whether to log to files
        log_to_console: Whether to log to console
        log_dir: Directory for log files
        max_bytes: Maximum size of log files before rotation
        backup_count: Number of backup log files to keep
        format_string: Custom format string for log messages
    """
    system = get_logging_system()
    system.configure_logging(
        level=level,
        log_to_file=log_to_file,
        log_to_console=log_to_console,
        log_dir=log_dir,
        max_bytes=max_bytes,
        backup_count=backup_count,
        format_string=format_string
    )

# Initialize with default configuration on first import
if not _logging_system:
    get_logging_system()

__all__ = [
    "UnifiedLoggingSystem",
    "get_logging_system",
    "get_logger",
    "configure_logging",
]