#!/usr/bin/env python3
"""
Centralized Logging Utilities - Agent Cellphone V2
==================================================

Unified logging infrastructure to eliminate code duplication across 499+ files.
Provides consistent logging setup, formatting, and configuration.

<!-- SSOT Domain: core -->

Author: Agent-1 (Integration & Core Systems)
Date: 2026-01-11

Usage:
    # Replace this pattern everywhere:
    # import logging
    # logger = logging.getLogger(__name__)

    # With this:
    from core.logging_utils import get_logger
    logger = get_logger(__name__)
"""

import logging
import logging.handlers
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from enum import Enum


class LogLevel(Enum):
    """Standardized log levels."""
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class LogFormat(Enum):
    """Available log formats."""
    CONSOLE = "console"
    JSON = "json"
    STRUCTURED = "structured"


class LoggerFactory:
    """
    Centralized logger factory for consistent logging across the application.

    Eliminates 572+ duplicate logging setups across 499+ files.
    """

    # Class-level configuration
    _configured = False
    _default_level = LogLevel.INFO
    _default_format = LogFormat.CONSOLE
    _log_directory = Path("runtime/logs")

    @classmethod
    def configure_global(
        cls,
        level: LogLevel = LogLevel.INFO,
        format_type: LogFormat = LogFormat.CONSOLE,
        log_directory: Optional[Path] = None,
        enable_file_logging: bool = True,
        enable_console_logging: bool = True,
        max_bytes: int = 10 * 1024 * 1024,  # 10MB
        backup_count: int = 5
    ) -> None:
        """
        Configure global logging settings for the entire application.

        This replaces the need for individual logging configuration in every file.
        """
        if cls._configured:
            return  # Already configured

        cls._default_level = level
        cls._default_format = format_type

        if log_directory:
            cls._log_directory = log_directory

        # Create log directory
        cls._log_directory.mkdir(parents=True, exist_ok=True)

        # Clear existing handlers to avoid duplication
        root_logger = logging.getLogger()
        root_logger.handlers.clear()
        root_logger.setLevel(level.value)

        # Create formatters
        formatters = cls._create_formatters(format_type)

        # Add console handler
        if enable_console_logging:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(level.value)
            console_handler.setFormatter(formatters[format_type.value])
            root_logger.addHandler(console_handler)

        # Add file handler
        if enable_file_logging:
            file_handler = logging.handlers.RotatingFileHandler(
                cls._log_directory / "application.log",
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(level.value)
            file_handler.setFormatter(formatters["structured"])  # Always use structured for files
            root_logger.addHandler(file_handler)

        cls._configured = True

    @classmethod
    def _create_formatters(cls, format_type: LogFormat) -> Dict[str, logging.Formatter]:
        """Create logging formatters based on format type."""

        formatters = {}

        # Console formatter - human readable
        console_format = "%(asctime)s | %(levelname)-8s | %(name)-30s | %(message)s"
        formatters["console"] = logging.Formatter(
            console_format,
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # JSON formatter - machine readable
        formatters["json"] = JSONFormatter()

        # Structured formatter - detailed structured format
        structured_format = (
            "%(asctime)s | %(levelname)-8s | %(name)-40s | "
            "%(filename)s:%(lineno)d | %(funcName)s() | %(message)s"
        )
        formatters["structured"] = logging.Formatter(
            structured_format,
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        return formatters

    @classmethod
    def get_logger(
        cls,
        name: str,
        level: Optional[LogLevel] = None,
        extra_fields: Optional[Dict[str, Any]] = None
    ) -> logging.Logger:
        """
        Get a configured logger instance.

        This replaces the duplicate pattern:
            import logging
            logger = logging.getLogger(__name__)

        Usage:
            from core.logging_utils import get_logger
            logger = get_logger(__name__)
        """
        # Ensure global configuration is set
        if not cls._configured:
            cls.configure_global()

        logger = logging.getLogger(name)

        # Set level if specified, otherwise use default
        if level:
            logger.setLevel(level.value)
        else:
            logger.setLevel(cls._default_level.value)

        # Add extra fields if provided (for structured logging)
        if extra_fields:
            # Create a logger adapter with extra context
            logger = ContextLoggerAdapter(logger, extra_fields)

        return logger

    @classmethod
    def create_service_logger(
        cls,
        service_name: str,
        service_version: Optional[str] = None,
        instance_id: Optional[str] = None
    ) -> logging.Logger:
        """
        Create a service-specific logger with additional context.

        Useful for services that need consistent identification in logs.
        """
        extra_fields = {
            "service": service_name,
            "timestamp": datetime.utcnow().isoformat()
        }

        if service_version:
            extra_fields["version"] = service_version
        if instance_id:
            extra_fields["instance_id"] = instance_id

        return cls.get_logger(f"service.{service_name}", extra_fields=extra_fields)

    @classmethod
    def create_request_logger(
        cls,
        request_id: str,
        user_id: Optional[str] = None,
        endpoint: Optional[str] = None
    ) -> logging.Logger:
        """
        Create a request-scoped logger with request context.

        Useful for tracking requests across multiple services.
        """
        extra_fields = {
            "request_id": request_id,
            "timestamp": datetime.utcnow().isoformat()
        }

        if user_id:
            extra_fields["user_id"] = user_id
        if endpoint:
            extra_fields["endpoint"] = endpoint

        return cls.get_logger("request", extra_fields=extra_fields)

    @classmethod
    def set_level(cls, level: LogLevel) -> None:
        """Change the global logging level."""
        cls._default_level = level
        logging.getLogger().setLevel(level.value)

    @classmethod
    def get_log_directory(cls) -> Path:
        """Get the current log directory."""
        return cls._log_directory


class ContextLoggerAdapter(logging.LoggerAdapter):
    """
    Logger adapter that adds context information to all log records.
    """

    def __init__(self, logger: logging.Logger, extra: Dict[str, Any]):
        super().__init__(logger, extra)
        self.extra_fields = extra

    def process(self, msg: str, kwargs: Dict[str, Any]) -> tuple[str, Dict[str, Any]]:
        """Process the logging record to include extra fields."""
        # Merge extra fields into kwargs
        if 'extra' not in kwargs:
            kwargs['extra'] = {}
        kwargs['extra'].update(self.extra_fields)

        return msg, kwargs


class JSONFormatter(logging.Formatter):
    """
    JSON formatter for structured logging.
    """

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        import json

        # Create base log entry
        log_entry = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        # Add any extra fields from the record
        if hasattr(record, '__dict__'):
            for key, value in record.__dict__.items():
                if key not in ['name', 'msg', 'args', 'levelname', 'levelno',
                             'pathname', 'filename', 'module', 'exc_info',
                             'exc_text', 'stack_info', 'lineno', 'funcName',
                             'created', 'msecs', 'relativeCreated', 'thread',
                             'threadName', 'processName', 'process', 'message']:
                    log_entry[key] = value

        return json.dumps(log_entry, default=str)


# Convenience functions for easy importing
def get_logger(
    name: str,
    level: Optional[LogLevel] = None,
    extra_fields: Optional[Dict[str, Any]] = None
) -> logging.Logger:
    """
    Convenience function to get a logger.

    This is the main entry point that replaces:
        import logging
        logger = logging.getLogger(__name__)

    Usage:
        from core.logging_utils import get_logger
        logger = get_logger(__name__)
    """
    return LoggerFactory.get_logger(name, level, extra_fields)


def configure_logging(
    level: LogLevel = LogLevel.INFO,
    format_type: LogFormat = LogFormat.CONSOLE,
    log_directory: Optional[Path] = None,
    enable_file_logging: bool = True,
    enable_console_logging: bool = True
) -> None:
    """
    Convenience function to configure global logging.

    Call this once at application startup.
    """
    LoggerFactory.configure_global(
        level=level,
        format_type=format_type,
        log_directory=log_directory,
        enable_file_logging=enable_file_logging,
        enable_console_logging=enable_console_logging
    )


def create_service_logger(
    service_name: str,
    service_version: Optional[str] = None,
    instance_id: Optional[str] = None
) -> logging.Logger:
    """Convenience function for service loggers."""
    return LoggerFactory.create_service_logger(service_name, service_version, instance_id)


def create_request_logger(
    request_id: str,
    user_id: Optional[str] = None,
    endpoint: Optional[str] = None
) -> logging.Logger:
    """Convenience function for request loggers."""
    return LoggerFactory.create_request_logger(request_id, user_id, endpoint)


# Initialize default configuration on import
LoggerFactory.configure_global()


# Migration helper for gradual rollout
def migrate_logger_usage():
    """
    Helper function to assist with migrating existing logging code.

    This can be used to find and replace old logging patterns.
    """
    print("🔍 Logging Migration Helper")
    print("Replace this pattern:")
    print("  import logging")
    print("  logger = logging.getLogger(__name__)")
    print()
    print("With this pattern:")
    print("  from core.logging_utils import get_logger")
    print("  logger = get_logger(__name__)")
    print()
    print("Benefits:")
    print("  ✅ Consistent formatting across all services")
    print("  ✅ Centralized configuration")
    print("  ✅ Structured logging support")
    print("  ✅ Automatic file/console handling")
    print("  ✅ Performance optimizations")


__all__ = [
    "LoggerFactory",
    "LogLevel",
    "LogFormat",
    "get_logger",
    "configure_logging",
    "create_service_logger",
    "create_request_logger",
    "migrate_logger_usage",
]