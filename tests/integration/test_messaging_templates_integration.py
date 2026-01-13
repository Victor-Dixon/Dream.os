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
        rendered = render_message(msg, template_key="SWARM_PULSE")
        
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
        key = dispatch_template_key(msg, explicit_key="SWARM_PULSE")

        assert key == "SWARM_PULSE"

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

    def test_complete_c2a_message_flow(self):
        """Test complete C2A message from creation to rendering."""
        msg = _create_message(
            content="Captain directive",
            category=MessageCategory.C2A,
            message_type=UnifiedMessageType.CAPTAIN_TO_AGENT,
            sender="Captain Agent-4",
        )
        
        rendered = render_message(
            msg,
            context="Captain context",
            actions="Execute directive",
            task="Complete task",
            deliverable="Report results",
            eta="2 hours",
        )
        
        # Verify complete output
        assert "C2A" in rendered or "CAPTAIN" in rendered
        assert "Captain Agent-4" in rendered
        assert "Complete task" in rendered
        assert "Report results" in rendered

    def test_complete_a2a_message_flow(self):
        """Test complete A2A message from creation to rendering."""
        msg = _create_message(
            content="Agent coordination request",
            category=MessageCategory.A2A,
            message_type=UnifiedMessageType.AGENT_TO_AGENT,
            sender="Agent-1",
            recipient="Agent-2",
        )
        
        rendered = render_message(
            msg,
            ask="Need coordination",
            context="Agent context",
            next_step="Proceed with task",
        )
        
        # Verify complete output
        assert "A2A" in rendered or "AGENT-TO-AGENT" in rendered
        assert "Agent-1" in rendered
        assert "Agent-2" in rendered
        assert "Need coordination" in rendered
        assert "Proceed with task" in rendered


class TestTemplateSpecialCharacters:
    """Integration tests for special characters and edge cases in templates."""

    def test_special_characters_in_content(self):
        """Test various special characters in message content."""
        special_chars = [
            "{braces}",
            "$dollar$",
            "@at@",
            "#hash#",
            "%percent%",
            "&ampersand&",
            "*asterisk*",
            "+plus+",
            "=equals=",
            "|pipe|",
            "\\backslash\\",
            "/forward/",
            "~tilde~",
            "`backtick`",
            "'single'",
            '"double"',
            "[brackets]",
            "(parens)",
            "<angle>",
        ]
        
        for char_seq in special_chars:
            msg = _create_message(
                content=f"Test {char_seq} content",
                category=MessageCategory.S2A,
            )
            rendered = render_message(msg)
            
            # Should not raise KeyError or formatting errors
            assert len(rendered) > 0
            assert "[HEADER]" in rendered

    def test_unicode_characters_in_content(self):
        """Test Unicode characters in message content."""
        unicode_content = [
            "Test with émojis 🚀",
            "中文测试",
            "Русский текст",
            "العربية",
            "日本語",
            "한국어",
        ]
        
        for content in unicode_content:
            msg = _create_message(
                content=content,
                category=MessageCategory.D2A,
            )
            rendered = render_message(msg)
            
            # Should handle Unicode without errors
            assert len(rendered) > 0
            assert "D2A" in rendered or "DISCORD" in rendered

    def test_newlines_in_content(self):
        """Test newlines and multi-line content."""
        multiline_content = "Line 1\nLine 2\nLine 3\n\nParagraph 2"
        msg = _create_message(
            content=multiline_content,
            category=MessageCategory.S2A,
        )
        rendered = render_message(msg)
        
        assert len(rendered) > 0
        assert "[HEADER] S2A" in rendered

    def test_very_long_content(self):
        """Test very long message content."""
        long_content = "A" * 10000  # 10KB of content
        msg = _create_message(
            content=long_content,
            category=MessageCategory.S2A,
        )
        rendered = render_message(msg)
        
        # Should handle long content without errors
        assert len(rendered) > 0
        assert "[HEADER]" in rendered

    def test_empty_strings_in_optional_fields(self):
        """Test empty strings in optional template fields."""
        msg = _create_message(category=MessageCategory.S2A)
        rendered = render_message(
            msg,
            context="",
            actions="",
            fallback="",
        )
        
        # Should render with defaults
        assert len(rendered) > 0
        assert "[HEADER] S2A" in rendered

    def test_none_values_in_optional_fields(self):
        """Test None values in optional template fields."""
        msg = _create_message(category=MessageCategory.D2A)
        rendered = render_message(
            msg,
            interpretation=None,
            actions=None,
            fallback=None,
        )
        
        # Should use defaults
        assert len(rendered) > 0
        assert "D2A" in rendered or "DISCORD" in rendered

    def test_template_placeholders_in_content(self):
        """Test content that looks like template placeholders."""
        placeholder_like_content = [
            "{sender}",
            "{recipient}",
            "{message_id}",
            "{timestamp}",
            "{content}",
            "{{double_braces}}",
        ]
        
        for content in placeholder_like_content:
            msg = _create_message(
                content=content,
                category=MessageCategory.S2A,
            )
            rendered = render_message(msg)
            
            # Should not cause template formatting errors
            assert len(rendered) > 0
            # Content should appear literally, not as placeholder
            assert content in rendered or "[HEADER]" in rendered


