# <!-- SSOT Domain: trading_robot -->
"""Discord webhook publisher."""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any

import requests


@dataclass(frozen=True)
class DiscordPublishResult:
    posted: bool
    status_code: int | None
    response_text: str | None


def post_to_discord(payload: dict[str, Any], *, dry_run: bool = False) -> DiscordPublishResult:
    webhook = os.getenv("DISCORD_WEBHOOK_URL", "").strip()
    if not webhook:
        return DiscordPublishResult(False, None, "DISCORD_WEBHOOK_URL not configured")
    if dry_run:
        return DiscordPublishResult(False, None, json.dumps(payload, indent=2))
    response = requests.post(webhook, json=payload, timeout=30)
    return DiscordPublishResult(response.ok, response.status_code, response.text)
