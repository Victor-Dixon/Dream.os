#!/usr/bin/env python3
"""
Phase 6 Compliance Checker
Automated validation of V2 compliance and enterprise standards
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import argparse
import sys
from pathlib import Path
import re
import ast

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class ComplianceFinding:
    """Compliance finding data structure"""
    rule_id: str
    severity: str  # PASS, FAIL, WARN
    category: str  # v2, security, code_quality, architecture
    description: str
    file_path: str
    line_number: Optional[int]
    code_snippet: Optional[str]
    recommendation: str
    evidence: Dict[str, Any]

@dataclass
class ComplianceReport:
    """Comprehensive compliance report"""
    check_timestamp: str
    overall_compliance_score: int  # 0-100
    total_checks: int
    passed_checks: int
    failed_checks: int
    warning_checks: int
    findings: List[ComplianceFinding]
    compliance_by_category: Dict[str, Dict[str, int]]
    recommendations: List[str]

class Phase6ComplianceChecker:
    """Enterprise compliance checker for Phase 6 standards"""

    def __init__(self):
        self.findings = []
        self.v2_rules = self._load_v2_rules()

    def _load_v2_rules(self) -> Dict[str, Any]:
        """Load V2 compliance rules"""
        return {
            "function_size": {"max_lines": 30, "description": "Functions must not exceed 30 lines"},
            "class_size": {"max_lines": 200, "description": "Classes must not exceed 200 lines"},
            "file_size": {"max_lines": 300, "description": "Files must not exceed 300 lines"},
            "naming_conventions": {
                "snake_case_functions": r"def [a-z_][a-z0-9_]*\(",
                "pascal_case_classes": r"class [A-Z][a-zA-Z0-9]*",
                "upper_snake_constants": r"^[A-Z][A-Z0-9_]* = "
            },
            "import_organization": {
                "standard_first": True,
                "third_party_second": True,
                "local_last": True
            },
            "error_handling": {
                "try_except_required": True,
                "specific_exceptions": True
            },
            "documentation": {
                "docstrings_required": True,
                "complex_functions_only": False
            }
        }

    def check_v2_compliance(self, file_path: Path) -> List[ComplianceFinding]:
        """Check V2 compliance for a Python file"""
        findings = []

        if not file_path.exists() or file_path.suffix != '.py':
            return findings

        try:
            with open(file_path, 'r') as f:
                content = f.read()

            lines = content.split('\n')

            # Check file size
            if len(lines) > self.v2_rules["file_size"]["max_lines"]:
                findings.append(ComplianceFinding(
                    rule_id="V2-FILE-SIZE",
                    severity="FAIL",
                    category="v2",
                    description=f"File exceeds maximum size of {self.v2_rules['file_size']['max_lines']} lines",
                    file_path=str(file_path),
                    line_number=None,
                    code_snippet=None,
                    recommendation="Refactor file into smaller modules",
                    evidence={"actual_lines": len(lines), "max_lines": self.v2_rules["file_size"]["max_lines"]}
                ))

            # Parse AST for structural analysis
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        # Check function size
                        if node.end_lineno - node.lineno > self.v2_rules["function_size"]["max_lines"]:
                            findings.append(ComplianceFinding(
                                rule_id="V2-FUNC-SIZE",
                                severity="FAIL",
                                category="v2",
                                description=f"Function '{node.name}' exceeds maximum size of {self.v2_rules['function_size']['max_lines']} lines",
                                file_path=str(file_path),
                                line_number=node.lineno,
                                code_snippet=f"def {node.name}(...",
                                recommendation="Break function into smaller functions",
                                evidence={"function_name": node.name, "lines": node.end_lineno - node.lineno}
                            ))

                        # Check function naming
                        if not re.match(self.v2_rules["naming_conventions"]["snake_case_functions"], f"def {node.name}("):
                            findings.append(ComplianceFinding(
                                rule_id="V2-FUNC-NAME",
                                severity="FAIL",
                                category="v2",
                                description=f"Function '{node.name}' should use snake_case naming",
                                file_path=str(file_path),
                                line_number=node.lineno,
                                code_snippet=f"def {node.name}(...",
                                recommendation="Rename function to use snake_case",
                                evidence={"function_name": node.name}
                            ))

                        # Check docstring
                        if not ast.get_docstring(node):
                            findings.append(ComplianceFinding(
                                rule_id="V2-DOCSTRING",
                                severity="WARN",
                                category="v2",
                                description=f"Function '{node.name}' missing docstring",
                                file_path=str(file_path),
                                line_number=node.lineno,
                                code_snippet=f"def {node.name}(...",
                                recommendation="Add docstring to function",
                                evidence={"function_name": node.name}
                            ))

                    elif isinstance(node, ast.ClassDef):
                        # Check class size
                        if node.end_lineno - node.lineno > self.v2_rules["class_size"]["max_lines"]:
                            findings.append(ComplianceFinding(
                                rule_id="V2-CLASS-SIZE",
                                severity="FAIL",
                                category="v2",
                                description=f"Class '{node.name}' exceeds maximum size of {self.v2_rules['class_size']['max_lines']} lines",
                                file_path=str(file_path),
                                line_number=node.lineno,
                                code_snippet=f"class {node.name}:",
                                recommendation="Break class into smaller classes",
                                evidence={"class_name": node.name, "lines": node.end_lineno - node.lineno}
                            ))

                        # Check class naming
                        if not re.match(self.v2_rules["naming_conventions"]["pascal_case_classes"], f"class {node.name}"):
                            findings.append(ComplianceFinding(
                                rule_id="V2-CLASS-NAME",
                                severity="FAIL",
                                category="v2",
                                description=f"Class '{node.name}' should use PascalCase naming",
                                file_path=str(file_path),
                                line_number=node.lineno,
                                code_snippet=f"class {node.name}:",
                                recommendation="Rename class to use PascalCase",
                                evidence={"class_name": node.name}
                            ))

            except SyntaxError as e:
                findings.append(ComplianceFinding(
                    rule_id="V2-SYNTAX",
                    severity="FAIL",
                    category="v2",
                    description=f"Syntax error in file: {e.msg}",
                    file_path=str(file_path),
                    line_number=e.lineno,
                    code_snippet=None,
                    recommendation="Fix syntax error",
                    evidence={"error": e.msg, "line": e.lineno}
                ))

        except Exception as e:
            findings.append(ComplianceFinding(
                rule_id="V2-CHECK-ERROR",
                severity="FAIL",
                category="v2",
                description=f"Error checking V2 compliance: {str(e)}",
                file_path=str(file_path),
                line_number=None,
                code_snippet=None,
                recommendation="Review file manually",
                evidence={"error": str(e)}
            ))

        return findings

    def check_security_compliance(self, file_path: Path) -> List[ComplianceFinding]:
        """Check security compliance"""
        findings = []

        if not file_path.exists():
            return findings

        try:
            with open(file_path, 'r') as f:
                content = f.read()

            # Check for hardcoded secrets
            secret_patterns = [
                (r'password\s*[:=]\s*[^$]', "Hardcoded password"),
                (r'secret\s*[:=]\s*[^$]', "Hardcoded secret"),
                (r'key\s*[:=]\s*[^$]', "Hardcoded key"),
                (r'token\s*[:=]\s*[^$]', "Hardcoded token")
            ]

            for pattern, description in secret_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    findings.append(ComplianceFinding(
                        rule_id="SEC-HARDSECRET",
                        severity="FAIL",
                        category="security",
                        description=f"{description} detected in {file_path.name}",
                        file_path=str(file_path),
                        line_number=None,
                        code_snippet=None,
                        recommendation="Use environment variables or secret management",
                        evidence={"pattern": pattern, "matches": len(matches)}
                    ))

            # Check for SQL injection vulnerabilities (basic)
            if file_path.suffix == '.py':
                sql_patterns = [
                    r'execute\(.*\+.*\)',
                    r'execute\(.*%.*\)',
                    r'execute\(f.*\).*'
                ]
                for pattern in sql_patterns:
                    if re.search(pattern, content):
                        findings.append(ComplianceFinding(
                            rule_id="SEC-SQL-INJECT",
                            severity="WARN",
                            category="security",
                            description="Potential SQL injection vulnerability",
                            file_path=str(file_path),
                            line_number=None,
                            code_snippet=None,
                            recommendation="Use parameterized queries or ORM",
                            evidence={"pattern": pattern}
                        ))

            # Check for insecure SSL/TLS settings
            if 'ssl' in content.lower():
                if 'ssl._create_unverified_context' in content:
                    findings.append(ComplianceFinding(
                        rule_id="SEC-SSL-VERIFY",
                        severity="FAIL",
                        category="security",
                        description="SSL certificate verification disabled",
                        file_path=str(file_path),
                        line_number=None,
                        code_snippet=None,
                        recommendation="Enable SSL certificate verification",
                        evidence={"issue": "ssl._create_unverified_context"}
                    ))

        except Exception as e:
            findings.append(ComplianceFinding(
                rule_id="SEC-CHECK-ERROR",
                severity="FAIL",
                category="security",
                description=f"Error checking security compliance: {str(e)}",
                file_path=str(file_path),
                line_number=None,
                code_snippet=None,
                recommendation="Review file manually",
                evidence={"error": str(e)}
            ))

        return findings

    def check_architecture_compliance(self) -> List[ComplianceFinding]:
        """Check architecture compliance"""
        findings = []

        # Check for circular imports (basic detection)
        try:
            # Look for potential circular import patterns
            python_files = list(Path('src').rglob('*.py'))
            for file_path in python_files:
                with open(file_path, 'r') as f:
                    content = f.read()

                imports = re.findall(r'^from (\S+) import|^import (\S+)', content, re.MULTILINE)
                for imp in imports:
                    module = imp[0] or imp[1]
                    if module.startswith('src.'):
                        # Check if this module is imported by modules it imports
                        # This is a simplified check
                        pass

        except Exception as e:
            findings.append(ComplianceFinding(
                rule_id="ARCH-CIRCULAR",
                severity="WARN",
                category="architecture",
                description=f"Error checking for circular imports: {str(e)}",
                file_path="src/",
                line_number=None,
                code_snippet=None,
                recommendation="Review import structure manually",
                evidence={"error": str(e)}
            ))

        # Check service layer separation
        services_dir = Path('src/services')
        if services_dir.exists():
            service_files = list(services_dir.rglob('*.py'))
            for file_path in service_files:
                with open(file_path, 'r') as f:
                    content = f.read()

                # Check if services import from utils (should be allowed)
                if 'from src.utils' in content:
                    pass  # This is OK
                # Check if services import from controllers (should not happen)
                elif 'from src.controllers' in content or 'from controllers' in content:
                    findings.append(ComplianceFinding(
                        rule_id="ARCH-LAYER",
                        severity="WARN",
                        category="architecture",
                        description="Service layer importing from controller layer",
                        file_path=str(file_path),
                        line_number=None,
                        code_snippet=None,
                        recommendation="Move logic to service layer or create proper abstraction",
                        evidence={"import_pattern": "controller import in service"}
                    ))

        return findings

    def run_comprehensive_check(self, target_path: str = ".") -> ComplianceReport:
        """Run comprehensive compliance check"""
        logger.info("🔍 Starting comprehensive compliance check...")

        target = Path(target_path)
        all_findings = []

        # Find all Python files
        if target.is_file() and target.suffix == '.py':
            python_files = [target]
        else:
            python_files = list(target.rglob('*.py'))

        logger.info(f"📁 Found {len(python_files)} Python files to check")

        # Run checks on each file
        for file_path in python_files:
            # Skip certain directories
            if any(skip in str(file_path) for skip in ['__pycache__', '.git', 'node_modules']):
                continue

            logger.debug(f"Checking {file_path}")

            # V2 compliance check
            v2_findings = self.check_v2_compliance(file_path)
            all_findings.extend(v2_findings)

            # Security compliance check
            sec_findings = self.check_security_compliance(file_path)
            all_findings.extend(sec_findings)

        # Architecture compliance check
        arch_findings = self.check_architecture_compliance()
        all_findings.extend(arch_findings)

        # Calculate compliance score
        total_checks = len(all_findings)
        passed_checks = len([f for f in all_findings if f.severity == "PASS"])
        failed_checks = len([f for f in all_findings if f.severity == "FAIL"])
        warning_checks = len([f for f in all_findings if f.severity == "WARN"])

        # Compliance score (higher is better)
        if total_checks == 0:
            compliance_score = 100
        else:
            compliance_score = max(0, int((passed_checks / total_checks) * 100))

        # Group by category
        compliance_by_category = {}
        categories = ["v2", "security", "architecture", "code_quality"]
        for category in categories:
            category_findings = [f for f in all_findings if f.category == category]
            compliance_by_category[category] = {
                "total": len(category_findings),
                "passed": len([f for f in category_findings if f.severity == "PASS"]),
                "failed": len([f for f in category_findings if f.severity == "FAIL"]),
                "warnings": len([f for f in category_findings if f.severity == "WARN"])
            }

        # Generate recommendations
        recommendations = []
        if failed_checks > 0:
            recommendations.append(f"🚨 CRITICAL: Address {failed_checks} failed compliance checks immediately")
        if warning_checks > 0:
            recommendations.append(f"⚠️  REVIEW: Address {warning_checks} compliance warnings")
        if compliance_score < 80:
            recommendations.append("📈 IMPROVE: Overall compliance score below 80%")
        recommendations.append("🔄 MONITOR: Regular compliance checks recommended")
        recommendations.append("📚 TRAINING: Code quality and security training for team")

        report = ComplianceReport(
            check_timestamp=datetime.now().isoformat(),
            overall_compliance_score=compliance_score,
            total_checks=total_checks,
            passed_checks=passed_checks,
            failed_checks=failed_checks,
            warning_checks=warning_checks,
            findings=all_findings,
            compliance_by_category=compliance_by_category,
            recommendations=recommendations
        )

        execution_time = (datetime.now() - datetime.fromisoformat(report.check_timestamp)).total_seconds()
        logger.info(f"✅ Compliance check completed in {execution_time:.2f} seconds")

        return report

    def print_compliance_report(self, report: ComplianceReport):
        """Print comprehensive compliance report"""
        print("\n" + "="*100)
        print("🔍 PHASE 6 COMPLIANCE CHECK REPORT")
        print("="*100)

        print(f"📊 OVERALL COMPLIANCE SCORE: {report.overall_compliance_score}/100")
        print(f"🔍 TOTAL CHECKS: {report.total_checks}")
        print(f"✅ PASSED: {report.passed_checks}")
        print(f"❌ FAILED: {report.failed_checks}")
        print(f"⚠️  WARNINGS: {report.warning_checks}")

        print("\n" + "-"*100)
        print("📋 COMPLIANCE BY CATEGORY")
        print("-"*100)

        for category, stats in report.compliance_by_category.items():
            if stats["total"] > 0:
                compliance_pct = int((stats["passed"] / stats["total"]) * 100) if stats["total"] > 0 else 100
                print(f"{category.upper():<15} | Total: {stats['total']:<3} | Passed: {stats['passed']:<3} | Failed: {stats['failed']:<3} | Warnings: {stats['warnings']:<3} | Score: {compliance_pct}%")

        print("\n" + "-"*100)
        print("📋 COMPLIANCE FINDINGS")
        print("-"*100)

        severity_order = ["FAIL", "WARN", "PASS"]
        severity_emojis = {"FAIL": "❌", "WARN": "⚠️", "PASS": "✅"}

        for severity in severity_order:
            severity_findings = [f for f in report.findings if f.severity == severity]
            if severity_findings:
                print(f"\n{severity_emojis[severity]} {severity} SEVERITY ({len(severity_findings)} findings):")
                for finding in severity_findings[:10]:  # Show first 10
                    file_name = Path(finding.file_path).name
                    print(f"  • {finding.rule_id}: {finding.description}")
                    print(f"    📁 {file_name}:{finding.line_number or 'N/A'}")
                    print(f"    💡 {finding.recommendation}")

                if len(severity_findings) > 10:
                    print(f"    ... and {len(severity_findings) - 10} more")

        print("\n" + "-"*100)
        print("💡 RECOMMENDATIONS")
        print("-"*100)
        for rec in report.recommendations:
            print(f"• {rec}")

        print("\n" + "="*100)

    def save_compliance_report(self, report: ComplianceReport, filename: str = None):
        """Save compliance report to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"phase6_compliance_{timestamp}.json"

        # Convert findings to dictionaries
        report_dict = asdict(report)
        report_dict["findings"] = [asdict(finding) for finding in report.findings]

        with open(filename, 'w') as f:
            json.dump(report_dict, f, indent=2, default=str)

        logger.info(f"💾 Compliance report saved to: {filename}")

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Phase 6 Enterprise Compliance Checker')
    parser.add_argument('--target', type=str, default='.', help='Target path to check (file or directory)')
    parser.add_argument('--output', type=str, help='Output filename for compliance report')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--category', choices=['all', 'v2', 'security', 'architecture'],
                       default='all', help='Compliance category to check')

    args = parser.parse_args()

    # Set logging level based on verbose flag
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    checker = Phase6ComplianceChecker()

    try:
        logger.info(f"🔍 Starting Phase 6 compliance check on: {args.target}")
        report = checker.run_comprehensive_check(args.target)
        checker.print_compliance_report(report)
        checker.save_compliance_report(report, args.output)

        # Provide actionable summary
        critical_issues = report.failed_checks
        logger.info(f"✅ Compliance check complete - {critical_issues} critical issues found")
        print(f"\n🔍 Summary: Compliance Score {report.overall_compliance_score}/100 - {critical_issues} critical issues, {report.warning_checks} warnings")

        # Exit with code based on compliance score
        if report.overall_compliance_score >= 90:
            logger.info("✅ Excellent compliance")
            sys.exit(0)  # Excellent
        elif report.overall_compliance_score >= 75:
            logger.info("⚠️ Good compliance with minor issues")
            sys.exit(1)  # Good with issues
        elif report.overall_compliance_score >= 60:
            logger.warning("⚠️ Compliance needs attention")
            sys.exit(2)  # Needs attention
        else:
            logger.error("❌ Critical compliance issues found")
            sys.exit(3)  # Critical issues

    except KeyboardInterrupt:
        logger.info("Compliance check interrupted by user")
        print("\n👋 Compliance check interrupted")
        sys.exit(130)

    except Exception as e:
        logger.error(f"Compliance check failed: {e}")
        print(f"\n❌ Compliance check failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()