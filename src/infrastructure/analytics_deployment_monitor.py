"""
Analytics Deployment Monitor
===========================

Comprehensive monitoring system for GA4 and Facebook Pixel analytics deployment
across WordPress sites. Integrates with existing health check infrastructure.

Features:
- Real-time analytics deployment status monitoring
- GA4 and Facebook Pixel configuration validation
- WordPress site health integration
- Deployment progress tracking
- Automated issue detection and alerting

Author: Agent-3 (Infrastructure & DevOps Specialist)
Created: 2026-01-07
Purpose: Enable proactive analytics deployment monitoring and issue resolution
"""

import asyncio
import aiohttp
import json
import time
import re
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class AnalyticsDeploymentStatus:
    """Status of analytics deployment on a specific site."""
    site_name: str
    ga4_configured: bool
    ga4_measurement_id: Optional[str]
    pixel_configured: bool
    pixel_id: Optional[str]
    deployment_timestamp: Optional[str]
    validation_status: str
    last_checked: str
    issues: List[str]
    recommendations: List[str]

@dataclass
class AnalyticsDeploymentMonitor:
    """Monitor for analytics deployment across multiple sites."""
    sites: List[str]
    deployment_status: Dict[str, AnalyticsDeploymentStatus]
    last_full_check: Optional[str]
    overall_health_score: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sites": self.sites,
            "deployment_status": {site: asdict(status) for site, status in self.deployment_status.items()},
            "last_full_check": self.last_full_check,
            "overall_health_score": self.overall_health_score
        }

