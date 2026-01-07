#!/usr/bin/env python3
"""
Analytics Deployment Dashboard
==============================

Executive dashboard for comprehensive analytics deployment ecosystem oversight.
Integrates all analytics deployment tools and provides unified enterprise visibility.

Features:
- Executive analytics deployment overview and KPIs
- Real-time deployment status across all sites
- Compliance and validation status monitoring
- Live verification results and trends
- Orchestration pipeline status and progress
- Enterprise analytics health scorecard
- Automated alerting and recommendations

Author: Agent-3 (Infrastructure & DevOps Specialist)
Created: 2026-01-07
Purpose: Provide executive oversight and unified visibility into enterprise analytics deployment ecosystem
"""

import asyncio
import json
import time
import subprocess
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class DashboardKPIs:
    """Key performance indicators for analytics deployment dashboard."""
    total_sites: int
    sites_configured: int
    sites_deployed: int
    sites_verified: int
    compliance_score_avg: float
    orchestration_completion: float
    critical_issues: int
    last_updated: str

@dataclass
class SiteAnalyticsStatus:
    """Comprehensive analytics status for a single site."""
    site_name: str
    configuration_status: str
    deployment_status: str
    verification_status: str
    compliance_score: int
    orchestration_stage: str
    last_checked: str
    critical_issues: List[str]
    recommendations: List[str]

@dataclass
class AnalyticsDeploymentDashboard:
    """Complete analytics deployment dashboard."""
    dashboard_id: str
    timestamp: str
    kpis: DashboardKPIs
    site_status: Dict[str, SiteAnalyticsStatus]
    ecosystem_health: Dict[str, Any]
    trends: Dict[str, Any]
    alerts: List[str]
    recommendations: List[str]

