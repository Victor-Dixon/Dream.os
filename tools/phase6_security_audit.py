#!/usr/bin/env python3
"""
Phase 6 Security Audit Tool
Comprehensive security assessment for enterprise infrastructure
"""

import json
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import argparse
import sys
from pathlib import Path
import re

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class SecurityFinding:
    """Security finding data structure"""
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW, INFO
    category: str  # ssl, auth, network, code, config
    title: str
    description: str
    recommendation: str
    affected_components: List[str]
    evidence: Dict[str, Any]
    timestamp: str

@dataclass
class SecurityAuditReport:
    """Comprehensive security audit report"""
    audit_timestamp: str
    overall_security_score: int  # 0-100
    total_findings: int
    critical_findings: int
    high_findings: int
    medium_findings: int
    low_findings: int
    info_findings: int
    findings: List[SecurityFinding]
    recommendations: List[str]
    compliance_status: Dict[str, bool]

class Phase6SecurityAuditor:
    """Enterprise security auditor for Phase 6 infrastructure"""

    def __init__(self):
        self.findings = []
        self.start_time = datetime.now()

    def audit_ssl_configuration(self) -> List[SecurityFinding]:
        """Audit SSL/TLS configuration"""
        findings = []

        try:
            # Check SSL certificate files
            ssl_paths = ['cert.pem', 'key.pem', 'ssl/ssl-config.sh']
            for path in ssl_paths:
                if not Path(path).exists():
                    findings.append(SecurityFinding(
                        severity="HIGH",
                        category="ssl",
                        title="Missing SSL Certificate",
                        description=f"SSL certificate file not found: {path}",
                        recommendation="Generate and deploy SSL certificates immediately",
                        affected_components=["nginx", "ssl_termination"],
                        evidence={"missing_file": path},
                        timestamp=datetime.now().isoformat()
                    ))
                else:
                    findings.append(SecurityFinding(
                        severity="INFO",
                        category="ssl",
                        title="SSL Certificate Present",
                        description=f"SSL certificate file found: {path}",
                        recommendation="Verify certificate validity and expiration",
                        affected_components=["ssl_termination"],
                        evidence={"file_exists": path},
                        timestamp=datetime.now().isoformat()
                    ))

            # Check nginx SSL configuration
            nginx_conf = Path('nginx/nginx.conf')
            if nginx_conf.exists():
                with open(nginx_conf, 'r') as f:
                    nginx_content = f.read()

                # Check for SSL protocols
                if 'ssl_protocols' not in nginx_content:
                    findings.append(SecurityFinding(
                        severity="MEDIUM",
                        category="ssl",
                        title="SSL Protocol Not Specified",
                        description="SSL protocols not explicitly configured in nginx",
                        recommendation="Configure ssl_protocols TLSv1.2 TLSv1.3;",
                        affected_components=["nginx"],
                        evidence={"config_file": "nginx/nginx.conf"},
                        timestamp=datetime.now().isoformat()
                    ))

                # Check for HSTS
                if 'Strict-Transport-Security' not in nginx_content:
                    findings.append(SecurityFinding(
                        severity="MEDIUM",
                        category="ssl",
                        title="HSTS Not Configured",
                        description="HTTP Strict Transport Security not enabled",
                        recommendation="Add HSTS header to SSL configuration",
                        affected_components=["nginx"],
                        evidence={"config_file": "nginx/nginx.conf"},
                        timestamp=datetime.now().isoformat()
                    ))

        except Exception as e:
            findings.append(SecurityFinding(
                severity="MEDIUM",
                category="ssl",
                title="SSL Audit Error",
                description=f"Error during SSL audit: {str(e)}",
                recommendation="Review SSL configuration manually",
                affected_components=["ssl_audit"],
                evidence={"error": str(e)},
                timestamp=datetime.now().isoformat()
            ))

        return findings

    def audit_authentication(self) -> List[SecurityFinding]:
        """Audit authentication and authorization"""
        findings = []

        try:
            # Check for JWT configuration
            docker_compose = Path('docker-compose.yml')
            if docker_compose.exists():
                with open(docker_compose, 'r') as f:
                    compose_content = f.read()

                if 'JWT_SECRET' not in compose_content and 'jwt' not in compose_content.lower():
                    findings.append(SecurityFinding(
                        severity="HIGH",
                        category="auth",
                        title="JWT Authentication Not Configured",
                        description="No JWT authentication found in container configuration",
                        recommendation="Implement JWT-based authentication for API endpoints",
                        affected_components=["fastapi", "authentication"],
                        evidence={"config_file": "docker-compose.yml"},
                        timestamp=datetime.now().isoformat()
                    ))

            # Check for RBAC in configuration
            if 'rbac' not in compose_content.lower() and 'role' not in compose_content.lower():
                findings.append(SecurityFinding(
                    severity="MEDIUM",
                    category="auth",
                    title="RBAC Not Configured",
                    description="Role-Based Access Control not implemented",
                    recommendation="Implement RBAC for user authorization",
                    affected_components=["fastapi", "authorization"],
                    evidence={"config_file": "docker-compose.yml"},
                    timestamp=datetime.now().isoformat()
                ))

        except Exception as e:
            findings.append(SecurityFinding(
                severity="MEDIUM",
                category="auth",
                title="Authentication Audit Error",
                description=f"Error during authentication audit: {str(e)}",
                recommendation="Review authentication configuration manually",
                affected_components=["auth_audit"],
                evidence={"error": str(e)},
                timestamp=datetime.now().isoformat()
            ))

        return findings

    def audit_network_security(self) -> List[SecurityFinding]:
        """Audit network security configuration"""
        findings = []

        try:
            # Check nginx configuration for security headers
            nginx_conf = Path('nginx/nginx.conf')
            if nginx_conf.exists():
                with open(nginx_conf, 'r') as f:
                    nginx_content = f.read()

                security_headers = [
                    'X-Frame-Options',
                    'X-Content-Type-Options',
                    'X-XSS-Protection',
                    'Content-Security-Policy'
                ]

                for header in security_headers:
                    if header not in nginx_content:
                        findings.append(SecurityFinding(
                            severity="MEDIUM",
                            category="network",
                            title=f"Missing Security Header: {header}",
                            description=f"Security header {header} not configured",
                            recommendation=f"Add {header} header to nginx configuration",
                            affected_components=["nginx", "security_headers"],
                            evidence={"header": header, "config_file": "nginx/nginx.conf"},
                            timestamp=datetime.now().isoformat()
                        ))

                # Check for rate limiting
                if 'limit_req' not in nginx_content:
                    findings.append(SecurityFinding(
                        severity="HIGH",
                        category="network",
                        title="Rate Limiting Not Configured",
                        description="No rate limiting configured for API endpoints",
                        recommendation="Implement rate limiting to prevent DoS attacks",
                        affected_components=["nginx", "rate_limiting"],
                        evidence={"config_file": "nginx/nginx.conf"},
                        timestamp=datetime.now().isoformat()
                    ))

        except Exception as e:
            findings.append(SecurityFinding(
                severity="MEDIUM",
                category="network",
                title="Network Security Audit Error",
                description=f"Error during network security audit: {str(e)}",
                recommendation="Review network security configuration manually",
                affected_components=["network_audit"],
                evidence={"error": str(e)},
                timestamp=datetime.now().isoformat()
            ))

        return findings

    def audit_configuration_security(self) -> List[SecurityFinding]:
        """Audit configuration security"""
        findings = []

        try:
            # Check for hardcoded secrets
            files_to_check = [
                'docker-compose.yml',
                'nginx/nginx.conf',
                'src/**/*.py'
            ]

            secret_patterns = [
                r'password\s*[:=]\s*[^$]',
                r'secret\s*[:=]\s*[^$]',
                r'key\s*[:=]\s*[^$]',
                r'token\s*[:=]\s*[^$]'
            ]

            for file_pattern in files_to_check:
                if '**' in file_pattern:
                    # Handle glob patterns
                    continue
                else:
                    file_path = Path(file_pattern)
                    if file_path.exists():
                        with open(file_path, 'r') as f:
                            content = f.read()

                        for pattern in secret_patterns:
                            matches = re.findall(pattern, content, re.IGNORECASE)
                            if matches:
                                findings.append(SecurityFinding(
                                    severity="CRITICAL",
                                    category="config",
                                    title="Potential Hardcoded Secret",
                                    description=f"Possible hardcoded secret found in {file_pattern}",
                                    recommendation="Use environment variables or secret management",
                                    affected_components=["configuration", file_pattern],
                                    evidence={"file": file_pattern, "pattern": pattern},
                                    timestamp=datetime.now().isoformat()
                                ))

            # Check environment file
            env_file = Path('.env')
            if env_file.exists():
                findings.append(SecurityFinding(
                    severity="INFO",
                    category="config",
                    title="Environment File Present",
                    description="Environment file found - ensure not committed to version control",
                    recommendation="Verify .env is in .gitignore",
                    affected_components=["environment"],
                    evidence={"file": ".env"},
                    timestamp=datetime.now().isoformat()
                ))

        except Exception as e:
            findings.append(SecurityFinding(
                severity="MEDIUM",
                category="config",
                title="Configuration Security Audit Error",
                description=f"Error during configuration security audit: {str(e)}",
                recommendation="Review configuration security manually",
                affected_components=["config_audit"],
                evidence={"error": str(e)},
                timestamp=datetime.now().isoformat()
            ))

        return findings

    async def run_comprehensive_audit(self) -> SecurityAuditReport:
        """Run comprehensive security audit"""
        logger.info("🔍 Starting comprehensive security audit...")

        # Run all audit categories
        ssl_findings = self.audit_ssl_configuration()
        auth_findings = self.audit_authentication()
        network_findings = self.audit_network_security()
        config_findings = self.audit_configuration_security()

        all_findings = ssl_findings + auth_findings + network_findings + config_findings
        self.findings = all_findings

        # Calculate security score
        severity_weights = {
            "CRITICAL": 100,
            "HIGH": 75,
            "MEDIUM": 50,
            "LOW": 25,
            "INFO": 0
        }

        total_weight = 0
        actual_weight = 0

        for finding in all_findings:
            weight = severity_weights.get(finding.severity, 0)
            total_weight += weight
            if finding.severity != "INFO":
                actual_weight += weight

        # Security score (higher is better)
        max_possible_weight = len(all_findings) * 100
        security_score = 100 - int((actual_weight / max_possible_weight) * 100) if max_possible_weight > 0 else 100

        # Count findings by severity
        severity_counts = {
            "CRITICAL": len([f for f in all_findings if f.severity == "CRITICAL"]),
            "HIGH": len([f for f in all_findings if f.severity == "HIGH"]),
            "MEDIUM": len([f for f in all_findings if f.severity == "MEDIUM"]),
            "LOW": len([f for f in all_findings if f.severity == "LOW"]),
            "INFO": len([f for f in all_findings if f.severity == "INFO"])
        }

        # Generate recommendations
        recommendations = []
        if severity_counts["CRITICAL"] > 0:
            recommendations.append("🚨 IMMEDIATE: Address all CRITICAL security findings")
        if severity_counts["HIGH"] > 0:
            recommendations.append("⚠️  PRIORITY: Address HIGH severity security issues")
        if severity_counts["MEDIUM"] > 0:
            recommendations.append("📋 TODO: Review MEDIUM severity findings")
        recommendations.append("🔄 MONITOR: Regular security audits recommended")
        recommendations.append("📚 TRAINING: Security awareness training for team")

        # Compliance status
        compliance_status = {
            "ssl_configured": len([f for f in ssl_findings if f.severity == "INFO"]) > 0,
            "auth_implemented": len([f for f in auth_findings if f.severity == "HIGH"]) == 0,
            "network_secured": len([f for f in network_findings if f.severity == "HIGH"]) == 0,
            "config_secure": len([f for f in config_findings if f.severity == "CRITICAL"]) == 0
        }

        report = SecurityAuditReport(
            audit_timestamp=datetime.now().isoformat(),
            overall_security_score=max(0, security_score),
            total_findings=len(all_findings),
            critical_findings=severity_counts["CRITICAL"],
            high_findings=severity_counts["HIGH"],
            medium_findings=severity_counts["MEDIUM"],
            low_findings=severity_counts["LOW"],
            info_findings=severity_counts["INFO"],
            findings=all_findings,
            recommendations=recommendations,
            compliance_status=compliance_status
        )

        execution_time = (datetime.now() - self.start_time).total_seconds()
        logger.info(f"✅ Security audit completed in {execution_time:.2f} seconds")

        return report

    def print_audit_report(self, report: SecurityAuditReport):
        """Print comprehensive security audit report"""
        print("\n" + "="*100)
        print("🔒 PHASE 6 ENTERPRISE SECURITY AUDIT REPORT")
        print("="*100)

        print(f"📊 OVERALL SECURITY SCORE: {report.overall_security_score}/100")
        print(f"🔍 TOTAL FINDINGS: {report.total_findings}")
        print(f"🚨 CRITICAL: {report.critical_findings}")
        print(f"⚠️  HIGH: {report.high_findings}")
        print(f"📋 MEDIUM: {report.medium_findings}")
        print(f"ℹ️  LOW: {report.low_findings}")
        print(f"✅ INFO: {report.info_findings}")

        print("\n" + "-"*100)
        print("📋 SECURITY FINDINGS")
        print("-"*100)

        severity_order = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]
        severity_emojis = {
            "CRITICAL": "🚨",
            "HIGH": "⚠️",
            "MEDIUM": "📋",
            "LOW": "ℹ️",
            "INFO": "✅"
        }

        for severity in severity_order:
            severity_findings = [f for f in report.findings if f.severity == severity]
            if severity_findings:
                print(f"\n{severity_emojis[severity]} {severity} SEVERITY ({len(severity_findings)} findings):")
                for finding in severity_findings:
                    print(f"  • {finding.title}")
                    print(f"    {finding.description}")
                    print(f"    💡 {finding.recommendation}")

        print("\n" + "-"*100)
        print("🎯 COMPLIANCE STATUS")
        print("-"*100)
        for component, compliant in report.compliance_status.items():
            status = "✅ PASS" if compliant else "❌ FAIL"
            print(f"{status} {component.replace('_', ' ').title()}")

        print("\n" + "-"*100)
        print("💡 RECOMMENDATIONS")
        print("-"*100)
        for rec in report.recommendations:
            print(f"• {rec}")

        print("\n" + "="*100)

    def save_audit_report(self, report: SecurityAuditReport, filename: str = None):
        """Save security audit report to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"phase6_security_audit_{timestamp}.json"

        # Convert findings to dictionaries
        report_dict = asdict(report)
        report_dict["findings"] = [asdict(finding) for finding in report.findings]

        with open(filename, 'w') as f:
            json.dump(report_dict, f, indent=2, default=str)

        logger.info(f"💾 Security audit report saved to: {filename}")

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Phase 6 Enterprise Security Audit Tool')
    parser.add_argument('--output', type=str, help='Output filename for security audit report')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--category', choices=['all', 'ssl', 'auth', 'network', 'config'],
                       default='all', help='Audit category to focus on')

    args = parser.parse_args()

    # Set logging level based on verbose flag
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    auditor = Phase6SecurityAuditor()

    try:
        logger.info("🔒 Starting Phase 6 Enterprise Security Audit...")
        report = asyncio.run(auditor.run_comprehensive_audit())
        auditor.print_audit_report(report)
        auditor.save_audit_report(report, args.output)

        # Provide actionable summary
        critical_issues = report.critical_findings + report.high_findings
        logger.info(f"✅ Security audit complete - {critical_issues} critical/high priority issues found")
        print(f"\n🔒 Summary: Security Score {report.overall_security_score}/100 - {critical_issues} critical/high issues, {report.medium_findings} medium issues")

        # Exit with code based on security score
        if report.overall_security_score >= 90:
            logger.info("✅ Excellent security posture")
            sys.exit(0)  # Excellent
        elif report.overall_security_score >= 75:
            logger.info("⚠️ Good security with minor issues")
            sys.exit(1)  # Good with issues
        elif report.overall_security_score >= 60:
            logger.warning("⚠️ Security needs attention")
            sys.exit(2)  # Needs attention
        else:
            logger.error("🚨 Critical security issues found")
            sys.exit(3)  # Critical issues

    except KeyboardInterrupt:
        logger.info("Security audit interrupted by user")
        print("\n👋 Security audit interrupted")
        sys.exit(130)

    except Exception as e:
        logger.error(f"Security audit failed: {e}")
        print(f"\n❌ Security audit failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()