#!/usr/bin/env python3
"""
Analytics Ecosystem Health Scoring System
==========================================

<!-- SSOT Domain: analytics -->

Comprehensive health scoring system for enterprise analytics ecosystems.
Provides quantitative health metrics, risk assessments, and optimization recommendations.

V2 Compliance | Author: Agent-3 | Date: 2026-01-07
"""

from __future__ import annotations

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict

import sys
import os

# Add the project root and tools directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tools.website_health_monitor import WebsiteHealthMonitor
from tools.enterprise_analytics_compliance_validator import EnterpriseAnalyticsComplianceValidator
from src.infrastructure.analytics_deployment_monitor import AnalyticsDeploymentMonitor
from tools.analytics_live_verification import AnalyticsLiveVerificationTool

logger = logging.getLogger(__name__)


@dataclass
class HealthComponent:
    """Individual health component with scoring."""
    name: str
    score: float  # 0-100
    weight: float  # Relative importance (0-1)
    status: str  # healthy, warning, critical
    issues: List[str]
    recommendations: List[str]
    metrics: Dict[str, Any]


@dataclass
class EcosystemHealthScore:
    """Complete ecosystem health assessment."""
    timestamp: str
    overall_score: float  # 0-100
    risk_level: str  # low, medium, high, critical
    components: Dict[str, HealthComponent]
    site_breakdown: Dict[str, Dict[str, Any]]
    recommendations: List[str]
    next_steps: List[str]


