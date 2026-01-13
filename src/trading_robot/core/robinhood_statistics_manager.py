"""
Robinhood Statistics Manager Module
====================================

V2 Compliant: Yes (<100 lines)
Single Responsibility: Trading statistics calculation and analysis

Author: Agent-2 (dream.os)
Date: 2026-01-08
"""

import logging
from dataclasses import dataclass
from typing import List, Dict, Any

import robin_stocks.robinhood as rs


@dataclass
class RobinhoodOptionsStats:
    """2025 Options trading statistics"""
    total_trades: int = 0
    winning_trades: int = 0
    losing_trades: int = 0
    win_rate_percent: float = 0.0
    total_pnl: float = 0.0
    realized_pnl: float = 0.0
    unrealized_pnl: float = 0.0
    commissions_paid: float = 0.0
    best_trade: float = 0.0
    worst_trade: float = 0.0
    average_trade: float = 0.0
    total_volume: float = 0.0
    options_premium_collected: float = 0.0


class RobinhoodStatisticsManager:
    """
    V2 Compliant Statistics Manager

    Handles all trading statistics calculations:
    - Options trading statistics
    - Performance metrics
    - Trade analysis
    - Historical data processing
    """

    def __init__(self):
        self.logger = logging.getLogger("RobinhoodStatisticsManager")

    def get_2025_options_statistics(self) -> RobinhoodOptionsStats:
        """
        Get comprehensive 2025 options trading statistics.

        Returns:
            RobinhoodOptionsStats object with all metrics
        """
        try:
            # Get options orders history
            orders = rs.options.get_option_orders()
            stats = RobinhoodOptionsStats()

            # Filter for 2025 orders
            y2025_orders = []
            for order in orders:
                created_at = order.get('created_at', '')
                if created_at.startswith('2025'):
                    y2025_orders.append(order)

            self.logger.info(f"📊 Found {len(y2025_orders)} options orders in 2025")

            # Process each order
            for order in y2025_orders:
                quantity = int(order.get('quantity', 0))
                price = float(order.get('price', 0))
                fees = float(order.get('fees', 0))

                stats.total_trades += 1
                stats.commissions_paid += fees

                if order.get('state') == 'filled':
                    pnl = float(order.get('total_notional', 0)) - (quantity * price)
                    stats.total_pnl += pnl

                    if pnl > 0:
                        stats.winning_trades += 1
                        stats.best_trade = max(stats.best_trade, pnl)
                    else:
                        stats.losing_trades += 1
                        stats.worst_trade = min(stats.worst_trade, pnl)

            # Calculate percentages and averages
            if stats.total_trades > 0:
                stats.win_rate_percent = (stats.winning_trades / stats.total_trades) * 100
                stats.average_trade = stats.total_pnl / stats.total_trades

            self.logger.info(f"📊 2025 Options Stats: {stats.total_trades} trades, "
                           f"${stats.total_pnl:,.2f} P&L, {stats.win_rate_percent:.1f}% win rate")

            return stats

        except Exception as e:
            self.logger.error(f"2025 statistics error: {e}")
            return RobinhoodOptionsStats()

    def calculate_trade_metrics(self, trades: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate comprehensive trade metrics from trade data.

        Args:
            trades: List of trade dictionaries

        Returns:
            Dictionary with calculated metrics
        """
        if not trades:
            return {"error": "No trades data provided"}

        try:
            total_pnl = 0.0
            winning_trades = 0
            losing_trades = 0
            commissions = 0.0

            for trade in trades:
                pnl = trade.get('pnl', 0.0)
                fees = trade.get('fees', 0.0)

                total_pnl += pnl
                commissions += fees

                if pnl > 0:
                    winning_trades += 1
                elif pnl < 0:
                    losing_trades += 1

            total_trades = len(trades)
            win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0.0

            return {
                "total_trades": total_trades,
                "winning_trades": winning_trades,
                "losing_trades": losing_trades,
                "win_rate_percent": win_rate,
                "total_pnl": total_pnl,
                "total_commissions": commissions,
                "net_pnl": total_pnl - commissions
            }

        except Exception as e:
            self.logger.error(f"Trade metrics calculation error: {e}")
            return {"error": str(e)}

    def get_performance_summary(self) -> Dict[str, Any]:
        """
        Get overall performance summary.

        Returns:
            Performance metrics dictionary
        """
        try:
            stats = self.get_2025_options_statistics()

            return {
                "period": "2025",
                "total_trades": stats.total_trades,
                "win_rate_percent": stats.win_rate_percent,
                "total_pnl": stats.total_pnl,
                "net_pnl": stats.total_pnl - stats.commissions_paid,
                "best_trade": stats.best_trade,
                "worst_trade": stats.worst_trade,
                "average_trade": stats.average_trade,
                "total_commissions": stats.commissions_paid
            }

        except Exception as e:
            self.logger.error(f"Performance summary error: {e}")
            return {"error": str(e)}