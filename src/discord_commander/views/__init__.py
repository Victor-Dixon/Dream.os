#!/usr/bin/env python3
"""
Discord GUI Views - V2 Compliance Refactor
===========================================

Views extracted from discord_gui_views.py for V2 compliance.

Author: Agent-6 (Coordination & Communication Specialist)
Date: 2025-01-27
License: MIT
"""

from .agent_messaging_view import AgentMessagingGUIView
from .swarm_status_view import SwarmStatusGUIView
from .help_view import HelpGUIView
from .main_control_panel_view import MainControlPanelView, UnstallAgentView

__all__ = [
    "AgentMessagingGUIView",
    "SwarmStatusGUIView",
    "HelpGUIView",
    "MainControlPanelView",
    "UnstallAgentView",
]