class AnalyticsEcosystemHealthScorer:
    """
    Comprehensive health scoring system for enterprise analytics ecosystems.

    Evaluates multiple dimensions:
    - Infrastructure Health (40% weight)
    - Analytics Deployment (30% weight)
    - Compliance & Security (20% weight)
    - Performance & Monitoring (10% weight)
    """

    def __init__(self, sites: List[Dict[str, str]]):
        self.sites = sites
        self.health_monitor = WebsiteHealthMonitor()
        self.compliance_validator = EnterpriseAnalyticsComplianceValidator(sites)
        self.deployment_monitor = AnalyticsDeploymentMonitor(sites)
        self.live_verifier = AnalyticsLiveVerificationTool()

        # Component weights for overall scoring
        self.component_weights = {
            "infrastructure": 0.40,
            "deployment": 0.30,
            "compliance": 0.20,
            "performance": 0.10
        }

    async def calculate_ecosystem_health(self) -> EcosystemHealthScore:
        """
        Calculate comprehensive ecosystem health score.

        Returns:
            Complete health assessment with scores, risks, and recommendations
        """
        logger.info("🩺 Starting comprehensive analytics ecosystem health assessment...")

        # Run all component assessments in parallel
        tasks = [
            self._assess_infrastructure_health(),
            self._assess_deployment_health(),
            self._assess_compliance_health(),
            self._assess_performance_health()
        ]

        results = await asyncio.gather(*tasks)

        # Unpack results
        infra_health, infra_sites = results[0]
        deploy_health, deploy_sites = results[1]
        compliance_health, compliance_sites = results[2]
        perf_health, perf_sites = results[3]

        # Build components dictionary
        components = {
            "infrastructure": infra_health,
            "deployment": deploy_health,
            "compliance": compliance_health,
            "performance": perf_health
        }

        # Calculate overall score using weighted average
        overall_score = sum(
            component.score * self.component_weights[component_name]
            for component_name, component in components.items()
        )

        # Determine risk level based on overall score and critical issues
        risk_level = self._calculate_risk_level(overall_score, components)

        # Generate comprehensive recommendations
        recommendations = self._generate_recommendations(components)

        # Generate next steps based on risk level and issues
        next_steps = self._generate_next_steps(risk_level, components)

        # Combine site breakdowns
        site_breakdown = {}
        for site in self.sites:
            site_name = site['name']
            site_breakdown[site_name] = {
                "infrastructure": infra_sites.get(site_name, {}),
                "deployment": deploy_sites.get(site_name, {}),
                "compliance": compliance_sites.get(site_name, {}),
                "performance": perf_sites.get(site_name, {})
            }

        health_score = EcosystemHealthScore(
            timestamp=datetime.now().isoformat(),
            overall_score=round(overall_score, 2),
            risk_level=risk_level,
            components=components,
            site_breakdown=site_breakdown,
            recommendations=recommendations,
            next_steps=next_steps
        )

        logger.info(f"✅ Ecosystem health assessment complete. Overall Score: {overall_score:.1f}/100 ({risk_level} risk)")

        return health_score

    async def _assess_infrastructure_health(self) -> Tuple[HealthComponent, Dict[str, Any]]:
        """Assess infrastructure health across all sites."""
        logger.debug("Assessing infrastructure health...")

        # Run full health check
        health_results = await self.health_monitor.run_full_check(self.sites)

        # Calculate component score
        total_sites = len(self.sites)
        healthy_sites = sum(1 for result in health_results if result.status == "healthy")
        warning_sites = sum(1 for result in health_results if result.status == "warning")
        critical_sites = sum(1 for result in health_results if result.status in ["critical", "error"])

        # Score calculation: 100% for healthy, penalties for issues
        base_score = (healthy_sites / total_sites) * 100
        warning_penalty = (warning_sites / total_sites) * 20  # -20% per warning site
        critical_penalty = (critical_sites / total_sites) * 50  # -50% per critical site

        infra_score = max(0, base_score - warning_penalty - critical_penalty)

        # Determine status
        if infra_score >= 80:
            status = "healthy"
        elif infra_score >= 60:
            status = "warning"
        else:
            status = "critical"

        # Collect issues and recommendations
        issues = []
        recommendations = []
        site_details = {}

        for result in health_results:
            site_issues = result.issues + result.recommendations
            if site_issues:
                issues.extend([f"{result.url}: {issue}" for issue in site_issues[:3]])  # Limit per site
                recommendations.extend([f"{result.url}: {rec}" for rec in result.recommendations[:2]])

            site_details[result.url.split('/')[-1]] = {
                "status": result.status,
                "response_time": getattr(result, 'response_time', None),
                "http_status": result.http_status,
                "issues_count": len(result.issues)
            }

        infra_component = HealthComponent(
            name="Infrastructure Health",
            score=round(infra_score, 2),
            weight=self.component_weights["infrastructure"],
            status=status,
            issues=issues[:10],  # Limit total issues
            recommendations=recommendations[:10],
            metrics={
                "total_sites": total_sites,
                "healthy_sites": healthy_sites,
                "warning_sites": warning_sites,
                "critical_sites": critical_sites,
                "average_response_time": sum(getattr(r, 'response_time', 0) or 0 for r in health_results) / len(health_results)
            }
        )

        return infra_component, site_details

    async def _assess_deployment_health(self) -> Tuple[HealthComponent, Dict[str, Any]]:
        """Assess analytics deployment health."""
        logger.debug("Assessing deployment health...")

        # Run deployment check
        await self.deployment_monitor.run_full_check()

        # Calculate scores based on deployment status
        deployment_results = self.deployment_monitor.deployment_status

        total_sites = len(self.sites)
        fully_deployed = sum(1 for status in deployment_results.values()
                           if getattr(status, 'validation_status', '') == 'fully_configured')
        partially_deployed = sum(1 for status in deployment_results.values()
                               if getattr(status, 'validation_status', '') == 'partially_configured')
        not_deployed = sum(1 for status in deployment_results.values()
                          if getattr(status, 'validation_status', '') in ['not_configured', 'site_unavailable'])

        # Score calculation
        deploy_score = (
            (fully_deployed * 100 + partially_deployed * 50) / total_sites
        )

        # Determine status
        if deploy_score >= 85:
            status = "healthy"
        elif deploy_score >= 60:
            status = "warning"
        else:
            status = "critical"

        # Collect issues and recommendations
        issues = []
        recommendations = []
        site_details = {}

        for site_name, status_obj in deployment_results.items():
            site_issues = getattr(status_obj, 'issues', [])
            if site_issues:
                issues.extend([f"{site_name}: {issue}" for issue in site_issues[:2]])

            recommendations.append(f"{site_name}: Complete analytics deployment and verification")

            site_details[site_name] = {
                "validation_status": getattr(status_obj, 'validation_status', 'unknown'),
                "ga4_configured": getattr(status_obj, 'ga4_configured', False),
                "pixel_configured": getattr(status_obj, 'pixel_configured', False),
                "issues_count": len(getattr(status_obj, 'issues', []))
            }

        deploy_component = HealthComponent(
            name="Analytics Deployment",
            score=round(deploy_score, 2),
            weight=self.component_weights["deployment"],
            status=status,
            issues=issues[:10],
            recommendations=recommendations[:10],
            metrics={
                "total_sites": total_sites,
                "fully_deployed": fully_deployed,
                "partially_deployed": partially_deployed,
                "not_deployed": not_deployed,
                "deployment_coverage": f"{fully_deployed + partially_deployed}/{total_sites}"
            }
        )

        return deploy_component, site_details

    async def _assess_compliance_health(self) -> Tuple[HealthComponent, Dict[str, Any]]:
        """Assess compliance and security health."""
        logger.debug("Assessing compliance health...")

        # Run compliance audit
        await self.compliance_validator.run_full_audit()

        # Calculate compliance scores
        audit_results = self.compliance_validator.audit_results

        if not audit_results:
            compliance_score = 0
            status = "critical"
            issues = ["No compliance audit data available"]
            recommendations = ["Run compliance audit immediately"]
            site_details = {}
        else:
            total_sites = len(audit_results)
            gdpr_compliant = sum(1 for audit in audit_results.values()
                                if getattr(audit, 'gdpr_status', '') == 'compliant')
            compliant_sites = sum(1 for audit in audit_results.values()
                                 if getattr(audit, 'overall_compliance_score', 0) >= 80)

            compliance_score = (gdpr_compliant / total_sites) * 100

            if compliance_score >= 90:
                status = "healthy"
            elif compliance_score >= 70:
                status = "warning"
            else:
                status = "critical"

            # Collect issues and recommendations
            issues = []
            recommendations = []
            site_details = {}

            for site_name, audit in audit_results.items():
                compliance_issues = getattr(audit, 'compliance_issues', [])
                if compliance_issues:
                    issues.extend([f"{site_name}: {issue}" for issue in compliance_issues[:2]])

                recommendations.extend([
                    f"{site_name}: Implement robust cookie consent management",
                    f"{site_name}: Enable IP anonymization for GA4"
                ])

                site_details[site_name] = {
                    "gdpr_status": getattr(audit, 'gdpr_status', 'unknown'),
                    "compliance_score": getattr(audit, 'overall_compliance_score', 0),
                    "integration_score": getattr(audit, 'overall_integration_score', 0)
                }

        compliance_component = HealthComponent(
            name="Compliance & Security",
            score=round(compliance_score, 2),
            weight=self.component_weights["compliance"],
            status=status,
            issues=issues[:10],
            recommendations=recommendations[:10],
            metrics={
                "total_sites": total_sites,
                "gdpr_compliant_sites": gdpr_compliant,
                "compliant_sites": compliant_sites,
                "average_compliance_score": sum(getattr(a, 'overall_compliance_score', 0) for a in audit_results.values()) / len(audit_results) if audit_results else 0
            }
        )

        return compliance_component, site_details

    async def _assess_performance_health(self) -> Tuple[HealthComponent, Dict[str, Any]]:
        """Assess performance and monitoring health."""
        logger.debug("Assessing performance health...")

        # Run live verification across sites
        verification_results = []
        for site in self.sites:
            result = await self.live_verifier.verify_analytics_live(
                site['url'],
                site.get('ga4_id'),
                site.get('pixel_id')
            )
            verification_results.append(result)

        # Calculate performance score
        total_sites = len(verification_results)
        verified_sites = sum(1 for result in verification_results
                           if getattr(result, 'verification_status', '') == 'fully_verified')
        partial_sites = sum(1 for result in verification_results
                          if getattr(result, 'verification_status', '') == 'partially_verified')

        perf_score = (
            (verified_sites * 100 + partial_sites * 50) / total_sites
        )

        if perf_score >= 80:
            status = "healthy"
        elif perf_score >= 50:
            status = "warning"
        else:
            status = "critical"

        # Collect issues and recommendations
        issues = []
        recommendations = []
        site_details = {}

        for result in verification_results:
            site_issues = getattr(result, 'issues', [])
            if site_issues:
                issues.extend([f"{result.url}: {issue}" for issue in site_issues[:2]])

            recommendations.append(f"{result.url}: Implement comprehensive analytics tracking")

            site_details[result.url.split('/')[-1]] = {
                "verification_status": getattr(result, 'verification_status', 'unknown'),
                "ga4_active": getattr(result, 'ga4_tracking_active', False),
                "pixel_active": getattr(result, 'pixel_tracking_active', False),
                "confidence_score": getattr(result, 'confidence_score', 0)
            }

        perf_component = HealthComponent(
            name="Performance & Monitoring",
            score=round(perf_score, 2),
            weight=self.component_weights["performance"],
            status=status,
            issues=issues[:10],
            recommendations=recommendations[:10],
            metrics={
                "total_sites": total_sites,
                "verified_sites": verified_sites,
                "partial_sites": partial_sites,
                "average_confidence": sum(getattr(r, 'confidence_score', 0) for r in verification_results) / total_sites
            }
        )

        return perf_component, site_details

    def _calculate_risk_level(self, overall_score: float, components: Dict[str, HealthComponent]) -> str:
        """Calculate risk level based on score and critical components."""
        # Critical components (infrastructure, compliance)
        critical_components = ["infrastructure", "compliance"]
        critical_issues = any(
            components[name].status == "critical"
            for name in critical_components
            if name in components
        )

        if overall_score >= 85 and not critical_issues:
            return "low"
        elif overall_score >= 70 or (overall_score >= 60 and not critical_issues):
            return "medium"
        elif overall_score >= 40 or critical_issues:
            return "high"
        else:
            return "critical"

    def _generate_recommendations(self, components: Dict[str, HealthComponent]) -> List[str]:
        """Generate prioritized recommendations based on component health."""
        recommendations = []

        # Sort components by score (worst first)
        sorted_components = sorted(
            components.items(),
            key=lambda x: x[1].score
        )

        for component_name, component in sorted_components:
            if component.score < 80:
                recommendations.extend([
                    f"Improve {component.name.lower()}: {rec}"
                    for rec in component.recommendations[:2]
                ])

        # Add enterprise-level recommendations
        if all(c.score >= 80 for c in components.values()):
            recommendations.append("Maintain current high-performance standards")
        else:
            recommendations.append("Implement automated monitoring and alerting")
            recommendations.append("Schedule regular health assessments and maintenance")

        return recommendations[:15]  # Limit recommendations

    def _generate_next_steps(self, risk_level: str, components: Dict[str, HealthComponent]) -> List[str]:
        """Generate prioritized next steps based on risk level."""
        next_steps = []

        if risk_level == "critical":
            next_steps.extend([
                "🚨 IMMEDIATE: Address critical infrastructure issues",
                "🚨 IMMEDIATE: Fix compliance violations",
                "🚨 IMMEDIATE: Restore site availability"
            ])
        elif risk_level == "high":
            next_steps.extend([
                "⚠️ HIGH PRIORITY: Complete analytics deployment for remaining sites",
                "⚠️ HIGH PRIORITY: Implement compliance requirements",
                "⚠️ HIGH PRIORITY: Fix infrastructure issues"
            ])
        elif risk_level == "medium":
            next_steps.extend([
                "📋 MEDIUM PRIORITY: Optimize performance issues",
                "📋 MEDIUM PRIORITY: Enhance monitoring capabilities",
                "📋 MEDIUM PRIORITY: Complete partial deployments"
            ])
        else:  # low risk
            next_steps.extend([
                "✅ MAINTENANCE: Regular health monitoring",
                "✅ MAINTENANCE: Performance optimization",
                "✅ MAINTENANCE: Feature enhancements"
            ])

        # Add component-specific next steps
        for component_name, component in components.items():
            if component.status == "critical":
                next_steps.append(f"🔧 FIX CRITICAL: {component.name} - {component.issues[0] if component.issues else 'Review issues'}")
            elif component.status == "warning":
                next_steps.append(f"📈 IMPROVE: {component.name} - {component.recommendations[0] if component.recommendations else 'Review recommendations'}")

        return next_steps[:10]  # Limit next steps


