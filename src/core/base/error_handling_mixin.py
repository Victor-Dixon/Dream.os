# Header-Variant: full
# Owner: Dream.os Platform
# Purpose: Error handling mixin.
# SSOT: docs/recovery/recovery_registry.yaml

"""
Error Handling Mixin
====================

<!-- SSOT Domain: core -->

@file Error handling mixin.
@summary Error handling mixin.
@registry docs/recovery/recovery_registry.yaml#unregistered-src-core-base-error-handling-mixin
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
