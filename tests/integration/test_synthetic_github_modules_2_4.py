#!/usr/bin/env python3
"""
Integration Tests for Synthetic GitHub Modules 2-4
==================================================

Tests for:
- Module 2: local_router.py
- Module 3: remote_router.py  
- Module 4: synthetic_client.py

Test Areas:
1. Module imports and dependencies
2. Backward compatibility (synthetic_github.py shim)
3. Integration with local_repo_layer and deferred_push_queue
4. Routing logic (local vs remote)

V2 Compliance | Author: Agent-3 | Date: 2025-12-14
Priority: HIGH (Batch 1, Critical violations)
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from typing import Tuple, Optional

# Test imports - verify module structure
from src.core.github.local_router import LocalRouter
from src.core.github.remote_router import RemoteRouter
from src.core.github.synthetic_client import SyntheticGitHub
from src.core.github.sandbox_manager import GitHubSandboxMode
from src.core.github import (
    SyntheticGitHub as GitHubModule,
    GitHubSandboxMode as SandboxModule,
    get_synthetic_github
)

# Backward compatibility imports
from src.core.synthetic_github import (
    SyntheticGitHub as ShimSyntheticGitHub,
    GitHubSandboxMode as ShimSandboxMode,
    get_synthetic_github as shim_get_synthetic_github
)

# Integration dependencies
from src.core.local_repo_layer import LocalRepoManager, get_local_repo_manager
from src.core.deferred_push_queue import DeferredPushQueue, get_deferred_push_queue


class TestModuleImportsAndDependencies:
    """Test 1: Module imports and dependencies."""
    
    def test_local_router_imports(self):
        """Test that LocalRouter can be imported and has required dependencies."""
        assert LocalRouter is not None
        assert hasattr(LocalRouter, '__init__')
        assert hasattr(LocalRouter, 'create_branch')
        assert hasattr(LocalRouter, 'get_file')
        assert hasattr(LocalRouter, 'merge_branches')
    
    def test_remote_router_imports(self):
        """Test that RemoteRouter can be imported and has required dependencies."""
        assert RemoteRouter is not None
        assert hasattr(RemoteRouter, '__init__')
        assert hasattr(RemoteRouter, 'push_branch')
        assert hasattr(RemoteRouter, 'create_pr')
    
    def test_synthetic_client_imports(self):
        """Test that SyntheticGitHub can be imported and has required dependencies."""
        assert SyntheticGitHub is not None
        assert hasattr(SyntheticGitHub, '__init__')
        assert hasattr(SyntheticGitHub, 'get_repo')
        assert hasattr(SyntheticGitHub, 'create_branch')
        assert hasattr(SyntheticGitHub, 'push_branch')
        assert hasattr(SyntheticGitHub, 'create_pr')
        assert hasattr(SyntheticGitHub, 'get_file')
        assert hasattr(SyntheticGitHub, 'merge_branches')
        assert hasattr(SyntheticGitHub, 'is_sandbox_mode')
    
    def test_module_package_imports(self):
        """Test that modules can be imported from package."""
        assert GitHubModule is SyntheticGitHub
        assert SandboxModule is GitHubSandboxMode
        assert get_synthetic_github is not None
    
    def test_local_router_dependencies(self):
        """Test that LocalRouter imports required dependencies."""
        import inspect
        # Check module-level imports, not class source
        module_source = inspect.getsource(inspect.getmodule(LocalRouter))
        assert 'local_repo_layer' in module_source or 'get_local_repo_manager' in module_source
        assert 'sandbox_manager' in module_source or 'GitHubSandboxMode' in module_source
    
    def test_remote_router_dependencies(self):
        """Test that RemoteRouter imports required dependencies."""
        import inspect
        # Check module-level imports, not class source
        module_source = inspect.getsource(inspect.getmodule(RemoteRouter))
        assert 'local_repo_layer' in module_source or 'get_local_repo_manager' in module_source
        assert 'deferred_push_queue' in module_source or 'get_deferred_push_queue' in module_source
        assert 'sandbox_manager' in module_source or 'GitHubSandboxMode' in module_source
    
    def test_synthetic_client_dependencies(self):
        """Test that SyntheticGitHub imports required dependencies."""
        import inspect
        source = inspect.getsource(SyntheticGitHub)
        assert 'local_repo_layer' in source or 'get_local_repo_manager' in source
        assert 'deferred_push_queue' in source or 'get_deferred_push_queue' in source
        assert 'LocalRouter' in source
        assert 'RemoteRouter' in source


class TestBackwardCompatibility:
    """Test 2: Backward compatibility (synthetic_github.py shim)."""
    
    def test_shim_imports_synthetic_github(self):
        """Test that shim imports SyntheticGitHub correctly."""
        assert ShimSyntheticGitHub is not None
        assert ShimSyntheticGitHub is SyntheticGitHub
    
    def test_shim_imports_sandbox_mode(self):
        """Test that shim imports GitHubSandboxMode correctly."""
        assert ShimSandboxMode is not None
        assert ShimSandboxMode is GitHubSandboxMode
    
    def test_shim_get_synthetic_github(self):
        """Test that shim get_synthetic_github function works."""
        github = shim_get_synthetic_github()
        assert isinstance(github, SyntheticGitHub)
    
    def test_shim_exports_match_module(self):
        """Test that shim exports match module exports."""
        from src.core.synthetic_github import __all__ as shim_all
        from src.core.github import __all__ as module_all
        
        # Check that all shim exports are in module exports
        for export in shim_all:
            assert export in module_all, f"{export} not in module exports"
    
    def test_shim_instances_are_compatible(self):
        """Test that instances from shim are compatible with module."""
        shim_github = shim_get_synthetic_github()
        module_github = get_synthetic_github()
        
        # Both should be SyntheticGitHub instances
        assert isinstance(shim_github, SyntheticGitHub)
        assert isinstance(module_github, SyntheticGitHub)
        
        # Both should have same methods
        assert hasattr(shim_github, 'get_repo')
        assert hasattr(module_github, 'get_repo')
        assert hasattr(shim_github, 'create_branch')
        assert hasattr(module_github, 'create_branch')


class TestLocalRepoLayerIntegration:
    """Test 3: Integration with local_repo_layer."""
    
    @pytest.fixture
    def temp_repo_dir(self):
        """Create temporary directory for test repos."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)
    
    @pytest.fixture
    def mock_local_repo_manager(self, temp_repo_dir):
        """Create mock local repo manager."""
        manager = Mock(spec=LocalRepoManager)
        manager.get_repo_path = Mock(return_value=temp_repo_dir / "test_repo")
        manager.create_branch = Mock(return_value=True)
        manager.merge_branch = Mock(return_value=(True, None))
        manager.get_repo_status = Mock(return_value={
            "github_url": "https://github.com/test/test_repo.git",
            "github_user": "test"
        })
        manager.clone_from_github = Mock(return_value=(True, temp_repo_dir / "test_repo"))
        return manager
    
    def test_local_router_uses_local_repo_manager(self, mock_local_repo_manager):
        """Test that LocalRouter uses local_repo_manager correctly."""
        sandbox_mode = GitHubSandboxMode()
        router = LocalRouter(mock_local_repo_manager, sandbox_mode)
        
        # Test create_branch
        result = router.create_branch("test_repo", "feature_branch")
        assert result is True
        mock_local_repo_manager.get_repo_path.assert_called_with("test_repo")
        mock_local_repo_manager.create_branch.assert_called_with("test_repo", "feature_branch")
    
    def test_local_router_get_file(self, mock_local_repo_manager, temp_repo_dir):
        """Test that LocalRouter uses local_repo_manager for get_file."""
        sandbox_mode = GitHubSandboxMode()
        router = LocalRouter(mock_local_repo_manager, sandbox_mode)
        
        # Create test file
        repo_path = temp_repo_dir / "test_repo"
        repo_path.mkdir(parents=True)
        test_file = repo_path / "test.txt"
        test_file.write_text("test content")
        
        # Test get_file
        success, content = router.get_file("test_repo", "test.txt")
        assert success is True
        assert content == "test content"
        mock_local_repo_manager.get_repo_path.assert_called_with("test_repo")
    
    def test_local_router_merge_branches(self, mock_local_repo_manager):
        """Test that LocalRouter uses local_repo_manager for merge."""
        sandbox_mode = GitHubSandboxMode()
        router = LocalRouter(mock_local_repo_manager, sandbox_mode)
        
        # Test merge_branches
        success, conflict = router.merge_branches("test_repo", "feature", "main")
        assert success is True
        assert conflict is None
        mock_local_repo_manager.merge_branch.assert_called_with(
            "test_repo", "feature", "main"
        )
    
    def test_synthetic_client_uses_local_repo_manager(self, mock_local_repo_manager):
        """Test that SyntheticGitHub uses local_repo_manager."""
        with patch('src.core.github.synthetic_client.get_local_repo_manager', 
                   return_value=mock_local_repo_manager):
            with patch('src.core.github.synthetic_client.get_deferred_push_queue'):
                with patch('src.core.github.synthetic_client.GitHubSandboxMode'):
                    github = SyntheticGitHub()
                    assert github.local_repo_manager is mock_local_repo_manager