async def main():
    """Command-line interface for health scoring."""
    import argparse

    parser = argparse.ArgumentParser(description="Analytics Ecosystem Health Scorer")
    parser.add_argument("--config", type=str, help="Path to sites configuration JSON")
    parser.add_argument("--output", type=str, help="Output file path")
    parser.add_argument("--json", action="store_true", help="Output JSON format")

    args = parser.parse_args()

    # Default sites configuration
    sites = [
        {"name": "freerideinvestor.com", "url": "https://freerideinvestor.com", "ga4_id": "G-XYZ789GHI5", "pixel_id": "876543210987654"},
        {"name": "tradingrobotplug.com", "url": "https://tradingrobotplug.com", "ga4_id": "G-ABC123DEF4", "pixel_id": "987654321098765"},
        {"name": "dadudekc.com", "url": "https://dadudekc.com"},
        {"name": "crosbyultimateevents.com", "url": "https://crosbyultimateevents.com"}
    ]

    # Initialize scorer
    scorer = AnalyticsEcosystemHealthScorer(sites)

    # Calculate health score
    health_score = await scorer.calculate_ecosystem_health()

    # Output results
    if args.json:
        output = json.dumps(asdict(health_score), indent=2)
    else:
        output = f"""
🩺 ANALYTICS ECOSYSTEM HEALTH ASSESSMENT
==========================================

📊 Overall Score: {health_score.overall_score}/100 ({health_score.risk_level.upper()} RISK)

🏗️ COMPONENT BREAKDOWN:
{chr(10).join(f"  • {comp.name}: {comp.score}/100 ({comp.status})" for comp in health_score.components.values())}

🚨 KEY ISSUES ({len([i for c in health_score.components.values() for i in c.issues])} total):
{chr(10).join(f"  • {issue}" for comp in health_score.components.values() for issue in comp.issues[:2])}

💡 RECOMMENDATIONS:
{chr(10).join(f"  • {rec}" for rec in health_score.recommendations[:5])}

🎯 NEXT STEPS:
{chr(10).join(f"  • {step}" for step in health_score.next_steps)}

📈 SITE BREAKDOWN:
{chr(10).join(f"  • {site}: {data.get('infrastructure', {}).get('status', 'unknown')}" for site, data in health_score.site_breakdown.items())}
"""

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"✅ Health assessment saved to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    asyncio.run(main())