# Header-Variant: full
# Owner: Dream.os
# Purpose: Module implementation and orchestration logic.
# SSOT: docs/recovery/recovery_registry.yaml#src-core-ssot-unified-ssot-execution-init
# @registry docs/recovery/recovery_registry.yaml#src-core-ssot-unified-ssot-execution-init

# <!-- SSOT Domain: core -->
# AUTO-GENERATED __init__.py
# DO NOT EDIT MANUALLY - changes may be overwritten

from . import execution_manager
from . import task_executor

__all__ = [
    'execution_manager',
    'task_executor',
]
