"""
Unit tests for soft onboarding message content.

Ensures the onboarding message contains required safety and compliance elements.
"""

import pytest


class TestSoftOnboardingMessage:
    """Tests for soft onboarding message content compliance."""

    def test_message_contains_shared_workspace_safety(self):
        """Verify onboarding message includes Shared Workspace Safety section."""
        from src.services.onboarding.soft.default_message import (
            get_full_onboarding_message,
        )
        
        message = get_full_onboarding_message("Agent-1")
        
        assert "SHARED WORKSPACE SAFETY" in message
        assert "git clean -fd" in message
        assert "git restore ." in message
        assert "Destructive git commands are FORBIDDEN" in message

    def test_message_contains_output_contract(self):
        """Verify onboarding message includes Output Contract skeleton."""
        from src.services.onboarding.soft.default_message import (
            get_full_onboarding_message,
        )
        
        message = get_full_onboarding_message("Agent-1")
        
        assert "OUTPUT CONTRACT (STRICT" in message
        assert "**Task:**" in message
        assert "**Actions Taken:**" in message
        assert "**Verification:**" in message
        assert "**Public Build Signal:**" in message
        assert "✅ Ready OR 🟡 Blocked" in message

    def test_message_contains_working_tree_audit(self):
        """Verify onboarding message references working_tree_audit.py tool."""
        from src.services.onboarding.soft.default_message import (
            get_full_onboarding_message,
        )
        
        message = get_full_onboarding_message("Agent-1")
        
        assert "python tools/working_tree_audit.py" in message

    def test_message_contains_agent_ownership_boundary(self):
        """Verify onboarding message explains agent ownership boundaries."""
        from src.services.onboarding.soft.default_message import (
            get_full_onboarding_message,
        )
        
        message = get_full_onboarding_message("Agent-1")
        
        assert "Agent Ownership Boundary" in message
        assert "agent_workspaces/" in message

    def test_message_contains_operating_cycle(self):
        """Verify onboarding message includes full operating cycle."""
        from src.services.onboarding.soft.default_message import (
            get_full_onboarding_message,
        )
        
        message = get_full_onboarding_message("Agent-1")
        
        # Check for cycle steps
        assert "Claim" in message
        assert "Sync" in message
        assert "Execute" in message
        assert "Validate" in message
        assert "Commit" in message
        assert "Report" in message

    def test_message_contains_reference_links(self):
        """Verify onboarding message includes reference links to templates."""
        from src.services.onboarding.soft.default_message import (
            get_full_onboarding_message,
        )
        
        message = get_full_onboarding_message("Agent-1")
        
        assert "templates/session-closure-template.md" in message
        assert "validate_closure_format.py" in message
        assert ".cursor/rules/session-closure.mdc" in message

    def test_message_substitutes_agent_id(self):
        """Verify agent_id is substituted in message."""
        from src.services.onboarding.soft.default_message import (
            get_full_onboarding_message,
        )
        
        message = get_full_onboarding_message("Agent-5")
        
        assert "Agent-5" in message
        assert "{agent_id}" not in message

    def test_output_contract_stub_format(self):
        """Verify output contract stub has correct structure."""
        from src.services.onboarding.soft.default_message import (
            get_output_contract_stub,
        )
        
        stub = get_output_contract_stub()
        
        # Check required A++ fields
        required_fields = [
            "**Task:**",
            "**Project:**",
            "**Actions Taken:**",
            "**Artifacts Created / Updated:**",
            "**Verification:**",
            "**Public Build Signal:**",
            "**Git Commit:**",
            "**Git Push:**",
            "**Status:**",
        ]
        
        for field in required_fields:
            assert field in stub, f"Missing required field: {field}"

    def test_branch_policy_included(self):
        """Verify branch policy is mentioned in onboarding."""
        from src.services.onboarding.soft.default_message import (
            get_full_onboarding_message,
        )
        
        message = get_full_onboarding_message("Agent-1")
        
        assert "Branch Policy" in message
        assert "main" in message
        assert "No feature branches" in message


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

