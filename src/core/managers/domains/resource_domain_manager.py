"""
<!-- SSOT Domain: core -->

Single Source of Truth (SSOT) for Resource Domain Management
Domain: resources
Owner: Agent-2 (Architecture & Design)
Last Updated: 2025-12-08
Related SSOT: src/core/managers/base_manager.py, src/core/managers/core_resource_manager.py

Resource Domain Manager - SSOT for Resource-Related Operations
===============================================================

Provides unified interface for all resource management operations.
Consolidates file operations, locking, CRUD operations, and context management.

V2 Compliance: < 300 lines, single responsibility, BaseManager inheritance.

Features:
- Unified resource operation interface
- File system operations (read, write, delete, move)
- Resource locking and concurrency control
- CRUD operations for resource management
- Context-aware resource operations
- Status monitoring and health checks

Consolidates:
- FileOperations functionality
- LockOperations functionality
- ResourceCRUDOperations functionality
- ContextOperations functionality
- CoreResourceManager coordination
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional, Union
from pathlib import Path

from .contracts import Manager, ManagerContext, ManagerResult
from .resource_file_operations import FileOperations
from .resource_lock_operations import LockOperations
from .resource_crud_operations import ResourceCRUDOperations
from .resource_context_operations import ContextOperations


class ResourceDomainManager(Manager):
    """
    SSOT for resource domain operations.

    Consolidates all resource management functionality into a unified interface.
    Provides high-level operations that delegate to specialized operation classes.
    """

    def __init__(self) -> None:
        """Initialize resource domain manager with all operation modules."""
        self.file_ops = FileOperations()
        self.lock_ops = LockOperations()
        self.crud_ops = ResourceCRUDOperations()
        self.context_ops = ContextOperations()
        self.initialized = False

    def initialize(self, context: ManagerContext) -> bool:
        """
        Initialize resource domain.

        Sets up all resource operation modules and validates environment.
        """
        try:
            # Initialize all operation modules
            modules_initialized = [
                self.file_ops.initialize(context),
                self.lock_ops.initialize(context),
                self.crud_ops.initialize(context),
                self.context_ops.initialize(context),
            ]

            # Check if all modules initialized successfully
            if not all(modules_initialized):
                failed_modules = [
                    name for name, init in zip(
                        ["file_ops", "lock_ops", "crud_ops", "context_ops"],
                        modules_initialized
                    ) if not init
                ]
                context.logger.error(f"Resource domain initialization failed for: {failed_modules}")
                return False

            self.initialized = True
            return True

        except Exception as e:
            context.logger.error(f"Resource domain initialization error: {e}")
            return False

    def execute(
        self, context: ManagerContext, operation: str, payload: Dict[str, Any]
    ) -> ManagerResult:
        """
        Execute resource operation by routing to appropriate module.

        Supports operations across all resource domains:
        - File operations: read, write, delete, move, copy
        - Lock operations: acquire, release, check status
        - CRUD operations: create, read, update, delete resources
        - Context operations: context-aware resource management
        """
        try:
            # Route file operations
            if operation in self._get_file_operations():
                return self._execute_file_operation(context, operation, payload)

            # Route lock operations
            if operation in self._get_lock_operations():
                return self._execute_lock_operation(context, operation, payload)

            # Route CRUD operations
            if operation in self._get_crud_operations():
                return self._execute_crud_operation(context, operation, payload)

            # Route context operations
            if operation in self._get_context_operations():
                return self._execute_context_operation(context, operation, payload)

            return ManagerResult(
                False, {}, {}, f"Unknown resource operation: {operation}"
            )

        except Exception as e:
            return ManagerResult(
                False, {}, {}, f"Resource operation error: {e}"
            )

    def cleanup(self, context: ManagerContext) -> bool:
        """Cleanup all resource domain resources."""
        try:
            # Cleanup all operation modules
            cleanup_results = [
                self.file_ops.cleanup(context),
                self.lock_ops.cleanup(context),
                self.crud_ops.cleanup(context),
                self.context_ops.cleanup(context),
            ]

            # Log any cleanup failures but don't fail overall cleanup
            failed_cleanups = [
                name for name, result in zip(
                    ["file_ops", "lock_ops", "crud_ops", "context_ops"],
                    cleanup_results
                ) if not result
            ]

            if failed_cleanups:
                context.logger.warning(f"Resource cleanup incomplete for: {failed_cleanups}")

            return True

        except Exception as e:
            context.logger.error(f"Resource domain cleanup error: {e}")
            return False

    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive resource domain status."""
        status = {
            "domain": "resources",
            "initialized": self.initialized,
            "modules": {
                "file_operations": self.file_ops.get_status(),
                "lock_operations": self.lock_ops.get_status(),
                "crud_operations": self.crud_ops.get_status(),
                "context_operations": self.context_ops.get_status(),
            }
        }

        # Aggregate health metrics
        health_metrics = self._calculate_health_metrics()
        status.update(health_metrics)

        return status

    def _calculate_health_metrics(self) -> Dict[str, Any]:
        """Calculate overall health metrics for resource domain."""
        try:
            # Get individual module statuses
            file_status = self.file_ops.get_status()
            lock_status = self.lock_ops.get_status()
            crud_status = self.crud_ops.get_status()
            context_status = self.context_ops.get_status()

            # Calculate aggregate metrics
            total_operations = (
                file_status.get("total_operations", 0) +
                lock_status.get("total_operations", 0) +
                crud_status.get("total_operations", 0) +
                context_status.get("total_operations", 0)
            )

            active_locks = lock_status.get("active_locks", 0)
            failed_operations = (
                file_status.get("failed_operations", 0) +
                lock_status.get("failed_operations", 0) +
                crud_status.get("failed_operations", 0) +
                context_status.get("failed_operations", 0)
            )

            return {
                "health_score": 100 - min(100, failed_operations * 5),  # Penalty per failure
                "total_operations": total_operations,
                "active_locks": active_locks,
                "failed_operations": failed_operations,
                "modules_healthy": all([
                    file_status.get("healthy", True),
                    lock_status.get("healthy", True),
                    crud_status.get("healthy", True),
                    context_status.get("healthy", True),
                ])
            }

        except Exception:
            return {
                "health_score": 0,
                "error": "Health calculation failed"
            }

    def _execute_file_operation(
        self, context: ManagerContext, operation: str, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Execute file-related operations."""
        file_path = payload.get("file_path")
        if not file_path:
            return ManagerResult(False, {}, {}, "file_path required for file operations")

        # Route to appropriate file operation
        if operation == "read_file":
            content = self.file_ops.read_file(file_path)
            return ManagerResult(True, {"content": content}, {}, "File read successfully")

        elif operation == "write_file":
            content = payload.get("content", "")
            success = self.file_ops.write_file(file_path, content)
            return ManagerResult(success, {}, {}, "File write completed" if success else "File write failed")

        elif operation == "delete_file":
            success = self.file_ops.delete_file(file_path)
            return ManagerResult(success, {}, {}, "File deleted" if success else "File delete failed")

        elif operation == "file_exists":
            exists = self.file_ops.file_exists(file_path)
            return ManagerResult(True, {"exists": exists}, {}, "File existence checked")

        return ManagerResult(False, {}, {}, f"Unsupported file operation: {operation}")

    def _execute_lock_operation(
        self, context: ManagerContext, operation: str, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Execute lock-related operations."""
        resource_id = payload.get("resource_id")
        if not resource_id:
            return ManagerResult(False, {}, {}, "resource_id required for lock operations")

        if operation == "acquire_lock":
            timeout = payload.get("timeout", 30)
            success = self.lock_ops.acquire_lock(resource_id, timeout)
            return ManagerResult(success, {}, {}, "Lock acquired" if success else "Lock acquisition failed")

        elif operation == "release_lock":
            success = self.lock_ops.release_lock(resource_id)
            return ManagerResult(success, {}, {}, "Lock released" if success else "Lock release failed")

        elif operation == "check_lock":
            locked = self.lock_ops.is_locked(resource_id)
            return ManagerResult(True, {"locked": locked}, {}, "Lock status checked")

        return ManagerResult(False, {}, {}, f"Unsupported lock operation: {operation}")

    def _execute_crud_operation(
        self, context: ManagerContext, operation: str, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Execute CRUD operations."""
        resource_id = payload.get("resource_id")
        if not resource_id:
            return ManagerResult(False, {}, {}, "resource_id required for CRUD operations")

        if operation == "create_resource":
            data = payload.get("data", {})
            success = self.crud_ops.create(resource_id, data)
            return ManagerResult(success, {}, {}, "Resource created" if success else "Resource creation failed")

        elif operation == "read_resource":
            data = self.crud_ops.read(resource_id)
            success = data is not None
            return ManagerResult(success, {"data": data or {}}, {}, "Resource read successfully" if success else "Resource not found")

        elif operation == "update_resource":
            data = payload.get("data", {})
            success = self.crud_ops.update(resource_id, data)
            return ManagerResult(success, {}, {}, "Resource updated" if success else "Resource update failed")

        elif operation == "delete_resource":
            success = self.crud_ops.delete(resource_id)
            return ManagerResult(success, {}, {}, "Resource deleted" if success else "Resource deletion failed")

        return ManagerResult(False, {}, {}, f"Unsupported CRUD operation: {operation}")

    def _execute_context_operation(
        self, context: ManagerContext, operation: str, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Execute context-aware operations."""
        if operation == "get_context":
            ctx_data = self.context_ops.get_context(context)
            return ManagerResult(True, {"context": ctx_data}, {}, "Context retrieved")

        elif operation == "update_context":
            updates = payload.get("updates", {})
            success = self.context_ops.update_context(context, updates)
            return ManagerResult(success, {}, {}, "Context updated" if success else "Context update failed")

        elif operation == "validate_context":
            valid = self.context_ops.validate_context(context)
            return ManagerResult(True, {"valid": valid}, {}, "Context validated")

        return ManagerResult(False, {}, {}, f"Unsupported context operation: {operation}")

    def _get_file_operations(self) -> List[str]:
        """Get list of supported file operations."""
        return ["read_file", "write_file", "delete_file", "file_exists", "move_file", "copy_file"]

    def _get_lock_operations(self) -> List[str]:
        """Get list of supported lock operations."""
        return ["acquire_lock", "release_lock", "check_lock", "list_locks"]

    def _get_crud_operations(self) -> List[str]:
        """Get list of supported CRUD operations."""
        return ["create_resource", "read_resource", "update_resource", "delete_resource", "list_resources"]

    def _get_context_operations(self) -> List[str]:
        """Get list of supported context operations."""
        return ["get_context", "update_context", "validate_context", "clear_context"]

