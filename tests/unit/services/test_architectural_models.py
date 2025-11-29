"""
Tests for architectural_models.py

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
"""

import pytest
from datetime import datetime
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))

from src.services.architectural_models import (
    ArchitecturalPrinciple,
    ArchitecturalGuidance,
    AgentAssignment,
    ComplianceValidationResult,
)


class TestArchitecturalPrinciple:
    """Test ArchitecturalPrinciple enum."""

    def test_solid_principles_exist(self):
        """Test all SOLID principles are defined."""
        assert ArchitecturalPrinciple.SINGLE_RESPONSIBILITY.value == "SRP"
        assert ArchitecturalPrinciple.OPEN_CLOSED.value == "OCP"
        assert ArchitecturalPrinciple.LISKOV_SUBSTITUTION.value == "LSP"
        assert ArchitecturalPrinciple.INTERFACE_SEGREGATION.value == "ISP"
        assert ArchitecturalPrinciple.DEPENDENCY_INVERSION.value == "DIP"

    def test_other_principles_exist(self):
        """Test other key principles are defined."""
        assert ArchitecturalPrinciple.SINGLE_SOURCE_OF_TRUTH.value == "SSOT"
        assert ArchitecturalPrinciple.DONT_REPEAT_YOURSELF.value == "DRY"
        assert ArchitecturalPrinciple.KEEP_IT_SIMPLE_STUPID.value == "KISS"

    def test_tdd_principle_exists(self):
        """Test TDD principle is defined."""
        assert ArchitecturalPrinciple.TEST_DRIVEN_DEVELOPMENT.value == "TDD"

    def test_enum_values_are_strings(self):
        """Test all enum values are strings."""
        for principle in ArchitecturalPrinciple:
            assert isinstance(principle.value, str)
            assert len(principle.value) > 0

    def test_enum_count(self):
        """Test expected number of principles."""
        principles = list(ArchitecturalPrinciple)
        assert len(principles) == 9  # 5 SOLID + 3 other + 1 TDD

    def test_enum_comparison(self):
        """Test enum comparison works."""
        assert ArchitecturalPrinciple.SINGLE_RESPONSIBILITY == ArchitecturalPrinciple.SINGLE_RESPONSIBILITY
        assert ArchitecturalPrinciple.SINGLE_RESPONSIBILITY != ArchitecturalPrinciple.OPEN_CLOSED

    def test_enum_access_by_value(self):
        """Test accessing enum by value."""
        assert ArchitecturalPrinciple("SRP") == ArchitecturalPrinciple.SINGLE_RESPONSIBILITY
        assert ArchitecturalPrinciple("DRY") == ArchitecturalPrinciple.DONT_REPEAT_YOURSELF


class TestArchitecturalGuidance:
    """Test ArchitecturalGuidance dataclass."""

    def test_create_architectural_guidance(self):
        """Test creating ArchitecturalGuidance instance."""
        guidance = ArchitecturalGuidance(
            principle=ArchitecturalPrinciple.SINGLE_RESPONSIBILITY,
            display_name="Single Responsibility",
            description="A class should have one reason to change",
            responsibilities=["One responsibility"],
            guidelines=["Keep classes focused"],
            examples=["Example code"],
            validation_rules=["Check class size"]
        )
        
        assert guidance.principle == ArchitecturalPrinciple.SINGLE_RESPONSIBILITY
        assert guidance.display_name == "Single Responsibility"
        assert guidance.description == "A class should have one reason to change"
        assert len(guidance.responsibilities) == 1
        assert len(guidance.guidelines) == 1
        assert len(guidance.examples) == 1
        assert len(guidance.validation_rules) == 1

    def test_architectural_guidance_empty_lists(self):
        """Test ArchitecturalGuidance with empty lists."""
        guidance = ArchitecturalGuidance(
            principle=ArchitecturalPrinciple.DONT_REPEAT_YOURSELF,
            display_name="DRY",
            description="Don't Repeat Yourself",
            responsibilities=[],
            guidelines=[],
            examples=[],
            validation_rules=[]
        )
        
        assert len(guidance.responsibilities) == 0
        assert len(guidance.guidelines) == 0
        assert len(guidance.examples) == 0
        assert len(guidance.validation_rules) == 0

    def test_architectural_guidance_multiple_items(self):
        """Test ArchitecturalGuidance with multiple items in lists."""
        guidance = ArchitecturalGuidance(
            principle=ArchitecturalPrinciple.KEEP_IT_SIMPLE_STUPID,
            display_name="KISS",
            description="Keep It Simple",
            responsibilities=["Item 1", "Item 2", "Item 3"],
            guidelines=["Guideline 1", "Guideline 2"],
            examples=["Example 1", "Example 2", "Example 3", "Example 4"],
            validation_rules=["Rule 1"]
        )
        
        assert len(guidance.responsibilities) == 3
        assert len(guidance.guidelines) == 2
        assert len(guidance.examples) == 4
        assert len(guidance.validation_rules) == 1

    def test_architectural_guidance_all_principles(self):
        """Test creating guidance for all principle types."""
        for principle in ArchitecturalPrinciple:
            guidance = ArchitecturalGuidance(
                principle=principle,
                display_name=f"Display {principle.name}",
                description=f"Description for {principle.name}",
                responsibilities=["Responsibility"],
                guidelines=["Guideline"],
                examples=["Example"],
                validation_rules=["Rule"]
            )
            assert guidance.principle == principle


