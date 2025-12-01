"""
Unit Tests for Test Categories Config
======================================
"""

import pytest
from src.core.test_categories_config import get_test_categories


class TestTestCategoriesConfig:
    """Tests for test categories configuration."""

    def test_get_test_categories(self):
        """Test getting test categories."""
        categories = get_test_categories()
        assert isinstance(categories, dict)
        assert len(categories) > 0

    def test_smoke_category(self):
        """Test smoke test category."""
        categories = get_test_categories()
        assert "smoke" in categories
        smoke = categories["smoke"]
        assert smoke["marker"] == "smoke"
        assert smoke["critical"] is True
        assert "description" in smoke

    def test_unit_category(self):
        """Test unit test category."""
        categories = get_test_categories()
        assert "unit" in categories
        unit = categories["unit"]
        assert unit["marker"] == "unit"
        assert unit["critical"] is True

    def test_integration_category(self):
        """Test integration test category."""
        categories = get_test_categories()
        assert "integration" in categories
        integration = categories["integration"]
        assert integration["marker"] == "integration"
        assert integration["critical"] is False

    def test_performance_category(self):
        """Test performance test category."""
        categories = get_test_categories()
        assert "performance" in categories
        performance = categories["performance"]
        assert performance["marker"] == "performance"
        assert performance["timeout"] == 600

    def test_security_category(self):
        """Test security test category."""
        categories = get_test_categories()
        assert "security" in categories
        security = categories["security"]
        assert security["marker"] == "security"
        assert security["critical"] is True

    def test_api_category(self):
        """Test API test category."""
        categories = get_test_categories()
        assert "api" in categories
        api = categories["api"]
        assert api["marker"] == "api"

    def test_behavior_category(self):
        """Test behavior test category."""
        categories = get_test_categories()
        assert "behavior" in categories
        behavior = categories["behavior"]
        assert behavior["marker"] == "behavior"

    def test_decision_category(self):
        """Test decision test category."""
        categories = get_test_categories()
        assert "decision" in categories
        decision = categories["decision"]
        assert decision["marker"] == "decision"

    def test_coordination_category(self):
        """Test coordination test category."""
        categories = get_test_categories()
        assert "coordination" in categories
        coordination = categories["coordination"]
        assert coordination["marker"] == "coordination"

    def test_learning_category(self):
        """Test learning test category."""
        categories = get_test_categories()
        assert "learning" in categories
        learning = categories["learning"]
        assert learning["marker"] == "learning"

    def test_all_categories_have_required_fields(self):
        """Test that all categories have required fields."""
        categories = get_test_categories()
        required_fields = ["description", "marker", "timeout", "critical", "directory"]
        
        for category_name, category_data in categories.items():
            for field in required_fields:
                assert field in category_data, f"Category {category_name} missing {field}"

    def test_category_timeouts_are_positive(self):
        """Test that all category timeouts are positive."""
        categories = get_test_categories()
        for category_name, category_data in categories.items():
            assert category_data["timeout"] > 0, f"Category {category_name} has invalid timeout"

    def test_category_directories_are_strings(self):
        """Test that all category directories are strings."""
        categories = get_test_categories()
        for category_name, category_data in categories.items():
            assert isinstance(category_data["directory"], str), f"Category {category_name} directory not string"
            assert len(category_data["directory"]) > 0, f"Category {category_name} directory is empty"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


