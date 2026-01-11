"""
Thea GUI System
===============

Complete PyQt6-based graphical user interface for the Thea MMORPG system.
Restored from archived implementation with 21 components and 62 panels.

Components:
- Main Window: Complete application interface
- Controllers: 5 specialized controllers for system management
- Components: 21 modular UI components
- Panels: 62 functional panels for various system features
"""

from .main_window import TheaMainWindow

__all__ = ["TheaMainWindow"]