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
        # Burst bucket tracking: key -> list of timestamps in last 60 seconds
        self.burst_buckets: Dict[str, list] = {}

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
        
        Logic order (FIXED):
        1. Enforce min_interval
        2. Enforce burst bucket
        3. Enforce 8h rolling cap (always-on)
        4. Enforce 24h rolling cap (always-on)
        5. Cooldown only if burst repeatedly violated or 8h cap hit

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
        if key not in self.burst_buckets:
            self.burst_buckets[key] = []

        recent_coords = self.cache[key]
        burst_bucket = self.burst_buckets[key]

        # Clean old entries (older than 24 hours)
        cutoff_time = current_time - (24 * 60 * 60)
        recent_coords[:] = [ts for ts in recent_coords if ts > cutoff_time]
        
        # Clean burst bucket (older than 60 seconds)
        burst_cutoff = current_time - 60
        burst_bucket[:] = [ts for ts in burst_bucket if ts > burst_cutoff]

        # ============================================================
        # OPTION A - BALANCED CONFIG
        # ============================================================
        MIN_INTERVAL = 20  # 20 seconds
        DAILY_LIMIT = 400  # 400 messages per 24 hours
        EIGHT_HOUR_LIMIT = 160  # 160 messages per 8 hours (always-on)
        BURST_LIMIT = 8  # 8 messages per 60 seconds
        COOLDOWN_SECONDS = 10 * 60  # 10 minutes cooldown
        
        # ============================================================
        # STEP 1: Enforce minimum interval between messages
        # ============================================================
        if recent_coords:
            last_coord = max(recent_coords)
            time_since_last = current_time - last_coord
            
            if time_since_last < MIN_INTERVAL:
                wait_seconds = MIN_INTERVAL - time_since_last
                return False, f"Rate limited: Minimum {MIN_INTERVAL}s interval between messages. Wait {wait_seconds:.1f}s", wait_seconds

        # ============================================================
        # STEP 2: Enforce burst bucket (8 messages / 60 seconds)
        # ============================================================
        if len(burst_bucket) >= BURST_LIMIT:
            # Burst limit hit - fall back to min_interval pacing
            oldest_in_burst = min(burst_bucket)
            time_until_oldest_expires = (oldest_in_burst + 60) - current_time
            
            if time_until_oldest_expires > 0:
                # Use min_interval as fallback pacing
                wait_seconds = max(MIN_INTERVAL, time_until_oldest_expires)
                return False, f"Rate limited: Burst limit ({BURST_LIMIT}/60s) exceeded. Wait {wait_seconds:.1f}s", wait_seconds

        # ============================================================
        # STEP 3: Enforce 8-hour rolling cap (ALWAYS-ON, not conditional)
        # ============================================================
        eight_hour_cutoff = current_time - (8 * 60 * 60)
        recent_8h = [ts for ts in recent_coords if ts > eight_hour_cutoff]
        
        if len(recent_8h) >= EIGHT_HOUR_LIMIT:
            # Hit 8h limit - apply cooldown
            oldest_in_8h = min(recent_8h)
            next_allowed = oldest_in_8h + (8 * 60 * 60)  # When oldest message expires from 8h window
            wait_seconds = max(0, next_allowed - current_time)
            
            # If still in cooldown from previous violation, extend it
            if wait_seconds < COOLDOWN_SECONDS:
                wait_seconds = COOLDOWN_SECONDS
            
            if wait_seconds > 0:
                return False, f"Rate limited: 8-hour limit ({EIGHT_HOUR_LIMIT} messages) exceeded. Cooldown {wait_seconds/60:.1f} minutes", wait_seconds

        # ============================================================
        # STEP 4: Enforce 24-hour rolling cap (ALWAYS-ON)
        # ============================================================
        if len(recent_coords) >= DAILY_LIMIT:
            # Hit 24h limit
            oldest_in_24h = min(recent_coords)
            next_allowed = oldest_in_24h + (24 * 60 * 60)  # When oldest message expires from 24h window
            wait_seconds = max(0, next_allowed - current_time)
            
            if wait_seconds > 0:
                return False, f"Rate limited: Daily limit ({DAILY_LIMIT} messages) exceeded. Wait {wait_seconds/3600:.1f} hours", wait_seconds

        # ============================================================
        # STEP 5: All checks passed - allow message
        # ============================================================
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
        if key not in self.burst_buckets:
            self.burst_buckets[key] = []

        # Record in main cache (24h window)
        self.cache[key].append(current_time)
        
        # Record in burst bucket (60s window)
        self.burst_buckets[key].append(current_time)

        # Keep only recent entries in main cache
        cutoff_time = current_time - (24 * 60 * 60)
        self.cache[key][:] = [ts for ts in self.cache[key] if ts > cutoff_time]
        
        # Keep only recent entries in burst bucket
        burst_cutoff = current_time - 60
        self.burst_buckets[key][:] = [ts for ts in self.burst_buckets[key] if ts > burst_cutoff]

        self._save_cache()
        logger.debug(f"Recorded coordination: {key} at {current_time}")

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
