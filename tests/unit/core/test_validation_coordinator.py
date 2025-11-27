"""
Unit tests for src/core/validation/validation_coordinator.py
"""

import pytest

from src.core.validation.validation_coordinator import ValidationCoordinator


class TestValidationCoordinator:
    """Test ValidationCoordinator functionality."""

    @pytest.fixture
    def coordinator(self):
        """Create ValidationCoordinator instance."""
        return ValidationCoordinator()

    @pytest.fixture
    def mock_engine(self):
        """Create mock validation engine."""
        class MockEngine:
            def validate(self, data, config):
                return {"valid": True, "errors": [], "warnings": []}
        return MockEngine()

    def test_coordinator_creation(self, coordinator):
        """Test that ValidationCoordinator can be created."""
        assert coordinator is not None
        assert coordinator.engines == {}

    def test_register_engine(self, coordinator, mock_engine):
        """Test that register_engine() registers an engine."""
        coordinator.register_engine("test_engine", mock_engine)
        assert "test_engine" in coordinator.engines
        assert coordinator.engines["test_engine"] == mock_engine

    def test_validate_with_registered_engine(self, coordinator, mock_engine):
        """Test that validate() uses registered engine."""
        coordinator.register_engine("test_engine", mock_engine)
        rules = {"test_engine": {"field": "value"}}
        result = coordinator.validate({"field": "value"}, rules)
        assert result["valid"] is True
        assert isinstance(result["errors"], list)
        assert isinstance(result["warnings"], list)

    def test_validate_without_engine(self, coordinator):
        """Test that validate() handles missing engine gracefully."""
        rules = {"missing_engine": {"field": "value"}}
        result = coordinator.validate({"field": "value"}, rules)
        # Should not crash, may or may not be valid depending on implementation
        assert isinstance(result, dict)

    def test_get_available_engines(self, coordinator, mock_engine):
        """Test that get_available_engines() returns registered engines."""
        coordinator.register_engine("test_engine", mock_engine)
        engines = coordinator.get_available_engines()
        assert "test_engine" in engines

