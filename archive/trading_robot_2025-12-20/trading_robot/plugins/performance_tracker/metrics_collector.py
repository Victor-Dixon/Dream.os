"""
Metrics Collector
================

Collects trading metrics from live executor, risk manager, and plugins.
Captures all trades and risk metrics for performance tracking.

V2 Compliant: < 200 lines
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class MetricsCollector:
    """Collects metrics from trading engine components."""
    
    def __init__(self, storage):
        """
        Initialize metrics collector.
        
        Args:
            storage: MetricsStorage instance
        """
        self.storage = storage
        self.trades: List[Dict[str, Any]] = []
        self.risk_metrics: List[Dict[str, Any]] = []
    
    def capture_trade(
        self,
        user_id: str,
        plugin_id: str,
        trade_data: Dict[str, Any]
    ) -> bool:
        """
        Capture a trade from live executor.
        
        Args:
            user_id: User identifier
            plugin_id: Plugin identifier
            trade_data: Trade data (symbol, side, quantity, entry_price, exit_price, pnl, etc.)
            
        Returns:
            True if successful
        """
        try:
            trade_metric = {
                "user_id": user_id,
                "plugin_id": plugin_id,
                "timestamp": datetime.now().isoformat(),
                **trade_data
            }
            
            self.trades.append(trade_metric)
            
            # Save to storage
            self.storage.save_trade_metric(user_id, plugin_id, trade_metric)
            
            logger.debug(f"📊 Captured trade: {plugin_id} - {trade_data.get('symbol', 'N/A')}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to capture trade: {e}")
            return False
    
    def capture_risk_metrics(
        self,
        user_id: str,
        plugin_id: str,
        risk_data: Dict[str, Any]
    ) -> bool:
        """
        Capture risk metrics from risk manager.
        
        Args:
            user_id: User identifier
            plugin_id: Plugin identifier
            risk_data: Risk metrics (portfolio_risk, position_risk, daily_loss, etc.)
            
        Returns:
            True if successful
        """
        try:
            risk_metric = {
                "user_id": user_id,
                "plugin_id": plugin_id,
                "timestamp": datetime.now().isoformat(),
                **risk_data
            }
            
            self.risk_metrics.append(risk_metric)
            
            logger.debug(f"📊 Captured risk metrics: {plugin_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to capture risk metrics: {e}")
            return False
    
    def capture_plugin_metrics(
        self,
        user_id: str,
        plugin_id: str,
        plugin_metrics: Dict[str, Any]
    ) -> bool:
        """
        Capture plugin-specific metrics from plugin manager.
        
        Args:
            user_id: User identifier
            plugin_id: Plugin identifier
            plugin_metrics: Plugin-specific metrics
            
        Returns:
            True if successful
        """
        try:
            metric = {
                "user_id": user_id,
                "plugin_id": plugin_id,
                "timestamp": datetime.now().isoformat(),
                **plugin_metrics
            }
            
            logger.debug(f"📊 Captured plugin metrics: {plugin_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to capture plugin metrics: {e}")
            return False
    
    def get_trades_for_user(
        self,
        user_id: str,
        plugin_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get trades for a user.
        
        Args:
            user_id: User identifier
            plugin_id: Optional plugin filter
            
        Returns:
            List of trade dictionaries
        """
        if plugin_id:
            return [t for t in self.trades if t.get("user_id") == user_id and t.get("plugin_id") == plugin_id]
        return [t for t in self.trades if t.get("user_id") == user_id]
    
    def get_risk_metrics_for_user(
        self,
        user_id: str,
        plugin_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get risk metrics for a user.
        
        Args:
            user_id: User identifier
            plugin_id: Optional plugin filter
            
        Returns:
            List of risk metric dictionaries
        """
        if plugin_id:
            return [r for r in self.risk_metrics if r.get("user_id") == user_id and r.get("plugin_id") == plugin_id]
        return [r for r in self.risk_metrics if r.get("user_id") == user_id]

