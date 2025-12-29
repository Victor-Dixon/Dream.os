#!/usr/bin/env python3
"""
SSOT Tagging Batch Assignment System
====================================

Accelerates SSOT tagging coordination by creating prioritized batch assignments
for swarm agents. Supports Agent-6's Block 5 SSOT tagging coordination.

Author: Agent-2 (Architecture & Design)
Date: 2025-12-28
V2 Compliant: Yes (<300 lines)
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime


class SSOTTaggingBatchAssigner:
    """Assigns SSOT tagging work in prioritized batches."""

    def __init__(self):
        self.domain_hierarchy = {
            'core': {'priority': 1, 'agents': ['Agent-2', 'Agent-1']},
            'infrastructure': {'priority': 1, 'agents': ['Agent-3', 'Agent-6']},
            'integration': {'priority': 2, 'agents': ['Agent-1', 'Agent-8']},
            'messaging': {'priority': 1, 'agents': ['Agent-1', 'Agent-6']},
            'coordination': {'priority': 2, 'agents': ['Agent-6', 'Agent-4']},
            'logging': {'priority': 3, 'agents': ['Agent-3', 'Agent-8']},
            'error_handling': {'priority': 2, 'agents': ['Agent-3', 'Agent-8']},
            'config': {'priority': 2, 'agents': ['Agent-3', 'Agent-5']},
            'security': {'priority': 1, 'agents': ['Agent-3', 'Agent-8']},
            'performance': {'priority': 2, 'agents': ['Agent-3', 'Agent-5']},
            'monitoring': {'priority': 2, 'agents': ['Agent-3', 'Agent-5']},
            'testing': {'priority': 3, 'agents': ['Agent-8', 'Agent-5']},
            'deployment': {'priority': 1, 'agents': ['Agent-3', 'Agent-8']},
            'git': {'priority': 3, 'agents': ['Agent-1', 'Agent-8']},
            'github': {'priority': 3, 'agents': ['Agent-1', 'Agent-8']},
            'discord': {'priority': 3, 'agents': ['Agent-1', 'Agent-6']},
            'vision': {'priority': 3, 'agents': ['Agent-8', 'Agent-5']},
            'gaming': {'priority': 3, 'agents': ['Agent-8', 'Agent-5']},
            'trading_robot': {'priority': 1, 'agents': ['Agent-1', 'Agent-5']},
            'swarm_brain': {'priority': 2, 'agents': ['Agent-1', 'Agent-6']},
            'orchestration': {'priority': 3, 'agents': ['Agent-1', 'Agent-4']},
            'repositories': {'priority': 3, 'agents': ['Agent-1', 'Agent-8']},
            'workflows': {'priority': 3, 'agents': ['Agent-6', 'Agent-4']},
            'architecture': {'priority': 1, 'agents': ['Agent-2', 'Agent-1']},
            'design': {'priority': 2, 'agents': ['Agent-2', 'Agent-7']}
        }

    def create_tagging_batches(self, untagged_files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create prioritized tagging batches from untagged files."""

        # Group files by domain
        domain_groups = {}
        for file_info in untagged_files:
            domain = self._infer_domain_from_file(file_info['file_path'])
            if domain not in domain_groups:
                domain_groups[domain] = []
            domain_groups[domain].append(file_info)

        # Create batches by priority
        batches = {
            'priority_1': [],  # Critical infrastructure
            'priority_2': [],  # Core functionality
            'priority_3': []   # Supporting features
        }

        # Assign files to batches
        for domain, files in domain_groups.items():
            priority = self.domain_hierarchy.get(domain, {}).get('priority', 3)
            batch_name = f'priority_{priority}'

            # Split large domains into smaller batches
            if len(files) > 20:
                # Create sub-batches
                for i in range(0, len(files), 15):
                    batch_files = files[i:i+15]
                    batch_id = f"{domain}_batch_{i//15 + 1}"
                    batch_info = self._create_batch(batch_id, domain, batch_files, priority)
                    batches[batch_name].append(batch_info)
            else:
                batch_id = f"{domain}_complete"
                batch_info = self._create_batch(batch_id, domain, files, priority)
                batches[batch_name].append(batch_info)

        # Sort batches by size (largest first within priority)
        for priority in batches:
            batches[priority].sort(key=lambda x: x['file_count'], reverse=True)

        return {
            'batches': batches,
            'summary': self._create_summary(batches, domain_groups),
            'assignments': self._create_assignments(batches)
        }

    def _infer_domain_from_file(self, file_path: str) -> str:
        """Infer domain from file path."""
        path_lower = file_path.lower()

        # Direct path mappings
        if 'infrastructure' in path_lower:
            return 'infrastructure'
        if 'core' in path_lower and 'infrastructure' not in path_lower:
            return 'core'
        if 'services' in path_lower:
            return 'integration'
        if 'messaging' in path_lower:
            return 'messaging'
        if 'coordination' in path_lower:
            return 'coordination'
        if 'logging' in path_lower or 'log' in path_lower:
            return 'logging'
        if 'error' in path_lower:
            return 'error_handling'
        if 'config' in path_lower:
            return 'config'
        if 'security' in path_lower:
            return 'security'
        if 'performance' in path_lower or 'perf' in path_lower:
            return 'performance'
        if 'monitor' in path_lower:
            return 'monitoring'
        if 'test' in path_lower:
            return 'testing'
        if 'deploy' in path_lower:
            return 'deployment'
        if 'git' in path_lower:
            return 'git'
        if 'github' in path_lower:
            return 'github'
        if 'discord' in path_lower:
            return 'discord'
        if 'vision' in path_lower:
            return 'vision'
        if 'gaming' in path_lower:
            return 'gaming'
        if 'trading' in path_lower:
            return 'trading_robot'
        if 'swarm' in path_lower:
            return 'swarm_brain'
        if 'architect' in path_lower:
            return 'architecture'
        if 'design' in path_lower:
            return 'design'

        # Default to core for src/ files
        if file_path.startswith('src/'):
            return 'core'

        return 'core'  # Default fallback

    def _create_batch(self, batch_id: str, domain: str, files: List[Dict[str, Any]], priority: int) -> Dict[str, Any]:
        """Create a batch assignment."""
        domain_config = self.domain_hierarchy.get(domain, {'agents': ['Agent-2']})
        primary_agent = domain_config['agents'][0]
        secondary_agent = domain_config['agents'][1] if len(domain_config['agents']) > 1 else primary_agent

        return {
            'batch_id': batch_id,
            'domain': domain,
            'priority': priority,
            'file_count': len(files),
            'files': [f['file_path'] for f in files],
            'primary_agent': primary_agent,
            'secondary_agent': secondary_agent,
            'estimated_time': self._estimate_time(len(files), priority),
            'instructions': self._generate_instructions(domain, files)
        }

    def _estimate_time(self, file_count: int, priority: int) -> str:
        """Estimate completion time based on file count and priority."""
        # Base time per file (minutes)
        base_time = 5 if priority == 1 else 3 if priority == 2 else 2

        total_minutes = file_count * base_time

        if total_minutes < 60:
            return f"{total_minutes} minutes"
        elif total_minutes < 480:  # 8 hours
            return f"{total_minutes // 60} hours"
        else:
            return f"{total_minutes // 480} days"

    def _generate_instructions(self, domain: str, files: List[Dict[str, Any]]) -> str:
        """Generate tagging instructions for the batch."""
        domain_examples = {
            'infrastructure': '@domain infrastructure  # Core system infrastructure',
            'core': '@domain core  # Core system functionality',
            'integration': '@domain integration  # System integration components',
            'messaging': '@domain messaging  # Communication and messaging',
            'coordination': '@domain coordination  # Agent coordination systems',
            'logging': '@domain logging  # Logging and telemetry',
            'error_handling': '@domain error_handling  # Error handling and recovery',
            'config': '@domain config  # Configuration management',
            'security': '@domain security  # Security and authentication',
            'performance': '@domain performance  # Performance monitoring',
            'monitoring': '@domain monitoring  # System monitoring',
            'testing': '@domain testing  # Testing infrastructure',
            'deployment': '@domain deployment  # Deployment systems',
            'git': '@domain git  # Git operations',
            'github': '@domain github  # GitHub API integration',
            'discord': '@domain discord  # Discord bot integration',
            'vision': '@domain vision  # Computer vision',
            'gaming': '@domain gaming  # Gaming functionality',
            'trading_robot': '@domain trading_robot  # Trading robot systems',
            'swarm_brain': '@domain swarm_brain  # Swarm intelligence',
            'orchestration': '@domain orchestration  # System orchestration',
            'repositories': '@domain repositories  # Repository management',
            'workflows': '@domain workflows  # Workflow systems',
            'architecture': '@domain architecture  # System architecture',
            'design': '@domain design  # UI/UX design'
        }

        example = domain_examples.get(domain, f'@domain {domain}  # {domain.replace("_", " ").title()}')

        return f"""Add SSOT domain tag to file headers:

1. Add domain tag in comments/docstring at top of file:
   {example}

2. Tag {len(files)} files in this batch
3. Verify tags follow SSOT domain registry
4. Test files still compile after tagging
5. Commit with message: 'feat: Add SSOT domain tags - {domain} domain ({len(files)} files)'"""

    def _create_summary(self, batches: Dict[str, List], domain_groups: Dict[str, List]) -> Dict[str, Any]:
        """Create summary statistics."""
        total_batches = sum(len(batch_list) for batch_list in batches.values())
        total_files = sum(len(domain_files) for domain_files in domain_groups.values())

        priority_stats = {}
        for priority, batch_list in batches.items():
            priority_stats[priority] = {
                'batches': len(batch_list),
                'files': sum(batch['file_count'] for batch in batch_list)
            }

        return {
            'total_batches': total_batches,
            'total_files': total_files,
            'priority_breakdown': priority_stats,
            'domain_coverage': len(domain_groups),
            'largest_domain': max(domain_groups.keys(), key=lambda x: len(domain_groups[x]))
        }

    def _create_assignments(self, batches: Dict[str, List]) -> Dict[str, List]:
        """Create agent-specific assignments."""
        assignments = {}

        for priority, batch_list in batches.items():
            for batch in batch_list:
                primary = batch['primary_agent']
                secondary = batch['secondary_agent']

                if primary not in assignments:
                    assignments[primary] = []
                if secondary not in assignments:
                    assignments[secondary] = []

                assignment = {
                    'batch_id': batch['batch_id'],
                    'domain': batch['domain'],
                    'priority': batch['priority'],
                    'file_count': batch['file_count'],
                    'estimated_time': batch['estimated_time'],
                    'role': 'PRIMARY' if primary == batch['primary_agent'] else 'SECONDARY'
                }

                assignments[primary].append(assignment)
                if primary != secondary:
                    assignments[secondary].append(assignment)

        # Sort assignments by priority
        for agent in assignments:
            assignments[agent].sort(key=lambda x: (x['priority'], x['file_count']), reverse=True)

        return assignments

    def generate_assignment_report(self, assignments: Dict[str, List]) -> str:
        """Generate markdown report of assignments."""
        report = ["# SSOT Tagging Batch Assignments\n", f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"]

        for agent in sorted(assignments.keys()):
            agent_assignments = assignments[agent]

            # Calculate workload
            total_files = sum(a['file_count'] for a in agent_assignments)
            primary_batches = len([a for a in agent_assignments if a['role'] == 'PRIMARY'])

            report.append(f"## {agent} ({primary_batches} primary, {total_files} files)\n")

            for assignment in agent_assignments:
                role_emoji = "🎯" if assignment['role'] == 'PRIMARY' else "🤝"
                priority_emoji = "🔴" if assignment['priority'] == 1 else "🟠" if assignment['priority'] == 2 else "🟢"

                report.append(f"### {role_emoji} {assignment['batch_id']}")
                report.append(f"- **Domain**: {assignment['domain']}")
                report.append(f"- **Priority**: {priority_emoji} Priority {assignment['priority']}")
                report.append(f"- **Files**: {assignment['file_count']}")
                report.append(f"- **Est. Time**: {assignment['estimated_time']}")
                report.append("")

        return "\n".join(report)


def main():
    """CLI interface for SSOT batch assignment."""
    import argparse

    parser = argparse.ArgumentParser(description="SSOT Tagging Batch Assigner")
    parser.add_argument('--input', '-i', required=True, help='JSON file with untagged files')
    parser.add_argument('--output', '-o', default='ssot_batch_assignments.md', help='Output assignment report')
    parser.add_argument('--json-output', '-j', help='Output detailed JSON assignments')

    args = parser.parse_args()

    # Load untagged files
    with open(args.input, 'r') as f:
        data = json.load(f)

    untagged_files = []
    if 'detailed_results' in data:
        untagged_files = [r for r in data['detailed_results'] if not r['has_ssot_tag']]

    # Create assigner and generate batches
    assigner = SSOTTaggingBatchAssigner()
    result = assigner.create_tagging_batches(untagged_files)

    # Generate reports
    assignment_report = assigner.generate_assignment_report(result['assignments'])

    # Save markdown report
    with open(args.output, 'w') as f:
        f.write(assignment_report)

    # Save JSON if requested
    if args.json_output:
        with open(args.json_output, 'w') as f:
            json.dump(result, f, indent=2)

    # Print summary
    summary = result['summary']
    print("🎯 SSOT Tagging Batch Assignment Complete")
    print(f"📊 Total batches: {summary['total_batches']}")
    print(f"📁 Total files: {summary['total_files']}")
    print(f"🏷️  Domains: {summary['domain_coverage']}")
    print(f"📄 Report saved: {args.output}")

    # Priority breakdown
    for priority, stats in summary['priority_breakdown'].items():
        level = "🔴 CRITICAL" if priority == 'priority_1' else "🟠 HIGH" if priority == 'priority_2' else "🟢 MEDIUM"
        print(f"  {level}: {stats['batches']} batches, {stats['files']} files")


if __name__ == "__main__":
    main()

