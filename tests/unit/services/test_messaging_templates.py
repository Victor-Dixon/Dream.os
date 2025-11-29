"""
Unit tests for messaging_templates.py
Target: ≥85% coverage
"""

import pytest
from src.services.utils.messaging_templates import (
    CLI_HELP_EPILOG,
    SURVEY_MESSAGE_TEMPLATE,
    ASSIGNMENT_MESSAGE_TEMPLATE,
    CONSOLIDATION_MESSAGE_TEMPLATE,
)


class TestMessagingTemplates:
    """Tests for messaging templates."""

    def test_cli_help_epilog_exists(self):
        """Test CLI_HELP_EPILOG is defined."""
        assert CLI_HELP_EPILOG is not None
        assert isinstance(CLI_HELP_EPILOG, str)
        assert len(CLI_HELP_EPILOG) > 0

    def test_cli_help_epilog_contains_examples(self):
        """Test CLI_HELP_EPILOG contains example commands."""
        assert "EXAMPLES" in CLI_HELP_EPILOG
        assert "--message" in CLI_HELP_EPILOG
        assert "--agent" in CLI_HELP_EPILOG
        assert "--broadcast" in CLI_HELP_EPILOG

    def test_cli_help_epilog_contains_swarm_tag(self):
        """Test CLI_HELP_EPILOG contains swarm tag."""
        assert "SWARM" in CLI_HELP_EPILOG or "swarm" in CLI_HELP_EPILOG

    def test_survey_message_template_exists(self):
        """Test SURVEY_MESSAGE_TEMPLATE is defined."""
        assert SURVEY_MESSAGE_TEMPLATE is not None
        assert isinstance(SURVEY_MESSAGE_TEMPLATE, str)
        assert len(SURVEY_MESSAGE_TEMPLATE) > 0

    def test_survey_message_template_contains_objective(self):
        """Test SURVEY_MESSAGE_TEMPLATE contains objective."""
        assert "OBJECTIVE" in SURVEY_MESSAGE_TEMPLATE or "objective" in SURVEY_MESSAGE_TEMPLATE

    def test_survey_message_template_contains_phases(self):
        """Test SURVEY_MESSAGE_TEMPLATE contains phases."""
        assert "PHASES" in SURVEY_MESSAGE_TEMPLATE or "phases" in SURVEY_MESSAGE_TEMPLATE

    def test_survey_message_template_contains_coordination(self):
        """Test SURVEY_MESSAGE_TEMPLATE contains coordination info."""
        assert "COORDINATION" in SURVEY_MESSAGE_TEMPLATE or "coordination" in SURVEY_MESSAGE_TEMPLATE

    def test_assignment_message_template_exists(self):
        """Test ASSIGNMENT_MESSAGE_TEMPLATE is defined."""
        assert ASSIGNMENT_MESSAGE_TEMPLATE is not None
        assert isinstance(ASSIGNMENT_MESSAGE_TEMPLATE, str)
        assert len(ASSIGNMENT_MESSAGE_TEMPLATE) > 0

    def test_assignment_message_template_contains_placeholders(self):
        """Test ASSIGNMENT_MESSAGE_TEMPLATE contains format placeholders."""
        assert "{agent}" in ASSIGNMENT_MESSAGE_TEMPLATE
        assert "{assignment}" in ASSIGNMENT_MESSAGE_TEMPLATE

    def test_assignment_message_template_formatting(self):
        """Test ASSIGNMENT_MESSAGE_TEMPLATE can be formatted."""
        formatted = ASSIGNMENT_MESSAGE_TEMPLATE.format(
            agent="Agent-1",
            assignment="Test Assignment"
        )
        assert "Agent-1" in formatted
        assert "Test Assignment" in formatted

    def test_assignment_message_template_contains_deliverables(self):
        """Test ASSIGNMENT_MESSAGE_TEMPLATE contains deliverables."""
        assert "DELIVERABLES" in ASSIGNMENT_MESSAGE_TEMPLATE or "deliverables" in ASSIGNMENT_MESSAGE_TEMPLATE

    def test_consolidation_message_template_exists(self):
        """Test CONSOLIDATION_MESSAGE_TEMPLATE is defined."""
        assert CONSOLIDATION_MESSAGE_TEMPLATE is not None
        assert isinstance(CONSOLIDATION_MESSAGE_TEMPLATE, str)
        assert len(CONSOLIDATION_MESSAGE_TEMPLATE) > 0

    def test_consolidation_message_template_contains_placeholders(self):
        """Test CONSOLIDATION_MESSAGE_TEMPLATE contains format placeholders."""
        assert "{batch}" in CONSOLIDATION_MESSAGE_TEMPLATE
        assert "{status}" in CONSOLIDATION_MESSAGE_TEMPLATE
        assert "{timestamp}" in CONSOLIDATION_MESSAGE_TEMPLATE

    def test_consolidation_message_template_formatting(self):
        """Test CONSOLIDATION_MESSAGE_TEMPLATE can be formatted."""
        formatted = CONSOLIDATION_MESSAGE_TEMPLATE.format(
            batch="batch-1",
            status="complete",
            timestamp="2025-11-28"
        )
        assert "batch-1" in formatted
        assert "complete" in formatted
        assert "2025-11-28" in formatted

    def test_consolidation_message_template_contains_coordination(self):
        """Test CONSOLIDATION_MESSAGE_TEMPLATE contains coordination info."""
        assert "COORDINATION" in CONSOLIDATION_MESSAGE_TEMPLATE or "coordination" in CONSOLIDATION_MESSAGE_TEMPLATE

    def test_templates_are_strings(self):
        """Test all templates are strings."""
        assert isinstance(CLI_HELP_EPILOG, str)
        assert isinstance(SURVEY_MESSAGE_TEMPLATE, str)
        assert isinstance(ASSIGNMENT_MESSAGE_TEMPLATE, str)
        assert isinstance(CONSOLIDATION_MESSAGE_TEMPLATE, str)

    def test_templates_not_empty(self):
        """Test all templates are not empty."""
        assert len(CLI_HELP_EPILOG) > 0
        assert len(SURVEY_MESSAGE_TEMPLATE) > 0
        assert len(ASSIGNMENT_MESSAGE_TEMPLATE) > 0
        assert len(CONSOLIDATION_MESSAGE_TEMPLATE) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
