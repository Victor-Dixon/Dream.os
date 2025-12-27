import asyncio
from dataclasses import dataclass
from datetime import datetime

import pytest


@dataclass
class _Summary:
    inactivity_duration_minutes: float
    last_activity: datetime | None = None
    activity_sources: list[str] | None = None


@pytest.mark.unit
def test_status_change_monitor_sends_resume_via_messaging_core(monkeypatch):
    """Regression: resumer prompts must attempt direct PyAutoGUI coordinate delivery."""
    from src.discord_commander.status_change_monitor import StatusChangeMonitor

    sent = {"called": False, "recipient": None, "content": None, "metadata": None}

    import src.services.contract_system.manager as contract_manager_mod
    import src.core.messaging_pyautogui as messaging_pyautogui_mod

    class _FakeContractManager:
        def get_next_task(self, agent_id: str):
            return {"status": "no_tasks"}

    monkeypatch.setattr(contract_manager_mod, "ContractManager", _FakeContractManager)

    def _fake_delivery_send_message(self, message):
        sent["called"] = True
        sent["recipient"] = getattr(message, "recipient", None)
        sent["content"] = getattr(message, "content", "")
        sent["metadata"] = getattr(message, "metadata", {})
        return True

    monkeypatch.setattr(
        messaging_pyautogui_mod.PyAutoGUIMessagingDelivery,
        "send_message",
        _fake_delivery_send_message,
    )

    monitor = StatusChangeMonitor(bot=None, channel_id=None, scheduler=None)
    summary = _Summary(inactivity_duration_minutes=10.0, last_activity=None, activity_sources=["status.json"])

    asyncio.run(
        monitor._send_resume_message_to_agent(
            agent_id="Agent-1",
            prompt="Resume work now.",
            summary=summary,
            skip_wrapper=False,
        )
    )

    assert sent["called"] is True
    assert sent["recipient"] == "Agent-1"
    # SWARM_PULSE template is expected output for resumer prompts
    assert isinstance(sent["content"], str) and "SWARM PULSE" in sent["content"]
    assert sent["metadata"].get("use_pyautogui") is True


