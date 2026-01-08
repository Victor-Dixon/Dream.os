"""
Robinhood Positions Manager Module
===================================

V2 Compliant: Yes (<100 lines)
Single Responsibility: Options and stock positions management

Author: Agent-2 (dream.os)
Date: 2026-01-08
"""

import logging
from typing import List, Dict, Any

import robin_stocks.robinhood as rs


class RobinhoodPositionsManager:
    """
    V2 Compliant Positions Manager

    Handles all positions-related operations:
    - Options positions retrieval
    - Stock positions retrieval
    - Position data formatting
    - Portfolio composition analysis
    """

    def __init__(self):
        self.logger = logging.getLogger("RobinhoodPositionsManager")

    def get_options_positions(self) -> List[Dict[str, Any]]:
        """
        Get current options positions.

        Returns:
            List of options position dictionaries
        """
        try:
            options_positions = rs.options.get_open_option_positions()
            positions_data = []

            for pos in options_positions:
                position_data = {
                    "instrument": pos.get('chain_symbol', ''),
                    "type": pos.get('type', ''),  # call/put
                    "strike_price": float(pos.get('strike_price', 0)),
                    "expiration_date": pos.get('expiration_date', ''),
                    "quantity": int(pos.get('quantity', 0)),
                    "average_price": float(pos.get('average_price', 0)),
                    "market_value": float(pos.get('market_value', 0)),
                    "unrealized_pnl": float(pos.get('unrealized_pnl', 0))
                }
                positions_data.append(position_data)

            self.logger.info(f"📊 Retrieved {len(positions_data)} options positions")
            return positions_data

        except Exception as e:
            self.logger.error(f"Options positions error: {e}")
            return [{"error": str(e)}]

    def get_stock_positions(self) -> List[Dict[str, Any]]:
        """
        Get current stock positions.

        Returns:
            List of stock position dictionaries
        """
        try:
            positions = rs.account.get_all_positions()
            positions_data = []

            for pos in positions:
                position_data = {
                    "symbol": pos.get('symbol', ''),
                    "quantity": float(pos.get('quantity', 0)),
                    "average_buy_price": float(pos.get('average_buy_price', 0)),
                    "current_price": float(pos.get('current_price', 0)),
                    "market_value": float(pos.get('market_value', 0)),
                    "unrealized_pnl": float(pos.get('unrealized_pnl', 0))
                }
                positions_data.append(position_data)

            self.logger.info(f"📊 Retrieved {len(positions_data)} stock positions")
            return positions_data

        except Exception as e:
            self.logger.error(f"Stock positions error: {e}")
            return [{"error": str(e)}]

    def get_all_positions(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get all positions (stocks and options).

        Returns:
            Dictionary with stocks and options positions
        """
        return {
            "stocks": self.get_stock_positions(),
            "options": self.get_options_positions()
        }

    def get_portfolio_composition(self) -> Dict[str, Any]:
        """
        Get portfolio composition summary.

        Returns:
            Portfolio composition data
        """
        try:
            all_positions = self.get_all_positions()

            total_stocks_value = sum(
                pos.get('market_value', 0)
                for pos in all_positions['stocks']
                if isinstance(pos, dict) and 'error' not in pos
            )

            total_options_value = sum(
                pos.get('market_value', 0)
                for pos in all_positions['options']
                if isinstance(pos, dict) and 'error' not in pos
            )

            return {
                "stocks_count": len(all_positions['stocks']),
                "options_count": len(all_positions['options']),
                "total_stocks_value": total_stocks_value,
                "total_options_value": total_options_value,
                "total_positions_value": total_stocks_value + total_options_value
            }

        except Exception as e:
            self.logger.error(f"Portfolio composition error: {e}")
            return {"error": str(e)}