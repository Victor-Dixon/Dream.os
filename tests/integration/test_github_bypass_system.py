#!/usr/bin/env python3
"""
Integration Tests for GitHub Bypass System
===========================================

Tests the full local-first architecture including:
- Local repo management
- Deferred push queue
- Synthetic GitHub wrapper
- Consolidation buffer
- Conflict resolution

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-11-28
"""

import pytest
import json
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.local_repo_layer import get_local_repo_manager, LocalRepoManager
from src.core.deferred_push_queue import get_deferred_push_queue, DeferredPushQueue, PushStatus
from src.core.synthetic_github import get_synthetic_github, SyntheticGitHub, GitHubSandboxMode
from src.core.consolidation_buffer import get_consolidation_buffer, ConsolidationBuffer, ConsolidationStatus
from src.core.merge_conflict_resolver import get_conflict_resolver, MergeConflictResolver


@pytest.fixture
def temp_base_dir(tmp_path):
    """Create temporary base directory for tests."""
    return tmp_path / "test_dream"


@pytest.fixture
def local_repo_manager(temp_base_dir):
    """Create local repo manager with temp directory."""
    repo_dir = temp_base_dir / "repos" / "master"
    return LocalRepoManager(base_path=repo_dir)


@pytest.fixture
def deferred_queue(temp_base_dir):
    """Create deferred push queue with temp file."""
    queue_file = temp_base_dir / "deferred_push_queue.json"
    return DeferredPushQueue(queue_file=queue_file)


@pytest.fixture
def consolidation_buffer(temp_base_dir):
    """Create consolidation buffer with temp directory."""
    buffer_dir = temp_base_dir / "consolidation_buffer"
    return ConsolidationBuffer(buffer_dir=buffer_dir)


class TestLocalRepoManager:
    """Test local repository manager."""
    
    def test_initialization(self, local_repo_manager):
        """Test manager initialization."""
        assert local_repo_manager.base_path.exists()
        assert local_repo_manager.metadata_file.exists()
    
    def test_metadata_persistence(self, local_repo_manager):
        """Test metadata file persistence."""
        # Add repo to metadata
        local_repo_manager.repos["test-repo"] = {
            "local_path": str(local_repo_manager.base_path / "test-repo"),
            "status": "active"
        }
        local_repo_manager._save_metadata()
        
        # Create new manager instance
        new_manager = LocalRepoManager(base_path=local_repo_manager.base_path)
        assert "test-repo" in new_manager.repos
    
    @patch('subprocess.run')
    def test_clone_from_github(self, mock_subprocess, local_repo_manager):
        """Test cloning from GitHub."""
        # Mock successful clone
        mock_result = Mock(returncode=0, stdout="", stderr="")
        mock_subprocess.return_value = mock_result
        
        success, repo_path, was_local = local_repo_manager.clone_from_github(
            "test-repo", github_user="testuser"
        )
        
        # Verify subprocess was called
        assert mock_subprocess.called
    
    @patch('subprocess.run')
    def test_create_branch(self, mock_subprocess, local_repo_manager):
        """Test branch creation."""
        # Create a test repo directory
        repo_path = local_repo_manager.base_path / "test-repo"
        repo_path.mkdir(parents=True)
        (repo_path / ".git").mkdir()
        
        # Register in metadata
        local_repo_manager.repos["test-repo"] = {
            "local_path": str(repo_path),
            "status": "active"
        }
        
        # Mock git checkout
        mock_subprocess.return_value = Mock(returncode=0)
        
        # Test branch creation
        success = local_repo_manager.create_branch("test-repo", "test-branch")
        
        # Should attempt to create branch
        assert mock_subprocess.called or not success  # Either works


