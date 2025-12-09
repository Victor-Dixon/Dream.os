"""
Tests for tools/devlog_poster.py routing logic.

We assert per-agent channel routing and Captain-major behavior without hitting Discord.
"""

import types
from pathlib import Path

import pytest

# Add project root
import sys
project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from tools.devlog_poster import DevlogPoster  # noqa: E402


@pytest.fixture
def poster(monkeypatch):
    p = DevlogPoster()
    # Force deterministic webhooks for tests
    monkeypatch.setitem(p.agent_webhooks, "agent-1", "wh-1")
    monkeypatch.setitem(p.agent_webhooks, "Agent-1", "wh-1")
    monkeypatch.setitem(p.agent_webhooks, "agent-6", "wh-6")
    monkeypatch.setitem(p.agent_webhooks, "Agent-6", "wh-6")
    monkeypatch.setitem(p.agent_webhooks, "agent-4", "wh-4")
    monkeypatch.setitem(p.agent_webhooks, "Agent-4", "wh-4")
    return p


@pytest.mark.parametrize(
    "agent,expected_channel,expected_wh",
    [
        ("Agent-1", "#agent-1-devlogs", "wh-1"),
        ("Agent-6", "#agent-6-devlogs", "wh-6"),
    ],
)
def test_target_channel_per_agent(poster, agent, expected_channel, expected_wh):
    channel, wh = poster._get_target_channel(agent, is_major=False)
    assert channel == expected_channel
    assert wh == expected_wh


def test_captain_major_posts_to_captain_channel(poster):
    channel, wh = poster._get_target_channel("Agent-4", is_major=True)
    assert channel == "#captain-updates"
    assert wh == "wh-4"


def test_captain_regular_posts_to_own_channel(poster):
    channel, wh = poster._get_target_channel("Agent-4", is_major=False)
    assert channel == "#agent-4-devlogs"
    assert wh == "wh-4"

