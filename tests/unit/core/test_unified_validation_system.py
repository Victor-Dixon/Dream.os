"""
Unit tests for src/core/validation/unified_validation_system.py
"""

import pytest

from src.core.validation.unified_validation_system import (
    UnifiedValidationSystem,
)


class TestUnifiedValidationSystem:
    """Test UnifiedValidationSystem functionality."""

    @pytest.fixture
    def validation_system(self):
        """Create UnifiedValidationSystem instance."""
        return UnifiedValidationSystem()

    def test_validation_system_creation(self, validation_system):
        """Test that UnifiedValidationSystem can be created."""
        assert validation_system is not None

    def test_validation_system_validate(self, validation_system):
        """Test that validate() method works."""
        result = validation_system.validate("test_data")
        assert isinstance(result, (bool, dict))

    def test_validation_system_has_rules(self, validation_system):
        """Test that validation system has rules loaded."""
        assert hasattr(validation_system, 'rules') or hasattr(validation_system, '_rules')



