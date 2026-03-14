# Header-Variant: full
# Owner: Dream.os Platform
# Purpose: Validation core engine.
# SSOT: docs/recovery/recovery_registry.yaml

"""Validation core engine stub."""
@registry docs/recovery/recovery_registry.yaml#unregistered-src-core-engines-validation-core-engine
@file Validation core engine.
@summary Validation core engine.
"""Validation core engine stub."""

from __future__ import annotations

from .base_engine import BaseEngine


class ValidationCoreEngine(BaseEngine):
    name = "validation"

    def execute(self, *args, **kwargs):
        return True
