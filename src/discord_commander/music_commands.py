#!/usr/bin/env python3
"""
Music Commands - Agent Cellphone V2
===================================

SSOT Domain: discord

Refactored entry point for Discord music commands.
All core logic has been extracted into service architecture for V2 compliance.

Features:
- YouTube audio download and playback (music_service.py)
- Voice channel management
- Music control commands (music_commands_v2.py)

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

# Re-export the main MusicCommands class for backward compatibility
from .music_commands_v2 import MusicCommands, setup

# Re-export music service for advanced usage
from .music_service import MusicService, music_service
