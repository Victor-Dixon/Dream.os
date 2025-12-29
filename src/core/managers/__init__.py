# <!-- SSOT Domain: core -->
# AUTO-GENERATED __init__.py
# DO NOT EDIT MANUALLY - changes may be overwritten

from . import base_manager
from . import base_manager_helpers
from . import config_defaults
from . import contracts
# from . import core_configuration_manager  # File does not exist - commented out
from . import core_execution_manager
# from . import core_monitoring_manager  # File does not exist - commented out
from . import core_onboarding_manager
from . import core_recovery_manager
from . import core_resource_manager
from . import core_results_manager
from . import core_service_coordinator
from . import core_service_manager
from . import manager_lifecycle
from . import manager_metrics
from . import manager_operations
from . import manager_state
from . import registry
from . import resource_context_operations
from . import resource_crud_operations
from . import resource_file_operations
from . import resource_lock_operations

__all__ = [
    'base_manager',
    'base_manager_helpers',
    'config_defaults',
    'contracts',
    # 'core_configuration_manager',  # Consolidated into config_manager.py and config_defaults.py
    'core_execution_manager',
    # 'core_monitoring_manager',  # Consolidated into monitoring/ subdirectory
    'core_onboarding_manager',
    'core_recovery_manager',
    'core_resource_manager',
    'core_results_manager',
    'core_service_coordinator',
    'core_service_manager',
    'manager_lifecycle',
    'manager_metrics',
    'manager_operations',
    'manager_state',
    'registry',
    'resource_context_operations',
    'resource_crud_operations',
    'resource_file_operations',
    'resource_lock_operations',
]
