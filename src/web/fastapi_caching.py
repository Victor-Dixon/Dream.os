"""
FastAPI Caching Module.

SSOT: src/web/fastapi_caching.py
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class CacheConfig:
    """Caching configuration."""

    ttl_seconds: int = 60


def build_cache_headers(config: CacheConfig) -> Dict[str, str]:
    """Return cache headers for API responses."""
    return {
        "Cache-Control": f"public, max-age={config.ttl_seconds}",
        "X-Cache-TTL": str(config.ttl_seconds),
    }
