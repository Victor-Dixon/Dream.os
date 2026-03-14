"""Validation core engine stub."""

from __future__ import annotations

from .base_engine import BaseEngine


class ValidationCoreEngine(BaseEngine):
    name = "validation"

    def execute(self, *args, **kwargs):
        return True
