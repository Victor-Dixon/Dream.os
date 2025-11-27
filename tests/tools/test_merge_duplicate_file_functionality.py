"""
Tests for merge_duplicate_file_functionality.py - Agent-3
"""

import pytest
import tempfile
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from tools.merge_duplicate_file_functionality import (
    read_file_lines,
    analyze_differences,
    generate_merge_suggestion
)


def test_read_file_lines_existing_file():
    """Test reading an existing file."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as f:
        f.write("def test():\n    pass\n")
        temp_path = Path(f.name)
    
    try:
        lines = read_file_lines(temp_path)
        assert len(lines) == 2
        assert "def test():" in lines[0]
    finally:
        temp_path.unlink()


def test_read_file_lines_nonexistent_file():
    """Test reading a non-existent file."""
    lines = read_file_lines(Path("/nonexistent/file.py"))
    assert lines == []


def test_analyze_differences_identical_files():
    """Test analyzing identical files."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as f1:
        f1.write("def test():\n    pass\n")
        temp_path1 = Path(f1.name)
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as f2:
        f2.write("def test():\n    pass\n")
        temp_path2 = Path(f2.name)
    
    try:
        result = analyze_differences(temp_path1, temp_path2)
        assert result['identical'] is True
        assert result['similarity'] == 1.0
    finally:
        temp_path1.unlink()
        temp_path2.unlink()


def test_analyze_differences_different_files():
    """Test analyzing different files."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as f1:
        f1.write("def test1():\n    pass\n")
        temp_path1 = Path(f1.name)
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as f2:
        f2.write("def test2():\n    return True\n")
        temp_path2 = Path(f2.name)
    
    try:
        result = analyze_differences(temp_path1, temp_path2)
        assert result['identical'] is False
        assert result['similarity'] < 1.0
        assert 'recommendation' in result
    finally:
        temp_path1.unlink()
        temp_path2.unlink()


def test_generate_merge_suggestion():
    """Test generating merge suggestion."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as f1:
        f1.write("def test1():\n    pass\n")
        temp_path1 = Path(f1.name)
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as f2:
        f2.write("def test2():\n    return True\n")
        temp_path2 = Path(f2.name)
    
    ssot = temp_path1
    
    try:
        report = generate_merge_suggestion(temp_path1, temp_path2, ssot)
        assert "Merge Analysis" in report
        assert "Files Compared" in report
        assert "Analysis Results" in report
        assert "Recommendation" in report
    finally:
        temp_path1.unlink()
        temp_path2.unlink()

