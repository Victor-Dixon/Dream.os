#!/usr/bin/env python3
"""
Enterprise Analytics Compliance & Integration Validator
======================================================

Comprehensive validation of enterprise analytics implementations for GDPR compliance,
conversion tracking, enhanced ecommerce, and integration quality assurance.

Features:
- GDPR compliance validation (cookie consent, data minimization, user rights)
- Conversion tracking verification and optimization
- Enhanced ecommerce implementation validation
- Cross-platform analytics integration testing
- Enterprise analytics audit and compliance reporting
- Automated compliance scoring and recommendations

Author: Agent-3 (Infrastructure & DevOps Specialist)
Created: 2026-01-07
Purpose: Ensure enterprise analytics implementations meet compliance and integration standards
"""

import asyncio
import aiohttp
import json
import re
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from pathlib import Path
from urllib.parse import urlparse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class GDPRComplianceCheck:
    """GDPR compliance validation result."""
    requirement: str
    compliant: bool
    severity: str  # critical, high, medium, low
    findings: List[str]
    recommendations: List[str]
    compliance_score: int  # 0-100

@dataclass
class ConversionTrackingValidation:
    """Conversion tracking validation result."""
    event_type: str
    implemented: bool
    optimized: bool
    issues: List[str]
    recommendations: List[str]
    tracking_score: int  # 0-100

@dataclass
class EcommerceIntegrationCheck:
    """Enhanced ecommerce integration validation."""
    feature: str
    implemented: bool
    configured: bool
    issues: List[str]
    recommendations: List[str]
    integration_score: int  # 0-100

@dataclass
class EnterpriseAnalyticsAudit:
    """Comprehensive enterprise analytics audit result."""
    site_name: str
    timestamp: str
    gdpr_compliance: List[GDPRComplianceCheck]
    conversion_tracking: List[ConversionTrackingValidation]
    ecommerce_integration: List[EcommerceIntegrationCheck]
    overall_compliance_score: int
    overall_integration_score: int
    critical_issues: List[str]
    recommended_actions: List[str]
    audit_summary: Dict[str, Any]

