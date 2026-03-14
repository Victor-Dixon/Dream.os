# Header-Variant: full
# Owner: Dream.os Platform
# Purpose: Error handling.
# SSOT: docs/recovery/recovery_registry.yaml

"""Core error handling logger shim."""
@registry docs/recovery/recovery_registry.yaml#unregistered-src-core-error-handling
@file Error handling.
@summary Error handling.
"""Core error handling logger shim."""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)
