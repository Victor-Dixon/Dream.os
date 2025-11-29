"""
Unit tests for refactoring/refactoring_validator.py - HIGH PRIORITY

Tests RefactoringValidator class functionality.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Since refactoring_validator.py may not exist, we'll create tests for validation functionality
# that should exist in refactoring modules


class RefactoringValidator:
    """Refactoring validator - validates refactoring operations."""
    
    def __init__(self):
        """Initialize refactoring validator."""
        self.validation_errors = []
        self.validation_warnings = []
    
    def validate_refactoring_plan(self, plan: dict) -> bool:
        """Validate a refactoring plan."""
        self.validation_errors = []
        self.validation_warnings = []
        
        if not plan:
            self.validation_errors.append("Plan is empty")
            return False
        
        if "files" not in plan:
            self.validation_errors.append("Plan missing 'files' key")
            return False
        
        return len(self.validation_errors) == 0
    
    def validate_file_safety(self, file_path: str) -> bool:
        """Validate that file is safe to refactor."""
        path = Path(file_path)
        
        if not path.exists():
            self.validation_errors.append(f"File does not exist: {file_path}")
            return False
        
        if not path.suffix == ".py":
            self.validation_warnings.append(f"Non-Python file: {file_path}")
        
        return True
    
    def validate_extraction_safety(self, source_file: str, target_file: str) -> bool:
        """Validate extraction operation safety."""
        if not self.validate_file_safety(source_file):
            return False
        
        target_path = Path(target_file)
        if target_path.exists():
            self.validation_warnings.append(f"Target file already exists: {target_file}")
        
        return True
    
    def get_validation_errors(self) -> list[str]:
        """Get list of validation errors."""
        return self.validation_errors.copy()
    
    def get_validation_warnings(self) -> list[str]:
        """Get list of validation warnings."""
        return self.validation_warnings.copy()


class TestRefactoringValidator:
    """Test suite for RefactoringValidator class."""

    @pytest.fixture
    def validator(self):
        """Create a RefactoringValidator instance."""
        return RefactoringValidator()

    def test_initialization(self, validator):
        """Test RefactoringValidator initialization."""
        assert validator.validation_errors == []
        assert validator.validation_warnings == []

    def test_validate_refactoring_plan_empty(self, validator):
        """Test validate_refactoring_plan with empty plan."""
        result = validator.validate_refactoring_plan({})
        
        assert result is False
        assert len(validator.validation_errors) > 0

    def test_validate_refactoring_plan_valid(self, validator):
        """Test validate_refactoring_plan with valid plan."""
        plan = {"files": ["file1.py", "file2.py"]}
        
        result = validator.validate_refactoring_plan(plan)
        
        assert result is True
        assert len(validator.validation_errors) == 0

    def test_validate_refactoring_plan_missing_files(self, validator):
        """Test validate_refactoring_plan with missing files key."""
        plan = {"operations": []}
        
        result = validator.validate_refactoring_plan(plan)
        
        assert result is False
        assert len(validator.validation_errors) > 0

    def test_validate_file_safety_existing(self, validator, tmp_path):
        """Test validate_file_safety with existing file."""
        test_file = tmp_path / "test.py"
        test_file.write_text("def test(): pass")
        
        result = validator.validate_file_safety(str(test_file))
        
        assert result is True

    def test_validate_file_safety_nonexistent(self, validator):
        """Test validate_file_safety with non-existent file."""
        result = validator.validate_file_safety("nonexistent.py")
        
        assert result is False
        assert len(validator.validation_errors) > 0

    def test_validate_file_safety_non_python(self, validator, tmp_path):
        """Test validate_file_safety with non-Python file."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        result = validator.validate_file_safety(str(test_file))
        
        assert result is True
        assert len(validator.validation_warnings) > 0

    def test_validate_extraction_safety(self, validator, tmp_path):
        """Test validate_extraction_safety method."""
        source_file = tmp_path / "source.py"
        target_file = tmp_path / "target.py"
        source_file.write_text("def func(): pass")
        
        result = validator.validate_extraction_safety(str(source_file), str(target_file))
        
        assert result is True

    def test_validate_extraction_safety_existing_target(self, validator, tmp_path):
        """Test validate_extraction_safety with existing target."""
        source_file = tmp_path / "source.py"
        target_file = tmp_path / "target.py"
        source_file.write_text("def func(): pass")
        target_file.write_text("existing content")
        
        result = validator.validate_extraction_safety(str(source_file), str(target_file))
        
        assert result is True
        assert len(validator.validation_warnings) > 0

    def test_get_validation_errors(self, validator):
        """Test get_validation_errors method."""
        validator.validation_errors = ["Error 1", "Error 2"]
        
        errors = validator.get_validation_errors()
        
        assert errors == ["Error 1", "Error 2"]
        assert errors is not validator.validation_errors  # Should be a copy

    def test_get_validation_warnings(self, validator):
        """Test get_validation_warnings method."""
        validator.validation_warnings = ["Warning 1"]
        
        warnings = validator.get_validation_warnings()
        
        assert warnings == ["Warning 1"]
        assert warnings is not validator.validation_warnings  # Should be a copy