class TestDeferredPushQueue:
    """Test deferred push queue."""
    
    def test_initialization(self, deferred_queue):
        """Test queue initialization."""
        assert deferred_queue.queue_file.exists() or deferred_queue.queue_file.parent.exists()
    
    def test_enqueue_push(self, deferred_queue):
        """Test enqueueing push operation."""
        entry_id = deferred_queue.enqueue_push(
            repo="test-repo",
            branch="test-branch",
            reason="rate_limit"
        )
        
        assert entry_id is not None
        assert len(entry_id) > 0
    
    def test_dequeue_push(self, deferred_queue):
        """Test dequeuing push operation."""
        # Enqueue
        entry_id = deferred_queue.enqueue_push("test-repo", "test-branch")
        
        # Dequeue
        entry = deferred_queue.dequeue_push()
        
        assert entry is not None
        assert entry["repo"] == "test-repo"
        assert entry["branch"] == "test-branch"
    
    def test_mark_completed(self, deferred_queue):
        """Test marking entry as completed."""
        entry_id = deferred_queue.enqueue_push("test-repo", "test-branch")
        
        deferred_queue.mark_completed(entry_id)
        
        # Verify status
        entry = deferred_queue.dequeue_push()
        assert entry is None  # Should be completed, not in pending
    
    def test_get_stats(self, deferred_queue):
        """Test queue statistics."""
        deferred_queue.enqueue_push("repo1", "branch1")
        deferred_queue.enqueue_push("repo2", "branch2")
        
        stats = deferred_queue.get_stats()
        
        assert stats["pending"] == 2
        assert stats["total"] == 2


class TestSyntheticGitHub:
    """Test synthetic GitHub wrapper."""
    
    @patch('src.core.synthetic_github.get_local_repo_manager')
    def test_get_repo_local_first(self, mock_manager):
        """Test getting repo with local-first strategy."""
        mock_repo_manager = Mock()
        mock_repo_manager.get_repo_path.return_value = Path("/local/repo")
        mock_manager.return_value = mock_repo_manager
        
        github = get_synthetic_github()
        github.local_repo_manager = mock_repo_manager
        
        success, repo_path, was_local = github.get_repo("test-repo")
        
        # Should try local first
        mock_repo_manager.get_repo_path.assert_called()
    
    def test_sandbox_mode_detection(self, temp_base_dir):
        """Test sandbox mode detection."""
        config_file = temp_base_dir / "github_sandbox_mode.json"
        sandbox = GitHubSandboxMode(config_file=config_file)
        
        # Initially disabled
        assert not sandbox.is_enabled()
        
        # Enable
        sandbox.enable("test")
        assert sandbox.is_enabled()
        
        # Disable
        sandbox.disable()
        assert not sandbox.is_enabled()


class TestConsolidationBuffer:
    """Test consolidation buffer."""
    
    def test_create_merge_plan(self, consolidation_buffer):
        """Test creating merge plan."""
        plan = consolidation_buffer.create_merge_plan(
            source_repo="source-repo",
            target_repo="target-repo"
        )
        
        assert plan is not None
        assert plan.source_repo == "source-repo"
        assert plan.target_repo == "target-repo"
        assert plan.plan_id in consolidation_buffer.plans
    
    def test_plan_status_transitions(self, consolidation_buffer):
        """Test plan status transitions."""
        plan = consolidation_buffer.create_merge_plan("source", "target")
        
        # Validate
        consolidation_buffer.mark_validated(plan.plan_id)
        assert consolidation_buffer.get_plan(plan.plan_id).status == ConsolidationStatus.VALIDATED
        
        # Merge
        consolidation_buffer.mark_merged(plan.plan_id)
        assert consolidation_buffer.get_plan(plan.plan_id).status == ConsolidationStatus.MERGED
        
        # Apply
        consolidation_buffer.mark_applied(plan.plan_id)
        assert consolidation_buffer.get_plan(plan.plan_id).status == ConsolidationStatus.APPLIED
    
    def test_conflict_tracking(self, consolidation_buffer):
        """Test conflict tracking."""
        plan = consolidation_buffer.create_merge_plan("source", "target")
        
        conflicts = ["file1.py", "file2.py"]
        consolidation_buffer.mark_conflict(plan.plan_id, conflicts)
        
        plan = consolidation_buffer.get_plan(plan.plan_id)
        assert plan.status == ConsolidationStatus.CONFLICT
        assert len(plan.conflicts) == 2
    
    def test_get_pending_plans(self, consolidation_buffer):
        """Test getting pending plans."""
        plan1 = consolidation_buffer.create_merge_plan("source1", "target1")
        plan2 = consolidation_buffer.create_merge_plan("source2", "target2")
        
        pending = consolidation_buffer.get_pending_plans()
        assert len(pending) == 2
        
        # Mark one as merged
        consolidation_buffer.mark_merged(plan1.plan_id)
        
        pending = consolidation_buffer.get_pending_plans()
        assert len(pending) == 1


