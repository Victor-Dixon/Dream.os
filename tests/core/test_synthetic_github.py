"""
Unit Tests for Synthetic GitHub
================================
"""

import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch, Mock
from src.core.synthetic_github import (
    SyntheticGitHub,
    GitHubSandboxMode,
    get_synthetic_github,
)


class TestGitHubSandboxMode:
    """Tests for GitHubSandboxMode."""

    def test_initialization(self):
        """Test sandbox mode initialization."""
        sandbox = GitHubSandboxMode()
        assert sandbox.config_file is not None
        assert "sandbox_mode" in sandbox.config

    def test_initialization_with_config_file(self, tmp_path):
        """Test initialization with config file."""
        config_file = tmp_path / "sandbox.json"
        import json
        config_file.write_text(json.dumps({"sandbox_mode": True}))
        
        sandbox = GitHubSandboxMode(config_file)
        assert sandbox.config_file == config_file

    def test_is_enabled_false(self):
        """Test checking if sandbox mode is disabled."""
        sandbox = GitHubSandboxMode()
        sandbox.config["sandbox_mode"] = False
        assert sandbox.is_enabled() is False

    def test_is_enabled_true(self):
        """Test checking if sandbox mode is enabled."""
        sandbox = GitHubSandboxMode()
        sandbox.config["sandbox_mode"] = True
        assert sandbox.is_enabled() is True

    @patch('src.core.synthetic_github.subprocess.run')
    def test_detect_github_availability_success(self, mock_subprocess):
        """Test detecting GitHub availability (success)."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "200"
        mock_subprocess.return_value = mock_result
        
        sandbox = GitHubSandboxMode()
        available = sandbox._detect_github_availability()
        assert available is True

    @patch('src.core.synthetic_github.subprocess.run')
    def test_detect_github_availability_failure(self, mock_subprocess):
        """Test detecting GitHub availability (failure)."""
        # Mock subprocess to raise exception (simulating curl failure)
        mock_subprocess.side_effect = Exception("Curl failed")
        
        sandbox = GitHubSandboxMode()
        available = sandbox._detect_github_availability()
        # Should return False when exception occurs
        assert available is False

    def test_enable(self, tmp_path):
        """Test enabling sandbox mode."""
        config_file = tmp_path / "sandbox.json"
        sandbox = GitHubSandboxMode(config_file)
        sandbox.enable("test_reason")
        assert sandbox.config["sandbox_mode"] is True
        assert sandbox.config["reason"] == "test_reason"

    def test_disable(self, tmp_path):
        """Test disabling sandbox mode."""
        config_file = tmp_path / "sandbox.json"
        sandbox = GitHubSandboxMode(config_file)
        sandbox.config["sandbox_mode"] = True
        sandbox.disable()
        assert sandbox.config["sandbox_mode"] is False


class TestSyntheticGitHub:
    """Tests for SyntheticGitHub."""

    @patch('src.core.synthetic_github.get_local_repo_manager')
    @patch('src.core.synthetic_github.get_deferred_push_queue')
    def test_initialization(self, mock_queue, mock_repo):
        """Test synthetic GitHub initialization."""
        mock_repo.return_value = MagicMock()
        mock_queue.return_value = MagicMock()
        
        github = SyntheticGitHub()
        assert github.local_repo_manager is not None
        assert github.deferred_queue is not None
        assert github.sandbox_mode is not None

    @patch('src.core.synthetic_github.get_local_repo_manager')
    @patch('src.core.synthetic_github.get_deferred_push_queue')
    def test_get_repo_local_exists(self, mock_queue, mock_repo):
        """Test getting repo when local exists."""
        mock_repo_manager = MagicMock()
        mock_repo_manager.get_repo_path.return_value = Path("/tmp/test_repo")
        mock_repo.return_value = mock_repo_manager
        mock_queue.return_value = MagicMock()
        
        github = SyntheticGitHub()
        success, repo_path, was_local = github.get_repo("test_repo")
        assert success is True
        assert was_local is True

    @patch('src.core.synthetic_github.get_local_repo_manager')
    @patch('src.core.synthetic_github.get_deferred_push_queue')
    def test_get_repo_sandbox_mode(self, mock_queue, mock_repo):
        """Test getting repo in sandbox mode."""
        mock_repo_manager = MagicMock()
        mock_repo_manager.get_repo_path.return_value = None
        mock_repo.return_value = mock_repo_manager
        mock_queue.return_value = MagicMock()
        
        github = SyntheticGitHub()
        github.sandbox_mode.config["sandbox_mode"] = True
        success, repo_path, was_local = github.get_repo("test_repo")
        assert success is False

    @patch('src.core.synthetic_github.get_local_repo_manager')
    @patch('src.core.synthetic_github.get_deferred_push_queue')
    def test_create_branch(self, mock_queue, mock_repo):
        """Test creating branch."""
        mock_repo_manager = MagicMock()
        mock_repo_manager.get_repo_path.return_value = Path("/tmp/test_repo")
        mock_repo_manager.create_branch.return_value = True
        mock_repo.return_value = mock_repo_manager
        mock_queue.return_value = MagicMock()
        
        github = SyntheticGitHub()
        success = github.create_branch("test_repo", "feature_branch")
        assert success is True

    @patch('src.core.synthetic_github.get_local_repo_manager')
    @patch('src.core.synthetic_github.get_deferred_push_queue')
    def test_push_branch_sandbox_mode(self, mock_queue, mock_repo):
        """Test pushing branch in sandbox mode."""
        mock_repo_manager = MagicMock()
        mock_repo.return_value = mock_repo_manager
        mock_queue_instance = MagicMock()
        mock_queue.return_value = mock_queue_instance
        
        github = SyntheticGitHub()
        github.sandbox_mode.config["sandbox_mode"] = True
        success, error = github.push_branch("test_repo", "feature_branch")
        assert success is False
        assert "Sandbox mode" in error
        mock_queue_instance.enqueue_push.assert_called_once()

    @patch('src.core.synthetic_github.get_local_repo_manager')
    @patch('src.core.synthetic_github.get_deferred_push_queue')
    def test_create_pr_sandbox_mode(self, mock_queue, mock_repo):
        """Test creating PR in sandbox mode."""
        mock_repo_manager = MagicMock()
        mock_repo.return_value = mock_repo_manager
        mock_queue_instance = MagicMock()
        mock_queue.return_value = mock_queue_instance
        
        github = SyntheticGitHub()
        github.sandbox_mode.config["sandbox_mode"] = True
        success, error = github.create_pr("test_repo", "feature_branch")
        assert success is False
        assert "Sandbox mode" in error

    @patch('src.core.synthetic_github.get_local_repo_manager')
    @patch('src.core.synthetic_github.get_deferred_push_queue')
    def test_get_file(self, mock_queue, mock_repo):
        """Test getting file content."""
        mock_repo_manager = MagicMock()
        repo_path = Path("/tmp/test_repo")
        mock_repo_manager.get_repo_path.return_value = repo_path
        mock_repo.return_value = mock_repo_manager
        mock_queue.return_value = MagicMock()
        
        # Create temporary file
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.txt"
            test_file.write_text("test content")
            
            github = SyntheticGitHub()
            github.local_repo_manager.get_repo_path = lambda x: Path(tmpdir)
            success, content = github.get_file("test_repo", "test.txt")
            assert success is True
            assert content == "test content"

    @patch('src.core.synthetic_github.get_local_repo_manager')
    @patch('src.core.synthetic_github.get_deferred_push_queue')
    def test_is_sandbox_mode(self, mock_queue, mock_repo):
        """Test checking sandbox mode."""
        mock_repo.return_value = MagicMock()
        mock_queue.return_value = MagicMock()
        
        github = SyntheticGitHub()
        github.sandbox_mode.config["sandbox_mode"] = True
        assert github.is_sandbox_mode() is True


class TestFactoryFunction:
    """Tests for factory function."""

    @patch('src.core.synthetic_github.get_local_repo_manager')
    @patch('src.core.synthetic_github.get_deferred_push_queue')
    def test_get_synthetic_github(self, mock_queue, mock_repo):
        """Test getting synthetic GitHub instance."""
        mock_repo.return_value = MagicMock()
        mock_queue.return_value = MagicMock()
        
        github1 = get_synthetic_github()
        github2 = get_synthetic_github()
        assert github1 is github2  # Should be singleton


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

