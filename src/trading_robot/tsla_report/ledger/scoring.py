# <!-- SSOT Domain: trading_robot -->
"""Recommendation scoring logic."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Iterable

from ..providers.base import MarketDataProvider, OHLCVBar


@dataclass(frozen=True)
class ScoreResult:
    rec_id: str
    scored_utc: str
    result: str
    mfe: float
    mae: float
    r_multiple: float
    hit_target: bool
    hit_stop: bool
    triggered: bool
    assumptions: dict


def score_recommendations(
    provider: MarketDataProvider,
    recommendations: Iterable[dict],
    *,
    slippage: float = 0.02,
) -> list[ScoreResult]:
    results: list[ScoreResult] = []
    for rec in recommendations:
        if rec.get("setup_type") == "WAIT":
            results.append(
                ScoreResult(
                    rec_id=rec["rec_id"],
                    scored_utc=datetime.now(timezone.utc).isoformat(),
                    result="invalid",
                    mfe=0.0,
                    mae=0.0,
                    r_multiple=0.0,
                    hit_target=False,
                    hit_stop=False,
                    triggered=False,
                    assumptions={"slippage": slippage, "fees": 0.0},
                )
            )
            continue
        created = datetime.fromisoformat(rec["created_utc"]).replace(tzinfo=timezone.utc)
        timebox = timedelta(minutes=rec["timebox_minutes"]) if rec["timebox_minutes"] else timedelta(hours=6)
        window_end = created + timebox
        bars = provider.get_intraday_bars(rec["ticker"], "1min")
        window = [bar for bar in bars if created <= _ensure_utc(bar.timestamp) <= window_end]
        score = _score_rec(rec, window, slippage)
        results.append(score)
    return results


def _score_rec(rec: dict, bars: list[OHLCVBar], slippage: float) -> ScoreResult:
    trigger_level = float(rec["trigger"]["level"])
    stop_level = float(rec["stop"]["price"])
    target_level = float(rec["target"]["price"])
    direction = rec["direction"]
    triggered = False
    hit_target = False
    hit_stop = False
    entry_price = trigger_level
    mfe = 0.0
    mae = 0.0
    for bar in bars:
        bar_high = bar.high
        bar_low = bar.low
        if not triggered:
            if bar_low <= trigger_level <= bar_high:
                triggered = True
                entry_price = trigger_level + (slippage if direction == "long" else -slippage)
            else:
                continue
        favorable = (bar_high - entry_price) if direction == "long" else (entry_price - bar_low)
        adverse = (entry_price - bar_low) if direction == "long" else (bar_high - entry_price)
        mfe = max(mfe, favorable)
        mae = max(mae, adverse)
        if direction == "long":
            if bar_high >= target_level:
                hit_target = True
                break
            if bar_low <= stop_level:
                hit_stop = True
                break
        if direction == "short":
            if bar_low <= target_level:
                hit_target = True
                break
            if bar_high >= stop_level:
                hit_stop = True
                break
    result = _determine_result(triggered, hit_target, hit_stop)
    r_multiple = _calc_r(entry_price, stop_level, target_level, result, direction)
    return ScoreResult(
        rec_id=rec["rec_id"],
        scored_utc=datetime.now(timezone.utc).isoformat(),
        result=result,
        mfe=mfe,
        mae=mae,
        r_multiple=r_multiple,
        hit_target=hit_target,
        hit_stop=hit_stop,
        triggered=triggered,
        assumptions={"slippage": slippage, "fees": 0.0},
    )


def _determine_result(triggered: bool, hit_target: bool, hit_stop: bool) -> str:
    if not triggered:
        return "no_trigger"
    if hit_target:
        return "win"
    if hit_stop:
        return "loss"
    return "timeout"


def _calc_r(entry: float, stop: float, target: float, result: str, direction: str) -> float:
    risk = abs(entry - stop)
    if risk == 0:
        return 0.0
    if result == "win":
        return abs(target - entry) / risk
    if result == "loss":
        return -1.0
    return 0.0


def _ensure_utc(ts: datetime) -> datetime:
    if ts.tzinfo is None:
        return ts.replace(tzinfo=timezone.utc)
    return ts.astimezone(timezone.utc)
