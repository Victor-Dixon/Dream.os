#!/usr/bin/env python3
"""
<!-- SSOT Domain: discord -->

Trading Data Service - Real Market Data Integration
====================================================

Service for fetching real market data from multiple sources:
- Alpaca API (primary)
- Yahoo Finance (fallback)
- Trading robot strategies integration

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-11-26
"""

import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional
import sys

# Add trading_robot to path
project_root = Path(__file__).resolve().parent.parent.parent
trading_robot_path = project_root / "trading_robot"
sys.path.insert(0, str(trading_robot_path))
sys.path.insert(0, str(project_root))

logger = logging.getLogger(__name__)

# Try to import market data sources
ALPACA_AVAILABLE = False
YFINANCE_AVAILABLE = False
TRADING_ROBOT_AVAILABLE = False

# Try yfinance first (most reliable fallback)
try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
    logger.info("✅ yfinance available")
except ImportError:
    logger.warning("⚠️ yfinance not available - install with: pip install yfinance")

# Try trading robot (may fail due to config issues)
try:
    from trading_robot.core.broker_factory import BrokerFactory
    from trading_robot.core.broker_interface import BrokerInterface
    from trading_robot.strategies.base_strategy import StrategyManager
    from trading_robot.strategies.strategy_implementations import TrendFollowingStrategy, MeanReversionStrategy
    TRADING_ROBOT_AVAILABLE = True
    logger.info("✅ Trading robot modules available")
except (ImportError, Exception) as e:
    logger.warning(f"⚠️ Trading robot not available (will use yfinance): {e}")
    BrokerFactory = None
    BrokerInterface = None
    StrategyManager = None
    TrendFollowingStrategy = None
    MeanReversionStrategy = None


