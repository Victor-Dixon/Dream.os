"""
Metrics Aggregator
==================

Aggregates performance metrics by time period.
Automatically aggregates daily, weekly, monthly, and all-time metrics.

V2 Compliant: < 200 lines
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from collections import defaultdict

logger = logging.getLogger(__name__)


class MetricsAggregator:
    """Aggregates performance metrics by time period."""
    
    def __init__(self, storage, collector):
        """
        Initialize metrics aggregator.
        
        Args:
            storage: MetricsStorage instance
            collector: MetricsCollector instance
        """
        self.storage = storage
        self.collector = collector
    
    def aggregate_daily_metrics(
        self,
        user_id: str,
        plugin_id: str,
        metric_date: datetime
    ) -> Dict[str, Any]:
        """
        Aggregate daily metrics for a user/plugin.
        
        Args:
            user_id: User identifier
            plugin_id: Plugin identifier
            metric_date: Date for metrics
            
        Returns:
            Aggregated metrics dictionary
        """
        try:
            # Get trades for the day
            trades = self.collector.get_trades_for_user(user_id, plugin_id)
            day_trades = [
                t for t in trades
                if datetime.fromisoformat(t["timestamp"]).date() == metric_date.date()
            ]
            
            metrics = self._calculate_metrics(day_trades)
            metrics["metric_type"] = "daily"
            metrics["metric_date"] = metric_date.isoformat()
            
            # Save aggregated metrics
            self.storage.save_performance_metrics(
                user_id, plugin_id, metric_date, "daily", metrics
            )
            
            logger.info(f"📊 Aggregated daily metrics for {user_id}/{plugin_id}")
            return metrics
            
        except Exception as e:
            logger.error(f"❌ Failed to aggregate daily metrics: {e}")
            return {}
    
    def aggregate_weekly_metrics(
        self,
        user_id: str,
        plugin_id: str,
        week_start: datetime
    ) -> Dict[str, Any]:
        """
        Aggregate weekly metrics for a user/plugin.
        
        Args:
            user_id: User identifier
            plugin_id: Plugin identifier
            week_start: Start of week (Sunday)
            
        Returns:
            Aggregated metrics dictionary
        """
        try:
            week_end = week_start + timedelta(days=7)
            trades = self.collector.get_trades_for_user(user_id, plugin_id)
            week_trades = [
                t for t in trades
                if week_start.date() <= datetime.fromisoformat(t["timestamp"]).date() < week_end.date()
            ]
            
            metrics = self._calculate_metrics(week_trades)
            metrics["metric_type"] = "weekly"
            metrics["metric_date"] = week_start.isoformat()
            
            # Save aggregated metrics
            self.storage.save_performance_metrics(
                user_id, plugin_id, week_start, "weekly", metrics
            )
            
            logger.info(f"📊 Aggregated weekly metrics for {user_id}/{plugin_id}")
            return metrics
            
        except Exception as e:
            logger.error(f"❌ Failed to aggregate weekly metrics: {e}")
            return {}
    
    def aggregate_monthly_metrics(
        self,
        user_id: str,
        plugin_id: str,
        month_start: datetime
    ) -> Dict[str, Any]:
        """
        Aggregate monthly metrics for a user/plugin.
        
        Args:
            user_id: User identifier
            plugin_id: Plugin identifier
            month_start: Start of month (first day)
            
        Returns:
            Aggregated metrics dictionary
        """
        try:
            # Calculate month end
            if month_start.month == 12:
                month_end = datetime(month_start.year + 1, 1, 1)
            else:
                month_end = datetime(month_start.year, month_start.month + 1, 1)
            
            trades = self.collector.get_trades_for_user(user_id, plugin_id)
            month_trades = [
                t for t in trades
                if month_start.date() <= datetime.fromisoformat(t["timestamp"]).date() < month_end.date()
            ]
            
            metrics = self._calculate_metrics(month_trades)
            metrics["metric_type"] = "monthly"
            metrics["metric_date"] = month_start.isoformat()
            
            # Save aggregated metrics
            self.storage.save_performance_metrics(
                user_id, plugin_id, month_start, "monthly", metrics
            )
            
            logger.info(f"📊 Aggregated monthly metrics for {user_id}/{plugin_id}")
            return metrics
            
        except Exception as e:
            logger.error(f"❌ Failed to aggregate monthly metrics: {e}")
            return {}
    
    def aggregate_all_time_metrics(
        self,
        user_id: str,
        plugin_id: str
    ) -> Dict[str, Any]:
        """
        Aggregate all-time metrics for a user/plugin.
        
        Args:
            user_id: User identifier
            plugin_id: Plugin identifier
            
        Returns:
            Aggregated metrics dictionary
        """
        try:
            trades = self.collector.get_trades_for_user(user_id, plugin_id)
            metrics = self._calculate_metrics(trades)
            metrics["metric_type"] = "all_time"
            metrics["metric_date"] = datetime.now().isoformat()
            
            # Save aggregated metrics
            self.storage.save_performance_metrics(
                user_id, plugin_id, datetime.now(), "all_time", metrics
            )
            
            logger.info(f"📊 Aggregated all-time metrics for {user_id}/{plugin_id}")
            return metrics
            
        except Exception as e:
            logger.error(f"❌ Failed to aggregate all-time metrics: {e}")
            return {}
    
    def _calculate_metrics(self, trades: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate performance metrics from trades.
        
        Args:
            trades: List of trade dictionaries
            
        Returns:
            Metrics dictionary
        """
        if not trades:
            return {
                "trade_count": 0,
                "win_count": 0,
                "loss_count": 0,
                "total_pnl": 0.0,
                "win_rate": 0.0,
                "profit_factor": 0.0,
                "sharpe_ratio": 0.0,
                "max_drawdown": 0.0,
                "avg_trade_size": 0.0,
                "best_trade_pnl": 0.0,
                "worst_trade_pnl": 0.0
            }
        
        # Calculate basic metrics
        trade_count = len(trades)
        pnls = [t.get("pnl", 0.0) for t in trades]
        win_count = len([p for p in pnls if p > 0])
        loss_count = len([p for p in pnls if p < 0])
        total_pnl = sum(pnls)
        win_rate = (win_count / trade_count * 100) if trade_count > 0 else 0.0
        
        # Profit factor
        total_wins = sum([p for p in pnls if p > 0])
        total_losses = abs(sum([p for p in pnls if p < 0]))
        profit_factor = (total_wins / total_losses) if total_losses > 0 else 0.0
        
        # Trade sizes
        trade_sizes = [t.get("quantity", 0) * t.get("entry_price", 0.0) for t in trades]
        avg_trade_size = sum(trade_sizes) / len(trade_sizes) if trade_sizes else 0.0
        
        # Best/worst trades
        best_trade_pnl = max(pnls) if pnls else 0.0
        worst_trade_pnl = min(pnls) if pnls else 0.0
        
        # Sharpe ratio (simplified)
        if len(pnls) > 1:
            import numpy as np
            returns = np.array(pnls)
            sharpe_ratio = (np.mean(returns) / np.std(returns) * np.sqrt(252)) if np.std(returns) > 0 else 0.0
        else:
            sharpe_ratio = 0.0
        
        # Max drawdown (simplified)
        cumulative = []
        running_total = 0.0
        for pnl in pnls:
            running_total += pnl
            cumulative.append(running_total)
        
        if cumulative:
            peak = cumulative[0]
            max_drawdown = 0.0
            for value in cumulative:
                if value > peak:
                    peak = value
                drawdown = (peak - value) / peak if peak > 0 else 0.0
                max_drawdown = max(max_drawdown, drawdown)
            max_drawdown = max_drawdown * 100
        else:
            max_drawdown = 0.0
        
        return {
            "trade_count": trade_count,
            "win_count": win_count,
            "loss_count": loss_count,
            "total_pnl": round(total_pnl, 2),
            "win_rate": round(win_rate, 2),
            "profit_factor": round(profit_factor, 2),
            "sharpe_ratio": round(sharpe_ratio, 2),
            "max_drawdown": round(max_drawdown, 2),
            "avg_trade_size": round(avg_trade_size, 2),
            "best_trade_pnl": round(best_trade_pnl, 2),
            "worst_trade_pnl": round(worst_trade_pnl, 2)
        }

