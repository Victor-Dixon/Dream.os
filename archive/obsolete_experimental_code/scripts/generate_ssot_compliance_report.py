#!/usr/bin/env python3
"""
SSOT Compliance Audit Report Generator
======================================

Generates comprehensive SSOT compliance audit reports by scanning
all files for @domain tags and validating against known domains.

Usage:
    python generate_ssot_compliance_report.py

Output:
    current_issues.json - Detailed compliance report
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Set
from collections import defaultdict, Counter


class SSOTComplianceAuditor:
    """Audits codebase for SSOT compliance issues."""

    # Known valid domains from the SSOT registry
    VALID_DOMAINS = {
        'core', 'swarm_brain', 'discord', 'messaging', 'web', 'git',
        'communication', 'integration', 'ai_training', 'analytics',
        'error_handling', 'safety', 'domain', 'gaming', 'vision',
        'orchestrators', 'qa', 'services', 'onboarding', 'trading_robot',
        'performance', 'deployment', 'documentation', 'tools', 'architecture',
        'seo', 'infrastructure', 'wordpress', 'logging'
    }

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.timestamp = datetime.now().isoformat()

    def scan_file(self, file_path: Path) -> Dict[str, Any]:
        """Scan a single file for SSOT compliance."""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')

            # Find @domain tags
            domain_pattern = r'<!--\s*@\s*domain:\s*([^-\s]+)\s*-->'
            matches = re.findall(domain_pattern, content, re.IGNORECASE)

            # Also check for SSOT Domain comments
            ssot_pattern = r'<!--\s*SSOT\s+Domain:\s*([^-\s]+)\s*-->'
            ssot_matches = re.findall(ssot_pattern, content, re.IGNORECASE)

            all_domains = set(matches + ssot_matches)

            # Check for issues
            issues = []
            recommendations = []

            # Check for unknown domains
            unknown_domains = all_domains - self.VALID_DOMAINS
            if unknown_domains:
                for domain in unknown_domains:
                    issues.append(f"Unknown domain tag: '{domain}'")
                    recommendations.append("Consider adding '{domain}' to SSOT domain registry or use existing domain")

            # Check for multiple domains (more than one unique domain)
            if len(all_domains) > 1:
                issues.append(f"Multiple domain tags: {', '.join(sorted(all_domains))}")
                recommendations.append("Review file for single responsibility - consider splitting or clarifying primary domain")

            # Check for mixed domains (integration + core is flagged as mixed)
            if len(all_domains) > 1 and 'integration' in all_domains and 'core' in all_domains:
                issues.append("Mixed domain usage: integration + core")
                recommendations.append("Clarify whether this file belongs to 'integration' or 'core' domain")

            return {
                "file_path": str(file_path.relative_to(self.project_root)),
                "has_ssot_tag": len(all_domains) > 0,
                "domain_tags": list(all_domains),
                "issues": issues,
                "recommendations": recommendations
            }

        except Exception as e:
            return {
                "file_path": str(file_path.relative_to(self.project_root)),
                "has_ssot_tag": False,
                "domain_tags": [],
                "issues": [f"Error scanning file: {str(e)}"],
                "recommendations": ["Check file permissions and encoding"]
            }

    def scan_codebase(self) -> Dict[str, Any]:
        """Scan entire codebase for SSOT compliance."""
        print("🔍 Scanning codebase for SSOT compliance...")

        # File extensions to scan
        extensions = {'.py', '.js', '.ts', '.tsx', '.md', '.json', '.yml', '.yaml'}

        # Directories to scan
        scan_dirs = ['src', 'tools', 'scripts', 'docs']

        all_files = []
        domain_usage = defaultdict(lambda: {'file_count': 0, 'files': []})

        total_files = 0
        tagged_files = 0

        for scan_dir in scan_dirs:
            scan_path = self.project_root / scan_dir
            if not scan_path.exists():
                continue

            for file_path in scan_path.rglob('*'):
                if file_path.is_file() and file_path.suffix.lower() in extensions:
                    total_files += 1
                    result = self.scan_file(file_path)

                    if result['has_ssot_tag']:
                        tagged_files += 1

                        # Update domain usage
                        for domain in result['domain_tags']:
                            domain_usage[domain]['file_count'] += 1
                            domain_usage[domain]['files'].append(result['file_path'])

                    all_files.append(result)

                    # Progress indicator
                    if total_files % 100 == 0:
                        print(f"  Scanned {total_files} files...")

        # Sort domain files and truncate long lists
        for domain_data in domain_usage.values():
            domain_data['files'].sort()
            if len(domain_data['files']) > 10:
                domain_data['files'] = domain_data['files'][:10]
                domain_data['truncated'] = True
            else:
                domain_data['truncated'] = False

        # Find files with most issues
        files_with_issues = [(f['file_path'], len(f['issues'])) for f in all_files if f['issues']]
        files_with_issues.sort(key=lambda x: x[1], reverse=True)
        files_with_issues = files_with_issues[:10]  # Top 10

        # Generate recommendations
        recommendations = [
            "Tag 0 files with appropriate @domain tags",
            "Review files with multiple domain tags for potential splitting",
            "Add unknown domains to SSOT domain registry if legitimate",
            "Ensure domain tags are placed in file headers/comments"
        ]

        return {
            "report": {
                "summary": {
                    "total_files": total_files,
                    "tagged_files": tagged_files,
                    "untagged_files": total_files - tagged_files,
                    "compliance_rate": round((tagged_files / total_files * 100), 1) if total_files > 0 else 0,
                    "total_issues": sum(len(f['issues']) for f in all_files)
                },
                "domain_usage": dict(domain_usage),
                "files_with_most_issues": files_with_issues,
                "recommendations": recommendations
            },
            "detailed_results": sorted(all_files, key=lambda x: x['file_path']),
            "timestamp": self.timestamp
        }

    def save_report(self, report: Dict[str, Any], output_file: str = "current_issues.json"):
        """Save compliance report to JSON file."""
        output_path = self.project_root / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"✅ Report saved to {output_path}")
        return output_path


def main():
    """Main entry point."""
    auditor = SSOTComplianceAuditor()
    report = auditor.scan_codebase()

    # Print summary
    summary = report['report']['summary']
    print(f"\n📊 SSOT Compliance Report Summary")
    print("=" * 40)
    print(f"Total files analyzed: {summary['total_files']}")
    print(f"Files with domain tags: {summary['tagged_files']}")
    print(f"Compliance rate: {summary['compliance_rate']}%")
    print(f"Total issues found: {summary['total_issues']}")

    # Save report
    output_file = auditor.save_report(report)
    print(f"\n📋 Detailed report saved to: {output_file}")

    # Show top issues
    if summary['total_issues'] > 0:
        print(f"\n🔍 Top Issues:")
        files_with_issues = report['report']['files_with_most_issues'][:5]
        for file_path, issue_count in files_with_issues:
            print(f"  - {file_path}: {issue_count} issues")


if __name__ == "__main__":
    main()