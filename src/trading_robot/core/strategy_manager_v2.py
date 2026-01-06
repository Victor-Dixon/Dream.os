#!/usr/bin/env python3
"""
StrategyManagerV2 - Advanced Strategy Management System
=======================================================

Advanced strategy management with dynamic loading, optimization,
and risk-aware strategy selection.

Features:
- Dynamic strategy loading and unloading
- Strategy performance optimization
- Risk-adjusted strategy allocation
- Multi-timeframe strategy coordination
- Strategy correlation analysis

Author: Agent-1 (Integration & Core Systems Specialist)
Created: 2026-01-06
Phase: Revenue Engine Phase 3 - Advanced Strategy Management
"""

import asyncio
import logging
import importlib
import inspect
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Type
from datetime import datetime, timedelta
from dataclasses import dataclass
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from .unified_event_system import EventPublisher
from .trading_engine_v2 import TradingSignal, TradingStrategy


@dataclass
class StrategyMetadata:
    """Strategy metadata information."""
    name: str
    version: str
    author: str
    description: str
    strategy_type: TradingStrategy
    parameters: Dict[str, Any]
    risk_level: str  # 'low', 'medium', 'high'
    timeframe: str   # 'short', 'medium', 'long'
    created: datetime
    last_modified: datetime


@dataclass
class StrategyPerformance:
    """Strategy performance metrics."""
    strategy_name: str
    total_trades: int
    win_rate: float
    avg_return: float
    max_drawdown: float
    sharpe_ratio: float
    sortino_ratio: float
    calmar_ratio: float
    alpha: float
    beta: float
    last_updated: datetime


class BaseStrategy(ABC):
    """Base strategy class for all trading strategies."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = config.get('name', self.__class__.__name__)
        self.is_active = False
        self.performance = StrategyPerformance(
            strategy_name=self.name,
            total_trades=0,
            win_rate=0.0,
            avg_return=0.0,
            max_drawdown=0.0,
            sharpe_ratio=0.0,
            sortino_ratio=0.0,
            calmar_ratio=0.0,
            alpha=0.0,
            beta=0.0,
            last_updated=datetime.now()
        )

    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the strategy."""
        pass

    @abstractmethod
    def generate_signal(self, market_data: Dict[str, Any]) -> Optional[TradingSignal]:
        """Generate trading signal based on market data."""
        pass

    @abstractmethod
    def update_performance(self, trade_result: Dict[str, Any]) -> None:
        """Update strategy performance based on trade results."""
        pass

    def get_metadata(self) -> StrategyMetadata:
        """Get strategy metadata."""
        return StrategyMetadata(
            name=self.name,
            version=getattr(self, '__version__', '1.0.0'),
            author=getattr(self, '__author__', 'Unknown'),
            description=getattr(self, '__doc__', '').strip().split('\n')[0] if getattr(self, '__doc__', '') else '',
            strategy_type=getattr(self, 'STRATEGY_TYPE', TradingStrategy.MOMENTUM),
            parameters=self.config,
            risk_level=getattr(self, 'RISK_LEVEL', 'medium'),
            timeframe=getattr(self, 'TIMEFRAME', 'medium'),
            created=getattr(self, 'CREATED_DATE', datetime.now()),
            last_modified=datetime.now()
        )

    def get_performance(self) -> StrategyPerformance:
        """Get current performance metrics."""
        return self.performance


class StrategyLoader:
    """Dynamic strategy loading and management."""

    def __init__(self, strategies_path: str = "src/trading_robot/strategies"):
        self.strategies_path = Path(strategies_path)
        self.loaded_strategies: Dict[str, Type[BaseStrategy]] = {}
        self.executor = ThreadPoolExecutor(max_workers=4)

    def discover_strategies(self) -> List[str]:
        """Discover available strategy files."""
        strategy_files = []

        if self.strategies_path.exists():
            for file_path in self.strategies_path.rglob("*.py"):
                if not file_path.name.startswith("__"):
                    strategy_files.append(str(file_path.relative_to(self.strategies_path)))

        return strategy_files

    def load_strategy_class(self, strategy_file: str) -> Optional[Type[BaseStrategy]]:
        """Load strategy class from file."""
        try:
            # Convert file path to module path
            module_path = strategy_file.replace('.py', '').replace('/', '.').replace('\\', '.')

            # Import the module
            full_module_path = f"src.trading_robot.strategies.{module_path}"
            module = importlib.import_module(full_module_path)

            # Find strategy classes
            for name, obj in inspect.getmembers(module):
                if (inspect.isclass(obj) and
                    issubclass(obj, BaseStrategy) and
                    obj != BaseStrategy):
                    return obj

        except Exception as e:
            logging.error(f"Failed to load strategy {strategy_file}: {e}")

        return None

    def load_all_strategies(self) -> Dict[str, Type[BaseStrategy]]:
        """Load all available strategies."""
        strategy_files = self.discover_strategies()
        loaded_strategies = {}

        for strategy_file in strategy_files:
            strategy_class = self.load_strategy_class(strategy_file)
            if strategy_class:
                strategy_name = strategy_class.__name__
                loaded_strategies[strategy_name] = strategy_class
                self.loaded_strategies[strategy_name] = strategy_class

        logging.info(f"Loaded {len(loaded_strategies)} strategies")
        return loaded_strategies


