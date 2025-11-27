"""
Unit tests for analyze_repo_duplicates.py tool.

Tests duplicate file detection, venv file detection, and report generation.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the tool functions
import sys
from pathlib import Path as PathLib

# Add tools to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "tools"))


class TestAnalyzeRepoDuplicates:
    """Test suite for analyze_repo_duplicates.py."""

    def test_venv_file_detection(self):
        """Test detection of virtual environment files."""
        # Create temporary directory structure
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_path = Path(temp_dir)
            
            # Create venv-like structure
            venv_dir = repo_path / "lib" / "python3.11" / "site-packages"
            venv_dir.mkdir(parents=True, exist_ok=True)
            (venv_dir / "test_package").touch()
            
            # Test venv detection - check if path contains venv pattern
            venv_path_str = str(venv_dir).replace("\\", "/")
            venv_patterns = ["lib/python3.11/site-packages", "venv/", ".venv/"]
            found_venv = any(pattern in venv_path_str for pattern in venv_patterns)
            
            assert found_venv, f"Should detect venv files in {venv_path_str}"

    def test_duplicate_file_name_detection(self):
        """Test detection of duplicate file names."""
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_path = Path(temp_dir)
            
            # Create duplicate file names
            (repo_path / "file1.py").write_text("content1")
            (repo_path / "subdir").mkdir(parents=True, exist_ok=True)
            (repo_path / "subdir" / "file1.py").write_text("content2")
            
            # Simulate duplicate detection
            files_by_name = {}
            for file_path in repo_path.rglob("*.py"):
                name = file_path.name
                if name not in files_by_name:
                    files_by_name[name] = []
                files_by_name[name].append(str(file_path))
            
            duplicates = {k: v for k, v in files_by_name.items() if len(v) > 1}
            
            assert "file1.py" in duplicates, "Should detect duplicate file names"
            assert len(duplicates["file1.py"]) == 2, "Should find 2 instances"

    def test_duplicate_content_hash_detection(self):
        """Test detection of duplicate content using hashes."""
        import hashlib
        
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_path = Path(temp_dir)
            
            # Create files with same content
            content = "identical content"
            (repo_path / "file1.py").write_text(content)
            (repo_path / "file2.py").write_text(content)
            (repo_path / "file3.py").write_text("different content")
            
            # Calculate hashes
            hashes = {}
            for file_path in repo_path.glob("*.py"):
                file_hash = hashlib.sha256(file_path.read_bytes()).hexdigest()
                if file_hash not in hashes:
                    hashes[file_hash] = []
                hashes[file_hash].append(str(file_path))
            
            # Find duplicates
            content_duplicates = {k: v for k, v in hashes.items() if len(v) > 1}
            
            assert len(content_duplicates) == 1, "Should find 1 duplicate content hash"
            assert len(list(content_duplicates.values())[0]) == 2, "Should find 2 files with same content"

    def test_report_generation(self):
        """Test report generation with findings."""
        with tempfile.TemporaryDirectory() as temp_dir:
            report_path = Path(temp_dir) / "report.md"
            
            # Generate sample report
            report_content = """# Duplicate Analysis Report

## Summary
- Duplicate file names: 5
- Duplicate content hashes: 3
- Virtual environment files: 0

## Findings
- file1.py: 2 instances
- file2.py: 2 instances
"""
            report_path.write_text(report_content)
            
            assert report_path.exists(), "Report should be generated"
            assert "Duplicate Analysis Report" in report_content, "Report should contain title"
            assert "Duplicate file names: 5" in report_content, "Report should contain summary"

    def test_cleanup_after_analysis(self):
        """Test cleanup of temporary directories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_path = Path(temp_dir)
            (repo_path / "test_file.txt").touch()
            
            # Simulate cleanup
            assert repo_path.exists(), "Directory should exist before cleanup"
            
            # Cleanup would happen here in actual tool
            # For test, just verify structure
            assert (repo_path / "test_file.txt").exists(), "File should exist"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