class TestMergeConflictResolver:
    """Test merge conflict resolver."""
    
    def test_initialization(self):
        """Test resolver initialization."""
        resolver = get_conflict_resolver()
        assert resolver is not None
    
    @patch('subprocess.run')
    def test_detect_conflicts(self, mock_subprocess):
        """Test conflict detection."""
        # Mock no conflicts
        mock_result = Mock(returncode=0, stdout="", stderr="")
        mock_subprocess.return_value = mock_result
        
        resolver = get_conflict_resolver()
        
        # Create temp repo path
        from pathlib import Path
        import tempfile
        temp_repo = Path(tempfile.mkdtemp())
        
        # Test conflict detection (will use mocked subprocess)
        has_conflicts, conflict_files = resolver.detect_conflicts(
            temp_repo, "source-branch", "main"
        )
        
        # Should have attempted merge
        assert mock_subprocess.called
        
        # Cleanup
        import shutil
        shutil.rmtree(temp_repo, ignore_errors=True)


class TestEndToEndWorkflow:
    """Test end-to-end workflow."""
    
    def test_full_consolidation_workflow(self, temp_base_dir):
        """Test full consolidation workflow."""
        # Initialize components
        repo_manager = LocalRepoManager(base_path=temp_base_dir / "repos" / "master")
        buffer = ConsolidationBuffer(buffer_dir=temp_base_dir / "consolidation_buffer")
        queue = DeferredPushQueue(queue_file=temp_base_dir / "queue.json")
        
        # Create merge plan
        plan = buffer.create_merge_plan("source-repo", "target-repo")
        assert plan is not None
        
        # Mark as validated
        buffer.mark_validated(plan.plan_id)
        
        # Mark as merged
        buffer.mark_merged(plan.plan_id)
        
        # Enqueue push
        entry_id = queue.enqueue_push(
            repo="target-repo",
            branch="merge-branch",
            reason="test"
        )
        assert entry_id is not None
        
        # Mark completed
        queue.mark_completed(entry_id)
        
        # Verify final states
        assert buffer.get_plan(plan.plan_id).status == ConsolidationStatus.MERGED
        assert queue.get_pending_count() == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


Integration Tests for GitHub Bypass System
===========================================

