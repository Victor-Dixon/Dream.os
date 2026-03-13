"""
FastAPI Rate Limiting Module.

SSOT: src/web/fastapi_rate_limiting.py
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict


@dataclass
class RateLimitConfig:
    """Basic rate limit configuration."""

    requests_per_minute: int = 60


def build_rate_limit_headers(config: RateLimitConfig) -> Dict[str, str]:
    """Return rate limit headers for API responses."""
    return {
        "X-RateLimit-Limit": str(config.requests_per_minute),
        "X-RateLimit-Remaining": str(config.requests_per_minute),
    }


def apply_rate_limit(config: RateLimitConfig, handler: Callable[[], object]) -> Callable[[], object]:
    """Wrap a handler with a no-op rate limit placeholder."""

    def _wrapped() -> object:
        return handler()

    return _wrapped
