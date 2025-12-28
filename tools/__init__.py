import importlib

__all__ = [
    'tool_registry',
    'toolbelt_core',
    'ToolRegistry',
    'get_tool_registry',
    'ToolbeltCore',
]


def __getattr__(name):
    """Lazy import to avoid circular dependencies."""
    if name in ('tool_registry', 'ToolRegistry', 'get_tool_registry'):
        module = importlib.import_module('.tool_registry', __package__)
        if name == 'tool_registry':
            return module
        return getattr(module, name)
    elif name in ('toolbelt_core', 'ToolbeltCore'):
        module = importlib.import_module('.toolbelt_core', __package__)
        if name == 'toolbelt_core':
            return module
        return getattr(module, name)
    raise AttributeError(f"module 'tools' has no attribute '{name}'")
