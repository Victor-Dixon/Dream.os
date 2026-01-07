#!/usr/bin/env python3
"""
GitHub Book Viewer - Agent Cellphone V2
======================================

SSOT Domain: git

Refactored entry point for GitHub book display functionality.
All core logic has been extracted into modular components for V2 compliance.

Features:
- Modular data loading (github_book_data.py)
- Shared UI components (discord_ui_components.py)
- Focused command handling (github_book_commands.py)

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

# Re-export the main components for backward compatibility
from .github_book_data import GitHubBookData
from .discord_ui_components import *
from .github_book_commands import GitHubBookCommands, setup

# Legacy alias for backward compatibility
GitHubBookNavigator = None  # Removed - functionality moved to discord_ui_components

__all__ = [
    "GitHubBookData",
    "GitHubBookCommands",
    "setup",
    # Re-export UI components
    "EmbedFormatter",
    "ModalHandler",
    "BaseNavigationView",
    "NavigationButton",
    "PreviousButton",
    "NextButton",
    "JumpButton",
    "SearchButton",
    "BackButton",
    "GoldmineButton"
]
