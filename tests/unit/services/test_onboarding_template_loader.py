"""
Tests for onboarding_template_loader.py

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-11-27
"""

import pytest
from unittest.mock import Mock, patch, mock_open
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))

from src.services.onboarding_template_loader import (
    OnboardingTemplateLoader,
    load_onboarding_template
)


class TestOnboardingTemplateLoader:
    """Test OnboardingTemplateLoader class."""

    def test_init_sets_template_path(self):
        """Test that __init__ sets correct template path."""
        loader = OnboardingTemplateLoader()
        assert loader.template_path is not None
        assert "prompts" in str(loader.template_path)
        assert "agents" in str(loader.template_path)
        assert "onboarding.md" in str(loader.template_path)

    @patch("src.services.onboarding_template_loader.Path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data="Test template content")
    def test_load_full_template_success(self, mock_file, mock_exists):
        """Test loading template when file exists."""
        mock_exists.return_value = True
        loader = OnboardingTemplateLoader()
        
        result = loader.load_full_template()
        
        assert result == "Test template content"
        mock_file.assert_called_once()
        assert "utf-8" in str(mock_file.call_args)

    @patch("src.services.onboarding_template_loader.Path.exists")
    def test_load_full_template_missing_file(self, mock_exists):
        """Test loading template when file doesn't exist."""
        mock_exists.return_value = False
        loader = OnboardingTemplateLoader()
        
        result = loader.load_full_template()
        
        assert result == ""

    @patch("src.services.onboarding_template_loader.Path.exists")
    @patch("builtins.open", side_effect=IOError("Permission denied"))
    def test_load_full_template_io_error(self, mock_file, mock_exists):
        """Test loading template when IO error occurs."""
        mock_exists.return_value = True
        loader = OnboardingTemplateLoader()
        
        result = loader.load_full_template()
        
        assert result == ""

    @patch.object(OnboardingTemplateLoader, "load_full_template")
    def test_create_onboarding_message_with_template(self, mock_load):
        """Test creating message when template exists."""
        template = "Hello {agent_id}, you are {role}. Mission: {custom_message}"
        mock_load.return_value = template
        loader = OnboardingTemplateLoader()
        
        result = loader.create_onboarding_message(
            agent_id="Agent-1",
            role="Test Specialist",
            custom_message="Test mission"
        )
        
        assert "Agent-1" in result
        assert "Test Specialist" in result
        assert "Test mission" in result
        assert "{agent_id}" not in result
        assert "{role}" not in result

    @patch.object(OnboardingTemplateLoader, "load_full_template")
    def test_create_onboarding_message_without_template(self, mock_load):
        """Test creating message when template is missing."""
        mock_load.return_value = ""
        loader = OnboardingTemplateLoader()
        
        result = loader.create_onboarding_message(
            agent_id="Agent-1",
            role="Test Specialist",
            custom_message="Test mission"
        )
        
        assert "Agent-1" in result
        assert "Test Specialist" in result
        assert "Test mission" in result
        assert "AGENT IDENTITY CONFIRMATION" in result
        assert "WE. ARE. SWARM" in result

    @patch.object(OnboardingTemplateLoader, "load_full_template")
    def test_create_onboarding_message_with_contract_info(self, mock_load):
        """Test creating message with contract info."""
        template = "Contract: {contract_info}"
        mock_load.return_value = template
        loader = OnboardingTemplateLoader()
        
        result = loader.create_onboarding_message(
            agent_id="Agent-1",
            role="Test Specialist",
            custom_message="Test mission",
            contract_info="Contract-123"
        )
        
        assert "Contract-123" in result
        assert "{contract_info}" not in result

    @patch.object(OnboardingTemplateLoader, "load_full_template")
    def test_create_onboarding_message_empty_contract_info(self, mock_load):
        """Test creating message with empty contract info."""
        template = "Contract: {contract_info}"
        mock_load.return_value = template
        loader = OnboardingTemplateLoader()
        
        result = loader.create_onboarding_message(
            agent_id="Agent-1",
            role="Test Specialist",
            custom_message="Test mission",
            contract_info=""
        )
        
        assert "See custom instructions below" in result

    @patch.object(OnboardingTemplateLoader, "load_full_template")
    def test_create_onboarding_message_empty_custom_message(self, mock_load):
        """Test creating message with empty custom message."""
        template = "Mission: {custom_message}"
        mock_load.return_value = template
        loader = OnboardingTemplateLoader()
        
        result = loader.create_onboarding_message(
            agent_id="Agent-1",
            role="Test Specialist",
            custom_message=""
        )
        
        assert "No additional instructions" in result

    def test_format_custom_message(self):
        """Test _format_custom_message fallback formatter."""
        loader = OnboardingTemplateLoader()
        
        result = loader._format_custom_message(
            agent_id="Agent-1",
            role="Test Specialist",
            custom_message="Test mission"
        )
        
        assert "Agent-1" in result
        assert "Test Specialist" in result
        assert "Test mission" in result
        assert "AGENT IDENTITY CONFIRMATION" in result
        assert "WE. ARE. SWARM" in result


class TestLoadOnboardingTemplateFunction:
    """Test load_onboarding_template convenience function."""

    @patch("src.services.onboarding_template_loader.OnboardingTemplateLoader")
    def test_load_onboarding_template_calls_loader(self, mock_loader_class):
        """Test that convenience function creates loader and calls method."""
        mock_loader = Mock()
        mock_loader.create_onboarding_message.return_value = "Test message"
        mock_loader_class.return_value = mock_loader
        
        result = load_onboarding_template(
            agent_id="Agent-1",
            role="Test Specialist",
            custom_message="Test mission"
        )
        
        assert result == "Test message"
        mock_loader_class.assert_called_once()
        mock_loader.create_onboarding_message.assert_called_once_with(
            "Agent-1",
            "Test Specialist",
            "Test mission",
            ""
        )

    @patch("src.services.onboarding_template_loader.OnboardingTemplateLoader")
    def test_load_onboarding_template_with_contract_info(self, mock_loader_class):
        """Test convenience function with contract info."""
        mock_loader = Mock()
        mock_loader.create_onboarding_message.return_value = "Test message"
        mock_loader_class.return_value = mock_loader
        
        result = load_onboarding_template(
            agent_id="Agent-1",
            role="Test Specialist",
            custom_message="Test mission",
            contract_info="Contract-123"
        )
        
        assert result == "Test message"
        mock_loader.create_onboarding_message.assert_called_once_with(
            "Agent-1",
            "Test Specialist",
            "Test mission",
            "Contract-123"
        )

    @patch("src.services.onboarding_template_loader.Path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data="Template with {agent_id} and {role}")
    def test_create_onboarding_message_placeholder_replacement(self, mock_file, mock_exists):
        """Test placeholder replacement in template."""
        mock_exists.return_value = True
        loader = OnboardingTemplateLoader()
        
        result = loader.create_onboarding_message(
            agent_id="Agent-7",
            role="Web Developer",
            custom_message="Build features"
        )
        
        assert "Agent-7" in result
        assert "Web Developer" in result
        assert "{agent_id}" not in result
        assert "{role}" not in result

    @patch("src.services.onboarding_template_loader.Path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data="Template")
    def test_create_onboarding_message_template_length_logging(self, mock_file, mock_exists):
        """Test that template length is logged."""
        mock_exists.return_value = True
        loader = OnboardingTemplateLoader()
        
        with patch('src.services.onboarding_template_loader.logger') as mock_logger:
            loader.create_onboarding_message("Agent-1", "Role", "Message")
            # Verify logging occurred
            assert mock_logger.info.called

    @patch.object(OnboardingTemplateLoader, "load_full_template")
    def test_create_onboarding_message_all_placeholders(self, mock_load):
        """Test all placeholder replacements."""
        template = "Agent: {agent_id}, Role: {role}, Contract: {contract_info}, Custom: {custom_message}"
        mock_load.return_value = template
        loader = OnboardingTemplateLoader()
        
        result = loader.create_onboarding_message(
            agent_id="Agent-1",
            role="Specialist",
            custom_message="Mission",
            contract_info="C-123"
        )
        
        assert "Agent-1" in result
        assert "Specialist" in result
        assert "C-123" in result
        assert "Mission" in result
        assert "{agent_id}" not in result
        assert "{role}" not in result
        assert "{contract_info}" not in result
        assert "{custom_message}" not in result

    def test_project_root_path(self):
        """Test that project_root is correctly set."""
        loader = OnboardingTemplateLoader()
        
        assert loader.project_root is not None
        assert isinstance(loader.project_root, Path)

    @patch("src.services.onboarding_template_loader.Path.exists")
    @patch("builtins.open", side_effect=PermissionError("Access denied"))
    def test_load_full_template_permission_error(self, mock_file, mock_exists):
        """Test loading template with permission error."""
        mock_exists.return_value = True
        loader = OnboardingTemplateLoader()
        
        result = loader.load_full_template()
        
        assert result == ""

    @patch("src.services.onboarding_template_loader.Path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_load_full_template_empty_file(self, mock_file, mock_exists):
        """Test loading empty template file."""
        mock_exists.return_value = True
        loader = OnboardingTemplateLoader()
        
        result = loader.load_full_template()
        
        assert result == ""

    @patch.object(OnboardingTemplateLoader, "load_full_template")
    def test_create_onboarding_message_no_role(self, mock_load):
        """Test creating message without role."""
        template = "Agent: {agent_id}"
        mock_load.return_value = template
        loader = OnboardingTemplateLoader()
        
        result = loader.create_onboarding_message(
            agent_id="Agent-1",
            role="",
            custom_message="Test"
        )
        
        assert "Agent-1" in result

    def test_format_custom_message_structure(self):
        """Test _format_custom_message structure."""
        loader = OnboardingTemplateLoader()
        
        result = loader._format_custom_message(
            agent_id="Agent-1",
            role="Test Role",
            custom_message="Test Mission"
        )
        
        assert "AGENT IDENTITY CONFIRMATION" in result
        assert "Agent-1" in result
        assert "Test Role" in result
        assert "Test Mission" in result
        assert "WE. ARE. SWARM" in result
        assert "ONBOARDING_GUIDE" in result

    @patch("src.services.onboarding_template_loader.OnboardingTemplateLoader")
    def test_load_onboarding_template_empty_parameters(self, mock_loader_class):
        """Test convenience function with empty parameters."""
        mock_loader = Mock()
        mock_loader.create_onboarding_message.return_value = "Message"
        mock_loader_class.return_value = mock_loader
        
        result = load_onboarding_template(
            agent_id="Agent-1",
            role="",
            custom_message="",
            contract_info=""
        )
        
        assert result == "Message"
        mock_loader.create_onboarding_message.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

