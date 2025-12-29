"""
<!-- SSOT Domain: core -->

Single Source of Truth (SSOT) for Execution Domain Management
Domain: execution
Owner: Agent-2 (Architecture & Design)
Last Updated: 2025-12-08
Related SSOT: src/core/managers/base_manager.py, src/core/managers/contracts.py

Execution Domain Manager - SSOT for Execution-Related Operations
=================================================================

Provides unified interface for all execution-related manager operations.
Consolidates execution coordination, service routing, and task management.

V2 Compliance: < 300 lines, single responsibility, BaseManager inheritance.

Features:
- Unified execution interface
- Service coordination routing
- Task lifecycle management
- Protocol registration and execution
- Status aggregation across execution components

Consolidates:
- CoreExecutionManager functionality
- CoreServiceCoordinator routing
- Execution protocol management
- Task coordination patterns
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Callable
from .contracts import Manager, ManagerContext, ManagerResult
from .execution import ExecutionCoordinator


class ExecutionDomainManager(Manager):
    """
    SSOT for execution domain operations.

    Consolidates execution management functionality across:
    - Task execution and coordination
    - Service routing and delegation
    - Protocol registration and execution
    - Status aggregation and monitoring
    """

    def __init__(self) -> None:
        """Initialize execution domain manager with coordinator."""
        self.coordinator = ExecutionCoordinator()
        self._protocols: Dict[str, Callable] = {}
        self._service_managers: Dict[str, Manager] = {}
        self.initialized = False

    def initialize(self, context: ManagerContext) -> bool:
        """
        Initialize execution domain.

        Sets up coordinator and registers core execution protocols.
        """
        try:
            # Initialize execution coordinator
            if not self.coordinator.initialize(context):
                return False

            # Register core execution protocols
            self._register_core_protocols()

            self.initialized = True
            return True

        except Exception as e:
            context.logger.error(f"Failed to initialize execution domain: {e}")
            return False

    def execute(
        self, context: ManagerContext, operation: str, payload: Dict[str, Any]
    ) -> ManagerResult:
        """
        Execute operation within execution domain.

        Routes operations to appropriate execution components:
        - Task operations → coordinator
        - Service operations → service managers
        - Protocol operations → registered protocols
        """
        try:
            # Route task operations to coordinator
            if operation in {"execute_task", "create_task", "get_task_status"}:
                return self._execute_task_operation(context, operation, payload)

            # Route service operations to appropriate managers
            if operation in self._get_service_operations():
                return self._execute_service_operation(context, operation, payload)

            # Route protocol operations
            if operation.startswith("protocol_"):
                return self._execute_protocol_operation(context, operation, payload)

            # Route general execution operations to coordinator
            return self.coordinator.execute(context, operation, payload)

        except Exception as e:
            return ManagerResult(
                False, {}, {}, f"Execution domain error: {e}"
            )

    def register_protocol(
        self, context: ManagerContext, protocol_name: str, protocol_handler: Callable
    ) -> ManagerResult:
        """Register a protocol handler."""
        try:
            self._protocols[protocol_name] = protocol_handler
            return ManagerResult(
                True, {"protocol_registered": protocol_name}, {}, "Protocol registered"
            )
        except Exception as e:
            return ManagerResult(
                False, {}, {}, f"Protocol registration failed: {e}"
            )

    def register_service_manager(
        self, service_name: str, manager: Manager
    ) -> bool:
        """Register a service manager for delegation."""
        try:
            self._service_managers[service_name] = manager
            return True
        except Exception:
            return False

    def cleanup(self, context: ManagerContext) -> bool:
        """Cleanup execution domain resources."""
        try:
            # Cleanup coordinator
            self.coordinator.cleanup(context)

            # Cleanup service managers
            for manager in self._service_managers.values():
                try:
                    manager.cleanup(context)
                except Exception:
                    pass  # Continue cleanup even if one fails

            # Clear registrations
            self._protocols.clear()
            self._service_managers.clear()

            return True

        except Exception as e:
            context.logger.error(f"Execution domain cleanup error: {e}")
            return False

    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive execution domain status."""
        status = {
            "domain": "execution",
            "initialized": self.initialized,
            "protocols_registered": len(self._protocols),
            "service_managers": len(self._service_managers),
            "coordinator_status": self.coordinator.get_status(),
        }

        # Aggregate service manager statuses
        service_statuses = {}
        for name, manager in self._service_managers.items():
            try:
                service_statuses[name] = manager.get_status()
            except Exception:
                service_statuses[name] = {"error": "Status unavailable"}

        status["service_statuses"] = service_statuses
        return status

    def _register_core_protocols(self) -> None:
        """Register core execution protocols."""
        # Task execution protocol
        self._protocols["task_execution"] = self._execute_task_protocol

        # Service coordination protocol
        self._protocols["service_coordination"] = self._execute_service_protocol

    def _execute_task_operation(
        self, context: ManagerContext, operation: str, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Execute task-related operations."""
        if operation == "execute_task":
            return self.coordinator.execute_task(
                context, payload.get("task_id"), payload.get("task_data", {})
            )
        elif operation == "create_task":
            return self.coordinator.create_task(
                context,
                payload.get("task_type", "default"),
                payload.get("priority", 5),
                payload.get("data")
            )
        elif operation == "get_task_status":
            return self.coordinator.get_task_status(
                context, payload.get("task_id", "")
            )

        return ManagerResult(
            False, {}, {}, f"Unknown task operation: {operation}"
        )

    def _execute_service_operation(
        self, context: ManagerContext, operation: str, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Execute service-related operations by routing to appropriate managers."""
        # Map operations to service managers
        service_routes = {
            # Onboarding operations
            ("onboard_agent", "start_onboarding", "complete_onboarding", "get_onboarding_status"): "onboarding",

            # Recovery operations
            ("register_recovery_strategy", "recover_from_error", "get_recovery_strategies"): "recovery",

            # Results operations
            ("process_results", "get_results"): "results",
        }

        for operations, service_name in service_routes.items():
            if operation in operations:
                manager = self._service_managers.get(service_name)
                if manager:
                    return manager.execute(context, operation, payload)
                else:
                    return ManagerResult(
                        False, {}, {}, f"Service manager not available: {service_name}"
                    )

        return ManagerResult(
            False, {}, {}, f"No route found for service operation: {operation}"
        )

    def _execute_protocol_operation(
        self, context: ManagerContext, operation: str, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Execute protocol-related operations."""
        protocol_name = operation.replace("protocol_", "")
        protocol_handler = self._protocols.get(protocol_name)

        if protocol_handler:
            try:
                return protocol_handler(context, payload)
            except Exception as e:
                return ManagerResult(
                    False, {}, {}, f"Protocol execution failed: {e}"
                )
        else:
            return ManagerResult(
                False, {}, {}, f"Protocol not found: {protocol_name}"
            )

    def _get_service_operations(self) -> List[str]:
        """Get list of all service operations."""
        return [
            "onboard_agent", "start_onboarding", "complete_onboarding", "get_onboarding_status",
            "register_recovery_strategy", "recover_from_error", "get_recovery_strategies",
            "process_results", "get_results"
        ]

    def _execute_task_protocol(
        self, context: ManagerContext, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Execute task protocol."""
        return self.coordinator.execute_protocol(
            context, "task_execution", payload
        )

    def _execute_service_protocol(
        self, context: ManagerContext, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Execute service coordination protocol."""
        service_name = payload.get("service")
        if service_name and service_name in self._service_managers:
            return self._service_managers[service_name].execute(
                context, payload.get("operation", ""), payload
            )

        return ManagerResult(
            False, {}, {}, "Service not found or operation not specified"
        )

