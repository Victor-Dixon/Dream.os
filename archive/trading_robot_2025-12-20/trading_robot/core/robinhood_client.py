"""
Robinhood API Client Wrapper using robin_stocks library
"""
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import pandas as pd
from loguru import logger

try:
    import robin_stocks.robinhood as rh
    ROBINHOOD_AVAILABLE = True
except ImportError:
    ROBINHOOD_AVAILABLE = False
    logger.warning("robin_stocks library not installed. Install with: pip install robin_stocks")

from config.settings import config
from .broker_interface import BrokerInterface


class RobinhoodClient(BrokerInterface):
    """Wrapper for Robinhood API interactions using robin_stocks library"""

    def __init__(self):
        self._connected = False
        self.username = None
        self.password = None

    def connect(self) -> bool:
        """Establish connection to Robinhood API"""
        if not ROBINHOOD_AVAILABLE:
            logger.error("robin_stocks library not available. Install with: pip install robin_stocks")
            return False

        try:
            # Get credentials from config or environment
            # Note: robin_stocks uses username/password, not API keys
            self.username = getattr(config, 'robinhood_username', '')
            self.password = getattr(config, 'robinhood_password', '')

            if not self.username or not self.password:
                logger.error("Robinhood username and password required")
                return False

            # Login to Robinhood
            login_response = rh.login(self.username, self.password)
            
            if login_response:
                self._connected = True
                logger.info("✅ Connected to Robinhood API")
                return True
            else:
                logger.error("❌ Failed to login to Robinhood")
                return False

        except Exception as e:
            logger.error(f"❌ Failed to connect to Robinhood API: {e}")
            logger.warning("⚠️ Note: Robinhood API access is unofficial and may violate ToS")
            return False

    def is_connected(self) -> bool:
        """Check if connected to Robinhood API"""
        return self._connected and ROBINHOOD_AVAILABLE

    def get_account_info(self) -> Dict[str, Any]:
        """Get account information"""
        if not self._connected:
            raise ConnectionError("Not connected to Robinhood API")

        try:
            account = rh.load_account_profile()
            positions = rh.get_open_stock_positions()
            
            # Calculate portfolio value
            portfolio_value = float(account.get('portfolio_value', 0))
            cash = float(account.get('cash', 0))
            buying_power = float(account.get('buying_power', 0))

            return {
                'id': account.get('account_number', ''),
                'cash': cash,
                'portfolio_value': portfolio_value,
                'buying_power': buying_power,
                'daytrade_count': account.get('day_trade_buying_power', 0),
                'status': account.get('account_status', 'unknown')
            }
        except Exception as e:
            logger.error(f"❌ Error getting account info: {e}")
            return {}

    def get_positions(self) -> List[Dict[str, Any]]:
        """Get current positions"""
        if not self._connected:
            raise ConnectionError("Not connected to Robinhood API")

        try:
            positions = rh.get_open_stock_positions()
            result = []

            for pos in positions:
                symbol = rh.get_symbol_by_url(pos['instrument'])
                quote = rh.get_quotes(symbol)[0] if symbol else {}
                
                result.append({
                    'symbol': symbol or 'UNKNOWN',
                    'qty': float(pos.get('quantity', 0)),
                    'avg_entry_price': float(pos.get('average_buy_price', 0)),
                    'current_price': float(quote.get('last_trade_price', 0)),
                    'market_value': float(pos.get('quantity', 0)) * float(quote.get('last_trade_price', 0)),
                    'unrealized_pl': float(pos.get('quantity', 0)) * (float(quote.get('last_trade_price', 0)) - float(pos.get('average_buy_price', 0))),
                    'unrealized_plpc': ((float(quote.get('last_trade_price', 0)) - float(pos.get('average_buy_price', 0))) / float(pos.get('average_buy_price', 0))) * 100 if pos.get('average_buy_price', 0) else 0
                })

            return result
        except Exception as e:
            logger.error(f"❌ Error getting positions: {e}")
            return []

    def get_orders(self, status: str = "open") -> List[Dict[str, Any]]:
        """Get orders by status"""
        if not self._connected:
            raise ConnectionError("Not connected to Robinhood API")

        try:
            if status == "open":
                orders = rh.get_all_open_stock_orders()
            else:
                orders = rh.get_all_stock_orders()

            result = []
            for order in orders:
                result.append({
                    'id': order.get('id', ''),
                    'symbol': order.get('symbol', ''),
                    'qty': float(order.get('quantity', 0)),
                    'side': order.get('side', ''),
                    'type': order.get('type', ''),
                    'status': order.get('state', ''),
                    'submitted_at': order.get('created_at', ''),
                    'filled_at': order.get('updated_at', ''),
                    'filled_qty': float(order.get('cumulative_quantity', 0)),
                    'filled_avg_price': float(order.get('average_price', 0)) if order.get('average_price') else None
                })

            return result
        except Exception as e:
            logger.error(f"❌ Error getting orders: {e}")
            return []

    def get_historical_data(
        self,
        symbol: str,
        timeframe: str = "1Min",
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        limit: int = 1000,
    ) -> pd.DataFrame:
        """Get historical market data"""
        if not self._connected:
            raise ConnectionError("Not connected to Robinhood API")

        try:
            # Convert timeframe to robin_stocks format
            # robin_stocks uses: '5minute', '10minute', 'hour', 'day', 'week'
            timeframe_map = {
                '1Min': '5minute',  # Closest available
                '5Min': '5minute',
                '15Min': '15minute',
                '1Hour': 'hour',
                '1Day': 'day',
            }
            rh_timeframe = timeframe_map.get(timeframe, '5minute')

            # Set default time range
            if end is None:
                end = datetime.now()
            if start is None:
                start = end - timedelta(days=30)

            # Get historical data
            historical_data = rh.get_stock_historicals(
                symbol,
                interval=rh_timeframe,
                span='year'  # robin_stocks span options
            )

            if not historical_data:
                return pd.DataFrame()

            # Convert to DataFrame
            df = pd.DataFrame(historical_data)
            if not df.empty:
                df['timestamp'] = pd.to_datetime(df['begins_at'])
                df = df.rename(columns={
                    'open_price': 'open',
                    'high_price': 'high',
                    'low_price': 'low',
                    'close_price': 'close',
                    'volume': 'volume'
                })
                df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
                df.set_index('timestamp', inplace=True)

            return df

        except Exception as e:
            logger.error(f"❌ Error getting historical data for {symbol}: {e}")
            return pd.DataFrame()

    def submit_market_order(
        self, symbol: str, qty: int, side: str, time_in_force: str = "gtc"
    ) -> Dict[str, Any]:
        """Submit a market order"""
        if not self._connected:
            raise ConnectionError("Not connected to Robinhood API")

        try:
            # robin_stocks order types
            order_type = "market"
            side_lower = side.lower()

            if side_lower == "buy":
                order = rh.order_buy_market(symbol, qty, timeInForce=time_in_force.upper())
            elif side_lower == "sell":
                order = rh.order_sell_market(symbol, qty, timeInForce=time_in_force.upper())
            else:
                raise ValueError(f"Invalid side: {side}")

            if order:
                logger.info(f"📋 Market order submitted: {side} {qty} {symbol}")
                return {
                    'id': order.get('id', ''),
                    'symbol': symbol,
                    'qty': qty,
                    'side': side,
                    'type': order_type,
                    'status': order.get('state', 'unknown')
                }
            else:
                raise Exception("Order submission returned None")

        except Exception as e:
            logger.error(f"❌ Error submitting market order for {symbol}: {e}")
            raise

    def submit_limit_order(
        self,
        symbol: str,
        qty: int,
        side: str,
        limit_price: float,
        time_in_force: str = "gtc",
    ) -> Dict[str, Any]:
        """Submit a limit order"""
        if not self._connected:
            raise ConnectionError("Not connected to Robinhood API")

        try:
            side_lower = side.lower()

            if side_lower == "buy":
                order = rh.order_buy_limit(symbol, qty, limit_price, timeInForce=time_in_force.upper())
            elif side_lower == "sell":
                order = rh.order_sell_limit(symbol, qty, limit_price, timeInForce=time_in_force.upper())
            else:
                raise ValueError(f"Invalid side: {side}")

            if order:
                logger.info(f"📋 Limit order submitted: {side} {qty} {symbol} @ {limit_price}")
                return {
                    'id': order.get('id', ''),
                    'symbol': symbol,
                    'qty': qty,
                    'side': side,
                    'type': 'limit',
                    'limit_price': limit_price,
                    'status': order.get('state', 'unknown')
                }
            else:
                raise Exception("Order submission returned None")

        except Exception as e:
            logger.error(f"❌ Error submitting limit order for {symbol}: {e}")
            raise

    def cancel_order(self, order_id: str) -> bool:
        """Cancel an order"""
        if not self._connected:
            raise ConnectionError("Not connected to Robinhood API")

        try:
            result = rh.cancel_stock_order(order_id)
            if result:
                logger.info(f"❌ Order cancelled: {order_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Error cancelling order {order_id}: {e}")
            return False

    def get_market_clock(self) -> Dict[str, Any]:
        """Get market clock information"""
        if not self._connected:
            raise ConnectionError("Not connected to Robinhood API")

        try:
            # robin_stocks doesn't have direct market clock, use market hours
            market_hours = rh.get_market_hours('NYSE')  # Default to NYSE
            
            return {
                'timestamp': datetime.now().isoformat(),
                'is_open': market_hours.get('is_open', False) if market_hours else False,
                'next_open': market_hours.get('opens_at', '') if market_hours else '',
                'next_close': market_hours.get('closes_at', '') if market_hours else ''
            }
        except Exception as e:
            logger.error(f"❌ Error getting market clock: {e}")
            return {
                'timestamp': datetime.now().isoformat(),
                'is_open': False,
                'next_open': '',
                'next_close': ''
            }

    def logout(self):
        """Logout from Robinhood"""
        if self._connected and ROBINHOOD_AVAILABLE:
            try:
                rh.logout()
                self._connected = False
                logger.info("✅ Logged out from Robinhood")
            except Exception as e:
                logger.error(f"❌ Error logging out: {e}")







