"""
Performance Tracker
===================

Main performance tracking plugin.
Orchestrates metrics collection, storage, and aggregation.

V2 Compliant: < 200 lines
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

from plugins.plugin_base import PluginBase
from plugins.plugin_metadata import PluginMetadata
from .metrics_collector import MetricsCollector
from .metrics_storage import MetricsStorage
from .metrics_aggregator import MetricsAggregator

logger = logging.getLogger(__name__)


class PerformanceTracker(PluginBase):
    """Main performance tracking plugin."""
    
    def __init__(self, metadata: PluginMetadata, parameters: Dict[str, Any] = None):
        """Initialize performance tracker."""
        super().__init__(metadata, parameters)
        
        # Initialize components
        self.storage = MetricsStorage()
        self.collector = MetricsCollector(self.storage)
        self.aggregator = MetricsAggregator(self.storage, self.collector)
        
        # Initialize storage
        self.storage.initialize()
    
    def analyze(self, data, symbol: str):
        """Performance tracker doesn't generate trading signals."""
        from strategies.signal_processing import Signal, StrategyResult
        return StrategyResult(symbol, Signal.HOLD, 0.0)
    
    def calculate_entry_quantity(self, account_balance: float, price: float, stop_loss_price: float) -> int:
        """Performance tracker doesn't calculate position sizes."""
        return 0
    
    def calculate_stop_loss(self, entry_price: float, is_long: bool) -> float:
        """Performance tracker doesn't calculate stop loss."""
        return entry_price
    
    def calculate_profit_target(self, entry_price: float, is_long: bool) -> float:
        """Performance tracker doesn't calculate profit target."""
        return entry_price
    
    def capture_trade(
        self,
        user_id: str,
        plugin_id: str,
        trade_data: Dict[str, Any]
    ) -> bool:
        """
        Capture a trade for performance tracking.
        
        Args:
            user_id: User identifier
            plugin_id: Plugin identifier
            trade_data: Trade data dictionary
            
        Returns:
            True if successful
        """
        return self.collector.capture_trade(user_id, plugin_id, trade_data)
    
    def capture_risk_metrics(
        self,
        user_id: str,
        plugin_id: str,
        risk_data: Dict[str, Any]
    ) -> bool:
        """
        Capture risk metrics for performance tracking.
        
        Args:
            user_id: User identifier
            plugin_id: Plugin identifier
            risk_data: Risk metrics dictionary
            
        Returns:
            True if successful
        """
        return self.collector.capture_risk_metrics(user_id, plugin_id, risk_data)
    
    def get_performance_metrics(
        self,
        user_id: str,
        plugin_id: Optional[str] = None,
        metric_type: str = "all_time"
    ) -> Dict[str, Any]:
        """
        Get performance metrics for a user.
        
        Args:
            user_id: User identifier
            plugin_id: Optional plugin identifier filter
            metric_type: Type (daily/weekly/monthly/all_time)
            
        Returns:
            Performance metrics dictionary
        """
        if metric_type == "all_time":
            return self.aggregator.aggregate_all_time_metrics(user_id, plugin_id or "all")
        elif metric_type == "daily":
            return self.aggregator.aggregate_daily_metrics(user_id, plugin_id or "all", datetime.now())
        elif metric_type == "weekly":
            # Get start of week (Sunday)
            today = datetime.now()
            days_since_sunday = today.weekday() + 1
            week_start = today - timedelta(days=days_since_sunday)
            return self.aggregator.aggregate_weekly_metrics(user_id, plugin_id or "all", week_start)
        elif metric_type == "monthly":
            # Get start of month
            today = datetime.now()
            month_start = datetime(today.year, today.month, 1)
            return self.aggregator.aggregate_monthly_metrics(user_id, plugin_id or "all", month_start)
        else:
            logger.warning(f"Unknown metric type: {metric_type}")
            return {}

