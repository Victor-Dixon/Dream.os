#!/usr/bin/env python3
"""
TradingEngineV2 - Advanced Trading Engine with Algorithm Optimization
=====================================================================

Advanced trading engine implementation with sophisticated algorithms,
risk management integration, and performance optimization.

Features:
- Multiple trading strategies (momentum, mean-reversion, arbitrage)
- Advanced risk management (VaR, CVaR, drawdown limits)
- Performance optimization (backtesting, parameter tuning)
- Real-time market data processing
- Portfolio optimization algorithms

Author: Agent-1 (Integration & Core Systems Specialist)
Created: 2026-01-06
Phase: Revenue Engine Phase 3 - Advanced Algorithms & Risk Management
"""

import asyncio
import logging
import numpy as np
import pandas as pd
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

from ..repositories.trading_repository import TradingRepository
from ..services.analytics.risk_analysis_engine import RiskAnalysisEngine
from ..services.analytics.performance_metrics_engine import PerformanceMetricsEngine
from .unified_event_system import EventPublisher


class TradingStrategy(Enum):
    """Available trading strategies."""
    MOMENTUM = "momentum"
    MEAN_REVERSION = "mean_reversion"
    ARBITRAGE = "arbitrage"
    PAIRS_TRADING = "pairs_trading"
    TREND_FOLLOWING = "trend_following"


class RiskManagementLevel(Enum):
    """Risk management strictness levels."""
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"


@dataclass
class TradingSignal:
    """Trading signal data structure."""
    symbol: str
    direction: str  # 'BUY', 'SELL', 'HOLD'
    strength: float  # 0.0 to 1.0
    confidence: float  # 0.0 to 1.0
    strategy: TradingStrategy
    timestamp: datetime
    price: float
    quantity: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None


@dataclass
class PortfolioPosition:
    """Portfolio position data."""
    symbol: str
    quantity: float
    avg_price: float
    current_price: float
    unrealized_pnl: float
    timestamp: datetime


class AdvancedTradingAlgorithm(ABC):
    """Base class for advanced trading algorithms."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = config.get('name', self.__class__.__name__)
        self.parameters = config.get('parameters', {})

    @abstractmethod
    def generate_signal(self, market_data: Dict[str, Any], portfolio: Dict[str, PortfolioPosition]) -> Optional[TradingSignal]:
        """Generate trading signal based on market data and portfolio state."""
        pass

    @abstractmethod
    def update_parameters(self, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update algorithm parameters based on performance data."""
        pass


class MomentumAlgorithm(AdvancedTradingAlgorithm):
    """Advanced momentum trading algorithm with multiple timeframes."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.lookback_periods = self.parameters.get('lookback_periods', [5, 10, 20])
        self.momentum_threshold = self.parameters.get('momentum_threshold', 0.02)
        self.volume_filter = self.parameters.get('volume_filter', True)

    def generate_signal(self, market_data: Dict[str, Any], portfolio: Dict[str, PortfolioPosition]) -> Optional[TradingSignal]:
        """Generate momentum-based trading signal."""
        symbol = market_data.get('symbol')
        if not symbol:
            return None

        prices = market_data.get('price_history', [])
        volumes = market_data.get('volume_history', [])

        if len(prices) < max(self.lookback_periods):
            return None

        # Calculate momentum across multiple timeframes
        momentum_scores = []
        for period in self.lookback_periods:
            if len(prices) >= period:
                recent_price = prices[-1]
                past_price = prices[-period]
                momentum = (recent_price - past_price) / past_price
                momentum_scores.append(momentum)

        avg_momentum = np.mean(momentum_scores)
        momentum_strength = abs(avg_momentum)

        # Volume confirmation
        if self.volume_filter and volumes:
            recent_volume = volumes[-1]
            avg_volume = np.mean(volumes[-10:]) if len(volumes) >= 10 else recent_volume
            volume_ratio = recent_volume / avg_volume if avg_volume > 0 else 1.0
        else:
            volume_ratio = 1.0

        # Generate signal
        if momentum_strength > self.momentum_threshold and volume_ratio > 0.8:
            direction = 'BUY' if avg_momentum > 0 else 'SELL'
            confidence = min(momentum_strength * volume_ratio, 1.0)

            return TradingSignal(
                symbol=symbol,
                direction=direction,
                strength=momentum_strength,
                confidence=confidence,
                strategy=TradingStrategy.MOMENTUM,
                timestamp=datetime.now(),
                price=prices[-1]
            )

        return None

    def update_parameters(self, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update momentum parameters based on performance."""
        win_rate = performance_data.get('win_rate', 0.5)
        avg_return = performance_data.get('avg_return', 0.0)

        # Adaptive parameter tuning
        if win_rate > 0.6 and avg_return > 0.01:
            # Increase sensitivity for good performance
            self.momentum_threshold *= 0.95
        elif win_rate < 0.4 or avg_return < -0.01:
            # Decrease sensitivity for poor performance
            self.momentum_threshold *= 1.05

        self.momentum_threshold = np.clip(self.momentum_threshold, 0.005, 0.1)

        return {
            'momentum_threshold': self.momentum_threshold,
            'lookback_periods': self.lookback_periods
        }


