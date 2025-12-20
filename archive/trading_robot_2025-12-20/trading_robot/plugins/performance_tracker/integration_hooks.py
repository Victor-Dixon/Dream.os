"""
Integration Hooks
=================

Integration hooks for live_executor, risk_manager, and plugin_manager.
Provides easy integration points for performance tracking.

V2 Compliant: < 200 lines
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class PerformanceTrackingHooks:
    """Integration hooks for performance tracking."""
    
    def __init__(self, performance_tracker):
        """
        Initialize integration hooks.
        
        Args:
            performance_tracker: PerformanceTracker instance
        """
        self.tracker = performance_tracker
        self.enabled = True
    
    def hook_trade_execution(
        self,
        user_id: str,
        plugin_id: str,
        symbol: str,
        side: str,
        quantity: int,
        entry_price: float,
        exit_price: Optional[float] = None,
        pnl: Optional[float] = None,
        order_id: Optional[str] = None
    ) -> bool:
        """
        Hook for trade execution from live_executor.
        
        Args:
            user_id: User identifier
            plugin_id: Plugin identifier
            symbol: Trading symbol
            side: Trade side (buy/sell)
            quantity: Trade quantity
            entry_price: Entry price
            exit_price: Optional exit price (for closed trades)
            pnl: Optional P&L (for closed trades)
            order_id: Optional order ID
            
        Returns:
            True if captured successfully
        """
        if not self.enabled:
            return False
        
        try:
            trade_data = {
                "symbol": symbol,
                "side": side,
                "quantity": quantity,
                "entry_price": entry_price,
                "exit_price": exit_price,
                "pnl": pnl,
                "order_id": order_id,
                "timestamp": datetime.now().isoformat()
            }
            
            return self.tracker.capture_trade(user_id, plugin_id, trade_data)
            
        except Exception as e:
            logger.error(f"❌ Failed to hook trade execution: {e}")
            return False
    
    def hook_risk_metrics(
        self,
        user_id: str,
        plugin_id: str,
        portfolio_risk: float,
        position_risk: float,
        daily_loss: float,
        max_drawdown: float,
        account_balance: float
    ) -> bool:
        """
        Hook for risk metrics from risk_manager.
        
        Args:
            user_id: User identifier
            plugin_id: Plugin identifier
            portfolio_risk: Portfolio risk percentage
            position_risk: Position risk percentage
            daily_loss: Daily loss amount
            max_drawdown: Maximum drawdown percentage
            account_balance: Current account balance
            
        Returns:
            True if captured successfully
        """
        if not self.enabled:
            return False
        
        try:
            risk_data = {
                "portfolio_risk": portfolio_risk,
                "position_risk": position_risk,
                "daily_loss": daily_loss,
                "max_drawdown": max_drawdown,
                "account_balance": account_balance,
                "timestamp": datetime.now().isoformat()
            }
            
            return self.tracker.capture_risk_metrics(user_id, plugin_id, risk_data)
            
        except Exception as e:
            logger.error(f"❌ Failed to hook risk metrics: {e}")
            return False
    
    def hook_plugin_metrics(
        self,
        user_id: str,
        plugin_id: str,
        plugin_metrics: Dict[str, Any]
    ) -> bool:
        """
        Hook for plugin-specific metrics from plugin_manager.
        
        Args:
            user_id: User identifier
            plugin_id: Plugin identifier
            plugin_metrics: Plugin-specific metrics dictionary
            
        Returns:
            True if captured successfully
        """
        if not self.enabled:
            return False
        
        try:
            return self.tracker.collector.capture_plugin_metrics(
                user_id, plugin_id, plugin_metrics
            )
            
        except Exception as e:
            logger.error(f"❌ Failed to hook plugin metrics: {e}")
            return False
    
    def enable(self):
        """Enable performance tracking hooks."""
        self.enabled = True
        logger.info("✅ Performance tracking hooks enabled")
    
    def disable(self):
        """Disable performance tracking hooks."""
        self.enabled = False
        logger.info("⚠️ Performance tracking hooks disabled")

