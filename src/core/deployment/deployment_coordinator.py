"""
<!-- SSOT Domain: core -->

Deployment Coordinator - SSOT for deployment coordination
========================================================

Central coordinator for deployment operations.
Provides unified interface for deployment execution, metrics, and discovery.

Author: Agent-2 (Architecture & Design Specialist) - Created to fix broken imports
License: MIT
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional, Dict, List
from enum import Enum

from ..config.timeout_constants import TimeoutConstants


class DeploymentStatus(Enum):
    """Deployment status states."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class DeploymentConfig:
    """Deployment configuration."""
    target_environment: str = "production"
    timeout_seconds: float = TimeoutConstants.HTTP_EXTENDED
    retry_attempts: int = 3
    enable_rollback: bool = True
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        """Initialize default values."""
        if self.metadata is None:
            self.metadata = {}


@dataclass
class DeploymentTask:
    """Deployment task model."""
    task_id: str
    description: str
    status: DeploymentStatus = DeploymentStatus.PENDING
    created_at: datetime = None
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        """Initialize default values."""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.metadata is None:
            self.metadata = {}


class DeploymentCoordinator:
    """Central coordinator for deployment operations."""
    
    def __init__(self, config: Optional[DeploymentConfig] = None):
        """Initialize deployment coordinator."""
        self.config = config or DeploymentConfig()
        self.active_deployments: Dict[str, DeploymentTask] = {}
        self.deployment_history: List[DeploymentTask] = []
    
    def create_deployment(self, task_id: str, description: str) -> DeploymentTask:
        """Create a new deployment task."""
        task = DeploymentTask(
            task_id=task_id,
            description=description
        )
        self.active_deployments[task_id] = task
        return task
    
    def get_deployment(self, task_id: str) -> Optional[DeploymentTask]:
        """Get deployment task by ID."""
        return self.active_deployments.get(task_id)
    
    def complete_deployment(self, task_id: str, success: bool = True) -> bool:
        """Mark deployment as completed."""
        task = self.active_deployments.get(task_id)
        if not task:
            return False
        
        task.status = DeploymentStatus.COMPLETED if success else DeploymentStatus.FAILED
        task.completed_at = datetime.now()
        
        self.deployment_history.append(task)
        self.active_deployments.pop(task_id, None)
        
        return True


__all__ = [
    "DeploymentCoordinator",
    "DeploymentConfig",
    "DeploymentTask",
    "DeploymentStatus",
]