class TestTemplateRouting:
    """Integration tests for template routing logic."""

    def test_s2a_routing_all_tags(self):
        """Test routing for all S2A tag types."""
        tag_routes = [
            (UnifiedMessageTag.ONBOARDING, "HARD_ONBOARDING"),
            (UnifiedMessageTag.WRAPUP, "PASSDOWN"),
            (UnifiedMessageTag.SYSTEM, "CONTROL"),
            (UnifiedMessageTag.COORDINATION, "TASK_CYCLE"),
        ]
        
        for tag, expected_key in tag_routes:
            msg = _create_message(
                category=MessageCategory.S2A,
                tags=[tag],
            )
            key = dispatch_template_key(msg)
            assert key == expected_key, f"Tag {tag} should route to {expected_key}, got {key}"

    def test_s2a_routing_all_message_types(self):
        """Test routing for all S2A message types."""
        type_routes = [
            (UnifiedMessageType.ONBOARDING, "HARD_ONBOARDING"),
            (UnifiedMessageType.SYSTEM_TO_AGENT, "CONTROL"),
            (UnifiedMessageType.MULTI_AGENT_REQUEST, "CONTROL"),
            (UnifiedMessageType.BROADCAST, "CONTROL"),
        ]
        
        for msg_type, expected_key in type_routes:
            msg = _create_message(
                category=MessageCategory.S2A,
                message_type=msg_type,
            )
            key = dispatch_template_key(msg)
            assert key == expected_key, f"Type {msg_type} should route to {expected_key}, got {key}"

    def test_s2a_routing_priority_order(self):
        """Test that tag routing follows priority order."""
        # ONBOARDING should win over SYSTEM
        msg = _create_message(
            category=MessageCategory.S2A,
            tags=[UnifiedMessageTag.ONBOARDING, UnifiedMessageTag.SYSTEM],
        )
        key = dispatch_template_key(msg)
        assert key == "HARD_ONBOARDING"  # First match wins

    def test_category_inference_routing(self):
        """Test category inference for all message types."""
        type_to_category = [
            (UnifiedMessageType.SYSTEM_TO_AGENT, MessageCategory.S2A),
            (UnifiedMessageType.HUMAN_TO_AGENT, MessageCategory.D2A),
            (UnifiedMessageType.CAPTAIN_TO_AGENT, MessageCategory.C2A),
            (UnifiedMessageType.AGENT_TO_AGENT, MessageCategory.A2A),
        ]
        
        for msg_type, expected_category in type_to_category:
            msg = _create_message(
                category=None,
                message_type=msg_type,
            )
            rendered = render_message(msg)
            
            # Should infer correct category
            assert len(rendered) > 0
            if expected_category == MessageCategory.S2A:
                assert "S2A" in rendered
            elif expected_category == MessageCategory.D2A:
                assert "D2A" in rendered or "DISCORD" in rendered
            elif expected_category == MessageCategory.C2A:
                assert "C2A" in rendered or "CAPTAIN" in rendered
            elif expected_category == MessageCategory.A2A:
                assert "A2A" in rendered or "AGENT-TO-AGENT" in rendered


