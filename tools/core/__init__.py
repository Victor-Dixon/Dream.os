"""
Tools Core Package
==================

Purpose: Core primitives for the `tools` toolbelt (facade/spec) used by registry/orchestrator layers.
Usage:
    from tools.core import tool_facade, tool_spec

Author: Swarm (SSOT tagging remediation)
Date: 2025-12-28
Description: Provides core building blocks for unified tool access.
"""

# AUTO-GENERATED __init__.py
# DO NOT EDIT MANUALLY - changes may be overwritten

from . import tool_facade
from . import tool_spec

__all__ = [
    'tool_facade',
    'tool_spec',
]
