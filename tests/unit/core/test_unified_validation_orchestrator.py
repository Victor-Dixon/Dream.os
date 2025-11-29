"""
Unit tests for src/core/validation/unified_validation_orchestrator.py
"""

import pytest

from src.core.validation.unified_validation_orchestrator import (
    UnifiedValidationOrchestrator,
)


class TestUnifiedValidationOrchestrator:
    """Test UnifiedValidationOrchestrator functionality."""

    @pytest.fixture
    def orchestrator(self):
        """Create UnifiedValidationOrchestrator instance."""
        return UnifiedValidationOrchestrator()

    def test_orchestrator_creation(self, orchestrator):
        """Test that UnifiedValidationOrchestrator can be created."""
        assert orchestrator is not None

    def test_orchestrator_has_validate_method(self, orchestrator):
        """Test that orchestrator has validate() method."""
        assert hasattr(orchestrator, 'validate') or hasattr(orchestrator, 'validate_data')



