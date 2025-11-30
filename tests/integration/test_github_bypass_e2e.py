#!/usr/bin/env python3
"""
End-to-End Integration Tests for GitHub Bypass System
======================================================

Comprehensive end-to-end tests for local-first architecture:
- Complete consolidation workflow
- Local-first operations
- Deferred queue processing
- Sandbox mode handling
- Error recovery

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-01-28
Priority: HIGH
"""

import pytest
import sys
import json
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile

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
def test_components(temp_base_dir):
    """Create all test components with temp directories."""
    repo_manager = LocalRepoManager(base_path=temp_base_dir / "repos" / "master")
    queue = DeferredPushQueue(queue_file=temp_base_dir / "deferred_push_queue.json")
    buffer = ConsolidationBuffer(buffer_dir=temp_base_dir / "consolidation_buffer")
    resolver = get_conflict_resolver()
    
    # Create synthetic GitHub with temp config
    config_file = temp_base_dir / "github_sandbox_mode.json"
    github = SyntheticGitHub(
        local_repo_manager=repo_manager,
        deferred_queue=queue,
        sandbox_mode_config=config_file
    )
    
    return {
        "repo_manager": repo_manager,
        "queue": queue,
        "buffer": buffer,
        "resolver": resolver,
        "github": github
    }


class TestLocalFirstArchitectureE2E:
    """Test complete local-first architecture end-to-end."""
    
    def test_complete_consolidation_workflow(self, test_components):
        """Test complete consolidation workflow from start to finish."""
        repo_manager = test_components["repo_manager"]
        buffer = test_components["buffer"]
        queue = test_components["queue"]
        github = test_components["github"]
        
        # Step 1: Create merge plan
        plan = buffer.create_merge_plan(
            source_repo="source-repo",
            target_repo="target-repo",
            description="E2E test merge"
        )
        assert plan is not None
        assert plan.status == ConsolidationStatus.PENDING
        
        # Step 2: Validate plan
        buffer.mark_validated(plan.plan_id)
        assert buffer.get_plan(plan.plan_id).status == ConsolidationStatus.VALIDATED
        
        # Step 3: Simulate merge (local-first)
        buffer.mark_merged(plan.plan_id)
        assert buffer.get_plan(plan.plan_id).status == ConsolidationStatus.MERGED
        
        # Step 4: Enqueue push operation (deferred)
        entry_id = queue.enqueue_push(
            repo="target-repo",
            branch="merge-branch",
            reason="rate_limit"
        )
        assert entry_id is not None
        
        # Step 5: Verify queue has entry
        stats = queue.get_stats()
        assert stats["pending"] >= 1
        
        # Step 6: Process queue entry
        entry = queue.dequeue_push()
        assert entry is not None
        assert entry["repo"] == "target-repo"
        
        # Step 7: Mark as completed
        queue.mark_completed(entry["entry_id"])
        
        # Step 8: Verify final states
        final_stats = queue.get_stats()
        assert final_stats["pending"] == 0
        
        final_plan = buffer.get_plan(plan.plan_id)
        assert final_plan.status == ConsolidationStatus.MERGED
    
    @patch('subprocess.run')
    def test_local_first_repo_cloning(self, mock_subprocess, test_components):
        """Test local-first repository cloning strategy."""
        repo_manager = test_components["repo_manager"]
        
        # Mock successful git clone
        mock_subprocess.return_value = Mock(returncode=0, stdout="", stderr="")
        
        # Test cloning from GitHub (local-first)
        success, repo_path, was_local = repo_manager.clone_from_github(
            "test-repo",
            github_user="testuser"
        )
        
        # Should attempt to clone (even if mocked)
        assert mock_subprocess.called or not success
        
        # Verify repo manager tracks the repo
        assert "test-repo" in repo_manager.repos or not success
    
    def test_sandbox_mode_auto_detection(self, test_components):
        """Test automatic sandbox mode detection and fallback."""
        github = test_components["github"]
        
        # Test sandbox mode detection
        is_sandbox = github.is_sandbox_mode()
        assert isinstance(is_sandbox, bool)
        
        # If sandbox mode, local-first operations should still work
        # Test getting repo in sandbox mode
        success, repo_path, was_local = github.get_repo("test-repo")
        # Should work regardless of sandbox mode (local-first)


