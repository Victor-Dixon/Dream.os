"""
Unit tests for core_resource_manager.py - MEDIUM PRIORITY

Tests CoreResourceManager class and resource operations.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.managers.contracts import ManagerContext, ManagerResult
from src.core.managers.core_resource_manager import CoreResourceManager


class TestCoreResourceManager:
    """Test suite for CoreResourceManager class."""

    @pytest.fixture
    def mock_context(self):
        """Create mock manager context."""
        return ManagerContext(
            config={"test": "config"},
            logger=lambda msg: None,
            metrics={},
            timestamp=datetime.now()
        )

    @pytest.fixture
    def manager(self):
        """Create CoreResourceManager instance with mocked operations."""
        with patch('src.core.managers.core_resource_manager.FileOperations') as mock_file_class, \
             patch('src.core.managers.core_resource_manager.LockOperations') as mock_lock_class, \
             patch('src.core.managers.core_resource_manager.ContextOperations') as mock_context_class, \
             patch('src.core.managers.core_resource_manager.ResourceCRUDOperations') as mock_crud_class:
            
            mock_file = MagicMock()
            mock_file.operations_count = 0
            mock_file.handle_operation = MagicMock(return_value=ManagerResult(success=True, data={}, metrics={}))
            mock_file_class.return_value = mock_file
            
            mock_lock = MagicMock()
            mock_lock.operations_count = 0
            mock_lock.load_locks = MagicMock()
            mock_lock.save_locks = MagicMock()
            mock_lock.clear_locks = MagicMock()
            mock_lock.get_lock_count = MagicMock(return_value=0)
            mock_lock.handle_operation = MagicMock(return_value=ManagerResult(success=True, data={}, metrics={}))
            mock_lock_class.return_value = mock_lock
            
            mock_context = MagicMock()
            mock_context.operations_count = 0
            mock_context.clear_contexts = MagicMock()
            mock_context.get_context_count = MagicMock(return_value=0)
            mock_context.get_context_ids = MagicMock(return_value=[])
            mock_context.handle_operation = MagicMock(return_value=ManagerResult(success=True, data={}, metrics={}))
            mock_context_class.return_value = mock_context
            
            mock_crud = MagicMock()
            mock_crud.create_resource = MagicMock(return_value=ManagerResult(success=True, data={}, metrics={}))
            mock_crud.get_resource = MagicMock(return_value=ManagerResult(success=True, data={}, metrics={}))
            mock_crud.update_resource = MagicMock(return_value=ManagerResult(success=True, data={}, metrics={}))
            mock_crud.delete_resource = MagicMock(return_value=ManagerResult(success=True, data={}, metrics={}))
            mock_crud_class.return_value = mock_crud
            
            manager = CoreResourceManager()
            manager.file_ops = mock_file
            manager.lock_ops = mock_lock
            manager.context_ops = mock_context
            manager.crud_ops = mock_crud
            return manager

    def test_manager_initialization(self, manager):
        """Test manager initialization."""
        assert manager is not None
        assert hasattr(manager, 'file_ops')
        assert hasattr(manager, 'lock_ops')
        assert hasattr(manager, 'context_ops')
        assert hasattr(manager, 'crud_ops')

    def test_initialize(self, manager, mock_context):
        """Test manager initialization with context."""
        result = manager.initialize(mock_context)
        assert result is True
        manager.lock_ops.load_locks.assert_called_once()

    def test_execute_create_resource(self, manager, mock_context):
        """Test execute create_resource operation."""
        expected_result = ManagerResult(
            success=True,
            data={"resource_id": "resource-123"},
            metrics={}
        )
        manager.crud_ops.create_resource.return_value = expected_result
        
        result = manager.execute(mock_context, "create_resource", {
            "resource_type": "file",
            "resource_id": "resource-123"
        })
        assert result.success is True
        manager.crud_ops.create_resource.assert_called_once()

    def test_execute_get_resource(self, manager, mock_context):
        """Test execute get_resource operation."""
        expected_result = ManagerResult(
            success=True,
            data={"resource_id": "resource-123", "data": {}},
            metrics={}
        )
        manager.crud_ops.get_resource.return_value = expected_result
        
        result = manager.execute(mock_context, "get_resource", {"resource_id": "resource-123"})
        assert result.success is True
        manager.crud_ops.get_resource.assert_called_once()

    def test_execute_update_resource(self, manager, mock_context):
        """Test execute update_resource operation."""
        expected_result = ManagerResult(
            success=True,
            data={"resource_id": "resource-123", "updated": True},
            metrics={}
        )
        manager.crud_ops.update_resource.return_value = expected_result
        
        result = manager.execute(mock_context, "update_resource", {
            "resource_id": "resource-123",
            "updates": {"key": "value"}
        })
        assert result.success is True
        manager.crud_ops.update_resource.assert_called_once()

    def test_execute_delete_resource(self, manager, mock_context):
        """Test execute delete_resource operation."""
        expected_result = ManagerResult(
            success=True,
            data={"resource_id": "resource-123", "deleted": True},
            metrics={}
        )
        manager.crud_ops.delete_resource.return_value = expected_result
        
        result = manager.execute(mock_context, "delete_resource", {"resource_id": "resource-123"})
        assert result.success is True
        manager.crud_ops.delete_resource.assert_called_once()

    def test_execute_file_operation(self, manager, mock_context):
        """Test execute file_operation."""
        expected_result = ManagerResult(
            success=True,
            data={"operation": "read", "file": "test.txt"},
            metrics={}
        )
        manager.file_ops.handle_operation.return_value = expected_result
        
        result = manager.execute(mock_context, "file_operation", {"operation": "read"})
        assert result.success is True
        manager.file_ops.handle_operation.assert_called_once()

    def test_execute_lock_operation(self, manager, mock_context):
        """Test execute lock_operation."""
        expected_result = ManagerResult(
            success=True,
            data={"lock_id": "lock-123", "locked": True},
            metrics={}
        )
        manager.lock_ops.handle_operation.return_value = expected_result
        
        result = manager.execute(mock_context, "lock_operation", {"operation": "acquire"})
        assert result.success is True
        manager.lock_ops.handle_operation.assert_called_once()

    def test_execute_context_operation(self, manager, mock_context):
        """Test execute context_operation."""
        expected_result = ManagerResult(
            success=True,
            data={"context_id": "ctx-123"},
            metrics={}
        )
        manager.context_ops.handle_operation.return_value = expected_result
        
        result = manager.execute(mock_context, "context_operation", {"operation": "create"})
        assert result.success is True
        manager.context_ops.handle_operation.assert_called_once()

    def test_execute_unknown_operation(self, manager, mock_context):
        """Test execute with unknown operation."""
        result = manager.execute(mock_context, "unknown_operation", {})
        assert result.success is False
        assert "Unknown operation" in result.error

    def test_create_resource(self, manager, mock_context):
        """Test create_resource public method."""
        expected_result = ManagerResult(
            success=True,
            data={"resource_id": "resource-456"},
            metrics={}
        )
        manager.crud_ops.create_resource.return_value = expected_result
        
        result = manager.create_resource(mock_context, "file", {"path": "/tmp/test.txt"})
        assert result.success is True
        manager.crud_ops.create_resource.assert_called_once()

    def test_get_resource(self, manager, mock_context):
        """Test get_resource public method."""
        expected_result = ManagerResult(
            success=True,
            data={"resource_id": "resource-789", "data": {}},
            metrics={}
        )
        manager.crud_ops.get_resource.return_value = expected_result
        
        result = manager.get_resource(mock_context, "resource-789")
        assert result.success is True
        manager.crud_ops.get_resource.assert_called_once()

    def test_update_resource(self, manager, mock_context):
        """Test update_resource public method."""
        expected_result = ManagerResult(
            success=True,
            data={"resource_id": "resource-123", "updated": True},
            metrics={}
        )
        manager.crud_ops.update_resource.return_value = expected_result
        
        result = manager.update_resource(mock_context, "resource-123", {"key": "new_value"})
        assert result.success is True
        manager.crud_ops.update_resource.assert_called_once()

    def test_delete_resource(self, manager, mock_context):
        """Test delete_resource public method."""
        expected_result = ManagerResult(
            success=True,
            data={"resource_id": "resource-123", "deleted": True},
            metrics={}
        )
        manager.crud_ops.delete_resource.return_value = expected_result
        
        result = manager.delete_resource(mock_context, "resource-123")
        assert result.success is True
        manager.crud_ops.delete_resource.assert_called_once()

    def test_cleanup(self, manager, mock_context):
        """Test cleanup operation."""
        result = manager.cleanup(mock_context)
        assert result is True
        manager.lock_ops.save_locks.assert_called_once()
        manager.context_ops.clear_contexts.assert_called_once()
        manager.lock_ops.clear_locks.assert_called_once()

    def test_get_status(self, manager):
        """Test get_status operation."""
        manager.file_ops.operations_count = 10
        manager.lock_ops.operations_count = 5
        manager.context_ops.operations_count = 3
        manager.lock_ops.get_lock_count.return_value = 2
        manager.context_ops.get_context_count.return_value = 1
        manager.context_ops.get_context_ids.return_value = ["ctx-1"]
        
        status = manager.get_status()
        assert status["file_operations"] == 10
        assert status["lock_operations"] == 5
        assert status["context_operations"] == 3
        assert status["active_locks"] == 2
        assert status["agent_contexts"] == 1
        assert len(status["context_ids"]) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])



