"""
Export Manager
=============

Export functionality for reports and dashboards in the expanded analytics system.
This component handles multiple export formats and file management.

Extracted from expanded_analytics_system.py for better modularity and maintainability.
"""

import json
import csv
import logging
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from io import StringIO
import uuid

from .analytics_models import AnalyticsReport, AnalyticsDashboard, AnalyticsExport
from .analytics_database import AnalyticsDatabaseManager

logger = logging.getLogger(__name__)


class ExportManager:
    """Manages export operations for analytics reports and dashboards."""
    
    def __init__(self, database_manager: AnalyticsDatabaseManager, export_dir: str = "outputs/analytics_exports"):
        """Initialize the export manager."""
        self.database_manager = database_manager
        self.export_dir = Path(export_dir)
        self.export_dir.mkdir(parents=True, exist_ok=True)
    
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
            logger.info(f"📤 Exporting report {report_id} in {format_type} format")
            
            # Load report
            report = self.database_manager.load_report(report_id)
            if not report:
                logger.warning(f"⚠️ Report not found: {report_id}")
                return ""
            
            # Generate export based on format
            if format_type == "json":
                export_path = self._export_report_json(report)
            elif format_type == "csv":
                export_path = self._export_report_csv(report)
            elif format_type == "html":
                export_path = self._export_report_html(report)
            else:
                logger.error(f"❌ Unsupported export format: {format_type}")
                return ""
            
            # Record export
            self._record_export(report_id, "report", format_type, export_path)
            
            logger.info(f"✅ Report exported: {export_path}")
            return export_path
            
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
            logger.info(f"📤 Exporting dashboard {dashboard_id} in {format_type} format")
            
            # Load dashboard
            dashboard = self.database_manager.load_dashboard(dashboard_id)
            if not dashboard:
                logger.warning(f"⚠️ Dashboard not found: {dashboard_id}")
                return ""
            
            # Generate export based on format
            if format_type == "json":
                export_path = self._export_dashboard_json(dashboard)
            elif format_type == "html":
                export_path = self._export_dashboard_html(dashboard)
            else:
                logger.error(f"❌ Unsupported export format for dashboard: {format_type}")
                return ""
            
            # Record export
            self._record_export(dashboard_id, "dashboard", format_type, export_path)
            
            logger.info(f"✅ Dashboard exported: {export_path}")
            return export_path
            
        except Exception as e:
            logger.error(f"❌ Failed to export dashboard: {e}")
            return ""
    
    def _export_report_json(self, report: AnalyticsReport) -> str:
        """Export report as JSON."""
        try:
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{report.id}_{timestamp}.json"
            export_path = self.export_dir / filename
            
            # Export report data
            report_data = report.to_dict()
            
            # Add export metadata
            export_data = {
                "export_info": {
                    "exported_at": datetime.now().isoformat(),
                    "format": "json",
                    "version": "1.0"
                },
                "report": report_data
            }
            
            # Write to file
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            return str(export_path)
            
        except Exception as e:
            logger.error(f"❌ Failed to export report as JSON: {e}")
            return ""
    
    def _export_report_csv(self, report: AnalyticsReport) -> str:
        """Export report as CSV."""
        try:
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{report.id}_{timestamp}.csv"
            export_path = self.export_dir / filename
            
            # Prepare CSV data
            csv_data = []
            
            # Report metadata
            csv_data.append(["Report Information"])
            csv_data.append(["ID", report.id])
            csv_data.append(["Title", report.title])
            csv_data.append(["Type", report.report_type])
            csv_data.append(["Generated At", report.generated_at.isoformat()])
            csv_data.append(["Time Period", report.time_period])
            csv_data.append(["Author", report.author_name])
            csv_data.append([])
            
            # Data summary
            csv_data.append(["Data Summary"])
            for key, value in report.data_summary.items():
                if isinstance(value, dict):
                    csv_data.append([key, json.dumps(value)])
                else:
                    csv_data.append([key, str(value)])
            csv_data.append([])
            
            # Insights
            csv_data.append(["Insights"])
            for i, insight in enumerate(report.insights, 1):
                csv_data.append([f"Insight {i}", insight.get('title', '')])
                csv_data.append([f"Description {i}", insight.get('description', '')])
                csv_data.append([f"Type {i}", insight.get('type', '')])
                csv_data.append([f"Impact {i}", insight.get('impact', '')])
                csv_data.append([])
            
            # Recommendations
            csv_data.append(["Recommendations"])
            for i, recommendation in enumerate(report.recommendations, 1):
                csv_data.append([f"Recommendation {i}", recommendation])
            csv_data.append([])
            
            # Charts data
            csv_data.append(["Charts Data"])
            for chart_name, chart_data in report.charts_data.items():
                csv_data.append([f"Chart: {chart_name}", json.dumps(chart_data)])
            
            # Write to file
            with open(export_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(csv_data)
            
            return str(export_path)
            
        except Exception as e:
            logger.error(f"❌ Failed to export report as CSV: {e}")
            return ""
    
    def _export_report_html(self, report: AnalyticsReport) -> str:
        """Export report as HTML."""
        try:
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{report.id}_{timestamp}.html"
            export_path = self.export_dir / filename
            
            # Generate HTML content
            html_content = self._generate_report_html(report)
            
            # Write to file
            with open(export_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return str(export_path)
            
        except Exception as e:
            logger.error(f"❌ Failed to export report as HTML: {e}")
            return ""
    
    def _export_dashboard_json(self, dashboard: AnalyticsDashboard) -> str:
        """Export dashboard as JSON."""
        try:
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"dashboard_{dashboard.id}_{timestamp}.json"
            export_path = self.export_dir / filename
            
            # Export dashboard data
            dashboard_data = dashboard.to_dict()
            
            # Add export metadata
            export_data = {
                "export_info": {
                    "exported_at": datetime.now().isoformat(),
                    "format": "json",
                    "version": "1.0"
                },
                "dashboard": dashboard_data
            }
            
            # Write to file
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            return str(export_path)
            
        except Exception as e:
            logger.error(f"❌ Failed to export dashboard as JSON: {e}")
            return ""
    
    def _export_dashboard_html(self, dashboard: AnalyticsDashboard) -> str:
        """Export dashboard as HTML."""
        try:
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"dashboard_{dashboard.id}_{timestamp}.html"
            export_path = self.export_dir / filename
            
            # Generate HTML content
            html_content = self._generate_dashboard_html(dashboard)
            
            # Write to file
            with open(export_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return str(export_path)
            
        except Exception as e:
            logger.error(f"❌ Failed to export dashboard as HTML: {e}")
            return ""
    
    def _generate_report_html(self, report: AnalyticsReport) -> str:
        """Generate HTML content for a report."""
        html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{report.title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .header {{
            border-bottom: 2px solid #007bff;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .section {{
            margin-bottom: 30px;
        }}
        .section h2 {{
            color: #007bff;
            border-bottom: 1px solid #ddd;
            padding-bottom: 5px;
        }}
        .insight {{
            background-color: #f8f9fa;
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #007bff;
            border-radius: 4px;
        }}
        .recommendation {{
            background-color: #e7f3ff;
            padding: 10px;
            margin: 5px 0;
            border-radius: 4px;
        }}
        .metadata {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            font-size: 0.9em;
        }}
        .chart-placeholder {{
            background-color: #f8f9fa;
            padding: 20px;
            text-align: center;
            border: 2px dashed #ddd;
            border-radius: 4px;
            margin: 10px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{report.title}</h1>
            <div class="metadata">
                <strong>Generated:</strong> {report.generated_at.strftime('%Y-%m-%d %H:%M:%S')}<br>
                <strong>Time Period:</strong> {report.time_period}<br>
                <strong>Author:</strong> {report.author_name or 'Unknown'}<br>
                <strong>Type:</strong> {report.report_type}
            </div>
        </div>
        
        <div class="section">
            <h2>Data Summary</h2>
            <div class="metadata">
                {self._format_data_summary_html(report.data_summary)}
            </div>
        </div>
        
        <div class="section">
            <h2>Insights</h2>
            {self._format_insights_html(report.insights)}
        </div>
        
        <div class="section">
            <h2>Recommendations</h2>
            {self._format_recommendations_html(report.recommendations)}
        </div>
        
        <div class="section">
            <h2>Charts</h2>
            {self._format_charts_html(report.charts_data)}
        </div>
    </div>
</body>
</html>
        """
        return html_template
    
    def _generate_dashboard_html(self, dashboard: AnalyticsDashboard) -> str:
        """Generate HTML content for a dashboard."""
        html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{dashboard.name}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .header {{
            border-bottom: 2px solid #28a745;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .widget {{
            background-color: #f8f9fa;
            padding: 15px;
            margin: 10px 0;
            border-radius: 4px;
            border: 1px solid #ddd;
        }}
        .widget h3 {{
            color: #28a745;
            margin-top: 0;
        }}
        .metadata {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{dashboard.name}</h1>
            <p>{dashboard.description}</p>
            <div class="metadata">
                <strong>Created:</strong> {dashboard.created_at.strftime('%Y-%m-%d %H:%M:%S')}<br>
                <strong>Updated:</strong> {dashboard.updated_at.strftime('%Y-%m-%d %H:%M:%S')}<br>
                <strong>Owner:</strong> {dashboard.owner_id or 'Unknown'}<br>
                <strong>Widgets:</strong> {len(dashboard.widgets)}
            </div>
        </div>
        
        <div class="section">
            <h2>Widgets</h2>
            {self._format_widgets_html(dashboard.widgets)}
        </div>
    </div>
</body>
</html>
        """
        return html_template
    
    def _format_data_summary_html(self, data_summary: Dict[str, Any]) -> str:
        """Format data summary for HTML."""
        html = ""
        for key, value in data_summary.items():
            if isinstance(value, dict):
                html += f"<strong>{key}:</strong><br>"
                for sub_key, sub_value in value.items():
                    html += f"&nbsp;&nbsp;{sub_key}: {sub_value}<br>"
            else:
                html += f"<strong>{key}:</strong> {value}<br>"
        return html
    
    def _format_insights_html(self, insights: List[Dict[str, Any]]) -> str:
        """Format insights for HTML."""
        html = ""
        for insight in insights:
            html += f"""
            <div class="insight">
                <h3>{insight.get('title', 'Insight')}</h3>
                <p>{insight.get('description', '')}</p>
                <small>Type: {insight.get('type', '')} | Impact: {insight.get('impact', '')}</small>
            </div>
            """
        return html
    
    def _format_recommendations_html(self, recommendations: List[str]) -> str:
        """Format recommendations for HTML."""
        html = ""
        for recommendation in recommendations:
            html += f'<div class="recommendation">• {recommendation}</div>'
        return html
    
    def _format_charts_html(self, charts_data: Dict[str, Any]) -> str:
        """Format charts data for HTML."""
        html = ""
        for chart_name, chart_data in charts_data.items():
            html += f"""
            <div class="chart-placeholder">
                <h3>{chart_name}</h3>
                <p>Chart data available: {len(chart_data)} data points</p>
                <small>Chart visualization would be rendered here</small>
            </div>
            """
        return html
    
    def _format_widgets_html(self, widgets: List[Dict[str, Any]]) -> str:
        """Format widgets for HTML."""
        html = ""
        for widget in widgets:
            html += f"""
            <div class="widget">
                <h3>{widget.get('title', 'Widget')}</h3>
                <p>Type: {widget.get('type', 'Unknown')}</p>
                <p>Data Source: {widget.get('data_source', 'Unknown')}</p>
                <small>Widget data would be rendered here</small>
            </div>
            """
        return html
    
    def _record_export(self, resource_id: str, resource_type: str, format_type: str, export_path: str):
        """Record export operation."""
        try:
            # Calculate file size and checksum
            file_size = Path(export_path).stat().st_size if Path(export_path).exists() else 0
            
            checksum = ""
            if Path(export_path).exists():
                with open(export_path, 'rb') as f:
                    checksum = hashlib.md5(f.read()).hexdigest()
            
            # Create export record
            export_record = AnalyticsExport(
                id=str(uuid.uuid4()),
                resource_id=resource_id,
                resource_type=resource_type,
                format_type=format_type,
                export_path=export_path,
                file_size=file_size,
                checksum=checksum
            )
            
            # Save to database (if export database is available)
            # Note: This would require adding export table to the database manager
            logger.info(f"📝 Export recorded: {export_record.id}")
            
        except Exception as e:
            logger.error(f"❌ Failed to record export: {e}")
    
    def get_export_summary(self) -> Dict[str, Any]:
        """Get summary of export operations."""
        try:
            # Count export files
            export_files = list(self.export_dir.glob("*"))
            
            # Group by format
            formats = {}
            for file_path in export_files:
                if file_path.is_file():
                    ext = file_path.suffix.lower()
                    formats[ext] = formats.get(ext, 0) + 1
            
            summary = {
                "total_exports": len(export_files),
                "exports_by_format": formats,
                "export_directory": str(self.export_dir)
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"❌ Failed to get export summary: {e}")
            return {}
    
    def cleanup_old_exports(self, days_old: int = 30) -> int:
        """Clean up old export files."""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_old)
            deleted_count = 0
            
            for file_path in self.export_dir.glob("*"):
                if file_path.is_file():
                    file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if file_mtime < cutoff_date:
                        file_path.unlink()
                        deleted_count += 1
            
            logger.info(f"✅ Cleaned up {deleted_count} old export files")
            return deleted_count
            
        except Exception as e:
            logger.error(f"❌ Failed to cleanup old exports: {e}")
            return 0 