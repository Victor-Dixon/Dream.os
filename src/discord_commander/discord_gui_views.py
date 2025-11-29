#!/usr/bin/env python3
"""
Discord GUI Views - Backward Compatibility Shim
==============================================

⚠️  DEPRECATED: This module is maintained for backward compatibility only.
    All views have been extracted to the `views/` directory for V2 compliance.

    New code should import from `.views` instead:
        from .views import AgentMessagingGUIView, SwarmStatusGUIView

This module re-exports the extracted views for backward compatibility.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-01-27
License: MIT
"""

# Re-export views from extracted modules for backward compatibility
from .views import (
    AgentMessagingGUIView,
    SwarmStatusGUIView,
)

__all__ = ["AgentMessagingGUIView", "SwarmStatusGUIView"]
