"""Unified logging utilities for tests."""

from __future__ import annotations

import logging
import re
from typing import Any, Dict


def get_logger(name: str | None = None) -> logging.Logger:
    return logging.getLogger(name if name else __name__)


def setup_service_logging(name: str, level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


class LoggingMixin:
    def __init__(self, logger_name: str | None = None) -> None:
        name = logger_name or self.__class__.__module__
        self.logger = get_logger(name)

    def log_method_entry(self, method_name: str, *args: Any, **kwargs: Any) -> None:
        self.logger.debug("Entering %s", method_name)

    def log_method_exit(self, method_name: str, result: Any = None) -> None:
        self.logger.debug("Exiting %s", method_name)

    def log_performance(self, operation: str, duration_ms: float, context: Dict[str, Any] | None = None) -> None:
        self.logger.info("Performance %s: %sms", operation, duration_ms)

    def log_error_with_context(self, error: Exception, context: Dict[str, Any], operation: str) -> None:
        self.logger.error("Error in %s: %s", operation, error)

    def _is_sensitive_key(self, key: Any) -> bool:
        if not isinstance(key, str):
            return False
        return any(token in key.lower() for token in ["password", "token", "api_key", "access_token", "secret"])

    def _is_sensitive_value(self, value: Any) -> bool:
        if not isinstance(value, str):
            return False
        if value.startswith("Bearer "):
            return True
        return bool(re.match(r"^[A-Za-z0-9-_]{20,}$", value))

    def _mask_sensitive_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        masked = {}
        for key, value in data.items():
            if self._is_sensitive_key(key):
                masked[key] = "***MASKED***"
            else:
                masked[key] = value
        return masked
