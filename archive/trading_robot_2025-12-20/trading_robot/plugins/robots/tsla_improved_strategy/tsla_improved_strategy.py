"""
TSLA Improved Strategy (Risk-True)
===================================

Risk-based TSLA trading strategy converted from TradingView Pine Script.
Uses 50/200 MA crossover with RSI filtering and true risk-based position sizing.

Original Pine Script: Improved TSLA Strategy (Risk-True)
"""

from typing import Any, Dict
import pandas as pd
import numpy as np
from loguru import logger

from strategies.signal_processing import Signal, StrategyResult
from plugins.plugin_base import PluginBase
from plugins.plugin_metadata import PluginMetadata


class TslaImprovedStrategy(PluginBase):
    """TSLA Improved Strategy with risk-based position sizing."""

    def __init__(self, metadata: PluginMetadata, parameters: Dict[str, Any] = None):
        """Initialize TSLA strategy."""
        super().__init__(metadata, parameters)

        # Trend parameters
        self.ma_short_length = self.parameters.get("ma_short_length", 50)
        self.ma_long_length = self.parameters.get("ma_long_length", 200)

        # RSI parameters
        self.rsi_length = self.parameters.get("rsi_length", 14)
        self.rsi_overbought = self.parameters.get("rsi_overbought", 60)
        self.rsi_oversold = self.parameters.get("rsi_oversold", 40)

        # Risk model
        self.risk_pct_equity = self.parameters.get(
            "risk_pct_equity", 0.5)  # 0.5% of equity per trade
        self.stop_pct_price = self.parameters.get(
            "stop_pct_price", 1.0)  # 1% stop loss

        # Reward parameters
        self.target_pct_price = self.parameters.get(
            "target_pct_price", 15.0)  # 15% profit target
        self.use_trailing_stop = self.parameters.get("use_trailing_stop", True)
        self.trail_offset_pct = self.parameters.get("trail_offset_pct", 0.5)
        self.trail_trigger_pct = self.parameters.get("trail_trigger_pct", 5.0)

    def analyze(self, data: pd.DataFrame, symbol: str) -> StrategyResult:
        """Analyze market data and generate trading signal."""
        if not self.validate_data(data):
            return StrategyResult(symbol, Signal.HOLD, 0.0, metadata={"error": "Invalid data"})

        # Need at least long MA period of data
        if len(data) < self.ma_long_length:
            return StrategyResult(symbol, Signal.HOLD, 0.0, metadata={"error": "Insufficient data"})

        try:
            # Calculate indicators
            ma_short = self.indicators.sma(data["close"], self.ma_short_length)
            ma_long = self.indicators.sma(data["close"], self.ma_long_length)
            rsi = self.indicators.rsi(data["close"], self.rsi_length)

            if ma_short is None or ma_long is None or rsi is None:
                return StrategyResult(symbol, Signal.HOLD, 0.0, metadata={"error": "Indicator calculation failed"})

            # Get latest values
            current_price = data["close"].iloc[-1]
            ma_short_val = ma_short.iloc[-1] if isinstance(
                ma_short, pd.Series) else ma_short
            ma_long_val = ma_long.iloc[-1] if isinstance(
                ma_long, pd.Series) else ma_long
            rsi_val = rsi.iloc[-1] if isinstance(rsi, pd.Series) else rsi

            # Entry conditions
            # Long: above both MAs and RSI not overheated
            long_condition = (current_price > ma_short_val and current_price > ma_long_val) and (
                rsi_val < self.rsi_overbought)

            # Short: below both MAs and RSI not too washed
            short_condition = (current_price < ma_short_val and current_price < ma_long_val) and (
                rsi_val > self.rsi_oversold)

            # Determine signal
            if long_condition:
                signal = Signal.BUY
                confidence = min(
                    (current_price - ma_long_val) / ma_long_val * 10, 1.0)
            elif short_condition:
                signal = Signal.SELL
                confidence = min(
                    (ma_long_val - current_price) / ma_long_val * 10, 1.0)
            else:
                signal = Signal.HOLD
                confidence = 0.0

            # Metadata with indicator values
            metadata = {
                "ma_short": round(ma_short_val, 2),
                "ma_long": round(ma_long_val, 2),
                "rsi": round(rsi_val, 2),
                "current_price": round(current_price, 2),
                "long_condition": long_condition,
                "short_condition": short_condition,
            }

            return StrategyResult(symbol, signal, confidence, indicators=metadata)

        except Exception as e:
            logger.error(f"Error in TSLA strategy analysis: {e}")
            return StrategyResult(symbol, Signal.HOLD, 0.0, metadata={"error": str(e)})

    def calculate_entry_quantity(
        self, account_balance: float, price: float, stop_loss_price: float
    ) -> int:
        """Calculate position size based on risk model (true risk-based sizing)."""
        # Risk amount = equity * risk percentage
        risk_amount = account_balance * (self.risk_pct_equity / 100.0)

        # Stop distance in price
        stop_dist = abs(price - stop_loss_price)

        # Avoid divide-by-zero / ultra-low stops
        min_tick = 0.01  # Minimum price movement
        safe_stop_dist = max(stop_dist, min_tick * 10)

        # Quantity = risk amount / stop distance
        raw_qty = risk_amount / safe_stop_dist
        qty = int(np.floor(raw_qty))

        # Only trade if quantity is meaningful
        if qty < 1:
            logger.warning(
                f"Calculated quantity {qty} is too small, skipping trade")
            return 0

        logger.info(
            f"📊 Position sizing: Risk ${risk_amount:.2f}, Stop ${safe_stop_dist:.2f}, Qty: {qty}"
        )
        return qty

    def calculate_stop_loss(self, entry_price: float, is_long: bool) -> float:
        """Calculate stop loss price."""
        stop_pct = self.stop_pct_price / 100.0
        if is_long:
            return entry_price * (1 - stop_pct)
        else:  # Short
            return entry_price * (1 + stop_pct)

    def calculate_profit_target(self, entry_price: float, is_long: bool) -> float:
        """Calculate profit target price."""
        target_pct = self.target_pct_price / 100.0
        if is_long:
            return entry_price * (1 + target_pct)
        else:  # Short
            return entry_price * (1 - target_pct)

    def calculate_trailing_stop(
        self, entry_price: float, current_price: float, is_long: bool
    ) -> float:
        """Calculate trailing stop price."""
        if not self.use_trailing_stop:
            return self.calculate_stop_loss(entry_price, is_long)

        trail_trigger_pct = self.trail_trigger_pct / 100.0
        trail_offset_pct = self.trail_offset_pct / 100.0

        if is_long:
            # Check if price has moved in favor by trigger amount
            if current_price >= entry_price * (1 + trail_trigger_pct):
                # Trail stop at offset below current price
                return current_price * (1 - trail_offset_pct)
            else:
                # Use regular stop loss
                return self.calculate_stop_loss(entry_price, is_long)
        else:  # Short
            # Check if price has moved in favor by trigger amount
            if current_price <= entry_price * (1 - trail_trigger_pct):
                # Trail stop at offset above current price
                return current_price * (1 + trail_offset_pct)
            else:
                # Use regular stop loss
                return self.calculate_stop_loss(entry_price, is_long)

