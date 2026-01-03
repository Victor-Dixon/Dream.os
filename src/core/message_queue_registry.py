#!/usr/bin/env python3
"""
Message Queue Registry - Service Locator Pattern
===============================================

Central registry for message queue components to avoid circular imports.

V2 Compliance | Author: Agent-2 | Date: 2026-01-01

<!-- SSOT Domain: core -->
"""

import logging
from typing import Any, Dict, Optional, Type

logger = logging.getLogger(__name__)

# Global registry for message queue components
_COMPONENT_REGISTRY: Dict[str, Any] = {}


def register_component(name: str, component: Any) -> None:
    """Register a component in the global registry."""
    _COMPONENT_REGISTRY[name] = component
    logger.debug(f"Registered component: {name}")


def get_component(name: str) -> Any:
    """Get a component from the global registry."""
    global _REGISTRY_INITIALIZED
    if not _REGISTRY_INITIALIZED:
        _initialize_registry()
        _REGISTRY_INITIALIZED = True

    if name not in _COMPONENT_REGISTRY:
        raise KeyError(f"Component '{name}' not registered")
    return _COMPONENT_REGISTRY[name]


def has_component(name: str) -> bool:
    """Check if a component is registered."""
    return name in _COMPONENT_REGISTRY


def unregister_component(name: str) -> bool:
    """Remove a component from the registry."""
    if name in _COMPONENT_REGISTRY:
        del _COMPONENT_REGISTRY[name]
        logger.debug(f"Unregistered component: {name}")
        return True
    return False


def list_components() -> list:
    """List all registered component names."""
    return list(_COMPONENT_REGISTRY.keys())


def clear_registry() -> None:
    """Clear all registered components."""
    _COMPONENT_REGISTRY.clear()
    logger.debug("Registry cleared")


# Initialize the registry with core components
def _initialize_registry():
    """Initialize the registry with core message queue components."""
    try:
        # Import and register core components using sys.path manipulation
        import sys
        import os

        # Temporarily modify sys.path to ensure we can import the module directly
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)

        # Import from the message_queue package (which imports from impl)
        from src.core.message_queue import MessageQueue, QueueConfig, AsyncQueueProcessor, IMessageQueue

        register_component('MessageQueue', MessageQueue)
        register_component('QueueConfig', QueueConfig)
        register_component('AsyncQueueProcessor', AsyncQueueProcessor)
        register_component('IMessageQueue', IMessageQueue)

        logger.info("Message queue registry initialized successfully")

    except ImportError as e:
        logger.warning(f"Could not initialize message queue registry: {e}")
        import traceback
        logger.debug(f"Registry initialization traceback: {traceback.format_exc()}")


# Initialize lazily when first accessed
_REGISTRY_INITIALIZED = False