class TestAgentAssignment:
    """Test AgentAssignment dataclass."""

    def test_create_agent_assignment(self):
        """Test creating AgentAssignment instance."""
        timestamp = datetime.now().isoformat()
        assignment = AgentAssignment(
            agent_id="Agent-1",
            principle=ArchitecturalPrinciple.SINGLE_RESPONSIBILITY,
            assigned_at=timestamp
        )
        
        assert assignment.agent_id == "Agent-1"
        assert assignment.principle == ArchitecturalPrinciple.SINGLE_RESPONSIBILITY
        assert assignment.assigned_at == timestamp
        assert assignment.assigned_by == "system"  # Default value

    def test_agent_assignment_with_custom_assigned_by(self):
        """Test AgentAssignment with custom assigned_by."""
        timestamp = datetime.now().isoformat()
        assignment = AgentAssignment(
            agent_id="Agent-2",
            principle=ArchitecturalPrinciple.DONT_REPEAT_YOURSELF,
            assigned_at=timestamp,
            assigned_by="Agent-4"
        )
        
        assert assignment.assigned_by == "Agent-4"

    def test_agent_assignment_all_principles(self):
        """Test creating assignments for all principles."""
        timestamp = datetime.now().isoformat()
        for principle in ArchitecturalPrinciple:
            assignment = AgentAssignment(
                agent_id="Agent-3",
                principle=principle,
                assigned_at=timestamp
            )
            assert assignment.principle == principle

    def test_agent_assignment_different_agents(self):
        """Test creating assignments for different agents."""
        timestamp = datetime.now().isoformat()
        for i, principle in enumerate(ArchitecturalPrinciple):
            agent_id = f"Agent-{i+1}"
            assignment = AgentAssignment(
                agent_id=agent_id,
                principle=principle,
                assigned_at=timestamp
            )
            assert assignment.agent_id == agent_id


class TestComplianceValidationResult:
    """Test ComplianceValidationResult dataclass."""

    def test_create_compliance_result_compliant(self):
        """Test creating compliant validation result."""
        timestamp = datetime.now().isoformat()
        result = ComplianceValidationResult(
            agent_id="Agent-1",
            principle=ArchitecturalPrinciple.SINGLE_RESPONSIBILITY,
            compliant=True,
            issues=[],
            recommendations=[],
            validated_at=timestamp
        )
        
        assert result.agent_id == "Agent-1"
        assert result.principle == ArchitecturalPrinciple.SINGLE_RESPONSIBILITY
        assert result.compliant is True
        assert len(result.issues) == 0
        assert len(result.recommendations) == 0
        assert result.validated_at == timestamp

    def test_create_compliance_result_non_compliant(self):
        """Test creating non-compliant validation result."""
        timestamp = datetime.now().isoformat()
        result = ComplianceValidationResult(
            agent_id="Agent-2",
            principle=ArchitecturalPrinciple.DONT_REPEAT_YOURSELF,
            compliant=False,
            issues=["Issue 1", "Issue 2"],
            recommendations=["Recommendation 1"],
            validated_at=timestamp
        )
        
        assert result.compliant is False
        assert len(result.issues) == 2
        assert len(result.recommendations) == 1

    def test_compliance_result_all_principles(self):
        """Test creating results for all principles."""
        timestamp = datetime.now().isoformat()
        for principle in ArchitecturalPrinciple:
            result = ComplianceValidationResult(
                agent_id="Agent-3",
                principle=principle,
                compliant=True,
                issues=[],
                recommendations=[],
                validated_at=timestamp
            )
            assert result.principle == principle

    def test_compliance_result_multiple_issues_and_recommendations(self):
        """Test result with multiple issues and recommendations."""
        timestamp = datetime.now().isoformat()
        result = ComplianceValidationResult(
            agent_id="Agent-4",
            principle=ArchitecturalPrinciple.KEEP_IT_SIMPLE_STUPID,
            compliant=False,
            issues=["Issue 1", "Issue 2", "Issue 3"],
            recommendations=["Rec 1", "Rec 2", "Rec 3", "Rec 4"],
            validated_at=timestamp
        )
        
        assert len(result.issues) == 3
        assert len(result.recommendations) == 4

