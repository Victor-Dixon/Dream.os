"""
Core Trading Engine for Multi-Broker Trading Robot
"""
import asyncio
from datetime import datetime, time
from typing import Dict, List, Optional, Any
from decimal import Decimal
from loguru import logger

from config.settings import config
from .broker_factory import create_broker_client
from .broker_interface import BrokerInterface


class TradingEngine:
    """Core trading engine managing broker API interactions"""

    def __init__(self, broker_client: Optional[BrokerInterface] = None):
        self.broker: BrokerInterface = broker_client or create_broker_client()
        self.account = None
        self.positions = {}
        self.orders = {}
        self.is_running = False
        self.market_open = False

    async def initialize(self, skip_preflight: bool = False):
        """Initialize broker API connection with pre-flight validation"""
        try:
            broker_name = config.broker.upper()
            logger.info(f"🔗 Connecting to {broker_name} API...")

            # Pre-flight validation (unless explicitly skipped)
            if not skip_preflight:
                from core.preflight_validator import PreFlightValidator
                validator = PreFlightValidator(self.broker)
                passed, results = await validator.validate_all()

                if not passed:
                    error_msg = f"Pre-flight validation failed:\n{validator.get_validation_report()}"
                    logger.error(f"❌ {error_msg}")
                    raise ValueError(error_msg)

                logger.info("✅ Pre-flight validation passed")

            # Validate configuration
            config_valid, config_errors = config.validate_config()
            if not config_valid:
                error_msg = f"Configuration validation failed: {', '.join(config_errors)}"
                logger.error(f"❌ {error_msg}")
                raise ValueError(error_msg)

            # Warn if live trading mode
            if config.is_live_trading():
                logger.warning("⚠️ LIVE TRADING MODE ENABLED - Real money at risk!")
                logger.warning("⚠️ Ensure all risk limits are properly configured")
            else:
                logger.info("📄 Paper trading mode enabled")

            # Connect to broker
            if not self.broker.connect():
                raise ConnectionError(f"Failed to connect to {broker_name} API")

            # Test connection
            await self._test_connection()

            # Get account information
            await self._update_account_info()

            logger.info(f"✅ {broker_name} API connection established")

        except Exception as e:
            logger.error(f"❌ Failed to initialize {config.broker.upper()} API: {e}")
            raise

    async def _test_connection(self):
        """Test broker API connection"""
        try:
            # Test API connectivity
            clock = self.broker.get_market_clock()
            logger.info(f"🕒 Market clock: {clock}")

            # Check if market is open
            self.market_open = clock.get('is_open', False)

        except Exception as e:
            logger.error(f"❌ {config.broker.upper()} API connection test failed: {e}")
            raise

    async def _update_account_info(self):
        """Update account information"""
        try:
            self.account = self.broker.get_account_info()
            cash = self.account.get('cash', 0)
            portfolio_value = self.account.get('portfolio_value', 0)
            logger.info(f"💰 Account: ${cash:.2f} cash, ${portfolio_value:.2f} portfolio value")

        except Exception as e:
            logger.error(f"❌ Failed to get account info: {e}")
            raise

    async def start(self):
        """Start the trading engine"""
        try:
            logger.info("🚀 Starting trading engine...")
            self.is_running = True

            # Start market monitoring
            asyncio.create_task(self._monitor_market_status())

            # Start position monitoring
            asyncio.create_task(self._monitor_positions())

            logger.info("✅ Trading engine started")

        except Exception as e:
            logger.error(f"❌ Failed to start trading engine: {e}")
            raise

    async def stop(self):
        """Stop the trading engine"""
        try:
            logger.info("🛑 Stopping trading engine...")
            self.is_running = False

            # Cancel all open orders
            await self._cancel_all_orders()

            logger.info("✅ Trading engine stopped")

        except Exception as e:
            logger.error(f"❌ Error stopping trading engine: {e}")

    async def _monitor_market_status(self):
        """Monitor market open/close status"""
        while self.is_running:
            try:
                clock = self.broker.get_market_clock()
                market_was_open = self.market_open
                self.market_open = clock.get('is_open', False)

                if market_was_open != self.market_open:
                    status = "🟢 OPEN" if self.market_open else "🔴 CLOSED"
                    logger.info(f"📊 Market status changed: {status}")

                await asyncio.sleep(60)  # Check every minute

            except Exception as e:
                logger.error(f"❌ Error monitoring market status: {e}")
                await asyncio.sleep(30)

    async def _monitor_positions(self):
        """Monitor current positions"""
        while self.is_running:
            try:
                positions = self.broker.get_positions()
                self.positions = {pos['symbol']: pos for pos in positions}

                if positions:
                    position_strs = [f"{p['symbol']}:{p['qty']}" for p in positions]
                    logger.debug(f"📊 Current positions: {position_strs}")

                await asyncio.sleep(30)  # Update every 30 seconds

            except Exception as e:
                logger.error(f"❌ Error monitoring positions: {e}")
                await asyncio.sleep(30)

    async def get_market_data(self, symbol: str, timeframe: str = "1Min", limit: int = 100):
        """Get market data for a symbol"""
        try:
            df = self.broker.get_historical_data(symbol, timeframe, limit=limit)
            
            if df.empty:
                return []

            # Convert DataFrame to list of dicts
            return df.reset_index().to_dict('records')

        except Exception as e:
            logger.error(f"❌ Error getting market data for {symbol}: {e}")
            return []

    async def place_order(self, symbol: str, qty: int, side: str, order_type: str = "market",
                         time_in_force: str = "gtc", limit_price: Optional[float] = None):
        """Place a trading order"""
        try:
            if not self.market_open and order_type != "limit":
                logger.warning(f"⚠️ Market is closed, placing limit order for {symbol}")
                order_type = "limit"
                limit_price = limit_price or await self._get_current_price(symbol)

            if order_type == "market":
                order = self.broker.submit_market_order(symbol, qty, side, time_in_force)
            elif order_type == "limit":
                if limit_price is None:
                    limit_price = await self._get_current_price(symbol)
                order = self.broker.submit_limit_order(symbol, qty, side, limit_price, time_in_force)
            else:
                raise ValueError(f"Unsupported order type: {order_type}")

            if order:
                order_id = order.get('id', '')
                self.orders[order_id] = order
                logger.info(f"📋 Order placed: {side} {qty} {symbol} @ {order_type}")
                return order

            return None

        except Exception as e:
            logger.error(f"❌ Error placing order for {symbol}: {e}")
            return None

    async def _get_current_price(self, symbol: str) -> float:
        """Get current price for a symbol"""
        try:
            bars = await self.get_market_data(symbol, limit=1)
            if bars:
                return bars[0]['close']
            return 0.0
        except Exception as e:
            logger.error(f"❌ Error getting current price for {symbol}: {e}")
            return 0.0

    async def cancel_order(self, order_id: str):
        """Cancel an order"""
        try:
            if self.broker.cancel_order(order_id):
                if order_id in self.orders:
                    del self.orders[order_id]
                logger.info(f"❌ Order cancelled: {order_id}")
            else:
                logger.warning(f"⚠️ Failed to cancel order: {order_id}")

        except Exception as e:
            logger.error(f"❌ Error cancelling order {order_id}: {e}")

    async def _cancel_all_orders(self):
        """Cancel all open orders"""
        try:
            orders = self.broker.get_orders(status="open")
            for order in orders:
                await self.cancel_order(order.get('id', ''))
            logger.info("❌ All open orders cancelled")

        except Exception as e:
            logger.error(f"❌ Error cancelling all orders: {e}")

    async def get_portfolio_value(self) -> float:
        """Get current portfolio value"""
        try:
            await self._update_account_info()
            return float(self.account.get('portfolio_value', 0))
        except Exception as e:
            logger.error(f"❌ Error getting portfolio value: {e}")
            return 0.0

    async def get_account_balance(self) -> float:
        """Get account cash balance"""
        try:
            await self._update_account_info()
            return float(self.account.get('cash', 0))
        except Exception as e:
            logger.error(f"❌ Error getting account balance: {e}")
            return 0.0

    def is_market_open(self) -> bool:
        """Check if market is currently open"""
        return self.market_open

    def can_trade_symbol(self, symbol: str) -> bool:
        """Check if we can trade a symbol"""
        # Add your trading restrictions here
        return symbol not in ["", None]  # Basic check
