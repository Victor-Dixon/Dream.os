"""
Unit tests for refactoring/refactoring_executor.py - HIGH PRIORITY

Tests RefactoringExecutor class functionality.
Note: Maps to tools/toolbelt/executors/refactor_executor.py RefactorExecutor.
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
from tools.toolbelt.executors.refactor_executor import RefactorExecutor


class TestRefactoringExecutor:
    """Test suite for RefactoringExecutor class."""

    @pytest.fixture
    def executor(self):
        """Create a RefactoringExecutor instance (static methods)."""
        return RefactorExecutor

    @pytest.fixture
    def args_split(self, tmp_path):
        """Create args for split action."""
        file_path = tmp_path / "large.py"
        file_path.write_text("class Class1:\n    pass\nclass Class2:\n    pass")
        
        args = MagicMock()
        args.refactor_action = "split"
        args.file = str(file_path)
        args.strategy = "auto"
        args.max_classes = 1
        return args

    @pytest.fixture
    def args_facade(self, tmp_path):
        """Create args for facade action."""
        args = MagicMock()
        args.refactor_action = "facade"
        args.directory = str(tmp_path)
        return args

    @pytest.fixture
    def args_extract(self, tmp_path):
        """Create args for extract action."""
        source_file = tmp_path / "source.py"
        source_file.write_text("class Class1:\n    pass\nclass Class2:\n    pass")
        
        args = MagicMock()
        args.refactor_action = "extract"
        args.source_file = str(source_file)
        args.class_names = ["Class1"]
        args.target = None
        return args

    def test_execute_split(self, executor, args_split):
        """Test execute with split action."""
        result = executor.execute(args_split)
        
        assert result == 0

    def test_execute_facade(self, executor, args_facade):
        """Test execute with facade action."""
        result = executor.execute(args_facade)
        
        assert result == 0

    def test_execute_extract(self, executor, args_extract):
        """Test execute with extract action."""
        result = executor.execute(args_extract)
        
        assert result == 0

    def test_execute_unknown_action(self, executor):
        """Test execute with unknown action."""
        args = MagicMock()
        args.refactor_action = "unknown"
        
        result = executor.execute(args)
        
        assert result == 1

    def test_split_file_compliant(self, executor, tmp_path):
        """Test _split_file with compliant file."""
        file_path = tmp_path / "small.py"
        file_path.write_text("class Class1:\n    pass")
        
        args = MagicMock()
        args.file = str(file_path)
        args.strategy = "auto"
        args.max_classes = 5
        
        result = executor._split_file(args)
        
        assert result == 0

    def test_split_file_violation(self, executor, tmp_path):
        """Test _split_file with violation."""
        file_path = tmp_path / "large.py"
        content = "\n".join([f"class Class{i}:\n    pass" for i in range(10)])
        file_path.write_text(content)
        
        args = MagicMock()
        args.file = str(file_path)
        args.strategy = "auto"
        args.max_classes = 3
        
        result = executor._split_file(args)
        
        assert result == 0

    def test_split_file_nonexistent(self, executor):
        """Test _split_file with nonexistent file."""
        args = MagicMock()
        args.file = "nonexistent.py"
        args.strategy = "auto"
        args.max_classes = 5
        
        result = executor._split_file(args)
        
        assert result == 1

    def test_auto_group_classes(self, executor):
        """Test _auto_group_classes method."""
        classes = ["Manager1", "Model1", "Handler1", "Exception1", "Other"]
        
        groups = executor._auto_group_classes(classes)
        
        assert isinstance(groups, dict)
        assert "managers" in groups
        assert "models" in groups

    def test_apply_facade_existing(self, executor, tmp_path):
        """Test _apply_facade with existing directory."""
        file1 = tmp_path / "module1.py"
        file2 = tmp_path / "module2.py"
        file1.write_text("content")
        file2.write_text("content")
        
        args = MagicMock()
        args.directory = str(tmp_path)
        
        result = executor._apply_facade(args)
        
        assert result == 0

    def test_apply_facade_nonexistent(self, executor):
        """Test _apply_facade with nonexistent directory."""
        args = MagicMock()
        args.directory = "nonexistent"
        
        result = executor._apply_facade(args)
        
        assert result == 1

    def test_extract_classes_success(self, executor, tmp_path):
        """Test _extract_classes with existing classes."""
        source_file = tmp_path / "source.py"
        source_file.write_text("class Class1:\n    pass\nclass Class2:\n    pass")
        
        args = MagicMock()
        args.source_file = str(source_file)
        args.class_names = ["Class1", "Class2"]
        args.target = None
        
        result = executor._extract_classes(args)
        
        assert result == 0

    def test_extract_classes_missing(self, executor, tmp_path):
        """Test _extract_classes with missing classes."""
        source_file = tmp_path / "source.py"
        source_file.write_text("class Class1:\n    pass")
        
        args = MagicMock()
        args.source_file = str(source_file)
        args.class_names = ["Class1", "ClassNotFound"]
        args.target = None
        
        result = executor._extract_classes(args)
        
        assert result == 1

    def test_extract_classes_source_missing(self, executor):
        """Test _extract_classes with missing source file."""
        args = MagicMock()
        args.source_file = "nonexistent.py"
        args.class_names = ["Class1"]
        args.target = None
        
        result = executor._extract_classes(args)
        
        assert result == 1

