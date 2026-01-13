# <!-- SSOT Domain: trading_robot -->
"""Provider interfaces for market, options, and news data."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, Sequence


@dataclass(frozen=True)
class OHLCVBar:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass(frozen=True)
class OptionsChainSnapshot:
    asof_utc: datetime
    atm_strike: float
    near_atm: Sequence[dict]


class MarketDataProvider(Protocol):
    """Interface for market data providers."""

    name: str

    def get_intraday_bars(self, symbol: str, interval: str) -> Sequence[OHLCVBar]:
        """Return intraday bars for symbol at interval."""

    def get_daily_bars(self, symbol: str, outputsize: str = "compact") -> Sequence[OHLCVBar]:
        """Return daily bars for symbol."""


class OptionsDataProvider(Protocol):
    """Interface for options data providers."""

    name: str

    def get_chain_snapshot(self, symbol: str) -> OptionsChainSnapshot | None:
        """Return options chain snapshot or None if unavailable."""


class NewsProvider(Protocol):
    """Interface for news providers."""

    name: str

    def get_headlines(self, symbol: str) -> list[str]:
        """Return recent headlines for symbol."""