class TradingDataService:
    """Service for fetching and analyzing real market data."""

    def __init__(self):
        self.broker_client: Optional[BrokerInterface] = None
        self.strategy_manager: Optional[StrategyManager] = None
        self._initialize_broker()

    def _initialize_broker(self):
        """Initialize broker client if available."""
        if not TRADING_ROBOT_AVAILABLE or BrokerFactory is None:
            logger.info("ℹ️ Trading robot not available, using yfinance only")
            return

        try:
            # Try to import config (may fail due to Pydantic validation)
            try:
                from trading_robot.config.settings import config as trading_config
            except Exception as e:
                logger.warning(f"⚠️ Trading robot config not available: {e}")
                return

            # Try to create broker client
            broker_factory = BrokerFactory()
            self.broker_client = broker_factory.create_broker(trading_config.broker)
            
            # Try to connect (may fail if credentials not configured)
            try:
                self.broker_client.connect()
                logger.info("✅ Connected to broker API")
            except Exception as e:
                logger.warning(f"⚠️ Broker connection failed (will use yfinance): {e}")
                self.broker_client = None

            # Initialize strategy manager (if available)
            if StrategyManager and TrendFollowingStrategy and MeanReversionStrategy:
                try:
                    self.strategy_manager = StrategyManager()
                    self.strategy_manager.add_strategy(TrendFollowingStrategy())
                    self.strategy_manager.add_strategy(MeanReversionStrategy())
                    logger.info("✅ Strategy manager initialized")
                except Exception as e:
                    logger.warning(f"⚠️ Strategy manager initialization failed: {e}")

        except Exception as e:
            logger.warning(f"⚠️ Could not initialize broker (will use yfinance): {e}")

    def get_market_data(self, symbol: str, period: str = "1d", interval: str = "1m") -> Optional[Any]:
        """Get market data for a symbol from available sources."""
        # Try Alpaca first
        if self.broker_client and self.broker_client.is_connected():
            try:
                data = self.broker_client.get_historical_data(
                    symbol=symbol,
                    timeframe=interval,
                    limit=100
                )
                if not data.empty:
                    return data
            except Exception as e:
                logger.warning(f"⚠️ Alpaca data fetch failed for {symbol}: {e}")

        # Fallback to yfinance
        if YFINANCE_AVAILABLE:
            try:
                ticker = yf.Ticker(symbol)
                data = ticker.history(period=period, interval=interval)
                if not data.empty:
                    # Rename columns to match expected format
                    data.columns = [col.lower() for col in data.columns]
                    return data
            except Exception as e:
                logger.warning(f"⚠️ yfinance data fetch failed for {symbol}: {e}")

        return None

    def get_current_price(self, symbol: str) -> Optional[float]:
        """Get current price for a symbol."""
        data = self.get_market_data(symbol, period="1d", interval="1m")
        if data is not None and not data.empty:
            if hasattr(data, 'close'):
                return float(data['close'].iloc[-1])
            elif 'Close' in data.columns:
                return float(data['Close'].iloc[-1])
        return None

    def analyze_symbol(self, symbol: str) -> Dict[str, Any]:
        """Analyze symbol using trading robot strategies."""
        data = self.get_market_data(symbol, period="5d", interval="1h")
        
        if data is None or data.empty:
            return {
                "symbol": symbol,
                "signal": "UNKNOWN",
                "confidence": 0.0,
                "reason": "No market data available",
                "price": None,
                "indicators": {}
            }

        # Get current price
        current_price = self.get_current_price(symbol)
        
        # Analyze with strategies if available
        if self.strategy_manager and TRADING_ROBOT_AVAILABLE:
            try:
                results = self.strategy_manager.analyze_symbol(symbol, data)
                
                # Get consensus signal
                if results:
                    buy_signals = sum(1 for r in results if r.signal.name == "BUY")
                    sell_signals = sum(1 for r in results if r.signal.name == "SELL")
                    avg_confidence = sum(r.confidence for r in results) / len(results) if results else 0.0
                    
                    if buy_signals > sell_signals:
                        signal = "CALL" if symbol == "TSLA" else "LONG"
                        reason = f"{buy_signals} strategies bullish"
                    elif sell_signals > buy_signals:
                        signal = "PUT" if symbol == "TSLA" else "SHORT"
                        reason = f"{sell_signals} strategies bearish"
                    else:
                        signal = "HOLD"
                        reason = "Mixed signals"
                    
                    return {
                        "symbol": symbol,
                        "signal": signal,
                        "confidence": avg_confidence,
                        "reason": reason,
                        "price": current_price,
                        "indicators": self._calculate_indicators(data),
                        "strategy_results": len(results)
                    }
            except Exception as e:
                logger.warning(f"⚠️ Strategy analysis failed for {symbol}: {e}")

        # Fallback: Simple analysis
        return {
            "symbol": symbol,
            "signal": "UNKNOWN",
            "confidence": 0.5,
            "reason": "Basic analysis (strategies not available)",
            "price": current_price,
            "indicators": self._calculate_indicators(data) if data is not None else {}
        }

    def _calculate_indicators(self, data: Any) -> Dict[str, float]:
        """Calculate technical indicators."""
        indicators = {}
        
        if data is None or data.empty:
            return indicators

        try:
            close_prices = data['close'] if 'close' in data.columns else data['Close']
            
            # Simple moving averages
            if len(close_prices) >= 20:
                indicators['sma_20'] = float(close_prices.tail(20).mean())
            if len(close_prices) >= 50:
                indicators['sma_50'] = float(close_prices.tail(50).mean())
            
            # Current price
            indicators['current'] = float(close_prices.iloc[-1])
            
            # Price change
            if len(close_prices) >= 2:
                change = close_prices.iloc[-1] - close_prices.iloc[-2]
                change_pct = (change / close_prices.iloc[-2]) * 100
                indicators['change'] = float(change)
                indicators['change_pct'] = float(change_pct)
            
        except Exception as e:
            logger.warning(f"⚠️ Indicator calculation failed: {e}")

        return indicators

    def get_market_conditions(self) -> Dict[str, Any]:
        """Get current market conditions."""
        conditions = {
            "market_status": "UNKNOWN",
            "vix": None,
            "spy_trend": "UNKNOWN",
            "sector_rotation": "UNKNOWN",
            "risk_level": "MODERATE"
        }

        # Try to get SPY data for market trend
        spy_data = self.get_market_data("SPY", period="5d", interval="1d")
        if spy_data is not None and not spy_data.empty:
            try:
                close_prices = spy_data['close'] if 'close' in spy_data.columns else spy_data['Close']
                if len(close_prices) >= 2:
                    current = close_prices.iloc[-1]
                    previous = close_prices.iloc[-2]
                    conditions['spy_trend'] = "BULLISH" if current > previous else "BEARISH"
            except:
                pass

        # Try to get VIX
        vix_data = self.get_market_data("^VIX", period="1d", interval="1d")
        if vix_data is not None and not vix_data.empty:
            try:
                close_prices = vix_data['close'] if 'close' in vix_data.columns else vix_data['Close']
                conditions['vix'] = f"{close_prices.iloc[-1]:.2f}"
            except:
                pass

        # Market status
        now = datetime.now()
        if now.weekday() < 5 and 9 <= now.hour < 16:  # Weekday, 9 AM - 4 PM
            conditions['market_status'] = "OPEN"
        else:
            conditions['market_status'] = "CLOSED"

        return conditions

