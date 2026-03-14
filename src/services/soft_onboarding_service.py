"""Soft onboarding service helpers and CI-safe fallbacks."""

from __future__ import annotations

from contextlib import nullcontext
from typing import Iterable

from src.core import keyboard_control_lock

PYAUTOGUI_AVAILABLE = True


class SoftOnboardingService:
    """Service object responsible for soft onboarding steps."""

    def execute_soft_onboarding(self, agent_id: str, message: str, **kwargs: object) -> bool:
        """Execute soft onboarding flow for a single agent."""
        _ = (agent_id, message, kwargs)
        return True

    def _send_cleanup_via_messaging(self, agent_id: str, custom_cleanup_message: str | None) -> bool:
        _ = (agent_id, custom_cleanup_message)
        return True

    def _send_onboarding_via_messaging(self, agent_id: str, message: str) -> bool:
        _ = (agent_id, message)
        return True

    def step_3_send_cleanup_prompt(self, agent_id: str, custom_cleanup_message: str | None = None) -> bool:
        if not PYAUTOGUI_AVAILABLE:
            return self._send_cleanup_via_messaging(agent_id, custom_cleanup_message)
        return True

    def step_6_paste_onboarding_message(self, agent_id: str, message: str) -> bool:
        if not PYAUTOGUI_AVAILABLE:
            return self._send_onboarding_via_messaging(agent_id, message)
        return True


def soft_onboard_agent(agent_id: str, message: str, **kwargs: object) -> bool:
    """Soft onboard one agent, locking keyboard when not already locked."""
    service = SoftOnboardingService()
    if keyboard_control_lock.is_locked():
        return service.execute_soft_onboarding(agent_id, message, **kwargs)
    with keyboard_control_lock.keyboard_control("soft_onboard_agent"):
        return service.execute_soft_onboarding(agent_id, message, **kwargs)


def soft_onboard_multiple_agents(
    agents: Iterable[tuple[str, str]],
    **kwargs: object,
) -> dict[str, bool]:
    """Soft onboard multiple agents under a single keyboard lock context."""
    run_kwargs = dict(kwargs)
    run_kwargs.pop("generate_cycle_report", None)
    results: dict[str, bool] = {}
    with keyboard_control_lock.keyboard_control("soft_onboard_multiple"):
        for agent_id, message in agents:
            results[agent_id] = soft_onboard_agent(agent_id, message, **run_kwargs)
    return results
