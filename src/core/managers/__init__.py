"""Core managers package exports.

<!-- SSOT Domain: core -->

Keep package initialization minimal to avoid circular imports and hard
failures from optional modules during test collection.
"""

from importlib import import_module

__all__ = [
    "base_manager",
    "base_manager_helpers",
    "config_defaults",
    "contracts",
    "core_execution_manager",
    "core_onboarding_manager",
    "core_recovery_manager",
    "core_resource_manager",
    "core_results_manager",
    "core_service_coordinator",
    "core_service_manager",
    "manager_lifecycle",
    "manager_metrics",
    "manager_operations",
    "manager_state",
    "registry",
    "resource_context_operations",
    "resource_crud_operations",
    "resource_file_operations",
    "resource_lock_operations",
]


def __getattr__(name: str):
    if name in __all__:
        module = import_module(f"{__name__}.{name}")
        globals()[name] = module
        return module
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
