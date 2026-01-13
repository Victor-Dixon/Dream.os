# <!-- SSOT Domain: trading_robot -->
"""Indicator calculations for TSLA report."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time
from zoneinfo import ZoneInfo

from ..providers.base import OHLCVBar


@dataclass(frozen=True)
class SessionStats:
    premarket_high: float
    premarket_low: float
    premarket_volume: float


@dataclass(frozen=True)
class IntradayIndicators:
    price: float
    vwap: float
    ema9: float
    ema21: float


@dataclass(frozen=True)
class DailyIndicators:
    atr14: float
    range_pct: float


EASTERN = ZoneInfo("America/New_York")


def compute_premarket_stats(bars: list[OHLCVBar]) -> SessionStats:
    premarket = [bar for bar in bars if _is_premarket(bar.timestamp)]
    if not premarket:
        return SessionStats(0.0, 0.0, 0.0)
    high = max(bar.high for bar in premarket)
    low = min(bar.low for bar in premarket)
    volume = sum(bar.volume for bar in premarket)
    return SessionStats(high, low, volume)


def compute_intraday_indicators(bars: list[OHLCVBar]) -> IntradayIndicators:
    regular_session = [bar for bar in bars if _is_regular_session(bar.timestamp)]
    target_bars = regular_session or bars
    last_price = target_bars[-1].close if target_bars else 0.0
    vwap = _compute_vwap(target_bars)
    closes = [bar.close for bar in target_bars]
    ema9 = _ema(closes, 9)
    ema21 = _ema(closes, 21)
    return IntradayIndicators(last_price, vwap, ema9, ema21)


def compute_daily_indicators(daily_bars: list[OHLCVBar]) -> DailyIndicators:
    if len(daily_bars) < 2:
        return DailyIndicators(0.0, 0.0)
    recent = daily_bars[-15:]
    atr = _atr(recent, period=14)
    latest = daily_bars[-1]
    range_pct = ((latest.high - latest.low) / latest.close) * 100 if latest.close else 0.0
    return DailyIndicators(atr, range_pct)


def _ema(values: list[float], period: int) -> float:
    if not values:
        return 0.0
    k = 2 / (period + 1)
    ema_value = values[0]
    for value in values[1:]:
        ema_value = value * k + ema_value * (1 - k)
    return ema_value


def _atr(bars: list[OHLCVBar], period: int) -> float:
    if len(bars) < 2:
        return 0.0
    trs = []
    for idx in range(1, len(bars)):
        current = bars[idx]
        prev = bars[idx - 1]
        tr = max(
            current.high - current.low,
            abs(current.high - prev.close),
            abs(current.low - prev.close),
        )
        trs.append(tr)
    if not trs:
        return 0.0
    relevant = trs[-period:]
    return sum(relevant) / len(relevant)


def _compute_vwap(bars: list[OHLCVBar]) -> float:
    if not bars:
        return 0.0
    total_volume = sum(bar.volume for bar in bars)
    if total_volume == 0:
        return 0.0
    total_price_volume = sum(((bar.high + bar.low + bar.close) / 3) * bar.volume for bar in bars)
    return total_price_volume / total_volume


def _is_premarket(timestamp: datetime) -> bool:
    localized = timestamp.replace(tzinfo=EASTERN) if timestamp.tzinfo is None else timestamp.astimezone(EASTERN)
    local_time = localized.time()
    return time(4, 0) <= local_time < time(9, 30)


def _is_regular_session(timestamp: datetime) -> bool:
    localized = timestamp.replace(tzinfo=EASTERN) if timestamp.tzinfo is None else timestamp.astimezone(EASTERN)
    local_time = localized.time()
    return time(9, 30) <= local_time <= time(16, 0)
