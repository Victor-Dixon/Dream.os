# Header-Variant: full
# Owner: @dreamos/platform
# Purpose: config package initialization.
# SSOT: docs/recovery/recovery_registry.yaml#unregistered-src-core-config-init
# @registry docs/recovery/recovery_registry.yaml#unregistered-src-core-config-init

"""Configuration package with lazy submodule loading.

This avoids importing heavy runtime configuration dependencies when callers only
need package discovery.
"""

from importlib import import_module

__all__ = [
    "config_accessors",
    "config_dataclasses",
    "config_enums",
    "config_manager",
]


def __getattr__(name: str):
    """Lazy-load configuration submodules."""
    if name in __all__:
        module = import_module(f"{__name__}.{name}")
        globals()[name] = module
        return module
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
