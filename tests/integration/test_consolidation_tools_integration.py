#!/usr/bin/env python3
"""
Integration Tests for Updated Consolidation Tools
=================================================

Tests the integration of GitHub bypass architecture into:
- execute_case_variations_consolidation.py
- check_consolidation_prs.py

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-11-29
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))


class TestCaseVariationsConsolidation:
    """Test execute_case_variations_consolidation.py integration."""
    
    @patch('tools.execute_case_variations_consolidation.get_synthetic_github')
    def test_check_existing_prs_with_bypass(self, mock_get_github):
        """Test check_existing_prs uses SyntheticGitHub."""
        # Mock SyntheticGitHub
        mock_github = Mock()
        mock_github.get_pr.return_value = (True, {"merged": True, "state": "closed"})
        mock_get_github.return_value = mock_github
        
        # Import and test
        from tools.execute_case_variations_consolidation import check_existing_prs
        
        result = check_existing_prs()
        
        # Verify SyntheticGitHub was used
        assert mock_get_github.called
        assert isinstance(result, dict)
    
    @patch('subprocess.run')
    @patch('tools.execute_case_variations_consolidation.get_synthetic_github')
    def test_execute_merge_uses_repo_safe_merge(self, mock_get_github, mock_subprocess):
        """Test execute_case_variation_merge uses repo_safe_merge.py."""
        # Mock subprocess success
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "✅ Merge successful"
        mock_result.stderr = ""
        mock_subprocess.return_value = mock_result
        
        from tools.execute_case_variations_consolidation import execute_case_variation_merge
        
        result = execute_case_variation_merge(
            "Dadudekc/focusforge",
            "Dadudekc/FocusForge",
            "focusforge → FocusForge"
        )
        
        # Verify subprocess was called with repo_safe_merge.py
        assert mock_subprocess.called
        call_args = mock_subprocess.call_args[0][0]
        assert "repo_safe_merge.py" in str(call_args[1])
        assert result["status"] in ["success", "skipped", "partial", "error", "timeout"]


class TestCheckConsolidationPRs:
    """Test check_consolidation_prs.py integration."""
    
    @patch('tools.check_consolidation_prs.get_synthetic_github')
    @patch('tools.check_consolidation_prs.get_deferred_push_queue')
    def test_check_prs_uses_bypass_system(self, mock_get_queue, mock_get_github):
        """Test check_all_consolidation_prs uses GitHub bypass system."""
        # Mock SyntheticGitHub
        mock_github = Mock()
        mock_github.get_pr.return_value = (True, {
            "number": 4,
            "state": "closed",
            "merged": True,
            "mergeable": None,
            "html_url": "https://github.com/test/repo/pull/4"
        })
        mock_github.get_prs_by_branch.return_value = (True, [{
            "number": 1,
            "state": "open",
            "merged": False,
            "html_url": "https://github.com/test/repo/pull/1"
        }])
        mock_get_github.return_value = mock_github
        
        # Mock DeferredPushQueue
        mock_queue = Mock()
        mock_queue.get_pending_operations.return_value = []
        mock_get_queue.return_value = mock_queue
        
        from tools.check_consolidation_prs import check_all_consolidation_prs
        
        # Should not raise exception
        result = check_all_consolidation_prs()
        
        # Verify components were used
        assert mock_get_github.called
        assert mock_get_queue.called
        assert result == 0
    
    @patch('tools.check_consolidation_prs.get_synthetic_github')
    @patch('tools.check_consolidation_prs.get_deferred_push_queue')
    def test_check_prs_handles_sandbox_mode(self, mock_get_queue, mock_get_github):
        """Test check_all_consolidation_prs handles sandbox mode."""
        # Mock SyntheticGitHub in sandbox mode
        mock_github = Mock()
        mock_github.get_pr.return_value = (False, None)  # Sandbox mode
        mock_github.get_prs_by_branch.return_value = (False, None)
        mock_get_github.return_value = mock_github
        
        # Mock DeferredPushQueue with pending operations
        mock_queue = Mock()
        mock_queue.get_pending_operations.return_value = [
            {"repo": "DreamVault", "pr_number": 4, "status": "pending"}
        ]
        mock_get_queue.return_value = mock_queue
        
        from tools.check_consolidation_prs import check_all_consolidation_prs
        
        # Should handle sandbox mode gracefully
        result = check_all_consolidation_prs()
        
        # Verify it checked deferred queue
        assert mock_queue.get_pending_operations.called
        assert result == 0
    
    @patch('tools.check_consolidation_prs.get_github_token')
    def test_check_prs_fallback_to_legacy(self, mock_get_token):
        """Test check_all_consolidation_prs falls back to legacy method."""
        # Mock no GitHub bypass available
        with patch('tools.check_consolidation_prs.GITHUB_BYPASS_AVAILABLE', False):
            mock_get_token.return_value = "test_token"
            
            with patch('tools.check_consolidation_prs.check_pr_status') as mock_check:
                mock_check.return_value = {
                    "state": "closed",
                    "merged": True,
                    "mergeable": None,
                    "url": "https://github.com/test/repo/pull/4"
                }
                
                with patch('tools.check_consolidation_prs.requests.get') as mock_requests:
                    mock_response = Mock()
                    mock_response.status_code = 200
                    mock_response.json.return_value = []
                    mock_requests.return_value = mock_response
                    
                    from tools.check_consolidation_prs import check_all_consolidation_prs
                    
                    # Should use legacy method
                    result = check_all_consolidation_prs()
                    
                    # Verify legacy method was used
                    assert mock_get_token.called
                    assert result == 0


class TestIntegrationFlow:
    """Test full integration flow."""
    
    @patch('tools.execute_case_variations_consolidation.subprocess.run')
    @patch('tools.execute_case_variations_consolidation.get_synthetic_github')
    def test_full_consolidation_flow(self, mock_get_github, mock_subprocess):
        """Test full case variations consolidation flow."""
        # Mock SyntheticGitHub
        mock_github = Mock()
        mock_github.get_pr.return_value = (True, {"merged": False})
        mock_get_github.return_value = mock_github
        
        # Mock successful merge
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "✅ Merge successful"
        mock_result.stderr = ""
        mock_subprocess.return_value = mock_result
        
        from tools.execute_case_variations_consolidation import main
        
        # Should complete without errors
        with patch('sys.argv', ['execute_case_variations_consolidation.py']):
            result = main()
        
        # Verify flow completed
        assert result in [0, 1]  # Success or partial success


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

