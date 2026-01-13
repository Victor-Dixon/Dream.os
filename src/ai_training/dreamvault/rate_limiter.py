"""
Rate Limiter for DreamVault AI Training Pipeline
===============================================

SSOT Domain: ai_training

V2 Compliant: <100 lines, single responsibility
Rate limiting for AI training operations to prevent API abuse.
"""

import time
import threading
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class RateLimitConfig:
    """Rate limiting configuration"""
    requests_per_minute: int = 60
    requests_per_hour: int = 1000
    burst_limit: int = 10
    cooldown_seconds: int = 60


class RateLimiter:
    """
    V2 Compliant Rate Limiter

    Prevents API abuse and ensures fair usage of AI training resources.
    Single responsibility: rate limiting.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = RateLimitConfig(**config)
        self._lock = threading.Lock()

        # Request tracking
        self.minute_requests: Dict[str, list] = {}
        self.hour_requests: Dict[str, list] = {}
        self.burst_counts: Dict[str, int] = {}
        self.cooldowns: Dict[str, float] = {}

    def check_limit(self, identifier: str) -> bool:
        """
        Check if request is within rate limits.

        Args:
            identifier: Unique identifier for the requester

        Returns:
            True if request is allowed, False if rate limited
        """
        with self._lock:
            current_time = time.time()

            # Check cooldown
            if identifier in self.cooldowns:
                if current_time < self.cooldowns[identifier]:
                    return False
                else:
                    del self.cooldowns[identifier]

            # Clean old requests
            self._clean_old_requests(identifier, current_time)

            # Check burst limit
            if self.burst_counts.get(identifier, 0) >= self.config.burst_limit:
                self.cooldowns[identifier] = current_time + self.config.cooldown_seconds
                return False

            # Check minute limit
            minute_count = len(self.minute_requests.get(identifier, []))
            if minute_count >= self.config.requests_per_minute:
                self.cooldowns[identifier] = current_time + self.config.cooldown_seconds
                return False

            # Check hour limit
            hour_count = len(self.hour_requests.get(identifier, []))
            if hour_count >= self.config.requests_per_hour:
                self.cooldowns[identifier] = current_time + self.config.cooldown_seconds
                return False

            return True

    def record_request(self, identifier: str) -> None:
        """
        Record a successful request.

        Args:
            identifier: Unique identifier for the requester
        """
        with self._lock:
            current_time = time.time()

            # Initialize lists if needed
            if identifier not in self.minute_requests:
                self.minute_requests[identifier] = []
            if identifier not in self.hour_requests:
                self.hour_requests[identifier] = []

            # Record request
            self.minute_requests[identifier].append(current_time)
            self.hour_requests[identifier].append(current_time)
            self.burst_counts[identifier] = self.burst_counts.get(identifier, 0) + 1

    def wait_if_needed(self, identifier: str) -> None:
        """
        Wait if rate limited, then record the request.

        Args:
            identifier: Unique identifier for the requester
        """
        while not self.check_limit(identifier):
            time.sleep(1)

        self.record_request(identifier)

    def _clean_old_requests(self, identifier: str, current_time: float) -> None:
        """Clean requests older than the time windows."""
        minute_cutoff = current_time - 60  # 1 minute
        hour_cutoff = current_time - 3600  # 1 hour

        # Clean minute requests
        if identifier in self.minute_requests:
            self.minute_requests[identifier] = [
                t for t in self.minute_requests[identifier] if t > minute_cutoff
            ]

        # Clean hour requests
        if identifier in self.hour_requests:
            self.hour_requests[identifier] = [
                t for t in self.hour_requests[identifier] if t > hour_cutoff
            ]

        # Reset burst count if no recent requests
        if identifier in self.minute_requests and not self.minute_requests[identifier]:
            self.burst_counts[identifier] = 0

    def get_remaining_limits(self, identifier: str) -> Dict[str, int]:
        """
        Get remaining requests for each limit.

        Args:
            identifier: Unique identifier for the requester

        Returns:
            Dict with remaining limits
        """
        with self._lock:
            self._clean_old_requests(identifier, time.time())

            return {
                "minute_remaining": max(0, self.config.requests_per_minute - len(self.minute_requests.get(identifier, []))),
                "hour_remaining": max(0, self.config.requests_per_hour - len(self.hour_requests.get(identifier, []))),
                "burst_remaining": max(0, self.config.burst_limit - self.burst_counts.get(identifier, 0))
            }