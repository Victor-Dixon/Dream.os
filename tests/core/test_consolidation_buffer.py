#!/usr/bin/env python3
"""
Unit tests for consolidation_buffer.py - SSOT & System Integration Test Coverage

Tests ConsolidationBuffer, MergePlan, and ConsolidationStatus classes.
Target: ≥10 tests, ≥85% coverage, 100% passing.

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-11-29
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, mock_open
from pathlib import Path
import json
from datetime import datetime, timedelta
import sys
import tempfile
import shutil

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.consolidation_buffer import (
    ConsolidationBuffer,
    MergePlan,
    ConsolidationStatus,
    get_consolidation_buffer
)


class TestConsolidationStatus:
    """Test suite for ConsolidationStatus enum."""
    
    def test_status_values(self):
        """Test all status enum values exist."""
        assert ConsolidationStatus.PENDING.value == "pending"
        assert ConsolidationStatus.VALIDATED.value == "validated"
        assert ConsolidationStatus.MERGED.value == "merged"
        assert ConsolidationStatus.CONFLICT.value == "conflict"
        assert ConsolidationStatus.APPLIED.value == "applied"
        assert ConsolidationStatus.FAILED.value == "failed"


class TestMergePlan:
    """Test suite for MergePlan class."""
    
    def test_init_basic(self):
        """Test basic MergePlan initialization."""
        plan = MergePlan(
            source_repo="source",
            target_repo="target"
        )
        assert plan.source_repo == "source"
        assert plan.target_repo == "target"
        assert plan.source_branch == "main"
        assert plan.target_branch == "main"
        assert plan.status == ConsolidationStatus.PENDING
        assert plan.plan_id is not None
        assert len(plan.plan_id) == 12
    
    def test_init_with_branches(self):
        """Test MergePlan initialization with custom branches."""
        plan = MergePlan(
            source_repo="source",
            target_repo="target",
            source_branch="dev",
            target_branch="master"
        )
        assert plan.source_branch == "dev"
        assert plan.target_branch == "master"
    
    def test_init_with_description(self):
        """Test MergePlan initialization with description."""
        plan = MergePlan(
            source_repo="source",
            target_repo="target",
            description="Test merge"
        )
        assert plan.description == "Test merge"
    
    def test_generate_id_uniqueness(self):
        """Test that plan IDs are unique."""
        plan1 = MergePlan("source1", "target1")
        plan2 = MergePlan("source2", "target2")
        assert plan1.plan_id != plan2.plan_id
    
    def test_to_dict(self):
        """Test MergePlan to_dict conversion."""
        plan = MergePlan("source", "target", description="Test")
        plan.status = ConsolidationStatus.VALIDATED
        plan.diff_file = Path("/tmp/test.diff")
        plan.conflicts = ["file1.py", "file2.py"]
        plan.metadata = {"key": "value"}
        
        data = plan.to_dict()
        assert data["source_repo"] == "source"
        assert data["target_repo"] == "target"
        assert data["status"] == "validated"
        assert data["description"] == "Test"
        assert data["diff_file"] == str(plan.diff_file)
        assert data["conflicts"] == ["file1.py", "file2.py"]
        assert data["metadata"] == {"key": "value"}
    
    def test_from_dict(self):
        """Test MergePlan from_dict creation."""
        data = {
            "plan_id": "test123456",
            "source_repo": "source",
            "target_repo": "target",
            "source_branch": "dev",
            "target_branch": "master",
            "description": "Test",
            "created_at": datetime.now().isoformat(),
            "status": "validated",
            "diff_file": "/tmp/test.diff",
            "conflicts": ["file1.py"],
            "metadata": {"key": "value"}
        }
        
        plan = MergePlan.from_dict(data)
        assert plan.plan_id == "test123456"
        assert plan.source_repo == "source"
        assert plan.target_repo == "target"
        assert plan.source_branch == "dev"
        assert plan.target_branch == "master"
        assert plan.status == ConsolidationStatus.VALIDATED
        assert plan.diff_file == Path("/tmp/test.diff")
        assert plan.conflicts == ["file1.py"]


class TestConsolidationBuffer:
    """Test suite for ConsolidationBuffer class."""
    
    @pytest.fixture
    def temp_buffer_dir(self):
        """Create temporary buffer directory."""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    @pytest.fixture
    def buffer(self, temp_buffer_dir):
        """Create ConsolidationBuffer instance."""
        return ConsolidationBuffer(buffer_dir=temp_buffer_dir)
    
    def test_init_default_path(self):
        """Test ConsolidationBuffer initialization with default path."""
        with patch('src.core.consolidation_buffer.Path') as mock_path:
            mock_file = Mock()
            mock_file.resolve.return_value.parent.parent.parent = Path("/project")
            mock_path.return_value = mock_file
            
            buffer = ConsolidationBuffer()
            assert buffer.buffer_dir.exists()
    
    def test_init_custom_path(self, temp_buffer_dir):
        """Test ConsolidationBuffer initialization with custom path."""
        buffer = ConsolidationBuffer(buffer_dir=temp_buffer_dir)
        assert buffer.buffer_dir == temp_buffer_dir
        assert buffer.buffer_dir.exists()
        assert buffer.diffs_dir.exists()
        assert buffer.conflicts_dir.exists()
    
    def test_load_plans_empty(self, buffer):
        """Test loading plans from empty file."""
        plans = buffer._load_plans()
        assert plans == {}
    
    def test_load_plans_with_data(self, buffer, temp_buffer_dir):
        """Test loading plans from existing file."""
        plan_data = {
            "test123": {
                "plan_id": "test123",
                "source_repo": "source",
                "target_repo": "target",
                "source_branch": "main",
                "target_branch": "main",
                "description": None,
                "created_at": datetime.now().isoformat(),
                "status": "pending",
                "diff_file": None,
                "conflicts": [],
                "metadata": {}
            }
        }
        
        buffer.plans_file.write_text(json.dumps(plan_data), encoding='utf-8')
        plans = buffer._load_plans()
        assert len(plans) == 1
        assert "test123" in plans
    
    def test_save_plans(self, buffer):
        """Test saving plans to file."""
        plan = buffer.create_merge_plan("source", "target")
        buffer._save_plans()
        
        assert buffer.plans_file.exists()
        data = json.loads(buffer.plans_file.read_text())
        assert plan.plan_id in data
    
    def test_create_merge_plan(self, buffer):
        """Test creating a new merge plan."""
        plan = buffer.create_merge_plan("source", "target", description="Test")
        assert plan.source_repo == "source"
        assert plan.target_repo == "target"
        assert plan.description == "Test"
        assert plan.plan_id in buffer.plans
    
    def test_get_plan(self, buffer):
        """Test getting plan by ID."""
        plan = buffer.create_merge_plan("source", "target")
        retrieved = buffer.get_plan(plan.plan_id)
        assert retrieved == plan
    
    def test_get_plan_not_found(self, buffer):
        """Test getting non-existent plan."""
        result = buffer.get_plan("nonexistent")
        assert result is None
    
    def test_get_pending_plans(self, buffer):
        """Test getting pending plans."""
        plan1 = buffer.create_merge_plan("source1", "target1")
        plan2 = buffer.create_merge_plan("source2", "target2")
        buffer.mark_validated(plan2.plan_id)
        
        pending = buffer.get_pending_plans()
        assert len(pending) == 1
        assert pending[0].plan_id == plan1.plan_id
    
    def test_get_conflict_plans(self, buffer):
        """Test getting conflict plans."""
        plan = buffer.create_merge_plan("source", "target")
        buffer.mark_conflict(plan.plan_id, ["file1.py"])
        
        conflicts = buffer.get_conflict_plans()
        assert len(conflicts) == 1
        assert conflicts[0].plan_id == plan.plan_id
    
    def test_store_diff(self, buffer):
        """Test storing diff content."""
        plan = buffer.create_merge_plan("source", "target")
        diff_path = buffer.store_diff(plan.plan_id, "diff content here")
        
        assert diff_path.exists()
        assert diff_path.read_text() == "diff content here"
        assert plan.diff_file == diff_path
    
    def test_store_diff_invalid_plan(self, buffer):
        """Test storing diff for non-existent plan."""
        with pytest.raises(ValueError, match="Plan not found"):
            buffer.store_diff("nonexistent", "diff")
    
    def test_mark_validated(self, buffer):
        """Test marking plan as validated."""
        plan = buffer.create_merge_plan("source", "target")
        buffer.mark_validated(plan.plan_id)
        
        assert plan.status == ConsolidationStatus.VALIDATED
    
    def test_mark_merged(self, buffer):
        """Test marking plan as merged."""
        plan = buffer.create_merge_plan("source", "target")
        buffer.mark_merged(plan.plan_id)
        
        assert plan.status == ConsolidationStatus.MERGED
    
    def test_mark_conflict(self, buffer):
        """Test marking plan with conflicts."""
        plan = buffer.create_merge_plan("source", "target")
        conflicts = ["file1.py", "file2.py"]
        buffer.mark_conflict(plan.plan_id, conflicts)
        
        assert plan.status == ConsolidationStatus.CONFLICT
        assert plan.conflicts == conflicts
        assert (buffer.conflicts_dir / f"{plan.plan_id}-conflicts.json").exists()
    
    def test_mark_applied(self, buffer):
        """Test marking plan as applied."""
        plan = buffer.create_merge_plan("source", "target")
        buffer.mark_applied(plan.plan_id)
        
        assert plan.status == ConsolidationStatus.APPLIED
    
    def test_mark_failed(self, buffer):
        """Test marking plan as failed."""
        plan = buffer.create_merge_plan("source", "target")
        buffer.mark_failed(plan.plan_id, "Error message")
        
        assert plan.status == ConsolidationStatus.FAILED
        assert plan.metadata["error"] == "Error message"
        assert "failed_at" in plan.metadata
    
    def test_get_stats(self, buffer):
        """Test getting buffer statistics."""
        plan1 = buffer.create_merge_plan("source1", "target1")
        plan2 = buffer.create_merge_plan("source2", "target2")
        buffer.mark_validated(plan1.plan_id)
        buffer.mark_conflict(plan2.plan_id, [])
        
        stats = buffer.get_stats()
        assert stats["total"] == 2
        assert stats["pending"] == 0
        assert stats["validated"] == 1
        assert stats["conflict"] == 1
    
    def test_clear_completed(self, buffer):
        """Test clearing completed plans."""
        plan1 = buffer.create_merge_plan("source1", "target1")
        plan2 = buffer.create_merge_plan("source2", "target2")
        buffer.mark_applied(plan1.plan_id)
        
        # Mock old timestamp
        plan1.created_at = (datetime.now() - timedelta(days=10)).isoformat()
        buffer._save_plans()
        
        removed = buffer.clear_completed(older_than_days=7)
        assert removed == 1
        assert plan1.plan_id not in buffer.plans
        assert plan2.plan_id in buffer.plans


class TestGlobalFunctions:
    """Test suite for global functions."""
    
    def test_get_consolidation_buffer_singleton(self, tmp_path):
        """Test global buffer singleton."""
        with patch('src.core.consolidation_buffer._consolidation_buffer', None):
            buffer1 = get_consolidation_buffer(buffer_dir=tmp_path)
            buffer2 = get_consolidation_buffer(buffer_dir=tmp_path)
            assert buffer1 is buffer2

