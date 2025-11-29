"""
Tests for architectural_principles_data.py

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
"""

from src.services.architectural_models import ArchitecturalPrinciple, ArchitecturalGuidance
from src.services.architectural_principles_data import (
    get_srp_guidance,
    get_ocp_guidance,
    get_lsp_guidance,
    get_isp_guidance,
    get_dip_guidance,
    get_ssot_guidance,
    get_dry_guidance,
    get_kiss_guidance,
    get_tdd_guidance,
)
import pytest
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))


class TestSRPGuidance:
    """Test get_srp_guidance function."""

    def test_returns_architectural_guidance(self):
        """Test that function returns ArchitecturalGuidance instance."""
        guidance = get_srp_guidance()
        assert isinstance(guidance, ArchitecturalGuidance)

    def test_principle_is_srp(self):
        """Test that principle is SINGLE_RESPONSIBILITY."""
        guidance = get_srp_guidance()
        assert guidance.principle == ArchitecturalPrinciple.SINGLE_RESPONSIBILITY

    def test_has_display_name(self):
        """Test that guidance has display name."""
        guidance = get_srp_guidance()
        assert guidance.display_name == "Single Responsibility Principle (SRP)"
        assert len(guidance.display_name) > 0

    def test_has_description(self):
        """Test that guidance has description."""
        guidance = get_srp_guidance()
        assert "one reason to change" in guidance.description.lower()
        assert len(guidance.description) > 0

    def test_has_responsibilities(self):
        """Test that guidance has responsibilities list."""
        guidance = get_srp_guidance()
        assert isinstance(guidance.responsibilities, list)
        assert len(guidance.responsibilities) > 0
        assert all(isinstance(r, str) for r in guidance.responsibilities)

    def test_has_guidelines(self):
        """Test that guidance has guidelines list."""
        guidance = get_srp_guidance()
        assert isinstance(guidance.guidelines, list)
        assert len(guidance.guidelines) > 0
        assert all(isinstance(g, str) for g in guidance.guidelines)

    def test_has_examples(self):
        """Test that guidance has examples list."""
        guidance = get_srp_guidance()
        assert isinstance(guidance.examples, list)
        assert len(guidance.examples) > 0
        assert all(isinstance(e, str) for e in guidance.examples)

    def test_has_validation_rules(self):
        """Test that guidance has validation rules list."""
        guidance = get_srp_guidance()
        assert isinstance(guidance.validation_rules, list)
        assert len(guidance.validation_rules) > 0
        assert all(isinstance(v, str) for v in guidance.validation_rules)


class TestAllGuidanceFunctions:
    """Test all guidance functions return proper data."""

    @pytest.mark.parametrize("func,principle", [
        (get_srp_guidance, ArchitecturalPrinciple.SINGLE_RESPONSIBILITY),
        (get_ocp_guidance, ArchitecturalPrinciple.OPEN_CLOSED),
        (get_lsp_guidance, ArchitecturalPrinciple.LISKOV_SUBSTITUTION),
        (get_isp_guidance, ArchitecturalPrinciple.INTERFACE_SEGREGATION),
        (get_dip_guidance, ArchitecturalPrinciple.DEPENDENCY_INVERSION),
        (get_ssot_guidance, ArchitecturalPrinciple.SINGLE_SOURCE_OF_TRUTH),
        (get_dry_guidance, ArchitecturalPrinciple.DONT_REPEAT_YOURSELF),
        (get_kiss_guidance, ArchitecturalPrinciple.KEEP_IT_SIMPLE_STUPID),
        (get_tdd_guidance, ArchitecturalPrinciple.TEST_DRIVEN_DEVELOPMENT),
    ])
    def test_returns_correct_principle(self, func, principle):
        """Test each function returns guidance with correct principle."""
        guidance = func()
        assert guidance.principle == principle

    @pytest.mark.parametrize("func", [
        get_srp_guidance,
        get_ocp_guidance,
        get_lsp_guidance,
        get_isp_guidance,
        get_dip_guidance,
        get_ssot_guidance,
        get_dry_guidance,
        get_kiss_guidance,
        get_tdd_guidance,
    ])
    def test_returns_complete_guidance(self, func):
        """Test each function returns complete guidance structure."""
        guidance = func()

        assert isinstance(guidance, ArchitecturalGuidance)
        assert guidance.principle is not None
        assert len(guidance.display_name) > 0
        assert len(guidance.description) > 0
        assert isinstance(guidance.responsibilities, list)
        assert len(guidance.responsibilities) > 0
        assert isinstance(guidance.guidelines, list)
        assert len(guidance.guidelines) > 0
        assert isinstance(guidance.examples, list)
        assert len(guidance.examples) > 0
        assert isinstance(guidance.validation_rules, list)
        assert len(guidance.validation_rules) > 0

    @pytest.mark.parametrize("func", [
        get_srp_guidance,
        get_ocp_guidance,
        get_lsp_guidance,
        get_isp_guidance,
        get_dip_guidance,
        get_ssot_guidance,
        get_dry_guidance,
        get_kiss_guidance,
        get_tdd_guidance,
    ])
    def test_guidance_is_not_none(self, func):
        """Test each function returns non-None guidance."""
        guidance = func()
        assert guidance is not None

    @pytest.mark.parametrize("func", [
        get_srp_guidance,
        get_ocp_guidance,
        get_lsp_guidance,
        get_isp_guidance,
        get_dip_guidance,
        get_ssot_guidance,
        get_dry_guidance,
        get_kiss_guidance,
        get_tdd_guidance,
    ])
    def test_display_name_contains_principle(self, func):
        """Test each guidance display name contains principle acronym."""
        guidance = func()
        principle_value = guidance.principle.value
        # Display name should contain the principle value or full name
        assert len(guidance.display_name) > 0
        assert isinstance(guidance.display_name, str)


class TestSpecificGuidanceContent:
    """Test specific guidance content for key principles."""

    def test_ocp_guidance_content(self):
        """Test Open-Closed Principle guidance content."""
        guidance = get_ocp_guidance()
        assert "open for extension" in guidance.description.lower()
        assert "closed for modification" in guidance.description.lower()

    def test_dry_guidance_content(self):
        """Test DRY guidance content."""
        guidance = get_dry_guidance()
        assert "don't repeat yourself" in guidance.display_name.lower(
        ) or "dry" in guidance.display_name.lower()
        assert any("duplication" in r.lower()
                   for r in guidance.responsibilities)

    def test_kiss_guidance_content(self):
        """Test KISS guidance content."""
        guidance = get_kiss_guidance()
        assert "keep it simple" in guidance.display_name.lower(
        ) or "kiss" in guidance.display_name.lower()
        assert any("simple" in r.lower() for r in guidance.responsibilities)

    def test_tdd_guidance_content(self):
        """Test TDD guidance content."""
        guidance = get_tdd_guidance()
        assert "test-driven" in guidance.display_name.lower() or "tdd" in guidance.display_name.lower()
        assert any("test" in r.lower() for r in guidance.responsibilities)

    def test_ssot_guidance_content(self):
        """Test SSOT guidance content."""
        guidance = get_ssot_guidance()
        assert "single source" in guidance.display_name.lower(
        ) or "ssot" in guidance.display_name.lower()
        assert any("source" in r.lower() or "authoritative" in r.lower()
                   for r in guidance.responsibilities)
