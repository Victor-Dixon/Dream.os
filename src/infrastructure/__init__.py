"""Infrastructure package exports.

<!-- SSOT Domain: infrastructure -->

Minimal lazy exports to avoid circular imports at package import time.
"""

from importlib import import_module

__all__ = [
    "unified_browser_service",
    "unified_logging_time",
    "unified_persistence",
    "browser",
    "logging",
    "persistence",
    "time",
]


def __getattr__(name: str):
    if name in __all__:
        module = import_module(f"{__name__}.{name}")
        globals()[name] = module
        return module
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
