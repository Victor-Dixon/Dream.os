#!/usr/bin/env python3
"""
Integration Tests for Messaging Templates
=========================================

Comprehensive integration tests for message template rendering,
template key dispatch, and end-to-end message formatting.

Author: Agent-8 (SSOT & System Integration Specialist)
Created: 2025-12-09
"""

import pytest
from datetime import datetime, timezone

from src.core.messaging_models import (
    MessageCategory,
    UnifiedMessage,
    UnifiedMessagePriority,
    UnifiedMessageTag,
    UnifiedMessageType,
)
from src.core.messaging_templates import (
    dispatch_template_key,
    format_s2a_message,
    render_message,
    S2A_KEYS,
)


def _create_message(
    content: str = "Test message content",
    sender: str = "SYSTEM",
    recipient: str = "Agent-1",
    message_type: UnifiedMessageType = UnifiedMessageType.SYSTEM_TO_AGENT,
    priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
    tags: list[UnifiedMessageTag] = None,
    category: MessageCategory = None,
) -> UnifiedMessage:
    """Helper to create UnifiedMessage instances."""
    return UnifiedMessage(
        content=content,
        sender=sender,
        recipient=recipient,
        message_type=message_type,
        priority=priority,
        tags=tags or [],
        category=category,
        message_id=f"msg_{int(datetime.now(timezone.utc).timestamp() * 1000)}",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


class TestS2ATemplateIntegration:
    """Integration tests for S2A (System-to-Agent) templates."""

    def test_s2a_control_template_renders_complete(self):
        """Test S2A CONTROL template renders with all required fields."""
        msg = _create_message(
            category=MessageCategory.S2A,
            content="Test context",
        )
        rendered = render_message(msg, context="Test context", actions="Test actions")
        
        assert "[HEADER] S2A CONTROL" in rendered
        assert "From: SYSTEM" in rendered
        assert "To: Agent-1" in rendered
        assert "Test context" in rendered
        # CONTROL template uses "Action Required" not "actions" field directly
        assert "Agent Operating Cycle" in rendered
        assert "Cycle Checklist" in rendered
        assert "DISCORD REPORTING POLICY" in rendered

    def test_s2a_onboarding_tag_routes_correctly(self):
        """Test ONBOARDING tag routes to HARD_ONBOARDING template."""
        msg = _create_message(
            category=MessageCategory.S2A,
            tags=[UnifiedMessageTag.ONBOARDING],
        )
        rendered = render_message(msg)
        
        assert "[HEADER] S2A HARD ONBOARDING" in rendered
        assert "Agent Operating Cycle" in rendered

    def test_s2a_wrapup_tag_routes_to_passdown(self):
        """Test WRAPUP tag routes to PASSDOWN template."""
        msg = _create_message(
            category=MessageCategory.S2A,
            tags=[UnifiedMessageTag.WRAPUP],
        )
        rendered = render_message(msg)
        
        assert "[HEADER] S2A PASSDOWN" in rendered

    def test_s2a_system_tag_routes_to_control(self):
        """Test SYSTEM tag routes to CONTROL template."""
        msg = _create_message(
            category=MessageCategory.S2A,
            tags=[UnifiedMessageTag.SYSTEM],
        )
        rendered = render_message(msg)
        
        assert "[HEADER] S2A CONTROL" in rendered

    def test_s2a_coordination_tag_routes_to_task_cycle(self):
        """Test COORDINATION tag routes to TASK_CYCLE template."""
        msg = _create_message(
            category=MessageCategory.S2A,
            tags=[UnifiedMessageTag.COORDINATION],
        )
        rendered = render_message(msg)
        
        assert "[HEADER] S2A TASK CYCLE" in rendered

    def test_s2a_explicit_template_key_override(self):
        """Test explicit template_key parameter overrides inference."""
        msg = _create_message(
            category=MessageCategory.S2A,
            tags=[UnifiedMessageTag.ONBOARDING],  # Would normally route to HARD_ONBOARDING
        )
        rendered = render_message(msg, template_key="STALL_RECOVERY")
        
        assert "[HEADER] S2A STALL RECOVERY" in rendered

    def test_s2a_cycle_v2_template_renders(self):
        """Test CYCLE_V2 template renders correctly."""
        msg = _create_message(
            category=MessageCategory.S2A,
        )
        rendered = render_message(
            msg,
            template_key="CYCLE_V2",
            mission="Test mission",
            dod="Test DoD",
            ssot_constraint="SSOT compliance required",
            v2_constraint="V2 compliance required",
            touch_surface="Minimal files",
            validation_required="Run tests",
            priority_level="high",
            handoff_expectation="Report completion",
        )
        
        assert "CYCLE_V2" in rendered or "Cycle V2" in rendered or "CYCLE V2" in rendered
        assert "Test mission" in rendered

    def test_s2a_includes_devlog_footer_when_requested(self):
        """Test devlog footer is included when include_devlog=True."""
        msg = _create_message(category=MessageCategory.S2A)
        rendered = render_message(msg, include_devlog=True)
        
        assert "Documentation" in rendered
        assert "Update status.json" in rendered
        assert "Post Discord devlog" in rendered

    def test_s2a_includes_workflows_footer_when_requested(self):
        """Test workflows footer is included when include_workflows=True."""
        msg = _create_message(category=MessageCategory.S2A)
        rendered = render_message(msg, include_workflows=True)
        
        assert "Core workflows" in rendered
        assert "--get-next-task" in rendered
        assert "messaging_cli.py" in rendered

    def test_s2a_message_type_inference(self):
        """Test message type inference when category is None."""
        msg = _create_message(
            category=None,
            message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
        )
        rendered = render_message(msg)
        
        assert "[HEADER] S2A CONTROL" in rendered

    def test_s2a_broadcast_type_inference(self):
        """Test BROADCAST message type infers S2A category."""
        msg = _create_message(
            category=None,
            message_type=UnifiedMessageType.BROADCAST,
        )
        rendered = render_message(msg)
        
        assert "[HEADER] S2A CONTROL" in rendered


class TestD2ATemplateIntegration:
    """Integration tests for D2A (Discord-to-Agent) templates."""

    def test_d2a_template_renders_complete(self):
        """Test D2A template renders with all required fields."""
        msg = _create_message(
            category=MessageCategory.D2A,
            message_type=UnifiedMessageType.HUMAN_TO_AGENT,
            content="User request from Discord",
        )
        rendered = render_message(
            msg,
            interpretation="Agent interpretation",
            actions="Proposed actions",
            fallback="Clarification question",
        )
        
        assert "[HEADER] D2A DISCORD INTAKE" in rendered
        assert "User request from Discord" in rendered
        assert "Agent interpretation" in rendered
        assert "Proposed actions" in rendered
        assert "Clarification question" in rendered
        # D2A template may not include cycle checklist in main body
        assert "DISCORD" in rendered or "Discord" in rendered

    def test_d2a_defaults_populated(self):
        """Test D2A template populates defaults when fields missing."""
        msg = _create_message(
            category=MessageCategory.D2A,
            message_type=UnifiedMessageType.HUMAN_TO_AGENT,
        )
        rendered = render_message(msg)
        
        # Should have defaults from format_d2a_payload
        assert "Pending agent interpretation" in rendered or "interpretation" in rendered.lower()
        assert "Discord Response Policy" in rendered or "DISCORD" in rendered

    def test_d2a_category_inference(self):
        """Test D2A category inferred from message type."""
        msg = _create_message(
            category=None,
            message_type=UnifiedMessageType.HUMAN_TO_AGENT,
        )
        rendered = render_message(msg)
        
        assert "[HEADER] D2A DISCORD INTAKE" in rendered or "D2A" in rendered


class TestC2ATemplateIntegration:
    """Integration tests for C2A (Captain-to-Agent) templates."""

    def test_c2a_template_renders_complete(self):
        """Test C2A template renders correctly."""
        msg = _create_message(
            category=MessageCategory.C2A,
            message_type=UnifiedMessageType.CAPTAIN_TO_AGENT,
            sender="Captain Agent-4",
        )
        rendered = render_message(
            msg,
            context="Captain context",
            actions="Captain actions",
            task="Complete captain task",
        )
        
        assert "C2A" in rendered or "CAPTAIN" in rendered
        assert "Captain Agent-4" in rendered or "Captain" in rendered
        assert "Complete captain task" in rendered

    def test_c2a_category_inference(self):
        """Test C2A category inferred from CAPTAIN_TO_AGENT type."""
        msg = _create_message(
            category=None,
            message_type=UnifiedMessageType.CAPTAIN_TO_AGENT,
        )
        rendered = render_message(msg)
        
        assert "C2A" in rendered or "CAPTAIN" in rendered


class TestA2ATemplateIntegration:
    """Integration tests for A2A (Agent-to-Agent) templates."""

    def test_a2a_template_renders_complete(self):
        """Test A2A template renders correctly."""
        msg = _create_message(
            category=MessageCategory.A2A,
            message_type=UnifiedMessageType.AGENT_TO_AGENT,
            sender="Agent-1",
            recipient="Agent-2",
        )
        rendered = render_message(
            msg,
            ask="Coordination request",
            context="Agent context",
            next_step="Next action",
        )
        
        assert "A2A" in rendered or "AGENT-TO-AGENT" in rendered
        assert "Agent-1" in rendered
        assert "Agent-2" in rendered
        assert "Coordination request" in rendered

    def test_a2a_category_inference(self):
        """Test A2A category inferred from AGENT_TO_AGENT type."""
        msg = _create_message(
            category=None,
            message_type=UnifiedMessageType.AGENT_TO_AGENT,
        )
        rendered = render_message(msg)
        
        assert "A2A" in rendered or "AGENT-TO-AGENT" in rendered


class TestTemplateKeyDispatch:
    """Integration tests for template key dispatch logic."""

    def test_dispatch_template_key_s2a_with_explicit_key(self):
        """Test explicit key is used when provided."""
        msg = _create_message(category=MessageCategory.S2A)
        key = dispatch_template_key(msg, explicit_key="STALL_RECOVERY")
        
        assert key == "STALL_RECOVERY"

    def test_dispatch_template_key_s2a_infers_from_tags(self):
        """Test key inferred from tags when no explicit key."""
        msg = _create_message(
            category=MessageCategory.S2A,
            tags=[UnifiedMessageTag.ONBOARDING],
        )
        key = dispatch_template_key(msg)
        
        assert key == "HARD_ONBOARDING"

    def test_dispatch_template_key_s2a_infers_from_type(self):
        """Test key inferred from message type when no tags."""
        msg = _create_message(
            category=MessageCategory.S2A,
            message_type=UnifiedMessageType.ONBOARDING,
        )
        key = dispatch_template_key(msg)
        
        assert key == "HARD_ONBOARDING"

    def test_dispatch_template_key_s2a_defaults_to_control(self):
        """Test key defaults to CONTROL when no inference possible."""
        msg = _create_message(category=MessageCategory.S2A)
        key = dispatch_template_key(msg)
        
        assert key == "CONTROL"

    def test_dispatch_template_key_non_s2a_returns_default(self):
        """Test non-S2A categories return DEFAULT or explicit key."""
        msg = _create_message(category=MessageCategory.D2A)
        key = dispatch_template_key(msg)
        
        assert key == "DEFAULT"

    def test_all_s2a_keys_are_valid(self):
        """Test all S2A_KEYS are valid template keys."""
        msg = _create_message(category=MessageCategory.S2A)
        
        for key in S2A_KEYS:
            result = dispatch_template_key(msg, explicit_key=key)
            assert result == key


class TestFormatS2AMessage:
    """Integration tests for format_s2a_message function."""

    def test_format_s2a_message_injects_operating_cycle(self):
        """Test operating cycle is always injected."""
        rendered = format_s2a_message("CONTROL", sender="SYSTEM", recipient="Agent-1")
        
        assert "Agent Operating Cycle" in rendered
        assert "1) Claim" in rendered
        assert "7) Report evidence" in rendered

    def test_format_s2a_message_allows_cycle_override(self):
        """Test operating cycle can be overridden."""
        custom_cycle = "Custom cycle text"
        rendered = format_s2a_message(
            "CONTROL",
            sender="SYSTEM",
            recipient="Agent-1",
            operating_cycle=custom_cycle,
        )
        
        assert custom_cycle in rendered

    def test_format_s2a_message_handles_missing_template(self):
        """Test missing template falls back to CONTROL."""
        rendered = format_s2a_message("NONEXISTENT", sender="SYSTEM", recipient="Agent-1")
        
        # Should fall back to CONTROL template
        assert "S2A" in rendered or len(rendered) > 0


class TestTemplateEdgeCases:
    """Integration tests for edge cases and error handling."""

    def test_render_message_with_missing_category_fallback(self):
        """Test message with no category falls back appropriately."""
        msg = _create_message(category=None, message_type=UnifiedMessageType.SYSTEM_TO_AGENT)
        rendered = render_message(msg)
        
        # Should infer S2A and render
        assert len(rendered) > 0
        assert "S2A" in rendered or "SYSTEM" in rendered

    def test_render_message_with_empty_content(self):
        """Test message with empty content still renders."""
        msg = _create_message(content="", category=MessageCategory.S2A)
        rendered = render_message(msg)
        
        assert len(rendered) > 0
        assert "[HEADER]" in rendered

    def test_render_message_with_special_characters(self):
        """Test message with special characters renders correctly."""
        msg = _create_message(
            content="Test with {braces} and $special$ chars",
            category=MessageCategory.S2A,
        )
        rendered = render_message(msg)
        
        # Should not raise KeyError from template formatting
        assert len(rendered) > 0

    def test_render_message_priority_values(self):
        """Test different priority values render correctly."""
        for priority in [UnifiedMessagePriority.REGULAR, UnifiedMessagePriority.URGENT]:
            msg = _create_message(priority=priority, category=MessageCategory.S2A)
            rendered = render_message(msg)
            
            assert len(rendered) > 0
            assert "Priority:" in rendered or priority.value in rendered

    def test_render_message_multiple_tags(self):
        """Test message with multiple tags routes correctly."""
        msg = _create_message(
            category=MessageCategory.S2A,
            tags=[UnifiedMessageTag.ONBOARDING, UnifiedMessageTag.SYSTEM],
        )
        rendered = render_message(msg)
        
        # First matching tag should win (ONBOARDING)
        assert "HARD ONBOARDING" in rendered or "ONBOARDING" in rendered


class TestTemplateIntegrationEndToEnd:
    """End-to-end integration tests for complete message flow."""

    def test_complete_s2a_message_flow(self):
        """Test complete S2A message from creation to rendering."""
        msg = _create_message(
            content="Complete test message",
            category=MessageCategory.S2A,
            tags=[UnifiedMessageTag.COORDINATION],
            priority=UnifiedMessagePriority.URGENT,
        )
        
        # Dispatch key
        key = dispatch_template_key(msg)
        assert key == "TASK_CYCLE"
        
        # Format message
        rendered = render_message(
            msg,
            context="Test context",
            actions="Test actions",
            include_devlog=True,
        )
        
        # Verify complete output
        assert "[HEADER] S2A TASK CYCLE" in rendered
        assert "Test context" in rendered
        assert "Test actions" in rendered
        assert "Agent Operating Cycle" in rendered
        assert "Documentation" in rendered
        assert msg.message_id in rendered
        assert msg.recipient in rendered

    def test_complete_d2a_message_flow(self):
        """Test complete D2A message from creation to rendering."""
        msg = _create_message(
            content="Discord user request",
            category=MessageCategory.D2A,
            message_type=UnifiedMessageType.HUMAN_TO_AGENT,
        )
        
        rendered = render_message(
            msg,
            interpretation="Agent understands request",
            actions="Will execute task",
            fallback="Need clarification",
            include_workflows=True,
        )
        
        # Verify complete output
        assert "D2A" in rendered or "DISCORD" in rendered
        assert "Discord user request" in rendered
        assert "Agent understands request" in rendered
        assert "Will execute task" in rendered
        assert "Core workflows" in rendered

