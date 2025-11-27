#!/usr/bin/env python3
"""
Tests for detect_duplicate_files.py

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-11-26
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add tools to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "tools"))

from detect_duplicate_files import (
    detect_duplicate_files,
    detect_duplicate_names,
    calculate_file_hash
)


def test_calculate_file_hash():
    """Test file hash calculation."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("test content")
        temp_path = f.name
    
    try:
        hash1 = calculate_file_hash(temp_path)
        hash2 = calculate_file_hash(temp_path)
        
        assert hash1 == hash2, "Same file should have same hash"
        assert hash1 is not None, "Hash should not be None"
    finally:
        os.unlink(temp_path)


def test_detect_duplicate_files_finds_duplicates():
    """Test that duplicate files are detected."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create two identical files
        file1 = os.path.join(tmpdir, "file1.txt")
        file2 = os.path.join(tmpdir, "file2.txt")
        
        with open(file1, 'w') as f:
            f.write("identical content")
        with open(file2, 'w') as f:
            f.write("identical content")
        
        duplicates = detect_duplicate_files(tmpdir)
        
        assert len(duplicates) > 0, "Should detect duplicate files"


def test_detect_duplicate_names_finds_duplicate_names():
    """Test that duplicate filenames are detected."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create files with same name in different directories
        dir1 = os.path.join(tmpdir, "dir1")
        dir2 = os.path.join(tmpdir, "dir2")
        os.makedirs(dir1)
        os.makedirs(dir2)
        
        file1 = os.path.join(dir1, "same_name.txt")
        file2 = os.path.join(dir2, "same_name.txt")
        
        with open(file1, 'w') as f:
            f.write("content1")
        with open(file2, 'w') as f:
            f.write("content2")
        
        duplicates = detect_duplicate_names(tmpdir)
        
        assert "same_name.txt" in duplicates, "Should detect duplicate filenames"
        assert len(duplicates["same_name.txt"]) == 2, "Should find 2 files with same name"


def test_detect_duplicate_files_skips_git():
    """Test that .git directories are skipped."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create .git directory
        git_dir = os.path.join(tmpdir, ".git")
        os.makedirs(git_dir)
        
        # Create duplicate files inside .git (should be skipped)
        file1 = os.path.join(git_dir, "file1.txt")
        file2 = os.path.join(git_dir, "file2.txt")
        
        with open(file1, 'w') as f:
            f.write("content")
        with open(file2, 'w') as f:
            f.write("content")
        
        duplicates = detect_duplicate_files(tmpdir)
        
        # Should not find duplicates inside .git
        assert len(duplicates) == 0, "Should skip .git directories"


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])

