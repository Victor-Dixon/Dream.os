"""
Plugin Base Class
=================

Base class for all trading robot plugins.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from datetime import datetime
import pandas as pd
from loguru import logger

from strategies.base_strategy import BaseStrategy
from strategies.signal_processing import Signal, StrategyResult
from .plugin_metadata import PluginMetadata


class PluginBase(BaseStrategy, ABC):
    """Base class for trading robot plugins."""

    def __init__(self, metadata: PluginMetadata, parameters: Dict[str, Any] = None):
        """Initialize plugin with metadata."""
        super().__init__(metadata.name, parameters or {})
        self.metadata = metadata
        self.performance_tracker = None
        self.paper_trades = []
        self.total_pnl = 0.0
        self.total_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0

    @abstractmethod
    def analyze(self, data: pd.DataFrame, symbol: str) -> StrategyResult:
        """Analyze market data and generate trading signal."""
        pass

    @abstractmethod
    def calculate_entry_quantity(
        self, account_balance: float, price: float, stop_loss_price: float
    ) -> int:
        """Calculate position size based on risk model."""
        pass

    @abstractmethod
    def calculate_stop_loss(self, entry_price: float, is_long: bool) -> float:
        """Calculate stop loss price."""
        pass

    @abstractmethod
    def calculate_profit_target(self, entry_price: float, is_long: bool) -> float:
        """Calculate profit target price."""
        pass

    def get_metadata(self) -> PluginMetadata:
        """Get plugin metadata."""
        return self.metadata

    def track_paper_trade(
        self,
        symbol: str,
        side: str,
        quantity: int,
        entry_price: float,
        stop_loss: float,
        profit_target: float,
        timestamp: datetime = None,
    ):
        """Track a paper trade for performance monitoring."""
        if timestamp is None:
            timestamp = datetime.now()

        trade = {
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "entry_price": entry_price,
            "stop_loss": stop_loss,
            "profit_target": profit_target,
            "entry_time": timestamp,
            "exit_time": None,
            "exit_price": None,
            "pnl": 0.0,
            "status": "OPEN",
        }

        self.paper_trades.append(trade)
        self.total_trades += 1
        logger.info(
            f"📊 Paper trade tracked: {side} {quantity} {symbol} @ ${entry_price:.2f}")

    def update_trade_exit(
        self, trade_index: int, exit_price: float, exit_time: datetime = None
    ):
        """Update trade with exit information."""
        if exit_time is None:
            exit_time = datetime.now()

        if 0 <= trade_index < len(self.paper_trades):
            trade = self.paper_trades[trade_index]
            trade["exit_time"] = exit_time
            trade["exit_price"] = exit_price
            trade["status"] = "CLOSED"

            # Calculate P&L
            if trade["side"] == "LONG":
                pnl = (exit_price - trade["entry_price"]) * trade["quantity"]
            else:  # SHORT
                pnl = (trade["entry_price"] - exit_price) * trade["quantity"]

            trade["pnl"] = pnl
            self.total_pnl += pnl

            if pnl > 0:
                self.winning_trades += 1
            else:
                self.losing_trades += 1

            logger.info(
                f"💰 Trade closed: {trade['side']} {trade['symbol']} P&L: ${pnl:.2f}"
            )

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary for the plugin."""
        closed_trades = [
            t for t in self.paper_trades if t["status"] == "CLOSED"]
        open_trades = [t for t in self.paper_trades if t["status"] == "OPEN"]

        win_rate = (
            (self.winning_trades / self.total_trades * 100)
            if self.total_trades > 0
            else 0.0
        )

        avg_win = (
            sum(t["pnl"]
                for t in closed_trades if t["pnl"] > 0) / self.winning_trades
            if self.winning_trades > 0
            else 0.0
        )

        avg_loss = (
            abs(sum(t["pnl"]
                for t in closed_trades if t["pnl"] < 0) / self.losing_trades)
            if self.losing_trades > 0
            else 0.0
        )

        profit_factor = (
            (sum(t["pnl"] for t in closed_trades if t["pnl"] > 0) / avg_loss)
            if avg_loss > 0
            else 0.0
        )

        return {
            "plugin_name": self.metadata.name,
            "plugin_id": self.metadata.plugin_id,
            "total_trades": self.total_trades,
            "closed_trades": len(closed_trades),
            "open_trades": len(open_trades),
            "winning_trades": self.winning_trades,
            "losing_trades": self.losing_trades,
            "win_rate": round(win_rate, 2),
            "total_pnl": round(self.total_pnl, 2),
            "average_win": round(avg_win, 2),
            "average_loss": round(avg_loss, 2),
            "profit_factor": round(profit_factor, 2),
            "is_for_sale": self.metadata.is_for_sale,
            "price": self.metadata.price,
        }

