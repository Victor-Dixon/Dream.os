"""
<!-- SSOT Domain: core -->

File Locking Engine Base - Redirect Shim
=========================================

Redirect for file_locking_engine_base to FileLockEngine.
Maintains backward compatibility for old imports.

This module resolves "cannot import name 'file_locking_engine_base'" errors
by providing a redirect to the correct SSOT implementation (FileLockEngine).

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-12-03
License: MIT
"""

from .file_locking_engine import FileLockEngine

# Re-export as file_locking_engine_base for backward compatibility
file_locking_engine_base = FileLockEngine
FileLockEngineBase = FileLockEngine

__all__ = ["file_locking_engine_base", "FileLockEngineBase", "FileLockEngine"]

