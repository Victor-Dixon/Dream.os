#!/usr/bin/env python3
"""
Characterization tests for onboarding services.

These tests lock in the current public behaviour of:
- hard_onboard_agent / hard_onboard_multiple_agents
- soft_onboard_agent / soft_onboard_multiple_agents

They are written specifically to support safe refactoring of
`hard_onboarding_service.py` and `soft_onboarding_service.py` using TDD.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Dict, List, Tuple

import pytest

from src.services import hard_onboarding_service as hard_mod
from src.services import soft_onboarding_service as soft_mod
from src.core import keyboard_control_lock as kcl


class _CallRecorder:
    """Simple helper to record calls in tests."""

    def __init__(self) -> None:
        self.events: List[Any] = []

    def add(self, value: Any) -> None:
        self.events.append(value)


def test_hard_onboard_agent_uses_service_execute(monkeypatch: pytest.MonkeyPatch) -> None:
    """hard_onboard_agent should construct service and delegate to execute_hard_onboarding."""
    recorder = _CallRecorder()

    class FakeHardService:
        def __init__(self) -> None:
            recorder.add(("init",))

        def execute_hard_onboarding(self, agent_id: str, message: str, role: str | None = None) -> bool:
            recorder.add(("execute", agent_id, message, role))
            return True

    monkeypatch.setattr(hard_mod, "HardOnboardingService", FakeHardService)

    result = hard_mod.hard_onboard_agent("Agent-1", "hello", role="Integrator")

    assert result is True
    assert ("init",) in recorder.events
    assert ("execute", "Agent-1", "hello", "Integrator") in recorder.events


def test_hard_onboard_multiple_agents_uses_single_service_and_returns_results(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """hard_onboard_multiple_agents should reuse one service and return per-agent results."""
    recorder = _CallRecorder()

    class FakeHardService:
        def __init__(self) -> None:
            recorder.add(("init",))

        def execute_hard_onboarding(self, agent_id: str, message: str, role: str | None = None) -> bool:
            recorder.add(("execute", agent_id, message, role))
            # Simulate one failure for characterization
            return agent_id != "Agent-2"

    # Use fake service and avoid real sleeps
    monkeypatch.setattr(hard_mod, "HardOnboardingService", FakeHardService)
    monkeypatch.setattr(hard_mod, "time", type(
        "T", (), {"sleep": staticmethod(lambda *_args, **_kw: None)}))

    agents: List[Tuple[str, str]] = [
        ("Agent-1", "msg-1"),
        ("Agent-2", "msg-2"),
    ]

    results = hard_mod.hard_onboard_multiple_agents(agents, role="Integrator")

    assert results == {"Agent-1": True, "Agent-2": False}
    # Service constructed once
    assert recorder.events.count(("init",)) == 1
    # Both agents passed through execute_hard_onboarding with role preserved
    assert ("execute", "Agent-1", "msg-1", "Integrator") in recorder.events
    assert ("execute", "Agent-2", "msg-2", "Integrator") in recorder.events


def test_soft_onboard_agent_acquires_lock_when_not_already_locked(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    When keyboard lock is not held, soft_onboard_agent should:
    - check lock status
    - acquire keyboard_control lock
    - delegate to SoftOnboardingService.execute_soft_onboarding
    """
    recorder = _CallRecorder()

    def fake_is_locked() -> bool:
        recorder.add("is_locked_checked")
        return False

    @contextmanager
    def fake_keyboard_control(source: str):
        recorder.add(("lock_acquired", source))
        try:
            yield
        finally:
            recorder.add(("lock_released", source))

    class FakeSoftService:
        def __init__(self) -> None:
            recorder.add(("soft_init",))

        def execute_soft_onboarding(self, agent_id: str, message: str, **kwargs: Any) -> bool:
            recorder.add(("execute_soft", agent_id, message, dict(kwargs)))
            return True

    # Patch lock helpers at the source module so the inline import in soft_onboard_agent sees them
    monkeypatch.setattr(kcl, "is_locked", fake_is_locked, raising=False)
    monkeypatch.setattr(kcl, "keyboard_control",
                        fake_keyboard_control, raising=False)
    monkeypatch.setattr(soft_mod, "SoftOnboardingService", FakeSoftService)

    result = soft_mod.soft_onboard_agent("Agent-1", "hello", role="Integrator")

    assert result is True
    # Behaviour expectations
    assert "is_locked_checked" in recorder.events
    assert ("soft_init",) in recorder.events
    assert any(e[0] == "lock_acquired" for e in recorder.events)
    assert any(e[0] == "lock_released" for e in recorder.events)
    assert ("execute_soft", "Agent-1", "hello",
            {"role": "Integrator"}) in recorder.events


