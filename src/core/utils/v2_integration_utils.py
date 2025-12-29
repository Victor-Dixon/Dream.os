"""
<!-- SSOT Domain: core -->

V2 Integration Utilities - SSOT
================================

Shared utilities and fallback implementations for V2 core integration.
Provides graceful degradation when V2 core modules are unavailable.

This is the single source of truth (SSOT) for V2 integration utilities
used across GUI, Vision, and other systems.

V2 Compliance: ≤200 lines, single responsibility.

Author: Agent-2 (Architecture & Design Specialist) - Consolidation
Date: 2025-12-04
License: MIT
"""

import logging
from typing import Any


# Fallback implementations for V2 integration
def get_coordinate_loader_fallback() -> None:
    """Fallback coordinate loader when V2 core unavailable."""
    return None


def get_unified_config_fallback() -> Any:
    """Fallback unified config when V2 core unavailable."""
    return type("MockConfig", (), {"get_env": lambda x, y=None: y})()


def get_logger_fallback(name: str) -> logging.Logger:
    """Fallback logger when V2 core unavailable."""
    return logging.getLogger(name)


# Import V2 integration with fallback
try:
    from ...core.coordinate_loader import get_coordinate_loader
    from ...core.config_ssot import get_unified_config
    from ...core.unified_logging_system import get_logger
except ImportError as e:
    logging.warning(f"V2 integration imports failed: {e} - using fallbacks")
    get_coordinate_loader = get_coordinate_loader_fallback
    get_unified_config = get_unified_config_fallback
    get_logger = get_logger_fallback


__all__ = [
    "get_coordinate_loader",
    "get_unified_config",
    "get_logger",
]

