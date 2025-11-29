"""
Unit tests for src/core/ssot/unified_ssot/enums.py
"""

import pytest

from src.core.ssot.unified_ssot.enums import (
    SSOTExecutionPhase,
    SSOTValidationLevel,
    SSOTComponentType,
    SSOTStatus,
    SSOTPriority,
)


class TestSSOTEnums:
    """Test SSOT enum classes."""

    def test_ssot_execution_phase_enum(self):
        """Test SSOTExecutionPhase enum values."""
        assert SSOTExecutionPhase.INITIALIZATION.value == "initialization"
        assert SSOTExecutionPhase.VALIDATION.value == "validation"
        assert SSOTExecutionPhase.EXECUTION.value == "execution"
        assert SSOTExecutionPhase.VERIFICATION.value == "verification"
        assert SSOTExecutionPhase.COMPLETION.value == "completion"
        assert SSOTExecutionPhase.ERROR.value == "error"

    def test_ssot_validation_level_enum(self):
        """Test SSOTValidationLevel enum values."""
        assert SSOTValidationLevel.BASIC.value == "basic"
        assert SSOTValidationLevel.STANDARD.value == "standard"
        assert SSOTValidationLevel.STRICT.value == "strict"
        assert SSOTValidationLevel.CRITICAL.value == "critical"

    def test_ssot_component_type_enum(self):
        """Test SSOTComponentType enum values."""
        assert SSOTComponentType.EXECUTION.value == "execution"
        assert SSOTComponentType.VALIDATION.value == "validation"
        assert SSOTComponentType.INTEGRATION.value == "integration"
        assert SSOTComponentType.MONITORING.value == "monitoring"
        assert SSOTComponentType.REPORTING.value == "reporting"

    def test_ssot_status_enum(self):
        """Test SSOTStatus enum values."""
        assert SSOTStatus.ACTIVE.value == "active"
        assert SSOTStatus.INACTIVE.value == "inactive"
        assert SSOTStatus.ERROR.value == "error"
        assert SSOTStatus.MAINTENANCE.value == "maintenance"

    def test_ssot_priority_enum(self):
        """Test SSOTPriority enum values."""
        assert SSOTPriority.LOW.value == "low"
        assert SSOTPriority.MEDIUM.value == "medium"
        assert SSOTPriority.HIGH.value == "high"
        assert SSOTPriority.CRITICAL.value == "critical"
