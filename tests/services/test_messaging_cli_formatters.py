"""
Tests for messaging_cli_formatters.py

Comprehensive tests for message templates and formatting.
Target: ≥85% coverage
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

    def test_survey_message_template_exists(self):
        """Test that survey message template exists."""
        assert SURVEY_MESSAGE_TEMPLATE is not None
        assert isinstance(SURVEY_MESSAGE_TEMPLATE, str)
        assert len(SURVEY_MESSAGE_TEMPLATE) > 0

    def test_survey_message_template_content(self):
        """Test survey message template content."""
        assert "SWARM SURVEY" in SURVEY_MESSAGE_TEMPLATE
        assert "OBJECTIVE" in SURVEY_MESSAGE_TEMPLATE
        assert "PHASES" in SURVEY_MESSAGE_TEMPLATE
        assert "COORDINATION" in SURVEY_MESSAGE_TEMPLATE

    def test_assignment_message_template_exists(self):
        """Test that assignment message template exists."""
        assert ASSIGNMENT_MESSAGE_TEMPLATE is not None
        assert isinstance(ASSIGNMENT_MESSAGE_TEMPLATE, str)
        assert len(ASSIGNMENT_MESSAGE_TEMPLATE) > 0

    def test_assignment_message_template_formatting(self):
        """Test assignment message template formatting."""
        formatted = ASSIGNMENT_MESSAGE_TEMPLATE.format(
            agent="Agent-1",
            assignment="Test assignment"
        )
        assert "Agent-1" in formatted
        assert "Test assignment" in formatted
        assert "SURVEY ASSIGNMENT" in formatted

    def test_assignment_message_template_placeholders(self):
        """Test that assignment template has required placeholders."""
        assert "{agent}" in ASSIGNMENT_MESSAGE_TEMPLATE
        assert "{assignment}" in ASSIGNMENT_MESSAGE_TEMPLATE

    def test_consolidation_message_template_exists(self):
        """Test that consolidation message template exists."""
        assert CONSOLIDATION_MESSAGE_TEMPLATE is not None
        assert isinstance(CONSOLIDATION_MESSAGE_TEMPLATE, str)
        assert len(CONSOLIDATION_MESSAGE_TEMPLATE) > 0

    def test_consolidation_message_template_formatting(self):
        """Test consolidation message template formatting."""
        formatted = CONSOLIDATION_MESSAGE_TEMPLATE.format(
            batch="Batch 1",
            status="Complete",
            timestamp="2025-11-28T12:00:00"
        )
        assert "Batch 1" in formatted
        assert "Complete" in formatted
        assert "2025-11-28T12:00:00" in formatted
        assert "CONSOLIDATION UPDATE" in formatted

    def test_consolidation_message_template_placeholders(self):
        """Test that consolidation template has required placeholders."""
        assert "{batch}" in CONSOLIDATION_MESSAGE_TEMPLATE
        assert "{status}" in CONSOLIDATION_MESSAGE_TEMPLATE
        assert "{timestamp}" in CONSOLIDATION_MESSAGE_TEMPLATE


class TestAgentAssignments:
    """Tests for agent assignments dictionary."""

    def test_agent_assignments_exists(self):
        """Test that agent assignments dictionary exists."""
        assert AGENT_ASSIGNMENTS is not None
        assert isinstance(AGENT_ASSIGNMENTS, dict)

    def test_agent_assignments_has_all_agents(self):
        """Test that all agents are in assignments."""
        expected_agents = [
            "Agent-1", "Agent-2", "Agent-3", "Agent-4",
            "Agent-5", "Agent-6", "Agent-7", "Agent-8"
        ]
        for agent in expected_agents:
            assert agent in AGENT_ASSIGNMENTS

    def test_agent_assignments_values_are_strings(self):
        """Test that assignment values are strings."""
        for agent, assignment in AGENT_ASSIGNMENTS.items():
            assert isinstance(assignment, str)
            assert len(assignment) > 0

    def test_agent_assignments_agent_1(self):
        """Test Agent-1 assignment."""
        assert "Agent-1" in AGENT_ASSIGNMENTS
        assert "Service Layer" in AGENT_ASSIGNMENTS["Agent-1"]

    def test_agent_assignments_agent_2(self):
        """Test Agent-2 assignment."""
        assert "Agent-2" in AGENT_ASSIGNMENTS
        assert "Core Systems" in AGENT_ASSIGNMENTS["Agent-2"]

    def test_agent_assignments_agent_4(self):
        """Test Agent-4 assignment."""
        assert "Agent-4" in AGENT_ASSIGNMENTS
        assert "Quality Assurance" in AGENT_ASSIGNMENTS["Agent-4"]

    def test_agent_assignments_count(self):
        """Test that we have 8 agent assignments."""
        assert len(AGENT_ASSIGNMENTS) == 8

