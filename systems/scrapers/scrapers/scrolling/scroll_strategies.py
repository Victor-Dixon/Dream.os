"""Enumerations for scrolling strategies."""

from enum import Enum

class ScrollStrategy(Enum):
    """Available scrolling strategies."""
    TARGETED = "targeted"
    AGGRESSIVE = "aggressive"
    SUPER_AGGRESSIVE = "super_aggressive"
    SCROLLPORT = "scrollport"
