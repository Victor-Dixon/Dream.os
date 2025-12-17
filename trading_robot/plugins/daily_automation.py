"""
Daily Automation System
========================

Automates daily trading plan execution for plugins.
Handles paper trading, performance tracking, and reporting.
"""

import asyncio
from datetime import datetime, time
from typing import Dict, List, Optional, Any
from pathlib import Path
import json
from loguru import logger
import pandas as pd

from plugins.plugin_manager import PluginManager
from plugins.plugin_base import PluginBase
from core.trading_engine import TradingEngine
from core.broker_interface import BrokerInterface
from strategies.signal_processing import Signal


class DailyAutomation:
    """Daily automation system for trading robot plugins."""

    def __init__(
        self,
        plugin_manager: PluginManager,
        trading_engine: TradingEngine,
        data_directory: str = "data/plugins",
    ):
        """Initialize daily automation."""
        self.plugin_manager = plugin_manager
        self.trading_engine = trading_engine
        self.data_directory = Path(data_directory)
        self.data_directory.mkdir(parents=True, exist_ok=True)
        self.active_plugins: Dict[str, PluginBase] = {}

    async def load_plugin_for_trading(self, plugin_id: str, parameters: Dict[str, Any] = None):
        """Load a plugin for daily trading."""
        plugin = self.plugin_manager.load_plugin(plugin_id, parameters)
        if plugin:
            self.active_plugins[plugin_id] = plugin
            logger.info(f"✅ Plugin {plugin_id} loaded for daily trading")
            return plugin
        else:
            logger.error(f"❌ Failed to load plugin {plugin_id}")
            return None

    async def execute_daily_plan(self, plugin_id: str, symbol: str = None):
        """Execute daily trading plan for a plugin."""
        if plugin_id not in self.active_plugins:
            logger.error(f"Plugin {plugin_id} not loaded")
            return None

        plugin = self.active_plugins[plugin_id]
        metadata = plugin.get_metadata()

        # Use symbol from metadata if not provided
        if symbol is None:
            symbol = metadata.symbol

        logger.info(f"📅 Executing daily plan for {plugin_id} ({symbol})")

        try:
            # Get market data
            market_data = await self.get_market_data(symbol)
            if market_data is None or market_data.empty:
                logger.error(f"Failed to get market data for {symbol}")
                return None

            # Analyze with plugin
            result = plugin.analyze(market_data, symbol)

            if result.signal == Signal.HOLD:
                logger.info(f"⏸️  No signal for {symbol}, holding")
                return {"action": "HOLD", "symbol": symbol, "reason": "No signal"}

            # Get account balance for position sizing
            account = await self.trading_engine.get_account()
            account_balance = float(account.get(
                "portfolio_value", 100000))  # Default $100k

            # Calculate entry price (current market price)
            current_price = market_data["close"].iloc[-1]

            # Determine if long or short
            is_long = result.signal == Signal.BUY

            # Calculate stop loss and profit target
            stop_loss = plugin.calculate_stop_loss(current_price, is_long)
            profit_target = plugin.calculate_profit_target(
                current_price, is_long)

            # Calculate position size
            quantity = plugin.calculate_entry_quantity(
                account_balance, current_price, stop_loss)

            if quantity == 0:
                logger.warning(f"Position size too small, skipping trade")
                return {"action": "SKIP", "symbol": symbol, "reason": "Position size too small"}

            # Execute paper trade
            trade_result = await self.execute_paper_trade(
                plugin=plugin,
                symbol=symbol,
                side="LONG" if is_long else "SHORT",
                quantity=quantity,
                entry_price=current_price,
                stop_loss=stop_loss,
                profit_target=profit_target,
            )

            # Save daily plan result
            await self.save_daily_plan_result(plugin_id, symbol, trade_result)

            return trade_result

        except Exception as e:
            logger.error(f"Error executing daily plan for {plugin_id}: {e}")
            return None

    async def get_market_data(self, symbol: str, period: str = "1y") -> Optional[pd.DataFrame]:
        """Get market data for symbol."""
        try:
            # Use trading engine's broker to get market data
            broker = self.trading_engine.broker
            if hasattr(broker, "get_bars"):
                bars = await broker.get_bars(symbol, period)
                if bars:
                    # Convert to DataFrame
                    df = pd.DataFrame(bars)
                    df.set_index("timestamp", inplace=True)
                    return df
            else:
                logger.warning(
                    "Broker does not support get_bars, using mock data")
                # Return mock data for testing
                return self._generate_mock_data(symbol)

        except Exception as e:
            logger.error(f"Error getting market data: {e}")
            return None

    def _generate_mock_data(self, symbol: str) -> pd.DataFrame:
        """Generate mock market data for testing."""
        import numpy as np
        dates = pd.date_range(end=datetime.now(), periods=252, freq="D")
        prices = 200 + np.cumsum(np.random.randn(252) * 2)
        df = pd.DataFrame(
            {
                "open": prices * 0.99,
                "high": prices * 1.02,
                "low": prices * 0.98,
                "close": prices,
                "volume": np.random.randint(1000000, 5000000, 252),
            },
            index=dates,
        )
        return df

    async def execute_paper_trade(
        self,
        plugin: PluginBase,
        symbol: str,
        side: str,
        quantity: int,
        entry_price: float,
        stop_loss: float,
        profit_target: float,
    ) -> Dict[str, Any]:
        """Execute a paper trade and track it."""
        logger.info(
            f"📝 Paper trade: {side} {quantity} {symbol} @ ${entry_price:.2f} "
            f"(Stop: ${stop_loss:.2f}, Target: ${profit_target:.2f})"
        )

        # Track the trade
        plugin.track_paper_trade(
            symbol=symbol,
            side=side,
            quantity=quantity,
            entry_price=entry_price,
            stop_loss=stop_loss,
            profit_target=profit_target,
            timestamp=datetime.now(),
        )

        # Save trade to file
        await self.save_paper_trade(plugin, symbol, side, quantity, entry_price, stop_loss, profit_target)

        return {
            "action": "TRADE",
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "entry_price": entry_price,
            "stop_loss": stop_loss,
            "profit_target": profit_target,
            "timestamp": datetime.now().isoformat(),
        }

    async def save_paper_trade(
        self,
        plugin: PluginBase,
        symbol: str,
        side: str,
        quantity: int,
        entry_price: float,
        stop_loss: float,
        profit_target: float,
    ):
        """Save paper trade to file."""
        plugin_id = plugin.metadata.plugin_id
        trade_file = self.data_directory / plugin_id / "trades.jsonl"

        trade_file.parent.mkdir(parents=True, exist_ok=True)

        trade_data = {
            "plugin_id": plugin_id,
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "entry_price": entry_price,
            "stop_loss": stop_loss,
            "profit_target": profit_target,
            "timestamp": datetime.now().isoformat(),
            "status": "OPEN",
        }

        with open(trade_file, "a") as f:
            f.write(json.dumps(trade_data) + "\n")

    async def save_daily_plan_result(
        self, plugin_id: str, symbol: str, result: Dict[str, Any]
    ):
        """Save daily plan execution result."""
        result_file = self.data_directory / plugin_id / "daily_plans.jsonl"

        result_file.parent.mkdir(parents=True, exist_ok=True)

        plan_data = {
            "plugin_id": plugin_id,
            "symbol": symbol,
            "date": datetime.now().date().isoformat(),
            "result": result,
            "timestamp": datetime.now().isoformat(),
        }

        with open(result_file, "a") as f:
            f.write(json.dumps(plan_data) + "\n")

    async def get_performance_report(self, plugin_id: str) -> Dict[str, Any]:
        """Get performance report for a plugin."""
        if plugin_id not in self.active_plugins:
            return None

        plugin = self.active_plugins[plugin_id]
        return plugin.get_performance_summary()

    async def update_trade_exits(self, plugin_id: str):
        """Update trade exits based on current market prices."""
        if plugin_id not in self.active_plugins:
            return

        plugin = self.active_plugins[plugin_id]
        metadata = plugin.get_metadata()
        symbol = metadata.symbol

        # Get current market price
        market_data = await self.get_market_data(symbol)
        if market_data is None:
            return

        current_price = market_data["close"].iloc[-1]

        # Check all open trades
        for i, trade in enumerate(plugin.paper_trades):
            if trade["status"] == "OPEN":
                # Check if stop loss or profit target hit
                should_exit = False
                exit_price = current_price

                if trade["side"] == "LONG":
                    if current_price <= trade["stop_loss"]:
                        should_exit = True
                        exit_price = trade["stop_loss"]
                    elif current_price >= trade["profit_target"]:
                        should_exit = True
                        exit_price = trade["profit_target"]
                else:  # SHORT
                    if current_price >= trade["stop_loss"]:
                        should_exit = True
                        exit_price = trade["stop_loss"]
                    elif current_price <= trade["profit_target"]:
                        should_exit = True
                        exit_price = trade["profit_target"]

                if should_exit:
                    plugin.update_trade_exit(i, exit_price)
                    logger.info(
                        f"✅ Trade closed: {trade['side']} {trade['symbol']} @ ${exit_price:.2f}"
                    )

