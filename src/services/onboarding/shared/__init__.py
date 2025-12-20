"""
Shared Onboarding Components
===========================

Shared utilities for hard and soft onboarding services:
- PyAutoGUI operations wrapper
- Coordinate management wrapper

V2 Compliant: < 200 lines per module
"""

from .operations import PyAutoGUIOperations
from .coordinates import OnboardingCoordinates

__all__ = [
    "PyAutoGUIOperations",
    "OnboardingCoordinates",
]

