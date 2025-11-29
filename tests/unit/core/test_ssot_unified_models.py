"""
Unit tests for src/core/ssot/unified_ssot/models.py
"""

import pytest

from src.core.ssot.unified_ssot.models import (
    SSOTComponent,
    SSOTComponentType,
    SSOTExecutionPhase,
    SSOTIntegrationResult,
    SSOTValidationLevel,
)


class TestSSOTUnifiedModels:
    """Test SSOT unified models (re-exports)."""

    def test_ssot_component_import(self):
        """Test that SSOTComponent can be imported."""
        assert SSOTComponent is not None

    def test_ssot_component_type_import(self):
        """Test that SSOTComponentType can be imported."""
        assert SSOTComponentType is not None

    def test_ssot_execution_phase_import(self):
        """Test that SSOTExecutionPhase can be imported."""
        assert SSOTExecutionPhase is not None

    def test_ssot_integration_result_import(self):
        """Test that SSOTIntegrationResult can be imported."""
        assert SSOTIntegrationResult is not None

    def test_ssot_validation_level_import(self):
        """Test that SSOTValidationLevel can be imported."""
        assert SSOTValidationLevel is not None

    def test_ssot_component_creation(self):
        """Test that SSOTComponent can be created."""
        component = SSOTComponent(
            component_id="test",
            component_type=SSOTComponentType.EXECUTION,
            name="Test Component"
        )
        assert component.component_id == "test"
        assert component.component_type == SSOTComponentType.EXECUTION



