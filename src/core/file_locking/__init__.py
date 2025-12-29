# <!-- SSOT Domain: core -->
# AUTO-GENERATED __init__.py
# DO NOT EDIT MANUALLY - changes may be overwritten

# Lazy imports to avoid circular dependencies
# Import only models at module level (no circular dependencies)
from . import file_locking_models

# Export models (SSOT - no circular dependencies)
from .file_locking_models import (
    LockConfig,
    LockInfo,
    LockMetrics,
    LockResult,
    LockStatus,
)

# Export manager (SSOT for high-level operations)
from .file_locking_manager import FileLockManager, FileLockContext, get_file_lock_manager

# Export engine base (redirect shim for backward compatibility)
from .file_locking_engine_base import file_locking_engine_base, FileLockEngineBase, FileLockEngine

__all__ = [
    'file_locking_models',
    'LockConfig',
    'LockInfo',
    'LockMetrics',
    'LockResult',
    'LockStatus',
    'FileLockManager',
    'FileLockContext',
    'get_file_lock_manager',
    'file_locking_engine_base',  # Redirect shim for backward compatibility
    'FileLockEngineBase',  # Alias for FileLockEngine
    'FileLockEngine',  # SSOT implementation
    # Other classes exported via lazy imports when modules are accessed
]
