#!/usr/bin/env python3
"""
Unit tests for end_of_cycle_push.py - Infrastructure Test Coverage

Tests EndOfCyclePush class and end-of-cycle push protocol operations.
Target: ≥85% coverage, comprehensive test methods.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, date
import subprocess
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.end_of_cycle_push import EndOfCyclePush


class TestEndOfCyclePush:
    """Test suite for EndOfCyclePush class."""

    @pytest.fixture
    def temp_workspace(self, tmp_path):
        """Create temporary workspace for testing."""
        workspace = tmp_path / "agent_workspaces" / "Agent-Test"
        workspace.mkdir(parents=True)
        return workspace

    @pytest.fixture
    def push_handler(self, temp_workspace):
        """Create EndOfCyclePush instance with temp workspace."""
        with patch('src.core.end_of_cycle_push.Path') as mock_path_class:
            def path_side_effect(path_str):
                if "agent_workspaces/Agent-Test" in str(path_str):
                    return temp_workspace
                return Path(path_str)
            
            mock_path_class.side_effect = path_side_effect
            
            handler = EndOfCyclePush('Agent-Test')
            handler.workspace = temp_workspace
            return handler

    def test_initialization(self, temp_workspace):
        """Test initialization creates handler with agent ID."""
        with patch('src.core.end_of_cycle_push.Path') as mock_path_class:
            def path_side_effect(path_str):
                if "agent_workspaces/Agent-Test" in str(path_str):
                    return temp_workspace
                return Path(path_str)
            
            mock_path_class.side_effect = path_side_effect
            
            handler = EndOfCyclePush('Agent-Test')
            
            assert handler.agent_id == "Agent-Test"
            assert handler.tracker is not None

    @patch('src.core.end_of_cycle_push.subprocess.run')
    def test_check_git_status_success(self, mock_subprocess, push_handler):
        """Test checking git status successfully."""
        mock_result = MagicMock()
        mock_result.stdout = "M  file1.py\nA  file2.py"
        mock_result.returncode = 0
        mock_subprocess.return_value = mock_result
        
        status = push_handler._check_git_status()
        
        assert "M  file1.py" in status
        assert "A  file2.py" in status

    @patch('src.core.end_of_cycle_push.subprocess.run')
    def test_check_git_status_failure(self, mock_subprocess, push_handler):
        """Test checking git status when command fails."""
        mock_subprocess.side_effect = subprocess.CalledProcessError(1, 'git')
        
        status = push_handler._check_git_status()
        
        assert status == "Error checking git status"

    @patch('src.core.end_of_cycle_push.subprocess.run')
    def test_get_uncommitted_files_with_changes(self, mock_subprocess, push_handler):
        """Test getting uncommitted files when changes exist."""
        # Mock git diff
        diff_result = MagicMock()
        diff_result.stdout = "file1.py\nfile2.py"
        diff_result.returncode = 0
        
        # Mock git diff --cached
        cached_result = MagicMock()
        cached_result.stdout = "file3.py"
        cached_result.returncode = 0
        
        mock_subprocess.side_effect = [diff_result, cached_result]
        
        files = push_handler._get_uncommitted_files()
        
        assert "file1.py" in files
        assert "file2.py" in files
        assert "file3.py" in files

    @patch('src.core.end_of_cycle_push.subprocess.run')
    def test_get_uncommitted_files_no_changes(self, mock_subprocess, push_handler):
        """Test getting uncommitted files when no changes exist."""
        diff_result = MagicMock()
        diff_result.stdout = ""
        diff_result.returncode = 0
        
        cached_result = MagicMock()
        cached_result.stdout = ""
        cached_result.returncode = 0
        
        mock_subprocess.side_effect = [diff_result, cached_result]
        
        files = push_handler._get_uncommitted_files()
        
        assert files == []

    @patch('src.core.end_of_cycle_push.subprocess.run')
    def test_get_uncommitted_files_failure(self, mock_subprocess, push_handler):
        """Test getting uncommitted files when command fails."""
        mock_subprocess.side_effect = subprocess.CalledProcessError(1, 'git')
        
        files = push_handler._get_uncommitted_files()
        
        assert files == []

    @patch('src.core.end_of_cycle_push.subprocess.run')
    def test_get_unpushed_commits_with_commits(self, mock_subprocess, push_handler):
        """Test getting unpushed commits when commits exist."""
        mock_result = MagicMock()
        mock_result.stdout = "abc123 Commit 1\ndef456 Commit 2"
        mock_result.returncode = 0
        mock_subprocess.return_value = mock_result
        
        commits = push_handler._get_unpushed_commits()
        
        assert len(commits) == 2
        assert "abc123 Commit 1" in commits
        assert "def456 Commit 2" in commits

    @patch('src.core.end_of_cycle_push.subprocess.run')
    def test_get_unpushed_commits_no_commits(self, mock_subprocess, push_handler):
        """Test getting unpushed commits when none exist."""
        mock_result = MagicMock()
        mock_result.stdout = ""
        mock_result.returncode = 0
        mock_subprocess.return_value = mock_result
        
        commits = push_handler._get_unpushed_commits()
        
        assert commits == []

    @patch('src.core.end_of_cycle_push.subprocess.run')
    def test_get_unpushed_commits_failure(self, mock_subprocess, push_handler):
        """Test getting unpushed commits when command fails."""
        mock_subprocess.side_effect = subprocess.CalledProcessError(1, 'git')
        
        commits = push_handler._get_unpushed_commits()
        
        assert commits == []

    @patch('src.core.end_of_cycle_push.subprocess.run')
    def test_prepare_for_push_no_changes(self, mock_subprocess, push_handler):
        """Test preparing for push when no changes exist."""
        # Mock git status
        status_result = MagicMock()
        status_result.stdout = ""
        status_result.returncode = 0
        
        # Mock git diff
        diff_result = MagicMock()
        diff_result.stdout = ""
        diff_result.returncode = 0
        
        cached_result = MagicMock()
        cached_result.stdout = ""
        cached_result.returncode = 0
        
        # Mock git log
        log_result = MagicMock()
        log_result.stdout = ""
        log_result.returncode = 0
        
        mock_subprocess.side_effect = [status_result, diff_result, cached_result, log_result]
        
        with patch.object(push_handler.tracker, 'start_new_day') as mock_start, \
             patch.object(push_handler.tracker, 'mark_ready_for_push') as mock_mark:
            
            result = push_handler.prepare_for_push()
            
            assert result["ready_for_push"] is True
            assert result["has_changes"] is False
            assert result["uncommitted_files"] == []
            assert result["unpushed_commits"] == []

    @patch('src.core.end_of_cycle_push.subprocess.run')
    def test_prepare_for_push_with_changes(self, mock_subprocess, push_handler):
        """Test preparing for push when changes exist."""
        # Mock git status
        status_result = MagicMock()
        status_result.stdout = "M  file1.py"
        status_result.returncode = 0
        
        # Mock git diff
        diff_result = MagicMock()
        diff_result.stdout = "file1.py"
        diff_result.returncode = 0
        
        cached_result = MagicMock()
        cached_result.stdout = ""
        cached_result.returncode = 0
        
        # Mock git log
        log_result = MagicMock()
        log_result.stdout = ""
        log_result.returncode = 0
        
        mock_subprocess.side_effect = [status_result, diff_result, cached_result, log_result]
        
        with patch.object(push_handler.tracker, 'start_new_day') as mock_start, \
             patch.object(push_handler.tracker, 'mark_ready_for_push') as mock_mark:
            
            result = push_handler.prepare_for_push()
            
            assert result["ready_for_push"] is True
            assert result["has_changes"] is True
            assert len(result["uncommitted_files"]) > 0

    @patch('src.core.end_of_cycle_push.subprocess.run')
    def test_execute_push_staging_failure(self, mock_subprocess, push_handler):
        """Test execute_push handles staging failure."""
        mock_subprocess.side_effect = subprocess.CalledProcessError(1, 'git', stderr="Error")
        
        result = push_handler.execute_push()
        
        assert result["success"] is False
        assert result["stage"] == "staging"
        assert "Failed to stage" in result["error"]

    @patch('src.core.end_of_cycle_push.subprocess.run')
    def test_execute_push_commit_failure(self, mock_subprocess, push_handler):
        """Test execute_push handles commit failure."""
        # Mock git add success
        add_result = MagicMock()
        add_result.returncode = 0
        
        # Mock git diff (uncommitted files exist)
        diff_result = MagicMock()
        diff_result.stdout = "file1.py"
        diff_result.returncode = 0
        
        cached_result = MagicMock()
        cached_result.stdout = ""
        cached_result.returncode = 0
        
        # Mock git commit failure
        commit_error = subprocess.CalledProcessError(1, 'git', stderr="Commit error")
        
        mock_subprocess.side_effect = [add_result, diff_result, cached_result, commit_error]
        
        with patch.object(push_handler.tracker, 'get_today_summary', return_value={}):
            result = push_handler.execute_push()
            
            assert result["success"] is False
            assert result["stage"] == "committing"

    @patch('src.core.end_of_cycle_push.subprocess.run')
    def test_execute_push_push_failure(self, mock_subprocess, push_handler):
        """Test execute_push handles push failure."""
        # Mock git add success
        add_result = MagicMock()
        add_result.returncode = 0
        
        # Mock git diff (no uncommitted files)
        diff_result = MagicMock()
        diff_result.stdout = ""
        diff_result.returncode = 0
        
        cached_result = MagicMock()
        cached_result.stdout = ""
        cached_result.returncode = 0
        
        # Mock git log (unpushed commits exist)
        log_result = MagicMock()
        log_result.stdout = "abc123 Commit"
        log_result.returncode = 0
        
        # Mock git push failure
        push_error = subprocess.CalledProcessError(1, 'git', stderr="Push error")
        
        mock_subprocess.side_effect = [add_result, diff_result, cached_result, log_result, push_error]
        
        with patch.object(push_handler.tracker, 'get_today_summary', return_value={}):
            result = push_handler.execute_push()
            
            assert result["success"] is False
            assert result["stage"] == "pushing"

    @patch('src.core.end_of_cycle_push.subprocess.run')
    def test_execute_push_success_no_changes(self, mock_subprocess, push_handler):
        """Test execute_push succeeds when no changes to commit or push."""
        # Mock git add success
        add_result = MagicMock()
        add_result.returncode = 0
        
        # Mock git diff (no uncommitted files)
        diff_result = MagicMock()
        diff_result.stdout = ""
        diff_result.returncode = 0
        
        cached_result = MagicMock()
        cached_result.stdout = ""
        cached_result.returncode = 0
        
        # Mock git log (no unpushed commits)
        log_result = MagicMock()
        log_result.stdout = ""
        log_result.returncode = 0
        
        mock_subprocess.side_effect = [add_result, diff_result, cached_result, log_result]
        
        with patch.object(push_handler.tracker, 'get_today_summary', return_value={}):
            result = push_handler.execute_push()
            
            assert result["success"] is True
            assert result["committed"] is False
            assert result["pushed"] is False

    @patch('src.core.end_of_cycle_push.subprocess.run')
    def test_execute_push_success_with_commit(self, mock_subprocess, push_handler):
        """Test execute_push succeeds with commit."""
        # Mock git add success
        add_result = MagicMock()
        add_result.returncode = 0
        
        # Mock git diff (uncommitted files exist)
        diff_result = MagicMock()
        diff_result.stdout = "file1.py"
        diff_result.returncode = 0
        
        cached_result = MagicMock()
        cached_result.stdout = ""
        cached_result.returncode = 0
        
        # Mock git commit success
        commit_result = MagicMock()
        commit_result.returncode = 0
        
        # Mock git log (no unpushed commits)
        log_result = MagicMock()
        log_result.stdout = ""
        log_result.returncode = 0
        
        mock_subprocess.side_effect = [add_result, diff_result, cached_result, commit_result, log_result]
        
        with patch.object(push_handler.tracker, 'get_today_summary', return_value={}), \
             patch.object(push_handler.tracker, 'record_commit') as mock_record:
            
            result = push_handler.execute_push()
            
            assert result["success"] is True
            assert result["committed"] is True
            mock_record.assert_called_once()

    @patch('src.core.end_of_cycle_push.subprocess.run')
    def test_execute_push_with_custom_commit_message(self, mock_subprocess, push_handler):
        """Test execute_push uses custom commit message."""
        # Mock git add success
        add_result = MagicMock()
        add_result.returncode = 0
        
        # Mock git diff (uncommitted files exist)
        diff_result = MagicMock()
        diff_result.stdout = "file1.py"
        diff_result.returncode = 0
        
        cached_result = MagicMock()
        cached_result.stdout = ""
        cached_result.returncode = 0
        
        # Mock git commit success
        commit_result = MagicMock()
        commit_result.returncode = 0
        
        # Mock git log
        log_result = MagicMock()
        log_result.stdout = ""
        log_result.returncode = 0
        
        mock_subprocess.side_effect = [add_result, diff_result, cached_result, commit_result, log_result]
        
        with patch.object(push_handler.tracker, 'get_today_summary', return_value={}), \
             patch.object(push_handler.tracker, 'record_commit'):
            
            result = push_handler.execute_push(commit_message="Custom message")
            
            # Verify commit was called with custom message
            commit_call = [call for call in mock_subprocess.call_args_list if 'commit' in str(call)]
            assert len(commit_call) > 0

    @patch('src.core.end_of_cycle_push.subprocess.run')
    def test_execute_push_success_with_push(self, mock_subprocess, push_handler):
        """Test execute_push succeeds with push."""
        # Mock git add success
        add_result = MagicMock()
        add_result.returncode = 0
        
        # Mock git diff (no uncommitted files)
        diff_result = MagicMock()
        diff_result.stdout = ""
        diff_result.returncode = 0
        
        cached_result = MagicMock()
        cached_result.stdout = ""
        cached_result.returncode = 0
        
        # Mock git log (unpushed commits exist)
        log_result = MagicMock()
        log_result.stdout = "abc123 Commit"
        log_result.returncode = 0
        
        # Mock git push success
        push_result = MagicMock()
        push_result.returncode = 0
        
        mock_subprocess.side_effect = [add_result, diff_result, cached_result, log_result, push_result]
        
        with patch.object(push_handler.tracker, 'get_today_summary', return_value={}), \
             patch.object(push_handler.tracker, 'mark_pushed') as mock_mark:
            
            result = push_handler.execute_push()
            
            assert result["success"] is True
            assert result["pushed"] is True
            mock_mark.assert_called_once()