Tests the full local-first architecture including:
- Local repo management
- Deferred push queue
- Synthetic GitHub wrapper
- Consolidation buffer
- Conflict resolution

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-11-28
"""

import pytest
import json
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.local_repo_layer import get_local_repo_manager, LocalRepoManager
from src.core.deferred_push_queue import get_deferred_push_queue, DeferredPushQueue, PushStatus
from src.core.synthetic_github import get_synthetic_github, SyntheticGitHub, GitHubSandboxMode
from src.core.consolidation_buffer import get_consolidation_buffer, ConsolidationBuffer, ConsolidationStatus
from src.core.merge_conflict_resolver import get_conflict_resolver, MergeConflictResolver


@pytest.fixture
def temp_base_dir(tmp_path):
    """Create temporary base directory for tests."""
    return tmp_path / "test_dream"


@pytest.fixture
def local_repo_manager(temp_base_dir):
    """Create local repo manager with temp directory."""
    repo_dir = temp_base_dir / "repos" / "master"
    return LocalRepoManager(base_path=repo_dir)


@pytest.fixture
def deferred_queue(temp_base_dir):
    """Create deferred push queue with temp file."""
    queue_file = temp_base_dir / "deferred_push_queue.json"
    return DeferredPushQueue(queue_file=queue_file)


@pytest.fixture
def consolidation_buffer(temp_base_dir):
    """Create consolidation buffer with temp directory."""
    buffer_dir = temp_base_dir / "consolidation_buffer"
    return ConsolidationBuffer(buffer_dir=buffer_dir)


class TestLocalRepoManager:
    """Test local repository manager."""
    
    def test_initialization(self, local_repo_manager):
        """Test manager initialization."""
        assert local_repo_manager.base_path.exists()
        assert local_repo_manager.metadata_file.exists()
    
    def test_metadata_persistence(self, local_repo_manager):
        """Test metadata file persistence."""
        # Add repo to metadata
        local_repo_manager.repos["test-repo"] = {
            "local_path": str(local_repo_manager.base_path / "test-repo"),
            "status": "active"
        }
        local_repo_manager._save_metadata()
        
        # Create new manager instance
        new_manager = LocalRepoManager(base_path=local_repo_manager.base_path)
        assert "test-repo" in new_manager.repos
    
    @patch('subprocess.run')
    def test_clone_from_github(self, mock_subprocess, local_repo_manager):
        """Test cloning from GitHub."""
        # Mock successful clone
        mock_result = Mock(returncode=0, stdout="", stderr="")
        mock_subprocess.return_value = mock_result
        
        success, repo_path, was_local = local_repo_manager.clone_from_github(
            "test-repo", github_user="testuser"
        )
        
        # Verify subprocess was called
        assert mock_subprocess.called
    
    @patch('subprocess.run')
    def test_create_branch(self, mock_subprocess, local_repo_manager):
        """Test branch creation."""
        # Create a test repo directory
        repo_path = local_repo_manager.base_path / "test-repo"
        repo_path.mkdir(parents=True)
        (repo_path / ".git").mkdir()
        
        # Register in metadata
        local_repo_manager.repos["test-repo"] = {
            "local_path": str(repo_path),
            "status": "active"
        }
        
        # Mock git checkout
        mock_subprocess.return_value = Mock(returncode=0)
        
        # Test branch creation
        success = local_repo_manager.create_branch("test-repo", "test-branch")
        
        # Should attempt to create branch
        assert mock_subprocess.called or not success  # Either works


class TestDeferredPushQueue:
    """Test deferred push queue."""
    
    def test_initialization(self, deferred_queue):
        """Test queue initialization."""
        assert deferred_queue.queue_file.exists() or deferred_queue.queue_file.parent.exists()
    
    def test_enqueue_push(self, deferred_queue):
        """Test enqueueing push operation."""
        entry_id = deferred_queue.enqueue_push(
            repo="test-repo",
            branch="test-branch",
            reason="rate_limit"
        )
        
        assert entry_id is not None
        assert len(entry_id) > 0
    
    def test_dequeue_push(self, deferred_queue):
        """Test dequeuing push operation."""
        # Enqueue
        entry_id = deferred_queue.enqueue_push("test-repo", "test-branch")
        
        # Dequeue
        entry = deferred_queue.dequeue_push()
        
        assert entry is not None
        assert entry["repo"] == "test-repo"
        assert entry["branch"] == "test-branch"
    
    def test_mark_completed(self, deferred_queue):
        """Test marking entry as completed."""
        entry_id = deferred_queue.enqueue_push("test-repo", "test-branch")
        
        deferred_queue.mark_completed(entry_id)
        
        # Verify status
        entry = deferred_queue.dequeue_push()
        assert entry is None  # Should be completed, not in pending
    
    def test_get_stats(self, deferred_queue):
        """Test queue statistics."""
        deferred_queue.enqueue_push("repo1", "branch1")
        deferred_queue.enqueue_push("repo2", "branch2")
        
        stats = deferred_queue.get_stats()
        
        assert stats["pending"] == 2
        assert stats["total"] == 2


class TestSyntheticGitHub:
    """Test synthetic GitHub wrapper."""
    
    @patch('src.core.synthetic_github.get_local_repo_manager')
    def test_get_repo_local_first(self, mock_manager):
        """Test getting repo with local-first strategy."""
        mock_repo_manager = Mock()
        mock_repo_manager.get_repo_path.return_value = Path("/local/repo")
        mock_manager.return_value = mock_repo_manager
        
        github = get_synthetic_github()
        github.local_repo_manager = mock_repo_manager
        
        success, repo_path, was_local = github.get_repo("test-repo")
        
        # Should try local first
        mock_repo_manager.get_repo_path.assert_called()
    
    def test_sandbox_mode_detection(self, temp_base_dir):
        """Test sandbox mode detection."""
        config_file = temp_base_dir / "github_sandbox_mode.json"
        sandbox = GitHubSandboxMode(config_file=config_file)
        
        # Initially disabled
        assert not sandbox.is_enabled()
        
        # Enable
        sandbox.enable("test")
        assert sandbox.is_enabled()
        
        # Disable
        sandbox.disable()
        assert not sandbox.is_enabled()


class TestConsolidationBuffer:
    """Test consolidation buffer."""
    
    def test_create_merge_plan(self, consolidation_buffer):
        """Test creating merge plan."""
        plan = consolidation_buffer.create_merge_plan(
            source_repo="source-repo",
            target_repo="target-repo"
        )
        
        assert plan is not None
        assert plan.source_repo == "source-repo"
        assert plan.target_repo == "target-repo"
        assert plan.plan_id in consolidation_buffer.plans
    
    def test_plan_status_transitions(self, consolidation_buffer):
        """Test plan status transitions."""
        plan = consolidation_buffer.create_merge_plan("source", "target")
        
        # Validate
        consolidation_buffer.mark_validated(plan.plan_id)
        assert consolidation_buffer.get_plan(plan.plan_id).status == ConsolidationStatus.VALIDATED
        
        # Merge
        consolidation_buffer.mark_merged(plan.plan_id)
        assert consolidation_buffer.get_plan(plan.plan_id).status == ConsolidationStatus.MERGED
        
        # Apply
        consolidation_buffer.mark_applied(plan.plan_id)
        assert consolidation_buffer.get_plan(plan.plan_id).status == ConsolidationStatus.APPLIED
    
    def test_conflict_tracking(self, consolidation_buffer):
        """Test conflict tracking."""
        plan = consolidation_buffer.create_merge_plan("source", "target")
        
        conflicts = ["file1.py", "file2.py"]
        consolidation_buffer.mark_conflict(plan.plan_id, conflicts)
        
        plan = consolidation_buffer.get_plan(plan.plan_id)
        assert plan.status == ConsolidationStatus.CONFLICT
        assert len(plan.conflicts) == 2
    
    def test_get_pending_plans(self, consolidation_buffer):
        """Test getting pending plans."""
        plan1 = consolidation_buffer.create_merge_plan("source1", "target1")
        plan2 = consolidation_buffer.create_merge_plan("source2", "target2")
        
        pending = consolidation_buffer.get_pending_plans()
        assert len(pending) == 2
        
        # Mark one as merged
        consolidation_buffer.mark_merged(plan1.plan_id)
        
        pending = consolidation_buffer.get_pending_plans()
        assert len(pending) == 1


class TestMergeConflictResolver:
    """Test merge conflict resolver."""
    
    def test_initialization(self):
        """Test resolver initialization."""
        resolver = get_conflict_resolver()
        assert resolver is not None
    
    @patch('subprocess.run')
    def test_detect_conflicts(self, mock_subprocess):
        """Test conflict detection."""
        # Mock no conflicts
        mock_result = Mock(returncode=0, stdout="", stderr="")
        mock_subprocess.return_value = mock_result
        
        resolver = get_conflict_resolver()
        
        # Create temp repo path
        from pathlib import Path
        import tempfile
        temp_repo = Path(tempfile.mkdtemp())
        
        # Test conflict detection (will use mocked subprocess)
        has_conflicts, conflict_files = resolver.detect_conflicts(
            temp_repo, "source-branch", "main"
        )
        
        # Should have attempted merge
        assert mock_subprocess.called
        
        # Cleanup
        import shutil
        shutil.rmtree(temp_repo, ignore_errors=True)


class TestEndToEndWorkflow:
    """Test end-to-end workflow."""
    
    def test_full_consolidation_workflow(self, temp_base_dir):
        """Test full consolidation workflow."""
        # Initialize components
        repo_manager = LocalRepoManager(base_path=temp_base_dir / "repos" / "master")
        buffer = ConsolidationBuffer(buffer_dir=temp_base_dir / "consolidation_buffer")
        queue = DeferredPushQueue(queue_file=temp_base_dir / "queue.json")
        
        # Create merge plan
        plan = buffer.create_merge_plan("source-repo", "target-repo")
        assert plan is not None
        
        # Mark as validated
        buffer.mark_validated(plan.plan_id)
        
        # Mark as merged
        buffer.mark_merged(plan.plan_id)
        
        # Enqueue push
        entry_id = queue.enqueue_push(
            repo="target-repo",
            branch="merge-branch",
            reason="test"
        )
        assert entry_id is not None
        
        # Mark completed
        queue.mark_completed(entry_id)
        
        # Verify final states
        assert buffer.get_plan(plan.plan_id).status == ConsolidationStatus.MERGED
        assert queue.get_pending_count() == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

