"""Browser infrastructure package.

<!-- SSOT Domain: infrastructure -->

Minimal, lazy exports to prevent circular imports during package import.
"""

from importlib import import_module

__all__ = [
    "browser_models",
    "unified",
    "unified_cookie_manager",
    "thea_browser_utils",
    "thea_browser_operations",
    "thea_browser_service",
    "thea_content_operations",
    "thea_session_management",
]


def __getattr__(name: str):
    if name in __all__:
        module = import_module(f"{__name__}.{name}")
        globals()[name] = module
        return module
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")