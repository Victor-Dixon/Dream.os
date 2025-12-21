"""
Performance Dashboard
=====================

Dashboard visualization and data formatting for performance metrics.
Provides formatted data for frontend display.

V2 Compliant: < 200 lines
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class PerformanceDashboard:
    """Dashboard visualization and data formatting."""
    
    def __init__(self, tracker):
        """
        Initialize performance dashboard.
        
        Args:
            tracker: PerformanceTracker instance
        """
        self.tracker = tracker
    
    def get_dashboard_data(
        self,
        user_id: str,
        plugin_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get complete dashboard data for a user.
        
        Args:
            user_id: User identifier
            plugin_id: Optional plugin identifier filter
            
        Returns:
            Dashboard data dictionary
        """
        try:
            # Get all metric types
            daily_metrics = self.tracker.get_performance_metrics(user_id, plugin_id, "daily")
            weekly_metrics = self.tracker.get_performance_metrics(user_id, plugin_id, "weekly")
            monthly_metrics = self.tracker.get_performance_metrics(user_id, plugin_id, "monthly")
            all_time_metrics = self.tracker.get_performance_metrics(user_id, plugin_id, "all_time")
            
            return {
                "user_id": user_id,
                "plugin_id": plugin_id or "all",
                "daily": daily_metrics,
                "weekly": weekly_metrics,
                "monthly": monthly_metrics,
                "all_time": all_time_metrics,
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to get dashboard data: {e}")
            return {}
    
    def format_metrics_for_display(
        self,
        metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Format metrics for frontend display.
        
        Args:
            metrics: Raw metrics dictionary
            
        Returns:
            Formatted metrics dictionary
        """
        if not metrics:
            return {
                "trade_count": 0,
                "win_rate": "0.0%",
                "total_pnl": "$0.00",
                "profit_factor": "0.00",
                "sharpe_ratio": "0.00",
                "max_drawdown": "0.0%",
                "status": "No data"
            }
        
        return {
            "trade_count": metrics.get("trade_count", 0),
            "win_count": metrics.get("win_count", 0),
            "loss_count": metrics.get("loss_count", 0),
            "win_rate": f"{metrics.get('win_rate', 0.0):.2f}%",
            "total_pnl": f"${metrics.get('total_pnl', 0.0):,.2f}",
            "profit_factor": f"{metrics.get('profit_factor', 0.0):.2f}",
            "sharpe_ratio": f"{metrics.get('sharpe_ratio', 0.0):.2f}",
            "max_drawdown": f"{metrics.get('max_drawdown', 0.0):.2f}%",
            "avg_trade_size": f"${metrics.get('avg_trade_size', 0.0):,.2f}",
            "best_trade_pnl": f"${metrics.get('best_trade_pnl', 0.0):,.2f}",
            "worst_trade_pnl": f"${metrics.get('worst_trade_pnl', 0.0):,.2f}",
            "status": "Active" if metrics.get("trade_count", 0) > 0 else "No trades"
        }
    
    def get_comparison_data(
        self,
        user_id: str,
        plugin_ids: List[str]
    ) -> Dict[str, Any]:
        """
        Get comparison data for multiple plugins.
        
        Args:
            user_id: User identifier
            plugin_ids: List of plugin identifiers
            
        Returns:
            Comparison data dictionary
        """
        try:
            comparison = {
                "user_id": user_id,
                "plugins": {},
                "best_performer": None,
                "worst_performer": None
            }
            
            best_pnl = float('-inf')
            worst_pnl = float('inf')
            
            for plugin_id in plugin_ids:
                metrics = self.tracker.get_performance_metrics(user_id, plugin_id, "all_time")
                formatted = self.format_metrics_for_display(metrics)
                comparison["plugins"][plugin_id] = formatted
                
                pnl = metrics.get("total_pnl", 0.0)
                if pnl > best_pnl:
                    best_pnl = pnl
                    comparison["best_performer"] = plugin_id
                if pnl < worst_pnl:
                    worst_pnl = pnl
                    comparison["worst_performer"] = plugin_id
            
            return comparison
            
        except Exception as e:
            logger.error(f"❌ Failed to get comparison data: {e}")
            return {}
    
    def get_trend_data(
        self,
        user_id: str,
        plugin_id: Optional[str] = None,
        days: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Get trend data for charting.
        
        Args:
            user_id: User identifier
            plugin_id: Optional plugin identifier filter
            days: Number of days to retrieve
            
        Returns:
            List of daily metrics dictionaries
        """
        try:
            trend_data = []
            today = datetime.now()
            
            for i in range(days):
                date = today - timedelta(days=i)
                metrics = self.tracker.aggregator.aggregate_daily_metrics(
                    user_id, plugin_id or "all", date
                )
                if metrics:
                    trend_data.append({
                        "date": date.isoformat(),
                        "total_pnl": metrics.get("total_pnl", 0.0),
                        "trade_count": metrics.get("trade_count", 0),
                        "win_rate": metrics.get("win_rate", 0.0)
                    })
            
            return sorted(trend_data, key=lambda x: x["date"])
            
        except Exception as e:
            logger.error(f"❌ Failed to get trend data: {e}")
            return []

