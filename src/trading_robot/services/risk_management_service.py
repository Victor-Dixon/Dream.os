#!/usr/bin/env python3
"""
Risk Management Service - Prevent Account Blowups
================================================

<!-- SSOT Domain: trading_robot -->

Enterprise-grade risk management to prevent automated trading disasters.
Implements multiple layers of protection learned from previous account losses.

Features:
- Daily loss limits with automatic shutdown
- Position size controls (percentage of portfolio)
- Trade frequency limits
- Emergency stop mechanisms
- Conservative strategy enforcement
- Account protection rules

Author: Agent-2 (Architecture & Design Specialist)
Mission: Prevent automated trading blowups through intelligent risk controls
"""

import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum

from ..core.broker_factory import BrokerFactory

logger = logging.getLogger(__name__)


class RiskLevel(Enum):
    """Risk tolerance levels."""
    ULTRA_CONSERVATIVE = "ultra_conservative"  # 0.5% daily loss, 2% position max
    CONSERVATIVE = "conservative"              # 1% daily loss, 5% position max
    MODERATE = "moderate"                      # 2% daily loss, 10% position max
    AGGRESSIVE = "aggressive"                  # 5% daily loss, 20% position max


@dataclass
class RiskLimits:
    """Comprehensive risk management limits."""
    daily_loss_limit_pct: float = 1.0      # Max % loss per day
    max_position_size_pct: float = 5.0     # Max % of portfolio per position
    max_portfolio_concentration: float = 20.0  # Max % in single symbol
    max_daily_trades: int = 5              # Max trades per day
    max_trade_frequency: int = 300         # Min seconds between trades
    min_order_value: float = 10.0          # Min dollar amount per trade
    max_order_value: float = 1000.0        # Max dollar amount per trade
    emergency_stop_loss_pct: float = 2.0   # Emergency stop trigger
    require_stop_loss: bool = True         # Enforce stop losses
    max_open_positions: int = 3            # Max concurrent positions