class RiskAdjustedAllocator:
    """Risk-adjusted strategy allocation optimizer."""

    def __init__(self, risk_tolerance: float = 0.1):
        self.risk_tolerance = risk_tolerance

    def optimize_allocation(self, strategies: Dict[str, StrategyPerformance],
                          total_capital: float) -> Dict[str, float]:
        """Optimize capital allocation across strategies using risk-adjusted metrics."""

        if not strategies:
            return {}

        # Calculate risk-adjusted returns for each strategy
        strategy_scores = {}
        for name, perf in strategies.items():
            if perf.total_trades > 10:  # Minimum sample size
                # Use Sharpe ratio as primary metric, with win rate as tiebreaker
                score = perf.sharpe_ratio * (1 + perf.win_rate)
                strategy_scores[name] = score
            else:
                strategy_scores[name] = 0.0  # Not enough data

        # Normalize scores
        if strategy_scores:
            max_score = max(strategy_scores.values())
            min_score = min(strategy_scores.values())

            if max_score > min_score:
                for name in strategy_scores:
                    strategy_scores[name] = (strategy_scores[name] - min_score) / (max_score - min_score)

        # Allocate capital based on scores
        total_score = sum(strategy_scores.values())
        allocations = {}

        if total_score > 0:
            for name, score in strategy_scores.items():
                allocation_pct = score / total_score
                # Apply risk tolerance constraint
                allocation_pct = min(allocation_pct, self.risk_tolerance)
                allocations[name] = allocation_pct * total_capital

        return allocations


class StrategyCorrelator:
    """Strategy correlation analysis for diversification."""

    def __init__(self):
        self.correlation_window = 50  # trades

    def calculate_correlations(self, strategy_returns: Dict[str, List[float]]) -> Dict[str, Dict[str, float]]:
        """Calculate correlation matrix between strategies."""
        correlations = {}

        strategy_names = list(strategy_returns.keys())

        for i, strategy_a in enumerate(strategy_names):
            correlations[strategy_a] = {}

            for j, strategy_b in enumerate(strategy_names):
                if i == j:
                    correlations[strategy_a][strategy_b] = 1.0
                else:
                    returns_a = strategy_returns[strategy_a][-self.correlation_window:]
                    returns_b = strategy_returns[strategy_b][-self.correlation_window:]

                    if len(returns_a) == len(returns_b) and len(returns_a) > 10:
                        try:
                            corr = self._calculate_correlation(returns_a, returns_b)
                            correlations[strategy_a][strategy_b] = corr
                        except:
                            correlations[strategy_a][strategy_b] = 0.0
                    else:
                        correlations[strategy_a][strategy_b] = 0.0

        return correlations

    def _calculate_correlation(self, returns_a: List[float], returns_b: List[float]) -> float:
        """Calculate Pearson correlation coefficient."""
        n = len(returns_a)
        if n != len(returns_b):
            return 0.0

        mean_a = sum(returns_a) / n
        mean_b = sum(returns_b) / n

        numerator = sum((returns_a[i] - mean_a) * (returns_b[i] - mean_b) for i in range(n))
        denominator_a = sum((r - mean_a) ** 2 for r in returns_a)
        denominator_b = sum((r - mean_b) ** 2 for r in returns_b)

        if denominator_a == 0 or denominator_b == 0:
            return 0.0

        return numerator / (denominator_a ** 0.5 * denominator_b ** 0.5)


