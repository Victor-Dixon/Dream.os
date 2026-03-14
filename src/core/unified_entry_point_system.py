#!/usr/bin/env python3
# Header-Variant: full
# Owner: Dream.OS
# Purpose: unified entry point system.
# SSOT: docs/recovery/recovery_registry.yaml#src-core-unified-entry-point-system
# @registry docs/recovery/recovery_registry.yaml#src-core-unified-entry-point-system

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