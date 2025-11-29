"""
Unit tests for task_repo_loader.py
Target: ≥85% coverage
"""

import pytest
import sqlite3
import tempfile
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch
from src.services.helpers.task_repo_loader import SimpleTask, SimpleTaskRepository


class TestSimpleTask:
    """Tests for SimpleTask class."""

    def test_init_with_all_params(self):
        """Test SimpleTask initialization with all parameters."""
        task = SimpleTask(
            id="task-1",
            title="Test Task",
            description="Test Description",
            assigned_agent_id="Agent-1",
            created_at=datetime(2025, 1, 1),
            assigned_at=datetime(2025, 1, 2),
            completed_at=datetime(2025, 1, 3),
            priority=3
        )
        assert task.id == "task-1"
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.assigned_agent_id == "Agent-1"
        assert task.priority == 3

    def test_init_with_minimal_params(self):
        """Test SimpleTask initialization with minimal parameters."""
        task = SimpleTask(id="task-1", title="Test Task")
        assert task.id == "task-1"
        assert task.title == "Test Task"
        assert task.description is None
        assert task.assigned_agent_id is None
        assert task.created_at is not None
        assert task.priority == 1

    def test_is_assigned_false_when_not_assigned(self):
        """Test is_assigned returns False when not assigned."""
        task = SimpleTask(id="task-1", title="Test")
        assert task.is_assigned is False

    def test_is_assigned_true_when_assigned(self):
        """Test is_assigned returns True when assigned."""
        task = SimpleTask(id="task-1", title="Test", assigned_agent_id="Agent-1")
        assert task.is_assigned is True

    def test_is_completed_false_when_not_completed(self):
        """Test is_completed returns False when not completed."""
        task = SimpleTask(id="task-1", title="Test")
        assert task.is_completed is False

    def test_is_completed_true_when_completed(self):
        """Test is_completed returns True when completed."""
        task = SimpleTask(id="task-1", title="Test", completed_at=datetime.utcnow())
        assert task.is_completed is True

    def test_is_pending_true_when_not_assigned_not_completed(self):
        """Test is_pending returns True when not assigned and not completed."""
        task = SimpleTask(id="task-1", title="Test")
        assert task.is_pending is True

    def test_is_pending_false_when_assigned(self):
        """Test is_pending returns False when assigned."""
        task = SimpleTask(id="task-1", title="Test", assigned_agent_id="Agent-1")
        assert task.is_pending is False

    def test_is_pending_false_when_completed(self):
        """Test is_pending returns False when completed."""
        task = SimpleTask(id="task-1", title="Test", completed_at=datetime.utcnow())
        assert task.is_pending is False

    def test_assign_to_success(self):
        """Test assign_to successfully assigns task."""
        task = SimpleTask(id="task-1", title="Test")
        task.assign_to("Agent-1")
        assert task.assigned_agent_id == "Agent-1"
        assert task.is_assigned is True
        assert task.assigned_at is not None

    def test_assign_to_raises_on_completed_task(self):
        """Test assign_to raises ValueError on completed task."""
        task = SimpleTask(id="task-1", title="Test", completed_at=datetime.utcnow())
        with pytest.raises(ValueError, match="Cannot assign a completed task"):
            task.assign_to("Agent-1")

    def test_complete_success(self):
        """Test complete successfully completes task."""
        task = SimpleTask(id="task-1", title="Test", assigned_agent_id="Agent-1")
        task.complete()
        assert task.is_completed is True
        assert task.completed_at is not None

    def test_complete_raises_on_unassigned_task(self):
        """Test complete raises ValueError on unassigned task."""
        task = SimpleTask(id="task-1", title="Test")
        with pytest.raises(ValueError, match="Cannot complete an unassigned task"):
            task.complete()

    def test_complete_idempotent(self):
        """Test complete is idempotent (can be called multiple times)."""
        task = SimpleTask(id="task-1", title="Test", assigned_agent_id="Agent-1")
        task.complete()
        first_completed_at = task.completed_at
        task.complete()  # Call again
        assert task.completed_at == first_completed_at


