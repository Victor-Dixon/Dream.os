# Header-Variant: full
# Owner: Dream.os Platform
# Purpose: Validation core engine.
# SSOT: docs/recovery/recovery_registry.yaml

"""Validation core engine stub.

@file Validation core engine.
@registry docs/recovery/recovery_registry.yaml#core-engines-validation-core-engine
@summary Validation core engine.
"""

from __future__ import annotations

from .base_engine import BaseEngine


class ValidationCoreEngine(BaseEngine):
    name = "validation"

    def execute(self, *args, **kwargs):
        return True