class EnterpriseAnalyticsComplianceValidator:
    """Comprehensive enterprise analytics compliance and integration validator."""

    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.timeout = aiohttp.ClientTimeout(total=30, connect=10)

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def audit_enterprise_analytics(self, site_name: str) -> EnterpriseAnalyticsAudit:
        """Perform comprehensive enterprise analytics audit."""
        audit = EnterpriseAnalyticsAudit(
            site_name=site_name,
            timestamp=datetime.now().isoformat(),
            gdpr_compliance=[],
            conversion_tracking=[],
            ecommerce_integration=[],
            overall_compliance_score=0,
            overall_integration_score=0,
            critical_issues=[],
            recommended_actions=[],
            audit_summary={}
        )

        try:
            # Get site content for analysis
            url = f"https://{site_name}"
            content, status_code = await self._fetch_site_content(url)

            if status_code != 200:
                audit.critical_issues.append(f"Site returned HTTP {status_code} - cannot perform analytics audit")
                audit.recommended_actions.append("Resolve site availability issues before analytics audit")
                return audit

            # GDPR Compliance Checks
            audit.gdpr_compliance = await self._check_gdpr_compliance(content, site_name)

            # Conversion Tracking Validation
            audit.conversion_tracking = self._validate_conversion_tracking(content)

            # Ecommerce Integration Checks
            audit.ecommerce_integration = self._check_ecommerce_integration(content)

            # Calculate overall scores
            audit.overall_compliance_score = self._calculate_compliance_score(audit.gdpr_compliance)
            audit.overall_integration_score = self._calculate_integration_score(audit.conversion_tracking, audit.ecommerce_integration)

            # Generate critical issues and recommendations
            audit.critical_issues, audit.recommended_actions = self._generate_audit_findings(audit)

            # Create audit summary
            audit.audit_summary = self._create_audit_summary(audit)

        except Exception as e:
            logger.error(f"Error during analytics audit for {site_name}: {e}")
            audit.critical_issues.append(f"Audit failed: {str(e)}")
            audit.recommended_actions.append("Review audit error logs and retry analysis")

        return audit

    async def _fetch_site_content(self, url: str) -> Tuple[str, int]:
        """Fetch site content for analysis."""
        try:
            async with self.session.get(url, allow_redirects=True) as response:
                content = await response.text()
                return content, response.status
        except Exception as e:
            logger.error(f"Failed to fetch content from {url}: {e}")
            return "", 0

    async def _check_gdpr_compliance(self, content: str, site_name: str) -> List[GDPRComplianceCheck]:
        """Check GDPR compliance requirements."""
        checks = []

        # Cookie Consent Check
        cookie_consent = GDPRComplianceCheck(
            requirement="Cookie Consent Banner",
            compliant=False,
            severity="critical",
            findings=[],
            recommendations=[],
            compliance_score=0
        )

        consent_patterns = [
            r"cookie.*consent|consent.*cookie",
            r"accept.*cookies|cookies.*accept",
            r"gdpr.*consent|consent.*gdpr",
            r"privacy.*consent|consent.*privacy"
        ]

        has_consent = any(re.search(pattern, content, re.IGNORECASE) for pattern in consent_patterns)

        if has_consent:
            cookie_consent.compliant = True
            cookie_consent.compliance_score = 90
        else:
            cookie_consent.findings.append("No cookie consent mechanism detected")
            cookie_consent.recommendations.extend([
                "Implement cookie consent banner with granular consent options",
                "Include categories: necessary, analytics, marketing, preferences",
                "Store consent preferences with user ID for GDPR compliance"
            ])

        checks.append(cookie_consent)

        # Data Minimization Check
        data_minimization = GDPRComplianceCheck(
            requirement="Data Minimization",
            compliant=True,  # Assume compliant unless excessive tracking detected
            severity="high",
            findings=[],
            recommendations=[],
            compliance_score=80
        )

        # Check for excessive tracking (more than 3 analytics services)
        analytics_services = []
        if 'googletagmanager' in content or 'gtag(' in content:
            analytics_services.append('Google Analytics')
        if 'facebook' in content.lower() and ('fbq(' in content or 'pixel' in content.lower()):
            analytics_services.append('Facebook Pixel')
        if 'linkedin' in content.lower() or 'licdn' in content:
            analytics_services.append('LinkedIn Insight')
        if 'twitter' in content.lower() or 'ads-twitter' in content:
            analytics_services.append('Twitter Ads')

        if len(analytics_services) > 3:
            data_minimization.compliant = False
            data_minimization.compliance_score = 40
            data_minimization.findings.append(f"Excessive tracking services detected: {', '.join(analytics_services)}")
            data_minimization.recommendations.append("Review and minimize analytics services to only necessary ones")

        checks.append(data_minimization)

        # User Rights Implementation
        user_rights = GDPRComplianceCheck(
            requirement="User Rights Implementation",
            compliant=False,
            severity="high",
            findings=[],
            recommendations=[],
            compliance_score=0
        )

        rights_indicators = [
            "delete.*data|data.*delete",
            "access.*data|data.*access",
            "right.*forgotten|forgotten.*right",
            "privacy.*policy|policy.*privacy",
            "data.*subject|subject.*data"
        ]

        has_rights_info = any(re.search(pattern, content, re.IGNORECASE) for pattern in rights_indicators)

        if has_rights_info:
            user_rights.compliant = True
            user_rights.compliance_score = 75
        else:
            user_rights.findings.append("No user rights information or data deletion options detected")
            user_rights.recommendations.extend([
                "Implement data access and deletion request forms",
                "Create privacy policy with user rights information",
                "Add 'Do Not Track' and data minimization options"
            ])

        checks.append(user_rights)

        # Data Processing Documentation
        data_processing = GDPRComplianceCheck(
            requirement="Data Processing Transparency",
            compliant=False,
            severity="medium",
            findings=[],
            recommendations=[],
            compliance_score=0
        )

        transparency_indicators = [
            "data.*processing|processing.*data",
            "personal.*data|data.*personal",
            "information.*collected|collected.*information",
            "privacy.*notice|notice.*privacy"
        ]

        has_transparency = any(re.search(pattern, content, re.IGNORECASE) for pattern in transparency_indicators)

        if has_transparency:
            data_processing.compliant = True
            data_processing.compliance_score = 85
        else:
            data_processing.findings.append("Limited transparency about data processing activities")
            data_processing.recommendations.extend([
                "Add clear privacy notice explaining data collection and processing",
                "Document all data processing purposes and legal basis",
                "Implement data processing inventory and records"
            ])

        checks.append(data_processing)

        return checks

    def _validate_conversion_tracking(self, content: str) -> List[ConversionTrackingValidation]:
        """Validate conversion tracking implementation."""
        validations = []

        # Purchase/Sale Conversion
        purchase_tracking = ConversionTrackingValidation(
            event_type="Purchase/Sale Conversion",
            implemented=False,
            optimized=False,
            issues=[],
            recommendations=[],
            tracking_score=0
        )

        purchase_indicators = [
            "purchase|sale|transaction|conversion",
            "thank.*you|order.*confirmation",
            "checkout.*complete|payment.*success"
        ]

        has_purchase_tracking = any(indicator in content.lower() for indicator in purchase_indicators)

        if has_purchase_tracking:
            purchase_tracking.implemented = True
            purchase_tracking.tracking_score = 70

            # Check for optimized implementation
            if 'gtag(' in content and 'purchase' in content:
                purchase_tracking.optimized = True
                purchase_tracking.tracking_score = 95
            else:
                purchase_tracking.issues.append("Purchase events not properly configured in GA4")
                purchase_tracking.recommendations.append("Implement GA4 purchase events with proper ecommerce parameters")
        else:
            purchase_tracking.issues.append("No purchase conversion tracking detected")
            purchase_tracking.recommendations.append("Implement purchase/sale conversion tracking for revenue attribution")

        validations.append(purchase_tracking)

        # Lead Generation
        lead_tracking = ConversionTrackingValidation(
            event_type="Lead Generation",
            implemented=False,
            optimized=False,
            issues=[],
            recommendations=[],
            tracking_score=0
        )

        lead_indicators = [
            "contact.*form|form.*contact",
            "newsletter.*signup|signup.*newsletter",
            "lead.*capture|capture.*lead",
            "email.*subscription|subscription.*email"
        ]

        has_lead_tracking = any(re.search(pattern, content, re.IGNORECASE) for pattern in lead_indicators)

        if has_lead_tracking:
            lead_tracking.implemented = True
            lead_tracking.tracking_score = 65

            # Check for form submission tracking
            if 'gtag(' in content and ('submit' in content or 'form' in content.lower()):
                lead_tracking.optimized = True
                lead_tracking.tracking_score = 90
            else:
                lead_tracking.issues.append("Lead generation forms not tracked")
                lead_tracking.recommendations.append("Implement form submission tracking for lead attribution")
        else:
            lead_tracking.issues.append("No lead generation tracking detected")
            lead_tracking.recommendations.append("Implement lead capture event tracking")

        validations.append(lead_tracking)

        # Content Engagement
        engagement_tracking = ConversionTrackingValidation(
            event_type="Content Engagement",
            implemented=False,
            optimized=False,
            issues=[],
            recommendations=[],
            tracking_score=0
        )

        engagement_indicators = [
            "scroll.*depth|depth.*scroll",
            "time.*page|page.*time",
            "engagement.*rate|rate.*engagement"
        ]

        has_engagement_tracking = any(re.search(pattern, content, re.IGNORECASE) for pattern in engagement_indicators)

        if has_engagement_tracking:
            engagement_tracking.implemented = True
            engagement_tracking.tracking_score = 75
            engagement_tracking.optimized = True
        else:
            engagement_tracking.issues.append("Limited content engagement tracking")
            engagement_tracking.recommendations.extend([
                "Implement scroll depth tracking",
                "Add time-on-page tracking",
                "Configure content engagement goals"
            ])

        validations.append(engagement_tracking)

        return validations

    def _check_ecommerce_integration(self, content: str) -> List[EcommerceIntegrationCheck]:
        """Check enhanced ecommerce integration."""
        checks = []

        # Product Impressions
        impressions = EcommerceIntegrationCheck(
            feature="Product Impressions",
            implemented=False,
            configured=False,
            issues=[],
            recommendations=[],
            integration_score=0
        )

        if 'impressions' in content.lower() or 'view_item_list' in content:
            impressions.implemented = True
            impressions.configured = True
            impressions.integration_score = 90
        else:
            impressions.issues.append("Product impression tracking not implemented")
            impressions.recommendations.append("Implement product impression tracking for catalog performance")

        checks.append(impressions)

        # Product Clicks
        clicks = EcommerceIntegrationCheck(
            feature="Product Clicks",
            implemented=False,
            configured=False,
            issues=[],
            recommendations=[],
            integration_score=0
        )

        if 'select_item' in content or 'product_click' in content.lower():
            clicks.implemented = True
            clicks.configured = True
            clicks.integration_score = 90
        else:
            clicks.issues.append("Product click tracking not implemented")
            clicks.recommendations.append("Implement product click tracking for user journey analysis")

        checks.append(clicks)

        # Add to Cart
        add_to_cart = EcommerceIntegrationCheck(
            feature="Add to Cart",
            implemented=False,
            configured=False,
            issues=[],
            recommendations=[],
            integration_score=0
        )

        if 'add_to_cart' in content:
            add_to_cart.implemented = True
            add_to_cart.configured = True
            add_to_cart.integration_score = 90
        else:
            add_to_cart.issues.append("Add to cart tracking not implemented")
            add_to_cart.recommendations.append("Implement add to cart event tracking")

        checks.append(add_to_cart)

        # Checkout Process
        checkout = EcommerceIntegrationCheck(
            feature="Checkout Process",
            implemented=False,
            configured=False,
            issues=[],
            recommendations=[],
            integration_score=0
        )

        checkout_steps = ['begin_checkout', 'checkout_progress', 'purchase']
        implemented_steps = [step for step in checkout_steps if step in content]

        if implemented_steps:
            checkout.implemented = True
            checkout.integration_score = min(95, 60 + (len(implemented_steps) * 15))

            if len(implemented_steps) < len(checkout_steps):
                missing_steps = [step for step in checkout_steps if step not in implemented_steps]
                checkout.issues.append(f"Missing checkout steps: {', '.join(missing_steps)}")
                checkout.recommendations.append("Implement complete checkout funnel tracking")
        else:
            checkout.issues.append("No checkout process tracking implemented")
            checkout.recommendations.append("Implement checkout funnel tracking from begin_checkout to purchase")

        checks.append(checkout)

        return checks

    def _calculate_compliance_score(self, gdpr_checks: List[GDPRComplianceCheck]) -> int:
        """Calculate overall GDPR compliance score."""
        if not gdpr_checks:
            return 0

        total_score = sum(check.compliance_score for check in gdpr_checks)
        return total_score // len(gdpr_checks)

    def _calculate_integration_score(self, conversion_checks: List[ConversionTrackingValidation],
                                   ecommerce_checks: List[EcommerceIntegrationCheck]) -> int:
        """Calculate overall integration score."""
        all_checks = conversion_checks + ecommerce_checks
        if not all_checks:
            return 0

        total_score = sum(check.tracking_score if hasattr(check, 'tracking_score')
                         else check.integration_score for check in all_checks)
        return total_score // len(all_checks)

    def _generate_audit_findings(self, audit: EnterpriseAnalyticsAudit) -> Tuple[List[str], List[str]]:
        """Generate critical issues and recommended actions from audit."""
        critical_issues = []
        recommended_actions = []

        # Check compliance issues
        for check in audit.gdpr_compliance:
            if check.severity == "critical" and not check.compliant:
                critical_issues.extend(check.findings)
                recommended_actions.extend(check.recommendations)

        # Check for low compliance scores
        if audit.overall_compliance_score < 70:
            critical_issues.append(f"Low GDPR compliance score: {audit.overall_compliance_score}%")
            recommended_actions.append("Conduct comprehensive GDPR compliance audit")

        # Check integration issues
        for check in audit.conversion_tracking + audit.ecommerce_integration:
            issues = check.issues if hasattr(check, 'issues') else []
            recommendations = check.recommendations if hasattr(check, 'recommendations') else []

            if issues:
                critical_issues.extend(issues)
            if recommendations:
                recommended_actions.extend(recommendations)

        # Deduplicate
        critical_issues = list(set(critical_issues))
        recommended_actions = list(set(recommended_actions))

        return critical_issues, recommended_actions

    def _create_audit_summary(self, audit: EnterpriseAnalyticsAudit) -> Dict[str, Any]:
        """Create audit summary statistics."""
        return {
            "site_name": audit.site_name,
            "audit_timestamp": audit.timestamp,
            "compliance_score": audit.overall_compliance_score,
            "integration_score": audit.overall_integration_score,
            "gdpr_checks_passed": sum(1 for check in audit.gdpr_compliance if check.compliant),
            "gdpr_checks_total": len(audit.gdpr_compliance),
            "conversion_events_implemented": sum(1 for check in audit.conversion_tracking if check.implemented),
            "conversion_events_total": len(audit.conversion_tracking),
            "ecommerce_features_implemented": sum(1 for check in audit.ecommerce_integration if check.implemented),
            "ecommerce_features_total": len(audit.ecommerce_integration),
            "critical_issues_count": len(audit.critical_issues),
            "recommended_actions_count": len(audit.recommended_actions)
        }

    async def audit_multiple_sites(self, sites: List[str]) -> List[EnterpriseAnalyticsAudit]:
        """Audit multiple sites concurrently."""
        tasks = [self.audit_enterprise_analytics(site) for site in sites]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter valid results
        valid_results = [r for r in results if isinstance(r, EnterpriseAnalyticsAudit)]
        return valid_results

    def generate_compliance_report(self, audits: List[EnterpriseAnalyticsAudit]) -> Dict[str, Any]:
        """Generate comprehensive compliance report."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "sites_audited": len(audits),
                "average_compliance_score": 0,
                "average_integration_score": 0,
                "sites_gdpr_compliant": 0,
                "sites_fully_integrated": 0
            },
            "site_reports": [asdict(audit) for audit in audits],
            "compliance_trends": {},
            "critical_findings": [],
            "enterprise_recommendations": []
        }

        if audits:
            total_compliance = sum(audit.overall_compliance_score for audit in audits)
            total_integration = sum(audit.overall_integration_score for audit in audits)

            report["summary"]["average_compliance_score"] = total_compliance // len(audits)
            report["summary"]["average_integration_score"] = total_integration // len(audits)

            # Count compliant sites (score >= 80)
            report["summary"]["sites_gdpr_compliant"] = sum(
                1 for audit in audits if audit.overall_compliance_score >= 80
            )

            # Count fully integrated sites (score >= 85)
            report["summary"]["sites_fully_integrated"] = sum(
                1 for audit in audits if audit.overall_integration_score >= 85
            )

        # Collect all critical findings
        for audit in audits:
            report["critical_findings"].extend(audit.critical_issues)
            report["enterprise_recommendations"].extend(audit.recommended_actions)

        # Deduplicate
        report["critical_findings"] = list(set(report["critical_findings"]))
        report["enterprise_recommendations"] = list(set(report["enterprise_recommendations"]))

        return report

# CLI interface
async def main():
    """Main CLI interface for enterprise analytics compliance validation."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Enterprise Analytics Compliance & Integration Validator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/enterprise_analytics_compliance_validator.py --site freerideinvestor.com
  python tools/enterprise_analytics_compliance_validator.py --p0-sites --json
  python tools/enterprise_analytics_compliance_validator.py --sites sites.txt --report
        """
    )

    parser.add_argument('--site', help='Audit single site')
    parser.add_argument('--sites', help='File containing list of sites to audit')
    parser.add_argument('--p0-sites', action='store_true', help='Audit all P0 sites')
    parser.add_argument('--json', action='store_true', help='Output results as JSON')
    parser.add_argument('--report', action='store_true', help='Generate detailed HTML report')
    parser.add_argument('--quiet', action='store_true', help='Suppress detailed output')

    args = parser.parse_args()

    # Define P0 sites
    p0_sites = [
        "freerideinvestor.com",
        "tradingrobotplug.com",
        "dadudekc.com",
        "crosbyultimateevents.com"
    ]

    # Determine sites to audit
    sites = []
    if args.site:
        sites = [args.site]
    elif args.sites:
        try:
            with open(args.sites, 'r') as f:
                sites = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"❌ Error: File {args.sites} not found")
            sys.exit(1)
    elif args.p0_sites:
        sites = p0_sites
    else:
        parser.error("Must specify --site, --sites, or --p0-sites")

    async with EnterpriseAnalyticsComplianceValidator() as validator:
        try:
            audits = await validator.audit_multiple_sites(sites)

            if args.json:
                report = validator.generate_compliance_report(audits)
                print(json.dumps(report, indent=2))
            elif args.report:
                report = validator.generate_compliance_report(audits)
                await generate_html_report(report)
            else:
                # Console output
                print("🏢 Enterprise Analytics Compliance Audit Results")
                print("=" * 60)

                for audit in audits:
                    print(f"\n🏢 {audit.site_name}")
                    print(f"   Compliance Score: {audit.overall_compliance_score}/100")
                    print(f"   Integration Score: {audit.overall_integration_score}/100")

                    if audit.overall_compliance_score >= 80:
                        print("   GDPR Status: ✅ Compliant")
                    elif audit.overall_compliance_score >= 60:
                        print("   GDPR Status: ⚠️ Needs Improvement")
                    else:
                        print("   GDPR Status: ❌ Non-Compliant")

                    if audit.overall_integration_score >= 85:
                        print("   Integration: ✅ Fully Integrated")
                    elif audit.overall_integration_score >= 70:
                        print("   Integration: ⚠️ Partially Integrated")
                    else:
                        print("   Integration: ❌ Poor Integration")

                    if audit.critical_issues:
                        print(f"   Critical Issues: {len(audit.critical_issues)}")
                        for issue in audit.critical_issues[:2]:  # Show top 2
                            print(f"     • {issue}")

                    if audit.recommended_actions:
                        print(f"   Recommendations: {len(audit.recommended_actions)}")
                        for action in audit.recommended_actions[:2]:  # Show top 2
                            print(f"     • {action}")

                # Summary
                if audits:
                    avg_compliance = sum(a.overall_compliance_score for a in audits) // len(audits)
                    avg_integration = sum(a.overall_integration_score for a in audits) // len(audits)

                    gdpr_compliant = sum(1 for a in audits if a.overall_compliance_score >= 80)
                    fully_integrated = sum(1 for a in audits if a.overall_integration_score >= 85)

                    print("\n📊 Enterprise Summary:")
                    print(f"   Sites Audited: {len(audits)}")
                    print(f"   Average Compliance: {avg_compliance:.1f}%")
                    print(f"   Average Integration: {avg_integration:.1f}%")
                    print(f"   GDPR Compliant Sites: {gdpr_compliant}/{len(audits)}")
                    print(f"   Fully Integrated Sites: {fully_integrated}/{len(audits)}")

        except KeyboardInterrupt:
            print("\n⚠️  Audit interrupted by user")
        except Exception as e:
            print(f"\n❌ Unexpected error: {str(e)}")
            sys.exit(1)

async def generate_html_report(report: Dict[str, Any]) -> None:
    """Generate HTML compliance report."""
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Enterprise Analytics Compliance Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .compliant {{ color: green; font-weight: bold; }}
        .warning {{ color: orange; font-weight: bold; }}
        .non-compliant {{ color: red; font-weight: bold; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .issues {{ background-color: #fff3cd; padding: 10px; margin: 10px 0; }}
        .recommendations {{ background-color: #d1ecf1; padding: 10px; margin: 10px 0; }}
        .score-high {{ color: green; }}
        .score-medium {{ color: orange; }}
        .score-low {{ color: red; }}
    </style>
</head>
<body>
    <h1>🏢 Enterprise Analytics Compliance Report</h1>
    <p><strong>Generated:</strong> {report['timestamp']}</p>

    <h2>Executive Summary</h2>
    <ul>
        <li><strong>Sites Audited:</strong> {report['summary']['sites_audited']}</li>
        <li><strong>Average Compliance Score:</strong> <span class="score-high">{report['summary']['average_compliance_score']}%</span></li>
        <li><strong>Average Integration Score:</strong> <span class="score-high">{report['summary']['average_integration_score']}%</span></li>
        <li><strong>GDPR Compliant Sites:</strong> <span class="compliant">{report['summary']['sites_gdpr_compliant']}</span></li>
        <li><strong>Fully Integrated Sites:</strong> <span class="compliant">{report['summary']['sites_fully_integrated']}</span></li>
    </ul>

    <h2>Critical Findings</h2>
    <div class="issues">
        <ul>
"""

    for finding in report.get('critical_findings', []):
        html_content += f"<li>{finding}</li>"

    html_content += """
        </ul>
    </div>

    <h2>Enterprise Recommendations</h2>
    <div class="recommendations">
        <ul>
"""

    for rec in report.get('enterprise_recommendations', []):
        html_content += f"<li>{rec}</li>"

    html_content += """
        </ul>
    </div>

    <h2>Detailed Site Reports</h2>
    <table>
        <tr>
            <th>Site</th>
            <th>Compliance Score</th>
            <th>Integration Score</th>
            <th>GDPR Status</th>
            <th>Integration Status</th>
            <th>Critical Issues</th>
        </tr>
"""

    for audit in report.get('site_reports', []):
        compliance_class = "score-high" if audit['overall_compliance_score'] >= 80 else "score-medium" if audit['overall_compliance_score'] >= 60 else "score-low"
        integration_class = "score-high" if audit['overall_integration_score'] >= 85 else "score-medium" if audit['overall_integration_score'] >= 70 else "score-low"

        gdpr_status = "✅ Compliant" if audit['overall_compliance_score'] >= 80 else "⚠️ Needs Work" if audit['overall_compliance_score'] >= 60 else "❌ Non-Compliant"
        integration_status = "✅ Fully Integrated" if audit['overall_integration_score'] >= 85 else "⚠️ Partially" if audit['overall_integration_score'] >= 70 else "❌ Poor"

        html_content += f"""
        <tr>
            <td>{audit['site_name']}</td>
            <td class="{compliance_class}">{audit['overall_compliance_score']}%</td>
            <td class="{integration_class}">{audit['overall_integration_score']}%</td>
            <td>{gdpr_status}</td>
            <td>{integration_status}</td>
            <td>{len(audit['critical_issues'])}</td>
        </tr>
"""

    html_content += """
    </table>
</body>
</html>
"""

    # Save report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"enterprise_analytics_compliance_report_{timestamp}.html"

    with open(filename, 'w') as f:
        f.write(html_content)

    print(f"📄 HTML report saved: {filename}")

if __name__ == "__main__":
    asyncio.run(main())