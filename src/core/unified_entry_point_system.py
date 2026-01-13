#!/usr/bin/env python3
"""
Unified Entry Point System
==========================

Provides unified access to main entry points across the system.

Navigation References:
├── Used by: gaming/performance_validation.py
└── Main entry point: main.py
"""

# Re-export main function from main module for backward compatibility
from main import main

__all__ = ['main']