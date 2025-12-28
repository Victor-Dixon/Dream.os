#!/usr/bin/env python3
"""
SSOT Coordination Report Generator
==================================

Generates coordination reports for Agent-6's SSOT tagging Block 5 work.
Provides actionable insights and coordination recommendations.

Author: Agent-2 (Architecture & Design)
Date: 2025-12-28
V2 Compliant: Yes (<300 lines)
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


def load_batch_assignments(json_file: str) -> Dict[str, Any]:
    """Load batch assignments from JSON file."""
    try:
        with open(json_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def generate_coordination_report(assignments: Dict[str, Any]) -> str:
    """Generate coordination report for Agent-6."""

    report = [f"# SSOT Coordination Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"]

    # Executive Summary
    batches = assignments.get('batches', {})
    summary = assignments.get('summary', {})

    report.append("## 📊 Executive Summary\n")
    report.append(f"- **Total Files to Tag**: {summary.get('total_files', 0)}")
    report.append(f"- **Total Batches**: {summary.get('total_batches', 0)}")
    report.append(f"- **Domains Affected**: {summary.get('domain_coverage', 0)}")
    report.append(f"- **Largest Domain**: {summary.get('largest_domain', 'N/A')}")
    report.append("")

    # Priority Breakdown
    report.append("## 🎯 Priority Breakdown\n")
    priority_stats = summary.get('priority_breakdown', {})
    for priority, stats in priority_stats.items():
        level = {
            'priority_1': '🔴 CRITICAL',
            'priority_2': '🟠 HIGH',
            'priority_3': '🟢 MEDIUM'
        }.get(priority, priority)

        report.append(f"### {level}")
        report.append(f"- **Batches**: {stats.get('batches', 0)}")
        report.append(f"- **Files**: {stats.get('files', 0)}")
        report.append("")

    # Agent Workload Summary
    report.append("## 👥 Agent Workload Summary\n")
    agent_assignments = assignments.get('assignments', {})

    # Calculate workloads
    workloads = {}
    for agent, tasks in agent_assignments.items():
        total_files = sum(task['file_count'] for task in tasks)
        primary_tasks = len([t for t in tasks if t['role'] == 'PRIMARY'])
        secondary_tasks = len([t for t in tasks if t['role'] == 'SECONDARY'])

        workloads[agent] = {
            'total_files': total_files,
            'primary_tasks': primary_tasks,
            'secondary_tasks': secondary_tasks,
            'total_tasks': len(tasks)
        }

    # Sort by total files (descending)
    sorted_workloads = sorted(workloads.items(), key=lambda x: x[1]['total_files'], reverse=True)

    for agent, stats in sorted_workloads:
        report.append(f"### {agent}")
        report.append(f"- **Total Files**: {stats['total_files']}")
        report.append(f"- **Primary Tasks**: {stats['primary_tasks']}")
        report.append(f"- **Secondary Tasks**: {stats['secondary_tasks']}")
        report.append(f"- **Total Tasks**: {stats['total_tasks']}")
        report.append("")

    # Coordination Recommendations
    report.append("## 🎯 Coordination Recommendations\n")

    # Critical Path Items
    critical_batches = []
    for priority_batches in batches.get('priority_1', []):
        critical_batches.append(priority_batches)

    if critical_batches:
        report.append("### 🔴 Critical Path (Priority 1)")
        report.append("**Immediate Focus Areas:**")
        for batch in critical_batches[:5]:  # Top 5 critical batches
            report.append(f"- **{batch['batch_id']}**: {batch['file_count']} files ({batch['domain']})")
            report.append(f"  - Primary: {batch['primary_agent']}, Secondary: {batch['secondary_agent']}")
            report.append(f"  - Est. Time: {batch['estimated_time']}")
        report.append("")

    # Force Multiplier Opportunities
    report.append("### 🚀 Force Multiplier Opportunities")
    report.append("**Parallel Execution Candidates:**")
    domain_groups = {}
    for priority in ['priority_1', 'priority_2']:
        for batch in batches.get(priority, []):
            domain = batch['domain']
            if domain not in domain_groups:
                domain_groups[domain] = []
            domain_groups[domain].append(batch)

    for domain, domain_batches in domain_groups.items():
        if len(domain_batches) > 3:  # Domains with multiple batches
            total_files = sum(b['file_count'] for b in domain_batches)
            report.append(f"- **{domain} Domain**: {len(domain_batches)} batches, {total_files} files")
            primary_agents = set(b['primary_agent'] for b in domain_batches)
            report.append(f"  - Can be parallelized across: {', '.join(primary_agents)}")
    report.append("")

    # Implementation Guide
    report.append("## 📋 Implementation Guide\n")
    report.append("### Phase 1: Critical Infrastructure (Week 1)")
    report.append("1. **Start with Priority 1 batches** (core, infrastructure, messaging domains)")
    report.append("2. **Assign primary agents** based on domain expertise")
    report.append("3. **Daily coordination sync** to track progress")
    report.append("4. **Validation checkpoints** every 50 files tagged")
    report.append("")

    report.append("### Phase 2: Core Functionality (Week 2)")
    report.append("1. **Priority 2 batches** (integration, coordination, security)")
    report.append("2. **Cross-agent coordination** for overlapping domains")
    report.append("3. **SSOT validation runs** after each domain completes")
    report.append("4. **Documentation updates** for new domain mappings")
    report.append("")

    report.append("### Phase 3: Supporting Features (Week 3)")
    report.append("1. **Priority 3 batches** (testing, monitoring, deployment)")
    report.append("2. **Final compliance audit** across all domains")
    report.append("3. **PSE rule validation** implementation")
    report.append("4. **Archived tools audit** for dependency verification")
    report.append("")

    # Success Metrics
    report.append("## 📈 Success Metrics\n")
    report.append("- **Daily Progress**: Track files tagged per agent")
    report.append("- **Domain Completion**: Monitor domain-by-domain progress")
    report.append("- **Compliance Rate**: Target 95%+ SSOT compliance")
    report.append("- **Validation Coverage**: 100% of tagged files validated")
    report.append("- **Timeline**: Complete within 3 weeks with parallel execution")
    report.append("")

    return "\n".join(report)


def main():
    """CLI interface for coordination report generation."""
    import argparse

    parser = argparse.ArgumentParser(description="SSOT Coordination Report Generator")
    parser.add_argument('--input', '-i', default='ssot_batch_assignments_latest.json',
                       help='Input JSON file with batch assignments')
    parser.add_argument('--output', '-o', default='ssot_coordination_report.md',
                       help='Output coordination report file')

    args = parser.parse_args()

    # Load assignments
    assignments = load_batch_assignments(args.input)
    if not assignments:
        print("❌ No batch assignments found. Run ssot_tagging_batch_assigner.py first.")
        return 1

    # Generate report
    report = generate_coordination_report(assignments)

    # Save report
    with open(args.output, 'w') as f:
        f.write(report)

    print("✅ SSOT Coordination Report Generated")
    print(f"📄 Saved to: {args.output}")
    print(f"📊 Total batches: {assignments.get('summary', {}).get('total_batches', 0)}")
    print(f"📁 Total files: {assignments.get('summary', {}).get('total_files', 0)}")
    print(f"👥 Agents involved: {len(assignments.get('assignments', {}))}")

    return 0


if __name__ == "__main__":
    exit(main())
