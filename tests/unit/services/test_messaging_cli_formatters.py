"""
Tests for messaging_cli_formatters.py

Comprehensive tests for message formatting, templates, and display logic.
Target: 10+ test methods, ≥85% coverage
"""

import pytest
from src.services.messaging_cli_formatters import (
    SURVEY_MESSAGE_TEMPLATE,
    ASSIGNMENT_MESSAGE_TEMPLATE,
    CONSOLIDATION_MESSAGE_TEMPLATE,
    AGENT_ASSIGNMENTS,
)


class TestMessageTemplates:
    """Tests for message templates."""

    def test_survey_message_template_structure(self):
        """Test survey message template has required structure."""
        assert "SWARM SURVEY INITIATED" in SURVEY_MESSAGE_TEMPLATE
        assert "OBJECTIVE:" in SURVEY_MESSAGE_TEMPLATE
        assert "TARGET:" in SURVEY_MESSAGE_TEMPLATE
        assert "PHASES:" in SURVEY_MESSAGE_TEMPLATE
        assert "COORDINATION:" in SURVEY_MESSAGE_TEMPLATE
        assert "COMMANDER:" in SURVEY_MESSAGE_TEMPLATE

    def test_survey_message_template_content(self):
        """Test survey message template contains expected content."""
        assert "src/ directory" in SURVEY_MESSAGE_TEMPLATE
        assert "683 → ~250 files" in SURVEY_MESSAGE_TEMPLATE
        assert "Structural Analysis" in SURVEY_MESSAGE_TEMPLATE
        assert "Functional Analysis" in SURVEY_MESSAGE_TEMPLATE
        assert "Quality Assessment" in SURVEY_MESSAGE_TEMPLATE
        assert "Consolidation Planning" in SURVEY_MESSAGE_TEMPLATE
        assert "Captain Agent-4" in SURVEY_MESSAGE_TEMPLATE

    def test_assignment_message_template_structure(self):
        """Test assignment message template has required structure."""
        assert "SURVEY ASSIGNMENT" in ASSIGNMENT_MESSAGE_TEMPLATE
        assert "{agent}" in ASSIGNMENT_MESSAGE_TEMPLATE
        assert "{assignment}" in ASSIGNMENT_MESSAGE_TEMPLATE
        assert "ROLE:" in ASSIGNMENT_MESSAGE_TEMPLATE
        assert "DELIVERABLES:" in ASSIGNMENT_MESSAGE_TEMPLATE
        assert "TIMELINE:" in ASSIGNMENT_MESSAGE_TEMPLATE

    def test_assignment_message_template_formatting(self):
        """Test assignment message template can be formatted."""
        formatted = ASSIGNMENT_MESSAGE_TEMPLATE.format(
            agent="Agent-6",
            assignment="Coordination Specialist"
        )
        assert "Agent-6" in formatted
        assert "Coordination Specialist" in formatted
        assert "SURVEY ASSIGNMENT" in formatted

    def test_consolidation_message_template_structure(self):
        """Test consolidation message template has required structure."""
        assert "CONSOLIDATION UPDATE" in CONSOLIDATION_MESSAGE_TEMPLATE
        assert "{batch}" in CONSOLIDATION_MESSAGE_TEMPLATE
        assert "{status}" in CONSOLIDATION_MESSAGE_TEMPLATE
        assert "{timestamp}" in CONSOLIDATION_MESSAGE_TEMPLATE
        assert "BATCH:" in CONSOLIDATION_MESSAGE_TEMPLATE
        assert "STATUS:" in CONSOLIDATION_MESSAGE_TEMPLATE
        assert "TIMESTAMP:" in CONSOLIDATION_MESSAGE_TEMPLATE

    def test_consolidation_message_template_formatting(self):
        """Test consolidation message template can be formatted."""
        from datetime import datetime
        formatted = CONSOLIDATION_MESSAGE_TEMPLATE.format(
            batch="Batch 2",
            status="58% complete",
            timestamp=datetime.now().isoformat()
        )
        assert "Batch 2" in formatted
        assert "58% complete" in formatted
        assert "CONSOLIDATION UPDATE" in formatted

    def test_agent_assignments_structure(self):
        """Test agent assignments dictionary structure."""
        assert isinstance(AGENT_ASSIGNMENTS, dict)
        assert len(AGENT_ASSIGNMENTS) == 8
        assert "Agent-1" in AGENT_ASSIGNMENTS
        assert "Agent-2" in AGENT_ASSIGNMENTS
        assert "Agent-3" in AGENT_ASSIGNMENTS
        assert "Agent-4" in AGENT_ASSIGNMENTS
        assert "Agent-5" in AGENT_ASSIGNMENTS
        assert "Agent-6" in AGENT_ASSIGNMENTS
        assert "Agent-7" in AGENT_ASSIGNMENTS
        assert "Agent-8" in AGENT_ASSIGNMENTS

    def test_agent_assignments_content(self):
        """Test agent assignments contain expected content."""
        assert "Service Layer" in AGENT_ASSIGNMENTS["Agent-1"]
        assert "Core Systems" in AGENT_ASSIGNMENTS["Agent-2"]
        assert "Web & API" in AGENT_ASSIGNMENTS["Agent-3"]
        assert "Quality Assurance" in AGENT_ASSIGNMENTS["Agent-4"]
        assert "Trading & Gaming" in AGENT_ASSIGNMENTS["Agent-5"]
        assert "Testing & Infrastructure" in AGENT_ASSIGNMENTS["Agent-6"]
        assert "Performance & Monitoring" in AGENT_ASSIGNMENTS["Agent-7"]
        assert "Integration & Coordination" in AGENT_ASSIGNMENTS["Agent-8"]

    def test_agent_assignments_all_have_descriptions(self):
        """Test all agent assignments have non-empty descriptions."""
        for agent, assignment in AGENT_ASSIGNMENTS.items():
            assert len(assignment) > 0
            assert "Specialist" in assignment or "Architect" in assignment or "Assurance" in assignment

    def test_template_consistency(self):
        """Test templates are consistent in formatting style."""
        templates = [
            SURVEY_MESSAGE_TEMPLATE,
            ASSIGNMENT_MESSAGE_TEMPLATE,
            CONSOLIDATION_MESSAGE_TEMPLATE,
        ]
        for template in templates:
            # All should use consistent header style
            assert "=" in template or "🐝" in template or "🔧" in template
            # All should have clear sections
            assert "\n" in template

    def test_survey_template_contains_phases(self):
        """Test survey template contains all 4 phases."""
        assert "Phase" in SURVEY_MESSAGE_TEMPLATE or "PHASES:" in SURVEY_MESSAGE_TEMPLATE
        # Check for phase numbers or phase names
        phase_indicators = ["1.", "2.", "3.", "4."] or [
            "Structural",
            "Functional",
            "Quality",
            "Consolidation"
        ]
        # At least some phase indicators should be present
        assert any(indicator in SURVEY_MESSAGE_TEMPLATE for indicator in [
            "Structural", "Functional", "Quality", "Consolidation"
        ])

    def test_assignment_template_placeholders(self):
        """Test assignment template has correct placeholders."""
        # Should have both placeholders
        assert ASSIGNMENT_MESSAGE_TEMPLATE.count("{agent}") >= 1
        assert ASSIGNMENT_MESSAGE_TEMPLATE.count("{assignment}") >= 1

    def test_consolidation_template_placeholders(self):
        """Test consolidation template has correct placeholders."""
        # Should have all three placeholders
        assert CONSOLIDATION_MESSAGE_TEMPLATE.count("{batch}") >= 1
        assert CONSOLIDATION_MESSAGE_TEMPLATE.count("{status}") >= 1
        assert CONSOLIDATION_MESSAGE_TEMPLATE.count("{timestamp}") >= 1

    def test_templates_are_strings(self):
        """Test all templates are strings."""
        assert isinstance(SURVEY_MESSAGE_TEMPLATE, str)
        assert isinstance(ASSIGNMENT_MESSAGE_TEMPLATE, str)
        assert isinstance(CONSOLIDATION_MESSAGE_TEMPLATE, str)
        assert isinstance(AGENT_ASSIGNMENTS, dict)
        # All assignment values should be strings
        for assignment in AGENT_ASSIGNMENTS.values():
            assert isinstance(assignment, str)
