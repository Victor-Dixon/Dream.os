"""
Tools Adapters Package
======================

Purpose: Defines the adapter interfaces and shared types used by the `tools` toolbelt.
Usage:
    from tools.adapters import IToolAdapter, ToolResult, ToolSpec

Author: Swarm (SSOT tagging remediation)
Date: 2025-12-28
Description: Package exports adapter primitives for tool discovery/execution.

<!-- SSOT Domain: tools -->
"""

"""
Tools Adapters Package
=====================

Purpose: Defines adapter interfaces and shared result/spec types used by the `tools` toolbelt.
Usage:
    from tools.adapters import IToolAdapter, ToolResult, ToolSpec

Author: Swarm (SSOT tagging remediation)
Date: 2025-12-28
Description: Adapter primitives for discovery, validation, and execution of tool adapters.
"""

# AUTO-GENERATED __init__.py
# DO NOT EDIT MANUALLY - changes may be overwritten

from . import base_adapter
from . import error_types
from .base_adapter import IToolAdapter, ToolResult, ToolSpec

__all__ = [
    'base_adapter',
    'error_types',
    'IToolAdapter',
    'ToolResult',
    'ToolSpec',
]