def test_soft_onboard_agent_skips_lock_when_already_locked(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    When keyboard lock is already held, soft_onboard_agent should:
    - detect existing lock
    - NOT acquire keyboard_control again
    - still delegate to execute_soft_onboarding
    """
    recorder = _CallRecorder()

    def fake_is_locked() -> bool:
        recorder.add("is_locked_checked")
        return True

    @contextmanager
    def fake_keyboard_control(source: str):
        # If this is called in this scenario, it is a regression.
        recorder.add(("unexpected_lock_acquired", source))
        yield

    class FakeSoftService:
        def __init__(self) -> None:
            recorder.add(("soft_init",))

        def execute_soft_onboarding(self, agent_id: str, message: str, **kwargs: Any) -> bool:
            recorder.add(("execute_soft", agent_id, message, dict(kwargs)))
            return True

    monkeypatch.setattr(kcl, "is_locked", fake_is_locked, raising=False)
    monkeypatch.setattr(kcl, "keyboard_control",
                        fake_keyboard_control, raising=False)
    monkeypatch.setattr(soft_mod, "SoftOnboardingService", FakeSoftService)

    result = soft_mod.soft_onboard_agent("Agent-2", "world", role="Integrator")

    assert result is True
    assert "is_locked_checked" in recorder.events
    assert ("soft_init",) in recorder.events
    assert ("execute_soft", "Agent-2", "world",
            {"role": "Integrator"}) in recorder.events
    # Ensure no unexpected lock acquisition in the already-locked path
    assert not any(e[0] == "unexpected_lock_acquired" for e in recorder.events)


def test_soft_onboard_multiple_agents_wraps_entire_operation_in_lock(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    soft_onboard_multiple_agents should:
    - acquire keyboard_control once for the whole operation
    - delegate to soft_onboard_agent for each agent
    - return a per-agent result mapping.
    """
    recorder = _CallRecorder()

    @contextmanager
    def fake_keyboard_control(source: str):
        recorder.add(("lock_acquired", source))
        try:
            yield
        finally:
            recorder.add(("lock_released", source))

    def fake_soft_onboard_agent(agent_id: str, message: str, **kwargs: Any) -> bool:
        recorder.add(("soft_onboard_agent", agent_id, message, dict(kwargs)))
        # Simulate one failure for characterization
        return agent_id != "Agent-2"

    # Patch keyboard_control at the source module (kcl), which soft_onboard_multiple_agents imports from
    monkeypatch.setattr(kcl, "keyboard_control",
                        fake_keyboard_control, raising=False)
    # Patch the public helper used inside the multi-agent helper
    monkeypatch.setattr(soft_mod, "soft_onboard_agent",
                        fake_soft_onboard_agent, raising=False)

    agents: List[Tuple[str, str]] = [
        ("Agent-1", "msg-1"),
        ("Agent-2", "msg-2"),
    ]

    results = soft_mod.soft_onboard_multiple_agents(
        agents, role="Integrator", generate_cycle_report=False
    )

    # Behaviour: per-agent mapping preserves individual success/failure
    assert results == {"Agent-1": True, "Agent-2": False}
    # One lock context for the entire operation
    assert recorder.events.count(
        ("lock_acquired", "soft_onboard_multiple")) == 1
    assert recorder.events.count(
        ("lock_released", "soft_onboard_multiple")) == 1
    # Delegation preserves role and order
    assert ("soft_onboard_agent", "Agent-1", "msg-1",
            {"role": "Integrator"}) in recorder.events
    assert ("soft_onboard_agent", "Agent-2", "msg-2",
            {"role": "Integrator"}) in recorder.events


def test_soft_onboarding_uses_messaging_cleanup_when_pyautogui_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    When PyAutoGUI is unavailable, step_3_send_cleanup_prompt should fall back
    to the messaging-based cleanup path rather than trying GUI operations.
    """
    recorder = _CallRecorder()

    # Force the global feature flag to represent a headless CI / non-GUI env
    monkeypatch.setattr(soft_mod, "PYAUTOGUI_AVAILABLE",
                        False, raising=False)

    class DummyService(soft_mod.SoftOnboardingService):
        def _send_cleanup_via_messaging(
            self, agent_id: str, custom_cleanup_message: str | None
        ) -> bool:
            recorder.add(
                ("cleanup_via_messaging", agent_id, custom_cleanup_message)
            )
            return True

    service = DummyService()

    result = service.step_3_send_cleanup_prompt(
        "Agent-1", custom_cleanup_message="CLEANUP"
    )

    assert result is True
    assert ("cleanup_via_messaging", "Agent-1", "CLEANUP") in recorder.events


def test_soft_onboarding_uses_messaging_onboarding_when_pyautogui_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    When PyAutoGUI is unavailable, step_6_paste_onboarding_message should fall
    back to the messaging-based onboarding path rather than GUI operations.
    """
    recorder = _CallRecorder()

    # Force the global feature flag to represent a headless CI / non-GUI env
    monkeypatch.setattr(soft_mod, "PYAUTOGUI_AVAILABLE",
                        False, raising=False)

    class DummyService(soft_mod.SoftOnboardingService):
        def _send_onboarding_via_messaging(
            self, agent_id: str, message: str
        ) -> bool:
            recorder.add(("onboarding_via_messaging", agent_id, message))
            return True

    service = DummyService()

    result = service.step_6_paste_onboarding_message("Agent-2", "ONBOARD")

    assert result is True
    assert ("onboarding_via_messaging", "Agent-2",
            "ONBOARD") in recorder.events
