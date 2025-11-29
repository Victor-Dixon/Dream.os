"""
Unit tests for onboarding_handler.py
Target: ≥85% coverage
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.services.handlers.onboarding_handler import OnboardingHandler


class TestOnboardingHandler:
    """Tests for OnboardingHandler class."""

    def test_init(self):
        """Test OnboardingHandler initialization."""
        handler = OnboardingHandler()
        assert handler.exit_code == 0

    def test_can_handle_onboarding_flag(self):
        """Test can_handle returns True for onboarding flag."""
        handler = OnboardingHandler()
        args = Mock(onboarding=True, onboard=False, hard_onboarding=False)
        assert handler.can_handle(args) is True

    def test_can_handle_onboard_flag(self):
        """Test can_handle returns True for onboard flag."""
        handler = OnboardingHandler()
        args = Mock(onboarding=False, onboard=True, hard_onboarding=False)
        assert handler.can_handle(args) is True

    def test_can_handle_hard_onboarding_flag(self):
        """Test can_handle returns True for hard_onboarding flag."""
        handler = OnboardingHandler()
        args = Mock(onboarding=False, onboard=False, hard_onboarding=True)
        assert handler.can_handle(args) is True

    def test_can_handle_false(self):
        """Test can_handle returns False when no flags set."""
        handler = OnboardingHandler()
        args = Mock(spec=[])  # No attributes
        assert handler.can_handle(args) is False

    def test_handle_calls_handle_onboarding_commands(self):
        """Test handle calls handle_onboarding_commands."""
        handler = OnboardingHandler()
        args = Mock(hard_onboarding=True, yes=True, dry_run=False, agent_subset=None, agents=None, timeout=60, ui=False, ui_retries=3, ui_tolerance=5, onboarding_mode="test", assign_roles=None, proof=False)
        
        with patch.object(handler, 'handle_onboarding_commands', return_value=True) as mock_handle:
            result = handler.handle(args)
            assert result is True
            mock_handle.assert_called_once_with(args)

    def test_derive_role_map_from_string(self):
        """Test _derive_role_map parses role map string."""
        handler = OnboardingHandler()
        
        with patch('src.services.handlers.onboarding_handler.ROLES', {'SOLID': 'SOLID', 'SSOT': 'SSOT'}):
            result = handler._derive_role_map(
                agent_ids=["Agent-1", "Agent-2"],
                mode="test",
                role_map_str="Agent-1:SOLID,Agent-2:SSOT"
            )
            assert result == {"Agent-1": "SOLID", "Agent-2": "SSOT"}

    def test_derive_role_map_invalid_role(self):
        """Test _derive_role_map raises ValueError for invalid role."""
        handler = OnboardingHandler()
        
        with patch('src.services.handlers.onboarding_handler.ROLES', {'SOLID': 'SOLID'}):
            with pytest.raises(ValueError, match="Unknown role"):
                handler._derive_role_map(
                    agent_ids=["Agent-1"],
                    mode="test",
                    role_map_str="Agent-1:INVALID"
                )

    def test_derive_role_map_quality_suite_mode(self):
        """Test _derive_role_map uses quality-suite cycle."""
        handler = OnboardingHandler()
        
        result = handler._derive_role_map(
            agent_ids=["Agent-1", "Agent-2", "Agent-3"],
            mode="quality-suite",
            role_map_str=None
        )
        assert result["Agent-1"] == "SOLID"
        assert result["Agent-2"] == "SSOT"
        assert result["Agent-3"] == "DRY"

    def test_derive_role_map_other_mode(self):
        """Test _derive_role_map uses mode for single role."""
        handler = OnboardingHandler()
        
        result = handler._derive_role_map(
            agent_ids=["Agent-1", "Agent-2"],
            mode="test-mode",
            role_map_str=None
        )
        assert result["Agent-1"] == "TEST-MODE"
        assert result["Agent-2"] == "TEST-MODE"

    def test_derive_role_map_empty_string(self):
        """Test _derive_role_map handles empty role map string."""
        handler = OnboardingHandler()
        
        result = handler._derive_role_map(
            agent_ids=["Agent-1"],
            mode="test",
            role_map_str=""
        )
        assert result["Agent-1"] == "TEST"

    def test_handle_onboarding_commands_no_hard_onboarding(self):
        """Test handle_onboarding_commands returns False when not hard onboarding."""
        handler = OnboardingHandler()
        args = Mock(hard_onboarding=False)
        
        result = handler.handle_onboarding_commands(args)
        assert result is False

    def test_handle_onboarding_commands_no_agents(self):
        """Test handle_onboarding_commands returns 1 when no agents found."""
        handler = OnboardingHandler()
        args = Mock(
            hard_onboarding=True,
            yes=True,
            dry_run=False,
            agent_subset=None,
            agents=None,
            timeout=60,
            ui=False,
            ui_retries=3,
            ui_tolerance=5,
            onboarding_mode="test",
            assign_roles=None,
            proof=False
        )
        
        with patch('src.services.handlers.onboarding_handler.AgentRegistry') as mock_registry:
            mock_reg = Mock()
            mock_reg.list_agents.return_value = []
            mock_registry.return_value = mock_reg
            
            result = handler.handle_onboarding_commands(args)
            assert result == 1

    def test_handle_onboarding_commands_role_mapping_error(self):
        """Test handle_onboarding_commands handles role mapping error."""
        handler = OnboardingHandler()
        args = Mock(
            hard_onboarding=True,
            yes=True,
            dry_run=False,
            agent_subset=None,
            agents=None,
            timeout=60,
            ui=False,
            ui_retries=3,
            ui_tolerance=5,
            onboarding_mode="test",
            assign_roles="Invalid:Role",
            proof=False
        )
        
        with patch('src.services.handlers.onboarding_handler.AgentRegistry') as mock_registry:
            mock_reg = Mock()
            mock_reg.list_agents.return_value = ["Agent-1"]
            mock_registry.return_value = mock_reg
            
            with patch('src.services.handlers.onboarding_handler.ROLES', {}):
                result = handler.handle_onboarding_commands(args)
                assert result == 1

    def test_handle_onboarding_commands_user_abort(self):
        """Test handle_onboarding_commands handles user abort."""
        handler = OnboardingHandler()
        args = Mock(
            hard_onboarding=True,
            yes=False,
            dry_run=False,
            agent_subset=None,
            agents=None,
            timeout=60,
            ui=False,
            ui_retries=3,
            ui_tolerance=5,
            onboarding_mode="test",
            assign_roles=None,
            proof=False
        )
        
        with patch('src.services.handlers.onboarding_handler.AgentRegistry') as mock_registry:
            mock_reg = Mock()
            mock_reg.list_agents.return_value = ["Agent-1"]
            mock_registry.return_value = mock_reg
            
            with patch('src.services.handlers.onboarding_handler.confirm', return_value=False):
                result = handler.handle_onboarding_commands(args)
                assert result == 1

    def test_handle_onboarding_commands_backup_failure(self):
        """Test handle_onboarding_commands handles backup failure."""
        handler = OnboardingHandler()
        args = Mock(
            hard_onboarding=True,
            yes=True,
            dry_run=False,
            agent_subset=None,
            agents=None,
            timeout=60,
            ui=False,
            ui_retries=3,
            ui_tolerance=5,
            onboarding_mode="test",
            assign_roles=None,
            proof=False,
            audit_cleanup=False
        )
        
        with patch('src.services.handlers.onboarding_handler.AgentRegistry') as mock_registry:
            mock_reg = Mock()
            mock_reg.list_agents.return_value = ["Agent-1"]
            mock_registry.return_value = mock_reg
            
            with patch('src.services.handlers.onboarding_handler.BackupManager') as mock_backup:
                mock_bm = Mock()
                mock_bm.create_backup.side_effect = Exception("Backup failed")
                mock_backup.return_value = mock_bm
                
                result = handler.handle_onboarding_commands(args)
                assert result == 1

    def test_handle_onboarding_commands_dry_run(self):
        """Test handle_onboarding_commands handles dry run."""
        handler = OnboardingHandler()
        args = Mock(
            hard_onboarding=True,
            yes=True,
            dry_run=True,
            agent_subset=None,
            agents=None,
            timeout=60,
            ui=False,
            ui_retries=3,
            ui_tolerance=5,
            onboarding_mode="test",
            assign_roles=None,
            proof=False,
            audit_cleanup=False
        )
        
        with patch('src.services.handlers.onboarding_handler.AgentRegistry') as mock_registry:
            mock_reg = Mock()
            mock_reg.list_agents.return_value = ["Agent-1"]
            mock_registry.return_value = mock_reg
            
            with patch('src.services.handlers.onboarding_handler.BackupManager'):
                with patch('src.services.handlers.onboarding_handler.build_role_message', return_value="Test message"):
                    with patch.object(mock_reg, 'verify_onboarded', return_value=True):
                        result = handler.handle_onboarding_commands(args)
                        assert result == 0

    def test_handle_onboarding_commands_ui_unavailable(self):
        """Test handle_onboarding_commands handles UI unavailable."""
        handler = OnboardingHandler()
        args = Mock(
            hard_onboarding=True,
            yes=True,
            dry_run=False,
            agent_subset=None,
            agents=None,
            timeout=60,
            ui=True,
            ui_retries=3,
            ui_tolerance=5,
            onboarding_mode="test",
            assign_roles=None,
            proof=False,
            audit_cleanup=False
        )
        
        with patch('src.services.handlers.onboarding_handler.AgentRegistry') as mock_registry:
            mock_reg = Mock()
            mock_reg.list_agents.return_value = ["Agent-1"]
            mock_registry.return_value = mock_reg
            
            with patch('src.services.handlers.onboarding_handler.BackupManager'):
                with patch('src.services.handlers.onboarding_handler.UIOnboarder') as mock_ui:
                    from src.automation.ui_onboarding import UIUnavailableError
                    mock_ui.side_effect = UIUnavailableError("UI unavailable")
                    
                    result = handler.handle_onboarding_commands(args)
                    assert result == 1

    def test_handle_onboarding_commands_agent_subset(self):
        """Test handle_onboarding_commands uses agent_subset when provided."""
        handler = OnboardingHandler()
        args = Mock(
            hard_onboarding=True,
            yes=True,
            dry_run=True,
            agent_subset="Agent-1,Agent-2",
            agents=None,
            timeout=60,
            ui=False,
            ui_retries=3,
            ui_tolerance=5,
            onboarding_mode="test",
            assign_roles=None,
            proof=False,
            audit_cleanup=False
        )
        
        with patch('src.services.handlers.onboarding_handler.AgentRegistry') as mock_registry:
            mock_reg = Mock()
            mock_registry.return_value = mock_reg
            
            with patch('src.services.handlers.onboarding_handler.BackupManager'):
                with patch('src.services.handlers.onboarding_handler.build_role_message', return_value="Test"):
                    with patch.object(mock_reg, 'verify_onboarded', return_value=True):
                        handler.handle_onboarding_commands(args)
                        # Verify agent_subset was parsed
                        assert args.agent_subset == "Agent-1,Agent-2"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

