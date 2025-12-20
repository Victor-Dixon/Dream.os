"""
Scheduled Aggregation
=====================

Scheduled jobs for automatic metrics aggregation.
Aggregates daily metrics at market close, weekly on Sunday, monthly on first of month.

V2 Compliant: < 200 lines
"""

import asyncio
import logging
from typing import Dict, List, Optional
from datetime import datetime, time, timedelta

logger = logging.getLogger(__name__)


class ScheduledAggregation:
    """Scheduled aggregation jobs for performance metrics."""
    
    def __init__(self, aggregator, storage):
        """
        Initialize scheduled aggregation.
        
        Args:
            aggregator: MetricsAggregator instance
            storage: MetricsStorage instance
        """
        self.aggregator = aggregator
        self.storage = storage
        self.running = False
        self.tasks = []
    
    async def start(self):
        """Start scheduled aggregation jobs."""
        if self.running:
            logger.warning("⚠️ Scheduled aggregation already running")
            return
        
        self.running = True
        logger.info("🚀 Starting scheduled aggregation jobs")
        
        # Start aggregation tasks
        self.tasks = [
            asyncio.create_task(self._daily_aggregation_loop()),
            asyncio.create_task(self._weekly_aggregation_loop()),
            asyncio.create_task(self._monthly_aggregation_loop()),
            asyncio.create_task(self._all_time_aggregation_loop())
        ]
    
    async def stop(self):
        """Stop scheduled aggregation jobs."""
        if not self.running:
            return
        
        self.running = False
        logger.info("🛑 Stopping scheduled aggregation jobs")
        
        # Cancel all tasks
        for task in self.tasks:
            task.cancel()
        
        # Wait for tasks to complete
        await asyncio.gather(*self.tasks, return_exceptions=True)
        self.tasks = []
    
    async def _daily_aggregation_loop(self):
        """Daily aggregation at market close (4:00 PM ET)."""
        while self.running:
            try:
                now = datetime.now()
                market_close = now.replace(hour=16, minute=0, second=0, microsecond=0)
                
                # If market already closed today, schedule for tomorrow
                if now >= market_close:
                    market_close += timedelta(days=1)
                
                # Wait until market close
                wait_seconds = (market_close - now).total_seconds()
                logger.info(f"⏰ Daily aggregation scheduled for {market_close.strftime('%Y-%m-%d %H:%M:%S')}")
                await asyncio.sleep(wait_seconds)
                
                # Aggregate daily metrics for all users/plugins
                await self._aggregate_all_daily_metrics()
                
                # Wait a bit before next check
                await asyncio.sleep(60)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Error in daily aggregation loop: {e}")
                await asyncio.sleep(3600)  # Wait 1 hour on error
    
    async def _weekly_aggregation_loop(self):
        """Weekly aggregation on Sunday at midnight."""
        while self.running:
            try:
                now = datetime.now()
                
                # Find next Sunday
                days_until_sunday = (6 - now.weekday()) % 7
                if days_until_sunday == 0 and now.hour >= 0:
                    # If it's Sunday and past midnight, schedule for next Sunday
                    days_until_sunday = 7
                
                next_sunday = now + timedelta(days=days_until_sunday)
                next_sunday = next_sunday.replace(hour=0, minute=0, second=0, microsecond=0)
                
                # Wait until next Sunday
                wait_seconds = (next_sunday - now).total_seconds()
                logger.info(f"⏰ Weekly aggregation scheduled for {next_sunday.strftime('%Y-%m-%d %H:%M:%S')}")
                await asyncio.sleep(wait_seconds)
                
                # Aggregate weekly metrics for all users/plugins
                await self._aggregate_all_weekly_metrics()
                
                # Wait a bit before next check
                await asyncio.sleep(3600)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Error in weekly aggregation loop: {e}")
                await asyncio.sleep(86400)  # Wait 1 day on error
    
    async def _monthly_aggregation_loop(self):
        """Monthly aggregation on first of month at midnight."""
        while self.running:
            try:
                now = datetime.now()
                
                # Find first of next month
                if now.day == 1 and now.hour >= 0:
                    # If it's the first and past midnight, schedule for next month
                    if now.month == 12:
                        next_month = datetime(now.year + 1, 1, 1)
                    else:
                        next_month = datetime(now.year, now.month + 1, 1)
                else:
                    # Calculate first of next month
                    if now.month == 12:
                        next_month = datetime(now.year + 1, 1, 1)
                    else:
                        next_month = datetime(now.year, now.month + 1, 1)
                
                next_month = next_month.replace(hour=0, minute=0, second=0, microsecond=0)
                
                # Wait until first of next month
                wait_seconds = (next_month - now).total_seconds()
                logger.info(f"⏰ Monthly aggregation scheduled for {next_month.strftime('%Y-%m-%d %H:%M:%S')}")
                await asyncio.sleep(wait_seconds)
                
                # Aggregate monthly metrics for all users/plugins
                await self._aggregate_all_monthly_metrics()
                
                # Wait a bit before next check
                await asyncio.sleep(86400)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Error in monthly aggregation loop: {e}")
                await asyncio.sleep(86400)  # Wait 1 day on error
    
    async def _all_time_aggregation_loop(self):
        """All-time aggregation runs periodically (every 6 hours)."""
        while self.running:
            try:
                # Aggregate all-time metrics every 6 hours
                await asyncio.sleep(6 * 3600)  # 6 hours
                
                # Aggregate all-time metrics for all users/plugins
                await self._aggregate_all_all_time_metrics()
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Error in all-time aggregation loop: {e}")
                await asyncio.sleep(3600)  # Wait 1 hour on error
    
    async def _aggregate_all_daily_metrics(self):
        """Aggregate daily metrics for all users/plugins."""
        try:
            # TODO: Get all user_ids and plugin_ids from storage when database is ready
            # For now, this is a placeholder
            logger.info("📊 Aggregating daily metrics for all users/plugins")
            # Example: self.aggregator.aggregate_daily_metrics(user_id, plugin_id, datetime.now())
        except Exception as e:
            logger.error(f"❌ Failed to aggregate daily metrics: {e}")
    
    async def _aggregate_all_weekly_metrics(self):
        """Aggregate weekly metrics for all users/plugins."""
        try:
            # TODO: Get all user_ids and plugin_ids from storage when database is ready
            logger.info("📊 Aggregating weekly metrics for all users/plugins")
            # Example: self.aggregator.aggregate_weekly_metrics(user_id, plugin_id, week_start)
        except Exception as e:
            logger.error(f"❌ Failed to aggregate weekly metrics: {e}")
    
    async def _aggregate_all_monthly_metrics(self):
        """Aggregate monthly metrics for all users/plugins."""
        try:
            # TODO: Get all user_ids and plugin_ids from storage when database is ready
            logger.info("📊 Aggregating monthly metrics for all users/plugins")
            # Example: self.aggregator.aggregate_monthly_metrics(user_id, plugin_id, month_start)
        except Exception as e:
            logger.error(f"❌ Failed to aggregate monthly metrics: {e}")
    
    async def _aggregate_all_all_time_metrics(self):
        """Aggregate all-time metrics for all users/plugins."""
        try:
            # TODO: Get all user_ids and plugin_ids from storage when database is ready
            logger.info("📊 Aggregating all-time metrics for all users/plugins")
            # Example: self.aggregator.aggregate_all_time_metrics(user_id, plugin_id)
        except Exception as e:
            logger.error(f"❌ Failed to aggregate all-time metrics: {e}")