class AnalyticsDeploymentDashboardService:
    """Service for generating comprehensive analytics deployment dashboards."""

    def __init__(self):
        self.p0_sites = [
            "freerideinvestor.com",
            "tradingrobotplug.com",
            "dadudekc.com",
            "crosbyultimateevents.com"
        ]
        self.dashboard_id = f"analytics_dashboard_{int(time.time())}"

    async def generate_dashboard(self) -> AnalyticsDeploymentDashboard:
        """Generate comprehensive analytics deployment dashboard."""
        dashboard = AnalyticsDeploymentDashboard(
            dashboard_id=self.dashboard_id,
            timestamp=datetime.now().isoformat(),
            kpis=DashboardKPIs(0, 0, 0, 0, 0.0, 0.0, 0, datetime.now().isoformat()),
            site_status={},
            ecosystem_health={},
            trends={},
            alerts=[],
            recommendations=[]
        )

        # Gather data from all analytics tools
        await self._gather_configuration_status(dashboard)
        await self._gather_compliance_status(dashboard)
        await self._gather_verification_status(dashboard)
        await self._gather_orchestration_status(dashboard)

        # Calculate KPIs and ecosystem health
        self._calculate_kpis(dashboard)
        self._assess_ecosystem_health(dashboard)
        self._generate_alerts_and_recommendations(dashboard)

        return dashboard

    async def _gather_configuration_status(self, dashboard: AnalyticsDeploymentDashboard):
        """Gather configuration validation status from all sites."""
        for site in self.p0_sites:
            site_status = SiteAnalyticsStatus(
                site_name=site,
                configuration_status="unknown",
                deployment_status="unknown",
                verification_status="unknown",
                compliance_score=0,
                orchestration_stage="unknown",
                last_checked=datetime.now().isoformat(),
                critical_issues=[],
                recommendations=[]
            )

            try:
                # Run configuration validation
                result = await self._run_tool_command(
                    "python", "tools/deploy_ga4_pixel_analytics.py",
                    "--validate-only", "--site", site
                )

                if result["returncode"] == 0:
                    site_status.configuration_status = "valid"
                else:
                    site_status.configuration_status = "invalid"
                    site_status.critical_issues.append("Configuration validation failed")

            except Exception as e:
                logger.debug(f"Configuration check failed for {site}: {e}")
                site_status.configuration_status = "error"
                site_status.critical_issues.append(f"Configuration check error: {str(e)}")

            dashboard.site_status[site] = site_status

    async def _gather_compliance_status(self, dashboard: AnalyticsDeploymentDashboard):
        """Gather compliance assessment status from all sites."""
        for site in self.p0_sites:
            if site in dashboard.site_status:
                site_status = dashboard.site_status[site]

                try:
                    # Run compliance assessment
                    result = await self._run_tool_command(
                        "python", "tools/enterprise_analytics_compliance_validator.py",
                        "--site", site
                    )

                    # Parse compliance score from output
                    output = result["stdout"]
                    score_match = None
                    for line in output.split('\n'):
                        if "Compliance Score:" in line:
                            try:
                                score_str = line.split(":")[1].split("/")[0].strip()
                                score_match = int(score_str)
                                break
                            except (ValueError, IndexError):
                                pass

                    if score_match is not None:
                        site_status.compliance_score = score_match
                    else:
                        site_status.compliance_score = 0
                        site_status.critical_issues.append("Compliance score parsing failed")

                except Exception as e:
                    logger.debug(f"Compliance check failed for {site}: {e}")
                    site_status.compliance_score = 0
                    site_status.critical_issues.append(f"Compliance check error: {str(e)}")

    async def _gather_verification_status(self, dashboard: AnalyticsDeploymentDashboard):
        """Gather live verification status from all sites."""
        for site in self.p0_sites:
            if site in dashboard.site_status:
                site_status = dashboard.site_status[site]

                try:
                    # Run live verification
                    result = await self._run_tool_command(
                        "python", "tools/analytics_live_verification.py",
                        "--site", site
                    )

                    # Parse verification status
                    output = result["stdout"]
                    if "✅" in output and "❌ Not detected" not in output.split("GA4:")[1].split("\n")[0]:
                        site_status.verification_status = "verified"
                    else:
                        site_status.verification_status = "unverified"
                        if "❌ Not detected" in output:
                            site_status.critical_issues.append("Analytics tracking not detected on live site")

                except Exception as e:
                    logger.debug(f"Verification check failed for {site}: {e}")
                    site_status.verification_status = "error"
                    site_status.critical_issues.append(f"Verification check error: {str(e)}")

    async def _gather_orchestration_status(self, dashboard: AnalyticsDeploymentDashboard):
        """Gather orchestration pipeline status."""
        try:
            # Run orchestration status check
            result = await self._run_tool_command(
                "python", "tools/analytics_deployment_orchestrator.py",
                "--p0-sites", "--status"
            )

            # Parse orchestration status
            output = result["stdout"]

            # Extract completion percentage
            completion_match = None
            for line in output.split('\n'):
                if "Completion:" in line:
                    try:
                        completion_str = line.split(":")[1].strip().replace("%", "")
                        completion_match = float(completion_str)
                        break
                    except (ValueError, IndexError):
                        pass

            if completion_match is not None:
                dashboard.kpis.orchestration_completion = completion_match

            # Parse site-specific orchestration stages
            current_site = None
            for line in output.split('\n'):
                if line.startswith('🏢 ') and '.com' in line:
                    current_site = line.replace('🏢 ', '').strip()
                elif current_site and 'Current Stage:' in line:
                    stage = line.split(':')[1].strip()
                    if current_site in dashboard.site_status:
                        dashboard.site_status[current_site].orchestration_stage = stage

        except Exception as e:
            logger.debug(f"Orchestration status check failed: {e}")
            dashboard.kpis.orchestration_completion = 0.0

    async def _run_tool_command(self, *args) -> Dict[str, Any]:
        """Run a tool command and return results."""
        try:
            process = await asyncio.create_subprocess_exec(
                *args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            return {
                "returncode": process.returncode,
                "stdout": stdout.decode(),
                "stderr": stderr.decode()
            }
        except Exception as e:
            return {
                "returncode": -1,
                "stdout": "",
                "stderr": str(e)
            }

    def _calculate_kpis(self, dashboard: AnalyticsDeploymentDashboard):
        """Calculate key performance indicators."""
        total_sites = len(dashboard.site_status)
        dashboard.kpis.total_sites = total_sites

        configured_sites = sum(1 for status in dashboard.site_status.values()
                             if status.configuration_status == "valid")
        dashboard.kpis.sites_configured = configured_sites

        deployed_sites = sum(1 for status in dashboard.site_status.values()
                           if status.deployment_status == "deployed")
        dashboard.kpis.sites_deployed = deployed_sites

        verified_sites = sum(1 for status in dashboard.site_status.values()
                           if status.verification_status == "verified")
        dashboard.kpis.sites_verified = verified_sites

        # Calculate average compliance score
        compliance_scores = [status.compliance_score for status in dashboard.site_status.values()
                           if status.compliance_score > 0]
        if compliance_scores:
            dashboard.kpis.compliance_score_avg = sum(compliance_scores) / len(compliance_scores)

        # Count critical issues
        critical_issues = sum(len(status.critical_issues) for status in dashboard.site_status.values())
        dashboard.kpis.critical_issues = critical_issues

    def _assess_ecosystem_health(self, dashboard: AnalyticsDeploymentDashboard):
        """Assess overall ecosystem health."""
        health = {
            "overall_score": 0,
            "configuration_health": 0,
            "deployment_health": 0,
            "compliance_health": 0,
            "verification_health": 0,
            "orchestration_health": dashboard.kpis.orchestration_completion,
            "health_trend": "stable",
            "risk_level": "low"
        }

        # Calculate component health scores
        total_sites = dashboard.kpis.total_sites
        if total_sites > 0:
            health["configuration_health"] = (dashboard.kpis.sites_configured / total_sites) * 100
            health["deployment_health"] = (dashboard.kpis.sites_deployed / total_sites) * 100
            health["compliance_health"] = dashboard.kpis.compliance_score_avg
            health["verification_health"] = (dashboard.kpis.sites_verified / total_sites) * 100

            # Calculate overall score
            health["overall_score"] = (
                health["configuration_health"] * 0.2 +
                health["deployment_health"] * 0.2 +
                health["compliance_health"] * 0.2 +
                health["verification_health"] * 0.2 +
                health["orchestration_health"] * 0.2
            )

            # Assess risk level
            if dashboard.kpis.critical_issues > 2:
                health["risk_level"] = "high"
            elif dashboard.kpis.critical_issues > 0:
                health["risk_level"] = "medium"
            else:
                health["risk_level"] = "low"

        dashboard.ecosystem_health = health

        # Generate trends (simplified for this implementation)
        dashboard.trends = {
            "completion_trend": "increasing" if dashboard.kpis.orchestration_completion > 0 else "stalled",
            "issue_trend": "decreasing" if dashboard.kpis.critical_issues == 0 else "stable",
            "compliance_trend": "improving" if dashboard.kpis.compliance_score_avg > 50 else "needs_attention"
        }

    def _generate_alerts_and_recommendations(self, dashboard: AnalyticsDeploymentDashboard):
        """Generate alerts and enterprise recommendations."""
        alerts = []
        recommendations = []

        # Configuration alerts
        if dashboard.kpis.sites_configured < dashboard.kpis.total_sites:
            alerts.append(f"⚠️ {dashboard.kpis.total_sites - dashboard.kpis.sites_configured} sites have configuration issues")

        # Deployment alerts
        if dashboard.kpis.sites_deployed == 0:
            alerts.append("🚨 No sites have been successfully deployed")
        elif dashboard.kpis.sites_deployed < dashboard.kpis.sites_configured:
            alerts.append(f"⚠️ {dashboard.kpis.sites_configured - dashboard.kpis.sites_deployed} configured sites not yet deployed")

        # Compliance alerts
        if dashboard.kpis.compliance_score_avg < 70:
            alerts.append(f"⚠️ Average compliance score ({dashboard.kpis.compliance_score_avg:.1f}%) below enterprise standards")

        # Verification alerts
        if dashboard.kpis.sites_verified == 0:
            alerts.append("🚨 No sites have been verified as working correctly")

        # Critical issues alerts
        if dashboard.kpis.critical_issues > 0:
            alerts.append(f"🚨 {dashboard.kpis.critical_issues} critical issues require immediate attention")

        # Orchestration alerts
        if dashboard.kpis.orchestration_completion == 0:
            alerts.append("ℹ️ Deployment orchestration has not started")

        # Generate recommendations
        if dashboard.kpis.sites_configured < dashboard.kpis.total_sites:
            recommendations.append("Complete configuration validation for all sites before proceeding with deployment")

        if dashboard.kpis.sites_deployed == 0:
            recommendations.append("Execute deployment for sites that have passed configuration validation")

        if dashboard.kpis.compliance_score_avg < 80:
            recommendations.append("Address GDPR compliance issues and implement proper user consent mechanisms")

        if dashboard.kpis.orchestration_completion < 50:
            recommendations.append("Utilize the analytics deployment orchestrator for streamlined deployment management")

        recommendations.append("Regular monitoring and verification should be established for ongoing analytics health")

        dashboard.alerts = alerts
        dashboard.recommendations = recommendations

    def print_dashboard(self, dashboard: AnalyticsDeploymentDashboard):
        """Print formatted dashboard to console."""
        print("🚀 Analytics Deployment Ecosystem Dashboard")
        print("=" * 60)
        print(f"Dashboard ID: {dashboard.dashboard_id}")
        print(f"Generated: {dashboard.timestamp}")
        print()

        # KPIs Section
        print("📊 Key Performance Indicators")
        print("-" * 30)
        print(f"Total Sites: {dashboard.kpis.total_sites}")
        print(f"Sites Configured: {dashboard.kpis.sites_configured}")
        print(f"Sites Deployed: {dashboard.kpis.sites_deployed}")
        print(f"Sites Verified: {dashboard.kpis.sites_verified}")
        print(".1f")
        print(".1f")
        print(f"Critical Issues: {dashboard.kpis.critical_issues}")
        print()

        # Ecosystem Health
        health = dashboard.ecosystem_health
        print("🏥 Ecosystem Health")
        print("-" * 20)
        print(".1f")
        print(".1f")
        print(".1f")
        print(".1f")
        print(".1f")
        print(".1f")
        print(f"Risk Level: {health['risk_level'].upper()}")
        print()

        # Site Status
        print("🏢 Site Status Overview")
        print("-" * 25)
        for site, status in dashboard.site_status.items():
            print(f"\n🏢 {site}")
            print(f"   Configuration: {status.configuration_status}")
            print(f"   Deployment: {status.deployment_status}")
            print(f"   Verification: {status.verification_status}")
            print(f"   Compliance: {status.compliance_score}/100")
            print(f"   Orchestration: {status.orchestration_stage}")
            if status.critical_issues:
                print(f"   Issues: {len(status.critical_issues)}")
        print()

        # Alerts
        if dashboard.alerts:
            print("🚨 Active Alerts")
            print("-" * 15)
            for alert in dashboard.alerts:
                print(f"• {alert}")
            print()

        # Recommendations
        if dashboard.recommendations:
            print("💡 Enterprise Recommendations")
            print("-" * 30)
            for rec in dashboard.recommendations:
                print(f"• {rec}")
            print()

# CLI interface
async def main():
    """Main CLI interface for analytics deployment dashboard."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Analytics Deployment Dashboard - Executive oversight of analytics deployment ecosystem",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/analytics_deployment_dashboard.py
  python tools/analytics_deployment_dashboard.py --json
  python tools/analytics_deployment_dashboard.py --site freerideinvestor.com
        """
    )

    parser.add_argument('--site', help='Focus dashboard on specific site')
    parser.add_argument('--json', action='store_true', help='Output dashboard as JSON')
    parser.add_argument('--quiet', action='store_true', help='Suppress detailed output')

    args = parser.parse_args()

    dashboard_service = AnalyticsDeploymentDashboardService()

    try:
        dashboard = await dashboard_service.generate_dashboard()

        if args.json:
            print(json.dumps(asdict(dashboard), indent=2))
        else:
            if args.site and args.site in dashboard.site_status:
                # Show detailed site view
                site_status = dashboard.site_status[args.site]
                print(f"🏢 Detailed Status for {args.site}")
                print("=" * 40)
                print(f"Configuration: {site_status.configuration_status}")
                print(f"Deployment: {site_status.deployment_status}")
                print(f"Verification: {site_status.verification_status}")
                print(f"Compliance Score: {site_status.compliance_score}/100")
                print(f"Orchestration Stage: {site_status.orchestration_stage}")
                if site_status.critical_issues:
                    print(f"Critical Issues: {len(site_status.critical_issues)}")
                    for issue in site_status.critical_issues[:3]:
                        print(f"  • {issue}")
                if site_status.recommendations:
                    print(f"Recommendations: {len(site_status.recommendations)}")
                    for rec in site_status.recommendations[:3]:
                        print(f"  • {rec}")
            else:
                # Show full dashboard
                dashboard_service.print_dashboard(dashboard)

    except KeyboardInterrupt:
        print("\n⚠️  Dashboard generation interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())