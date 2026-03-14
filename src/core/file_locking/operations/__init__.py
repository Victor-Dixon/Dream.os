# Header-Variant: full
# Owner: Dream.os Platform
# Purpose:   init  .
# SSOT: docs/recovery/recovery_registry.yaml

"""
@file   init  .
@summary   init  .
@registry docs/recovery/recovery_registry.yaml#unregistered-src-core-file-locking-operations-init
"""

# <!-- SSOT Domain: core -->
# AUTO-GENERATED __init__.py
# DO NOT EDIT MANUALLY - changes may be overwritten

# LockOperations removed - use FileLockManager directly
from . import lock_queries

__all__ = [
    'lock_queries',
]
