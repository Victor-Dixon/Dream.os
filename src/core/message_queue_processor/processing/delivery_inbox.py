#!/usr/bin/env python3
"""
Inbox delivery handler.

SSOT: src/core/message_queue_processor/processing/delivery_inbox.py
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, Tuple

logger = logging.getLogger(__name__)


def deliver_to_inbox(
    inbox_dir: Path,
    recipient: str,
    content: str,
    metadata: Dict[str, Any],
) -> Tuple[bool, str | None]:
    """Persist a message payload to the recipient inbox."""
    inbox_dir.mkdir(parents=True, exist_ok=True)
    filepath = inbox_dir / f"{recipient}.json"
    payload = {"recipient": recipient, "content": content, "metadata": metadata}
    try:
        filepath.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        logger.info("Message delivered to inbox: %s", filepath)
        return True, None
    except Exception as exc:
        logger.error("Inbox delivery error: %s", exc)
        return False, f"Inbox delivery failed: {exc}"
