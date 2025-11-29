"""
Unit tests for soft_onboarding_handler.py
Target: ≥85% coverage
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from src.services.handlers.soft_onboarding_handler import SoftOnboardingHandler


class TestSoftOnboardingHandler:
    """Tests for SoftOnboardingHandler class."""

    def test_init(self):
        """Test SoftOnboardingHandler initialization."""
        handler = SoftOnboardingHandler()
        assert handler.exit_code == 0

    def test_can_handle_soft_onboarding_flag(self):
        """Test can_handle returns True for soft_onboarding flag."""
        handler = SoftOnboardingHandler()
        args = Mock(soft_onboarding=True, onboarding_step=None)
        assert handler.can_handle(args) is True

    def test_can_handle_onboarding_step_flag(self):
        """Test can_handle returns True for onboarding_step flag."""
        handler = SoftOnboardingHandler()
        args = Mock(soft_onboarding=False, onboarding_step=1)
        assert handler.can_handle(args) is True

    def test_can_handle_false(self):
        """Test can_handle returns False when no flags set."""
        handler = SoftOnboardingHandler()
        args = Mock(spec=[])
        assert handler.can_handle(args) is False

    def test_load_full_onboarding_template_success(self):
        """Test _load_full_onboarding_template loads template successfully."""
        handler = SoftOnboardingHandler()
        
        template_content = "Template with {agent_id} and {role}"
        
        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.read_text', return_value=template_content):
                result = handler._load_full_onboarding_template(
                    agent_id="Agent-1",
                    role="Test Role",
                    custom_message="Custom message"
                )
                
                assert "Custom message" in result
                assert "Agent-1" in result
                assert "Test Role" in result

    def test_load_full_onboarding_template_no_custom_message(self):
        """Test _load_full_onboarding_template without custom message."""
        handler = SoftOnboardingHandler()
        
        template_content = "Template with {agent_id} and {role}"
        
        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.read_text', return_value=template_content):
                result = handler._load_full_onboarding_template(
                    agent_id="Agent-1",
                    role="Test Role",
                    custom_message=""
                )
                
                assert result == template_content.replace("{agent_id}", "Agent-1").replace("{role}", "Test Role")

    def test_load_full_onboarding_template_not_found(self):
        """Test _load_full_onboarding_template handles missing template."""
        handler = SoftOnboardingHandler()
        
        with patch('pathlib.Path.exists', return_value=False):
            result = handler._load_full_onboarding_template(
                agent_id="Agent-1",
                role="Test Role",
                custom_message="Custom message"
            )
            
            assert result == "Custom message"

    def test_load_full_onboarding_template_exception(self):
        """Test _load_full_onboarding_template handles exceptions."""
        handler = SoftOnboardingHandler()
        
        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.read_text', side_effect=Exception("Read error")):
                result = handler._load_full_onboarding_template(
                    agent_id="Agent-1",
                    role="Test Role",
                    custom_message="Custom message"
                )
                
                assert result == "Custom message"

    def test_handle_missing_agent(self):
        """Test handle returns error when agent missing."""
        handler = SoftOnboardingHandler()
        args = Mock(agent=None, onboarding_step=None, message=None, onboarding_file=None)
        
        result = handler.handle(args)
        assert result is True
        assert handler.exit_code == 1

    def test_handle_missing_message_and_file(self):
        """Test handle returns error when message and file missing."""
        handler = SoftOnboardingHandler()
        args = Mock(agent="Agent-1", onboarding_step=None, message=None, onboarding_file=None)
        
        result = handler.handle(args)
        assert result is True
        assert handler.exit_code == 1

    def test_handle_load_from_file(self):
        """Test handle loads message from file."""
        handler = SoftOnboardingHandler()
        args = Mock(
            agent="Agent-1",
            onboarding_step=None,
            message=None,
            onboarding_file="test.md",
            role=None,
            dry_run=False
        )
        
        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.read_text', return_value="File content"):
                with patch('src.services.handlers.soft_onboarding_handler.SoftOnboardingService') as mock_service:
                    mock_svc = Mock()
                    mock_svc.execute_soft_onboarding.return_value = True
                    mock_service.return_value = mock_svc
                    
                    result = handler.handle(args)
                    assert result is True

    def test_handle_file_not_found(self):
        """Test handle handles file not found."""
        handler = SoftOnboardingHandler()
        args = Mock(
            agent="Agent-1",
            onboarding_step=None,
            message=None,
            onboarding_file="nonexistent.md",
            role=None
        )
        
        with patch('pathlib.Path.exists', return_value=False):
            result = handler.handle(args)
            assert result is True
            assert handler.exit_code == 1

    def test_handle_file_read_error(self):
        """Test handle handles file read error."""
        handler = SoftOnboardingHandler()
        args = Mock(
            agent="Agent-1",
            onboarding_step=None,
            message=None,
            onboarding_file="test.md",
            role=None
        )
        
        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.read_text', side_effect=Exception("Read error")):
                result = handler.handle(args)
                assert result is True
                assert handler.exit_code == 1

    def test_handle_dry_run(self):
        """Test handle handles dry run."""
        handler = SoftOnboardingHandler()
        args = Mock(
            agent="Agent-1",
            onboarding_step=None,
            message="Test message",
            onboarding_file=None,
            role="Test Role",
            dry_run=True
        )
        
        result = handler.handle(args)
        assert result is True
        assert handler.exit_code == 0

    def test_handle_single_step_step1(self):
        """Test handle executes step 1."""
        handler = SoftOnboardingHandler()
        args = Mock(
            agent="Agent-1",
            onboarding_step=1,
            message=None,
            onboarding_file=None,
            role=None,
            dry_run=False
        )
        
        with patch('src.services.handlers.soft_onboarding_handler.SoftOnboardingService') as mock_service:
            mock_svc = Mock()
            mock_svc.step_1_click_chat_input.return_value = True
            mock_service.return_value = mock_svc
            
            result = handler.handle(args)
            assert result is True
            assert handler.exit_code == 0

    def test_handle_single_step_step2(self):
        """Test handle executes step 2."""
        handler = SoftOnboardingHandler()
        args = Mock(
            agent=None,
            onboarding_step=2,
            message=None,
            onboarding_file=None,
            role=None,
            dry_run=False
        )
        
        with patch('src.services.handlers.soft_onboarding_handler.SoftOnboardingService') as mock_service:
            mock_svc = Mock()
            mock_svc.step_2_save_session.return_value = True
            mock_service.return_value = mock_svc
            
            result = handler.handle(args)
            assert result is True
            assert handler.exit_code == 0

    def test_handle_single_step_step3(self):
        """Test handle executes step 3."""
        handler = SoftOnboardingHandler()
        args = Mock(
            agent="Agent-1",
            onboarding_step=3,
            message=None,
            onboarding_file=None,
            role=None,
            cleanup_message="Cleanup message",
            dry_run=False
        )
        
        with patch('src.services.handlers.soft_onboarding_handler.SoftOnboardingService') as mock_service:
            mock_svc = Mock()
            mock_svc.step_3_send_cleanup_prompt.return_value = True
            mock_service.return_value = mock_svc
            
            result = handler.handle(args)
            assert result is True
            assert handler.exit_code == 0

    def test_handle_single_step_step4(self):
        """Test handle executes step 4."""
        handler = SoftOnboardingHandler()
        args = Mock(
            agent=None,
            onboarding_step=4,
            message=None,
            onboarding_file=None,
            role=None,
            dry_run=False
        )
        
        with patch('src.services.handlers.soft_onboarding_handler.SoftOnboardingService') as mock_service:
            mock_svc = Mock()
            mock_svc.step_4_open_new_tab.return_value = True
            mock_service.return_value = mock_svc
            
            result = handler.handle(args)
            assert result is True
            assert handler.exit_code == 0

    def test_handle_single_step_step5(self):
        """Test handle executes step 5."""
        handler = SoftOnboardingHandler()
        args = Mock(
            agent="Agent-1",
            onboarding_step=5,
            message=None,
            onboarding_file=None,
            role=None,
            dry_run=False
        )
        
        with patch('src.services.handlers.soft_onboarding_handler.SoftOnboardingService') as mock_service:
            mock_svc = Mock()
            mock_svc.step_5_navigate_to_onboarding.return_value = True
            mock_service.return_value = mock_svc
            
            result = handler.handle(args)
            assert result is True
            assert handler.exit_code == 0

    def test_handle_single_step_step6(self):
        """Test handle executes step 6."""
        handler = SoftOnboardingHandler()
        args = Mock(
            agent="Agent-1",
            onboarding_step=6,
            message="Test message",
            onboarding_file=None,
            role=None,
            dry_run=False
        )
        
        with patch('src.services.handlers.soft_onboarding_handler.SoftOnboardingService') as mock_service:
            mock_svc = Mock()
            mock_svc.step_6_paste_onboarding_message.return_value = True
            mock_service.return_value = mock_svc
            
            result = handler.handle(args)
            assert result is True
            assert handler.exit_code == 0

    def test_handle_single_step_step3_missing_agent(self):
        """Test handle step 3 requires agent."""
        handler = SoftOnboardingHandler()
        args = Mock(
            agent=None,
            onboarding_step=3,
            message=None,
            onboarding_file=None,
            role=None,
            cleanup_message="Cleanup",
            dry_run=False
        )
        
        result = handler.handle(args)
        assert result is True
        assert handler.exit_code == 1

    def test_handle_single_step_step6_missing_message(self):
        """Test handle step 6 requires message."""
        handler = SoftOnboardingHandler()
        args = Mock(
            agent="Agent-1",
            onboarding_step=6,
            message=None,
            onboarding_file=None,
            role=None,
            dry_run=False
        )
        
        with patch('src.services.handlers.soft_onboarding_handler.SoftOnboardingService') as mock_service:
            mock_svc = Mock()
            mock_service.return_value = mock_svc
            
            result = handler.handle(args)
            assert result is True
            assert handler.exit_code == 1

    def test_handle_full_onboarding_success(self):
        """Test handle executes full onboarding successfully."""
        handler = SoftOnboardingHandler()
        args = Mock(
            agent="Agent-1",
            onboarding_step=None,
            message="Test message",
            onboarding_file=None,
            role="Test Role",
            cleanup_message=None,
            dry_run=False
        )
        
        with patch('src.services.handlers.soft_onboarding_handler.SoftOnboardingService') as mock_service:
            mock_svc = Mock()
            mock_svc.execute_soft_onboarding.return_value = True
            mock_service.return_value = mock_svc
            
            result = handler.handle(args)
            assert result is True
            assert handler.exit_code == 0

    def test_handle_full_onboarding_failure(self):
        """Test handle handles full onboarding failure."""
        handler = SoftOnboardingHandler()
        args = Mock(
            agent="Agent-1",
            onboarding_step=None,
            message="Test message",
            onboarding_file=None,
            role="Test Role",
            cleanup_message=None,
            dry_run=False
        )
        
        with patch('src.services.handlers.soft_onboarding_handler.SoftOnboardingService') as mock_service:
            mock_svc = Mock()
            mock_svc.execute_soft_onboarding.return_value = False
            mock_service.return_value = mock_svc
            
            result = handler.handle(args)
            assert result is True
            assert handler.exit_code == 1

    def test_handle_import_error(self):
        """Test handle handles ImportError."""
        handler = SoftOnboardingHandler()
        args = Mock(agent="Agent-1", message="Test")
        
        with patch('src.services.handlers.soft_onboarding_handler.SoftOnboardingService', side_effect=ImportError("Service not available")):
            result = handler.handle(args)
            assert result is True
            assert handler.exit_code == 1

    def test_handle_general_exception(self):
        """Test handle handles general exceptions."""
        handler = SoftOnboardingHandler()
        args = Mock(agent="Agent-1", message="Test")
        
        with patch('src.services.handlers.soft_onboarding_handler.SoftOnboardingService', side_effect=Exception("General error")):
            result = handler.handle(args)
            assert result is True
            assert handler.exit_code == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

