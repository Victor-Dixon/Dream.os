"""
Indicator Calculations for Morning Plan.

<!-- SSOT Domain: trading_robot -->
"""

from typing import Sequence

import pandas as pd


def macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    """Calculate MACD values for a dataframe containing Close prices."""
    close = df["Close"].astype(float)
    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    hist = macd_line - signal_line
    out = df.copy()
    out["MACD"] = macd_line
    out["SIGNAL"] = signal_line
    out["HIST"] = hist
    return out


def detect_macd_curl(last_hist_vals: Sequence[float]) -> bool:
    """
    Curl heuristic: histogram is still negative but rising with a higher low.
    Example: [-0.12, -0.09, -0.06] -> curl up.
    """
    if len(last_hist_vals) < 3:
        return False
    a, b, c = last_hist_vals[-3], last_hist_vals[-2], last_hist_vals[-1]
    return (a < b < c) and (c < 0)


def detect_macd_cross(macd_vals: pd.Series, signal_vals: pd.Series) -> bool:
    """Cross heuristic: MACD crosses SIGNAL on the latest bar."""
    if len(macd_vals) < 2 or len(signal_vals) < 2:
        return False
    prev = macd_vals.iloc[-2] - signal_vals.iloc[-2]
    curr = macd_vals.iloc[-1] - signal_vals.iloc[-1]
    return prev <= 0 and curr > 0
