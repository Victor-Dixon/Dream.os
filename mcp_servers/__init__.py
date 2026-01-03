# AUTO-GENERATED __init__.py
# DO NOT EDIT MANUALLY - changes may be overwritten

# Use lazy imports to avoid circular import issues
def __getattr__(name):
    if name == 'messaging_server':
        from . import agent_messaging_mcp_server as messaging_server
        return messaging_server
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

__all__ = [
    'messaging_server',
]