class MeanReversionAlgorithm(AdvancedTradingAlgorithm):
    """Advanced mean reversion algorithm with statistical testing."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.lookback_period = self.parameters.get('lookback_period', 20)
        self.std_dev_threshold = self.parameters.get('std_dev_threshold', 2.0)
        self.min_reversion_time = self.parameters.get('min_reversion_time', 5)

    def generate_signal(self, market_data: Dict[str, Any], portfolio: Dict[str, PortfolioPosition]) -> Optional[TradingSignal]:
        """Generate mean reversion trading signal."""
        symbol = market_data.get('symbol')
        if not symbol:
            return None

        prices = market_data.get('price_history', [])
        if len(prices) < self.lookback_period + self.min_reversion_time:
            return None

        # Calculate rolling mean and standard deviation
        prices_series = pd.Series(prices)
        rolling_mean = prices_series.rolling(window=self.lookback_period).mean()
        rolling_std = prices_series.rolling(window=self.lookback_period).std()

        current_price = prices[-1]
        current_mean = rolling_mean.iloc[-1]
        current_std = rolling_std.iloc[-1]

        if pd.isna(current_mean) or pd.isna(current_std) or current_std == 0:
            return None

        # Calculate z-score (standard deviations from mean)
        z_score = (current_price - current_mean) / current_std

        # Check for extreme deviation
        if abs(z_score) > self.std_dev_threshold:
            # Check if price has been deviating for minimum time
            recent_prices = prices[-self.min_reversion_time:]
            recent_z_scores = [(p - current_mean) / current_std for p in recent_prices]

            # All recent prices should be on the same side of mean
            consistent_direction = all(z > 0 for z in recent_z_scores) or all(z < 0 for z in recent_z_scores)

            if consistent_direction:
                direction = 'SELL' if z_score > 0 else 'BUY'
                confidence = min(abs(z_score) / (self.std_dev_threshold * 2), 1.0)

                return TradingSignal(
                    symbol=symbol,
                    direction=direction,
                    strength=abs(z_score),
                    confidence=confidence,
                    strategy=TradingStrategy.MEAN_REVERSION,
                    timestamp=datetime.now(),
                    price=current_price
                )

        return None

    def update_parameters(self, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update mean reversion parameters based on performance."""
        win_rate = performance_data.get('win_rate', 0.5)

        # Adaptive threshold tuning
        if win_rate > 0.65:
            self.std_dev_threshold *= 0.98  # More sensitive
        elif win_rate < 0.45:
            self.std_dev_threshold *= 1.02  # Less sensitive

        self.std_dev_threshold = np.clip(self.std_dev_threshold, 1.5, 3.5)

        return {
            'std_dev_threshold': self.std_dev_threshold,
            'lookback_period': self.lookback_period
        }


