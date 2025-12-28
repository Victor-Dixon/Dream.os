# tools package init
# Lazy imports to avoid circular dependencies

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
        from . import tool_registry as _tool_registry
        if name == 'tool_registry':
            return _tool_registry
        return getattr(_tool_registry, name)
    elif name in ('toolbelt_core', 'ToolbeltCore'):
        from . import toolbelt_core as _toolbelt_core
        if name == 'toolbelt_core':
            return _toolbelt_core
        return getattr(_toolbelt_core, name)
    raise AttributeError(f"module 'tools' has no attribute '{name}'")
