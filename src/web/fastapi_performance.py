"""
FastAPI Performance Module.

SSOT: src/web/fastapi_performance.py
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class PerformanceConfig:
    """Configuration for performance tuning."""

    cache_control: str = "no-store"


def build_performance_headers(config: PerformanceConfig) -> Dict[str, str]:
    """Return performance-related headers."""
    return {
        "Cache-Control": config.cache_control,
        "X-Accel-Buffering": "no",
    }
