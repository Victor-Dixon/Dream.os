import importlib

__all__ = [
    'tool_registry',
    'toolbelt_core',
    'ToolRegistry',
    'get_tool_registry',
    'ToolbeltCore',
    'get_toolbelt_core',
]

"""
SSOT TOOL METADATA
Purpose: Provide the `tools` package public API with lazy imports to avoid circular dependencies.
Description: Exposes Tool Registry / Toolbelt Core entry points while deferring heavy imports until first access.
Usage:
  - from tools import ToolRegistry, get_tool_registry
  - from tools import ToolbeltCore, get_toolbelt_core
Author: Swarm (maintainers)
Date: 2025-12-28
Tags: ssot, tooling, python-package
"""


def __getattr__(name):
    """Lazy import to avoid circular dependencies."""
    if name in ('tool_registry', 'ToolRegistry', 'get_tool_registry'):
        module = importlib.import_module('.tool_registry', __package__)
        if name == 'tool_registry':
            return module
        return getattr(module, name)
    elif name in ('toolbelt_core', 'ToolbeltCore', 'get_toolbelt_core'):
        module = importlib.import_module('.toolbelt_core', __package__)
        if name == 'toolbelt_core':
            return module
        return getattr(module, name)
    raise AttributeError(f"module 'tools' has no attribute '{name}'")
