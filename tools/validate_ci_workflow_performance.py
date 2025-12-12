#!/usr/bin/env python3
"""
Validate CI Workflow Performance
=================================

Analyzes CI workflow files for performance issues and optimization opportunities.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Task: CP-010

<!-- SSOT Domain: infrastructure -->
"""

import yaml
import json
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime


def analyze_workflow_file(workflow_path: Path) -> Dict:
    """Analyze a single workflow file for performance issues."""
    print(f"\n{'='*60}")
    print(f"📋 Analyzing: {workflow_path.name}")
    print(f"{'='*60}")
    
    results = {
        "file": str(workflow_path),
        "jobs": [],
        "issues": [],
        "optimizations": [],
        "total_jobs": 0,
        "estimated_time": 0
    }
    
    try:
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)
        
        if not workflow or 'jobs' not in workflow:
            print("⚠️  No jobs found in workflow")
            return results
        
        results["total_jobs"] = len(workflow['jobs'])
        print(f"Jobs: {results['total_jobs']}")
        
        for job_name, job_config in workflow['jobs'].items():
            job_analysis = analyze_job(job_name, job_config)
            results["jobs"].append(job_analysis)
            results["estimated_time"] += job_analysis.get("estimated_time", 0)
            
            if job_analysis.get("issues"):
                results["issues"].extend(job_analysis["issues"])
            if job_analysis.get("optimizations"):
                results["optimizations"].extend(job_analysis["optimizations"])
        
        # Overall workflow analysis
        analyze_workflow_structure(workflow, results)
        
    except Exception as e:
        print(f"❌ Error analyzing workflow: {e}")
        results["issues"].append(f"Error parsing workflow: {e}")
    
    return results


def analyze_job(job_name: str, job_config: Dict) -> Dict:
    """Analyze a single job for performance issues."""
    analysis = {
        "name": job_name,
        "runs_on": job_config.get("runs-on", "unknown"),
        "timeout": job_config.get("timeout-minutes"),
        "estimated_time": job_config.get("timeout-minutes", 60),
        "steps": len(job_config.get("steps", [])),
        "strategy": job_config.get("strategy"),
        "needs": job_config.get("needs", []),
        "issues": [],
        "optimizations": []
    }
    
    # Check for timeout
    if not analysis["timeout"]:
        analysis["issues"].append("No timeout set - risk of hanging jobs")
        analysis["optimizations"].append("Add timeout-minutes to prevent hanging")
    
    # Check for matrix strategy
    if analysis["strategy"]:
        matrix = analysis["strategy"].get("matrix", {})
        matrix_size = 1
        for values in matrix.values():
            if isinstance(values, list):
                matrix_size *= len(values)
        if matrix_size > 4:
            analysis["issues"].append(f"Large matrix strategy ({matrix_size} combinations) - may cause timeouts")
            analysis["optimizations"].append(f"Consider reducing matrix size or using conditional jobs")
    
    # Check for parallel execution
    steps = job_config.get("steps", [])
    has_parallel = any("&" in str(step) or "wait" in str(step) for step in steps)
    if not has_parallel and len(steps) > 5:
        analysis["optimizations"].append("Consider parallel step execution for faster runs")
    
    # Check for caching
    has_cache = any("cache" in str(step).lower() for step in steps)
    if not has_cache:
        analysis["optimizations"].append("Add pip/cache steps to speed up dependency installation")
    
    # Check for continue-on-error misuse
    continue_on_error_count = sum(1 for step in steps if step.get("continue-on-error"))
    if continue_on_error_count == len(steps):
        analysis["issues"].append("All steps have continue-on-error - may hide failures")
    
    return analysis


def analyze_workflow_structure(workflow: Dict, results: Dict):
    """Analyze overall workflow structure."""
    jobs = workflow.get("jobs", {})
    
    # Check for sequential dependencies
    job_deps = {}
    for job_name, job_config in jobs.items():
        needs = job_config.get("needs", [])
        job_deps[job_name] = needs
    
    # Find longest dependency chain
    max_chain = find_longest_chain(job_deps)
    if max_chain > 3:
        results["issues"].append(f"Long dependency chain ({max_chain} jobs) - consider parallelization")
        results["optimizations"].append("Break dependency chains to enable parallel execution")
    
    # Check for conditional jobs
    conditional_count = sum(1 for job_config in jobs.values() if "if:" in str(job_config))
    if conditional_count > 0:
        results["optimizations"].append(f"{conditional_count} conditional jobs - good for optimization")


