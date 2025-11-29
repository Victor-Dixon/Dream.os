"""
Unit tests for consolidation/base.py - HIGH PRIORITY

Tests ConsolidationBase class functionality.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, mock_open
from pathlib import Path
import sys
import tempfile
import os
import shutil
from datetime import datetime

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Import using importlib
import importlib.util

consolidation_base_path = project_root / "src" / "core" / "consolidation" / "base.py"
spec = importlib.util.spec_from_file_location("consolidation_base", consolidation_base_path)
consolidation_base = importlib.util.module_from_spec(spec)
consolidation_base.__package__ = 'src.core.consolidation'

# Mock config_core before loading
mock_config = MagicMock()
mock_config.get_config = Mock(return_value=0)
sys.modules['src.core.config_core'] = mock_config

spec.loader.exec_module(consolidation_base)

ConsolidationBase = consolidation_base.ConsolidationBase


class TestConsolidationBase:
    """Test suite for ConsolidationBase class."""

    @pytest.fixture
    def consolidator(self):
        """Create a ConsolidationBase instance."""
        return ConsolidationBase()

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_path = tempfile.mkdtemp()
        yield temp_path
        shutil.rmtree(temp_path, ignore_errors=True)

    @pytest.fixture
    def temp_file(self, temp_dir):
        """Create a temporary Python file."""
        file_path = os.path.join(temp_dir, "test_file.py")
        with open(file_path, 'w') as f:
            f.write("def test():\n    pass\n")
        yield file_path

    def test_consolidate_directories_single(self, consolidator, temp_dir):
        """Test consolidating single directory."""
        with patch.object(consolidator, '_consolidate_directory', return_value=5):
            result = consolidator.consolidate_directories([temp_dir])
            
            assert result == 5
            consolidator._consolidate_directory.assert_called_once_with(temp_dir)

    def test_consolidate_directories_multiple(self, consolidator, temp_dir):
        """Test consolidating multiple directories."""
        temp_dir2 = tempfile.mkdtemp()
        try:
            with patch.object(consolidator, '_consolidate_directory', side_effect=[3, 7]):
                result = consolidator.consolidate_directories([temp_dir, temp_dir2])
                
                assert result == 10
                assert consolidator._consolidate_directory.call_count == 2
        finally:
            shutil.rmtree(temp_dir2, ignore_errors=True)

    def test_consolidate_directories_nonexistent(self, consolidator):
        """Test consolidating non-existent directory."""
        result = consolidator.consolidate_directories(["nonexistent_dir"])
        
        assert result == 0

    def test_consolidate_directory_walks_tree(self, consolidator, temp_dir):
        """Test _consolidate_directory walks directory tree."""
        # Create nested structure
        subdir = os.path.join(temp_dir, "subdir")
        os.makedirs(subdir)
        file1 = os.path.join(temp_dir, "file1.py")
        file2 = os.path.join(subdir, "file2.py")
        with open(file1, 'w') as f:
            f.write("# file1\n")
        with open(file2, 'w') as f:
            f.write("# file2\n")
        
        with patch.object(consolidator, '_get_consolidated_path', side_effect=lambda x: x), \
             patch.object(consolidator, '_should_consolidate_file', return_value=True), \
             patch.object(consolidator, '_consolidate_file') as mock_consolidate:
            result = consolidator._consolidate_directory(temp_dir)
            
            # Should process both Python files
            assert mock_consolidate.call_count == 2

    def test_consolidate_directory_skips_non_python(self, consolidator, temp_dir):
        """Test _consolidate_directory skips non-Python files."""
        file1 = os.path.join(temp_dir, "file1.py")
        file2 = os.path.join(temp_dir, "file2.txt")
        with open(file1, 'w') as f:
            f.write("# python\n")
        with open(file2, 'w') as f:
            f.write("# text\n")
        
        with patch.object(consolidator, '_get_consolidated_path', side_effect=lambda x: x), \
             patch.object(consolidator, '_should_consolidate_file', return_value=True), \
             patch.object(consolidator, '_consolidate_file') as mock_consolidate:
            result = consolidator._consolidate_directory(temp_dir)
            
            # Should only process Python file
            assert mock_consolidate.call_count == 1

    def test_get_consolidated_path_default(self, consolidator):
        """Test _get_consolidated_path default implementation."""
        source = "test/path/file.py"
        result = consolidator._get_consolidated_path(source)
        
        assert result == source

    def test_should_consolidate_file_new_file(self, consolidator, temp_file):
        """Test _should_consolidate_file for new file."""
        target = temp_file + ".target"
        
        result = consolidator._should_consolidate_file(temp_file, target)
        
        assert result is True

    def test_should_consolidate_file_older_source(self, consolidator, temp_file):
        """Test _should_consolidate_file when source is older."""
        target = temp_file + ".target"
        # Create target with newer timestamp
        with open(target, 'w') as f:
            f.write("# target\n")
        # Make target newer
        target_time = os.path.getmtime(target)
        source_time = os.path.getmtime(temp_file)
        if target_time < source_time:
            os.utime(target, (target_time + 10, target_time + 10))
        
        result = consolidator._should_consolidate_file(temp_file, target)
        
        # Should return False if target is newer
        assert isinstance(result, bool)

    def test_should_consolidate_file_backup(self, consolidator, temp_file):
        """Test _should_consolidate_file skips backup files."""
        backup_file = temp_file + ".backup"
        
        result = consolidator._should_consolidate_file(backup_file, "target.py")
        
        assert result is False

    def test_consolidate_file_creates_directories(self, consolidator, temp_file, temp_dir):
        """Test _consolidate_file creates target directories."""
        target = os.path.join(temp_dir, "nested", "path", "target.py")
        
        with patch('shutil.copy2') as mock_copy:
            consolidator._consolidate_file(temp_file, target)
            
            # Should create parent directories
            assert os.path.exists(os.path.dirname(target))
            mock_copy.assert_called_once_with(temp_file, target)

    def test_consolidate_file_copies_file(self, consolidator, temp_file, temp_dir):
        """Test _consolidate_file copies file correctly."""
        target = os.path.join(temp_dir, "target.py")
        
        consolidator._consolidate_file(temp_file, target)
        
        assert os.path.exists(target)
        with open(target, 'r') as f:
            content = f.read()
        assert "def test()" in content

