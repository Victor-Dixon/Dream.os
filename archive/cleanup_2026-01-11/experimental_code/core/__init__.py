"""
Core Module - Backward Compatibility Package
============================================

Provides backward compatibility for core module imports.
"""

# Re-export config_manager for backward compatibility
from . import config_manager

__all__ = ['config_manager']

