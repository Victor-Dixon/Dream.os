"""
Session Test Fixtures - Trader Replay Journal
=============================================

Deterministic test data for replay sessions.
Provides golden fixtures for testing replay engine and scoring algorithms.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any


def create_test_candles(count: int = 12, base_price: float = 100.0) -> List[Dict[str, Any]]:
    """
    Create deterministic test candles.

    Args:
        count: Number of candles to create
        base_price: Starting price

    Returns:
        List of candle dictionaries
    """
    candles = []
    base_time = datetime(2024, 1, 15, 9, 30, 0)  # Market open
    price = base_price

    for i in range(count):
        timestamp = base_time + timedelta(minutes=i)
        open_price = price
        # Small random walk for realism
        change = (i % 3 - 1) * 0.5  # -0.5, 0, 0.5 pattern
        close_price = open_price + change
        high_price = max(open_price, close_price) + 0.3
        low_price = min(open_price, close_price) - 0.3
        volume = 1000 + (i * 100)

        candles.append({
            "timestamp": timestamp.isoformat(),
            "open": round(open_price, 2),
            "high": round(high_price, 2),
            "low": round(low_price, 2),
            "close": round(close_price, 2),
            "volume": volume,
        })

        price = close_price

    return candles


def create_disciplined_session_fixture() -> Dict[str, Any]:
    """
    Create a "disciplined" session fixture.

    Characteristics:
    - Proper stop loss usage
    - Patient trading (fewer trades)
    - Consistent position sizing
    - Good risk-reward ratios

    Returns:
        Dictionary with session data and trades
    """
    candles = create_test_candles(12, 100.0)
    base_time = datetime.fromisoformat(candles[0]["timestamp"])

    # Good trade 1: Entry after pattern, stop placed, target hit
    trade1 = {
        "entry_timestamp": (base_time + timedelta(minutes=2)).isoformat(),
        "entry_price": 100.5,
        "exit_timestamp": (base_time + timedelta(minutes=5)).isoformat(),
        "exit_price": 102.0,
        "quantity": 10,
        "side": "long",
        "entry_type": "market",
        "stop_loss": 99.5,
        "take_profit": 102.0,
        "pnl": 15.0,
        "r_multiple": 1.5,
        "status": "closed",
    }

    # Good trade 2: Small loss per plan
    trade2 = {
        "entry_timestamp": (base_time + timedelta(minutes=7)).isoformat(),
        "entry_price": 101.0,
        "exit_timestamp": (base_time + timedelta(minutes=8)).isoformat(),
        "exit_price": 99.5,
        "quantity": 10,
        "side": "long",
        "entry_type": "market",
        "stop_loss": 99.5,
        "take_profit": None,
        "pnl": -15.0,
        "r_multiple": -1.5,
        "status": "stopped",
    }

    return {
        "symbol": "TEST",
        "session_date": "2024-01-15",
        "timeframe": "1m",
        "candles": candles,
        "trades": [trade1, trade2],
        "expected_scores": {
            "stop_integrity": (80, 100),  # High - all trades have stops
            "patience": (70, 90),  # Good - only 2 trades
            "risk_discipline": (75, 95),  # Good - consistent sizing
            "rule_adherence": (80, 100),  # High - proper usage
        },
    }


def create_chaotic_session_fixture() -> Dict[str, Any]:
    """
    Create a "chaotic" session fixture.

    Characteristics:
    - No stop losses
    - Overtrading (many trades)
    - Inconsistent position sizing
    - Poor risk management

    Returns:
        Dictionary with session data and trades
    """
    candles = create_test_candles(12, 100.0)
    base_time = datetime.fromisoformat(candles[0]["timestamp"])

    # Bad trade 1: No stop, oversized position
    trade1 = {
        "entry_timestamp": (base_time + timedelta(minutes=1)).isoformat(),
        "entry_price": 100.2,
        "exit_timestamp": (base_time + timedelta(minutes=2)).isoformat(),
        "exit_price": 99.0,
        "quantity": 50,  # Oversized
        "side": "long",
        "entry_type": "market",
        "stop_loss": None,  # No stop
        "take_profit": None,
        "pnl": -60.0,
        "r_multiple": None,
        "status": "closed",
    }

    # Bad trade 2: Revenge trade, no stop
    trade2 = {
        "entry_timestamp": (base_time + timedelta(minutes=3)).isoformat(),
        "entry_price": 99.5,
        "exit_timestamp": (base_time + timedelta(minutes=4)).isoformat(),
        "exit_price": 98.5,
        "quantity": 30,
        "side": "long",
        "entry_type": "market",
        "stop_loss": None,
        "take_profit": None,
        "pnl": -30.0,
        "r_multiple": None,
        "status": "closed",
    }

    # Bad trade 3: Another overtrade
    trade3 = {
        "entry_timestamp": (base_time + timedelta(minutes=5)).isoformat(),
        "entry_price": 99.0,
        "exit_timestamp": (base_time + timedelta(minutes=6)).isoformat(),
        "exit_price": 99.5,
        "quantity": 20,
        "side": "long",
        "entry_type": "market",
        "stop_loss": None,
        "take_profit": None,
        "pnl": 10.0,
        "r_multiple": None,
        "status": "closed",
    }

    return {
        "symbol": "TEST",
        "session_date": "2024-01-15",
        "timeframe": "1m",
        "candles": candles,
        "trades": [trade1, trade2, trade3],
        "expected_scores": {
            "stop_integrity": (0, 20),  # Low - no stops used
            "patience": (20, 40),  # Low - overtrading
            "risk_discipline": (20, 40),  # Low - inconsistent sizing
            "rule_adherence": (20, 40),  # Low - poor risk management
        },
    }


def create_test_session_data(
    symbol: str = "TEST",
    session_date: str = "2024-01-15",
    candle_count: int = 12,
) -> Dict[str, Any]:
    """
    Create minimal test session data.

    Args:
        symbol: Trading symbol
        session_date: Session date (YYYY-MM-DD)
        candle_count: Number of candles

    Returns:
        Dictionary with session configuration
    """
    candles = create_test_candles(candle_count)

    return {
        "symbol": symbol,
        "session_date": session_date,
        "timeframe": "1m",
        "candles": candles,
    }