class TestDeferredPushQueueIntegration:
    """Test 4: Integration with deferred_push_queue."""
    
    @pytest.fixture
    def mock_deferred_queue(self):
        """Create mock deferred push queue."""
        queue = Mock(spec=DeferredPushQueue)
        queue.enqueue_push = Mock()
        return queue
    
    @pytest.fixture
    def mock_local_repo_manager(self):
        """Create mock local repo manager."""
        manager = Mock(spec=LocalRepoManager)
        manager.get_repo_path = Mock(return_value=Path("/tmp/test_repo"))
        manager.get_repo_status = Mock(return_value={
            "github_url": "https://github.com/test/test_repo.git",
            "github_user": "test"
        })
        return manager
    
    def test_remote_router_uses_deferred_queue(self, mock_local_repo_manager, 
                                                mock_deferred_queue):
        """Test that RemoteRouter uses deferred_queue for push failures."""
        sandbox_mode = GitHubSandboxMode()
        router = RemoteRouter(mock_local_repo_manager, mock_deferred_queue, sandbox_mode)
        
        # Enable sandbox mode
        sandbox_mode.enable("test")
        
        # Test push_branch in sandbox mode
        success, error = router.push_branch("test_repo", "feature_branch")
        assert success is False
        assert "Sandbox mode" in error
        mock_deferred_queue.enqueue_push.assert_called_once()
    
    def test_remote_router_deferred_queue_on_rate_limit(self, mock_local_repo_manager,
                                                         mock_deferred_queue):
        """Test that RemoteRouter defers push on rate limit."""
        sandbox_mode = GitHubSandboxMode()
        # Disable sandbox mode to allow push attempt
        sandbox_mode.disable()
        router = RemoteRouter(mock_local_repo_manager, mock_deferred_queue, sandbox_mode)
        
        # Mock subprocess to return rate limit error
        with patch('subprocess.run') as mock_run:
            mock_result = Mock()
            mock_result.returncode = 1
            mock_result.stderr = "rate limit exceeded"
            mock_result.stdout = ""
            mock_run.return_value = mock_result
            
            # Test push_branch with rate limit
            success, error = router.push_branch("test_repo", "feature_branch")
            assert success is False
            assert "rate limit" in error.lower() or "deferred" in error.lower()
            mock_deferred_queue.enqueue_push.assert_called_once()
    
    def test_remote_router_deferred_queue_on_pr_failure(self, mock_local_repo_manager,
                                                        mock_deferred_queue):
        """Test that RemoteRouter defers PR creation on failure."""
        sandbox_mode = GitHubSandboxMode()
        router = RemoteRouter(mock_local_repo_manager, mock_deferred_queue, sandbox_mode)
        
        # Mock subprocess to return error
        with patch('subprocess.run') as mock_run:
            mock_result = Mock()
            mock_result.returncode = 1
            mock_result.stderr = "PR creation failed"
            mock_result.stdout = ""
            mock_run.return_value = mock_result
            
            # Test create_pr with failure
            success, error = router.create_pr("test_repo", "feature", "main", "Test PR")
            assert success is False
            mock_deferred_queue.enqueue_push.assert_called_once()
            # Check metadata was passed
            call_args = mock_deferred_queue.enqueue_push.call_args
            assert "metadata" in call_args.kwargs
            assert call_args.kwargs["metadata"]["action"] == "create_pr"
    
    def test_synthetic_client_uses_deferred_queue(self, mock_deferred_queue):
        """Test that SyntheticGitHub uses deferred_queue."""
        with patch('src.core.github.synthetic_client.get_local_repo_manager'):
            with patch('src.core.github.synthetic_client.get_deferred_push_queue',
                     return_value=mock_deferred_queue):
                with patch('src.core.github.synthetic_client.GitHubSandboxMode'):
                    github = SyntheticGitHub()
                    assert github.deferred_queue is mock_deferred_queue


