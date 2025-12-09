"""
Dependency Injection Container
==============================

Provides dependency injection for use cases.
Wires domain ports to infrastructure implementations.

<!-- SSOT Domain: infrastructure -->

V2 Compliance: < 300 lines, DI container pattern.
"""

from collections.abc import Iterable
from typing import Any, Dict

from src.domain.entities.agent import Agent as DomainAgent
from src.domain.entities.task import Task as DomainTask
from src.domain.ports.agent_repository import AgentRepository
from src.domain.ports.logger import Logger
from src.domain.ports.message_bus import MessageBus
from src.domain.ports.task_repository import TaskRepository
from src.domain.services.assignment_service import AssignmentService
from src.domain.value_objects.ids import AgentId, TaskId
from src.infrastructure.persistence.agent_repository import (
    AgentRepository as InfraAgentRepository,
)
from src.infrastructure.persistence.database_connection import (
    DatabaseConnection,
)
from src.infrastructure.persistence.task_repository import (
    TaskRepository as InfraTaskRepository,
)


class DomainTaskRepositoryAdapter:
    """Adapter to bridge infrastructure TaskRepository to domain TaskRepository port."""

    def __init__(self, infra_repo: InfraTaskRepository):
        self.infra_repo = infra_repo

    def get(self, task_id: TaskId) -> DomainTask | None:
        """Get task by ID."""
        infra_task = self.infra_repo.get(str(task_id))
        if not infra_task:
            return None
        return self._to_domain(infra_task)

    def get_by_agent(self, agent_id: str, limit: int = 100) -> Iterable[DomainTask]:
        """Get tasks by agent ID."""
        for infra_task in self.infra_repo.get_by_agent(agent_id, limit):
            yield self._to_domain(infra_task)

    def get_pending(self, limit: int = 100) -> Iterable[DomainTask]:
        """Get pending tasks."""
        for infra_task in self.infra_repo.get_pending(limit):
            yield self._to_domain(infra_task)

    def add(self, task: DomainTask) -> None:
        """Add new task."""
        infra_task = self._to_infra(task)
        self.infra_repo.save(infra_task)

    def save(self, task: DomainTask) -> None:
        """Save task."""
        infra_task = self._to_infra(task)
        self.infra_repo.save(infra_task)

    def delete(self, task_id: TaskId) -> bool:
        """Delete task."""
        return self.infra_repo.delete(str(task_id))

    def list_all(self, limit: int = 1000) -> Iterable[DomainTask]:
        """List all tasks."""
        for infra_task in self.infra_repo.list_all(limit):
            yield self._to_domain(infra_task)

    def _to_domain(self, infra_task) -> DomainTask:
        """Convert infrastructure task to domain task."""
        # Infrastructure repository returns persistence model objects
        # Extract assigned_at from task if available
        assigned_at = getattr(infra_task, "assigned_at", None)
        # If not in persistence model, try to infer from status
        if assigned_at is None and infra_task.assigned_agent_id:
            # Task is assigned but assigned_at not stored - use created_at as fallback
            assigned_at = infra_task.created_at

        return DomainTask(
            id=TaskId(infra_task.id),
            title=infra_task.title,
            description=infra_task.description or None,
            assigned_agent_id=AgentId(infra_task.assigned_agent_id)
            if infra_task.assigned_agent_id
            else None,
            created_at=infra_task.created_at,
            assigned_at=assigned_at,
            completed_at=infra_task.completed_at,
            priority=infra_task.priority,
        )

    def _to_infra(self, domain_task: DomainTask):
        """Convert domain task to infrastructure task."""
        from src.infrastructure.persistence.persistence_models import TaskPersistenceModel

        task = TaskPersistenceModel(
            id=str(domain_task.id),
            title=domain_task.title,
            description=domain_task.description or "",
            assigned_agent_id=str(domain_task.assigned_agent_id)
            if domain_task.assigned_agent_id
            else None,
            status="completed" if domain_task.is_completed else "pending",
            priority=domain_task.priority,
            created_at=domain_task.created_at,
            completed_at=domain_task.completed_at,
        )
        # Add assigned_at if available (persistence model may not have it)
        if domain_task.assigned_at:
            task.assigned_at = domain_task.assigned_at
        return task