class RiskManager:
    """Advanced risk management system with multiple risk metrics."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.max_drawdown_limit = config.get('max_drawdown_limit', 0.1)
        self.max_position_size = config.get('max_position_size', 0.1)
        self.var_limit = config.get('var_limit', 0.05)
        self.stress_test_enabled = config.get('stress_test_enabled', True)

    def calculate_portfolio_risk(self, portfolio: Dict[str, PortfolioPosition],
                               market_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate comprehensive portfolio risk metrics."""
        if not portfolio:
            return {'total_risk': 0.0, 'var_95': 0.0, 'expected_shortfall': 0.0}

        # Calculate position values and weights
        total_value = sum(pos.quantity * pos.current_price for pos in portfolio.values())
        if total_value == 0:
            return {'total_risk': 0.0, 'var_95': 0.0, 'expected_shortfall': 0.0}

        # Simplified VaR calculation (historical simulation)
        returns = []
        for symbol, position in portfolio.items():
            price_history = market_data.get(symbol, {}).get('price_history', [])
            if len(price_history) > 1:
                symbol_returns = np.diff(price_history) / price_history[:-1]
                weight = (position.quantity * position.current_price) / total_value
                returns.append(symbol_returns * weight)

        if returns:
            portfolio_returns = np.sum(returns, axis=0)
            var_95 = np.percentile(portfolio_returns, 5)  # 95% VaR
            expected_shortfall = np.mean(portfolio_returns[portfolio_returns < var_95])
        else:
            var_95 = 0.0
            expected_shortfall = 0.0

        # Calculate maximum drawdown
        cumulative_returns = np.cumprod(1 + portfolio_returns)
        running_max = np.maximum.accumulate(cumulative_returns)
        drawdowns = (running_max - cumulative_returns) / running_max
        max_drawdown = np.max(drawdowns) if len(drawdowns) > 0 else 0.0

        return {
            'total_risk': abs(var_95),
            'var_95': var_95,
            'expected_shortfall': expected_shortfall,
            'max_drawdown': max_drawdown
        }

    def validate_trade_signal(self, signal: TradingSignal,
                            portfolio: Dict[str, PortfolioPosition],
                            risk_metrics: Dict[str, float]) -> Tuple[bool, str]:
        """Validate trading signal against risk limits."""

        # Check drawdown limit
        if risk_metrics.get('max_drawdown', 0) > self.max_drawdown_limit:
            return False, f"Portfolio drawdown {risk_metrics['max_drawdown']:.2%} exceeds limit {self.max_drawdown_limit:.2%}"

        # Check VaR limit
        if abs(risk_metrics.get('var_95', 0)) > self.var_limit:
            return False, f"Portfolio VaR {risk_metrics['var_95']:.2%} exceeds limit {self.var_limit:.2%}"

        # Check position size limit
        total_value = sum(pos.quantity * pos.current_price for pos in portfolio.values())
        if total_value > 0:
            position_value = signal.quantity * signal.price if signal.quantity else total_value * self.max_position_size
            position_pct = position_value / total_value

            if position_pct > self.max_position_size:
                return False, f"Position size {position_pct:.2%} exceeds limit {self.max_position_size:.2%}"

        return True, "Trade approved"

    def apply_stop_loss_take_profit(self, signal: TradingSignal) -> TradingSignal:
        """Apply stop loss and take profit levels based on risk parameters."""
        if signal.direction == 'BUY':
            stop_loss_pct = self.config.get('stop_loss_pct', 0.05)
            take_profit_pct = self.config.get('take_profit_pct', 0.10)

            signal.stop_loss = signal.price * (1 - stop_loss_pct)
            signal.take_profit = signal.price * (1 + take_profit_pct)

        elif signal.direction == 'SELL':
            stop_loss_pct = self.config.get('stop_loss_pct', 0.05)
            take_profit_pct = self.config.get('take_profit_pct', 0.10)

            signal.stop_loss = signal.price * (1 + stop_loss_pct)
            signal.take_profit = signal.price * (1 - take_profit_pct)

        return signal


