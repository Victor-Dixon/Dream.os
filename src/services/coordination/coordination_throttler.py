#!/usr/bin/env python3
"""
Coordination Throttler - Prevents Coordination Message Spam
===========================================================

<!-- SSOT Domain: communication -->

Rate limiting system for bilateral coordination messages to prevent spam
and ensure quality coordination over quantity.

V2 Compliance | Author: Agent-5 | Date: 2025-12-19
"""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Dict, Optional, Tuple

logger = logging.getLogger(__name__)


class CoordinationThrottler:
    """Rate limiter for bilateral coordination messages."""

    def __init__(self, cache_file: Optional[Path] = None):
        """Initialize coordination throttler.

        Args:
            cache_file: File to store coordination history (defaults to project root)
        """
        if cache_file is None:
            # Default to project root
            project_root = Path(__file__).resolve().parent.parent.parent.parent
            cache_file = project_root / "coordination_cache.json"

        self.cache_file = cache_file
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        self._load_cache()

    def _load_cache(self) -> None:
        """Load coordination history from cache file."""
        self.cache: Dict[str, list] = {}

        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    data = json.load(f)
                    # Convert timestamps back to float
                    for agent, timestamps in data.items():
                        self.cache[agent] = [float(ts) for ts in timestamps]
                logger.debug(f"Loaded coordination cache: {len(self.cache)} agents")
            except Exception as e:
                logger.warning(f"Failed to load coordination cache: {e}")
                self.cache = {}

    def _save_cache(self) -> None:
        """Save coordination history to cache file."""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except Exception as e:
            logger.warning(f"Failed to save coordination cache: {e}")

    def can_send_coordination(self, recipient: str, sender: str) -> Tuple[bool, str, Optional[float]]:
        """Check if coordination message can be sent to recipient.

        Args:
            recipient: Agent receiving coordination request
            sender: Agent sending coordination request

        Returns:
            Tuple of (can_send, reason, wait_seconds)
        """
        current_time = time.time()
        key = f"{sender}->{recipient}"

        # Initialize if not exists
        if key not in self.cache:
            self.cache[key] = []

        recent_coords = self.cache[key]

        # Clean old entries (older than 24 hours)
        cutoff_time = current_time - (24 * 60 * 60)
        recent_coords[:] = [ts for ts in recent_coords if ts > cutoff_time]

        # Check rate limits
        if len(recent_coords) >= 3:  # Max 3 coordination messages per 24 hours
            oldest_allowed = current_time - (8 * 60 * 60)  # 8 hour window
            recent_in_window = [ts for ts in recent_coords if ts > oldest_allowed]

            if len(recent_in_window) >= 2:  # Max 2 in 8 hours
                next_allowed = min(recent_in_window) + (4 * 60 * 60)  # 4 hour cooldown
                wait_seconds = max(0, next_allowed - current_time)

                if wait_seconds > 0:
                    return False, f"Rate limited: Too many coordination messages. Wait {wait_seconds/3600:.1f} hours", wait_seconds

        # Check minimum interval between messages (30 minutes)
        if recent_coords:
            last_coord = max(recent_coords)
            min_interval = 30 * 60  # 30 minutes
            time_since_last = current_time - last_coord

            if time_since_last < min_interval:
                wait_seconds = min_interval - time_since_last
                return False, f"Rate limited: Minimum 30-minute interval between coordination messages", wait_seconds

        return True, "OK", None

    def record_coordination(self, recipient: str, sender: str) -> None:
        """Record that a coordination message was sent.

        Args:
            recipient: Agent receiving coordination request
            sender: Agent sending coordination request
        """
        key = f"{sender}->{recipient}"
        current_time = time.time()

        if key not in self.cache:
            self.cache[key] = []

        self.cache[key].append(current_time)

        # Keep only recent entries
        cutoff_time = current_time - (24 * 60 * 60)
        self.cache[key][:] = [ts for ts in self.cache[key] if ts > cutoff_time]

        self._save_cache()
        logger.info(f"Recorded coordination: {key} at {current_time}")

    def get_coordination_stats(self, recipient: str, sender: str) -> Dict:
        """Get coordination statistics for a sender->recipient pair.

        Args:
            recipient: Agent receiving coordination request
            sender: Agent sending coordination request

        Returns:
            Dict with coordination statistics
        """
        key = f"{sender}->{recipient}"
        current_time = time.time()

        if key not in self.cache:
            return {
                "total_messages": 0,
                "messages_last_24h": 0,
                "messages_last_8h": 0,
                "last_message_hours_ago": None,
                "next_allowed_seconds": 0
            }

        timestamps = self.cache[key]

        # Clean old entries
        cutoff_time = current_time - (24 * 60 * 60)
        recent_timestamps = [ts for ts in timestamps if ts > cutoff_time]

        last_24h_cutoff = current_time - (24 * 60 * 60)
        last_8h_cutoff = current_time - (8 * 60 * 60)

        messages_24h = len([ts for ts in recent_timestamps if ts > last_24h_cutoff])
        messages_8h = len([ts for ts in recent_timestamps if ts > last_8h_cutoff])

        last_message = max(recent_timestamps) if recent_timestamps else None
        last_message_hours_ago = (current_time - last_message) / 3600 if last_message else None

        # Calculate next allowed time
        can_send, _, wait_seconds = self.can_send_coordination(recipient, sender)
        next_allowed_seconds = wait_seconds if not can_send and wait_seconds else 0

        return {
            "total_messages": len(recent_timestamps),
            "messages_last_24h": messages_24h,
            "messages_last_8h": messages_8h,
            "last_message_hours_ago": last_message_hours_ago,
            "next_allowed_seconds": next_allowed_seconds
        }


# Global instance for easy access
_coordination_throttler = None

def get_coordination_throttler() -> CoordinationThrottler:
    """Get global coordination throttler instance."""
    global _coordination_throttler
    if _coordination_throttler is None:
        _coordination_throttler = CoordinationThrottler()
    return _coordination_throttler
