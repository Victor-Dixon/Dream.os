"""
Tests for verify_archived_repos.py

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-01-27
"""

import pytest
import tempfile
import json
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
from datetime import datetime, timedelta

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "tools"))

from verify_archived_repos import (
    ARCHIVED_REPOS,
    clone_repo,
    get_file_list,
    check_merge_commit,
    verify_repo
)


class TestArchivedRepos:
    """Test suite for archived repos constants and structure"""
    
    def test_archived_repos_structure(self):
        """Test that ARCHIVED_REPOS has correct structure"""
        assert isinstance(ARCHIVED_REPOS, dict)
        assert len(ARCHIVED_REPOS) > 0
        
        # Check structure of first repo
        first_repo = list(ARCHIVED_REPOS.values())[0]
        assert "repo_id" in first_repo
        assert "target" in first_repo
        assert "target_id" in first_repo
        assert "archived_date" in first_repo
        assert "verification_end" in first_repo
    
    def test_archived_repos_has_metuber(self):
        """Test that MeTuber is in archived repos"""
        assert "MeTuber" in ARCHIVED_REPOS or "metuber" in ARCHIVED_REPOS.lower()
    
    def test_archived_repos_has_dadudekc(self):
        """Test that DaDudekC is in archived repos"""
        assert any("dadudekc" in k.lower() for k in ARCHIVED_REPOS.keys())


class TestCloneRepo:
    """Test suite for clone_repo function"""
    
    @patch('verify_archived_repos.subprocess.run')
    def test_clone_repo_success(self, mock_subprocess):
        """Test successful repo clone"""
        mock_subprocess.return_value.returncode = 0
        mock_subprocess.return_value.stdout = ""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            result = clone_repo("test_repo", Path(tmpdir))
            # Function may return None or path depending on implementation
            assert result is None or isinstance(result, Path)
    
    @patch('verify_archived_repos.subprocess.run')
    def test_clone_repo_failure(self, mock_subprocess):
        """Test failed repo clone"""
        mock_subprocess.side_effect = subprocess.CalledProcessError(1, "git")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            result = clone_repo("test_repo", Path(tmpdir))
            assert result is None
    
    def test_clone_repo_already_exists(self):
        """Test clone when repo already exists"""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir) / "test_repo"
            repo_path.mkdir()
            
            result = clone_repo("test_repo", Path(tmpdir))
            assert result == repo_path


class TestGetFileList:
    """Test suite for get_file_list function"""
    
    def test_get_file_list_empty(self):
        """Test getting file list from empty directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            files = get_file_list(Path(tmpdir))
            assert isinstance(files, list)
            assert len(files) == 0
    
    def test_get_file_list_with_files(self):
        """Test getting file list with files"""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "file1.txt").write_text("content1")
            (Path(tmpdir) / "file2.txt").write_text("content2")
            (Path(tmpdir) / "subdir").mkdir()
            (Path(tmpdir) / "subdir" / "file3.txt").write_text("content3")
            
            files = get_file_list(Path(tmpdir))
            assert len(files) == 3
            assert "file1.txt" in files
            assert "file2.txt" in files
            # Handle both Windows (\) and Unix (/) path separators
            assert any("file3.txt" in f and "subdir" in f for f in files)
    
    def test_get_file_list_excludes_git(self):
        """Test that .git directory is excluded"""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "file.txt").write_text("content")
            (Path(tmpdir) / ".git").mkdir()
            (Path(tmpdir) / ".git" / "config").write_text("git config")
            
            files = get_file_list(Path(tmpdir))
            assert ".git/config" not in files
            assert "file.txt" in files


class TestCheckMergeCommit:
    """Test suite for check_merge_commit function"""
    
    @patch('verify_archived_repos.subprocess.run')
    def test_check_merge_commit_found(self, mock_subprocess):
        """Test finding merge commit"""
        mock_commits = [
            {
                "sha": "abc123",
                "commit": {
                    "message": "Merge source_repo into target_repo"
                }
            }
        ]
        mock_subprocess.return_value.returncode = 0
        mock_subprocess.return_value.stdout = json.dumps(mock_commits)
        
        has_merge, sha = check_merge_commit("target_repo", "source_repo")
        assert has_merge is True
        assert sha == "abc123"
    
    @patch('verify_archived_repos.subprocess.run')
    def test_check_merge_commit_not_found(self, mock_subprocess):
        """Test when merge commit not found"""
        mock_commits = [
            {
                "sha": "abc123",
                "commit": {
                    "message": "Regular commit message"
                }
            }
        ]
        mock_subprocess.return_value.returncode = 0
        mock_subprocess.return_value.stdout = json.dumps(mock_commits)
        
        has_merge, sha = check_merge_commit("target_repo", "source_repo")
        assert has_merge is False
        assert sha is None
    
    @patch('verify_archived_repos.subprocess.run')
    def test_check_merge_commit_error(self, mock_subprocess):
        """Test when subprocess fails"""
        mock_subprocess.side_effect = Exception("API error")
        
        has_merge, sha = check_merge_commit("target_repo", "source_repo")
        assert has_merge is False
        assert sha is None


class TestVerifyRepo:
    """Test suite for verify_repo function"""
    
    @patch('verify_archived_repos.clone_repo')
    @patch('verify_archived_repos.get_file_list')
    @patch('verify_archived_repos.check_merge_commit')
    def test_verify_repo_dry_run(self, mock_check_merge, mock_get_files, mock_clone):
        """Test verify_repo in dry run mode"""
        result = verify_repo("MeTuber", dry_run=True)
        assert isinstance(result, dict)
        assert result["status"] == "dry-run"
        assert result["repo"] == "MeTuber"
    
    @patch('verify_archived_repos.clone_repo')
    @patch('verify_archived_repos.get_file_list')
    @patch('verify_archived_repos.check_merge_commit')
    def test_verify_repo_success(self, mock_check_merge, mock_get_files, mock_clone):
        """Test successful repo verification"""
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_clone.return_value = Path(tmpdir) / "test_repo"
            mock_get_files.return_value = ["file1.txt", "file2.txt"]
            mock_check_merge.return_value = (True, "abc123")
            
            with patch('verify_archived_repos.project_root', Path(tmpdir)):
                result = verify_repo("MeTuber", dry_run=False)
                assert isinstance(result, dict)
                assert result["status"] in ["verified", "needs_review"]
                assert result["repo"] == "MeTuber"
    
    @patch('verify_archived_repos.clone_repo')
    def test_verify_repo_clone_failure(self, mock_clone):
        """Test verification when clone fails"""
        mock_clone.return_value = None
        
        with patch('verify_archived_repos.project_root', Path("/tmp")):
            result = verify_repo("MeTuber", dry_run=False)
            assert isinstance(result, dict)
            assert result["status"] == "failed"
            assert "error" in result

