import pytest

from src.core.messaging_models import (
    MessageCategory,
    UnifiedMessage,
    UnifiedMessagePriority,
    UnifiedMessageTag,
    UnifiedMessageType,
)
from src.core.messaging_templates import render_message


def _basic_msg(**overrides):
    defaults = dict(
        content="test content",
        sender="SYSTEM",
        recipient="Agent-1",
        message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
        priority=UnifiedMessagePriority.REGULAR,
        tags=[],
        category=MessageCategory.S2A,
    )
    defaults.update(overrides)
    return UnifiedMessage(**defaults)


def test_s2a_control_renders_with_defaults():
    msg = _basic_msg()
    rendered = render_message(msg)
    assert "[HEADER] S2A CONTROL" in rendered
    assert "Agent Operating Cycle" in rendered
    assert "Cycle Checklist" in rendered
    assert "DISCORD REPORTING POLICY" in rendered


def test_s2a_onboarding_tag_routes_to_hard_onboarding():
    msg = _basic_msg(tags=[UnifiedMessageTag.ONBOARDING])
    rendered = render_message(msg)
    assert "[HEADER] S2A ONBOARDING (HARD)" in rendered


def test_d2a_defaults_include_policies():
    msg = _basic_msg(
        category=MessageCategory.D2A,
        message_type=UnifiedMessageType.HUMAN_TO_AGENT,
    )
    rendered = render_message(msg)
    assert "Discord Response Policy" in rendered
    assert "Preferred Reply Format" in rendered


def test_broadcast_infers_s2a_and_renders():
    msg = _basic_msg(
        category=None,
        message_type=UnifiedMessageType.BROADCAST,
    )
    rendered = render_message(msg)
    assert "[HEADER] S2A CONTROL" in rendered