class TestSimpleTaskRepository:
    """Tests for SimpleTaskRepository class."""

    @pytest.fixture
    def temp_db(self):
        """Create temporary database for testing."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = f.name
        yield db_path
        # Close any connections before deleting
        import time
        time.sleep(0.1)  # Brief delay to ensure connections are closed
        try:
            Path(db_path).unlink(missing_ok=True)
        except PermissionError:
            # File may still be in use, skip deletion
            pass

    def test_init_creates_database(self, temp_db):
        """Test repository initialization creates database."""
        repo = SimpleTaskRepository(db_path=temp_db)
        assert Path(temp_db).exists()

    def test_init_creates_tasks_table(self, temp_db):
        """Test repository initialization creates tasks table."""
        repo = SimpleTaskRepository(db_path=temp_db)
        with sqlite3.connect(temp_db) as conn:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='tasks'"
            )
            assert cursor.fetchone() is not None

    def test_save_new_task(self, temp_db):
        """Test save creates new task."""
        repo = SimpleTaskRepository(db_path=temp_db)
        task = SimpleTask(id="task-1", title="Test Task")
        repo.save(task)
        
        saved_task = repo.get("task-1")
        assert saved_task is not None
        assert saved_task.id == "task-1"
        assert saved_task.title == "Test Task"

    def test_save_updates_existing_task(self, temp_db):
        """Test save updates existing task."""
        repo = SimpleTaskRepository(db_path=temp_db)
        task1 = SimpleTask(id="task-1", title="Original Title")
        repo.save(task1)
        
        task2 = SimpleTask(id="task-1", title="Updated Title")
        repo.save(task2)
        
        saved_task = repo.get("task-1")
        assert saved_task.title == "Updated Title"

    def test_get_existing_task(self, temp_db):
        """Test get retrieves existing task."""
        repo = SimpleTaskRepository(db_path=temp_db)
        task = SimpleTask(id="task-1", title="Test Task", priority=3)
        repo.save(task)
        
        retrieved = repo.get("task-1")
        assert retrieved is not None
        assert retrieved.id == "task-1"
        assert retrieved.title == "Test Task"
        assert retrieved.priority == 3

    def test_get_nonexistent_task(self, temp_db):
        """Test get returns None for nonexistent task."""
        repo = SimpleTaskRepository(db_path=temp_db)
        result = repo.get("nonexistent")
        assert result is None

    def test_get_pending_returns_pending_tasks(self, temp_db):
        """Test get_pending returns only pending tasks."""
        repo = SimpleTaskRepository(db_path=temp_db)
        
        # Create pending task
        pending = SimpleTask(id="pending-1", title="Pending Task")
        repo.save(pending)
        
        # Create assigned task
        assigned = SimpleTask(id="assigned-1", title="Assigned Task", assigned_agent_id="Agent-1")
        repo.save(assigned)
        
        # Create completed task
        completed = SimpleTask(
            id="completed-1",
            title="Completed Task",
            assigned_agent_id="Agent-1",
            completed_at=datetime.utcnow()
        )
        repo.save(completed)
        
        pending_tasks = list(repo.get_pending())
        assert len(pending_tasks) == 1
        assert pending_tasks[0].id == "pending-1"

    def test_get_pending_respects_limit(self, temp_db):
        """Test get_pending respects limit parameter."""
        repo = SimpleTaskRepository(db_path=temp_db)
        
        # Create multiple pending tasks
        for i in range(5):
            task = SimpleTask(id=f"pending-{i}", title=f"Task {i}", priority=i)
            repo.save(task)
        
        pending_tasks = list(repo.get_pending(limit=3))
        assert len(pending_tasks) == 3

    def test_get_pending_orders_by_priority(self, temp_db):
        """Test get_pending orders by priority DESC."""
        repo = SimpleTaskRepository(db_path=temp_db)
        
        # Create tasks with different priorities
        task1 = SimpleTask(id="task-1", title="Low Priority", priority=1)
        task2 = SimpleTask(id="task-2", title="High Priority", priority=3)
        task3 = SimpleTask(id="task-3", title="Medium Priority", priority=2)
        
        repo.save(task1)
        repo.save(task2)
        repo.save(task3)
        
        pending_tasks = list(repo.get_pending())
        assert pending_tasks[0].priority == 3  # Highest priority first
        assert pending_tasks[1].priority == 2
        assert pending_tasks[2].priority == 1

    def test_list_all_returns_all_tasks(self, temp_db):
        """Test list_all returns all tasks."""
        repo = SimpleTaskRepository(db_path=temp_db)
        
        task1 = SimpleTask(id="task-1", title="Task 1")
        task2 = SimpleTask(id="task-2", title="Task 2")
        task3 = SimpleTask(id="task-3", title="Task 3")
        
        repo.save(task1)
        repo.save(task2)
        repo.save(task3)
        
        all_tasks = list(repo.list_all())
        assert len(all_tasks) == 3

    def test_list_all_respects_limit(self, temp_db):
        """Test list_all respects limit parameter."""
        repo = SimpleTaskRepository(db_path=temp_db)
        
        for i in range(10):
            task = SimpleTask(id=f"task-{i}", title=f"Task {i}")
            repo.save(task)
        
        all_tasks = list(repo.list_all(limit=5))
        assert len(all_tasks) == 5

    def test_list_all_orders_by_created_at_desc(self, temp_db):
        """Test list_all orders by created_at DESC."""
        repo = SimpleTaskRepository(db_path=temp_db)
        
        task1 = SimpleTask(id="task-1", title="First", created_at=datetime(2025, 1, 1))
        task2 = SimpleTask(id="task-2", title="Second", created_at=datetime(2025, 1, 2))
        task3 = SimpleTask(id="task-3", title="Third", created_at=datetime(2025, 1, 3))
        
        repo.save(task1)
        repo.save(task2)
        repo.save(task3)
        
        all_tasks = list(repo.list_all())
        # Most recent first
        assert all_tasks[0].id == "task-3"
        assert all_tasks[1].id == "task-2"
        assert all_tasks[2].id == "task-1"

    def test_save_preserves_all_fields(self, temp_db):
        """Test save preserves all task fields."""
        repo = SimpleTaskRepository(db_path=temp_db)
        created = datetime(2025, 1, 1, 12, 0, 0)
        assigned = datetime(2025, 1, 2, 12, 0, 0)
        completed = datetime(2025, 1, 3, 12, 0, 0)
        
        task = SimpleTask(
            id="task-1",
            title="Test Task",
            description="Test Description",
            assigned_agent_id="Agent-1",
            created_at=created,
            assigned_at=assigned,
            completed_at=completed,
            priority=3
        )
        repo.save(task)
        
        retrieved = repo.get("task-1")
        assert retrieved.id == "task-1"
        assert retrieved.title == "Test Task"
        assert retrieved.description == "Test Description"
        assert retrieved.assigned_agent_id == "Agent-1"
        assert retrieved.priority == 3
        assert retrieved.created_at == created
        assert retrieved.assigned_at == assigned
        assert retrieved.completed_at == completed

    def test_save_handles_none_fields(self, temp_db):
        """Test save handles None fields correctly."""
        repo = SimpleTaskRepository(db_path=temp_db)
        task = SimpleTask(id="task-1", title="Test")
        repo.save(task)
        
        retrieved = repo.get("task-1")
        assert retrieved.description is None
        assert retrieved.assigned_agent_id is None
        assert retrieved.assigned_at is None
        assert retrieved.completed_at is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

