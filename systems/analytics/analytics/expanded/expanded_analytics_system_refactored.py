"""
Refactored Expanded Analytics System
===================================

Main orchestrator for the expanded analytics system using modular components.
This replaces the monolithic expanded_analytics_system.py with a clean, maintainable architecture.

FEATURES:
- Advanced reporting and data visualization
- Trend analysis and predictive analytics
- Comprehensive dashboards and insights
- Custom report generation
- Real-time analytics monitoring
- Export and sharing capabilities

MODULAR ARCHITECTURE:
- analytics_models.py: Data models and classes
- analytics_database.py: Database operations and management
- report_generator.py: Report generation and analysis
- dashboard_manager.py: Dashboard creation and management
- export_manager.py: Export functionality and file management
"""

import logging
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

from .analytics_models import (
    AnalyticsReport, AnalyticsDashboard, AnalyticsWidget,
    TrendAnalysis, PredictiveInsight, create_analytics_report,
    create_analytics_dashboard, create_analytics_widget
)
from .analytics_database import AnalyticsDatabaseManager
from .report_generator import ReportGenerator
from .dashboard_manager import DashboardManager
from .export_manager import ExportManager

logger = logging.getLogger(__name__)


class RefactoredExpandedAnalyticsSystem:
    """Refactored expanded analytics system using modular components."""
    
    def __init__(self, data_dir: str = "data/expanded_analytics"):
        """Initialize the refactored expanded analytics system."""
        logger.info("🔧 Initializing Refactored Expanded Analytics System")
        
        # Initialize database manager
        self.database_manager = AnalyticsDatabaseManager(data_dir)
        
        # Initialize component managers
        self.report_generator = ReportGenerator(self.database_manager)
        self.dashboard_manager = DashboardManager(self.database_manager)
        self.export_manager = ExportManager(self.database_manager)
        
        # System state
        self.initialized = True
        self.components = {
            "database_manager": self.database_manager,
            "report_generator": self.report_generator,
            "dashboard_manager": self.dashboard_manager,
            "export_manager": self.export_manager
        }
        
        logger.info("✅ Refactored Expanded Analytics System initialized successfully")
    
    # Report Operations
    def generate_comprehensive_report(
        self, 
        report_type: str = "comprehensive", 
        time_period: str = "30d",
        author_id: str = "", 
        author_name: str = ""
    ) -> AnalyticsReport:
        """
        Generate a comprehensive analytics report.
        
        Args:
            report_type: Type of report to generate
            time_period: Time period for analysis
            author_id: ID of the report author
            author_name: Name of the report author
            
        Returns:
            AnalyticsReport object
        """
        try:
            logger.info(f"📊 Generating comprehensive report: {report_type}")
            return self.report_generator.generate_comprehensive_report(
                report_type, time_period, author_id, author_name
            )
        except Exception as e:
            logger.error(f"❌ Failed to generate comprehensive report: {e}")
            raise
    
    def get_report(self, report_id: str) -> Optional[AnalyticsReport]:
        """Get a specific report by ID."""
        try:
            return self.database_manager.load_report(report_id)
        except Exception as e:
            logger.error(f"❌ Failed to get report {report_id}: {e}")
            return None
    
    def get_all_reports(self) -> List[AnalyticsReport]:
        """Get all reports."""
        try:
            return self.database_manager.load_all_reports()
        except Exception as e:
            logger.error(f"❌ Failed to get all reports: {e}")
            return []
    
    def save_report(self, report: AnalyticsReport) -> bool:
        """Save a report."""
        try:
            return self.database_manager.save_report(report)
        except Exception as e:
            logger.error(f"❌ Failed to save report: {e}")
            return False
    
    def delete_report(self, report_id: str) -> bool:
        """Delete a report."""
        try:
            return self.database_manager.delete_report(report_id)
        except Exception as e:
            logger.error(f"❌ Failed to delete report: {e}")
            return False
    
    # Dashboard Operations
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
            return self.dashboard_manager.create_dashboard(name, description, owner_id, widgets)
        except Exception as e:
            logger.error(f"❌ Failed to create dashboard: {e}")
            raise
    
    def get_dashboard(self, dashboard_id: str) -> Optional[AnalyticsDashboard]:
        """Get a specific dashboard by ID."""
        try:
            return self.database_manager.load_dashboard(dashboard_id)
        except Exception as e:
            logger.error(f"❌ Failed to get dashboard {dashboard_id}: {e}")
            return None
    
    def get_dashboard_data(self, dashboard_id: str) -> Dict[str, Any]:
        """Get dashboard data with widget data populated."""
        try:
            return self.dashboard_manager.get_dashboard_data(dashboard_id)
        except Exception as e:
            logger.error(f"❌ Failed to get dashboard data: {e}")
            return {}
    
    def get_all_dashboards(self) -> List[AnalyticsDashboard]:
        """Get all dashboards."""
        try:
            return self.database_manager.load_all_dashboards()
        except Exception as e:
            logger.error(f"❌ Failed to get all dashboards: {e}")
            return []
    
    def update_dashboard(self, dashboard_id: str, updates: Dict[str, Any]) -> bool:
        """Update a dashboard."""
        try:
            return self.dashboard_manager.update_dashboard(dashboard_id, updates)
        except Exception as e:
            logger.error(f"❌ Failed to update dashboard: {e}")
            return False
    
    def delete_dashboard(self, dashboard_id: str) -> bool:
        """Delete a dashboard."""
        try:
            return self.dashboard_manager.delete_dashboard(dashboard_id)
        except Exception as e:
            logger.error(f"❌ Failed to delete dashboard: {e}")
            return False
    
    def add_widget_to_dashboard(self, dashboard_id: str, widget_config: Dict[str, Any]) -> bool:
        """Add a widget to a dashboard."""
        try:
            return self.dashboard_manager.add_widget_to_dashboard(dashboard_id, widget_config)
        except Exception as e:
            logger.error(f"❌ Failed to add widget to dashboard: {e}")
            return False
    
    def remove_widget_from_dashboard(self, dashboard_id: str, widget_id: str) -> bool:
        """Remove a widget from a dashboard."""
        try:
            return self.dashboard_manager.remove_widget_from_dashboard(dashboard_id, widget_id)
        except Exception as e:
            logger.error(f"❌ Failed to remove widget from dashboard: {e}")
            return False
    
    # Export Operations
    def export_report(self, report_id: str, format_type: str = "json") -> str:
        """
        Export a report in the specified format.
        
        Args:
            report_id: ID of the report to export
            format_type: Export format ("json", "csv", "html")
            
        Returns:
            Path to the exported file
        """
        try:
            return self.export_manager.export_report(report_id, format_type)
        except Exception as e:
            logger.error(f"❌ Failed to export report: {e}")
            return ""
    
    def export_dashboard(self, dashboard_id: str, format_type: str = "json") -> str:
        """
        Export a dashboard in the specified format.
        
        Args:
            dashboard_id: ID of the dashboard to export
            format_type: Export format ("json", "html")
            
        Returns:
            Path to the exported file
        """
        try:
            return self.export_manager.export_dashboard(dashboard_id, format_type)
        except Exception as e:
            logger.error(f"❌ Failed to export dashboard: {e}")
            return ""
    
    # Trend Analysis Operations
    def analyze_trend(self, metric: str, period: str) -> Optional[TrendAnalysis]:
        """Analyze trend for a specific metric."""
        try:
            return self.report_generator._analyze_trend(metric, period)
        except Exception as e:
            logger.error(f"❌ Failed to analyze trend: {e}")
            return None
    
    def get_trends(self) -> List[TrendAnalysis]:
        """Get all trend analyses."""
        try:
            return self.database_manager.load_trends()
        except Exception as e:
            logger.error(f"❌ Failed to get trends: {e}")
            return []
    
    # System Information
    def get_system_status(self) -> Dict[str, Any]:
        """Get the current status of the analytics system."""
        try:
            db_stats = self.database_manager.get_database_stats()
            export_summary = self.export_manager.get_export_summary()
            
            return {
                "system": "Refactored Expanded Analytics System",
                "status": "operational" if self.initialized else "initializing",
                "initialized": self.initialized,
                "components": {
                    "database_manager": True,
                    "report_generator": True,
                    "dashboard_manager": True,
                    "export_manager": True
                },
                "statistics": db_stats,
                "exports": export_summary,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ Failed to get system status: {e}")
            return {"status": "error", "error": str(e)}
    
    def get_reports_summary(self) -> Dict[str, Any]:
        """Get summary of all reports."""
        try:
            return self.report_generator.get_reports_summary()
        except Exception as e:
            logger.error(f"❌ Failed to get reports summary: {e}")
            return {}
    
    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Get summary of all dashboards."""
        try:
            return self.dashboard_manager.get_dashboard_summary()
        except Exception as e:
            logger.error(f"❌ Failed to get dashboard summary: {e}")
            return {}
    
    def get_export_summary(self) -> Dict[str, Any]:
        """Get summary of export operations."""
        try:
            return self.export_manager.get_export_summary()
        except Exception as e:
            logger.error(f"❌ Failed to get export summary: {e}")
            return {}
    
    # Utility Operations
    def cleanup_old_data(self, days_old: int = 90) -> int:
        """Clean up old data from the system."""
        try:
            db_cleanup = self.database_manager.cleanup_old_data(days_old)
            export_cleanup = self.export_manager.cleanup_old_exports(days_old)
            return db_cleanup + export_cleanup
        except Exception as e:
            logger.error(f"❌ Failed to cleanup old data: {e}")
            return 0
    
    def get_component(self, component_name: str):
        """Get a specific component by name."""
        return self.components.get(component_name)
    
    def test_system(self) -> Dict[str, Any]:
        """Test all system components."""
        try:
            logger.info("🧪 Testing Refactored Expanded Analytics System")
            
            test_results = {
                "database_manager": False,
                "report_generator": False,
                "dashboard_manager": False,
                "export_manager": False,
                "overall": False
            }
            
            # Test database manager
            try:
                db_stats = self.database_manager.get_database_stats()
                test_results["database_manager"] = True
                logger.info("✅ Database manager test passed")
            except Exception as e:
                logger.error(f"❌ Database manager test failed: {e}")
            
            # Test report generator
            try:
                # Create a test report
                test_report = create_analytics_report(
                    "Test Report",
                    "test",
                    "7d",
                    "test_user",
                    "Test User"
                )
                test_results["report_generator"] = True
                logger.info("✅ Report generator test passed")
            except Exception as e:
                logger.error(f"❌ Report generator test failed: {e}")
            
            # Test dashboard manager
            try:
                # Create a test dashboard
                test_dashboard = create_analytics_dashboard(
                    "Test Dashboard",
                    "Test dashboard for system testing",
                    "test_user"
                )
                test_results["dashboard_manager"] = True
                logger.info("✅ Dashboard manager test passed")
            except Exception as e:
                logger.error(f"❌ Dashboard manager test failed: {e}")
            
            # Test export manager
            try:
                export_summary = self.export_manager.get_export_summary()
                test_results["export_manager"] = True
                logger.info("✅ Export manager test passed")
            except Exception as e:
                logger.error(f"❌ Export manager test failed: {e}")
            
            # Overall test result
            test_results["overall"] = all([
                test_results["database_manager"],
                test_results["report_generator"],
                test_results["dashboard_manager"],
                test_results["export_manager"]
            ])
            
            logger.info(f"🧪 System test completed: {'PASSED' if test_results['overall'] else 'FAILED'}")
            return test_results
            
        except Exception as e:
            logger.error(f"❌ System test failed: {e}")
            return {"overall": False, "error": str(e)}
    
    def shutdown(self):
        """Shutdown the analytics system."""
        try:
            logger.info("🔄 Shutting down Refactored Expanded Analytics System")
            
            # Perform cleanup
            self.cleanup_old_data()
            
            # Mark as not initialized
            self.initialized = False
            
            logger.info("✅ Refactored Expanded Analytics System shutdown completed")
            
        except Exception as e:
            logger.error(f"❌ Failed to shutdown system: {e}")


# Convenience function to get a system instance
def get_expanded_analytics_system(data_dir: str = "data/expanded_analytics") -> RefactoredExpandedAnalyticsSystem:
    """
    Get a new instance of the refactored expanded analytics system.
    
    Args:
        data_dir: Directory for storing analytics data
        
    Returns:
        RefactoredExpandedAnalyticsSystem instance
    """
    return RefactoredExpandedAnalyticsSystem(data_dir) 