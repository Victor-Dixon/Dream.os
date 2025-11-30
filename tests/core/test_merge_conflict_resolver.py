#!/usr/bin/env python3
"""
Unit tests for merge_conflict_resolver.py - SSOT & System Integration Test Coverage

Tests MergeConflictResolver class and conflict resolution methods.
Target: ≥10 tests, ≥85% coverage, 100% passing.

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-11-29
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, mock_open
from pathlib import Path
import subprocess
import sys
import tempfile
import shutil

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.merge_conflict_resolver import (
    MergeConflictResolver,
    get_conflict_resolver
)


class TestMergeConflictResolver:
    """Test suite for MergeConflictResolver class."""
    
    @pytest.fixture
    def resolver(self):
        """Create MergeConflictResolver instance."""
        return MergeConflictResolver()
    
    @pytest.fixture
    def temp_repo(self):
        """Create temporary git repository."""
        temp_dir = Path(tempfile.mkdtemp())
        
        # Initialize git repo
        subprocess.run(
            ["git", "init"],
            cwd=temp_dir,
            capture_output=True,
            text=True
        )
        
        # Create initial file and commit
        test_file = temp_dir / "test.txt"
        test_file.write_text("initial content")
        
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
    
    def test_init(self, resolver):
        """Test resolver initialization."""
        assert resolver is not None
    
    @patch('subprocess.run')
    def test_detect_conflicts_no_conflicts(self, mock_run, resolver, temp_repo):
        """Test conflict detection with no conflicts."""
        # Mock successful merge
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = ""
        mock_run.return_value.stderr = ""
        
        has_conflicts, conflict_files = resolver.detect_conflicts(
            temp_repo, "branch1", "main"
        )
        
        assert has_conflicts is False
        assert conflict_files == []
    
    @patch('subprocess.run')
    def test_detect_conflicts_with_conflicts(self, mock_run, resolver, temp_repo):
        """Test conflict detection with conflicts."""
        # Mock merge with conflicts
        mock_run.side_effect = [
            Mock(returncode=0, stdout="", stderr=""),  # checkout
            Mock(
                returncode=1,
                stdout="CONFLICT (content): Merge conflict in file1.py\nCONFLICT (content): Merge conflict in file2.py",
                stderr=""
            ),  # merge attempt
            Mock(returncode=0, stdout="", stderr="")  # abort
        ]
        
        has_conflicts, conflict_files = resolver.detect_conflicts(
            temp_repo, "branch1", "main"
        )
        
        assert has_conflicts is True
        assert "file1.py" in conflict_files or "file2.py" in conflict_files
    
    @patch('subprocess.run')
    def test_resolve_conflicts_theirs(self, mock_run, resolver, temp_repo):
        """Test auto-resolve conflicts using 'theirs' strategy."""
        conflict_files = ["file1.py"]
        
        # Mock successful resolution
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = ""
        
        result = resolver.resolve_conflicts_auto(temp_repo, conflict_files, "theirs")
        
        assert result is True
        assert mock_run.call_count >= len(conflict_files) * 2  # checkout + add
    
    @patch('subprocess.run')
    def test_resolve_conflicts_ours(self, mock_run, resolver, temp_repo):
        """Test auto-resolve conflicts using 'ours' strategy."""
        conflict_files = ["file1.py"]
        
        # Mock successful resolution
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = ""
        
        result = resolver.resolve_conflicts_auto(temp_repo, conflict_files, "ours")
        
        assert result is True
    
    def test_resolve_conflicts_invalid_strategy(self, resolver, temp_repo):
        """Test auto-resolve with invalid strategy."""
        conflict_files = ["file1.py"]
        
        result = resolver.resolve_conflicts_auto(temp_repo, conflict_files, "invalid")
        
        assert result is False
    
    def test_generate_conflict_report(self, resolver, temp_repo):
        """Test conflict report generation."""
        # Create file with conflict markers
        conflict_file = temp_repo / "conflict.txt"
        conflict_file.write_text("""<<<<<<< HEAD
our content
=======
their content
>>>>>>> branch
<<<<<<< HEAD
more our content
=======
more their content
>>>>>>> branch
""")
        
        conflict_files = ["conflict.txt"]
        report = resolver.generate_conflict_report(temp_repo, conflict_files)
        
        assert report["conflict_count"] == 1
        assert "conflict.txt" in report["conflict_files"]
        assert len(report["conflict_details"]) == 1
        assert report["conflict_details"][0]["file"] == "conflict.txt"
        assert report["conflict_details"][0]["total_conflicts"] == 2
    
    def test_generate_conflict_report_missing_file(self, resolver, temp_repo):
        """Test conflict report with missing file."""
        conflict_files = ["nonexistent.txt"]
        report = resolver.generate_conflict_report(temp_repo, conflict_files)
        
        assert report["conflict_count"] == 1
        assert len(report["conflict_details"]) == 0
    
    @patch('subprocess.run')
    def test_merge_with_conflict_resolution_success(self, mock_run, resolver, temp_repo):
        """Test merge with conflict resolution - success case."""
        # Mock successful merge
        mock_run.side_effect = [
            Mock(returncode=0, stdout="", stderr=""),  # checkout
            Mock(returncode=0, stdout="", stderr=""),  # detect conflicts (no conflicts)
            Mock(returncode=0, stdout="", stderr="")   # merge
        ]
        
        success, conflicts, error = resolver.merge_with_conflict_resolution(
            temp_repo, "branch1", "main", "theirs"
        )
        
        assert success is True
        assert conflicts is None
        assert error is None
    
    @patch('subprocess.run')
    def test_merge_with_conflict_resolution_conflicts(self, mock_run, resolver, temp_repo):
        """Test merge with conflict resolution - conflicts detected."""
        # Mock merge with conflicts detected but resolved
        mock_run.side_effect = [
            Mock(returncode=0, stdout="", stderr=""),  # checkout
            Mock(
                returncode=1,
                stdout="CONFLICT: file1.py",
                stderr=""
            ),  # detect conflicts
            Mock(returncode=1, stdout="", stderr=""),  # merge attempt
            Mock(returncode=0, stdout="", stderr=""),  # checkout theirs
            Mock(returncode=0, stdout="", stderr=""),  # add
        ]
        
        # Mock resolve_conflicts_auto to return True
        with patch.object(resolver, 'resolve_conflicts_auto', return_value=True):
            with patch.object(resolver, 'generate_conflict_report') as mock_report:
                mock_report.return_value = {"conflict_count": 1, "conflict_files": ["file1.py"], "conflict_details": []}
                
                success, conflicts, error = resolver.merge_with_conflict_resolution(
                    temp_repo, "branch1", "main", "theirs"
                )
                
                assert success is True
    
    def test_detect_conflicts_exception(self, resolver, temp_repo):
        """Test conflict detection handles exceptions."""
        with patch('subprocess.run', side_effect=Exception("Test error")):
            has_conflicts, conflict_files = resolver.detect_conflicts(
                temp_repo, "branch1", "main"
            )
            
            # Should assume conflicts on error
            assert has_conflicts is True


class TestGlobalFunctions:
    """Test suite for global functions."""
    
    def test_get_conflict_resolver_singleton(self):
        """Test global resolver singleton."""
        with patch('src.core.merge_conflict_resolver._conflict_resolver', None):
            resolver1 = get_conflict_resolver()
            resolver2 = get_conflict_resolver()
            assert resolver1 is resolver2
            assert isinstance(resolver1, MergeConflictResolver)

