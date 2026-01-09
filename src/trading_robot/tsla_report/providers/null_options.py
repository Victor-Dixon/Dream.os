# <!-- SSOT Domain: trading_robot -->
"""Null options provider used when options data is unavailable."""
from __future__ import annotations

from datetime import datetime, timezone

from .base import OptionsChainSnapshot, OptionsDataProvider


class NullOptionsProvider:
    """Placeholder options provider that signals unavailable data."""

    name = "unavailable"

    def get_chain_snapshot(self, symbol: str) -> OptionsChainSnapshot | None:
        _ = symbol
        return OptionsChainSnapshot(
            asof_utc=datetime.now(timezone.utc),
            atm_strike=0.0,
            near_atm=[],
        )
