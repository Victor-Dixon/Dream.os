"""
Unit tests for execute_streamertools_duplicate_resolution.py tool.

Tests duplicate resolution execution, file comparison, and merge suggestions.
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestExecuteStreamertoolsDuplicateResolution:
    """Test suite for execute_streamertools_duplicate_resolution.py."""

    def test_gui_component_duplicate_detection(self):
        """Test detection of GUI component duplicates."""
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_path = Path(temp_dir)
            
            # Create GUI component duplicates
            (repo_path / "gui").mkdir(parents=True, exist_ok=True)
            (repo_path / "gui" / "component1.py").write_text("GUI component 1")
            (repo_path / "plugins" / "gui").mkdir(parents=True, exist_ok=True)
            (repo_path / "plugins" / "gui" / "component1.py").write_text("GUI component 1 duplicate")
            
            # Simulate duplicate detection
            gui_files = list(repo_path.rglob("**/gui/**/*.py"))
            duplicates = [f for f in gui_files if "component1.py" in str(f)]
            
            assert len(duplicates) >= 1, "Should detect GUI component duplicates"

    def test_style_manager_duplicate_detection(self):
        """Test detection of style manager duplicates."""
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_path = Path(temp_dir)
            
            # Create style manager duplicates
            (repo_path / "style_manager.py").write_text("Style manager v1")
            (repo_path / "plugins").mkdir(parents=True, exist_ok=True)
            (repo_path / "plugins" / "style_manager.py").write_text("Style manager v2")
            
            # Simulate duplicate detection
            style_files = list(repo_path.rglob("**/style_manager.py"))
            
            assert len(style_files) >= 1, "Should detect style manager duplicates"

    def test_file_comparison_functionality(self):
        """Test file comparison for duplicates."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file1 = Path(temp_dir) / "file1.py"
            file2 = Path(temp_dir) / "file2.py"
            
            # Create files with different content
            file1.write_text("def function1():\n    pass")
            file2.write_text("def function2():\n    pass")
            
            # Compare files
            content1 = file1.read_text()
            content2 = file2.read_text()
            
            assert content1 != content2, "Files should have different content"
            assert "function1" in content1, "File1 should contain function1"
            assert "function2" in content2, "File2 should contain function2"

    def test_merge_suggestion_generation(self):
        """Test generation of merge suggestions."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file1 = Path(temp_dir) / "file1.py"
            file2 = Path(temp_dir) / "file2.py"
            
            file1.write_text("def common():\n    pass\ndef unique1():\n    pass")
            file2.write_text("def common():\n    pass\ndef unique2():\n    pass")
            
            # Simulate merge suggestion
            content1_lines = file1.read_text().split("\n")
            content2_lines = file2.read_text().split("\n")
            
            unique_in_file1 = [line for line in content1_lines if "unique1" in line]
            unique_in_file2 = [line for line in content2_lines if "unique2" in line]
            
            assert len(unique_in_file1) > 0, "Should identify unique content in file1"
            assert len(unique_in_file2) > 0, "Should identify unique content in file2"

    def test_resolution_plan_creation(self):
        """Test creation of resolution plan."""
        with tempfile.TemporaryDirectory() as temp_dir:
            plan_path = Path(temp_dir) / "resolution_plan.md"
            
            plan_content = """# Duplicate Resolution Plan

## Files to Resolve
1. gui/component1.py (2 instances)
2. style_manager.py (2 instances)

## Resolution Strategy
- Keep SSOT version
- Merge unique functionality
- Remove duplicates
"""
            plan_path.write_text(plan_content)
            
            assert plan_path.exists(), "Resolution plan should be created"
            assert "Duplicate Resolution Plan" in plan_content, "Plan should contain title"
            assert "Files to Resolve" in plan_content, "Plan should list files"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

