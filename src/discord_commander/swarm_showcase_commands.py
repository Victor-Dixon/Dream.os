#!/usr/bin/env python3
"""
Swarm Showcase Commands - Agent Cellphone V2
===========================================

<!-- SSOT Domain: discord -->

SSOT Domain: discord

Refactored entry point for swarm showcase functionality.
All core logic has been extracted into modular components for V2 compliance.

Features:
- Modular data loading (swarm_showcase_data.py)
- Professional embed factory (swarm_showcase_embeds.py)
- Focused command handling (swarm_showcase_commands_v2.py)

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

# Re-export the main components for backward compatibility
from .swarm_showcase_data import SwarmShowcaseData
from .swarm_showcase_embeds import SwarmShowcaseEmbeds
from .swarm_showcase_commands_v2 import SwarmShowcaseCommands, setup

