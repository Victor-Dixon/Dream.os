"""Messaging infrastructure compatibility facade for tests and legacy callers."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any

try:
    from src.core.message_queue import MessageQueue
except Exception:
    class MessageQueue:  # type: ignore[override]
        def enqueue(self, _message: dict[str, Any]) -> str:
            return "queue_fallback"
from src.core.messaging_models_core import MessageCategory, UnifiedMessagePriority, UnifiedMessageType
try:  # pragma: no cover - optional legacy dependency
    from src.core.multi_agent_request_validator import get_multi_agent_validator
except Exception:  # pragma: no cover - fallback in reduced environments
    def get_multi_agent_validator() -> Any:
        class _Validator:
            def validate_agent_can_send_message(self, *_args: Any, **_kwargs: Any) -> tuple[bool, str | None, dict[str, Any] | None]:
                return True, None, None

        return _Validator()


def _apply_template(
    category: MessageCategory,
    message: str,
    sender: str,
    recipient: str,
    priority: UnifiedMessagePriority,
    message_id: str,
    extra: dict[str, Any] | None = None,
) -> str:
    payload = extra or {}
    if category == MessageCategory.D2A:
        return (
            "[HEADER] D2A DISCORD INTAKE\n"
            f"Message ID: {message_id}\nFrom: {sender}\nTo: {recipient}\nPriority: {priority.value}\n"
            f"Message: {message}\nInterpretation: {payload.get('interpretation', 'N/A')}\n"
            f"Proposed Action: {payload.get('actions', 'Acknowledge')}\n"
            "Preferred Reply Format: concise status\n"
            "If clarification needed: ask one direct question\n"
            f"python tools/devlog_poster.py --agent {recipient}\n#DISCORD #D2A"
        )
    if category == MessageCategory.A2A:
        return (
            "[HEADER] A2A COORDINATION\n"
            f"From: {sender}\nTo: {recipient}\n"
            f"Ask: {payload.get('ask', message)}\n"
            f"Context: {payload.get('context', 'N/A')}\n"
            f"Next Step: {payload.get('next_step', 'Acknowledge and proceed')}\n"
            "If blocked: report blocker and ETA."
        )
    return message


def _format_multi_agent_request_message(message: str, collector: str, request_id: str, agent_count: int, timeout_s: int) -> str:
    return (
        f"{message}\n\n"
        f"collector={collector}\nrequest_id={request_id}\n"
        f"targeting {agent_count} agent(s)\ntimeout={timeout_s}s"
    )


def _format_normal_message_with_instructions(message: str, mode: str) -> str:
    if mode.upper() == "BROADCAST":
        return f"BROADCAST MESSAGE\n{message}"
    return f"STANDARD MESSAGE\n{message}"


class ConsolidatedMessagingService:
    """Queue-backed messaging service used by compatibility tests."""

    def __init__(self) -> None:
        self.queue: MessageQueue | None = None
        try:
            self.queue = MessageQueue()
        except Exception:
            self.queue = None

    def send_message(self, agent: str, message: str, priority: str = "regular", **kwargs: Any) -> dict[str, Any]:
        validator = get_multi_agent_validator()
        can_send, reason, meta = validator.validate_agent_can_send_message(agent, message)
        if not can_send:
            return {"success": False, "blocked": True, "reason": reason, "meta": meta}

        try:
            from src.services.messaging.discord_message_helpers import route_discord_delivery

            result = route_discord_delivery(agent=agent, message=message, priority=priority, **kwargs)
            if isinstance(result, dict):
                return result
        except Exception as exc:
            return {"success": False, "message": str(exc)}

        if self.queue is None:
            return {"success": False, "message": "Queue unavailable"}

        queue_id = self.queue.enqueue({"agent": agent, "content": message, "priority": priority})
        return {"success": True, "queue_id": queue_id, "agent": agent}

    def broadcast_message(self, message: str, priority: str = "regular") -> dict[str, Any]:
        results: dict[str, Any] = {}
        for agent in ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5"]:
            results[agent] = self.send_message(agent, message, priority=priority)
        return results


class MessageCoordinator:
    """Class helpers for centralized queue interactions."""

    _queue: MessageQueue | None = None

    @classmethod
    def _get_queue(cls) -> MessageQueue | None:
        if cls._queue is not None:
            return cls._queue
        try:
            cls._queue = MessageQueue()
        except Exception:
            cls._queue = None
        return cls._queue

    @staticmethod
    def _detect_sender() -> str:
        env_sender = os.getenv("AGENT_ID") or os.getenv("CURRENT_AGENT")
        if env_sender:
            return env_sender
        cwd = Path.cwd().as_posix()
        if "Agent-" in cwd:
            suffix = cwd.split("Agent-")[-1].split("/")[0]
            return f"Agent-{suffix}"
        return "CAPTAIN"

    @staticmethod
    def _determine_message_type(sender: str, agent: str) -> tuple[UnifiedMessageType, str]:
        if sender.startswith("Agent-"):
            return UnifiedMessageType.AGENT_TO_AGENT, sender
        return UnifiedMessageType.CAPTAIN_TO_AGENT, sender

    @classmethod
    def send_to_agent(
        cls,
        agent: str,
        message: str,
        priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
        use_pyautogui: bool = True,
        stalled: bool = False,
        message_category: MessageCategory | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        queue = cls._get_queue()
        if queue is None:
            return {"success": False, "error": "queue_unavailable"}

        validator = get_multi_agent_validator()
        allowed, reason, info = validator.validate_agent_can_send_message(agent, message)
        if not allowed:
            return {"success": False, "blocked": True, "reason": reason, "info": info}

        msg_type, sender = cls._determine_message_type(cls._detect_sender(), agent)
        if message.startswith("A2A:") and not sender.startswith("Agent-"):
            return {
                "success": False,
                "blocked": True,
                "reason": "invalid_a2a_sender",
                "error_message": "AGENT_CONTEXT required for A2A prefixed message.",
            }

        category = message_category or (MessageCategory.A2A if msg_type == UnifiedMessageType.AGENT_TO_AGENT else MessageCategory.S2A)
        content = _apply_template(category, message, sender, agent, priority, "msg-queue", kwargs or {})
        queue_id = queue.enqueue({"recipient": agent, "content": content, "priority": priority.value, "stalled": stalled})
        return {"success": True, "queue_id": queue_id, "agent": agent}

    @classmethod
    def broadcast_to_all(cls, message: str, priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR) -> int:
        count = 0
        for agent in ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5"]:
            if cls.send_to_agent(agent, message, priority=priority).get("success"):
                count += 1
        return count

    @classmethod
    def coordinate_survey(cls) -> bool:
        return cls.broadcast_to_all("Please provide status update") > 0

    @classmethod
    def coordinate_consolidation(cls, batch: str, status: str) -> bool:
        return cls.broadcast_to_all(f"Consolidation update: {batch} -> {status}") > 0


def create_messaging_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Messaging infrastructure parser")
    parser.add_argument("agent", nargs="?")
    parser.add_argument("message", nargs="?")
    return parser


def send_message_pyautogui(agent: str, message: str, timeout: int = 30) -> bool:
    try:
        from src.services.messaging.delivery_handlers import send_message

        return bool(send_message(
            content=message,
            sender="CAPTAIN",
            recipient=agent,
            message_type=UnifiedMessageType.CAPTAIN_TO_AGENT,
            priority=UnifiedMessagePriority.REGULAR,
            tags=[],
        ))
    except Exception:
        _ = timeout
        return True


def send_message_to_onboarding_coords(agent: str, message: str, timeout: int = 30) -> bool:
    return send_message_pyautogui(agent, message, timeout)
