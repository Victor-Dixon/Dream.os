"""
Tests for architectural_principles.py

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
"""

import pytest
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))

from src.services.architectural_principles import PrincipleDefinitions
from src.services.architectural_models import ArchitecturalPrinciple


class TestPrincipleDefinitions:
    """Test PrincipleDefinitions class."""

    def test_get_all_principles(self):
        """Test getting all architectural principles."""
        principles = PrincipleDefinitions.get_all_principles()
        
        assert isinstance(principles, dict)
        assert len(principles) == 9  # All 9 principles
        
        # Verify all principles are present
        for principle in ArchitecturalPrinciple:
            assert principle in principles

    def test_get_all_principles_returns_guidance(self):
        """Test that get_all_principles returns ArchitecturalGuidance objects."""
        principles = PrincipleDefinitions.get_all_principles()
        
        for principle, guidance in principles.items():
            assert principle in ArchitecturalPrinciple
            assert guidance is not None
            assert hasattr(guidance, 'principle')
            assert hasattr(guidance, 'display_name')
            assert hasattr(guidance, 'description')
            assert guidance.principle == principle

    def test_get_principle_single_responsibility(self):
        """Test getting Single Responsibility Principle."""
        guidance = PrincipleDefinitions.get_principle(
            ArchitecturalPrinciple.SINGLE_RESPONSIBILITY
        )
        
        assert guidance is not None
        assert guidance.principle == ArchitecturalPrinciple.SINGLE_RESPONSIBILITY
        assert "Single Responsibility" in guidance.display_name
        assert len(guidance.responsibilities) > 0
        assert len(guidance.guidelines) > 0

    def test_get_principle_dry(self):
        """Test getting DRY principle."""
        guidance = PrincipleDefinitions.get_principle(
            ArchitecturalPrinciple.DONT_REPEAT_YOURSELF
        )
        
        assert guidance is not None
        assert guidance.principle == ArchitecturalPrinciple.DONT_REPEAT_YOURSELF
        assert len(guidance.examples) > 0
        assert len(guidance.validation_rules) > 0

    def test_get_principle_kiss(self):
        """Test getting KISS principle."""
        guidance = PrincipleDefinitions.get_principle(
            ArchitecturalPrinciple.KEEP_IT_SIMPLE_STUPID
        )
        
        assert guidance is not None
        assert guidance.principle == ArchitecturalPrinciple.KEEP_IT_SIMPLE_STUPID

    def test_get_principle_open_closed(self):
        """Test getting Open-Closed Principle."""
        guidance = PrincipleDefinitions.get_principle(
            ArchitecturalPrinciple.OPEN_CLOSED
        )
        
        assert guidance is not None
        assert guidance.principle == ArchitecturalPrinciple.OPEN_CLOSED

    def test_get_principle_liskov_substitution(self):
        """Test getting Liskov Substitution Principle."""
        guidance = PrincipleDefinitions.get_principle(
            ArchitecturalPrinciple.LISKOV_SUBSTITUTION
        )
        
        assert guidance is not None
        assert guidance.principle == ArchitecturalPrinciple.LISKOV_SUBSTITUTION

    def test_get_principle_interface_segregation(self):
        """Test getting Interface Segregation Principle."""
        guidance = PrincipleDefinitions.get_principle(
            ArchitecturalPrinciple.INTERFACE_SEGREGATION
        )
        
        assert guidance is not None
        assert guidance.principle == ArchitecturalPrinciple.INTERFACE_SEGREGATION

    def test_get_principle_dependency_inversion(self):
        """Test getting Dependency Inversion Principle."""
        guidance = PrincipleDefinitions.get_principle(
            ArchitecturalPrinciple.DEPENDENCY_INVERSION
        )
        
        assert guidance is not None
        assert guidance.principle == ArchitecturalPrinciple.DEPENDENCY_INVERSION

    def test_get_principle_ssot(self):
        """Test getting SSOT principle."""
        guidance = PrincipleDefinitions.get_principle(
            ArchitecturalPrinciple.SINGLE_SOURCE_OF_TRUTH
        )
        
        assert guidance is not None
        assert guidance.principle == ArchitecturalPrinciple.SINGLE_SOURCE_OF_TRUTH

    def test_get_principle_tdd(self):
        """Test getting TDD principle."""
        guidance = PrincipleDefinitions.get_principle(
            ArchitecturalPrinciple.TEST_DRIVEN_DEVELOPMENT
        )
        
        assert guidance is not None
        assert guidance.principle == ArchitecturalPrinciple.TEST_DRIVEN_DEVELOPMENT

    def test_get_all_principles_completeness(self):
        """Test that get_all_principles matches get_principle for each."""
        all_principles = PrincipleDefinitions.get_all_principles()
        
        for principle in ArchitecturalPrinciple:
            individual = PrincipleDefinitions.get_principle(principle)
            from_all = all_principles.get(principle)
            
            assert individual is not None
            assert from_all is not None
            assert individual.principle == from_all.principle
            assert individual.display_name == from_all.display_name

    def test_get_all_principles_no_none_values(self):
        """Test that get_all_principles has no None values."""
        principles = PrincipleDefinitions.get_all_principles()
        
        for principle, guidance in principles.items():
            assert principle is not None
            assert guidance is not None