def find_longest_chain(deps: Dict) -> int:
    """Find the longest dependency chain."""
    def chain_length(job: str, visited: set) -> int:
        if job in visited:
            return 0
        visited.add(job)
        if job not in deps or not deps[job]:
            return 1
        return 1 + max((chain_length(dep, visited.copy()) for dep in deps[job]), default=0)
    
    max_len = 0
    for job in deps:
        max_len = max(max_len, chain_length(job, set()))
    return max_len


def generate_optimization_report(all_results: List[Dict]) -> str:
    """Generate optimization report."""
    report = []
    report.append("# CI Workflow Performance Analysis\n")
    report.append(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report.append(f"**Task**: CP-010 - Optimize CI workflow performance\n\n")
    
    total_jobs = sum(r["total_jobs"] for r in all_results)
    total_issues = sum(len(r["issues"]) for r in all_results)
    total_optimizations = sum(len(r["optimizations"]) for r in all_results)
    total_time = sum(r["estimated_time"] for r in all_results)
    
    report.append("## Summary\n\n")
    report.append(f"- **Workflows Analyzed**: {len(all_results)}\n")
    report.append(f"- **Total Jobs**: {total_jobs}\n")
    report.append(f"- **Estimated Total Time**: {total_time} minutes\n")
    report.append(f"- **Issues Found**: {total_issues}\n")
    report.append(f"- **Optimizations Suggested**: {total_optimizations}\n\n")
    
    # Issues
    if total_issues > 0:
        report.append("## Issues Found\n\n")
        for result in all_results:
            if result["issues"]:
                report.append(f"### {Path(result['file']).name}\n\n")
                for issue in result["issues"]:
                    report.append(f"- ⚠️  {issue}\n")
                report.append("\n")
    
    # Optimizations
    if total_optimizations > 0:
        report.append("## Optimization Recommendations\n\n")
        for result in all_results:
            if result["optimizations"]:
                report.append(f"### {Path(result['file']).name}\n\n")
                for opt in result["optimizations"]:
                    report.append(f"- 💡 {opt}\n")
                report.append("\n")
    
    # Per-workflow details
    report.append("## Workflow Details\n\n")
    for result in all_results:
        report.append(f"### {Path(result['file']).name}\n\n")
        report.append(f"- Jobs: {result['total_jobs']}\n")
        report.append(f"- Estimated Time: {result['estimated_time']} minutes\n")
        report.append(f"- Issues: {len(result['issues'])}\n")
        report.append(f"- Optimizations: {len(result['optimizations'])}\n\n")
    
    return "".join(report)


def main():
    """Main analysis function."""
    print("=" * 60)
    print("🔍 CI Workflow Performance Analysis")
    print("=" * 60)
    print("Task: CP-010 - Optimize CI workflow performance\n")
    
    workflows_dir = Path(".github/workflows")
    if not workflows_dir.exists():
        print("❌ .github/workflows directory not found")
        return
    
    workflow_files = list(workflows_dir.glob("*.yml")) + list(workflows_dir.glob("*.yaml"))
    
    if not workflow_files:
        print("⚠️  No workflow files found")
        return
    
    print(f"Found {len(workflow_files)} workflow file(s)\n")
    
    all_results = []
    for workflow_file in workflow_files:
        result = analyze_workflow_file(workflow_file)
        all_results.append(result)
    
    # Generate report
    report = generate_optimization_report(all_results)
    
    # Save report
    report_file = Path("agent_workspaces/Agent-3/ci_workflow_performance_analysis_2025-12-12.md")
    report_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_file, 'w') as f:
        f.write(report)
    
    print("\n" + "=" * 60)
    print("📊 Analysis Complete")
    print("=" * 60)
    
    total_issues = sum(len(r["issues"]) for r in all_results)
    total_optimizations = sum(len(r["optimizations"]) for r in all_results)
    
    print(f"\n✅ Analyzed {len(all_results)} workflow(s)")
    print(f"⚠️  Found {total_issues} issue(s)")
    print(f"💡 Suggested {total_optimizations} optimization(s)")
    print(f"\n📄 Report saved: {report_file}")
    print()


if __name__ == "__main__":
    try:
        import yaml
    except ImportError:
        print("❌ PyYAML not installed. Install with: pip install pyyaml")
        sys.exit(1)
    
    import sys
    main()

