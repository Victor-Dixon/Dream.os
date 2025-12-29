"""
<!-- SSOT Domain: core -->

Base Execution Manager - Phase-2 V2 Compliance Refactoring + DUP-004
==========================================================
Base class for execution management. Refactored to <200 lines.
DUP-004: Now inherits from BaseManager for proper hierarchy.
Author: Agent-3, Refactored: Agent-5 | DUP-004: Agent-2 | License: MIT
"""

from __future__ import annotations

import threading
from typing import Any

from src.core.config.timeout_constants import TimeoutConstants

from ..base_manager import BaseManager
from ..contracts import ManagerContext, ManagerResult
from ..manager_state import ManagerType
from .execution_operations import ExecutionOperations, TaskStatus
from .execution_runner import ExecutionRunner
from .protocol_manager import ProtocolManager
from .task_executor import TaskExecutor


class BaseExecutionManager(BaseManager):
    """Base execution manager with common functionality - inherits from BaseManager."""

    def __init__(self):
        """Initialize base execution manager."""
        # Initialize BaseManager first (gets all utilities for free!)
        super().__init__(ManagerType.EXECUTION, "Base Execution Manager")

        # Execution-specific state
        self.tasks: dict[str, dict[str, Any]] = {}
        self.executions: dict[str, dict[str, Any]] = {}
        self.task_queue: list[str] = []
        self.execution_threads: dict[str, threading.Thread] = {}
        self.max_concurrent_tasks = 5
        self.task_timeout=TimeoutConstants.HTTP_EXTENDED

        # Initialize subcomponents
        self.task_executor = TaskExecutor()
        self.protocol_manager = ProtocolManager()
        self.operations = ExecutionOperations(self.tasks, self.task_queue)
        self.runner = ExecutionRunner(
            self.tasks, self.executions, self.execution_threads, self.task_executor
        )

    def initialize(self, context: ManagerContext) -> bool:
        """Initialize execution manager - extends BaseManager initialization."""
        try:
            # Call parent initialization first
            if not super().initialize(context):
                return False

            # Execution-specific initialization
            self.protocol_manager.register_default_protocols()
            self._start_task_processor()
            self.logger.info("Base Execution Manager initialized")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize execution manager: {e}")
            return False

    def _execute_operation(
        self, context: ManagerContext, operation: str, payload: dict[str, Any]
    ) -> ManagerResult:
        """Execute execution-specific operations."""
        # Execution-specific operations only (BaseManager handles validation/error handling)
        if operation == "execute_task":
            return self.runner.execute_task(
                context, payload.get("task_id"), payload.get("task_data", {}), TaskStatus
            )
        elif operation == "register_protocol":
            return self.register_protocol(
                context, payload.get("protocol_name"), payload.get("protocol_data", {})
            )
        elif operation == "get_execution_status":
            return self.runner.get_execution_status(context, payload.get("execution_id"))
        elif operation == "create_task":
            return self.operations.create_task(context, payload)
        elif operation == "cancel_task":
            return self.operations.cancel_task(context, payload)
        elif operation == "list_tasks":
            return self.operations.list_tasks(context, payload)
        elif operation == "list_protocols":
            return self._list_protocols(context, payload)
        else:
            return ManagerResult(
                success=False,
                data={},
                metrics={},
                error=f"Unknown operation: {operation}",
            )

    def execute_task(
        self, context: ManagerContext, task_id: str | None, task_data: dict[str, Any]
    ) -> ManagerResult:
        """Execute a task."""
        return self.runner.execute_task(context, task_id, task_data, TaskStatus)

    def register_protocol(
        self, context: ManagerContext, protocol_name: str | None, protocol_data: dict[str, Any]
    ) -> ManagerResult:
        """Register an execution protocol."""
        try:
            if not protocol_name:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error="Protocol name is required",
                )
            protocol_type = protocol_data.get("type", "routine")
            priority = protocol_data.get("priority", 1)
            timeout = protocol_data.get("timeout", 300)
            success = self.protocol_manager.register_protocol(
                protocol_name, protocol_type, priority, timeout
            )
            if success:
                return ManagerResult(
                    success=True,
                    data={"protocol_name": protocol_name},
                    metrics={"protocols_registered": 1},
                )
            else:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error=f"Failed to register protocol: {protocol_name}",
                )
        except Exception as e:
            self.logger.error(f"Failed to register protocol: {e}")
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def get_execution_status(
        self, context: ManagerContext, execution_id: str | None
    ) -> ManagerResult:
        """Get execution status."""
        return self.runner.get_execution_status(context, execution_id)

    def _list_protocols(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """List all protocols."""
        try:
            protocols = self.protocol_manager.list_protocols()
            return ManagerResult(
                success=True,
                data={"protocols": protocols, "count": len(protocols)},
                metrics={"protocols_listed": len(protocols)},
            )
        except Exception as e:
            self.logger.error(f"Failed to list protocols: {e}")
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def _start_task_processor(self) -> None:
        """Start background task processor."""
        try:
            # Start background thread to process tasks from queue
            def process_tasks():
                """Background task processing loop."""
                while True:
                    try:
                        # Check if there are tasks in queue
                        if self.task_queue:
                            task_id = self.task_queue[0]  # Get first task
                            if task_id in self.tasks:
                                task = self.tasks[task_id]
                                
                                # Update task status
                                task['status'] = 'running'
                                
                                # Execute task using task executor
                                try:
                                    # Determine task type and execute
                                    task_type = task.get('type', 'general')
                                    task_data = task.get('data', {})
                                    
                                    if task_type == 'file':
                                        result = self.task_executor.execute_file_task(task_data)
                                    elif task_type == 'data':
                                        result = self.task_executor.execute_data_task(task_data)
                                    elif task_type == 'api':
                                        result = self.task_executor.execute_api_task(task_data)
                                    else:
                                        result = {'status': 'completed', 'message': 'Task executed'}
                                    
                                    if result.get('status') == 'completed':
                                        task['status'] = 'completed'
                                    else:
                                        task['status'] = 'failed'
                                except Exception as e:
                                    self.logger.error(f"Task {task_id} execution failed: {e}")
                                    task['status'] = 'failed'
                                
                                # Remove from queue
                                if task_id in self.task_queue:
                                    self.task_queue.remove(task_id)
                        
                        # Sleep to avoid busy waiting
                        import time
                        time.sleep(0.5)
                    except Exception as e:
                        self.logger.error(f"Error in task processor loop: {e}")
                        import time
                        time.sleep(1.0)
            
            # Start background thread
            processor_thread = threading.Thread(target=process_tasks, daemon=True)
            processor_thread.start()
            self.logger.info("Background task processor started")
        except Exception as e:
            self.logger.error(f"Failed to start task processor: {e}")
