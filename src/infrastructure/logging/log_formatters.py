#!/usr/bin/env python3
"""
Log Formatters Module
====================

Logging formatters extracted from unified_logger.py for better modularity.

<!-- SSOT Domain: infrastructure -->

Author: Agent-3 (Infrastructure & DevOps) - ROI Refactoring
License: MIT
"""

import json
import logging
from typing import Any, Dict


class ColorFormatter(logging.Formatter):
    """Logging formatter with color support."""

    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
        "RESET": "\033[0m",  # Reset
    }

    def __init__(
        self,
        fmt: str = "%(levelname)s:%(name)s:%(message)s",
        datefmt: str = "%Y-%m-%d %H:%M:%S",
        use_colors: bool = True,
    ):
        """Initialize color formatter."""
        super().__init__(fmt, datefmt)
        self.use_colors = use_colors

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with optional colors."""
        if self.use_colors and record.levelname in self.COLORS:
            levelname = record.levelname
            colored_level = (
                f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
            )
            record.levelname = colored_level
        return super().format(record)


class PlainFormatter(logging.Formatter):
    """Plain logging formatter without colors (for files)."""

    def __init__(
        self,
        fmt: str = "%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt: str = "%Y-%m-%d %H:%M:%S",
    ):
        """Initialize plain formatter."""
        super().__init__(fmt, datefmt)
        self.default_msec_format = "%s.%03d"


class JsonFormatter(logging.Formatter):
    """Minimal JSON formatter for structured logs."""

    def format(self, record: logging.LogRecord) -> str:
        payload: Dict[str, Any] = {
            "name": record.name,
            "level": record.levelname,
            "message": record.getMessage(),
            "timestamp": self.formatTime(record, self.datefmt),
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload)


class StructuredFormatter(logging.Formatter):
    """Structured formatter (semi-JSON) for compatibility."""

    def format(self, record: logging.LogRecord) -> str:
        base = {
            "name": record.name,
            "level": record.levelname,
            "message": record.getMessage(),
            "timestamp": self.formatTime(record, self.datefmt),
        }
        return json.dumps(base)


__all__ = ["ColorFormatter", "PlainFormatter", "JsonFormatter", "StructuredFormatter"]
