"""
Activity Emitter

<!-- SSOT Domain: infrastructure -->

================

Single-source activity event emitter for agent telemetry.

Responsibilities:
- Append JSONL events to runtime/agent_comms/activity_events.jsonl
- Enforce simple dedupe window to avoid spam
- Classify Tier 1 vs Tier 2 for downstream sinks
- Optional Discord sink can be injected; default is no-op

Notes:
- Keep interface small and dependency-free for easy reuse by CLIs/hooks.
- No implicit posting; caller controls sinks.
"""

from __future__ import annotations

import json
import hashlib
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional


class ActivityType(str, Enum):
    TASK_CLAIMED = "TASK_CLAIMED"
    TASK_COMPLETED = "TASK_COMPLETED"
    DEVLOG_CREATED = "DEVLOG_CREATED"
    GIT_COMMIT = "GIT_COMMIT"
    GIT_PUSH = "GIT_PUSH"
    TOOL_RUN = "TOOL_RUN"
    BRAIN_WRITE = "BRAIN_WRITE"
    MONEY_METRIC = "MONEY_METRIC"


class Tier(str, Enum):
    TIER_1 = "TIER_1"
    TIER_2 = "TIER_2"


@dataclass
class ActivityEvent:
    ts: str
    agent: str
    type: ActivityType
    source: str
    summary: str
    artifact: Dict[str, Any]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def event_key(event: ActivityEvent) -> str:
    """Stable key for dedupe."""
    core = event.artifact.get("task_id") or event.artifact.get("commit") or event.summary
    base = f"{event.agent}|{event.type.value}|{core}"
    return hashlib.sha256(base.encode("utf-8")).hexdigest()


class ActivityEmitter:
    """Minimal JSONL activity emitter with dedupe and tier classification."""

    def __init__(self, log_path: Path, discord_sink: Optional[Any] = None):
        self.log_path = log_path
        self.discord_sink = discord_sink
        self._recent_keys: Dict[str, float] = {}

    def classify_tier(self, event: ActivityEvent) -> Tier:
        if event.type in {
            ActivityType.TASK_COMPLETED,
            ActivityType.GIT_PUSH,
            ActivityType.MONEY_METRIC,
        }:
            return Tier.TIER_1
        if event.type == ActivityType.TOOL_RUN and event.artifact.get("exit_code", 0) != 0:
            return Tier.TIER_1
        return Tier.TIER_2

    def should_dedupe(self, key: str, now_ts: float, window_s: int = 300) -> bool:
        last = self._recent_keys.get(key)
        if last is None:
            return False
        return (now_ts - last) < window_s

    def emit(self, event: ActivityEvent, *, force_discord: bool = False) -> None:
        key = event_key(event)
        now_ts = time.time()

        if self.should_dedupe(key, now_ts):
            return

        self._recent_keys[key] = now_ts

        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(
                json.dumps(
                    {
                        **asdict(event),
                        "type": event.type.value,
                        "tier": self.classify_tier(event).value,
                    }
                )
                + "\n"
            )

        tier = self.classify_tier(event)
        if self.discord_sink and (force_discord or tier == Tier.TIER_1):
            try:
                self.discord_sink.post_event(event)
            except Exception:
                # Swallow sink errors to keep emitter non-fatal.
                pass


# Lightweight helper for one-liner emission from scripts/CLIs
_default_emitter: Optional[ActivityEmitter] = None


def emit_activity_event(
    event_type: str,
    source: str,
    agent_id: str,
    summary: str = "",
    artifact: Optional[Dict[str, Any]] = None,
    meta: Optional[Dict[str, Any]] = None,
    *,
    force_discord: bool = False,
    log_path: Path = Path("runtime/agent_comms/activity_events.jsonl"),
) -> None:
    """
    Convenience wrapper so tools can emit without boilerplate.

    Args:
        event_type: ActivityType name (string)
        source: Logical source (e.g., cycle_v2_spreadsheet)
        agent_id: Agent identifier
        summary: Human-readable one-liner
        artifact: Structured artifact payload
        meta: Additional metadata (non-indexed)
        force_discord: Force sink even if Tier 2
        log_path: Override log path (defaults to runtime/agent_comms)
    """
    global _default_emitter

    try:
        atype = ActivityType(event_type)
    except Exception:
        return  # Ignore unknown types to avoid breaking callers

    event = ActivityEvent(
        ts=now_iso(),
        agent=agent_id,
        type=atype,
        source=source,
        summary=summary or "",
        artifact=artifact or {},
    )

    if _default_emitter is None or _default_emitter.log_path != log_path:
        _default_emitter = ActivityEmitter(log_path=log_path)

    _default_emitter.emit(event, force_discord=force_discord)