class DomainAgentRepositoryAdapter:
    """Adapter to bridge infrastructure AgentRepository to domain AgentRepository port."""

    def __init__(self, infra_repo: InfraAgentRepository):
        self.infra_repo = infra_repo

    def get(self, agent_id: AgentId) -> DomainAgent | None:
        """Get agent by ID."""
        infra_agent = self.infra_repo.get(str(agent_id))
        if not infra_agent:
            return None
        return self._to_domain(infra_agent)

    def get_by_capability(self, capability: str) -> Iterable[DomainAgent]:
        """Get agents by capability."""
        for infra_agent in self.infra_repo.get_by_capability(capability):
            yield self._to_domain(infra_agent)

    def get_active(self) -> Iterable[DomainAgent]:
        """Get active agents."""
        for infra_agent in self.infra_repo.get_active():
            yield self._to_domain(infra_agent)

    def get_available(self) -> Iterable[DomainAgent]:
        """Get available agents."""
        for infra_agent in self.infra_repo.get_available():
            yield self._to_domain(infra_agent)

    def add(self, agent: DomainAgent) -> None:
        """Add new agent."""
        infra_agent = self._to_infra(agent)
        self.infra_repo.save(infra_agent)

    def save(self, agent: DomainAgent) -> None:
        """Save agent."""
        infra_agent = self._to_infra(agent)
        self.infra_repo.save(infra_agent)

    def delete(self, agent_id: AgentId) -> bool:
        """Delete agent."""
        return self.infra_repo.delete(str(agent_id))

    def list_all(self) -> Iterable[DomainAgent]:
        """List all agents."""
        for infra_agent in self.infra_repo.list_all():
            yield self._to_domain(infra_agent)

    def _to_domain(self, infra_agent) -> DomainAgent:
        """Convert infrastructure agent to domain agent."""
        # Infrastructure repository returns persistence model objects
        return DomainAgent(
            id=AgentId(infra_agent.id),
            name=infra_agent.name,
            role=infra_agent.role,
            capabilities=set(infra_agent.capabilities or []),
            max_concurrent_tasks=infra_agent.max_concurrent_tasks,
            is_active=infra_agent.is_active,
            created_at=infra_agent.created_at,
            last_active_at=infra_agent.last_active_at,
            current_task_ids=[],  # Would need to query tasks separately
        )

    def _to_infra(self, domain_agent: DomainAgent):
        """Convert domain agent to infrastructure agent."""
        from src.infrastructure.persistence.persistence_models import Agent

        return Agent(
            id=str(domain_agent.id),
            name=domain_agent.name,
            role=domain_agent.role,
            capabilities=list(domain_agent.capabilities),
            max_concurrent_tasks=domain_agent.max_concurrent_tasks,
            is_active=domain_agent.is_active,
            created_at=domain_agent.created_at,
            last_active_at=domain_agent.last_active_at,
        )


class SimpleLogger:
    """Simple logger implementation for use cases."""

    def info(self, message: str, **kwargs) -> None:
        """Log info message."""
        print(f"INFO: {message} {kwargs}")

    def error(self, message: str, **kwargs) -> None:
        """Log error message."""
        print(f"ERROR: {message} {kwargs}")


class SimpleMessageBus(MessageBus):
    """Simple message bus implementation for use cases."""

    def publish(self, event_type: str, event_data: Dict[str, Any]) -> None:
        """Publish domain event."""
        print(f"EVENT: {event_type} {event_data}")

    def subscribe(self, event_type: str, handler: callable) -> None:
        """Subscribe to event type."""
        pass  # Simple implementation - no-op

    def unsubscribe(self, event_type: str, handler: callable) -> None:
        """Unsubscribe from event type."""
        pass  # Simple implementation - no-op

    def get_subscribers(self, event_type: str) -> list:
        """Get subscribers for event type."""
        return []  # Simple implementation - no subscribers

    def is_available(self) -> bool:
        """Check if message bus is available."""
        return True

    def get_stats(self) -> Dict[str, Any]:
        """Get message bus statistics."""
        return {"events_published": 0}


# Singleton instances
_task_repository: TaskRepository | None = None
_agent_repository: AgentRepository | None = None
_message_bus: MessageBus | None = None
_logger: Logger | None = None
_assignment_service: AssignmentService | None = None


def get_dependencies() -> Dict[str, Any]:
    """
    Get dependency injection container.

    Returns:
        Dictionary of dependencies
    """
    global _task_repository, _agent_repository, _message_bus, _logger, _assignment_service

    # Lazy initialization
    if _task_repository is None:
        from src.infrastructure.persistence.persistence_models import (
            PersistenceConfig,
        )

        config = PersistenceConfig()
        db_conn = DatabaseConnection(config)
        infra_task_repo = InfraTaskRepository(db_conn)
        _task_repository = DomainTaskRepositoryAdapter(infra_task_repo)

    if _agent_repository is None:
        from src.infrastructure.persistence.persistence_models import (
            PersistenceConfig,
        )

        config = PersistenceConfig()
        db_conn = DatabaseConnection(config)
        infra_agent_repo = InfraAgentRepository(db_conn)
        _agent_repository = DomainAgentRepositoryAdapter(infra_agent_repo)

    if _message_bus is None:
        _message_bus = SimpleMessageBus()

    if _logger is None:
        _logger = SimpleLogger()

    if _assignment_service is None:
        _assignment_service = AssignmentService(_logger)

    return {
        "task_repository": _task_repository,
        "agent_repository": _agent_repository,
        "message_bus": _message_bus,
        "logger": _logger,
        "assignment_service": _assignment_service,
    }

