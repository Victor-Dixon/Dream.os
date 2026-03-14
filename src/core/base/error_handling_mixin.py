"""
Error Handling Mixin
====================

<!-- SSOT Domain: core -->
"""

from __future__ import annotations

import logging


class ErrorHandlingMixin:
    """Minimal error handling mixin for legacy imports."""

    logger = logging.getLogger(__name__)

    def handle_error(self, message: str, exc: Exception | None = None) -> None:
        if exc:
            self.logger.error(message, exc_info=exc)
        else:
            self.logger.error(message)
