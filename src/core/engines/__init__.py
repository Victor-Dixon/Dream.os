# <!-- SSOT Domain: core -->
# AUTO-GENERATED __init__.py
# DO NOT EDIT MANUALLY - changes may be overwritten

from .base_engine import BaseEngine

__all__ = ["BaseEngine"]

# Registry removed from __init__.py to avoid circular dependencies
# Import directly: from src.core.engines.registry import EngineRegistry

from . import analysis_core_engine
from . import communication_core_engine
from . import contracts
from . import coordination_core_engine
from . import data_core_engine
from . import engine_lifecycle
from . import engine_monitoring
from . import engine_state
from . import integration_core_engine
from . import ml_core_engine
from . import monitoring_core_engine
from . import orchestration_core_engine
from . import performance_core_engine
from . import processing_core_engine
from . import security_core_engine
from . import storage_core_engine
from . import utility_core_engine
from . import validation_core_engine

__all__ = [
    'analysis_core_engine',
    'communication_core_engine',
    'contracts',
    'coordination_core_engine',
    'data_core_engine',
    'engine_lifecycle',
    'engine_monitoring',
    'engine_state',
    'integration_core_engine',
    'ml_core_engine',
    'monitoring_core_engine',
    'orchestration_core_engine',
    'performance_core_engine',
    'processing_core_engine',
    # 'registry' - Import directly: from src.core.engines.registry import EngineRegistry
    'security_core_engine',
    'storage_core_engine',
    'utility_core_engine',
    'validation_core_engine',
]
