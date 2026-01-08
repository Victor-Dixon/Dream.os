"""
Status Reader - Agent Cellphone V2
==================================

SSOT Domain: discord

Refactored entry point for Discord status reading commands.
All core logic has been extracted into service architecture for V2 compliance.

Features:
- Async/sync status reading with caching
- Discord embed formatting
- Error handling and fallbacks
- Command-based interface (status_reader_v2.py)

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

# Import StatusReader from v2 implementation for backward compatibility
from .status_reader_v2 import StatusReaderCommands as StatusReader
