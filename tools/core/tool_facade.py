"""
Tool Facade - Unified Tool Access
=================================

Purpose: Provides a stable facade alias (`ToolFacade`) over the core tool orchestrator.
Usage:
    from tools.core.tool_facade import ToolFacade
    result = ToolFacade().run("tool.name", {"param": "value"})

Author: Swarm (SSOT tagging remediation)
Date: 2025-12-28
Description: Backwards-compatible facade pattern for unified tool access.
"""

from ..toolbelt_core import ToolbeltCore

# Alias for backward compatibility
ToolFacade = ToolbeltCore
