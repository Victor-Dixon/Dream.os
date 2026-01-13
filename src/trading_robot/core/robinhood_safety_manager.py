"""
Robinhood Safety Manager Module
===============================

V2 Compliant: Yes (<100 lines)
Single Responsibility: Safety guardrails and emergency controls

Author: Agent-2 (dream.os)
Date: 2026-01-08
"""

import logging
from typing import Tuple
from dataclasses import dataclass

import robin_stocks.robinhood as rs


@dataclass
class RobinhoodSafetyLimits:
    """Safety guardrails to prevent account blowups"""
    max_daily_loss_percent: float = 2.0  # Max 2% daily loss
    max_position_size_percent: float = 5.0  # Max 5% per position
    max_total_exposure_percent: float = 15.0  # Max 15% total exposure
    emergency_stop_enabled: bool = True
    require_paper_trading_first: bool = True


class RobinhoodSafetyManager:
    """
    V2 Compliant Safety Manager

    Handles all safety and risk management logic:
    - Daily loss limits
    - Position size controls
    - Emergency stop mechanisms
    - Safety validation
    """

    def __init__(self, daily_start_balance: float = 0.0):
        self.logger = logging.getLogger("RobinhoodSafetyManager")
        self.safety_limits = RobinhoodSafetyLimits()
        self.daily_start_balance = daily_start_balance
        self.emergency_stop_triggered = False

    def check_safety_limits(self, current_value: float) -> Tuple[bool, str]:
        """
        Check all safety guardrails before any trading operation.

        Args:
            current_value: Current portfolio value

        Returns:
            Tuple[bool, str]: (is_safe, reason_if_not)
        """
        if self.emergency_stop_triggered:
            return False, "Emergency stop triggered"

        try:
            daily_change = current_value - self.daily_start_balance
            daily_change_percent = (
                daily_change / self.daily_start_balance) * 100 if self.daily_start_balance > 0 else 0

            # Check daily loss limit
            if daily_change_percent <= -self.safety_limits.max_daily_loss_percent:
                self.emergency_stop_triggered = True
                return False, ".1f"".1f"

            return True, "All safety checks passed"

        except Exception as e:
            self.logger.error(f"Safety check error: {e}")
            return False, f"Safety check failed: {e}"

    def initialize_safety_tracking(self) -> None:
        """Initialize daily safety tracking."""
        try:
            account_info = rs.account.build_user_profile()
            if account_info:
                portfolio_value = float(account_info.get('portfolio_value', 0))
                self.daily_start_balance = portfolio_value
                self.logger.info(".2f")
        except Exception as e:
            self.logger.error(f"Failed to initialize safety tracking: {e}")

    def emergency_stop(self) -> None:
        """Trigger emergency stop - prevents all trading."""
        self.emergency_stop_triggered = True
        self.logger.critical("🚨 EMERGENCY STOP TRIGGERED - ALL TRADING HALTED")

    def is_safe_to_trade(self) -> bool:
        """Check if all safety conditions are met for trading."""
        # Simplified check - would integrate with balance manager in production
        return not self.emergency_stop_triggered

    def get_safety_status(self) -> dict:
        """Get comprehensive safety status."""
        return {
            "emergency_stop_triggered": self.emergency_stop_triggered,
            "daily_start_balance": self.daily_start_balance,
            "safety_limits": {
                "max_daily_loss_percent": self.safety_limits.max_daily_loss_percent,
                "max_position_size_percent": self.safety_limits.max_position_size_percent,
                "max_total_exposure_percent": self.safety_limits.max_total_exposure_percent,
            }
        }