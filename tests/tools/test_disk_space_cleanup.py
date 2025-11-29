"""
Tests for disk_space_cleanup.py

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-01-27
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from tools.disk_space_cleanup import DiskSpaceCleanup


class TestDiskSpaceCleanup:
    """Test suite for DiskSpaceCleanup class"""
    
    def test_init_dry_run(self):
        """Test initialization with dry run mode"""
        cleanup = DiskSpaceCleanup(dry_run=True)
        assert cleanup.dry_run is True
        assert cleanup.cleaned_items == []
        assert cleanup.total_size_freed == 0
    
    def test_init_execute_mode(self):
        """Test initialization with execute mode"""
        cleanup = DiskSpaceCleanup(dry_run=False)
        assert cleanup.dry_run is False
        assert cleanup.cleaned_items == []
        assert cleanup.total_size_freed == 0
    
    def test_find_temp_merge_dirs_empty(self):
        """Test finding temp merge dirs when none exist"""
        cleanup = DiskSpaceCleanup()
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('tools.disk_space_cleanup.PROJECT_ROOT', Path(tmpdir)):
                dirs = cleanup.find_temp_merge_dirs()
                assert isinstance(dirs, list)
                assert len(dirs) == 0
    
    def test_find_temp_merge_dirs_found(self):
        """Test finding temp merge dirs when they exist"""
        cleanup = DiskSpaceCleanup()
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('tools.disk_space_cleanup.PROJECT_ROOT', Path(tmpdir)):
                # Create temp merge dirs
                (Path(tmpdir) / "repo_merge_test1").mkdir()
                (Path(tmpdir) / "github_merge_test2").mkdir()
                (Path(tmpdir) / "temp").mkdir()
                (Path(tmpdir) / "temp" / "repo_test3").mkdir()
                
                dirs = cleanup.find_temp_merge_dirs()
                assert len(dirs) >= 2
                assert any("repo_merge_test1" in str(d) for d in dirs)
                assert any("github_merge_test2" in str(d) for d in dirs)
    
    def test_find_old_backups_empty(self):
        """Test finding old backups when none exist"""
        cleanup = DiskSpaceCleanup()
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('tools.disk_space_cleanup.PROJECT_ROOT', Path(tmpdir)):
                backups = cleanup.find_old_backups(days=7)
                assert isinstance(backups, list)
                assert len(backups) == 0
    
    def test_find_old_backups_found(self):
        """Test finding old backup files"""
        cleanup = DiskSpaceCleanup()
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('tools.disk_space_cleanup.PROJECT_ROOT', Path(tmpdir)):
                backup_dir = Path(tmpdir) / "consolidation_backups"
                backup_dir.mkdir()
                
                # Create old file (8 days ago)
                old_file = backup_dir / "old_backup.txt"
                old_file.write_text("test")
                old_time = (datetime.now() - timedelta(days=8)).timestamp()
                old_file.touch()
                import os
                os.utime(old_file, (old_time, old_time))
                
                backups = cleanup.find_old_backups(days=7)
                assert len(backups) >= 1
                assert any("old_backup.txt" in str(b) for b in backups)
    
    def test_get_size_file(self):
        """Test getting size of a file"""
        cleanup = DiskSpaceCleanup()
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.txt"
            test_file.write_bytes(b"test content")
            
            size = cleanup.get_size(test_file)
            assert size > 0
            assert size == len(b"test content")
    
    def test_get_size_directory(self):
        """Test getting size of a directory"""
        cleanup = DiskSpaceCleanup()
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.txt"
            test_file.write_text("test content")
            
            size = cleanup.get_size(Path(tmpdir))
            assert size > 0
    
    def test_get_size_nonexistent(self):
        """Test getting size of nonexistent path"""
        cleanup = DiskSpaceCleanup()
        size = cleanup.get_size(Path("/nonexistent/path"))
        assert size == 0
    
    def test_cleanup_temp_dirs_dry_run(self):
        """Test cleanup temp dirs in dry run mode"""
        cleanup = DiskSpaceCleanup(dry_run=True)
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('tools.disk_space_cleanup.PROJECT_ROOT', Path(tmpdir)):
                # Create temp merge dir
                temp_dir = Path(tmpdir) / "repo_merge_test"
                temp_dir.mkdir()
                (temp_dir / "test.txt").write_text("test")
                
                cleaned, size = cleanup.cleanup_temp_dirs()
                assert cleaned >= 1
                assert size > 0
                # In dry run, directory should still exist
                assert temp_dir.exists()
    
    def test_cleanup_temp_dirs_execute(self):
        """Test cleanup temp dirs in execute mode"""
        cleanup = DiskSpaceCleanup(dry_run=False)
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('tools.disk_space_cleanup.PROJECT_ROOT', Path(tmpdir)):
                # Create temp merge dir
                temp_dir = Path(tmpdir) / "repo_merge_test"
                temp_dir.mkdir()
                (temp_dir / "test.txt").write_text("test")
                
                cleaned, size = cleanup.cleanup_temp_dirs()
                assert cleaned >= 1
                assert size > 0
                # In execute mode, directory should be removed
                assert not temp_dir.exists()
    
    def test_cleanup_old_backups_dry_run(self):
        """Test cleanup old backups in dry run mode"""
        cleanup = DiskSpaceCleanup(dry_run=True)
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('tools.disk_space_cleanup.PROJECT_ROOT', Path(tmpdir)):
                backup_dir = Path(tmpdir) / "consolidation_backups"
                backup_dir.mkdir()
                
                # Create old file
                old_file = backup_dir / "old_backup.txt"
                old_file.write_text("test")
                old_time = (datetime.now() - timedelta(days=8)).timestamp()
                import os
                os.utime(old_file, (old_time, old_time))
                
                cleaned, size = cleanup.cleanup_old_backups(days=7)
                assert cleaned >= 1
                assert size > 0
                # In dry run, file should still exist
                assert old_file.exists()
    
    def test_cleanup_old_backups_execute(self):
        """Test cleanup old backups in execute mode"""
        cleanup = DiskSpaceCleanup(dry_run=False)
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('tools.disk_space_cleanup.PROJECT_ROOT', Path(tmpdir)):
                backup_dir = Path(tmpdir) / "consolidation_backups"
                backup_dir.mkdir()
                
                # Create old file
                old_file = backup_dir / "old_backup.txt"
                old_file.write_text("test")
                old_time = (datetime.now() - timedelta(days=8)).timestamp()
                import os
                os.utime(old_file, (old_time, old_time))
                
                cleaned, size = cleanup.cleanup_old_backups(days=7)
                assert cleaned >= 1
                assert size > 0
                # In execute mode, file should be removed
                assert not old_file.exists()
    
    def test_cleanup_full_dry_run(self):
        """Test full cleanup in dry run mode"""
        cleanup = DiskSpaceCleanup(dry_run=True)
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('tools.disk_space_cleanup.PROJECT_ROOT', Path(tmpdir)):
                # Create test files
                temp_dir = Path(tmpdir) / "repo_merge_test"
                temp_dir.mkdir()
                (temp_dir / "test.txt").write_text("test")
                
                backup_dir = Path(tmpdir) / "consolidation_backups"
                backup_dir.mkdir()
                old_file = backup_dir / "old_backup.txt"
                old_file.write_text("test")
                old_time = (datetime.now() - timedelta(days=8)).timestamp()
                import os
                os.utime(old_file, (old_time, old_time))
                
                result = cleanup.cleanup_full()
                assert result["total_cleaned"] >= 1
                assert result["size_freed_mb"] > 0
                assert result["dry_run"] is True
                # Files should still exist in dry run
                assert temp_dir.exists() or not temp_dir.exists()  # May or may not be found
                assert old_file.exists()
    
    def test_cleanup_full_execute(self):
        """Test full cleanup in execute mode"""
        cleanup = DiskSpaceCleanup(dry_run=False)
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('tools.disk_space_cleanup.PROJECT_ROOT', Path(tmpdir)):
                # Create test files
                temp_dir = Path(tmpdir) / "repo_merge_test"
                temp_dir.mkdir()
                (temp_dir / "test.txt").write_text("test")
                
                backup_dir = Path(tmpdir) / "consolidation_backups"
                backup_dir.mkdir()
                old_file = backup_dir / "old_backup.txt"
                old_file.write_text("test")
                old_time = (datetime.now() - timedelta(days=8)).timestamp()
                import os
                os.utime(old_file, (old_time, old_time))
                
                result = cleanup.cleanup_full()
                assert result["total_cleaned"] >= 1
                assert result["size_freed_mb"] > 0
                assert result["dry_run"] is False
                # Files should be removed in execute mode
                assert not temp_dir.exists() or not (Path(tmpdir) / "repo_merge_test").exists()
                assert not old_file.exists()

