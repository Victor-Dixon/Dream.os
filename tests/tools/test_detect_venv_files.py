#!/usr/bin/env python3
"""
Tests for detect_venv_files.py

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

from detect_venv_files import detect_venv_files, VENV_PATTERNS


def test_detect_venv_files_finds_venv():
    """Test that venv directory is detected."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create venv directory
        venv_dir = os.path.join(tmpdir, "venv")
        os.makedirs(venv_dir)
        
        findings = detect_venv_files(tmpdir)
        
        assert len(findings['venv/']) > 0, "Should detect venv directory"


def test_detect_venv_files_finds_site_packages():
    """Test that site-packages is detected."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create site-packages directory
        site_packages = os.path.join(tmpdir, "lib", "python3.11", "site-packages")
        os.makedirs(site_packages)
        
        findings = detect_venv_files(tmpdir)
        
        # Check if any pattern matched (the tool finds paths containing the pattern)
        found = False
        for pattern, paths in findings.items():
            if 'site-packages' in pattern or any('site-packages' in p for p in paths):
                found = True
                break
        
        assert found, "Should detect site-packages"


def test_detect_venv_files_skips_git():
    """Test that .git directories are skipped."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create .git directory
        git_dir = os.path.join(tmpdir, ".git")
        os.makedirs(git_dir)
        
        # Create venv inside .git (should be skipped)
        venv_in_git = os.path.join(git_dir, "venv")
        os.makedirs(venv_in_git)
        
        findings = detect_venv_files(tmpdir)
        
        # Should not find venv inside .git
        assert len(findings['venv/']) == 0, "Should skip .git directories"


def test_detect_venv_files_finds_pycache():
    """Test that __pycache__ is detected."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create __pycache__ directory
        pycache = os.path.join(tmpdir, "__pycache__")
        os.makedirs(pycache)
        
        findings = detect_venv_files(tmpdir)
        
        assert len(findings['__pycache__/']) > 0, "Should detect __pycache__"


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])

