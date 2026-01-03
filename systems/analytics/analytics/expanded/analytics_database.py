"""
Analytics Database Management
============================

Database operations and management for the expanded analytics system.
This component handles all database initialization, CRUD operations, and data persistence.

Extracted from expanded_analytics_system.py for better modularity and maintainability.
"""

import sqlite3
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple
from contextlib import contextmanager

from .analytics_models import (
    AnalyticsReport, AnalyticsDashboard, AnalyticsWidget,
    TrendAnalysis, PredictiveInsight, AnalyticsShare, AnalyticsExport
)

logger = logging.getLogger(__name__)


class AnalyticsDatabaseManager:
    """Manages database operations for the expanded analytics system."""
    
    def __init__(self, data_dir: str = "data/expanded_analytics"):
        """Initialize the database manager."""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Database paths
        self.reports_db = self.data_dir / "analytics_reports.db"
        self.dashboards_db = self.data_dir / "analytics_dashboards.db"
        self.trends_db = self.data_dir / "trends_analysis.db"
        self.shares_db = self.data_dir / "analytics_shares.db"
        self.exports_db = self.data_dir / "analytics_exports.db"
        
        # Initialize databases
        self.init_databases()
    
    def init_databases(self):
        """Initialize all analytics databases."""
        logger.info("🔧 Initializing analytics databases...")
        
        # Initialize reports database
        self._init_reports_database()
        
        # Initialize dashboards database
        self._init_dashboards_database()
        
        # Initialize trends database
        self._init_trends_database()
        
        # Initialize shares database
        self._init_shares_database()
        
        # Initialize exports database
        self._init_exports_database()
        
        logger.info("✅ Analytics databases initialized successfully")
    
    def _init_reports_database(self):
        """Initialize reports database."""
        with sqlite3.connect(self.reports_db) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS analytics_reports (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    report_type TEXT NOT NULL,
                    generated_at TEXT NOT NULL,
                    time_period TEXT NOT NULL,
                    data_summary TEXT,
                    insights TEXT,
                    recommendations TEXT,
                    charts_data TEXT,
                    export_formats TEXT,
                    is_public INTEGER DEFAULT 0,
                    author_id TEXT,
                    author_name TEXT
                )
            """)
            
            # Create indexes for better performance
            conn.execute("CREATE INDEX IF NOT EXISTS idx_reports_type ON analytics_reports (report_type)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_reports_author ON analytics_reports (author_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_reports_public ON analytics_reports (is_public)")
            
            conn.commit()
    
    def _init_dashboards_database(self):
        """Initialize dashboards database."""
        with sqlite3.connect(self.dashboards_db) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS analytics_dashboards (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    widgets TEXT,
                    layout TEXT,
                    refresh_interval INTEGER DEFAULT 300,
                    is_public INTEGER DEFAULT 0,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    owner_id TEXT
                )
            """)
            
            # Create indexes for better performance
            conn.execute("CREATE INDEX IF NOT EXISTS idx_dashboards_owner ON analytics_dashboards (owner_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_dashboards_public ON analytics_dashboards (is_public)")
            
            conn.commit()
    
    def _init_trends_database(self):
        """Initialize trends database."""
        with sqlite3.connect(self.trends_db) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS trend_analysis (
                    id TEXT PRIMARY KEY,
                    metric TEXT NOT NULL,
                    trend_direction TEXT NOT NULL,
                    trend_strength REAL NOT NULL,
                    change_percentage REAL NOT NULL,
                    confidence REAL NOT NULL,
                    period TEXT NOT NULL,
                    data_points TEXT,
                    prediction REAL,
                    created_at TEXT NOT NULL
                )
            """)
            
            # Create indexes for better performance
            conn.execute("CREATE INDEX IF NOT EXISTS idx_trends_metric ON trend_analysis (metric)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_trends_period ON trend_analysis (period)")
            
            conn.commit()
    
    def _init_shares_database(self):
        """Initialize shares database."""
        with sqlite3.connect(self.shares_db) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS analytics_shares (
                    id TEXT PRIMARY KEY,
                    resource_id TEXT NOT NULL,
                    resource_type TEXT NOT NULL,
                    shared_with TEXT NOT NULL,
                    shared_at TEXT NOT NULL,
                    permissions TEXT
                )
            """)
            
            # Create indexes for better performance
            conn.execute("CREATE INDEX IF NOT EXISTS idx_shares_resource ON analytics_shares (resource_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_shares_shared_with ON analytics_shares (shared_with)")
            
            conn.commit()
    
    def _init_exports_database(self):
        """Initialize exports database."""
        with sqlite3.connect(self.exports_db) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS analytics_exports (
                    id TEXT PRIMARY KEY,
                    resource_id TEXT NOT NULL,
                    resource_type TEXT NOT NULL,
                    format_type TEXT NOT NULL,
                    export_path TEXT NOT NULL,
                    exported_at TEXT NOT NULL,
                    file_size INTEGER,
                    checksum TEXT
                )
            """)
            
            # Create indexes for better performance
            conn.execute("CREATE INDEX IF NOT EXISTS idx_exports_resource ON analytics_exports (resource_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_exports_format ON analytics_exports (format_type)")
            
            conn.commit()
    
    # Reports operations
    def save_report(self, report: AnalyticsReport) -> bool:
        """Save an analytics report to database."""
        try:
            with sqlite3.connect(self.reports_db) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO analytics_reports 
                    (id, title, report_type, generated_at, time_period, data_summary, 
                     insights, recommendations, charts_data, export_formats, 
                     is_public, author_id, author_name)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    report.id, report.title, report.report_type, 
                    report.generated_at.isoformat(), report.time_period,
                    json.dumps(report.data_summary), json.dumps(report.insights),
                    json.dumps(report.recommendations), json.dumps(report.charts_data),
                    json.dumps(report.export_formats), report.is_public,
                    report.author_id, report.author_name
                ))
                conn.commit()
                logger.info(f"✅ Report saved: {report.id}")
                return True
        except Exception as e:
            logger.error(f"❌ Failed to save report {report.id}: {e}")
            return False
    
    def load_report(self, report_id: str) -> Optional[AnalyticsReport]:
        """Load an analytics report from database."""
        try:
            with sqlite3.connect(self.reports_db) as conn:
                cursor = conn.execute(
                    "SELECT * FROM analytics_reports WHERE id = ?", 
                    (report_id,)
                )
                row = cursor.fetchone()
                
                if row:
                    report_data = {
                        'id': row['id'],
                        'title': row['title'],
                        'report_type': row['report_type'],
                        'generated_at': datetime.fromisoformat(row['generated_at']),
                        'time_period': row['time_period'],
                        'data_summary': json.loads(row['data_summary']) if row['data_summary'] else {},
                        'insights': json.loads(row['insights']) if row['insights'] else [],
                        'recommendations': json.loads(row['recommendations']) if row['recommendations'] else [],
                        'charts_data': json.loads(row['charts_data']) if row['charts_data'] else {},
                        'export_formats': json.loads(row['export_formats']) if row['export_formats'] else [],
                        'is_public': bool(row['is_public']),
                        'author_id': row['author_id'] or '',
                        'author_name': row['author_name'] or ''
                    }
                    
                    return AnalyticsReport(**report_data)
                else:
                    logger.warning(f"⚠️ Report not found: {report_id}")
                    return None
        except Exception as e:
            logger.error(f"❌ Failed to load report {report_id}: {e}")
            return None
    
    def load_all_reports(self) -> List[AnalyticsReport]:
        """Load all analytics reports from database."""
        reports = []
        try:
            with sqlite3.connect(self.reports_db) as conn:
                cursor = conn.execute("SELECT * FROM analytics_reports ORDER BY generated_at DESC")
                for row in cursor.fetchall():
                    report_data = {
                        'id': row['id'],
                        'title': row['title'],
                        'report_type': row['report_type'],
                        'generated_at': datetime.fromisoformat(row['generated_at']),
                        'time_period': row['time_period'],
                        'data_summary': json.loads(row['data_summary']) if row['data_summary'] else {},
                        'insights': json.loads(row['insights']) if row['insights'] else [],
                        'recommendations': json.loads(row['recommendations']) if row['recommendations'] else [],
                        'charts_data': json.loads(row['charts_data']) if row['charts_data'] else {},
                        'export_formats': json.loads(row['export_formats']) if row['export_formats'] else [],
                        'is_public': bool(row['is_public']),
                        'author_id': row['author_id'] or '',
                        'author_name': row['author_name'] or ''
                    }
                    
                    reports.append(AnalyticsReport(**report_data))
                
                logger.info(f"✅ Loaded {len(reports)} reports")
                return reports
        except Exception as e:
            logger.error(f"❌ Failed to load reports: {e}")
            return []
    
    def delete_report(self, report_id: str) -> bool:
        """Delete an analytics report from database."""
        try:
            with sqlite3.connect(self.reports_db) as conn:
                conn.execute("DELETE FROM analytics_reports WHERE id = ?", (report_id,))
                conn.commit()
                logger.info(f"✅ Report deleted: {report_id}")
                return True
        except Exception as e:
            logger.error(f"❌ Failed to delete report {report_id}: {e}")
            return False
    
    # Dashboards operations
    def save_dashboard(self, dashboard: AnalyticsDashboard) -> bool:
        """Save an analytics dashboard to database."""
        try:
            with sqlite3.connect(self.dashboards_db) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO analytics_dashboards 
                    (id, name, description, widgets, layout, refresh_interval, 
                     is_public, created_at, updated_at, owner_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    dashboard.id, dashboard.name, dashboard.description,
                    json.dumps(dashboard.widgets), json.dumps(dashboard.layout),
                    dashboard.refresh_interval, dashboard.is_public,
                    dashboard.created_at.isoformat(), dashboard.updated_at.isoformat(),
                    dashboard.owner_id
                ))
                conn.commit()
                logger.info(f"✅ Dashboard saved: {dashboard.id}")
                return True
        except Exception as e:
            logger.error(f"❌ Failed to save dashboard {dashboard.id}: {e}")
            return False
    
    def load_dashboard(self, dashboard_id: str) -> Optional[AnalyticsDashboard]:
        """Load an analytics dashboard from database."""
        try:
            with sqlite3.connect(self.dashboards_db) as conn:
                cursor = conn.execute(
                    "SELECT * FROM analytics_dashboards WHERE id = ?", 
                    (dashboard_id,)
                )
                row = cursor.fetchone()
                
                if row:
                    dashboard_data = {
                        'id': row['id'],
                        'name': row['name'],
                        'description': row['description'],
                        'widgets': json.loads(row['widgets']) if row['widgets'] else [],
                        'layout': json.loads(row['layout']) if row['layout'] else {},
                        'refresh_interval': row['refresh_interval'],
                        'is_public': bool(row['is_public']),
                        'created_at': datetime.fromisoformat(row['created_at']),
                        'updated_at': datetime.fromisoformat(row['updated_at']),
                        'owner_id': row['owner_id'] or ''
                    }
                    
                    return AnalyticsDashboard(**dashboard_data)
                else:
                    logger.warning(f"⚠️ Dashboard not found: {dashboard_id}")
                    return None
        except Exception as e:
            logger.error(f"❌ Failed to load dashboard {dashboard_id}: {e}")
            return None
    
    def load_all_dashboards(self) -> List[AnalyticsDashboard]:
        """Load all analytics dashboards from database."""
        dashboards = []
        try:
            with sqlite3.connect(self.dashboards_db) as conn:
                cursor = conn.execute("SELECT * FROM analytics_dashboards ORDER BY updated_at DESC")
                for row in cursor.fetchall():
                    dashboard_data = {
                        'id': row['id'],
                        'name': row['name'],
                        'description': row['description'],
                        'widgets': json.loads(row['widgets']) if row['widgets'] else [],
                        'layout': json.loads(row['layout']) if row['layout'] else {},
                        'refresh_interval': row['refresh_interval'],
                        'is_public': bool(row['is_public']),
                        'created_at': datetime.fromisoformat(row['created_at']),
                        'updated_at': datetime.fromisoformat(row['updated_at']),
                        'owner_id': row['owner_id'] or ''
                    }
                    
                    dashboards.append(AnalyticsDashboard(**dashboard_data))
                
                logger.info(f"✅ Loaded {len(dashboards)} dashboards")
                return dashboards
        except Exception as e:
            logger.error(f"❌ Failed to load dashboards: {e}")
            return []
    
    def delete_dashboard(self, dashboard_id: str) -> bool:
        """Delete an analytics dashboard from database."""
        try:
            with sqlite3.connect(self.dashboards_db) as conn:
                conn.execute("DELETE FROM analytics_dashboards WHERE id = ?", (dashboard_id,))
                conn.commit()
                logger.info(f"✅ Dashboard deleted: {dashboard_id}")
                return True
        except Exception as e:
            logger.error(f"❌ Failed to delete dashboard {dashboard_id}: {e}")
            return False
    
    # Trends operations
    def save_trend(self, trend: TrendAnalysis) -> bool:
        """Save a trend analysis to database."""
        try:
            with sqlite3.connect(self.trends_db) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO trend_analysis 
                    (id, metric, trend_direction, trend_strength, change_percentage, 
                     confidence, period, data_points, prediction, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    trend.id, trend.metric, trend.trend_direction, trend.trend_strength,
                    trend.change_percentage, trend.confidence, trend.period,
                    json.dumps([(dt.isoformat(), value) for dt, value in trend.data_points]),
                    trend.prediction, datetime.now().isoformat()
                ))
                conn.commit()
                logger.info(f"✅ Trend saved: {trend.metric}")
                return True
        except Exception as e:
            logger.error(f"❌ Failed to save trend {trend.metric}: {e}")
            return False
    
    def load_trends(self) -> List[TrendAnalysis]:
        """Load all trend analyses from database."""
        trends = []
        try:
            with sqlite3.connect(self.trends_db) as conn:
                cursor = conn.execute("SELECT * FROM trend_analysis ORDER BY created_at DESC")
                for row in cursor.fetchall():
                    trend_data = {
                        'id': row['id'],
                        'metric': row['metric'],
                        'trend_direction': row['trend_direction'],
                        'trend_strength': row['trend_strength'],
                        'change_percentage': row['change_percentage'],
                        'confidence': row['confidence'],
                        'period': row['period'],
                        'data_points': [
                            (datetime.fromisoformat(dt_str), value) 
                            for dt_str, value in json.loads(row['data_points'])
                        ] if row['data_points'] else [],
                        'prediction': row['prediction']
                    }
                    
                    trends.append(TrendAnalysis(**trend_data))
                
                logger.info(f"✅ Loaded {len(trends)} trends")
                return trends
        except Exception as e:
            logger.error(f"❌ Failed to load trends: {e}")
            return []
    
    # Utility methods
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        stats = {}
        
        try:
            # Reports stats
            with sqlite3.connect(self.reports_db) as conn:
                cursor = conn.execute("SELECT COUNT(*) as count FROM analytics_reports")
                stats['reports_count'] = cursor.fetchone()['count']
                
                cursor = conn.execute("SELECT COUNT(*) as count FROM analytics_reports WHERE is_public = 1")
                stats['public_reports_count'] = cursor.fetchone()['count']
            
            # Dashboards stats
            with sqlite3.connect(self.dashboards_db) as conn:
                cursor = conn.execute("SELECT COUNT(*) as count FROM analytics_dashboards")
                stats['dashboards_count'] = cursor.fetchone()['count']
                
                cursor = conn.execute("SELECT COUNT(*) as count FROM analytics_dashboards WHERE is_public = 1")
                stats['public_dashboards_count'] = cursor.fetchone()['count']
            
            # Trends stats
            with sqlite3.connect(self.trends_db) as conn:
                cursor = conn.execute("SELECT COUNT(*) as count FROM trend_analysis")
                stats['trends_count'] = cursor.fetchone()['count']
            
            logger.info("✅ Database stats collected")
            return stats
            
        except Exception as e:
            logger.error(f"❌ Failed to get database stats: {e}")
            return {}
    
    def cleanup_old_data(self, days_old: int = 90) -> int:
        """Clean up old data from databases."""
        cutoff_date = datetime.now() - timedelta(days=days_old)
        deleted_count = 0
        
        try:
            # Clean up old reports
            with sqlite3.connect(self.reports_db) as conn:
                cursor = conn.execute(
                    "DELETE FROM analytics_reports WHERE generated_at < ?",
                    (cutoff_date.isoformat(),)
                )
                deleted_count += cursor.rowcount
            
            # Clean up old trends
            with sqlite3.connect(self.trends_db) as conn:
                cursor = conn.execute(
                    "DELETE FROM trend_analysis WHERE created_at < ?",
                    (cutoff_date.isoformat(),)
                )
                deleted_count += cursor.rowcount
            
            logger.info(f"✅ Cleaned up {deleted_count} old records")
            return deleted_count
            
        except Exception as e:
            logger.error(f"❌ Failed to cleanup old data: {e}")
            return 0
    
    @contextmanager
    def get_connection(self, db_type: str = "reports"):
        """Get a database connection with context management."""
        if db_type == "reports":
            db_path = self.reports_db
        elif db_type == "dashboards":
            db_path = self.dashboards_db
        elif db_type == "trends":
            db_path = self.trends_db
        elif db_type == "shares":
            db_path = self.shares_db
        elif db_type == "exports":
            db_path = self.exports_db
        else:
            raise ValueError(f"Unknown database type: {db_type}")
        
        conn = sqlite3.connect(db_path)
        try:
            yield conn
        finally:
            conn.close() 