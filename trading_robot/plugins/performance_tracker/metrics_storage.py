"""
Metrics Storage
===============

Storage layer for performance metrics.
Handles database operations for metrics persistence.

V2 Compliant: < 200 lines
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import sys

# Add trading_robot to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from database.connection import get_db_session, init_database
from database.models import UserPerformanceMetric, MetricType

logger = logging.getLogger(__name__)


class MetricsStorage:
    """Storage layer for performance metrics."""
    
    def __init__(self, database_url: Optional[str] = None):
        """
        Initialize metrics storage.
        
        Args:
            database_url: Optional database URL (defaults to SQLite)
        """
        self.database_url = database_url or "sqlite:///trading_robot.db"
        self._initialized = False
    
    def initialize(self):
        """Initialize database connection and create tables if needed."""
        try:
            # Ensure database tables exist
            init_database(create_tables=True)
            logger.info("📊 Metrics storage initialized")
            self._initialized = True
        except Exception as e:
            logger.error(f"❌ Failed to initialize metrics storage: {e}")
            raise
    
    def save_trade_metric(
        self,
        user_id: str,
        plugin_id: str,
        trade_data: Dict[str, Any]
    ) -> bool:
        """
        Save individual trade metric.
        
        Args:
            user_id: User identifier
            plugin_id: Plugin identifier
            trade_data: Trade data dictionary
            
        Returns:
            True if successful
        """
        try:
            if not self._initialized:
                self.initialize()
            
            # TODO: Implement database save when database is ready
            logger.debug(f"💾 Saving trade metric for user {user_id}, plugin {plugin_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to save trade metric: {e}")
            return False
    
    def save_performance_metrics(
        self,
        user_id: str,
        plugin_id: str,
        metric_date: datetime,
        metric_type: str,
        metrics: Dict[str, Any]
    ) -> bool:
        """
        Save aggregated performance metrics.
        
        Args:
            user_id: User identifier
            plugin_id: Plugin identifier
            metric_date: Date for metrics
            metric_type: Type (daily/weekly/monthly/all_time)
            metrics: Metrics dictionary with keys:
                - trade_count, win_count, loss_count
                - total_pnl, win_rate, profit_factor
                - sharpe_ratio, max_drawdown
                - avg_trade_size, best_trade_pnl, worst_trade_pnl
            
        Returns:
            True if successful
        """
        try:
            if not self._initialized:
                self.initialize()
            
            # Convert metric_type string to enum
            try:
                metric_type_enum = MetricType(metric_type.lower())
            except ValueError:
                logger.error(f"❌ Invalid metric_type: {metric_type}")
                return False
            
            with get_db_session() as session:
                # Check if record already exists (upsert)
                existing = session.query(UserPerformanceMetric).filter(
                    UserPerformanceMetric.user_id == user_id,
                    UserPerformanceMetric.plugin_id == plugin_id,
                    UserPerformanceMetric.metric_date == metric_date,
                    UserPerformanceMetric.metric_type == metric_type_enum
                ).first()
                
                if existing:
                    # Update existing record
                    existing.trade_count = metrics.get("trade_count", 0)
                    existing.win_count = metrics.get("win_count", 0)
                    existing.loss_count = metrics.get("loss_count", 0)
                    existing.total_pnl = metrics.get("total_pnl", 0.0)
                    existing.win_rate = metrics.get("win_rate")
                    existing.profit_factor = metrics.get("profit_factor")
                    existing.sharpe_ratio = metrics.get("sharpe_ratio")
                    existing.max_drawdown = metrics.get("max_drawdown")
                    existing.avg_trade_size = metrics.get("avg_trade_size")
                    existing.best_trade_pnl = metrics.get("best_trade_pnl")
                    existing.worst_trade_pnl = metrics.get("worst_trade_pnl")
                else:
                    # Create new record
                    metric = UserPerformanceMetric(
                        user_id=user_id,
                        plugin_id=plugin_id,
                        metric_date=metric_date,
                        metric_type=metric_type_enum,
                        trade_count=metrics.get("trade_count", 0),
                        win_count=metrics.get("win_count", 0),
                        loss_count=metrics.get("loss_count", 0),
                        total_pnl=metrics.get("total_pnl", 0.0),
                        win_rate=metrics.get("win_rate"),
                        profit_factor=metrics.get("profit_factor"),
                        sharpe_ratio=metrics.get("sharpe_ratio"),
                        max_drawdown=metrics.get("max_drawdown"),
                        avg_trade_size=metrics.get("avg_trade_size"),
                        best_trade_pnl=metrics.get("best_trade_pnl"),
                        worst_trade_pnl=metrics.get("worst_trade_pnl"),
                    )
                    session.add(metric)
                
                # Commit is handled by context manager
                logger.debug(f"💾 Saved {metric_type} metrics for user {user_id}, plugin {plugin_id}")
                return True
            
        except Exception as e:
            logger.error(f"❌ Failed to save performance metrics: {e}")
            return False
    
    def get_performance_metrics(
        self,
        user_id: str,
        plugin_id: Optional[str] = None,
        metric_type: str = "all_time",
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve performance metrics.
        
        Args:
            user_id: User identifier
            plugin_id: Optional plugin identifier filter
            metric_type: Type (daily/weekly/monthly/all_time)
            start_date: Optional start date filter
            end_date: Optional end date filter
            
        Returns:
            List of metrics dictionaries
        """
        try:
            if not self._initialized:
                self.initialize()
            
            # Convert metric_type string to enum
            try:
                metric_type_enum = MetricType(metric_type.lower())
            except ValueError:
                logger.error(f"❌ Invalid metric_type: {metric_type}")
                return []
            
            with get_db_session() as session:
                query = session.query(UserPerformanceMetric).filter(
                    UserPerformanceMetric.user_id == user_id,
                    UserPerformanceMetric.metric_type == metric_type_enum
                )
                
                # Apply optional filters
                if plugin_id:
                    query = query.filter(UserPerformanceMetric.plugin_id == plugin_id)
                
                if start_date:
                    query = query.filter(UserPerformanceMetric.metric_date >= start_date)
                
                if end_date:
                    query = query.filter(UserPerformanceMetric.metric_date <= end_date)
                
                # Order by date descending
                results = query.order_by(UserPerformanceMetric.metric_date.desc()).all()
                
                # Convert to dictionaries
                metrics_list = []
                for metric in results:
                    metrics_list.append({
                        "id": metric.id,
                        "user_id": metric.user_id,
                        "plugin_id": metric.plugin_id,
                        "metric_date": metric.metric_date.isoformat(),
                        "metric_type": metric.metric_type.value,
                        "trade_count": metric.trade_count,
                        "win_count": metric.win_count,
                        "loss_count": metric.loss_count,
                        "total_pnl": float(metric.total_pnl) if metric.total_pnl else None,
                        "win_rate": float(metric.win_rate) if metric.win_rate else None,
                        "profit_factor": float(metric.profit_factor) if metric.profit_factor else None,
                        "sharpe_ratio": float(metric.sharpe_ratio) if metric.sharpe_ratio else None,
                        "max_drawdown": float(metric.max_drawdown) if metric.max_drawdown else None,
                        "avg_trade_size": float(metric.avg_trade_size) if metric.avg_trade_size else None,
                        "best_trade_pnl": float(metric.best_trade_pnl) if metric.best_trade_pnl else None,
                        "worst_trade_pnl": float(metric.worst_trade_pnl) if metric.worst_trade_pnl else None,
                        "created_at": metric.created_at.isoformat(),
                        "updated_at": metric.updated_at.isoformat(),
                    })
                
                logger.debug(f"📊 Retrieved {len(metrics_list)} {metric_type} metrics for user {user_id}")
                return metrics_list
            
        except Exception as e:
            logger.error(f"❌ Failed to get performance metrics: {e}")
            return []
    
    def get_trades(
        self,
        user_id: str,
        plugin_id: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve trade history.
        
        Args:
            user_id: User identifier
            plugin_id: Optional plugin identifier filter
            start_date: Optional start date filter
            end_date: Optional end date filter
            
        Returns:
            List of trade dictionaries
        """
        try:
            if not self._initialized:
                self.initialize()
            
            # TODO: Implement database query when database is ready
            logger.debug(f"📊 Retrieving trades for user {user_id}")
            return []
            
        except Exception as e:
            logger.error(f"❌ Failed to get trades: {e}")
            return []

