#!/usr/bin/env python3
# Header-Variant: full
# Owner: Dream.os
# Purpose: Shared keyboard lock helper for PyAutoGUI send paths.
# SSOT: docs/recovery/recovery_registry.yaml#src-core-messaging-pyautogui

"""Global keyboard control lock shim used by PyAutoGUI messaging."""

from __future__ import annotations

from contextlib import contextmanager
from threading import RLock

_LOCK = RLock()
_LOCK_HELD = False


def is_locked() -> bool:
    """Return True when keyboard lock is currently held."""
    return _LOCK_HELD


@contextmanager
def keyboard_control(source: str = "unknown"):
    """Context manager that serializes keyboard control operations."""
    del source  # reserved for future telemetry
    global _LOCK_HELD
    with _LOCK:
        _LOCK_HELD = True
        try:
            yield
        finally:
            _LOCK_HELD = False

