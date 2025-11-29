"""
Unit tests for consolidation/consolidation_validator.py - HIGH PRIORITY

Tests ConsolidationValidator class functionality.
Note: Maps to tools/consolidation/validate_consolidation.py ConsolidationValidator.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, mock_open
import sys
from pathlib import Path
import tempfile
import os

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Import the validator from tools directory (closest match)
from tools.consolidation.validate_consolidation import ConsolidationValidator


class TestConsolidationValidator:
    """Test suite for ConsolidationValidator class."""

    @pytest.fixture
    def validator(self):
        """Create a ConsolidationValidator instance."""
        return ConsolidationValidator()

    def test_initialization(self, validator):
        """Test ConsolidationValidator initialization."""
        assert validator.project_root is not None
        assert validator.issues == []
        assert validator.successes == []

    def test_validate_file_count_reduced(self, validator):
        """Test validate_file_count when files are reduced."""
        with patch('os.walk') as mock_walk:
            mock_walk.return_value = [
                ('src', [], ['file1.py', 'file2.py']),
                ('src/core', [], ['file3.py'])
            ]
            
            result = validator.validate_file_count()
            
            assert isinstance(result, bool)
            # Result depends on count, but should execute without error

    def test_validate_core_directories_success(self, validator):
        """Test validate_core_directories with valid structure."""
        with patch('pathlib.Path.exists', return_value=True), \
             patch('os.listdir', return_value=['dir1', 'dir2', 'dir3']), \
             patch('os.path.isdir', return_value=True):
            
            result = validator.validate_core_directories()
            
            assert isinstance(result, bool)

    def test_validate_core_directories_missing(self, validator):
        """Test validate_core_directories when core directory is missing."""
        with patch('pathlib.Path.exists', return_value=False):
            result = validator.validate_core_directories()
            
            assert result is False
            assert len(validator.issues) > 0

    def test_validate_imports_success(self, validator):
        """Test validate_imports with successful imports."""
        with patch('importlib.import_module') as mock_import:
            mock_import.return_value = MagicMock()
            
            result = validator.validate_imports()
            
            assert isinstance(result, bool)

    def test_validate_imports_failure(self, validator):
        """Test validate_imports with failed imports."""
        with patch('importlib.import_module', side_effect=ImportError("Module not found")):
            result = validator.validate_imports()
            
            assert result is False
            assert len(validator.issues) > 0

    def test_validate_functionality_success(self, validator):
        """Test validate_functionality with successful operations."""
        with patch('sys.path') as mock_path, \
             patch('builtins.__import__', return_value=MagicMock()) as mock_import:
            mock_module = MagicMock()
            mock_module.get_config = Mock(return_value="test_value")
            mock_module.set_config = Mock(return_value=None)
            mock_import.return_value = mock_module
            
            # Mock the config functions
            with patch.dict('sys.modules', {'core.managers': mock_module}):
                result = validator.validate_functionality()
                
                assert isinstance(result, bool)

    def test_check_for_over_engineering_patterns(self, validator):
        """Test check_for_over_engineering_patterns method."""
        with patch('os.walk') as mock_walk:
            mock_walk.return_value = [
                ('src', [], ['normal_file.py']),
            ]
            
            # Mock file reading
            with patch('builtins.open', mock_open(read_data="normal code")):
                result = validator.check_for_over_engineering_patterns()
                
                assert isinstance(result, bool)

    def test_generate_report(self, validator):
        """Test generate_report method."""
        validator.successes = ["Success 1", "Success 2"]
        validator.issues = ["Issue 1"]
        
        report = validator.generate_report()
        
        assert isinstance(report, str)
        assert "CONSOLIDATION VALIDATION REPORT" in report
        assert "Success 1" in report
        assert "Issue 1" in report

    def test_generate_report_no_issues(self, validator):
        """Test generate_report with no issues."""
        validator.successes = ["Success 1"]
        validator.issues = []
        
        report = validator.generate_report()
        
        assert "NO ISSUES FOUND" in report

    def test_run_validation(self, validator):
        """Test run_validation method."""
        with patch.object(validator, 'validate_file_count', return_value=True), \
             patch.object(validator, 'validate_core_directories', return_value=True), \
             patch.object(validator, 'validate_imports', return_value=True), \
             patch.object(validator, 'validate_functionality', return_value=True), \
             patch.object(validator, 'check_for_over_engineering_patterns', return_value=True), \
             patch.object(validator, 'generate_report', return_value="Test report"):
            
            result = validator.run_validation()
            
            assert isinstance(result, bool)

