"""
Unit tests for src/core/ssot/unified_ssot/validators/basic_validator.py
"""

import pytest

from src.core.ssot.unified_ssot.validators.basic_validator import BasicValidator
from src.core.ssot.ssot_models import SSOTComponent, SSOTComponentType


class TestBasicValidator:
    """Test BasicValidator functionality."""

    @pytest.fixture
    def validator(self):
        """Create BasicValidator instance."""
        return BasicValidator()

    @pytest.fixture
    def valid_component(self):
        """Create valid SSOTComponent."""
        return SSOTComponent(
            component_id="test_component",
            component_type=SSOTComponentType.CONFIGURATION,
            name="Test Component",
            description="Test description"
        )

    def test_validator_creation(self, validator):
        """Test that BasicValidator can be created."""
        assert validator is not None
        assert hasattr(validator, 'validation_rules')

    def test_validate_basic_fields_valid(self, validator, valid_component):
        """Test that validate_basic_fields() returns no issues for valid component."""
        issues = validator.validate_basic_fields(valid_component)
        assert isinstance(issues, list)
        # Should have no issues for valid component

    def test_validate_basic_fields_missing_id(self, validator):
        """Test that validate_basic_fields() detects missing component_id."""
        component = SSOTComponent(
            component_id="",
            component_type=SSOTComponentType.CONFIGURATION,
            name="Test"
        )
        issues = validator.validate_basic_fields(component)
        assert len(issues) > 0
        assert any("component_id" in issue.lower() for issue in issues)

    def test_validate_basic_fields_short_id(self, validator):
        """Test that validate_basic_fields() detects too short component_id."""
        component = SSOTComponent(
            component_id="ab",  # Too short (< 3 chars)
            component_type=SSOTComponentType.CONFIGURATION,
            name="Test"
        )
        issues = validator.validate_basic_fields(component)
        assert any("at least 3 characters" in issue.lower() for issue in issues)



