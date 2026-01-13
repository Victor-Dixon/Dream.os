"""
Dashboard Manager
================

Dashboard creation, management, and widget functionality for the expanded analytics system.
This component handles dashboard operations, widget management, and data generation.

Extracted from expanded_analytics_system.py for better modularity and maintainability.
"""

import logging
import uuid
from datetime import datetime
from typing import List, Dict, Optional, Any, Tuple
from pathlib import Path

from .analytics_models import AnalyticsDashboard, AnalyticsWidget
from .analytics_database import AnalyticsDatabaseManager

logger = logging.getLogger(__name__)


class DashboardManager:
    """Manages dashboard operations and widget functionality."""
    
    def __init__(self, database_manager: AnalyticsDatabaseManager):
        """Initialize the dashboard manager."""
        self.database_manager = database_manager
        self.analytics_subsystems = {}
        self._init_analytics_subsystems()
    
    def _init_analytics_subsystems(self):
        """Initialize analytics subsystems."""
        try:
            # Import existing analytics systems
            from dreamscape.core.analytics.analytics_system import ComprehensiveAnalyticsSystem
            from dreamscape.core.analytics.content_analytics_integration import ContentAnalyticsIntegration
            from dreamscape.core.analytics.time_series_analyzer import TimeSeriesAnalyzer
            
            self.analytics_subsystems['comprehensive'] = ComprehensiveAnalyticsSystem()
            self.analytics_subsystems['content'] = ContentAnalyticsIntegration()
            self.analytics_subsystems['time_series'] = TimeSeriesAnalyzer()
            
            logger.info("✅ Dashboard analytics subsystems initialized")
            
        except ImportError as e:
            logger.warning(f"⚠️ Some analytics subsystems not available: {e}")
            self.analytics_subsystems = {}
    
    def create_dashboard(
        self, 
        name: str, 
        description: str = "", 
        owner_id: str = "",
        widgets: List[Dict[str, Any]] = None
    ) -> AnalyticsDashboard:
        """
        Create a new analytics dashboard.
        
        Args:
            name: Dashboard name
            description: Dashboard description
            owner_id: ID of the dashboard owner
            widgets: List of widget configurations
            
        Returns:
            AnalyticsDashboard object
        """
        try:
            logger.info(f"📊 Creating dashboard: {name}")
            
            # Generate default widgets if none provided
            if widgets is None:
                widgets = self._get_default_widgets()
            
            # Create dashboard
            dashboard = AnalyticsDashboard(
                id=str(uuid.uuid4()),
                name=name,
                description=description,
                widgets=widgets,
                layout=self._get_default_layout(),
                owner_id=owner_id
            )
            
            # Save dashboard to database
            self.database_manager.save_dashboard(dashboard)
            
            logger.info(f"✅ Dashboard created: {dashboard.id}")
            return dashboard
            
        except Exception as e:
            logger.error(f"❌ Failed to create dashboard: {e}")
            raise
    
    def get_dashboard_data(self, dashboard_id: str) -> Dict[str, Any]:
        """
        Get dashboard data with widget data populated.
        
        Args:
            dashboard_id: ID of the dashboard
            
        Returns:
            Dictionary containing dashboard data and widget data
        """
        try:
            logger.info(f"📊 Getting dashboard data: {dashboard_id}")
            
            # Load dashboard
            dashboard = self.database_manager.load_dashboard(dashboard_id)
            if not dashboard:
                logger.warning(f"⚠️ Dashboard not found: {dashboard_id}")
                return {}
            
            # Generate widget data
            widget_data = {}
            for widget in dashboard.widgets:
                try:
                    widget_data[widget['id']] = self._generate_widget_data(widget)
                except Exception as e:
                    logger.error(f"❌ Failed to generate widget data for {widget['id']}: {e}")
                    widget_data[widget['id']] = {"error": str(e)}
            
            # Prepare dashboard data
            dashboard_data = {
                "dashboard": dashboard.to_dict(),
                "widgets": widget_data,
                "generated_at": datetime.now().isoformat()
            }
            
            logger.info(f"✅ Dashboard data generated: {dashboard_id}")
            return dashboard_data
            
        except Exception as e:
            logger.error(f"❌ Failed to get dashboard data: {e}")
            return {}
    
    def update_dashboard(
        self, 
        dashboard_id: str, 
        updates: Dict[str, Any]
    ) -> bool:
        """
        Update an existing dashboard.
        
        Args:
            dashboard_id: ID of the dashboard to update
            updates: Dictionary containing updates
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"📊 Updating dashboard: {dashboard_id}")
            
            # Load existing dashboard
            dashboard = self.database_manager.load_dashboard(dashboard_id)
            if not dashboard:
                logger.warning(f"⚠️ Dashboard not found: {dashboard_id}")
                return False
            
            # Apply updates
            for key, value in updates.items():
                if hasattr(dashboard, key):
                    setattr(dashboard, key, value)
            
            # Update timestamp
            dashboard.updated_at = datetime.now()
            
            # Save updated dashboard
            success = self.database_manager.save_dashboard(dashboard)
            
            if success:
                logger.info(f"✅ Dashboard updated: {dashboard_id}")
            else:
                logger.error(f"❌ Failed to save updated dashboard: {dashboard_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Failed to update dashboard: {e}")
            return False
    
    def delete_dashboard(self, dashboard_id: str) -> bool:
        """
        Delete a dashboard.
        
        Args:
            dashboard_id: ID of the dashboard to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"📊 Deleting dashboard: {dashboard_id}")
            
            success = self.database_manager.delete_dashboard(dashboard_id)
            
            if success:
                logger.info(f"✅ Dashboard deleted: {dashboard_id}")
            else:
                logger.error(f"❌ Failed to delete dashboard: {dashboard_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Failed to delete dashboard: {e}")
            return False
    
    def add_widget_to_dashboard(
        self, 
        dashboard_id: str, 
        widget_config: Dict[str, Any]
    ) -> bool:
        """
        Add a widget to a dashboard.
        
        Args:
            dashboard_id: ID of the dashboard
            widget_config: Widget configuration
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"📊 Adding widget to dashboard: {dashboard_id}")
            
            # Load dashboard
            dashboard = self.database_manager.load_dashboard(dashboard_id)
            if not dashboard:
                logger.warning(f"⚠️ Dashboard not found: {dashboard_id}")
                return False
            
            # Add widget
            dashboard.widgets.append(widget_config)
            dashboard.updated_at = datetime.now()
            
            # Save updated dashboard
            success = self.database_manager.save_dashboard(dashboard)
            
            if success:
                logger.info(f"✅ Widget added to dashboard: {dashboard_id}")
            else:
                logger.error(f"❌ Failed to save dashboard with new widget: {dashboard_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Failed to add widget to dashboard: {e}")
            return False
    
    def remove_widget_from_dashboard(
        self, 
        dashboard_id: str, 
        widget_id: str
    ) -> bool:
        """
        Remove a widget from a dashboard.
        
        Args:
            dashboard_id: ID of the dashboard
            widget_id: ID of the widget to remove
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"📊 Removing widget from dashboard: {dashboard_id}")
            
            # Load dashboard
            dashboard = self.database_manager.load_dashboard(dashboard_id)
            if not dashboard:
                logger.warning(f"⚠️ Dashboard not found: {dashboard_id}")
                return False
            
            # Remove widget
            dashboard.widgets = [
                widget for widget in dashboard.widgets 
                if widget.get('id') != widget_id
            ]
            dashboard.updated_at = datetime.now()
            
            # Save updated dashboard
            success = self.database_manager.save_dashboard(dashboard)
            
            if success:
                logger.info(f"✅ Widget removed from dashboard: {dashboard_id}")
            else:
                logger.error(f"❌ Failed to save dashboard after widget removal: {dashboard_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Failed to remove widget from dashboard: {e}")
            return False
    
    def _generate_widget_data(self, widget: Dict[str, Any]) -> Dict[str, Any]:
        """Generate data for a specific widget."""
        try:
            widget_type = widget.get('type', 'metric')
            data_source = widget.get('data_source', '')
            config = widget.get('config', {})
            
            if widget_type == 'metric':
                return self._generate_metrics_data(data_source, config)
            elif widget_type == 'chart':
                return self._generate_chart_data(data_source, config)
            elif widget_type == 'table':
                return self._generate_table_data(data_source, config)
            elif widget_type == 'text':
                return self._generate_text_data(data_source, config)
            else:
                logger.warning(f"⚠️ Unknown widget type: {widget_type}")
                return {"error": f"Unknown widget type: {widget_type}"}
                
        except Exception as e:
            logger.error(f"❌ Failed to generate widget data: {e}")
            return {"error": str(e)}
    
    def _generate_metrics_data(self, data_source: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate metrics widget data."""
        try:
            # Get database statistics
            db_stats = self.database_manager.get_database_stats()
            
            # Generate metrics based on data source
            if data_source == 'reports':
                return {
                    "type": "metric",
                    "value": db_stats.get('reports_count', 0),
                    "label": "Total Reports",
                    "trend": "+5%",
                    "trend_direction": "up"
                }
            elif data_source == 'dashboards':
                return {
                    "type": "metric",
                    "value": db_stats.get('dashboards_count', 0),
                    "label": "Total Dashboards",
                    "trend": "+2%",
                    "trend_direction": "up"
                }
            elif data_source == 'trends':
                return {
                    "type": "metric",
                    "value": db_stats.get('trends_count', 0),
                    "label": "Active Trends",
                    "trend": "+10%",
                    "trend_direction": "up"
                }
            else:
                return {
                    "type": "metric",
                    "value": 0,
                    "label": "Unknown Metric",
                    "trend": "0%",
                    "trend_direction": "stable"
                }
                
        except Exception as e:
            logger.error(f"❌ Failed to generate metrics data: {e}")
            return {"error": str(e)}
    
    def _generate_chart_data(self, data_source: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate chart widget data."""
        try:
            # Load data for charts
            all_reports = self.database_manager.load_all_reports()
            all_dashboards = self.database_manager.load_all_dashboards()
            
            if data_source == 'reports_over_time':
                # Group reports by date
                reports_by_date = {}
                for report in all_reports:
                    date_str = report.generated_at.strftime("%Y-%m-%d")
                    reports_by_date[date_str] = reports_by_date.get(date_str, 0) + 1
                
                return {
                    "type": "line_chart",
                    "title": "Reports Over Time",
                    "x_axis": "Date",
                    "y_axis": "Number of Reports",
                    "data": reports_by_date
                }
            
            elif data_source == 'report_types':
                # Count reports by type
                report_types = {}
                for report in all_reports:
                    report_type = report.report_type
                    report_types[report_type] = report_types.get(report_type, 0) + 1
                
                return {
                    "type": "pie_chart",
                    "title": "Report Types Distribution",
                    "data": report_types
                }
            
            elif data_source == 'dashboard_activity':
                # Group dashboards by date
                dashboards_by_date = {}
                for dashboard in all_dashboards:
                    date_str = dashboard.updated_at.strftime("%Y-%m-%d")
                    dashboards_by_date[date_str] = dashboards_by_date.get(date_str, 0) + 1
                
                return {
                    "type": "bar_chart",
                    "title": "Dashboard Activity",
                    "x_axis": "Date",
                    "y_axis": "Number of Dashboards",
                    "data": dashboards_by_date
                }
            
            else:
                return {
                    "type": "chart",
                    "title": "Unknown Chart",
                    "data": {}
                }
                
        except Exception as e:
            logger.error(f"❌ Failed to generate chart data: {e}")
            return {"error": str(e)}
    
    def _generate_table_data(self, data_source: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate table widget data."""
        try:
            # Load data for tables
            all_reports = self.database_manager.load_all_reports()
            all_dashboards = self.database_manager.load_all_dashboards()
            
            if data_source == 'recent_reports':
                # Get recent reports
                recent_reports = sorted(all_reports, key=lambda x: x.generated_at, reverse=True)[:10]
                
                table_data = []
                for report in recent_reports:
                    table_data.append({
                        "Title": report.title,
                        "Type": report.report_type,
                        "Generated": report.generated_at.strftime("%Y-%m-%d"),
                        "Author": report.author_name or "Unknown"
                    })
                
                return {
                    "type": "table",
                    "title": "Recent Reports",
                    "columns": ["Title", "Type", "Generated", "Author"],
                    "data": table_data
                }
            
            elif data_source == 'dashboard_list':
                # Get dashboard list
                table_data = []
                for dashboard in all_dashboards:
                    table_data.append({
                        "Name": dashboard.name,
                        "Description": dashboard.description,
                        "Widgets": len(dashboard.widgets),
                        "Updated": dashboard.updated_at.strftime("%Y-%m-%d")
                    })
                
                return {
                    "type": "table",
                    "title": "Dashboards",
                    "columns": ["Name", "Description", "Widgets", "Updated"],
                    "data": table_data
                }
            
            else:
                return {
                    "type": "table",
                    "title": "Unknown Table",
                    "columns": [],
                    "data": []
                }
                
        except Exception as e:
            logger.error(f"❌ Failed to generate table data: {e}")
            return {"error": str(e)}
    
    def _generate_text_data(self, data_source: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate text widget data."""
        try:
            if data_source == 'system_status':
                return {
                    "type": "text",
                    "title": "System Status",
                    "content": "All systems operational. Analytics running smoothly.",
                    "status": "success"
                }
            
            elif data_source == 'summary':
                db_stats = self.database_manager.get_database_stats()
                return {
                    "type": "text",
                    "title": "Analytics Summary",
                    "content": f"Total Reports: {db_stats.get('reports_count', 0)}, "
                              f"Total Dashboards: {db_stats.get('dashboards_count', 0)}, "
                              f"Active Trends: {db_stats.get('trends_count', 0)}",
                    "status": "info"
                }
            
            else:
                return {
                    "type": "text",
                    "title": "Information",
                    "content": "No specific information available.",
                    "status": "info"
                }
                
        except Exception as e:
            logger.error(f"❌ Failed to generate text data: {e}")
            return {"error": str(e)}
    
    def _get_default_widgets(self) -> List[Dict[str, Any]]:
        """Get default widget configurations."""
        return [
            {
                "id": str(uuid.uuid4()),
                "type": "metric",
                "title": "Total Reports",
                "data_source": "reports",
                "config": {},
                "position": {"x": 0, "y": 0, "width": 3, "height": 2},
                "refresh_interval": 60
            },
            {
                "id": str(uuid.uuid4()),
                "type": "metric",
                "title": "Total Dashboards",
                "data_source": "dashboards",
                "config": {},
                "position": {"x": 3, "y": 0, "width": 3, "height": 2},
                "refresh_interval": 60
            },
            {
                "id": str(uuid.uuid4()),
                "type": "chart",
                "title": "Reports Over Time",
                "data_source": "reports_over_time",
                "config": {},
                "position": {"x": 0, "y": 2, "width": 6, "height": 4},
                "refresh_interval": 300
            },
            {
                "id": str(uuid.uuid4()),
                "type": "table",
                "title": "Recent Reports",
                "data_source": "recent_reports",
                "config": {},
                "position": {"x": 0, "y": 6, "width": 6, "height": 4},
                "refresh_interval": 300
            },
            {
                "id": str(uuid.uuid4()),
                "type": "text",
                "title": "System Status",
                "data_source": "system_status",
                "config": {},
                "position": {"x": 6, "y": 0, "width": 3, "height": 2},
                "refresh_interval": 60
            }
        ]
    
    def _get_default_layout(self) -> Dict[str, Any]:
        """Get default dashboard layout."""
        return {
            "grid": {
                "columns": 12,
                "rows": 12,
                "cell_height": 50,
                "cell_width": 100
            },
            "background": "#f5f5f5",
            "padding": 10
        }
    
    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Get summary of all dashboards."""
        try:
            all_dashboards = self.database_manager.load_all_dashboards()
            
            summary = {
                "total_dashboards": len(all_dashboards),
                "public_dashboards": len([d for d in all_dashboards if d.is_public]),
                "private_dashboards": len([d for d in all_dashboards if not d.is_public]),
                "total_widgets": sum(len(d.widgets) for d in all_dashboards),
                "recent_dashboards": self._get_recent_dashboards(all_dashboards, 5)
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"❌ Failed to get dashboard summary: {e}")
            return {}
    
    def _get_recent_dashboards(self, dashboards: List[AnalyticsDashboard], limit: int) -> List[Dict[str, Any]]:
        """Get recent dashboards."""
        sorted_dashboards = sorted(dashboards, key=lambda x: x.updated_at, reverse=True)
        recent_dashboards = sorted_dashboards[:limit]
        
        return [
            {
                "id": dashboard.id,
                "name": dashboard.name,
                "description": dashboard.description,
                "updated_at": dashboard.updated_at.isoformat(),
                "widget_count": len(dashboard.widgets),
                "owner": dashboard.owner_id
            }
            for dashboard in recent_dashboards
        ] 