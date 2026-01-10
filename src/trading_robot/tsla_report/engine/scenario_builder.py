# <!-- SSOT Domain: trading_robot -->
"""Scenario and recommendation engine for TSLA report."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class Regime:
    trend: str
    volatility: str


@dataclass(frozen=True)
class Recommendation:
    setup_type: str
    direction: str
    confidence: float
    trigger: dict[str, Any]
    entry_assumption: dict[str, Any]
    stop: dict[str, Any]
    target: dict[str, Any]
    timebox_minutes: int
    notes: str
    created_utc: str


def build_regime(price: float, vwap: float, ema9: float, ema21: float, range_pct: float) -> Regime:
    if ema9 > ema21 and price >= vwap:
        trend = "up"
    elif ema9 < ema21 and price <= vwap:
        trend = "down"
    else:
        trend = "range"
    if range_pct >= 4:
        volatility = "high"
    elif range_pct <= 2:
        volatility = "low"
    else:
        volatility = "normal"
    return Regime(trend=trend, volatility=volatility)


def confidence_score(regime: Regime, gap_pct: float) -> float:
    base = 0.55
    if regime.trend != "range":
        base += 0.15
    if regime.volatility == "high":
        base += 0.05
    if abs(gap_pct) >= 2:
        base += 0.05
    return min(0.85, max(0.3, base))


def build_recommendations(
    levels: dict[str, float],
    regime: Regime,
    confidence: float,
) -> list[Recommendation]:
    now = datetime.now(timezone.utc).isoformat()
    recs: list[Recommendation] = []
    if regime.trend == "range" and confidence < 0.55:
        recs.append(_wait(now, "Chop filter: low confidence range."))
        return recs
    if regime.trend == "up":
        recs.append(
            Recommendation(
                setup_type="BREAKOUT_CALL",
                direction="long",
                confidence=confidence,
                trigger={"type": "level_break", "level": levels["PMH"]},
                entry_assumption={"type": "market_on_trigger", "price": levels["PMH"]},
                stop={"price": levels["VWAP"], "rule": "hard"},
                target={"price": levels["ATR_UP"], "rule": "first_touch"},
                timebox_minutes=60,
                notes="Break above PMH with strength; respect VWAP.",
                created_utc=now,
            )
        )
    if regime.trend == "down":
        recs.append(
            Recommendation(
                setup_type="BREAKDOWN_PUT",
                direction="short",
                confidence=confidence,
                trigger={"type": "level_break", "level": levels["PML"]},
                entry_assumption={"type": "market_on_trigger", "price": levels["PML"]},
                stop={"price": levels["VWAP"], "rule": "hard"},
                target={"price": levels["ATR_DN"], "rule": "first_touch"},
                timebox_minutes=60,
                notes="Break below PML with momentum; invalidate above VWAP.",
                created_utc=now,
            )
        )
    if len(recs) < 2 and regime.trend == "range":
        mid = (levels["PMH"] + levels["PML"]) / 2
        recs.append(
            Recommendation(
                setup_type="RANGE_SCALP",
                direction="long",
                confidence=confidence,
                trigger={"type": "vwap_reclaim", "level": levels["VWAP"]},
                entry_assumption={"type": "limit", "price": mid},
                stop={"price": levels["PML"], "rule": "hard"},
                target={"price": levels["PMH"], "rule": "first_touch"},
                timebox_minutes=45,
                notes="Range scalp between PML/PMH with VWAP reclaim.",
                created_utc=now,
            )
        )
    if not recs:
        recs.append(_wait(now, "No clean setup. WAIT."))
    if len(recs) > 2:
        recs = recs[:2]
    return recs


def _wait(created_utc: str, reason: str) -> Recommendation:
    return Recommendation(
        setup_type="WAIT",
        direction="none",
        confidence=0.4,
        trigger={"type": "none", "level": 0},
        entry_assumption={"type": "none", "price": 0},
        stop={"price": 0, "rule": "none"},
        target={"price": 0, "rule": "none"},
        timebox_minutes=0,
        notes=reason,
        created_utc=created_utc,
    )
