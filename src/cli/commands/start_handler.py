"""Backward-compatible StartHandler import.

SSOT: `src.cli.commands.handlers.start_handler` remains the implementation source.
"""

from .handlers.start_handler import StartHandler, create_start_handler

__all__ = ["StartHandler", "create_start_handler"]
