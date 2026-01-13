"""
Robinhood Balance Manager Module
=================================

V2 Compliant: Yes (<100 lines)
Single Responsibility: Account balance and portfolio data retrieval

Author: Agent-2 (dream.os)
Date: 2026-01-08
"""

import logging
from datetime import datetime
from typing import Dict, Any

import robin_stocks.robinhood as rs


class RobinhoodBalanceManager:
    """
    V2 Compliant Balance Manager

    Handles all account balance and portfolio data operations:
    - Unified balance retrieval
    - Account information aggregation
    - Portfolio value calculations
    - Position summaries
    """

    def __init__(self, daily_start_balance: float = 0.0):
        self.logger = logging.getLogger("RobinhoodBalanceManager")
        self.daily_start_balance = daily_start_balance

    def get_unified_balance_data(self) -> Dict[str, Any]:
        """
        UNIFIED BALANCE RETRIEVAL - Single source of truth for all balance data.

        Returns:
            Comprehensive, standardized balance data dictionary
        """
        try:
            # Get account profile (comprehensive data)
            account_info = rs.account.build_user_profile()
            if not account_info:
                return {"error": "Cannot retrieve account information"}

            # Get detailed account data
            account_details = rs.account.get_account()
            if not account_details:
                return {"error": "Cannot retrieve account details"}

            # Get positions for portfolio calculations
            positions = rs.account.get_all_positions()
            total_positions_value = 0.0
            if positions:
                for position in positions:
                    quantity = float(position.get('quantity', 0))
                    average_price = float(position.get('average_buy_price', 0))
                    total_positions_value += quantity * average_price

            # Build comprehensive unified balance data
            balance_data = {
                # Core balances
                "cash": float(account_details.get('cash', 0)),
                "portfolio_value": float(account_info.get('portfolio_value', 0)),
                "buying_power": float(account_info.get('buying_power', 0)),
                "total_positions_value": total_positions_value,

                # Extended account info
                "equity": float(account_info.get('equity', 0)),
                "margin": float(account_details.get('margin_balances', {}).get('margin_limit', 0)),
                "market_value": float(account_info.get('market_value', 0)),
                "withdrawable_amount": float(account_details.get('withdrawable_amount', 0)),

                # Account metadata
                "account_number": account_details.get('account_number', 'N/A'),
                "account_type": account_details.get('type', 'individual'),
                "status": "active" if account_details.get('active', False) else "inactive",
                "currency": "USD",

                # Performance tracking
                "day_change": 0.0,
                "day_change_percent": 0.0,

                # Metadata
                "retrieved_at": datetime.now().isoformat(),
                "data_source": "robinhood_api_real",
                "consolidated": True
            }

            # Calculate day change if we have baseline
            if self.daily_start_balance > 0:
                balance_data["day_change"] = balance_data["portfolio_value"] - self.daily_start_balance
                balance_data["day_change_percent"] = (
                    balance_data["day_change"] / self.daily_start_balance) * 100

            self.logger.info(".2f")
            return balance_data

        except Exception as e:
            self.logger.error(f"UNIFIED Balance retrieval error: {e}")
            return {"error": str(e)}

    def get_balance(self) -> Dict[str, Any]:
        """Get comprehensive account balance."""
        return self.get_unified_balance_data()

    def get_account_info(self) -> Dict[str, Any]:
        """Get account information in legacy format for backward compatibility."""
        balance_data = self.get_balance()
        if "error" in balance_data:
            return balance_data

        return {
            "balance": balance_data.get("cash", 0),
            "margin": balance_data.get("margin", 0),
            "buying_power": balance_data.get("buying_power", 0),
            "equity": balance_data.get("equity", balance_data.get("portfolio_value", 0)),
            "market_value": balance_data.get("market_value", balance_data.get("portfolio_value", 0)),
            "account_type": balance_data.get("account_type", "robinhood_real"),
            "status": balance_data.get("status", "active"),
            "currency": balance_data.get("currency", "USD")
        }

    def get_portfolio_summary(self) -> Dict[str, Any]:
        """Get high-level portfolio summary."""
        balance = self.get_balance()
        if "error" in balance:
            return balance

        return {
            "total_value": balance.get("portfolio_value", 0),
            "cash": balance.get("cash", 0),
            "positions_value": balance.get("total_positions_value", 0),
            "buying_power": balance.get("buying_power", 0),
            "day_change": balance.get("day_change", 0),
            "day_change_percent": balance.get("day_change_percent", 0)
        }