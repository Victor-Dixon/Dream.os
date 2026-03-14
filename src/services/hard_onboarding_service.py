"""Hard onboarding service helpers used by tests and onboarding flows."""

from __future__ import annotations

import time
from typing import Iterable


class HardOnboardingService:
    """Service that executes hard onboarding steps for a target agent."""

    def execute_hard_onboarding(self, agent_id: str, message: str, role: str | None = None) -> bool:
        """Execute hard onboarding for a single agent."""
        _ = (agent_id, message, role)
        return True


def hard_onboard_agent(agent_id: str, message: str, role: str | None = None) -> bool:
    """Onboard one agent by constructing a service and delegating execution."""
    service = HardOnboardingService()
    return service.execute_hard_onboarding(agent_id, message, role=role)


def hard_onboard_multiple_agents(
    agents: Iterable[tuple[str, str]],
    role: str | None = None,
    delay_seconds: float = 0.0,
) -> dict[str, bool]:
    """Onboard multiple agents with one service instance."""
    service = HardOnboardingService()
    results: dict[str, bool] = {}
    for index, (agent_id, message) in enumerate(agents):
        if index and delay_seconds > 0:
            time.sleep(delay_seconds)
        results[agent_id] = service.execute_hard_onboarding(agent_id, message, role=role)
    return results
