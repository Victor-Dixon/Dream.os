#!/usr/bin/env python3
"""
Queue utility helpers.

SSOT: src/core/message_queue_processor/utils/queue_utilities.py
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ActivityTracker:
    """Minimal activity tracker stub."""

    active: bool = True

    def mark_inactive(self) -> None:
        self.active = False


def mark_agent_inactive(tracker: ActivityTracker) -> None:
    """Mark an agent as inactive via the tracker."""
    tracker.mark_inactive()