class TradingEngineV2:
    """Advanced Trading Engine V2 with algorithm optimization and risk management."""

    def __init__(self, config: Dict[str, Any], repository: TradingRepository,
                 event_publisher: EventPublisher, risk_manager: RiskManager):
        self.config = config
        self.repository = repository
        self.event_publisher = event_publisher
        self.risk_manager = risk_manager

        # Initialize algorithms
        self.algorithms = self._initialize_algorithms()

        # Performance tracking
        self.performance_tracker = PerformanceMetricsEngine({})

        # Engine state
        self.is_running = False
        self.portfolio = {}
        self.active_strategies = set()

        # Logging
        self.logger = logging.getLogger(__name__)

    def _initialize_algorithms(self) -> Dict[str, AdvancedTradingAlgorithm]:
        """Initialize trading algorithms."""
        algorithms_config = self.config.get('algorithms', {})

        algorithms = {}
        for algo_name, algo_config in algorithms_config.items():
            if algo_name == 'momentum':
                algorithms[algo_name] = MomentumAlgorithm(algo_config)
            elif algo_name == 'mean_reversion':
                algorithms[algo_name] = MeanReversionAlgorithm(algo_config)

        return algorithms

    async def initialize(self, config: Dict[str, Any]) -> bool:
        """Initialize trading engine with configuration."""
        try:
            self.config.update(config)

            # Load existing portfolio
            self.portfolio = await self._load_portfolio()

            # Initialize algorithms with updated config
            self.algorithms = self._initialize_algorithms()

            self.event_publisher.publish('engine.initialized', {
                'timestamp': datetime.now(),
                'algorithms_loaded': len(self.algorithms),
                'portfolio_positions': len(self.portfolio)
            })

            self.logger.info(f"TradingEngineV2 initialized with {len(self.algorithms)} algorithms")
            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize TradingEngineV2: {e}")
            return False

    async def start(self) -> bool:
        """Start the trading engine."""
        try:
            self.is_running = True
            self.event_publisher.publish('engine.started', {
                'timestamp': datetime.now(),
                'status': 'active'
            })

            self.logger.info("TradingEngineV2 started")
            return True

        except Exception as e:
            self.logger.error(f"Failed to start TradingEngineV2: {e}")
            return False

    async def stop(self) -> bool:
        """Stop the trading engine gracefully."""
        try:
            self.is_running = False
            self.event_publisher.publish('engine.stopped', {
                'timestamp': datetime.now(),
                'status': 'stopped'
            })

            self.logger.info("TradingEngineV2 stopped")
            return True

        except Exception as e:
            self.logger.error(f"Failed to stop TradingEngineV2: {e}")
            return False

    async def process_market_data(self, market_data: Dict[str, Any]) -> List[TradingSignal]:
        """Process market data and generate trading signals."""
        if not self.is_running:
            return []

        signals = []

        # Calculate portfolio risk metrics
        risk_metrics = self.risk_manager.calculate_portfolio_risk(self.portfolio, market_data)

        # Generate signals from all algorithms
        for algo_name, algorithm in self.algorithms.items():
            try:
                signal = algorithm.generate_signal(market_data, self.portfolio)
                if signal:
                    # Validate signal against risk limits
                    is_valid, reason = self.risk_manager.validate_trade_signal(signal, self.portfolio, risk_metrics)

                    if is_valid:
                        # Apply stop loss and take profit
                        signal = self.risk_manager.apply_stop_loss_take_profit(signal)
                        signals.append(signal)

                        self.event_publisher.publish('signal.generated', {
                            'algorithm': algo_name,
                            'signal': signal.__dict__,
                            'risk_metrics': risk_metrics
                        })
                    else:
                        self.logger.warning(f"Signal rejected by risk manager: {reason}")

            except Exception as e:
                self.logger.error(f"Error in algorithm {algo_name}: {e}")

        return signals

    async def execute_signal(self, signal: TradingSignal) -> Optional[Dict[str, Any]]:
        """Execute a trading signal."""
        try:
            # Create trade record
            trade_data = {
                'symbol': signal.symbol,
                'direction': signal.direction,
                'quantity': signal.quantity or 100,  # Default quantity
                'price': signal.price,
                'timestamp': signal.timestamp,
                'strategy': signal.strategy.value,
                'stop_loss': signal.stop_loss,
                'take_profit': signal.take_profit
            }

            # Save trade to repository
            trade_id = await self.repository.save_trade(trade_data)

            # Update portfolio
            await self._update_portfolio(signal)

            # Publish trade execution event
            self.event_publisher.publish('trade.executed', {
                'trade_id': trade_id,
                'signal': signal.__dict__,
                'portfolio_value': self._calculate_portfolio_value()
            })

            self.logger.info(f"Executed trade: {signal.symbol} {signal.direction} at {signal.price}")
            return trade_data

        except Exception as e:
            self.logger.error(f"Failed to execute signal: {e}")
            return None

    def get_status(self) -> Dict[str, Any]:
        """Get current engine status."""
        return {
            'is_running': self.is_running,
            'algorithms_loaded': len(self.algorithms),
            'active_strategies': list(self.active_strategies),
            'portfolio_positions': len(self.portfolio),
            'portfolio_value': self._calculate_portfolio_value(),
            'timestamp': datetime.now()
        }

    async def optimize_algorithms(self) -> Dict[str, Any]:
        """Optimize algorithm parameters based on performance."""
        optimization_results = {}

        for algo_name, algorithm in self.algorithms.items():
            try:
                # Get performance data for this algorithm
                performance_data = await self._get_algorithm_performance(algo_name)

                # Update algorithm parameters
                new_params = algorithm.update_parameters(performance_data)

                optimization_results[algo_name] = {
                    'old_parameters': algorithm.parameters,
                    'new_parameters': new_params,
                    'performance_metrics': performance_data
                }

                self.logger.info(f"Optimized algorithm {algo_name}: {new_params}")

            except Exception as e:
                self.logger.error(f"Failed to optimize algorithm {algo_name}: {e}")

        return optimization_results

    async def _load_portfolio(self) -> Dict[str, PortfolioPosition]:
        """Load current portfolio from repository."""
        try:
            positions_data = await self.repository.get_all_positions()
            portfolio = {}

            for pos_data in positions_data:
                position = PortfolioPosition(
                    symbol=pos_data['symbol'],
                    quantity=pos_data['quantity'],
                    avg_price=pos_data['avg_price'],
                    current_price=pos_data['current_price'],
                    unrealized_pnl=pos_data['unrealized_pnl'],
                    timestamp=pos_data['timestamp']
                )
                portfolio[pos_data['symbol']] = position

            return portfolio

        except Exception as e:
            self.logger.error(f"Failed to load portfolio: {e}")
            return {}

    async def _update_portfolio(self, signal: TradingSignal) -> None:
        """Update portfolio after trade execution."""
        try:
            quantity = signal.quantity or 100

            if signal.symbol not in self.portfolio:
                self.portfolio[signal.symbol] = PortfolioPosition(
                    symbol=signal.symbol,
                    quantity=0,
                    avg_price=0,
                    current_price=signal.price,
                    unrealized_pnl=0,
                    timestamp=signal.timestamp
                )

            position = self.portfolio[signal.symbol]

            if signal.direction == 'BUY':
                # Calculate new average price
                total_value = position.quantity * position.avg_price + quantity * signal.price
                total_quantity = position.quantity + quantity
                new_avg_price = total_value / total_quantity if total_quantity > 0 else 0

                position.quantity = total_quantity
                position.avg_price = new_avg_price

            elif signal.direction == 'SELL':
                position.quantity -= quantity
                if position.quantity <= 0:
                    del self.portfolio[signal.symbol]
                    return

            position.current_price = signal.price
            position.unrealized_pnl = (position.current_price - position.avg_price) * position.quantity
            position.timestamp = signal.timestamp

        except Exception as e:
            self.logger.error(f"Failed to update portfolio: {e}")

    def _calculate_portfolio_value(self) -> float:
        """Calculate total portfolio value."""
        return sum(pos.quantity * pos.current_price for pos in self.portfolio.values())

    async def _get_algorithm_performance(self, algo_name: str) -> Dict[str, Any]:
        """Get performance metrics for a specific algorithm."""
        try:
            # Get trades for this algorithm
            trades = await self.repository.get_trades_by_strategy(algo_name)

            if not trades:
                return {'win_rate': 0.5, 'avg_return': 0.0, 'total_trades': 0}

            # Calculate basic performance metrics
            profitable_trades = sum(1 for trade in trades if trade.get('pnl', 0) > 0)
            win_rate = profitable_trades / len(trades)

            total_pnl = sum(trade.get('pnl', 0) for trade in trades)
            avg_return = total_pnl / len(trades) if trades else 0

            return {
                'win_rate': win_rate,
                'avg_return': avg_return,
                'total_trades': len(trades),
                'total_pnl': total_pnl
            }

        except Exception as e:
            self.logger.error(f"Failed to get algorithm performance: {e}")
            return {'win_rate': 0.5, 'avg_return': 0.0, 'total_trades': 0}