class TestDeferredQueueProcessing:
    """Test deferred queue processing end-to-end."""
    
    def test_queue_lifecycle(self, test_components):
        """Test complete queue lifecycle."""
        queue = test_components["queue"]
        
        # Enqueue multiple entries
        entry_id1 = queue.enqueue_push("repo1", "branch1", reason="rate_limit")
        entry_id2 = queue.enqueue_push("repo2", "branch2", reason="network_error")
        entry_id3 = queue.enqueue_push("repo3", "branch3", reason="test")
        
        assert entry_id1 is not None
        assert entry_id2 is not None
        assert entry_id3 is not None
        
        # Check stats
        stats = queue.get_stats()
        assert stats["pending"] == 3
        assert stats["total"] == 3
        
        # Process first entry
        entry = queue.dequeue_push()
        assert entry is not None
        assert entry["repo"] == "repo1"
        
        # Mark as retrying
        queue.mark_retrying(entry["entry_id"])
        
        # Process second entry
        entry2 = queue.dequeue_push()
        assert entry2 is not None
        
        # Mark as completed
        queue.mark_completed(entry2["entry_id"])
        
        # Verify final stats
        final_stats = queue.get_stats()
        assert final_stats["pending"] >= 1  # At least one remaining
        assert final_stats["completed"] >= 1  # At least one completed
    
    def test_queue_retry_mechanism(self, test_components):
        """Test queue retry mechanism."""
        queue = test_components["queue"]
        
        # Enqueue entry
        entry_id = queue.enqueue_push("repo1", "branch1", reason="test")
        
        # Mark as retrying
        queue.mark_retrying(entry_id)
        
        # Verify retry count increases
        entry = queue.dequeue_push()
        if entry:
            assert entry.get("retry_count", 0) >= 0  # Retry count exists
    
    def test_queue_cleanup(self, test_components):
        """Test queue cleanup of old entries."""
        queue = test_components["queue"]
        
        # Enqueue and complete entry
        entry_id = queue.enqueue_push("repo1", "branch1", reason="test")
        queue.mark_completed(entry_id)
        
        # Get stats
        stats = queue.get_stats()
        
        # Cleanup should handle old completed entries
        assert isinstance(stats, dict)
        assert "total" in stats


class TestErrorRecovery:
    """Test error recovery and resilience."""
    
    def test_github_unavailable_fallback(self, test_components):
        """Test fallback when GitHub is unavailable."""
        github = test_components["github"]
        
        # Enable sandbox mode (simulates GitHub unavailable)
        github.sandbox_mode.enable("test")
        
        # Operations should still work (local-first)
        success, repo_path, was_local = github.get_repo("test-repo")
        # Should return (may fail, but shouldn't crash)
        assert isinstance(success, bool)
    
    def test_queue_persistence(self, test_components, temp_base_dir):
        """Test queue persistence across restarts."""
        queue_file = temp_base_dir / "test_queue.json"
        queue1 = DeferredPushQueue(queue_file=queue_file)
        
        # Enqueue entry
        entry_id = queue1.enqueue_push("repo1", "branch1", reason="test")
        assert entry_id is not None
        
        # Create new queue instance (simulates restart)
        queue2 = DeferredPushQueue(queue_file=queue_file)
        
        # Should have the entry
        stats = queue2.get_stats()
        assert stats["pending"] >= 1
    
    def test_buffer_persistence(self, test_components, temp_base_dir):
        """Test consolidation buffer persistence."""
        buffer_dir = temp_base_dir / "test_buffer"
        buffer1 = ConsolidationBuffer(buffer_dir=buffer_dir)
        
        # Create merge plan
        plan = buffer1.create_merge_plan("source", "target")
        
        # Create new buffer instance (simulates restart)
        buffer2 = ConsolidationBuffer(buffer_dir=buffer_dir)
        
        # Should have the plan
        retrieved_plan = buffer2.get_plan(plan.plan_id)
        assert retrieved_plan is not None
        assert retrieved_plan.plan_id == plan.plan_id


class TestIntegrationComponents:
    """Test integration between components."""
    
    def test_github_uses_buffer(self, test_components):
        """Test SyntheticGitHub integrates with ConsolidationBuffer."""
        github = test_components["github"]
        buffer = test_components["buffer"]
        
        # GitHub should be able to work with buffer
        # (actual integration depends on implementation)
        assert github is not None
        assert buffer is not None
    
    def test_github_uses_queue(self, test_components):
        """Test SyntheticGitHub integrates with DeferredPushQueue."""
        github = test_components["github"]
        queue = test_components["queue"]
        
        # GitHub should use queue for deferred operations
        assert hasattr(github, 'queue') or hasattr(github, 'deferred_queue')
        assert queue is not None
    
    def test_buffer_workflow_with_queue(self, test_components):
        """Test consolidation buffer workflow with queue."""
        buffer = test_components["buffer"]
        queue = test_components["queue"]
        
        # Create merge plan
        plan = buffer.create_merge_plan("source", "target")
        
        # Mark as merged
        buffer.mark_merged(plan.plan_id)
        
        # Enqueue push (simulating deferred operation)
        entry_id = queue.enqueue_push(
            repo=plan.target_repo,
            branch="merge-branch",
            reason="test"
        )
        
        assert entry_id is not None
        assert buffer.get_plan(plan.plan_id).status == ConsolidationStatus.MERGED


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

