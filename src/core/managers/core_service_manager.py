"""
Core Service Manager - Backward-Compatible Wrapper
==================================================

<!-- SSOT Domain: integration -->

Backward-compatible wrapper for CoreServiceCoordinator.
Maintains historical import path while delegating to new coordinator.

V2 Compliance: Wrapper pattern, <100 lines
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-12-03
"""

from __future__ import annotations

from typing import Any

from .core_service_coordinator import CoreServiceCoordinator
from .contracts import ManagerContext, ManagerResult


class CoreServiceManager(CoreServiceCoordinator):
    """
    Maintains historical import path for service manager.
    
    This class provides backward compatibility for code that imports
    CoreServiceManager instead of CoreServiceCoordinator.
    
    All functionality is delegated to CoreServiceCoordinator.
    """

    def __init__(self) -> None:
        """Initialize core service manager (delegates to coordinator)."""
        super().__init__()

    def get_onboarding_manager(self):
        """Get onboarding manager instance."""
        return self.onboarding

    def get_recovery_manager(self):
        """Get recovery manager instance."""
        return self.recovery

    def get_results_manager(self):
        """Get results manager instance."""
        return self.results

    def is_initialized(self) -> bool:
        """Check if service manager is initialized."""
        return self.initialized

    def get_status(self) -> dict[str, Any]:
        """Get service manager status."""
        return {
            "initialized": self.initialized,
            "onboarding_available": self.onboarding is not None,
            "recovery_available": self.recovery is not None,
            "results_available": self.results is not None,
        }
