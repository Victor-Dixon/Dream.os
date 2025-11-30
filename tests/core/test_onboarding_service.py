#!/usr/bin/env python3
"""
Unit tests for onboarding_service.py - Infrastructure Test Coverage

Tests OnboardingService class and onboarding message generation.
Target: ≥85% coverage, comprehensive test methods.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.onboarding_service import OnboardingService, IOnboardingService


class TestOnboardingService:
    """Test suite for OnboardingService class."""

    @pytest.fixture
    def service(self):
        """Create OnboardingService instance."""
        return OnboardingService()

    def test_initialization(self, service):
        """Test service initialization."""
        assert service is not None
        assert service.logger is not None
        assert service._template_loader is None

    def test_template_loader_lazy_loading_success(self, service):
        """Test template loader lazy loads successfully."""
        with patch('src.services.onboarding_template_loader.OnboardingTemplateLoader') as mock_loader_class:
            mock_loader = MagicMock()
            mock_loader_class.return_value = mock_loader
            
            loader = service.template_loader
            
            assert loader is not None
            assert service._template_loader is not None

    def test_template_loader_lazy_loading_import_error(self, service):
        """Test template loader handles import error gracefully."""
        with patch('builtins.__import__', side_effect=ImportError("Module not found")):
            loader = service.template_loader
            
            assert loader is None
            assert service._template_loader is None

    def test_template_loader_cached_after_first_access(self, service):
        """Test template loader is cached after first access."""
        with patch('src.services.onboarding_template_loader.OnboardingTemplateLoader') as mock_loader_class:
            mock_loader = MagicMock()
            mock_loader_class.return_value = mock_loader
            
            loader1 = service.template_loader
            loader2 = service.template_loader
            
            # Should only be called once (cached)
            assert mock_loader_class.call_count == 1
            assert loader1 is loader2

    def test_generate_onboarding_message_with_template_loader(self, service):
        """Test generating message with template loader available."""
        mock_loader = MagicMock()
        mock_loader.load_onboarding_template.return_value = "Custom template message"
        service._template_loader = mock_loader
        
        message = service.generate_onboarding_message("Agent-1", "friendly")
        
        assert message == "Custom template message"
        mock_loader.load_onboarding_template.assert_called_once_with("Agent-1", "friendly")

    def test_generate_onboarding_message_fallback_default_friendly(self, service):
        """Test generating message falls back to default friendly message."""
        service._template_loader = None
        
        message = service.generate_onboarding_message("Agent-1", "friendly")
        
        assert "Welcome Agent-1" in message
        assert "Ready to get started" in message

    def test_generate_onboarding_message_fallback_default_professional(self, service):
        """Test generating message falls back to default professional message."""
        service._template_loader = None
        
        message = service.generate_onboarding_message("Agent-1", "professional")
        
        assert "Agent-1" in message
        assert "Activation initiated" in message

    def test_generate_onboarding_message_default_style(self, service):
        """Test generating message uses default style when not specified."""
        service._template_loader = None
        
        message = service.generate_onboarding_message("Agent-1")
        
        # Default is "friendly"
        assert "Welcome Agent-1" in message

    def test_generate_onboarding_message_template_loader_exception(self, service):
        """Test generating message handles template loader exception."""
        mock_loader = MagicMock()
        mock_loader.load_onboarding_template.side_effect = Exception("Template error")
        service._template_loader = mock_loader
        
        message = service.generate_onboarding_message("Agent-1", "friendly")
        
        # Should fallback to default
        assert "Welcome Agent-1" in message

    def test_default_onboarding_message_friendly(self, service):
        """Test default message generation for friendly style."""
        message = service._default_onboarding_message("Agent-1", "friendly")
        
        assert "Welcome Agent-1" in message
        assert "Ready to get started" in message
        assert "🚀" in message

    def test_default_onboarding_message_professional(self, service):
        """Test default message generation for professional style."""
        message = service._default_onboarding_message("Agent-1", "professional")
        
        assert "Agent-1" in message
        assert "Activation initiated" in message
        assert "🚀" in message

    def test_default_onboarding_message_other_style(self, service):
        """Test default message generation for other styles."""
        message = service._default_onboarding_message("Agent-1", "other")
        
        # Should use professional format for non-friendly styles
        assert "Agent-1" in message
        assert "Activation initiated" in message

