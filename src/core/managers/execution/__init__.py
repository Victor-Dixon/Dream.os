# Header-Variant: full
# Owner: @dreamos/platform
# Purpose: __init__ module.
# SSOT: docs/recovery/recovery_registry.yaml#src-core-managers-execution-init
# @registry docs/recovery/recovery_registry.yaml#src-core-managers-execution-init

"""
@file __init__.py
@summary Module implementation.
@registry docs/recovery/recovery_registry.yaml#src-core-managers-execution-init
"""
# <!-- SSOT Domain: core -->
# AUTO-GENERATED __init__.py
# DO NOT EDIT MANUALLY - changes may be overwritten

from . import base_execution_manager
from . import execution_coordinator
from . import execution_operations
from . import execution_runner
from . import protocol_manager
from . import task_executor

# Export ExecutionCoordinator for use in core_execution_manager
from .execution_coordinator import ExecutionCoordinator

__all__ = [
    'base_execution_manager',
    'execution_coordinator',
    'execution_operations',
    'execution_runner',
    'protocol_manager',
    'task_executor',
    'ExecutionCoordinator',
]
