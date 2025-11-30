#!/usr/bin/env python3
"""
Unit tests for local_repo_layer.py - SSOT & System Integration Test Coverage

Tests LocalRepoManager class and repository management methods.
Target: ≥10 tests, ≥85% coverage, 100% passing.

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-11-29
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, mock_open
from pathlib import Path
import json
import sys
import tempfile
import shutil
import subprocess

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.local_repo_layer import (
    LocalRepoManager,
    get_local_repo_manager
)


class TestLocalRepoManager:
    """Test suite for LocalRepoManager class."""
    
    @pytest.fixture
    def temp_base(self):
        """Create temporary base directory."""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    @pytest.fixture
    def manager(self, temp_base):
        """Create LocalRepoManager instance."""
        return LocalRepoManager(base_path=temp_base)
    
    @pytest.fixture
    def temp_git_repo(self):
        """Create temporary git repository."""
        temp_dir = Path(tempfile.mkdtemp())
        
        # Initialize git repo
        subprocess.run(
            ["git", "init"],
            cwd=temp_dir,
            capture_output=True,
            text=True
        )
        
        # Configure git
        subprocess.run(
            ["git", "config", "user.name", "Test"],
            cwd=temp_dir,
            capture_output=True
        )
        subprocess.run(
            ["git", "config", "user.email", "test@test.com"],
            cwd=temp_dir,
            capture_output=True
        )
        
        # Create and commit initial file
        test_file = temp_dir / "test.txt"
        test_file.write_text("initial content")
        
        subprocess.run(
            ["git", "add", "test.txt"],
            cwd=temp_dir,
            capture_output=True
        )
        subprocess.run(
            ["git", "commit", "-m", "Initial commit"],
            cwd=temp_dir,
            capture_output=True
        )
        
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    def test_init_default_path(self):
        """Test initialization with default path."""
        with patch('src.core.local_repo_layer.Path') as mock_path:
            mock_file = Mock()
            mock_file.resolve.return_value.parent.parent.parent = Path("/project")
            mock_path.return_value = mock_file
            
            manager = LocalRepoManager()
            assert manager.base_path.exists()
    
    def test_init_custom_path(self, manager, temp_base):
        """Test initialization with custom path."""
        assert manager.base_path == temp_base
        assert manager.metadata_file.exists() or manager.metadata_file.parent.exists()
    
    def test_load_metadata_empty(self, manager):
        """Test loading metadata from empty file."""
        if manager.metadata_file.exists():
            manager.metadata_file.unlink()
        
        metadata = manager._load_metadata()
        assert metadata == {}
    
    def test_load_metadata_with_data(self, manager):
        """Test loading metadata from existing file."""
        test_data = {
            "repo1": {
                "local_path": str(manager.base_path / "repo1"),
                "github_url": "https://github.com/user/repo1.git",
                "status": "active"
            }
        }
        
        manager.metadata_file.parent.mkdir(parents=True, exist_ok=True)
        manager.metadata_file.write_text(json.dumps(test_data), encoding='utf-8')
        
        metadata = manager._load_metadata()
        assert "repo1" in metadata
    
    def test_load_metadata_invalid_json(self, manager):
        """Test loading metadata with invalid JSON."""
        manager.metadata_file.parent.mkdir(parents=True, exist_ok=True)
        manager.metadata_file.write_text("invalid json", encoding='utf-8')
        
        metadata = manager._load_metadata()
        assert metadata == {}
    
    def test_save_metadata(self, manager):
        """Test saving metadata to file."""
        manager.repos = {
            "repo1": {
                "local_path": str(manager.base_path / "repo1"),
                "status": "active"
            }
        }
        
        manager._save_metadata()
        
        assert manager.metadata_file.exists()
        data = json.loads(manager.metadata_file.read_text())
        assert "repo1" in data
    
    @patch('subprocess.run')
    def test_clone_from_github_success(self, mock_run, manager):
        """Test cloning repository from GitHub."""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stderr = ""
        
        success, repo_path = manager.clone_from_github("test-repo")
        
        assert success is True
        assert repo_path is not None
        assert "test-repo" in manager.repos
    
    @patch('subprocess.run')
    def test_clone_from_github_already_exists(self, mock_run, manager):
        """Test cloning repository that already exists."""
        # Create existing repo directory
        repo_path = manager.base_path / "test-repo"
        repo_path.mkdir(parents=True, exist_ok=True)
        
        manager.repos["test-repo"] = {
            "local_path": str(repo_path),
            "status": "active"
        }
        
        success, path = manager.clone_from_github("test-repo")
        
        assert success is True
        assert path == repo_path
        # Should not call git clone
        mock_run.assert_not_called()
    
    @patch('subprocess.run')
    def test_clone_from_github_failure(self, mock_run, manager):
        """Test cloning repository failure."""
        mock_run.return_value.returncode = 1
        mock_run.return_value.stderr = "Clone failed"
        
        success, repo_path = manager.clone_from_github("test-repo")
        
        assert success is False
        assert repo_path is None
    
    def test_clone_locally(self, manager, temp_git_repo):
        """Test cloning from local repository."""
        success, repo_path = manager.clone_locally("local-repo", temp_git_repo)
        
        assert success is True
        assert repo_path is not None
        assert repo_path.exists()
        assert "local-repo" in manager.repos
    
    def test_get_repo_path_exists(self, manager):
        """Test getting repo path that exists."""
        repo_path = manager.base_path / "test-repo"
        repo_path.mkdir(parents=True, exist_ok=True)
        
        manager.repos["test-repo"] = {
            "local_path": str(repo_path)
        }
        
        result = manager.get_repo_path("test-repo")
        assert result == repo_path
    
    def test_get_repo_path_not_found(self, manager):
        """Test getting repo path that doesn't exist."""
        result = manager.get_repo_path("nonexistent")
        assert result is None
    
    def test_get_repo_path_missing_directory(self, manager):
        """Test getting repo path where directory is missing."""
        manager.repos["test-repo"] = {
            "local_path": str(manager.base_path / "nonexistent")
        }
        
        result = manager.get_repo_path("test-repo")
        assert result is None
    
    @patch('subprocess.run')
    def test_create_branch_success(self, mock_run, manager):
        """Test creating branch successfully."""
        repo_path = manager.base_path / "test-repo"
        repo_path.mkdir(parents=True, exist_ok=True)
        
        manager.repos["test-repo"] = {
            "local_path": str(repo_path)
        }
        
        mock_run.return_value.returncode = 0
        
        result = manager.create_branch("test-repo", "new-branch")
        
        assert result is True
    
    def test_create_branch_repo_not_found(self, manager):
        """Test creating branch for non-existent repo."""
        result = manager.create_branch("nonexistent", "branch")
        assert result is False
    
    @patch('subprocess.run')
    def test_merge_branch_success(self, mock_run, manager, temp_git_repo):
        """Test merging branches successfully."""
        manager.repos["test-repo"] = {
            "local_path": str(temp_git_repo)
        }
        
        mock_run.return_value.returncode = 0
        
        success, error = manager.merge_branch("test-repo", "branch1", "main")
        
        assert success is True
        assert error is None
    
    @patch('subprocess.run')
    def test_merge_branch_conflict(self, mock_run, manager, temp_git_repo):
        """Test merging branches with conflict."""
        manager.repos["test-repo"] = {
            "local_path": str(temp_git_repo)
        }
        
        mock_run.return_value.returncode = 1
        mock_run.return_value.stdout = "CONFLICT: file.txt"
        mock_run.return_value.stderr = ""
        
        success, error = manager.merge_branch("test-repo", "branch1", "main")
        
        assert success is False
        assert error is not None
    
    def test_merge_branch_repo_not_found(self, manager):
        """Test merging branches for non-existent repo."""
        success, error = manager.merge_branch("nonexistent", "branch1", "main")
        assert success is False
        assert error == "Repository not found"
    
    @patch('subprocess.run')
    def test_generate_patch(self, mock_run, manager, temp_git_repo):
        """Test generating patch file."""
        manager.repos["test-repo"] = {
            "local_path": str(temp_git_repo)
        }
        
        mock_run.side_effect = [
            Mock(returncode=0, stdout="main\n", stderr=""),
            Mock(returncode=0, stdout="patch content", stderr="")
        ]
        
        patch_path = manager.generate_patch("test-repo", "branch1")
        
        assert patch_path is not None
        assert patch_path.exists()
    
    def test_generate_patch_repo_not_found(self, manager):
        """Test generating patch for non-existent repo."""
        patch_path = manager.generate_patch("nonexistent", "branch")
        assert patch_path is None
    
    def test_list_repos(self, manager):
        """Test listing repositories."""
        manager.repos = {
            "repo1": {},
            "repo2": {}
        }
        
        repos = manager.list_repos()
        assert len(repos) == 2
        assert "repo1" in repos
        assert "repo2" in repos
    
    def test_get_repo_status(self, manager):
        """Test getting repo status."""
        manager.repos["test-repo"] = {
            "status": "active",
            "local_path": "/path/to/repo"
        }
        
        status = manager.get_repo_status("test-repo")
        assert status is not None
        assert status["status"] == "active"
    
    def test_get_repo_status_not_found(self, manager):
        """Test getting status for non-existent repo."""
        status = manager.get_repo_status("nonexistent")
        assert status is None
    
    def test_remove_repo(self, manager):
        """Test removing repository."""
        repo_path = manager.base_path / "test-repo"
        repo_path.mkdir(parents=True, exist_ok=True)
        
        manager.repos["test-repo"] = {
            "local_path": str(repo_path)
        }
        
        result = manager.remove_repo("test-repo")
        
        assert result is True
        assert "test-repo" not in manager.repos
    
    def test_remove_repo_not_found(self, manager):
        """Test removing non-existent repository."""
        result = manager.remove_repo("nonexistent")
        assert result is False


class TestGlobalFunctions:
    """Test suite for global functions."""
    
    def test_get_local_repo_manager_singleton(self, tmp_path):
        """Test global manager singleton."""
        with patch('src.core.local_repo_layer._local_repo_manager', None):
            manager1 = get_local_repo_manager(base_path=tmp_path)
            manager2 = get_local_repo_manager(base_path=tmp_path)
            assert manager1 is manager2

