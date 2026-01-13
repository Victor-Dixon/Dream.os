# <!-- SSOT Domain: trading_robot -->
"""Alpha Vantage market data provider."""
from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime
from typing import Sequence

import requests

from .base import OHLCVBar, MarketDataProvider


@dataclass(frozen=True)
class AlphaVantageConfig:
    api_key: str
    base_url: str = "https://www.alphavantage.co/query"


class AlphaVantageMarketDataProvider:
    """Alpha Vantage implementation for market data."""

    name = "alpha_vantage"

    def __init__(self, config: AlphaVantageConfig | None = None) -> None:
        if config is None:
            api_key = os.getenv("ALPHA_VANTAGE_API_KEY", "").strip()
            if not api_key:
                raise ValueError("ALPHA_VANTAGE_API_KEY is required for Alpha Vantage provider")
            config = AlphaVantageConfig(api_key=api_key)
        self.config = config

    def get_intraday_bars(self, symbol: str, interval: str) -> Sequence[OHLCVBar]:
        payload = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol,
            "interval": interval,
            "outputsize": "compact",
            "apikey": self.config.api_key,
            "datatype": "json",
            "extended_hours": "true",
        }
        data = self._get_json(payload)
        return _parse_time_series(data, key_prefix="Time Series")

    def get_daily_bars(self, symbol: str, outputsize: str = "compact") -> Sequence[OHLCVBar]:
        payload = {
            "function": "TIME_SERIES_DAILY_ADJUSTED",
            "symbol": symbol,
            "outputsize": outputsize,
            "apikey": self.config.api_key,
            "datatype": "json",
        }
        data = self._get_json(payload)
        return _parse_time_series(data, key_prefix="Time Series")

    def _get_json(self, payload: dict) -> dict:
        response = requests.get(self.config.base_url, params=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        if "Error Message" in data:
            raise RuntimeError(f"Alpha Vantage error: {data['Error Message']}")
        if "Note" in data:
            raise RuntimeError(f"Alpha Vantage rate limit: {data['Note']}")
        return data


def _parse_time_series(data: dict, key_prefix: str) -> Sequence[OHLCVBar]:
    series_key = next((k for k in data.keys() if k.startswith(key_prefix)), None)
    if not series_key:
        raise KeyError("Time series data not found in provider response")
    series = data[series_key]
    bars: list[OHLCVBar] = []
    for timestamp_str, values in series.items():
        timestamp = datetime.fromisoformat(timestamp_str)
        bars.append(
            OHLCVBar(
                timestamp=timestamp,
                open=float(values["1. open"]),
                high=float(values["2. high"]),
                low=float(values["3. low"]),
                close=float(values["4. close"]),
                volume=float(values["5. volume"]),
            )
        )
    bars.sort(key=lambda bar: bar.timestamp)
    return bars
