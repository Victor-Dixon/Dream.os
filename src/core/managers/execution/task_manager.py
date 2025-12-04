"""
Task Manager - Redirect Shim
============================

Redirects imports from `src.core.managers.execution.task_manager` to the
actual task management components. This maintains backward compatibility
for code expecting the old import path.

The actual task management functionality is provided by:
- `TaskExecutor` - Task execution logic
- `BaseExecutionManager` - Execution management
- `ExecutionOperations` - Task operations

<!-- SSOT Domain: integration -->

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-12-03
V2 Compliant: Yes (<300 lines)
"""

# Import actual task management components
from .task_executor import TaskExecutor
from .base_execution_manager import BaseExecutionManager
from .execution_operations import ExecutionOperations, TaskStatus
from .execution_coordinator import ExecutionCoordinator

# Re-export for backward compatibility
# Most code expects a "TaskManager" class, so we alias TaskExecutor
TaskManager = TaskExecutor

__all__ = [
    "TaskManager",
    "TaskExecutor",
    "BaseExecutionManager",
    "ExecutionOperations",
    "ExecutionCoordinator",
    "TaskStatus",
]

