"""
Core Utilities Package
======================

Consolidated utility modules for tools consolidation.
Part of Phase 2A: Foundation Consolidation.

This package provides:
- file_utils: File and path operations
- type_utils: Type system standardization
- error_utils: Error handling patterns

Author: Agent-7 (Tools Consolidation & Architecture Lead)
Date: 2026-01-13
"""

from .file_utils import FileUtils, ensure_dir, read_json_safe, write_json_safe
from .type_utils import TypeUtils, safe_get, to_list, to_dict
from .error_utils import ErrorUtils, safe_call, log_exception

__all__ = [
    # Classes
    'FileUtils',
    'TypeUtils',
    'ErrorUtils',

    # Convenience functions
    'ensure_dir',
    'read_json_safe',
    'write_json_safe',
    'safe_get',
    'to_list',
    'to_dict',
    'safe_call',
    'log_exception'
]

__version__ = "1.0.0"