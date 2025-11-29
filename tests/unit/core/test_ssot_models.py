"""
Unit tests for src/core/ssot/ssot_models.py
"""

import pytest

from src.core.ssot.ssot_models import (
    SSOTEntity,
    SSOTRelation,
    SSOTViolation,
)


class TestSSOTModels:
    """Test SSOT model classes."""

    def test_ssot_entity_creation(self):
        """Test that SSOTEntity can be created."""
        entity = SSOTEntity(
            name="test_entity",
            entity_type="test_type",
            source="test_source"
        )
        assert entity.name == "test_entity"
        assert entity.entity_type == "test_type"
        assert entity.source == "test_source"

    def test_ssot_relation_creation(self):
        """Test that SSOTRelation can be created."""
        relation = SSOTRelation(
            from_entity="entity1",
            to_entity="entity2",
            relation_type="depends_on"
        )
        assert relation.from_entity == "entity1"
        assert relation.to_entity == "entity2"
        assert relation.relation_type == "depends_on"

    def test_ssot_violation_creation(self):
        """Test that SSOTViolation can be created."""
        violation = SSOTViolation(
            violation_type="duplicate",
            entity_name="test_entity",
            message="Test violation"
        )
        assert violation.violation_type == "duplicate"
        assert violation.entity_name == "test_entity"
        assert violation.message == "Test violation"



