"""
Unit tests for src/services/compliance_validator.py

Tests compliance validation functionality including:
- Agent compliance validation
- Principle-specific validation
- Recommendation generation
"""

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime

from src.services.compliance_validator import ComplianceValidator
from src.services.architectural_models import ArchitecturalPrinciple, ComplianceValidationResult


class TestComplianceValidator:
    """Test compliance validator."""

    @pytest.fixture
    def validator(self):
        """Create compliance validator instance."""
        return ComplianceValidator()

    def test_validate_agent_compliance_single_responsibility(self, validator):
        """Test validation for Single Responsibility Principle."""
        code_changes = [
            "class MyClass:\n    def method1(self): pass\n    def method2(self): pass"
        ]
        
        result = validator.validate_agent_compliance(
            "Agent-1",
            ArchitecturalPrinciple.SINGLE_RESPONSIBILITY,
            code_changes
        )
        
        assert isinstance(result, ComplianceValidationResult)
        assert result.agent_id == "Agent-1"
        assert result.principle == ArchitecturalPrinciple.SINGLE_RESPONSIBILITY
        assert isinstance(result.compliant, bool)
        assert isinstance(result.issues, list)
        assert isinstance(result.recommendations, list)

    def test_validate_agent_compliance_dry_principle(self, validator):
        """Test validation for DRY Principle."""
        code_changes = [
            "def func1(): pass\ndef func2(): pass\ndef func3(): pass"
        ]
        
        result = validator.validate_agent_compliance(
            "Agent-7",
            ArchitecturalPrinciple.DONT_REPEAT_YOURSELF,
            code_changes
        )
        
        assert isinstance(result, ComplianceValidationResult)
        assert result.principle == ArchitecturalPrinciple.DONT_REPEAT_YOURSELF

    def test_validate_agent_compliance_kiss_principle(self, validator):
        """Test validation for KISS Principle."""
        code_changes = [
            "def complex_method():\n" + "\n".join(["    pass"] * 60)
        ]
        
        result = validator.validate_agent_compliance(
            "Agent-8",
            ArchitecturalPrinciple.KEEP_IT_SIMPLE_STUPID,
            code_changes
        )
        
        assert isinstance(result, ComplianceValidationResult)
        assert result.principle == ArchitecturalPrinciple.KEEP_IT_SIMPLE_STUPID

    def test_validate_agent_compliance_open_closed(self, validator):
        """Test validation for Open-Closed Principle."""
        code_changes = [
            "if isinstance(obj, Type):\n    do_something()"
        ]
        
        result = validator.validate_agent_compliance(
            "Agent-2",
            ArchitecturalPrinciple.OPEN_CLOSED,
            code_changes
        )
        
        assert isinstance(result, ComplianceValidationResult)
        assert result.principle == ArchitecturalPrinciple.OPEN_CLOSED

    def test_validate_single_responsibility_god_class(self, validator):
        """Test detection of God class violation."""
        change = "class GodClass:\n" + "\n".join([f"    def method{i}(self): pass" for i in range(6)])
        
        issues = validator._validate_single_responsibility(change)
        
        assert isinstance(issues, list)
        assert any("God class" in issue or "too many methods" in issue for issue in issues)

    def test_validate_single_responsibility_compliant(self, validator):
        """Test compliant Single Responsibility code."""
        change = "class SimpleClass:\n    def method(self): pass"
        
        issues = validator._validate_single_responsibility(change)
        
        assert len(issues) == 0

    def test_validate_dry_principle_violations(self, validator):
        """Test DRY principle violation detection."""
        change = "def func1(): pass\n" * 6
        change += "for i in range(10):\n" * 4
        
        issues = validator._validate_dry_principle(change)
        
        assert isinstance(issues, list)
        assert len(issues) > 0

    def test_validate_dry_principle_compliant(self, validator):
        """Test compliant DRY code."""
        change = "def func1(): pass\ndef func2(): pass"
        
        issues = validator._validate_dry_principle(change)
        
        assert len(issues) == 0

    def test_validate_kiss_principle_long_method(self, validator):
        """Test KISS principle - long method detection."""
        change = "\n".join(["    pass"] * 60)
        
        issues = validator._validate_kiss_principle(change)
        
        assert isinstance(issues, list)
        assert any("Method too long" in issue for issue in issues)

    def test_validate_kiss_principle_complex_conditionals(self, validator):
        """Test KISS principle - complex conditionals detection."""
        change = "if x and y or z and a or b: pass"
        
        issues = validator._validate_kiss_principle(change)
        
        assert isinstance(issues, list)
        assert any("boolean expressions" in issue for issue in issues)

    def test_validate_kiss_principle_compliant(self, validator):
        """Test compliant KISS code."""
        change = "def simple_method():\n    return True"
        
        issues = validator._validate_kiss_principle(change)
        
        assert len(issues) == 0

    def test_validate_open_closed_type_checking(self, validator):
        """Test Open-Closed principle - type checking detection."""
        change = "if isinstance(obj, Type): pass"
        
        issues = validator._validate_open_closed(change)
        
        assert isinstance(issues, list)
        assert any("type checking" in issue.lower() for issue in issues)

    def test_validate_open_closed_compliant(self, validator):
        """Test compliant Open-Closed code."""
        change = "def process(data): return data.process()"
        
        issues = validator._validate_open_closed(change)
        
        assert len(issues) == 0

    def test_generate_recommendations_god_class(self, validator):
        """Test recommendation generation for God class."""
        issues = ["Potential God class detected - class definition too complex"]
        
        recommendations = validator._generate_recommendations(
            ArchitecturalPrinciple.SINGLE_RESPONSIBILITY,
            issues
        )
        
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        assert any("Extract smaller classes" in rec for rec in recommendations)

    def test_generate_recommendations_too_many_methods(self, validator):
        """Test recommendation generation for too many methods."""
        issues = ["Class has too many methods - consider splitting responsibilities"]
        
        recommendations = validator._generate_recommendations(
            ArchitecturalPrinciple.SINGLE_RESPONSIBILITY,
            issues
        )
        
        assert isinstance(recommendations, list)
        assert any("Split class" in rec for rec in recommendations)

    def test_generate_recommendations_method_too_long(self, validator):
        """Test recommendation generation for long method."""
        issues = ["Method too long - consider breaking into smaller functions"]
        
        recommendations = validator._generate_recommendations(
            ArchitecturalPrinciple.KEEP_IT_SIMPLE_STUPID,
            issues
        )
        
        assert isinstance(recommendations, list)
        assert any("Break method" in rec for rec in recommendations)

    def test_generate_recommendations_no_issues(self, validator):
        """Test recommendation generation with no issues."""
        issues = []
        
        recommendations = validator._generate_recommendations(
            ArchitecturalPrinciple.SINGLE_RESPONSIBILITY,
            issues
        )
        
        assert isinstance(recommendations, list)
        assert len(recommendations) == 0

    def test_get_current_timestamp(self, validator):
        """Test getting current timestamp."""
        timestamp = validator._get_current_timestamp()
        
        assert isinstance(timestamp, str)
        assert len(timestamp) > 0
        # Should be ISO format timestamp
        assert 'T' in timestamp or '-' in timestamp

    def test_validate_agent_compliance_multiple_changes(self, validator):
        """Test validation with multiple code changes."""
        code_changes = [
            "class Class1:\n    def method1(self): pass",
            "class Class2:\n    def method2(self): pass"
        ]
        
        result = validator.validate_agent_compliance(
            "Agent-1",
            ArchitecturalPrinciple.SINGLE_RESPONSIBILITY,
            code_changes
        )
        
        assert isinstance(result, ComplianceValidationResult)
        assert result.agent_id == "Agent-1"

    def test_validate_agent_compliance_compliant_result(self, validator):
        """Test validation returns compliant result when no issues."""
        code_changes = [
            "def simple_function(): return True"
        ]
        
        result = validator.validate_agent_compliance(
            "Agent-8",
            ArchitecturalPrinciple.KEEP_IT_SIMPLE_STUPID,
            code_changes
        )
        
        assert result.compliant is True
        assert len(result.issues) == 0

    def test_validate_agent_compliance_non_compliant_result(self, validator):
        """Test validation returns non-compliant result when issues found."""
        code_changes = [
            "\n".join(["    pass"] * 60)  # Long method
        ]
        
        result = validator.validate_agent_compliance(
            "Agent-8",
            ArchitecturalPrinciple.KEEP_IT_SIMPLE_STUPID,
            code_changes
        )
        
        assert result.compliant is False
        assert len(result.issues) > 0
        assert len(result.recommendations) > 0