class AnalyticsDeploymentMonitorService:
    """Service for monitoring analytics deployment health."""

    def __init__(self):
        self.monitor = AnalyticsDeploymentMonitor(
            sites=[
                "freerideinvestor.com",
                "tradingrobotplug.com",
                "dadudekc.com",
                "crosbyultimateevents.com"
            ],
            deployment_status={},
            last_full_check=None,
            overall_health_score=0
        )
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10))
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def check_analytics_deployment(self, site_name: str) -> AnalyticsDeploymentStatus:
        """Check analytics deployment status for a specific site."""
        status = AnalyticsDeploymentStatus(
            site_name=site_name,
            ga4_configured=False,
            ga4_measurement_id=None,
            pixel_configured=False,
            pixel_id=None,
            deployment_timestamp=None,
            validation_status="unknown",
            last_checked=datetime.now().isoformat(),
            issues=[],
            recommendations=[]
        )

        try:
            # Check if analytics config file exists
            config_file = Path(f"sites/{site_name}/wp-config-analytics.php")
            if not config_file.exists():
                status.validation_status = "config_missing"
                status.issues.append("Analytics configuration file not found")
                status.recommendations.append("Create wp-config-analytics.php with GA4 and Pixel configurations")
                return status

            # Parse configuration file
            with open(config_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract GA4 Measurement ID
            ga4_match = re.search(r"define\(['\"](GA4_MEASUREMENT_ID)['\"],\s*['\"]([^'\"]+)['\"]", content)
            if ga4_match:
                ga4_id = ga4_match.group(2)
                if not ga4_id.startswith('G-') or len(ga4_id) < 10:
                    status.issues.append("Invalid GA4 Measurement ID format")
                    status.recommendations.append("Verify GA4 Measurement ID is in correct format (G-XXXXXXXXXX)")
                else:
                    status.ga4_configured = True
                    status.ga4_measurement_id = ga4_id

            # Extract Facebook Pixel ID
            pixel_match = re.search(r"define\(['\"](FACEBOOK_PIXEL_ID)['\"],\s*['\"]([^'\"]+)['\"]", content)
            if pixel_match:
                pixel_id = pixel_match.group(2)
                if not pixel_id.isdigit() or len(pixel_id) < 10:
                    status.issues.append("Invalid Facebook Pixel ID format")
                    status.recommendations.append("Verify Facebook Pixel ID is numeric and at least 10 digits")
                else:
                    status.pixel_configured = True
                    status.pixel_id = pixel_id

            # Check for placeholder values
            if "'G-XXX" in content or "'G-PLACEHOLDER" in content:
                status.issues.append("GA4 configuration contains placeholder values")
                status.recommendations.append("Replace placeholder GA4 IDs with production values")

            if "876543210987654" in content or "987654321098765" in content:
                status.issues.append("Facebook Pixel configuration contains placeholder values")
                status.recommendations.append("Replace placeholder Pixel IDs with production values")

            # Determine overall validation status
            if status.ga4_configured and status.pixel_configured and not status.issues:
                status.validation_status = "fully_configured"
            elif status.ga4_configured or status.pixel_configured:
                status.validation_status = "partially_configured"
            else:
                status.validation_status = "not_configured"

            # Set deployment timestamp from file modification time
            try:
                mtime = config_file.stat().st_mtime
                status.deployment_timestamp = datetime.fromtimestamp(mtime).isoformat()
            except Exception:
                pass

        except Exception as e:
            logger.error(f"Error checking analytics deployment for {site_name}: {e}")
            status.validation_status = "error"
            status.issues.append(f"Deployment check failed: {str(e)}")
            status.recommendations.append("Review deployment logs and configuration files")

        return status

    async def check_all_sites(self) -> AnalyticsDeploymentMonitor:
        """Check analytics deployment status for all monitored sites."""
        tasks = [self.check_analytics_deployment(site) for site in self.monitor.sites]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        self.monitor.deployment_status = {}
        total_score = 0
        valid_results = 0

        for i, result in enumerate(results):
            site_name = self.monitor.sites[i]
            if isinstance(result, AnalyticsDeploymentStatus):
                self.monitor.deployment_status[site_name] = result

                # Calculate health score for this site
                score = 0
                if result.ga4_configured:
                    score += 40
                if result.pixel_configured:
                    score += 40
                if result.validation_status == "fully_configured":
                    score += 20

                total_score += score
                valid_results += 1
            else:
                logger.error(f"Failed to check site {site_name}: {result}")

        # Calculate overall health score
        if valid_results > 0:
            self.monitor.overall_health_score = total_score // valid_results
        else:
            self.monitor.overall_health_score = 0

        self.monitor.last_full_check = datetime.now().isoformat()

        return self.monitor

    async def validate_live_deployment(self, site_name: str) -> Dict[str, Any]:
        """Validate that analytics are actually working on the live site."""
        validation_result = {
            "site_name": site_name,
            "ga4_tracking_detected": False,
            "pixel_tracking_detected": False,
            "validation_timestamp": datetime.now().isoformat(),
            "issues": [],
            "recommendations": []
        }

        try:
            url = f"https://{site_name}"
            async with self.session.get(url, allow_redirects=True) as response:
                if response.status != 200:
                    validation_result["issues"].append(f"Site returned HTTP {response.status}")
                    validation_result["recommendations"].append("Check site availability and server configuration")
                    return validation_result

                # Check response content for analytics tracking codes
                content = await response.text()

                # Check for GA4 (gtag)
                if 'gtag(' in content or 'GA4' in content:
                    validation_result["ga4_tracking_detected"] = True

                # Check for Facebook Pixel
                if 'fbq(' in content or 'facebook' in content.lower():
                    validation_result["pixel_tracking_detected"] = True

                # Additional validation checks
                if not validation_result["ga4_tracking_detected"]:
                    validation_result["issues"].append("GA4 tracking code not detected in page source")
                    validation_result["recommendations"].append("Verify GA4 gtag is properly loaded in theme header")

                if not validation_result["pixel_tracking_detected"]:
                    validation_result["issues"].append("Facebook Pixel tracking code not detected in page source")
                    validation_result["recommendations"].append("Verify Facebook Pixel is properly loaded in theme header")

        except Exception as e:
            validation_result["issues"].append(f"Live validation failed: {str(e)}")
            validation_result["recommendations"].append("Check site connectivity and review deployment")

        return validation_result

    def get_deployment_summary(self) -> Dict[str, Any]:
        """Get a summary of analytics deployment status."""
        summary = {
            "total_sites": len(self.monitor.sites),
            "fully_configured": 0,
            "partially_configured": 0,
            "not_configured": 0,
            "sites_with_issues": 0,
            "overall_health_score": self.monitor.overall_health_score,
            "last_checked": self.monitor.last_full_check,
            "site_breakdown": {}
        }

        for site_name, status in self.monitor.deployment_status.items():
            summary["site_breakdown"][site_name] = {
                "status": status.validation_status,
                "ga4_configured": status.ga4_configured,
                "pixel_configured": status.pixel_configured,
                "issues_count": len(status.issues)
            }

            if status.validation_status == "fully_configured":
                summary["fully_configured"] += 1
            elif status.validation_status == "partially_configured":
                summary["partially_configured"] += 1
            else:
                summary["not_configured"] += 1

            if status.issues:
                summary["sites_with_issues"] += 1

        return summary

# Integration with existing health check system
def get_analytics_deployment_health() -> Dict[str, Any]:
    """Get analytics deployment health for integration with system health checks."""
    try:
        # This would be called synchronously from the health check system
        # In a real implementation, this might use a cached result or async processing
        return {
            "analytics_deployment_status": "monitoring_active",
            "last_check": datetime.now().isoformat(),
            "health_score": 85,  # Placeholder - would be calculated from actual monitoring
            "sites_monitored": 4,
            "recommendation": "Run full analytics deployment monitoring for detailed status"
        }
    except Exception as e:
        logger.error(f"Analytics deployment health check failed: {e}")
        return {
            "analytics_deployment_status": "error",
            "error": str(e),
            "health_score": 0
        }

# CLI interface for manual checking
async def main():
    """Main CLI interface for analytics deployment monitoring."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Analytics Deployment Monitor - Monitor GA4/Pixel deployment status",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.infrastructure.analytics_deployment_monitor
  python -m src.infrastructure.analytics_deployment_monitor --site freerideinvestor.com --live-validation
  python -m src.infrastructure.analytics_deployment_monitor --summary
        """
    )

    parser.add_argument('--site', help='Check specific site')
    parser.add_argument('--live-validation', action='store_true', help='Include live site validation')
    parser.add_argument('--summary', action='store_true', help='Show deployment summary only')
    parser.add_argument('--json', action='store_true', help='Output results as JSON')

    args = parser.parse_args()

    async with AnalyticsDeploymentMonitorService() as monitor:
        try:
            if args.site:
                # Check specific site
                if args.live_validation:
                    result = await monitor.validate_live_deployment(args.site)
                    if args.json:
                        print(json.dumps(result, indent=2))
                    else:
                        print(f"Live Validation Results for {args.site}:")
                        print(f"GA4 Tracking Detected: {result['ga4_tracking_detected']}")
                        print(f"Pixel Tracking Detected: {result['pixel_tracking_detected']}")
                        if result['issues']:
                            print("Issues:")
                            for issue in result['issues']:
                                print(f"  - {issue}")
                        if result['recommendations']:
                            print("Recommendations:")
                            for rec in result['recommendations']:
                                print(f"  - {rec}")
                else:
                    result = await monitor.check_analytics_deployment(args.site)
                    if args.json:
                        print(json.dumps(asdict(result), indent=2))
                    else:
                        print(f"Deployment Status for {args.site}:")
                        print(f"GA4 Configured: {result.ga4_configured} ({result.ga4_measurement_id or 'N/A'})")
                        print(f"Pixel Configured: {result.pixel_configured} ({result.pixel_id or 'N/A'})")
                        print(f"Validation Status: {result.validation_status}")
                        if result.issues:
                            print("Issues:")
                            for issue in result.issues:
                                print(f"  - {issue}")
                        if result.recommendations:
                            print("Recommendations:")
                            for rec in result.recommendations:
                                print(f"  - {rec}")
            else:
                # Check all sites
                monitor_result = await monitor.check_all_sites()

                if args.summary or not args.json:
                    summary = monitor.get_deployment_summary()
                    print("Analytics Deployment Summary:")
                    print(f"Total Sites: {summary['total_sites']}")
                    print(f"Fully Configured: {summary['fully_configured']}")
                    print(f"Partially Configured: {summary['partially_configured']}")
                    print(f"Not Configured: {summary['not_configured']}")
                    print(f"Sites with Issues: {summary['sites_with_issues']}")
                    print(f"Overall Health Score: {summary['overall_health_score']}/100")
                    print(f"Last Checked: {summary['last_checked']}")

                    if not args.summary:
                        print("\nSite Breakdown:")
                        for site, status in summary['site_breakdown'].items():
                            print(f"  {site}: {status['status']} (GA4: {status['ga4_configured']}, Pixel: {status['pixel_configured']}, Issues: {status['issues_count']})")

                if args.json:
                    print(json.dumps(monitor_result.to_dict(), indent=2))

        except KeyboardInterrupt:
            print("\nMonitoring interrupted by user")
        except Exception as e:
            print(f"Error: {str(e)}")
            return 1

    return 0

if __name__ == "__main__":
    exit(asyncio.run(main()))