class RiskManagementService:
    """
    Enterprise Risk Management Service

    Prevents account blowups through comprehensive risk controls.
    Multiple protection layers with automatic emergency responses.
    """

    def __init__(self, risk_level: RiskLevel = RiskLevel.CONSERVATIVE):
        """
        Initialize risk management service.

        Args:
            risk_level: Base risk tolerance level
        """
        self.risk_level = risk_level
        self.risk_limits = self._get_risk_limits_for_level(risk_level)

        # Trading state tracking
        self.daily_start_value: Optional[float] = None
        self.daily_trades: List[Dict[str, Any]] = []
        self.open_positions: Dict[str, Dict[str, Any]] = {}
        self.last_trade_time: Optional[float] = None

        # Emergency controls
        self.emergency_stop_triggered = False
        self.circuit_breaker_tripped = False

        # Broker connection for real-time data
        self.broker = None

        logger.info(f"🛡️ Risk Management Service initialized: {risk_level.value}")
        logger.info(f"📊 Daily loss limit: {self.risk_limits.daily_loss_limit_pct}%")
        logger.info(f"📊 Max position size: {self.risk_limits.max_position_size_pct}%")

    def connect_broker(self, broker_type: str = "robinhood", **credentials):
        """Connect to broker for real-time risk monitoring."""
        self.broker = BrokerFactory.create_broker(broker_type, **credentials)
        if self.broker and self.broker.connect():
            logger.info("✅ Risk management connected to broker")
            return True
        else:
            logger.error("❌ Risk management failed to connect to broker")
            return False

    def _get_risk_limits_for_level(self, level: RiskLevel) -> RiskLimits:
        """Get risk limits based on risk tolerance level."""
        base_limits = RiskLimits()

        if level == RiskLevel.ULTRA_CONSERVATIVE:
            base_limits.daily_loss_limit_pct = 0.5
            base_limits.max_position_size_pct = 2.0
            base_limits.max_daily_trades = 3
            base_limits.max_trade_frequency = 600  # 10 minutes
            base_limits.max_open_positions = 2

        elif level == RiskLevel.CONSERVATIVE:
            base_limits.daily_loss_limit_pct = 1.0
            base_limits.max_position_size_pct = 5.0
            base_limits.max_daily_trades = 5
            base_limits.max_trade_frequency = 300  # 5 minutes
            base_limits.max_open_positions = 3

        elif level == RiskLevel.MODERATE:
            base_limits.daily_loss_limit_pct = 2.0
            base_limits.max_position_size_pct = 10.0
            base_limits.max_daily_trades = 8
            base_limits.max_trade_frequency = 180  # 3 minutes
            base_limits.max_open_positions = 5

        elif level == RiskLevel.AGGRESSIVE:
            base_limits.daily_loss_limit_pct = 5.0
            base_limits.max_position_size_pct = 20.0
            base_limits.max_daily_trades = 12
            base_limits.max_trade_frequency = 120  # 2 minutes
            base_limits.max_open_positions = 7

        return base_limits

    def start_trading_day(self):
        """Initialize daily trading session with baseline values."""
        try:
            if not self.broker:
                logger.error("No broker connected for daily start")
                return False

            account_info = self.broker.get_account_info()
            if 'balance' in account_info:
                self.daily_start_value = account_info['balance'] + account_info.get('margin', 0)
                self.daily_trades = []
                self.emergency_stop_triggered = False
                self.circuit_breaker_tripped = False

                logger.info(f"📅 Trading day started - Portfolio value: ${self.daily_start_value:.2f}")
                logger.info(f"🛡️ Daily loss limit: ${self.daily_start_value * self.risk_limits.daily_loss_limit_pct / 100:.2f}")
                return True
            else:
                logger.error("Failed to get account info for daily start")
                return False

        except Exception as e:
            logger.error(f"Failed to start trading day: {e}")
            return False

    def validate_trade(self, symbol: str, quantity: int, price: float,
                      order_type: str, **kwargs) -> Dict[str, Any]:
        """
        Comprehensive trade validation against all risk rules.

        Args:
            symbol: Trading symbol
            quantity: Number of shares/contracts
            price: Trade price
            order_type: Type of order (market, limit, etc.)
            **kwargs: Additional trade parameters

        Returns:
            Validation result with approval status and reasons
        """
        violations = []
        warnings = []

        # Check emergency stop
        if self.emergency_stop_triggered:
            return {
                "approved": False,
                "reason": "Emergency stop is active",
                "violations": ["emergency_stop"],
                "action_required": "Manual reset required"
            }

        # 1. Daily Loss Limit Check
        daily_loss_check = self._check_daily_loss_limit()
        if not daily_loss_check['approved']:
            violations.append("daily_loss_limit_exceeded")
            if daily_loss_check.get('emergency_stop', False):
                self.emergency_stop_triggered = True

        # 2. Daily Trade Frequency Check
        trade_freq_check = self._check_trade_frequency()
        if not trade_freq_check['approved']:
            violations.append("trade_frequency_violation")

        # 3. Daily Trade Count Check
        trade_count_check = self._check_daily_trade_count()
        if not trade_count_check['approved']:
            violations.append("daily_trade_limit_exceeded")

        # 4. Position Size Validation
        position_check = self._validate_position_size(symbol, quantity, price)
        if not position_check['approved']:
            violations.append("position_size_violation")

        # 5. Order Value Limits
        order_value = abs(quantity * price)
        if order_value < self.risk_limits.min_order_value:
            violations.append("order_value_too_small")
        elif order_value > self.risk_limits.max_order_value:
            violations.append("order_value_too_large")

        # 6. Open Positions Limit
        open_pos_check = self._check_open_positions_limit(symbol)
        if not open_pos_check['approved']:
            violations.append("open_positions_limit_exceeded")

        # 7. Stop Loss Requirement
        if self.risk_limits.require_stop_loss and 'stop_loss' not in kwargs:
            violations.append("stop_loss_required")

        # 8. Market Hours (basic check)
        market_check = self._check_market_hours()
        if not market_check['approved']:
            violations.append("market_hours_violation")

        # Determine overall approval
        approved = len(violations) == 0

        result = {
            "approved": approved,
            "violations": violations,
            "warnings": warnings,
            "risk_level": self.risk_level.value,
            "checks_performed": [
                "daily_loss_limit",
                "trade_frequency",
                "daily_trade_count",
                "position_size",
                "order_value",
                "open_positions",
                "stop_loss",
                "market_hours"
            ]
        }

        if approved:
            logger.info(f"✅ Trade validated: {symbol} {quantity}@{price} ({order_type})")
        else:
            logger.warning(f"🚫 Trade rejected: {symbol} - Violations: {violations}")

        return result

    def _check_daily_loss_limit(self) -> Dict[str, Any]:
        """Check if daily loss limit has been exceeded."""
        if not self.daily_start_value:
            return {"approved": False, "reason": "No daily start value set"}

        try:
            # Get current portfolio value
            account_info = self.broker.get_account_info()
            current_value = account_info.get('balance', 0) + account_info.get('margin', 0)

            # Calculate daily P&L
            daily_pnl = current_value - self.daily_start_value
            daily_pnl_pct = (daily_pnl / self.daily_start_value) * 100

            # Check against limit
            loss_limit = -abs(self.risk_limits.daily_loss_limit_pct)
            emergency_limit = -abs(self.risk_limits.emergency_stop_loss_pct)

            if daily_pnl_pct <= emergency_limit:
                # Emergency stop triggered
                return {
                    "approved": False,
                    "reason": f"Emergency stop: {daily_pnl_pct:.2f}% loss (limit: {emergency_limit:.2f}%)",
                    "current_loss_pct": daily_pnl_pct,
                    "emergency_stop": True
                }
            elif daily_pnl_pct <= loss_limit:
                # Trading limit exceeded but not emergency
                return {
                    "approved": False,
                    "reason": f"Daily loss limit exceeded: {daily_pnl_pct:.2f}% (limit: {loss_limit:.2f}%)",
                    "current_loss_pct": daily_pnl_pct
                }
            else:
                return {
                    "approved": True,
                    "current_pnl_pct": daily_pnl_pct
                }

        except Exception as e:
            logger.error(f"Daily loss check failed: {e}")
            return {"approved": False, "reason": f"Check failed: {e}"}

    def _check_trade_frequency(self) -> Dict[str, Any]:
        """Check time since last trade."""
        if not self.last_trade_time:
            return {"approved": True}

        time_since_last_trade = time.time() - self.last_trade_time
        min_interval = self.risk_limits.max_trade_frequency

        if time_since_last_trade < min_interval:
            remaining_time = min_interval - time_since_last_trade
            return {
                "approved": False,
                "reason": f"Trade too frequent. Wait {remaining_time:.0f} seconds",
                "remaining_time": remaining_time
            }

        return {"approved": True}

    def _check_daily_trade_count(self) -> Dict[str, Any]:
        """Check daily trade count limit."""
        if len(self.daily_trades) >= self.risk_limits.max_daily_trades:
            return {
                "approved": False,
                "reason": f"Daily trade limit reached: {len(self.daily_trades)}/{self.risk_limits.max_daily_trades}",
                "trades_today": len(self.daily_trades)
            }

        return {"approved": True, "trades_today": len(self.daily_trades)}

    def _validate_position_size(self, symbol: str, quantity: int, price: float) -> Dict[str, Any]:
        """Validate position size against portfolio limits."""
        try:
            if not self.daily_start_value:
                return {"approved": False, "reason": "No portfolio value available"}

            order_value = abs(quantity * price)
            position_pct = (order_value / self.daily_start_value) * 100

            if position_pct > self.risk_limits.max_position_size_pct:
                return {
                    "approved": False,
                    "reason": f"Position size {position_pct:.2f}% exceeds limit {self.risk_limits.max_position_size_pct:.2f}%",
                    "position_pct": position_pct
                }

            # Check existing position concentration
            if symbol in self.open_positions:
                existing_value = self.open_positions[symbol].get('value', 0)
                total_position_value = existing_value + order_value
                concentration_pct = (total_position_value / self.daily_start_value) * 100

                if concentration_pct > self.risk_limits.max_portfolio_concentration:
                    return {
                        "approved": False,
                        "reason": f"Symbol concentration {concentration_pct:.2f}% exceeds limit {self.risk_limits.max_portfolio_concentration:.2f}%",
                        "concentration_pct": concentration_pct
                    }

            return {"approved": True, "position_pct": position_pct}

        except Exception as e:
            logger.error(f"Position size validation failed: {e}")
            return {"approved": False, "reason": f"Validation error: {e}"}

    def _check_open_positions_limit(self, symbol: str) -> Dict[str, Any]:
        """Check if opening this position would exceed limits."""
        current_positions = len(self.open_positions)

        # If symbol not already in positions, check if we can add one
        if symbol not in self.open_positions:
            if current_positions >= self.risk_limits.max_open_positions:
                return {
                    "approved": False,
                    "reason": f"Maximum open positions reached: {current_positions}/{self.risk_limits.max_open_positions}",
                    "current_positions": current_positions
                }

        return {"approved": True, "current_positions": current_positions}

    def _check_market_hours(self) -> Dict[str, Any]:
        """Basic market hours check (simplified)."""
        # IMPLEMENT: Real market hours checking
        # For now, assume trading is allowed during business hours
        now = datetime.now()

        # US Market hours: 9:30 AM - 4:00 PM ET on weekdays
        if now.weekday() >= 5:  # Saturday/Sunday
            return {"approved": False, "reason": "Markets closed on weekends"}

        market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
        market_close = now.replace(hour=16, minute=0, second=0, microsecond=0)

        if not (market_open <= now <= market_close):
            return {"approved": False, "reason": "Outside market hours"}

        return {"approved": True}

    def record_trade(self, trade_data: Dict[str, Any]):
        """Record a completed trade for risk tracking."""
        self.daily_trades.append(trade_data)
        self.last_trade_time = time.time()

        # Update position tracking
        symbol = trade_data.get('symbol')
        if symbol:
            if symbol not in self.open_positions:
                self.open_positions[symbol] = {
                    'quantity': 0,
                    'value': 0,
                    'trades': []
                }

            # Update position (simplified)
            quantity = trade_data.get('quantity', 0)
            price = trade_data.get('price', 0)

            self.open_positions[symbol]['quantity'] += quantity
            self.open_positions[symbol]['value'] += (quantity * price)
            self.open_positions[symbol]['trades'].append(trade_data)

        logger.info(f"📊 Trade recorded: {trade_data}")

    def get_risk_status(self) -> Dict[str, Any]:
        """Get comprehensive risk status."""
        return {
            "risk_level": self.risk_level.value,
            "daily_start_value": self.daily_start_value,
            "daily_trades": len(self.daily_trades),
            "open_positions": len(self.open_positions),
            "emergency_stop": self.emergency_stop_triggered,
            "circuit_breaker": self.circuit_breaker_tripped,
            "limits": {
                "daily_loss_limit_pct": self.risk_limits.daily_loss_limit_pct,
                "max_position_size_pct": self.risk_limits.max_position_size_pct,
                "max_daily_trades": self.risk_limits.max_daily_trades,
                "max_open_positions": self.risk_limits.max_open_positions
            }
        }

    def emergency_stop(self):
        """Trigger emergency stop - halt all trading."""
        logger.critical("🚨 EMERGENCY STOP ACTIVATED - All trading halted")
        self.emergency_stop_triggered = True

        # Close all positions (in real implementation)
        # Cancel pending orders
        # Send alerts

    def reset_emergency_stop(self):
        """Manually reset emergency stop (requires human confirmation)."""
        logger.warning("🔄 Emergency stop manually reset")
        self.emergency_stop_triggered = False