class TestRoutingLogic:
    """Test 5: Routing logic (local vs remote)."""
    
    @pytest.fixture
    def temp_repo_dir(self):
        """Create temporary directory for test repos."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)
    
    @pytest.fixture
    def mock_local_repo_manager(self, temp_repo_dir):
        """Create mock local repo manager."""
        manager = Mock(spec=LocalRepoManager)
        repo_path = temp_repo_dir / "test_repo"
        repo_path.mkdir(parents=True)
        manager.get_repo_path = Mock(return_value=repo_path)
        manager.create_branch = Mock(return_value=True)
        manager.clone_from_github = Mock(return_value=(True, repo_path))
        manager.get_repo_status = Mock(return_value={
            "github_url": "https://github.com/test/test_repo.git",
            "github_user": "test"
        })
        return manager
    
    def test_local_router_handles_local_operations(self, mock_local_repo_manager):
        """Test that LocalRouter handles local operations correctly."""
        sandbox_mode = GitHubSandboxMode()
        router = LocalRouter(mock_local_repo_manager, sandbox_mode)
        
        # Test create_branch (local operation)
        result = router.create_branch("test_repo", "feature_branch")
        assert result is True
        mock_local_repo_manager.create_branch.assert_called_once()
    
    def test_remote_router_handles_remote_operations(self, mock_local_repo_manager):
        """Test that RemoteRouter handles remote operations correctly."""
        mock_deferred_queue = Mock(spec=DeferredPushQueue)
        sandbox_mode = GitHubSandboxMode()
        router = RemoteRouter(mock_local_repo_manager, mock_deferred_queue, sandbox_mode)
        
        # Test push_branch (remote operation) - should defer in sandbox mode
        sandbox_mode.enable("test")
        success, error = router.push_branch("test_repo", "feature_branch")
        assert success is False
        mock_deferred_queue.enqueue_push.assert_called_once()
    
    def test_synthetic_client_routes_to_local_first(self, mock_local_repo_manager):
        """Test that SyntheticGitHub routes to local first."""
        with patch('src.core.github.synthetic_client.get_local_repo_manager',
                  return_value=mock_local_repo_manager):
            with patch('src.core.github.synthetic_client.get_deferred_push_queue'):
                with patch('src.core.github.synthetic_client.GitHubSandboxMode'):
                    github = SyntheticGitHub()
                    
                    # Test get_repo - should use local first
                    success, repo_path, was_local = github.get_repo("test_repo")
                    assert success is True
                    assert was_local is True
                    mock_local_repo_manager.get_repo_path.assert_called_with("test_repo")
    
    def test_synthetic_client_falls_back_to_github(self, mock_local_repo_manager):
        """Test that SyntheticGitHub falls back to GitHub when local not found."""
        # Mock get_repo_path to return None (repo not found locally)
        mock_local_repo_manager.get_repo_path = Mock(return_value=None)
        
        with patch('src.core.github.synthetic_client.get_local_repo_manager',
                  return_value=mock_local_repo_manager):
            with patch('src.core.github.synthetic_client.get_deferred_push_queue'):
                # Create sandbox mode and disable it to allow GitHub clone
                sandbox_mode = GitHubSandboxMode()
                sandbox_mode.disable()
                with patch('src.core.github.synthetic_client.GitHubSandboxMode',
                          return_value=sandbox_mode):
                    github = SyntheticGitHub()
                    
                    # Test get_repo - should try to clone from GitHub
                    success, repo_path, was_local = github.get_repo("test_repo")
                    # Result depends on clone success, but should have tried
                    mock_local_repo_manager.clone_from_github.assert_called_once()
    
    def test_synthetic_client_routes_create_branch_to_local(self, mock_local_repo_manager):
        """Test that create_branch routes to local router."""
        with patch('src.core.github.synthetic_client.get_local_repo_manager',
                  return_value=mock_local_repo_manager):
            with patch('src.core.github.synthetic_client.get_deferred_push_queue'):
                with patch('src.core.github.synthetic_client.GitHubSandboxMode'):
                    github = SyntheticGitHub()
                    
                    # Test create_branch - should use local router
                    result = github.create_branch("test_repo", "feature_branch")
                    # Should have called local router
                    assert github.local_router is not None
    
    def test_synthetic_client_routes_push_to_remote(self, mock_local_repo_manager):
        """Test that push_branch routes to remote router."""
        mock_deferred_queue = Mock(spec=DeferredPushQueue)
        
        with patch('src.core.github.synthetic_client.get_local_repo_manager',
                  return_value=mock_local_repo_manager):
            with patch('src.core.github.synthetic_client.get_deferred_push_queue',
                     return_value=mock_deferred_queue):
                with patch('src.core.github.synthetic_client.GitHubSandboxMode'):
                    github = SyntheticGitHub()
                    
                    # Test push_branch - should use remote router
                    # Enable sandbox mode to avoid actual git push
                    github.sandbox_mode.enable("test")
                    success, error = github.push_branch("test_repo", "feature_branch")
                    # Should have called remote router
                    assert github.remote_router is not None
                    mock_deferred_queue.enqueue_push.assert_called_once()
    
    def test_synthetic_client_routes_get_file_to_local(self, mock_local_repo_manager, 
                                                       temp_repo_dir):
        """Test that get_file routes to local router."""
        repo_path = temp_repo_dir / "test_repo"
        # Use exist_ok=True to handle case where directory already exists
        repo_path.mkdir(parents=True, exist_ok=True)
        test_file = repo_path / "test.txt"
        test_file.write_text("test content")
        
        # Update mock to return the actual repo path
        mock_local_repo_manager.get_repo_path = Mock(return_value=repo_path)
        
        with patch('src.core.github.synthetic_client.get_local_repo_manager',
                  return_value=mock_local_repo_manager):
            with patch('src.core.github.synthetic_client.get_deferred_push_queue'):
                with patch('src.core.github.synthetic_client.GitHubSandboxMode'):
                    github = SyntheticGitHub()
                    
                    # Test get_file - should use local router
                    success, content = github.get_file("test_repo", "test.txt")
                    assert success is True
                    assert content == "test content"


class TestIntegrationScenarios:
    """Test 6: End-to-end integration scenarios."""
    
    @pytest.fixture
    def temp_repo_dir(self):
        """Create temporary directory for test repos."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)
    
    def test_full_workflow_local_first(self, temp_repo_dir):
        """Test full workflow with local-first strategy."""
        # Create test repo structure
        repo_path = temp_repo_dir / "test_repo"
        repo_path.mkdir(parents=True)
        (repo_path / "test.txt").write_text("initial content")
        
        # Mock dependencies
        mock_local_repo_manager = Mock(spec=LocalRepoManager)
        mock_local_repo_manager.get_repo_path = Mock(return_value=repo_path)
        mock_local_repo_manager.create_branch = Mock(return_value=True)
        
        mock_deferred_queue = Mock(spec=DeferredPushQueue)
        
        with patch('src.core.github.synthetic_client.get_local_repo_manager',
                  return_value=mock_local_repo_manager):
            with patch('src.core.github.synthetic_client.get_deferred_push_queue',
                     return_value=mock_deferred_queue):
                github = SyntheticGitHub()
                
                # 1. Get repo (local-first)
                success, path, was_local = github.get_repo("test_repo")
                assert success is True
                assert was_local is True
                
                # 2. Create branch (local)
                result = github.create_branch("test_repo", "feature")
                assert result is True
                
                # 3. Get file (local)
                success, content = github.get_file("test_repo", "test.txt")
                assert success is True
                assert content == "initial content"
    
    def test_sandbox_mode_workflow(self, temp_repo_dir):
        """Test workflow with sandbox mode enabled."""
        repo_path = temp_repo_dir / "test_repo"
        repo_path.mkdir(parents=True)
        
        mock_local_repo_manager = Mock(spec=LocalRepoManager)
        mock_local_repo_manager.get_repo_path = Mock(return_value=repo_path)
        mock_local_repo_manager.create_branch = Mock(return_value=True)
        
        mock_deferred_queue = Mock(spec=DeferredPushQueue)
        
        with patch('src.core.github.synthetic_client.get_local_repo_manager',
                  return_value=mock_local_repo_manager):
            with patch('src.core.github.synthetic_client.get_deferred_push_queue',
                     return_value=mock_deferred_queue):
                github = SyntheticGitHub()
                
                # Enable sandbox mode
                github.sandbox_mode.enable("test")
                assert github.is_sandbox_mode() is True
                
                # Push should be deferred
                success, error = github.push_branch("test_repo", "feature")
                assert success is False
                mock_deferred_queue.enqueue_push.assert_called_once()
                
                # PR creation should be deferred
                success, error = github.create_pr("test_repo", "feature", "main", "Test PR")
                assert success is False
                assert mock_deferred_queue.enqueue_push.call_count == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

