#!/usr/bin/env python3
"""
Discord Messaging Commands - Agent Cellphone V2
==============================================

SSOT Domain: messaging

Refactored entry point for Discord messaging commands.
All core logic has been extracted into base classes and focused implementations.

Features:
- Messaging command implementations (messaging_commands_v2.py)
- Command base classes (command_base.py)
- Messaging controller integration (messaging_controller.py)

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

# Re-export the main MessagingCommands class for backward compatibility
from .messaging_commands_v2 import MessagingCommands, setup

# Re-export base classes for extension
from .command_base import BaseDiscordCommand, MessagingCommandBase, StatusCommandBase