class StrategyManagerV2:
    """Advanced Strategy Manager V2 with optimization and risk management."""

    def __init__(self, config: Dict[str, Any], event_publisher: EventPublisher):
        self.config = config
        self.event_publisher = event_publisher

        # Core components
        self.strategy_loader = StrategyLoader()
        self.risk_allocator = RiskAdjustedAllocator(
            risk_tolerance=config.get('risk_tolerance', 0.1)
        )
        self.correlator = StrategyCorrelator()

        # Strategy management
        self.loaded_strategies: Dict[str, BaseStrategy] = {}
        self.active_strategies: Dict[str, BaseStrategy] = {}
        self.strategy_performance: Dict[str, StrategyPerformance] = {}
        self.strategy_allocations: Dict[str, float] = {}

        # Configuration
        self.max_active_strategies = config.get('max_active_strategies', 5)
        self.rebalance_frequency = config.get('rebalance_frequency', 24)  # hours

        # Logging
        self.logger = logging.getLogger(__name__)

    async def initialize(self) -> bool:
        """Initialize strategy manager."""
        try:
            # Load available strategies
            available_strategies = self.strategy_loader.load_all_strategies()

            self.event_publisher.publish('strategy_manager.initialized', {
                'available_strategies': len(available_strategies),
                'timestamp': datetime.now()
            })

            self.logger.info(f"StrategyManagerV2 initialized with {len(available_strategies)} available strategies")
            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize StrategyManagerV2: {e}")
            return False

    async def load_strategy(self, strategy_name: str, config: Dict[str, Any]) -> bool:
        """Load a strategy by name."""
        try:
            if strategy_name in self.loaded_strategies:
                self.logger.warning(f"Strategy {strategy_name} already loaded")
                return True

            strategy_class = self.strategy_loader.loaded_strategies.get(strategy_name)
            if not strategy_class:
                self.logger.error(f"Strategy {strategy_name} not found")
                return False

            # Instantiate strategy
            strategy = strategy_class(config)

            # Initialize strategy
            if not strategy.initialize():
                self.logger.error(f"Failed to initialize strategy {strategy_name}")
                return False

            self.loaded_strategies[strategy_name] = strategy
            self.strategy_performance[strategy_name] = strategy.get_performance()

            self.event_publisher.publish('strategy.loaded', {
                'strategy_name': strategy_name,
                'metadata': strategy.get_metadata().__dict__,
                'timestamp': datetime.now()
            })

            self.logger.info(f"Loaded strategy: {strategy_name}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to load strategy {strategy_name}: {e}")
            return False

    async def unload_strategy(self, strategy_name: str) -> bool:
        """Unload a strategy."""
        try:
            if strategy_name not in self.loaded_strategies:
                self.logger.warning(f"Strategy {strategy_name} not loaded")
                return True

            # Deactivate if active
            if strategy_name in self.active_strategies:
                await self.deactivate_strategy(strategy_name)

            # Remove from loaded strategies
            del self.loaded_strategies[strategy_name]

            self.event_publisher.publish('strategy.unloaded', {
                'strategy_name': strategy_name,
                'timestamp': datetime.now()
            })

            self.logger.info(f"Unloaded strategy: {strategy_name}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to unload strategy {strategy_name}: {e}")
            return False

    async def activate_strategy(self, strategy_name: str) -> bool:
        """Activate a loaded strategy."""
        try:
            if strategy_name not in self.loaded_strategies:
                self.logger.error(f"Strategy {strategy_name} not loaded")
                return False

            if strategy_name in self.active_strategies:
                self.logger.warning(f"Strategy {strategy_name} already active")
                return True

            if len(self.active_strategies) >= self.max_active_strategies:
                # Deactivate worst performing strategy
                worst_strategy = self._find_worst_performing_strategy()
                if worst_strategy:
                    await self.deactivate_strategy(worst_strategy)

            strategy = self.loaded_strategies[strategy_name]
            strategy.is_active = True
            self.active_strategies[strategy_name] = strategy

            self.event_publisher.publish('strategy.activated', {
                'strategy_name': strategy_name,
                'active_strategies': len(self.active_strategies),
                'timestamp': datetime.now()
            })

            self.logger.info(f"Activated strategy: {strategy_name}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to activate strategy {strategy_name}: {e}")
            return False

    async def deactivate_strategy(self, strategy_name: str) -> bool:
        """Deactivate an active strategy."""
        try:
            if strategy_name not in self.active_strategies:
                self.logger.warning(f"Strategy {strategy_name} not active")
                return True

            strategy = self.active_strategies[strategy_name]
            strategy.is_active = False
            del self.active_strategies[strategy_name]

            self.event_publisher.publish('strategy.deactivated', {
                'strategy_name': strategy_name,
                'active_strategies': len(self.active_strategies),
                'timestamp': datetime.now()
            })

            self.logger.info(f"Deactivated strategy: {strategy_name}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to deactivate strategy {strategy_name}: {e}")
            return False

    async def get_strategy(self, strategy_name: str) -> Optional[BaseStrategy]:
        """Get a loaded strategy instance."""
        return self.loaded_strategies.get(strategy_name)

    async def list_strategies(self) -> List[Dict[str, Any]]:
        """List all loaded strategies with their status."""
        strategies = []

        for name, strategy in self.loaded_strategies.items():
            strategy_info = {
                'name': name,
                'is_active': name in self.active_strategies,
                'metadata': strategy.get_metadata().__dict__,
                'performance': strategy.get_performance().__dict__
            }
            strategies.append(strategy_info)

        return strategies

    async def optimize_strategies(self) -> Dict[str, Any]:
        """Optimize strategy portfolio and allocations."""
        try:
            # Update strategy allocations based on performance
            self.strategy_allocations = self.risk_allocator.optimize_allocation(
                self.strategy_performance,
                total_capital=100000  # This should come from config
            )

            # Calculate strategy correlations
            strategy_returns = await self._get_strategy_returns()
            correlations = self.correlator.calculate_correlations(strategy_returns)

            optimization_result = {
                'allocations': self.strategy_allocations,
                'correlations': correlations,
                'active_strategies': len(self.active_strategies),
                'total_strategies': len(self.loaded_strategies),
                'timestamp': datetime.now()
            }

            self.event_publisher.publish('strategies.optimized', optimization_result)

            self.logger.info("Strategy optimization completed")
            return optimization_result

        except Exception as e:
            self.logger.error(f"Failed to optimize strategies: {e}")
            return {}

    async def update_strategy_performance(self, strategy_name: str, trade_result: Dict[str, Any]) -> None:
        """Update performance metrics for a strategy."""
        try:
            if strategy_name in self.loaded_strategies:
                strategy = self.loaded_strategies[strategy_name]
                strategy.update_performance(trade_result)

                # Update our performance tracking
                self.strategy_performance[strategy_name] = strategy.get_performance()

        except Exception as e:
            self.logger.error(f"Failed to update strategy performance: {e}")

    def validate_strategy_config(self, config: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate strategy configuration."""
        errors = []

        # Check required fields
        required_fields = ['name', 'parameters']
        for field in required_fields:
            if field not in config:
                errors.append(f"Missing required field: {field}")

        # Validate parameter types
        parameters = config.get('parameters', {})
        if not isinstance(parameters, dict):
            errors.append("Parameters must be a dictionary")

        return len(errors) == 0, errors

    async def generate_signals(self, market_data: Dict[str, Any]) -> List[TradingSignal]:
        """Generate trading signals from all active strategies."""
        signals = []

        for strategy_name, strategy in self.active_strategies.items():
            try:
                signal = strategy.generate_signal(market_data)
                if signal:
                    signals.append(signal)

                    self.event_publisher.publish('strategy.signal_generated', {
                        'strategy_name': strategy_name,
                        'signal': signal.__dict__,
                        'timestamp': datetime.now()
                    })

            except Exception as e:
                self.logger.error(f"Error generating signal from {strategy_name}: {e}")

        return signals

    def _find_worst_performing_strategy(self) -> Optional[str]:
        """Find the worst performing active strategy."""
        if not self.active_strategies:
            return None

        worst_strategy = None
        worst_score = float('inf')

        for name in self.active_strategies:
            perf = self.strategy_performance.get(name)
            if perf:
                # Simple score: lower is better (higher risk, lower returns)
                score = (1 - perf.win_rate) + abs(perf.max_drawdown)
                if score < worst_score:
                    worst_score = score
                    worst_strategy = name

        return worst_strategy

    async def _get_strategy_returns(self) -> Dict[str, List[float]]:
        """Get return series for correlation analysis."""
        # This would typically query the repository for historical returns
        # For now, return empty dict
        return {}