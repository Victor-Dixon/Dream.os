"""
Unit tests for consolidation/consolidation_executor.py - HIGH PRIORITY

Tests ConsolidationExecutor class functionality.
Note: Maps to tools/toolbelt/executors/consolidation_executor.py ConsolidationExecutor.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import sys
from pathlib import Path
import tempfile

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Import the executor
from tools.toolbelt.executors.consolidation_executor import ConsolidationExecutor


class TestConsolidationExecutor:
    """Test suite for ConsolidationExecutor class."""

    @pytest.fixture
    def executor(self):
        """Create a ConsolidationExecutor instance (static methods)."""
        return ConsolidationExecutor

    @pytest.fixture
    def args_find_duplicates(self):
        """Create args for find-duplicates action."""
        args = MagicMock()
        args.consol_action = "find-duplicates"
        args.path = str(tempfile.mkdtemp())
        args.type = "files"
        return args

    @pytest.fixture
    def args_suggest(self):
        """Create args for suggest action."""
        args = MagicMock()
        args.consol_action = "suggest"
        args.path = str(tempfile.mkdtemp())
        args.min_similarity = 0.8
        return args

    @pytest.fixture
    def args_verify(self, tmp_path):
        """Create args for verify action."""
        source_file = tmp_path / "source.py"
        source_file.write_text("def func(): pass")
        
        args = MagicMock()
        args.consol_action = "verify"
        args.source_file = str(source_file)
        args.target_file = str(tmp_path / "target.py")
        return args

    def test_execute_find_duplicates(self, executor, args_find_duplicates):
        """Test execute with find-duplicates action."""
        result = executor.execute(args_find_duplicates)
        
        assert result == 0

    def test_execute_suggest(self, executor, args_suggest):
        """Test execute with suggest action."""
        result = executor.execute(args_suggest)
        
        assert result == 0

    def test_execute_verify(self, executor, args_verify):
        """Test execute with verify action."""
        result = executor.execute(args_verify)
        
        assert result == 0

    def test_execute_unknown_action(self, executor):
        """Test execute with unknown action."""
        args = MagicMock()
        args.consol_action = "unknown"
        
        result = executor.execute(args)
        
        assert result == 1

    def test_find_duplicates_files(self, executor, tmp_path):
        """Test _find_duplicates for files."""
        # Create duplicate files
        file1 = tmp_path / "duplicate.py"
        file2 = tmp_path / "duplicate.py"
        file1.write_text("content")
        if tmp_path / "duplicate.py" != file2:
            file2.write_text("content")
        
        args = MagicMock()
        args.path = str(tmp_path)
        args.type = "files"
        
        result = executor._find_duplicates(args)
        
        assert result == 0

    def test_find_duplicates_classes(self, executor, tmp_path):
        """Test _find_duplicates for classes."""
        file1 = tmp_path / "file1.py"
        file2 = tmp_path / "file2.py"
        file1.write_text("class TestClass:\n    pass")
        file2.write_text("class TestClass:\n    pass")
        
        args = MagicMock()
        args.path = str(tmp_path)
        args.type = "classes"
        
        result = executor._find_duplicates(args)
        
        assert result == 0

    def test_find_duplicates_no_duplicates(self, executor, tmp_path):
        """Test _find_duplicates with no duplicates."""
        file1 = tmp_path / "file1.py"
        file2 = tmp_path / "file2.py"
        file1.write_text("class Class1: pass")
        file2.write_text("class Class2: pass")
        
        args = MagicMock()
        args.path = str(tmp_path)
        args.type = "classes"
        
        result = executor._find_duplicates(args)
        
        assert result == 0

    def test_suggest_consolidation(self, executor, tmp_path):
        """Test _suggest_consolidation method."""
        args = MagicMock()
        args.path = str(tmp_path)
        args.min_similarity = 0.8
        
        result = executor._suggest_consolidation(args)
        
        assert result == 0

    def test_suggest_consolidation_with_files(self, executor, tmp_path):
        """Test _suggest_consolidation with similar files."""
        file1 = tmp_path / "test_v1.py"
        file2 = tmp_path / "test_v2.py"
        file1.write_text("content")
        file2.write_text("content")
        
        args = MagicMock()
        args.path = str(tmp_path)
        args.min_similarity = 0.8
        
        result = executor._suggest_consolidation(args)
        
        assert result == 0

    def test_verify_consolidation_success(self, executor, tmp_path):
        """Test _verify_consolidation with existing files."""
        source = tmp_path / "source.py"
        target = tmp_path / "target.py"
        source.write_text("content")
        
        args = MagicMock()
        args.source_file = str(source)
        args.target_file = str(target)
        
        result = executor._verify_consolidation(args)
        
        assert result == 0

    def test_verify_consolidation_source_missing(self, executor, tmp_path):
        """Test _verify_consolidation with missing source."""
        args = MagicMock()
        args.source_file = str(tmp_path / "nonexistent.py")
        args.target_file = str(tmp_path / "target.py")
        
        result = executor._verify_consolidation(args)
        
        assert result == 1

    def test_verify_consolidation_target_missing(self, executor, tmp_path):
        """Test _verify_consolidation with missing target."""
        source = tmp_path / "source.py"
        source.write_text("content")
        
        args = MagicMock()
        args.source_file = str(source)
        args.target_file = str(tmp_path / "target.py")
        
        result = executor._verify_consolidation(args)
        
        # Should return 0 (target missing is acceptable)
        assert result == 0

