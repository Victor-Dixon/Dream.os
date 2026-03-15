# Header-Variant: full
# Owner: @dreamos/platform
# Purpose: core package initialization.
# SSOT: docs/recovery/recovery_registry.yaml#unregistered-src-core-init
# @registry docs/recovery/recovery_registry.yaml#unregistered-src-core-init

"""Core package exports with lazy loading.

This module keeps package import side effects low while preserving the legacy
`from src.core import ...` API surface.
"""

from importlib import import_module

_LAZY_EXPORTS = {
    "get_logger": ("unified_logging_system", "get_logger"),
    "get_logging_system": ("unified_logging_system", "get_logging_system"),
    "configure_logging": ("unified_logging_system", "configure_logging"),
    "get_config": ("config.config_accessors", "get_config"),
    "get_agent_config": ("config.config_accessors", "get_agent_config"),
    "get_timeout_config": ("config.config_accessors", "get_timeout_config"),
    "get_browser_config": ("config.config_accessors", "get_browser_config"),
    "get_threshold_config": ("config.config_accessors", "get_threshold_config"),
    "UnifiedConfigManager": ("config.config_accessors", "get_unified_config"),
    "get_coordinate_loader": ("coordinate_loader", "get_coordinate_loader"),
    "CoordinateLoader": ("coordinate_loader", "CoordinateLoader"),
    "MessageQueue": ("message_queue", "MessageQueue"),
    "IMessageQueue": ("message_queue", "IMessageQueue"),
    "get_activity_tracker": ("agent_activity_tracker", "get_activity_tracker"),
    "AgentActivityTracker": ("agent_activity_tracker", "AgentActivityTracker"),
    "keyboard_control": ("keyboard_control_lock", "keyboard_control"),
    "is_locked": ("keyboard_control_lock", "is_locked"),
    "AgentDocs": ("agent_documentation_service", "AgentDocumentationService"),
    "create_agent_docs": ("agent_documentation_service", "create_agent_docs"),
}

__all__ = sorted(_LAZY_EXPORTS.keys()) + ["managers"]


def __getattr__(name: str):
    """Lazily expose heavyweight subpackages and exported symbols."""
    if name == "managers":
        module = import_module(f"{__name__}.managers")
        globals()[name] = module
        return module

    target = _LAZY_EXPORTS.get(name)
    if target is None:
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

    module_name, attr_name = target
    module = import_module(f"{__name__}.{module_name}")
    value = getattr(module, attr_name)
    globals()[name] = value
    return value