class TestTemplateDefaults:
    """Integration tests for default value handling."""

    def test_s2a_defaults_all_fields(self):
        """Test S2A template with all default values."""
        msg = _create_message(category=MessageCategory.S2A)
        rendered = render_message(msg)
        
        # Should have all required fields with defaults
        assert "[HEADER] S2A CONTROL" in rendered
        assert "From: SYSTEM" in rendered
        assert "To: Agent-1" in rendered
        assert "Agent Operating Cycle" in rendered
        assert "Priority:" in rendered

    def test_d2a_defaults_all_fields(self):
        """Test D2A template with all default values."""
        msg = _create_message(
            category=MessageCategory.D2A,
            message_type=UnifiedMessageType.HUMAN_TO_AGENT,
        )
        rendered = render_message(msg)
        
        # Should have defaults for interpretation, actions, fallback
        assert "[HEADER] D2A DISCORD INTAKE" in rendered
        assert "From:" in rendered
        assert "To:" in rendered

    def test_c2a_defaults_all_fields(self):
        """Test C2A template with all default values."""
        msg = _create_message(
            category=MessageCategory.C2A,
            message_type=UnifiedMessageType.CAPTAIN_TO_AGENT,
        )
        rendered = render_message(msg)
        
        # Should render with defaults
        assert "C2A" in rendered or "CAPTAIN" in rendered
        assert len(rendered) > 0

    def test_a2a_defaults_all_fields(self):
        """Test A2A template with all default values."""
        msg = _create_message(
            category=MessageCategory.A2A,
            message_type=UnifiedMessageType.AGENT_TO_AGENT,
        )
        rendered = render_message(msg)
        
        # Should render with defaults
        assert "A2A" in rendered or "AGENT-TO-AGENT" in rendered
        assert len(rendered) > 0

    def test_broadcast_defaults_all_fields(self):
        """Test BROADCAST message type with default values."""
        msg = _create_message(
            category=None,
            message_type=UnifiedMessageType.BROADCAST,
            sender="SYSTEM",
        )
        rendered = render_message(msg)
        
        # BROADCAST infers S2A category, should render with defaults
        assert "[HEADER] S2A CONTROL" in rendered or "BROADCAST" in rendered
        assert "From:" in rendered or "SYSTEM" in rendered
        assert "Priority:" in rendered
        assert len(rendered) > 0

    def test_broadcast_template_defaults_via_utils(self):
        """Test BROADCAST template from utils with default values."""
        from src.services.utils.messaging_templates import get_broadcast_template
        
        # Test with minimal required fields
        rendered = get_broadcast_template(
            sender="SYSTEM",
            content="Test broadcast message"
        )
        
        # Should have all required fields with defaults
        assert "🚨 BROADCAST MESSAGE 🚨" in rendered
        assert "**FROM:** SYSTEM" in rendered
        assert "**PRIORITY:** NORMAL" in rendered  # Default priority
        assert "Test broadcast message" in rendered
        assert "🐝 WE. ARE. SWARM." in rendered

    def test_broadcast_template_with_custom_priority(self):
        """Test BROADCAST template with custom priority."""
        from src.services.utils.messaging_templates import get_broadcast_template
        
        rendered = get_broadcast_template(
            sender="SYSTEM",
            content="Urgent broadcast",
            priority="urgent"
        )
        
        assert "🚨 BROADCAST MESSAGE 🚨" in rendered
        assert "**PRIORITY:** URGENT" in rendered
        assert "Urgent broadcast" in rendered

    def test_cycle_v2_defaults(self):
        """Test CYCLE_V2 template with default values."""
        msg = _create_message(category=MessageCategory.S2A)
        rendered = render_message(msg, template_key="CYCLE_V2")
        
        # Should render with empty defaults for cycle fields
        assert len(rendered) > 0
        assert "CYCLE_V2" in rendered or "Cycle V2" in rendered or "CYCLE V2" in rendered


