#!/usr/bin/env python3
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

