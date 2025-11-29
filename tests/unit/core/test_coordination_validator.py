"""
Unit tests for src/core/validation/coordination_validator.py
"""

import pytest

from src.core.validation.coordination_validator import (
    CoordinationValidator,
    ValidationSeverity,
    ValidationResult,
    ValidationIssue,
)


class TestCoordinationValidator:
    """Test CoordinationValidator functionality."""

    @pytest.fixture
    def validator(self):
        """Create CoordinationValidator instance."""
        return CoordinationValidator()

    def test_validator_creation(self, validator):
        """Test that CoordinationValidator can be created."""
        assert validator is not None
        assert hasattr(validator, 'rules')
        assert hasattr(validator, 'validation_history')

    def test_validation_severity_enum(self):
        """Test ValidationSeverity enum values."""
        assert ValidationSeverity.ERROR.value == "ERROR"
        assert ValidationSeverity.WARNING.value == "WARNING"
        assert ValidationSeverity.INFO.value == "INFO"

    def test_validation_result_enum(self):
        """Test ValidationResult enum values."""
        assert ValidationResult.PASS.value == "PASS"
        assert ValidationResult.FAIL.value == "FAIL"
        assert ValidationResult.WARNING.value == "WARNING"

    def test_validation_issue_creation(self):
        """Test that ValidationIssue can be created."""
        from datetime import datetime
        issue = ValidationIssue(
            rule_id="test_rule",
            rule_name="Test Rule",
            severity=ValidationSeverity.ERROR,
            message="Test message",
            details={},
            timestamp=datetime.now(),
            component="test_component"
        )
        assert issue.rule_id == "test_rule"
        assert issue.severity == ValidationSeverity.ERROR



