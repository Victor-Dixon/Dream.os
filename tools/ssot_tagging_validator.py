#!/usr/bin/env python3
"""
SSOT Tagging Validator
=====================

Validates SSOT domain tag consistency across the codebase.
Supports Agent-6's Block 5 SSOT tagging coordination efforts.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-12-28
V2 Compliant: Yes (<300 lines)

<!-- SSOT Domain: tools -->
"""

import os
import re
import json
import dataclasses
from pathlib import Path
from typing import Dict, List, Set, Tuple
from datetime import datetime


@dataclasses.dataclass
class SSOTValidationResult:
    """SSOT validation result for a file."""
    file_path: str
    has_ssot_tag: bool
    domain_tags: List[str]
    issues: List[str]
    recommendations: List[str]


@dataclasses.dataclass
class SSOTDomainStats:
    """Statistics for SSOT domain usage."""
    domain: str
    file_count: int
    files: List[str]


class SSOTTaggingValidator:
    """Validates SSOT tagging consistency across codebase."""

    def __init__(self):
        # Load known SSOT domains from registry
        self.known_domains = self._load_ssot_domains()
        self.validation_results = []
        self.domain_stats = {}

    def _load_ssot_domains(self) -> Set[str]:
        """Load known SSOT domains from registry."""
        domains = {
            'core', 'infrastructure', 'integration', 'onboarding', 'messaging',
            'coordination', 'logging', 'error_handling', 'config', 'security',
            'performance', 'monitoring', 'testing', 'deployment', 'git',
            'github', 'discord', 'vision', 'gaming', 'trading_robot', 'swarm_brain',
            'orchestration', 'repositories', 'workflows', 'architecture', 'design',
            # Additional domains from SSOT_DOMAIN_MAPPING.md
            'communication', 'data', 'analytics', 'safety', 'domain',
            'ai_training', 'qa', 'services', 'web', 'seo', 'documentation',
            'tools', 'validation'
        }

        # Try to load from SSOT domain mapping if available
        ssot_mapping = Path("docs/SSOT_DOMAIN_MAPPING.md")
        if ssot_mapping.exists():
            try:
                with open(ssot_mapping, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Extract domains from HTML comment format: <!-- SSOT Domain: domain_name -->
                    html_comment_pattern = r'<!--\s*SSOT\s+Domain:\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*-->'
                    html_matches = re.findall(html_comment_pattern, content, re.IGNORECASE)
                    for match in html_matches:
                        domains.add(match.lower())
                    # Also extract from domain list sections
                    domain_list_pattern = r'\*\*([a-zA-Z_][a-zA-Z0-9_]*)\*\*.*?Owner:'
                    list_matches = re.findall(domain_list_pattern, content, re.IGNORECASE | re.DOTALL)
                    for match in list_matches:
                        domains.add(match.lower())
            except Exception:
                pass

        return domains

    def validate_file(self, file_path: str) -> SSOTValidationResult:
        """Validate SSOT tagging for a single file."""
        issues = []
        recommendations = []
        domain_tags = []

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Check for SSOT domain tags in comments/docstrings
            # Support multiple formats: HTML comments, @domain, @ssot, SSOT domain:
            ssot_pattern = r'<!--\s*SSOT\s+Domain:\s*(\w+)\s*-->|@domain\s+(\w+)|@ssot\s+(\w+)|SSOT\s*domain\s*:\s*(\w+)'
            matches = re.findall(ssot_pattern, content, re.IGNORECASE)

            for match in matches:
                domain = match[0] or match[1] or match[2] or match[3]
                if domain:
                    domain_tags.append(domain.lower())

            has_ssot_tag = len(domain_tags) > 0

            # Validate domain tags
            if has_ssot_tag:
                for domain in domain_tags:
                    if domain not in self.known_domains:
                        issues.append(f"Unknown domain tag: '{domain}'")
                        recommendations.append(f"Consider adding '{domain}' to SSOT domain registry or use existing domain")
                    else:
                        # Track domain usage
                        if domain not in self.domain_stats:
                            self.domain_stats[domain] = SSOTDomainStats(domain, 0, [])
                        self.domain_stats[domain].file_count += 1
                        self.domain_stats[domain].files.append(file_path)
            else:
                # No SSOT tags found
                issues.append("Missing SSOT domain tag")
                recommendations.append("Add @domain tag in file header comment/docstring")
                recommendations.append("Use format: @domain <domain_name>")

                # Suggest domain based on file path
                suggested_domain = self._suggest_domain_from_path(file_path)
                if suggested_domain:
                    recommendations.append(f"Suggested domain: {suggested_domain}")

            # Check for multiple domains (usually indicates unclear boundaries)
            if len(set(domain_tags)) > 1:
                issues.append(f"Multiple domain tags found: {', '.join(set(domain_tags))}")
                recommendations.append("Consider if file serves single domain or needs splitting")

        except Exception as e:
            issues.append(f"Error reading file: {str(e)}")

        return SSOTValidationResult(
            file_path=file_path,
            has_ssot_tag=has_ssot_tag,
            domain_tags=domain_tags,
            issues=issues,
            recommendations=recommendations
        )

    def _suggest_domain_from_path(self, file_path: str) -> str:
        """Suggest domain based on file path."""
        path_lower = file_path.lower()

        domain_mappings = {
            'core/': 'core',
            'infrastructure/': 'infrastructure',
            'integration/': 'integration',
            'services/': 'integration',
            'messaging/': 'messaging',
            'coordination/': 'coordination',
            'logging': 'logging',
            'error': 'error_handling',
            'config': 'config',
            'security': 'security',
            'performance': 'performance',
            'monitoring': 'monitoring',
            'test': 'testing',
            'deploy': 'deployment',
            'git': 'git',
            'github': 'github',
            'discord': 'discord',
            'vision': 'vision',
            'gaming': 'gaming',
            'trading': 'trading_robot',
            'swarm': 'swarm_brain',
            'orchestrat': 'orchestration',
            'repository': 'repositories',
            'workflow': 'workflows',
            'architect': 'architecture',
            'design': 'design'
        }

        for path_pattern, domain in domain_mappings.items():
            if path_pattern in path_lower:
                return domain

        return 'core'  # Default fallback

    def validate_directory(self, directory: str, extensions: List[str] = None) -> List[SSOTValidationResult]:
        """Validate SSOT tagging for all files in a directory."""
        if extensions is None:
            extensions = ['.py', '.js', '.ts', '.php', '.md']

        results = []

        for root, dirs, files in os.walk(directory):
            # Skip certain directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]

            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    result = self.validate_file(file_path)
                    results.append(result)
                    self.validation_results.append(result)

        return results

    def generate_report(self, results: List[SSOTValidationResult] = None) -> Dict:
        """Generate comprehensive validation report."""
        if results is None:
            results = self.validation_results

        total_files = len(results)
        tagged_files = sum(1 for r in results if r.has_ssot_tag)
        untagged_files = total_files - tagged_files

        # Count issues
        total_issues = sum(len(r.issues) for r in results)

        # Domain usage summary
        domain_summary = {}
        for domain, stats in self.domain_stats.items():
            domain_summary[domain] = {
                'file_count': stats.file_count,
                'files': stats.files[:5],  # Show first 5 files
                'truncated': len(stats.files) > 5
            }

        # Files with issues (top 20)
        files_with_issues = sorted(
            [(r.file_path, len(r.issues)) for r in results if r.issues],
            key=lambda x: x[1],
            reverse=True
        )[:20]

        return {
            'summary': {
                'total_files': total_files,
                'tagged_files': tagged_files,
                'untagged_files': untagged_files,
                'compliance_rate': round((tagged_files / total_files * 100), 1) if total_files > 0 else 0,
                'total_issues': total_issues
            },
            'domain_usage': domain_summary,
            'files_with_most_issues': files_with_issues,
            'recommendations': [
                f"Tag {untagged_files} files with appropriate @domain tags",
                "Review files with multiple domain tags for potential splitting",
                "Add unknown domains to SSOT domain registry if legitimate",
                "Ensure domain tags are placed in file headers/comments"
            ]
        }


def main():
    """Main validation function."""
    import argparse

    parser = argparse.ArgumentParser(description="SSOT Tagging Validator")
    parser.add_argument('--directory', '-d', default='src',
                       help='Directory to validate (default: src)')
    parser.add_argument('--extensions', '-e', nargs='+',
                       default=['.py', '.js', '.ts', '.php', '.md'],
                       help='File extensions to check')
    parser.add_argument('--output', '-o', default='ssot_validation_report.json',
                       help='Output report file')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')

    args = parser.parse_args()

    validator = SSOTTaggingValidator()

    print(f"🔍 Validating SSOT tagging in {args.directory}...")
    results = validator.validate_directory(args.directory, args.extensions)

    report = validator.generate_report(results)

    # Save detailed results
    detailed_results = []
    for result in results:
        detailed_results.append({
            'file_path': result.file_path,
            'has_ssot_tag': result.has_ssot_tag,
            'domain_tags': result.domain_tags,
            'issues': result.issues,
            'recommendations': result.recommendations
        })

    output_data = {
        'report': report,
        'detailed_results': detailed_results,
        'timestamp': str(datetime.now())
    }

    with open(args.output, 'w') as f:
        json.dump(output_data, f, indent=2)

    # Print summary
    print("\n📊 SSOT TAGGING VALIDATION SUMMARY")
    print("=" * 50)
    summary = report['summary']
    print(f"Total files scanned: {summary['total_files']}")
    print(f"Files with SSOT tags: {summary['tagged_files']}")
    print(f"Files missing tags: {summary['untagged_files']}")
    print(f"Compliance rate: {summary['compliance_rate']}%")
    print(f"Total issues found: {summary['total_issues']}")

    if summary['untagged_files'] > 0:
        print(f"\n⚠️  {summary['untagged_files']} files need SSOT tagging")

    if report['files_with_most_issues']:
        print("\n🔍 Files with most issues:")
        for file_path, issue_count in report['files_with_most_issues'][:5]:
            print(f"  • {file_path}: {issue_count} issues")

    print(f"\n📄 Detailed report saved to: {args.output}")


if __name__ == "__main__":
    main()
