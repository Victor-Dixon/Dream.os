# <!-- SSOT Domain: trading_robot -->
"""Orchestrates TSLA report pipeline."""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .engine.scenario_builder import build_regime, build_recommendations, confidence_score
import os

from .features.indicators import compute_daily_indicators, compute_intraday_indicators, compute_premarket_stats

from .providers.alpha_vantage import AlphaVantageMarketDataProvider
from .providers.base import MarketDataProvider
from .providers.null_options import NullOptionsProvider


def build_snapshot(
    symbol: str,
    provider: MarketDataProvider,
) -> tuple[dict[str, Any], dict[str, Any]]:
    intraday_1m = list(provider.get_intraday_bars(symbol, "1min"))
    intraday_5m = list(provider.get_intraday_bars(symbol, "5min"))
    daily = list(provider.get_daily_bars(symbol))
    if not intraday_1m or not daily:
        raise RuntimeError("Missing required market data for snapshot")
    premarket = compute_premarket_stats(intraday_1m)
    intraday_indicators = compute_intraday_indicators(intraday_1m)
    daily_indicators = compute_daily_indicators(daily)
    prior_day = daily[-2] if len(daily) >= 2 else daily[-1]
    gap_pct = ((intraday_indicators.price - prior_day.close) / prior_day.close) * 100 if prior_day.close else 0.0
    levels = {
        "PMH": premarket.premarket_high,
        "PML": premarket.premarket_low,
        "PDH": prior_day.high,
        "PDL": prior_day.low,
        "VWAP": intraday_indicators.vwap,
        "ATR_UP": prior_day.close + daily_indicators.atr14,
        "ATR_DN": prior_day.close - daily_indicators.atr14,
    }
    regime = build_regime(
        intraday_indicators.price,
        intraday_indicators.vwap,
        intraday_indicators.ema9,
        intraday_indicators.ema21,
        daily_indicators.range_pct,
    )
    confidence = confidence_score(regime, gap_pct)
    recs = build_recommendations(levels, regime, confidence)
    options_snapshot = NullOptionsProvider().get_chain_snapshot(symbol)
    snapshot = {
        "asof_utc": datetime.now(timezone.utc).isoformat(),
        "ticker": symbol,
        "session_context": {
            "premarket": {
                "high": premarket.premarket_high,
                "low": premarket.premarket_low,
                "volume": premarket.premarket_volume,
            },
            "prior_day": {
                "open": prior_day.open,
                "high": prior_day.high,
                "low": prior_day.low,
                "close": prior_day.close,
            },
            "gap_pct": gap_pct,
        },
        "intraday": {
            "price": intraday_indicators.price,
            "vwap": intraday_indicators.vwap,
            "ema9": intraday_indicators.ema9,
            "ema21": intraday_indicators.ema21,
            "atr14": daily_indicators.atr14,
            "range_pct": daily_indicators.range_pct,
        },
        "levels": levels,
        "options": {
            "available": bool(options_snapshot and options_snapshot.near_atm),
            "chain_asof_utc": options_snapshot.asof_utc.isoformat() if options_snapshot else None,
            "atm_strike": options_snapshot.atm_strike if options_snapshot else None,
            "near_atm": options_snapshot.near_atm if options_snapshot else [],
        },
        "regime": asdict(regime),
        "confidence": confidence,
        "recommendations": [asdict(rec) for rec in recs],
        "providers": {"market": provider.name, "options": "unavailable"},
        "raw": {"intraday_1m": len(intraday_1m), "intraday_5m": len(intraday_5m), "daily": len(daily)},
    }
    report_context = {
        "intraday_1m": intraday_1m,
        "intraday_5m": intraday_5m,
        "daily": daily,
    }
    return snapshot, report_context


def snapshot_hash(snapshot: dict[str, Any]) -> str:
    payload = json.dumps(snapshot, sort_keys=True).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def archive_artifacts(snapshot: dict[str, Any], report_md: str, payload: dict[str, Any]) -> Path:
    day = snapshot["asof_utc"].split("T")[0]
    target_dir = Path("data/devlogs") / day
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "analysis_snapshot.json").write_text(json.dumps(snapshot, indent=2))
    (target_dir / "report.md").write_text(report_md)
    (target_dir / "discord_payload.json").write_text(json.dumps(payload, indent=2))
    return target_dir


def get_market_provider() -> MarketDataProvider:
    provider_name = os.getenv("TSLA_MARKET_PROVIDER", "alpha_vantage").lower()
    providers = {
        "alpha_vantage": AlphaVantageMarketDataProvider,
    }
    provider_cls = providers.get(provider_name)
    if not provider_cls:
        raise ValueError(f"Unsupported market provider: {provider_name}")
    return provider_cls()
