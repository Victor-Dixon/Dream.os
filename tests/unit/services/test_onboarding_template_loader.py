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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

