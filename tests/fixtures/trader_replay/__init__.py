"""
Trader replay test fixtures.
Lightweight data to satisfy replay/scoring tests.
"""

from datetime import datetime, timedelta


def _make_candle(ts: datetime, o=100.0, h=101.0, l=99.0, c=100.5, v=1000):
    return {
        "timestamp": ts.isoformat(),
        "open": o,
        "high": h,
        "low": l,
        "close": c,
        "volume": v,
    }


def create_test_candles(count: int = 12):
    now = datetime(2024, 1, 15, 9, 30)
    return [_make_candle(now + timedelta(minutes=i)) for i in range(count)]


def create_test_session_data(symbol: str = "TEST", candle_count: int = 12):
    candles = create_test_candles(candle_count)
    return {
        "symbol": symbol,
        "session_date": "2024-01-15",
        "timeframe": "1m",
        "candles": candles,
    }


def create_disciplined_session_fixture():
    candles = create_test_candles(10)
    trades = [
        {
            "entry_timestamp": candles[1]["timestamp"],
            "exit_timestamp": candles[4]["timestamp"],
            "entry_price": 100.0,
            "exit_price": 101.0,
            "quantity": 10,
            "side": "BUY",
            "entry_type": "market",
            "stop_loss": 99.0,
            "take_profit": 102.0,
            "pnl": 10.0,
            "r_multiple": 1.0,
            "status": "CLOSED",
        },
        {
            "entry_timestamp": candles[5]["timestamp"],
            "exit_timestamp": candles[7]["timestamp"],
            "entry_price": 101.0,
            "exit_price": 102.0,
            "quantity": 5,
            "side": "BUY",
            "entry_type": "limit",
            "stop_loss": 99.5,
            "take_profit": 103.0,
            "pnl": 5.0,
            "r_multiple": 0.8,
            "status": "CLOSED",
        },
    ]
    expected_scores = {
        "stop_integrity": (0.5, 1.0),
        "patience": (0.5, 1.0),
    }
    return {
        "symbol": "DISC",
        "session_date": "2024-01-15",
        "timeframe": "1m",
        "candles": candles,
        "trades": trades,
        "expected_scores": expected_scores,
    }


def create_chaotic_session_fixture():
    candles = create_test_candles(10)
    trades = [
        {
            "entry_timestamp": candles[1]["timestamp"],
            "exit_timestamp": candles[2]["timestamp"],
            "entry_price": 100.0,
            "exit_price": 98.0,
            "quantity": 20,
            "side": "BUY",
            "entry_type": "market",
            "stop_loss": 97.0,
            "take_profit": 101.0,
            "pnl": -40.0,
            "r_multiple": -1.0,
            "status": "CLOSED",
        },
        {
            "entry_timestamp": candles[3]["timestamp"],
            "exit_timestamp": candles[3]["timestamp"],
            "entry_price": 99.0,
            "exit_price": 99.0,
            "quantity": 10,
            "side": "SELL",
            "entry_type": "market",
            "stop_loss": 101.0,
            "take_profit": 97.0,
            "pnl": 0.0,
            "r_multiple": 0.0,
            "status": "CLOSED",
        },
    ]
    expected_scores = {
        "stop_integrity": (0.0, 0.6),
        "patience": (0.0, 0.6),
    }
    return {
        "symbol": "CHAOS",
        "session_date": "2024-01-15",
        "timeframe": "1m",
        "candles": candles,
        "trades": trades,
        "expected_scores": expected_scores,
    }


__all__ = [
    "create_disciplined_session_fixture",
    "create_chaotic_session_fixture",
    "create_test_candles",
    "create_test_session_data",
]
"""
Trader Replay Test Fixtures
============================

Test fixtures for trading replay journal system.
Provides deterministic test data for replay, scoring, and repository tests.
"""

from .session_fixtures import (
    create_test_candles,
    create_disciplined_session_fixture,
    create_chaotic_session_fixture,
    create_test_session_data,
)

__all__ = [
    "create_test_candles",
    "create_disciplined_session_fixture",
    "create_chaotic_session_fixture",
    "create_test_session_data",
]



