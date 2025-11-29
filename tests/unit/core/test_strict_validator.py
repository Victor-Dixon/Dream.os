"""
Unit tests for src/core/ssot/unified_ssot/validators/strict_validator.py
"""

import pytest

from src.core.ssot.unified_ssot.validators.strict_validator import StrictValidator
from src.core.ssot.ssot_models import SSOTComponent, SSOTComponentType


class TestStrictValidator:
    """Test StrictValidator functionality."""

    @pytest.fixture
    def validator(self):
        """Create StrictValidator instance."""
        return StrictValidator()

    @pytest.fixture
    def valid_component(self):
        """Create valid SSOTComponent."""
        return SSOTComponent(
            component_id="test_component",
            component_type=SSOTComponentType.CONFIGURATION,
            name="Test Component"
        )

    def test_validator_creation(self, validator):
        """Test that StrictValidator can be created."""
        assert validator is not None

    def test_validate_component(self, validator, valid_component):
        """Test that validate() method works."""
        result = validator.validate(valid_component)
        assert isinstance(result, (bool, dict, list))



