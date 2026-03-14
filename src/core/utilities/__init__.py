"""Core utilities package.

<!-- SSOT Domain: core -->

Package init intentionally avoids eager imports to prevent circular import
issues and mismatches with moved/removed utility modules.
"""

from importlib import import_module

__all__ = [
    "base_utilities",
    "cleanup_utilities",
    "config_utilities",
    "handler_utilities",
    "init_utilities",
    "processing_utilities",
    "result_utilities",
    "status_utilities",
]


def __getattr__(name: str):
    if name in __all__:
        module = import_module(f"{__name__}.{name}")
        globals()[name] = module
        return module
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
