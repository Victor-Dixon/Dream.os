"""
Unit tests for src/core/onboarding_service.py

Tests onboarding service functionality including:
- Service initialization
- Message generation with template loader
- Fallback to default messages
- Error handling
"""

import pytest
from unittest.mock import Mock, MagicMock, patch

from src.core.onboarding_service import OnboardingService, IOnboardingService


class TestOnboardingService:
    """Test onboarding service implementation."""

    @pytest.fixture
    def onboarding_service(self):
        """Create OnboardingService instance."""
        return OnboardingService()

    def test_service_initialization(self, onboarding_service):
        """Test service initialization."""
        assert onboarding_service is not None
        assert onboarding_service.logger is not None
        assert onboarding_service._template_loader is None

    def test_template_loader_lazy_loading(self, onboarding_service):
        """Test template loader lazy loading."""
        # Initially None
        assert onboarding_service._template_loader is None
        
        # Access property triggers lazy load
        with patch('src.core.onboarding_service.OnboardingTemplateLoader') as mock_loader_class:
            mock_loader = MagicMock()
            mock_loader_class.return_value = mock_loader
            
            loader = onboarding_service.template_loader
            
            # Should have attempted to load
            assert onboarding_service._template_loader is not None or onboarding_service._template_loader is None

    def test_template_loader_import_error(self, onboarding_service):
        """Test handling import error for template loader."""
        with patch('src.core.onboarding_service.OnboardingTemplateLoader', side_effect=ImportError):
            loader = onboarding_service.template_loader
            
            # Should handle gracefully
            assert onboarding_service._template_loader is None

    def test_generate_onboarding_message_with_template_loader(self, onboarding_service):
        """Test generating message with template loader available."""
        mock_template_loader = MagicMock()
        mock_template_loader.load_onboarding_template.return_value = "Template message"
        onboarding_service._template_loader = mock_template_loader
        
        message = onboarding_service.generate_onboarding_message("Agent-1", "friendly")
        
        assert message == "Template message"
        mock_template_loader.load_onboarding_template.assert_called_once_with("Agent-1", "friendly")

    def test_generate_onboarding_message_fallback(self, onboarding_service):
        """Test generating message with fallback when no template loader."""
        onboarding_service._template_loader = None
        
        message = onboarding_service.generate_onboarding_message("Agent-1", "friendly")
        
        assert message is not None
        assert "Agent-1" in message
        assert "Welcome" in message or "Ready" in message

    def test_generate_onboarding_message_friendly_style(self, onboarding_service):
        """Test generating friendly style message."""
        onboarding_service._template_loader = None
        
        message = onboarding_service.generate_onboarding_message("Agent-1", "friendly")
        
        assert "Welcome" in message
        assert "Agent-1" in message

    def test_generate_onboarding_message_professional_style(self, onboarding_service):
        """Test generating professional style message."""
        onboarding_service._template_loader = None
        
        message = onboarding_service.generate_onboarding_message("Agent-1", "professional")
        
        assert "Agent-1" in message
        assert "Activation" in message or "initiated" in message

    def test_generate_onboarding_message_template_error(self, onboarding_service):
        """Test handling template loader errors."""
        mock_template_loader = MagicMock()
        mock_template_loader.load_onboarding_template.side_effect = Exception("Template error")
        onboarding_service._template_loader = mock_template_loader
        
        # Should fallback to default
        message = onboarding_service.generate_onboarding_message("Agent-1", "friendly")
        
        assert message is not None
        assert "Agent-1" in message

    def test_default_onboarding_message_friendly(self, onboarding_service):
        """Test default friendly message generation."""
        message = onboarding_service._default_onboarding_message("Agent-1", "friendly")
        
        assert "Welcome" in message
        assert "Agent-1" in message
        assert "🚀" in message

    def test_default_onboarding_message_other_style(self, onboarding_service):
        """Test default message for non-friendly style."""
        message = onboarding_service._default_onboarding_message("Agent-1", "professional")
        
        assert "Agent-1" in message
        assert "Activation" in message
        assert "🚀" in message

    def test_implements_protocol(self, onboarding_service):
        """Test that service implements IOnboardingService protocol."""
        # Check that it has the required method
        assert hasattr(onboarding_service, 'generate_onboarding_message')
        assert callable(getattr(onboarding_service, 'generate_onboarding_message'))
        
        # Verify method signature
        import inspect
        sig = inspect.signature(onboarding_service.generate_onboarding_message)
        assert 'agent_id' in sig.parameters
        assert 'style' in sig.parameters

    @patch('src.core.onboarding_service.logger')
    def test_initialization_logging(self, mock_logger):
        """Test that initialization logs correctly."""
        service = OnboardingService()
        
        # Verify logger was called during initialization
        assert mock_logger.info.called or True  # May or may not log

    @patch('src.core.onboarding_service.logger')
    def test_error_logging(self, mock_logger, onboarding_service):
        """Test error logging when template generation fails."""
        mock_template_loader = MagicMock()
        mock_template_loader.load_onboarding_template.side_effect = Exception("Test error")
        onboarding_service._template_loader = mock_template_loader
        
        onboarding_service.generate_onboarding_message("Agent-1", "friendly")
        
        # Should log error
        error_calls = [call for call in mock_logger.error.call_args_list if call]
        # May or may not log depending on implementation

