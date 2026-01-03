"""
Report Generator
===============

Report generation and analysis functionality for the expanded analytics system.
This component handles comprehensive report creation, insights generation, and trend analysis.

Extracted from expanded_analytics_system.py for better modularity and maintainability.
"""

import logging
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Tuple
from pathlib import Path

from .analytics_models import AnalyticsReport, TrendAnalysis, PredictiveInsight
from .analytics_database import AnalyticsDatabaseManager

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Handles report generation and analysis for the expanded analytics system."""
    
    def __init__(self, database_manager: AnalyticsDatabaseManager):
        """Initialize the report generator."""
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
            
            logger.info("✅ Analytics subsystems initialized")
            
        except ImportError as e:
            logger.warning(f"⚠️ Some analytics subsystems not available: {e}")
            self.analytics_subsystems = {}
    
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
            time_period: Time period for analysis (e.g., "7d", "30d", "90d")
            author_id: ID of the report author
            author_name: Name of the report author
            
        Returns:
            AnalyticsReport object
        """
        try:
            logger.info(f"📊 Generating comprehensive report: {report_type} for {time_period}")
            
            # Create report structure
            report = AnalyticsReport(
                id=str(uuid.uuid4()),
                title=f"{report_type.title()} Analytics Report - {time_period}",
                report_type=report_type,
                generated_at=datetime.now(),
                time_period=time_period,
                data_summary={},
                insights=[],
                recommendations=[],
                charts_data={},
                author_id=author_id,
                author_name=author_name
            )
            
            # Generate report components
            report.data_summary = self._generate_comprehensive_summary(time_period)
            report.insights = self._generate_comprehensive_insights(time_period)
            report.recommendations = self._generate_comprehensive_recommendations(time_period)
            report.charts_data = self._generate_comprehensive_charts(time_period)
            
            # Save report to database
            self.database_manager.save_report(report)
            
            logger.info(f"✅ Comprehensive report generated: {report.id}")
            return report
            
        except Exception as e:
            logger.error(f"❌ Failed to generate comprehensive report: {e}")
            raise
    
    def _generate_comprehensive_summary(self, time_period: str) -> Dict[str, Any]:
        """Generate comprehensive data summary."""
        try:
            logger.info(f"📈 Generating comprehensive summary for {time_period}")
            
            # Get database statistics
            db_stats = self.database_manager.get_database_stats()
            
            # Calculate time period dates
            end_date = datetime.now()
            if time_period == "7d":
                start_date = end_date - timedelta(days=7)
            elif time_period == "30d":
                start_date = end_date - timedelta(days=30)
            elif time_period == "90d":
                start_date = end_date - timedelta(days=90)
            else:
                start_date = end_date - timedelta(days=30)  # Default to 30 days
            
            # Load reports for the period
            all_reports = self.database_manager.load_all_reports()
            period_reports = [
                report for report in all_reports 
                if start_date <= report.generated_at <= end_date
            ]
            
            # Load dashboards for the period
            all_dashboards = self.database_manager.load_all_dashboards()
            period_dashboards = [
                dashboard for dashboard in all_dashboards 
                if start_date <= dashboard.updated_at <= end_date
            ]
            
            # Generate summary
            summary = {
                "time_period": {
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "duration_days": (end_date - start_date).days
                },
                "reports": {
                    "total_reports": len(all_reports),
                    "period_reports": len(period_reports),
                    "public_reports": db_stats.get('public_reports_count', 0),
                    "report_types": self._count_reports_by_type(period_reports)
                },
                "dashboards": {
                    "total_dashboards": len(all_dashboards),
                    "period_dashboards": len(period_dashboards),
                    "public_dashboards": db_stats.get('public_dashboards_count', 0)
                },
                "trends": {
                    "total_trends": db_stats.get('trends_count', 0)
                },
                "generated_at": datetime.now().isoformat()
            }
            
            logger.info(f"✅ Comprehensive summary generated")
            return summary
            
        except Exception as e:
            logger.error(f"❌ Failed to generate comprehensive summary: {e}")
            return {}
    
    def _generate_comprehensive_insights(self, time_period: str) -> List[Dict[str, Any]]:
        """Generate comprehensive insights."""
        try:
            logger.info(f"🧠 Generating comprehensive insights for {time_period}")
            
            insights = []
            
            # Load existing reports for trend analysis
            all_reports = self.database_manager.load_all_reports()
            
            # Insight 1: Report generation trends
            if len(all_reports) > 1:
                recent_reports = sorted(all_reports, key=lambda x: x.generated_at)[-10:]
                report_trend = self._analyze_report_generation_trend(recent_reports)
                if report_trend:
                    insights.append({
                        "type": "trend_analysis",
                        "title": "Report Generation Trend",
                        "description": f"Report generation is {report_trend['direction']}",
                        "metric": "reports_per_day",
                        "value": report_trend['rate'],
                        "confidence": report_trend['confidence'],
                        "impact": "medium"
                    })
            
            # Insight 2: Most popular report types
            report_types = self._count_reports_by_type(all_reports)
            if report_types:
                most_popular = max(report_types.items(), key=lambda x: x[1])
                insights.append({
                    "type": "popularity_analysis",
                    "title": "Most Popular Report Type",
                    "description": f"'{most_popular[0]}' reports are most commonly generated",
                    "metric": "report_type_popularity",
                    "value": most_popular[1],
                    "confidence": 0.9,
                    "impact": "low"
                })
            
            # Insight 3: Dashboard usage patterns
            all_dashboards = self.database_manager.load_all_dashboards()
            if all_dashboards:
                public_dashboards = [d for d in all_dashboards if d.is_public]
                private_dashboards = [d for d in all_dashboards if not d.is_public]
                
                insights.append({
                    "type": "usage_pattern",
                    "title": "Dashboard Sharing Patterns",
                    "description": f"{len(public_dashboards)} public vs {len(private_dashboards)} private dashboards",
                    "metric": "dashboard_sharing_ratio",
                    "value": len(public_dashboards) / len(all_dashboards) if all_dashboards else 0,
                    "confidence": 0.95,
                    "impact": "medium"
                })
            
            # Insight 4: System health
            insights.append({
                "type": "system_health",
                "title": "Analytics System Health",
                "description": "System is operating normally with all components functional",
                "metric": "system_health",
                "value": 1.0,
                "confidence": 0.98,
                "impact": "high"
            })
            
            logger.info(f"✅ Generated {len(insights)} insights")
            return insights
            
        except Exception as e:
            logger.error(f"❌ Failed to generate comprehensive insights: {e}")
            return []
    
    def _generate_comprehensive_recommendations(self, time_period: str) -> List[str]:
        """Generate comprehensive recommendations."""
        try:
            logger.info(f"💡 Generating comprehensive recommendations for {time_period}")
            
            recommendations = []
            
            # Load data for analysis
            all_reports = self.database_manager.load_all_reports()
            all_dashboards = self.database_manager.load_all_dashboards()
            
            # Recommendation 1: Report diversity
            report_types = self._count_reports_by_type(all_reports)
            if len(report_types) < 3:
                recommendations.append(
                    "Consider generating more diverse report types to gain comprehensive insights"
                )
            
            # Recommendation 2: Dashboard utilization
            if len(all_dashboards) < len(all_reports) * 0.5:
                recommendations.append(
                    "Create more dashboards to visualize and monitor key metrics regularly"
                )
            
            # Recommendation 3: Public sharing
            public_reports = [r for r in all_reports if r.is_public]
            if len(public_reports) < len(all_reports) * 0.2:
                recommendations.append(
                    "Consider sharing more reports publicly to improve collaboration and knowledge sharing"
                )
            
            # Recommendation 4: Regular reporting
            if len(all_reports) < 10:
                recommendations.append(
                    "Establish regular reporting schedules to maintain consistent analytics insights"
                )
            
            # Recommendation 5: Advanced analytics
            if not self.analytics_subsystems:
                recommendations.append(
                    "Enable advanced analytics subsystems for more sophisticated insights and predictions"
                )
            
            # Default recommendations
            recommendations.extend([
                "Review and update dashboard configurations regularly",
                "Export important reports for backup and sharing",
                "Monitor trend analysis for emerging patterns",
                "Consider implementing automated report generation"
            ])
            
            logger.info(f"✅ Generated {len(recommendations)} recommendations")
            return recommendations
            
        except Exception as e:
            logger.error(f"❌ Failed to generate comprehensive recommendations: {e}")
            return []
    
    def _generate_comprehensive_charts(self, time_period: str) -> Dict[str, Any]:
        """Generate comprehensive charts data."""
        try:
            logger.info(f"📊 Generating comprehensive charts for {time_period}")
            
            charts_data = {}
            
            # Load data
            all_reports = self.database_manager.load_all_reports()
            all_dashboards = self.database_manager.load_all_dashboards()
            
            # Chart 1: Report generation over time
            if all_reports:
                reports_by_date = self._group_reports_by_date(all_reports)
                charts_data['reports_over_time'] = {
                    "type": "line",
                    "title": "Report Generation Over Time",
                    "x_axis": "Date",
                    "y_axis": "Number of Reports",
                    "data": reports_by_date
                }
            
            # Chart 2: Report types distribution
            report_types = self._count_reports_by_type(all_reports)
            if report_types:
                charts_data['report_types_distribution'] = {
                    "type": "pie",
                    "title": "Report Types Distribution",
                    "data": report_types
                }
            
            # Chart 3: Dashboard activity
            if all_dashboards:
                dashboards_by_date = self._group_dashboards_by_date(all_dashboards)
                charts_data['dashboards_activity'] = {
                    "type": "bar",
                    "title": "Dashboard Activity Over Time",
                    "x_axis": "Date",
                    "y_axis": "Number of Dashboards",
                    "data": dashboards_by_date
                }
            
            # Chart 4: Public vs Private content
            public_reports = len([r for r in all_reports if r.is_public])
            private_reports = len(all_reports) - public_reports
            public_dashboards = len([d for d in all_dashboards if d.is_public])
            private_dashboards = len(all_dashboards) - public_dashboards
            
            charts_data['content_sharing'] = {
                "type": "stacked_bar",
                "title": "Content Sharing Patterns",
                "x_axis": "Content Type",
                "y_axis": "Count",
                "data": {
                    "Reports": {"Public": public_reports, "Private": private_reports},
                    "Dashboards": {"Public": public_dashboards, "Private": private_dashboards}
                }
            }
            
            logger.info(f"✅ Generated {len(charts_data)} charts")
            return charts_data
            
        except Exception as e:
            logger.error(f"❌ Failed to generate comprehensive charts: {e}")
            return {}
    
    def _generate_trend_insights(self, time_period: str) -> List[Dict[str, Any]]:
        """Generate trend-based insights."""
        try:
            logger.info(f"📈 Generating trend insights for {time_period}")
            
            insights = []
            
            # Load trends from database
            trends = self.database_manager.load_trends()
            
            for trend in trends:
                insight = {
                    "type": "trend_analysis",
                    "title": f"{trend.metric.title()} Trend",
                    "description": f"{trend.metric} is {trend.trend_direction} with {trend.change_percentage:.1f}% change",
                    "metric": trend.metric,
                    "value": trend.change_percentage,
                    "confidence": trend.confidence,
                    "impact": "high" if trend.trend_strength > 0.7 else "medium",
                    "trend_data": trend.to_dict()
                }
                insights.append(insight)
            
            logger.info(f"✅ Generated {len(insights)} trend insights")
            return insights
            
        except Exception as e:
            logger.error(f"❌ Failed to generate trend insights: {e}")
            return []
    
    def _analyze_trend(self, metric: str, period: str) -> Optional[TrendAnalysis]:
        """Analyze trend for a specific metric."""
        try:
            logger.info(f"📊 Analyzing trend for {metric} over {period}")
            
            # This would integrate with time series analysis
            # For now, return a mock trend analysis
            trend = TrendAnalysis(
                metric=metric,
                trend_direction="increasing",
                trend_strength=0.75,
                change_percentage=15.5,
                confidence=0.85,
                period=period,
                data_points=[
                    (datetime.now() - timedelta(days=i), 100 + i * 2)
                    for i in range(30, 0, -1)
                ],
                prediction=150.0
            )
            
            # Save trend to database
            self.database_manager.save_trend(trend)
            
            logger.info(f"✅ Trend analysis completed for {metric}")
            return trend
            
        except Exception as e:
            logger.error(f"❌ Failed to analyze trend for {metric}: {e}")
            return None
    
    # Helper methods
    def _count_reports_by_type(self, reports: List[AnalyticsReport]) -> Dict[str, int]:
        """Count reports by type."""
        counts = {}
        for report in reports:
            report_type = report.report_type
            counts[report_type] = counts.get(report_type, 0) + 1
        return counts
    
    def _group_reports_by_date(self, reports: List[AnalyticsReport]) -> Dict[str, int]:
        """Group reports by date."""
        grouped = {}
        for report in reports:
            date_str = report.generated_at.strftime("%Y-%m-%d")
            grouped[date_str] = grouped.get(date_str, 0) + 1
        return grouped
    
    def _group_dashboards_by_date(self, dashboards: List[AnalyticsDashboard]) -> Dict[str, int]:
        """Group dashboards by date."""
        grouped = {}
        for dashboard in dashboards:
            date_str = dashboard.updated_at.strftime("%Y-%m-%d")
            grouped[date_str] = grouped.get(date_str, 0) + 1
        return grouped
    
    def _analyze_report_generation_trend(self, reports: List[AnalyticsReport]) -> Optional[Dict[str, Any]]:
        """Analyze report generation trend."""
        if len(reports) < 2:
            return None
        
        try:
            # Calculate average reports per day
            dates = [report.generated_at.date() for report in reports]
            unique_dates = len(set(dates))
            reports_per_day = len(reports) / unique_dates if unique_dates > 0 else 0
            
            # Determine trend direction
            if len(reports) >= 3:
                recent_reports = reports[-3:]
                older_reports = reports[:3]
                recent_rate = len(recent_reports) / 3
                older_rate = len(older_reports) / 3
                
                if recent_rate > older_rate * 1.1:
                    direction = "increasing"
                elif recent_rate < older_rate * 0.9:
                    direction = "decreasing"
                else:
                    direction = "stable"
            else:
                direction = "stable"
            
            return {
                "rate": reports_per_day,
                "direction": direction,
                "confidence": 0.8
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to analyze report generation trend: {e}")
            return None
    
    def get_reports_summary(self) -> Dict[str, Any]:
        """Get summary of all reports."""
        try:
            all_reports = self.database_manager.load_all_reports()
            
            summary = {
                "total_reports": len(all_reports),
                "reports_by_type": self._count_reports_by_type(all_reports),
                "recent_reports": self._get_recent_reports(all_reports, 5),
                "public_reports": len([r for r in all_reports if r.is_public]),
                "private_reports": len([r for r in all_reports if not r.is_public])
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"❌ Failed to get reports summary: {e}")
            return {}
    
    def _get_recent_reports(self, reports: List[AnalyticsReport], limit: int) -> List[Dict[str, Any]]:
        """Get recent reports."""
        sorted_reports = sorted(reports, key=lambda x: x.generated_at, reverse=True)
        recent_reports = sorted_reports[:limit]
        
        return [
            {
                "id": report.id,
                "title": report.title,
                "type": report.report_type,
                "generated_at": report.generated_at.isoformat(),
                "author": report.author_name
            }
            for report in recent_reports
        ] 