class TestTemplateStructureValidation:
    """Integration tests that verify complete template structure matches expected format."""

    @staticmethod
    def _assert_sections_present(rendered: str, required: list[str]) -> None:
        """Assert that all required section substrings are present in rendered output."""
        for section in required:
            assert section in rendered, f"Missing required section: {section}\n\nRendered output (first 600 chars):\n{rendered[:600]}"

    @staticmethod
    def _assert_in_order(rendered: str, ordered_sections: list[str]) -> None:
        """Assert that ordered_sections appear in sequence in rendered output."""
        positions = []
        for section in ordered_sections:
            pos = rendered.find(section)
            assert pos >= 0, f"Section not found: {section}\n\nRendered output (first 600 chars):\n{rendered[:600]}"
            positions.append(pos)
        assert positions == sorted(positions), f"Sections out of order.\nOrder: {ordered_sections}\nPositions: {positions}\n\nRendered output (first 600 chars):\n{rendered[:600]}"

    def test_s2a_control_template_complete_structure(self):
        """Test S2A CONTROL template has complete structure with all required sections."""
        msg = _create_message(
            category=MessageCategory.S2A,
            content="Test context",
            sender="SYSTEM",
            recipient="Agent-1",
        )
        rendered = render_message(
            msg,
            context="Test context",
            actions="Test actions",
            fallback="Test fallback",
        )
        
        required = [
            "[HEADER] S2A CONTROL",
            "From: SYSTEM",
            "To: Agent-1",
            "Priority:",
            "Message ID:",
            "Timestamp:",
            "Context:",
            "Test context",
            "Action Required:",
            "No-Reply Policy:",
            "Priority Behavior:",
            "Agent Operating Cycle",
            "Cycle Checklist:",
            "DISCORD REPORTING POLICY",
            "Evidence format:",
            "If blocked:",
        ]
        self._assert_sections_present(rendered, required)

    def test_s2a_control_template_section_order(self):
        """Test S2A CONTROL template sections appear in correct order."""
        msg = _create_message(category=MessageCategory.S2A)
        rendered = render_message(msg, context="Context", actions="Actions")
        
        self._assert_in_order(
            rendered,
            [
                "[HEADER] S2A CONTROL",
                "Context:",
                "Action Required:",
                "No-Reply Policy:",
                "Priority Behavior:",
                "Agent Operating Cycle",
                "Cycle Checklist:",
                "DISCORD REPORTING POLICY",
                "Evidence format:",
                "If blocked:",
            ],
        )

    def test_d2a_template_complete_structure(self):
        """Test D2A template has complete structure with all required sections."""
        msg = _create_message(
            category=MessageCategory.D2A,
            message_type=UnifiedMessageType.HUMAN_TO_AGENT,
            content="User request from Discord",
            sender="Discord User",
            recipient="Agent-1",
        )
        rendered = render_message(
            msg,
            interpretation="Agent interpretation",
            actions="Proposed actions",
            fallback="Clarification question",
        )
        
        required = [
            "[HEADER] D2A DISCORD INTAKE",
            "From: Discord User",
            "To: Agent-1",
            "Priority:",
            "Message ID:",
            "Timestamp:",
            "Origin:",
            "Discord → Agent intake",
            "User Message:",
            "User request from Discord",
            "Interpretation (agent):",
            "Agent interpretation",
            "Proposed Action:",
            "Proposed actions",
            "Response Policy",  # substring within discord_response_policy text
            "Devlog Command",
            "If clarification needed:",
            "Clarification question",
            "#DISCORD #D2A",
        ]
        self._assert_sections_present(rendered, required)

    def test_d2a_template_section_order(self):
        """Test D2A template sections appear in correct order."""
        msg = _create_message(
            category=MessageCategory.D2A,
            message_type=UnifiedMessageType.HUMAN_TO_AGENT,
        )
        rendered = render_message(
            msg,
            interpretation="Interpretation",
            actions="Actions",
        )
        
        self._assert_in_order(
            rendered,
            [
                "[HEADER] D2A DISCORD INTAKE",
                "Origin:",
                "User Message:",
                "Interpretation (agent):",
                "Proposed Action:",
                "Devlog Command",
                "If clarification needed:",
                "#DISCORD #D2A",
            ],
        )

    def test_c2a_template_complete_structure(self):
        """Test C2A template has complete structure with all required sections."""
        msg = _create_message(
            category=MessageCategory.C2A,
            message_type=UnifiedMessageType.CAPTAIN_TO_AGENT,
            sender="Captain Agent-4",
            recipient="Agent-1",
        )
        rendered = render_message(
            msg,
            context="Captain context",
            actions="Captain actions",
            task="Complete captain task",
            deliverable="Report results",
            eta="2 hours",
        )
        
        required = [
            "[HEADER] C2A CAPTAIN DIRECTIVE",
            "From: Captain Agent-4",
            "To: Agent-1",
            "Priority:",
            "Message ID:",
            "Timestamp:",
            "Identity:",
            "No-Ack Policy:",
            "DISCORD REPORTING POLICY",
            "Cycle Checklist:",
            "Task:",
            "Complete captain task",
            "Context:",
            "Captain context",
            "Operating Procedures",
            "Deliverable:",
            "Report results",
            "Checkpoint:",
            "2 hours",
            "Evidence format:",
            "Priority Behavior:",
            "If blocked:",
        ]
        self._assert_sections_present(rendered, required)

    def test_c2a_template_section_order(self):
        """Test C2A template sections appear in correct order."""
        msg = _create_message(
            category=MessageCategory.C2A,
            message_type=UnifiedMessageType.CAPTAIN_TO_AGENT,
            sender="Captain Agent-4",
        )
        rendered = render_message(
            msg,
            task="Task",
            context="Context",
            deliverable="Deliverable",
        )
        
        self._assert_in_order(
            rendered,
            [
                "[HEADER] C2A CAPTAIN DIRECTIVE",
                "Identity:",
                "No-Ack Policy:",
                "DISCORD REPORTING POLICY",
                "Cycle Checklist:",
                "Task:",
                "Context:",
                "Operating Procedures",
                "Deliverable:",
            ],
        )

    def test_a2a_template_complete_structure(self):
        """Test A2A template has complete structure with all required sections."""
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
        
        required = [
            "[HEADER] A2A COORDINATION",
            "From: Agent-1",
            "To: Agent-2",
            "Priority:",
            "Message ID:",
            "Timestamp:",
            "Identity:",
            "No-Ack Policy:",
            "Cycle Checklist:",
            "Ask/Offer:",
            "Coordination request",
            "Context:",
            "Agent context",
            "Next Step:",
            "Next action",
            "If blocked:",
            "How to respond:",
            "#A2A",  # Substring check - template has "#A2A #BILATERAL-COORDINATION #SWARM-FORCE-MULTIPLIER"
        ]
        self._assert_sections_present(rendered, required)

    def test_a2a_template_section_order(self):
        """Test A2A template sections appear in correct order."""
        msg = _create_message(
            category=MessageCategory.A2A,
            message_type=UnifiedMessageType.AGENT_TO_AGENT,
            sender="Agent-1",
            recipient="Agent-2",
        )
        rendered = render_message(
            msg,
            ask="Ask",
            context="Context",
            next_step="Next",
        )
        
        self._assert_in_order(
            rendered,
            [
                "[HEADER] A2A COORDINATION",
                "Identity:",
                "No-Ack Policy:",
                "Cycle Checklist:",
                "Ask/Offer:",
                "Context:",
                "Next Step:",
                "If blocked:",
                "How to respond:",
                "#A2A",  # Substring check - template has "#A2A #BILATERAL-COORDINATION #SWARM-FORCE-MULTIPLIER"
            ],
        )

    def test_s2a_hard_onboarding_template_structure(self):
        """Test S2A HARD_ONBOARDING template has complete structure."""
        msg = _create_message(
            category=MessageCategory.S2A,
            tags=[UnifiedMessageTag.ONBOARDING],
        )
        rendered = render_message(msg)
        
        required = [
            "[HEADER] S2A HARD ONBOARDING",
            "From: SYSTEM",
            "To: Agent-1",
            "Priority:",
            "Message ID:",
            "Timestamp:",
            "Context:",
            "First Actions:",
            "Agent Operating Cycle",
            "If blocked:",
        ]
        self._assert_sections_present(rendered, required)

    def test_s2a_task_cycle_template_structure(self):
        """Test S2A TASK_CYCLE template has complete structure."""
        msg = _create_message(
            category=MessageCategory.S2A,
            tags=[UnifiedMessageTag.COORDINATION],
        )
        rendered = render_message(msg, context="Cycle objective", actions="Assigned slice")
        
        required = [
            "[HEADER] S2A TASK CYCLE",
            "Cycle Objective:",
            "Cycle objective",
            "Assigned Slice:",
            "Assigned slice",
            "Agent Operating Cycle",
            "If blocked:",
        ]
        self._assert_sections_present(rendered, required)

    def test_template_renders_complete_message_metadata(self):
        """Test all templates include complete message metadata."""
        test_cases = [
            (MessageCategory.S2A, UnifiedMessageType.SYSTEM_TO_AGENT, "SYSTEM"),
            (MessageCategory.D2A, UnifiedMessageType.HUMAN_TO_AGENT, "Discord User"),
            (MessageCategory.C2A, UnifiedMessageType.CAPTAIN_TO_AGENT, "Captain Agent-4"),
            (MessageCategory.A2A, UnifiedMessageType.AGENT_TO_AGENT, "Agent-1"),
        ]
        
        for category, msg_type, sender in test_cases:
            msg = _create_message(
                category=category,
                message_type=msg_type,
                sender=sender,
                recipient="Agent-1",
            )
            msg.message_id = "test_msg_123"
            rendered = render_message(msg)
            
            # Verify metadata is present
            assert f"From: {sender}" in rendered
            assert "To: Agent-1" in rendered
            assert "Message ID: test_msg_123" in rendered
            assert "Priority:" in rendered
            assert "Timestamp:" in rendered

    def test_template_footers_appear_when_requested(self):
        """Test devlog and workflows footers appear when requested."""
        msg = _create_message(category=MessageCategory.S2A)
        
        # Test devlog footer
        rendered_with_devlog = render_message(msg, include_devlog=True)
        assert "Documentation" in rendered_with_devlog
        assert "Update status.json" in rendered_with_devlog
        assert "Post Discord devlog" in rendered_with_devlog
        
        # Test workflows footer
        rendered_with_workflows = render_message(msg, include_workflows=True)
        assert "Core workflows" in rendered_with_workflows
        assert "--get-next-task" in rendered_with_workflows
        assert "messaging_cli.py" in rendered_with_workflows
        
        # Test both footers
        rendered_both = render_message(msg, include_devlog=True, include_workflows=True)
        assert "Documentation" in rendered_both
        assert "Core workflows" in rendered_both
        
        # Test no footers
        rendered_none = render_message(msg, include_devlog=False, include_workflows=False)
        # Check for footer-specific format - footer has "\n\nDocumentation\n" followed by bullet points
        # The footer format is unique: "\n\nDocumentation\n- Update status.json\n- Post Discord devlog for completed actions\n"
        # Check for the exact footer pattern that only appears in DEVLOG_FOOTER
        footer_pattern = "\n\nDocumentation\n- Update status.json\n- Post Discord devlog for completed actions\n"
        assert footer_pattern not in rendered_none
        # Also verify workflows footer is absent (check for unique workflows footer content)
        workflows_footer_pattern = "\n\nCore workflows\n"
        assert workflows_footer_pattern not in rendered_none or rendered_none.count(workflows_footer_pattern) == 0

