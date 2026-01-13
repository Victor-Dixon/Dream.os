#!/usr/bin/env python3
"""
Discord Test Utilities - Unified Mock Objects
==============================================

Unified test utilities for Discord.py when the library is not available.
Consolidates MockCog, MockCommands, MockExt, and MockDiscord implementations
from multiple locations into a single SSOT.

<!-- SSOT Domain: web -->

Author: Agent-7 (Web Development Specialist)
Date: 2025-12-05
V2 Compliant: Yes (<300 lines)
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


# --- Mock UI Components ---

class MockView:
    """Mock Discord View class."""
    def __init__(self, *args, **kwargs):
        pass
    
    def add_item(self, item):
        """Add item to view."""
        pass


class MockSelect:
    """Mock Discord Select class."""
    def __init__(self, *args, **kwargs):
        pass


class MockButton:
    """Mock Discord Button class."""
    def __init__(self, *args, **kwargs):
        pass


class MockSelectOption:
    """Mock Discord SelectOption class."""
    def __init__(self, *args, **kwargs):
        pass


class MockButtonStyle:
    """Mock Discord ButtonStyle class."""
    primary = "primary"
    secondary = "secondary"
    success = "success"
    danger = "danger"
    link = "link"


class MockUI:
    """Mock Discord UI namespace."""
    View = MockView
    Select = MockSelect
    Button = MockButton
    SelectOption = MockSelectOption


# --- Mock Command System ---

class MockCog:
    """Mock Discord Cog class."""
    def __init__(self, *args, **kwargs):
        pass


def mock_command(*args, **kwargs):
    """Mock decorator for commands.command."""
    def decorator(func):
        return func
    return decorator


class MockCommandError(Exception):
    """Mock CommandError exception."""
    pass


class MockCommands:
    """Mock Discord Commands namespace."""
    Cog = MockCog
    command = mock_command
    Context = type('Context', (), {})()
    CommandError = MockCommandError


class MockExt:
    """Mock Discord Extensions namespace."""
    commands = MockCommands()


# --- Mock Discord Module ---

class MockDiscord:
    """Mock Discord module."""
    class ui:
        View = MockView
        Select = MockSelect
        Button = MockButton
        SelectOption = MockSelectOption
    
    SelectOption = MockSelectOption
    ButtonStyle = MockButtonStyle
    Interaction = type('Interaction', (), {})()
    Embed = type('Embed', (), {})()
    Color = type('Color', (), {'blue': lambda: None, 'green': lambda: None, 'red': lambda: None})()
    File = type('File', (), {})()
    ext = MockExt()


# --- Utility Functions ---

def get_mock_discord():
    """
    Get mock Discord module when discord.py is not available.
    
    Returns:
        Tuple of (discord, commands) mock objects
    """
    return MockDiscord(), MockCommands()


def create_mock_discord_imports():
    """
    Create mock Discord imports for use when discord.py is unavailable.
    
    Returns:
        Dict with 'discord' and 'commands' keys
    """
    return {
        'discord': MockDiscord(),
        'commands': MockCommands()
    }

