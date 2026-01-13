#!/usr/bin/env python3
"""
Root Directory Analysis - 2026-01-13
====================================

Comprehensive analysis of root directory clutter and cleanup opportunities.
Based on the root directory cleanup plan and current file structure.

Author: Agent-1 (Integration & Core Systems Specialist)
"""

import os
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime


class RootDirectoryAnalyzer:
    """Analyzes root directory structure and provides cleanup recommendations."""

    def __init__(self, root_path: str = "D:\\Agent_Cellphone_V2_Repository"):
        self.root_path = Path(root_path)
        self.analysis_results = {
            "timestamp": datetime.now().isoformat(),
            "total_files": 0,
            "total_dirs": 0,
            "categories": {},
            "issues": [],
            "recommendations": [],
            "cleanup_plan": {}
        }

    def analyze_directory(self) -> dict:
        """Perform complete directory analysis."""
        print("🔍 Analyzing root directory structure...")

        # Get all items in root
        root_items = list(self.root_path.iterdir())

        # Categorize items
        self._categorize_items(root_items)

        # Analyze issues
        self._analyze_issues()

        # Generate recommendations
        self._generate_recommendations()

        # Create cleanup plan
        self._create_cleanup_plan()

        return self.analysis_results

    def _categorize_items(self, items):
        """Categorize root directory items."""
        categories = defaultdict(list)
        total_files = 0
        total_dirs = 0

        for item in items:
            if item.is_file():
                total_files += 1
                category = self._categorize_file(item)
                categories[category].append(str(item.name))
            elif item.is_dir():
                total_dirs += 1
                category = self._categorize_directory(item)
                categories[category].append(str(item.name))

        self.analysis_results.update({
            "total_files": total_files,
            "total_dirs": total_dirs,
            "categories": dict(categories)
        })

    def _categorize_file(self, file_path: Path) -> str:
        """Categorize a file based on its name and extension."""
        name = file_path.name.lower()

        # Configuration files
        if any(name.startswith(prefix) for prefix in ['.env', 'config', 'agent_mode', 'cursor_agent', 'coordination_cache']):
            return "configuration"
        if name.endswith(('.json', '.yaml', '.yml', '.toml', '.ini')) and not name.startswith('.'):
            return "configuration"

        # Documentation
        if name.endswith('.md') and name not in ['readme.md', 'changelog.md']:
            return "documentation"

        # Scripts and utilities
        if name.endswith('.py') and any(keyword in name for keyword in [
            'test_', 'check_', 'debug_', 'audit_', 'merge_', 'set_env',
            'discord_', 'deploy_', 'generate_', 'stop_', 'temp_removed_'
        ]):
            return "scripts_utilities"

        # Development logs and reports
        if any(keyword in name for keyword in [
            'devlog', 'progress', 'report', 'audit', 'status', 'summary',
            'accomplishments', 'validation', 'completion', 'victory',
            'revolution', 'consolidation', 'final_', 'today_', 'phase'
        ]):
            return "development_logs"

        # Logs and temporary files
        if any(name.endswith(ext) for ext in ['.log', '.txt']) or 'temp' in name:
            return "logs_temp"

        # Build and cache
        if any(name.startswith(prefix) for prefix in ['__pycache__', '.pytest', '.benchmarks', '.coverage']):
            return "build_cache"

        # Core files (keep in root)
        core_files = {
            'readme.md', 'changelog.md', 'requirements.txt', 'setup.py',
            'main.py', 'pyproject.toml', 'dockerfile', 'docker-compose.yml',
            '.gitignore', 'pytest.ini', 'manifest.in'
        }
        if name in core_files:
            return "core_files"

        # Archives and backups
        if 'archive' in name or 'backup' in name:
            return "archives"

        return "uncategorized"

    def _categorize_directory(self, dir_path: Path) -> str:
        """Categorize a directory."""
        name = dir_path.name.lower()

        # Standard project directories
        standard_dirs = {
            'src', 'docs', 'tests', 'config', 'scripts', 'tools',
            'agent_workspaces', 'reports', 'assets', 'data',
            'logs', 'cache', 'fsm_data', 'message_queue',
            'migrations', 'runtime', 'validation_results', 'website_data'
        }
        if name in standard_dirs:
            return "standard_project_dirs"

        # Development and build
        if any(name.startswith(prefix) for prefix in ['.git', '.cursor', '.github', '__pycache__', '.pytest', '.coveragerc']):
            return "development_build"

        # Archives
        if 'archive' in name:
            return "archives"

        # Agent workspaces (should be organized)
        if name.startswith('agent-') or name == 'captain':
            return "agent_workspaces"

        return "other_directories"

    def _analyze_issues(self):
        """Analyze directory structure issues."""
        categories = self.analysis_results["categories"]

        # Issue 1: Too many files in root
        total_files = self.analysis_results["total_files"]
        if total_files > 50:
            self.analysis_results["issues"].append({
                "type": "excessive_root_files",
                "severity": "high",
                "description": f"Too many files in root directory: {total_files} (target: <40)",
                "impact": "Poor navigation, maintenance difficulty"
            })

        # Issue 2: Configuration scatter
        config_files = len(categories.get("configuration", []))
        if config_files > 5:
            self.analysis_results["issues"].append({
                "type": "configuration_scatter",
                "severity": "medium",
                "description": f"Too many configuration files: {config_files} (target: 2-3)",
                "impact": "Hard to manage configuration"
            })

        # Issue 3: Documentation clutter
        doc_files = len(categories.get("documentation", []))
        if doc_files > 3:
            self.analysis_results["issues"].append({
                "type": "documentation_clutter",
                "severity": "medium",
                "description": f"Too many documentation files in root: {doc_files} (target: 2)",
                "impact": "Hard to find important documentation"
            })

        # Issue 4: Script pollution
        script_files = len(categories.get("scripts_utilities", []))
        if script_files > 10:
            self.analysis_results["issues"].append({
                "type": "script_pollution",
                "severity": "medium",
                "description": f"Too many utility scripts in root: {script_files} (target: <5)",
                "impact": "Cluttered root directory"
            })

        # Issue 5: Log file presence
        log_files = len(categories.get("logs_temp", []))
        if log_files > 0:
            self.analysis_results["issues"].append({
                "type": "log_files_in_root",
                "severity": "low",
                "description": f"Log files in root directory: {log_files}",
                "impact": "Should be in logs/ directory or ignored"
            })

    def _generate_recommendations(self):
        """Generate cleanup recommendations."""
        categories = self.analysis_results["categories"]

        # General recommendations
        self.analysis_results["recommendations"].extend([
            "Create proper directory structure following Python project conventions",
            "Move configuration files to config/ directory",
            "Relocate documentation to docs/ subdirectories",
            "Organize scripts into scripts/ subdirectories",
            "Archive development logs to docs/devlogs/",
            "Remove or ignore log files and cache directories"
        ])

        # Specific recommendations based on categories
        if "configuration" in categories:
            config_files = categories["configuration"]
            self.analysis_results["recommendations"].append(
                f"Consolidate {len(config_files)} configuration files into 2-3 organized configs"
            )

        if "scripts_utilities" in categories:
            script_files = categories["scripts_utilities"]
            self.analysis_results["recommendations"].append(
                f"Move {len(script_files)} utility scripts to appropriate scripts/ subdirectories"
            )

        if "development_logs" in categories:
            log_files = categories["development_logs"]
            self.analysis_results["recommendations"].append(
                f"Archive {len(log_files)} development logs to docs/devlogs/"
            )

    def _create_cleanup_plan(self):
        """Create detailed cleanup execution plan."""
        categories = self.analysis_results["categories"]

        cleanup_plan = {
            "phase_1_config_consolidation": {
                "priority": "HIGH",
                "description": "Consolidate configuration files",
                "actions": [],
                "estimated_files": 0
            },
            "phase_2_documentation_relocation": {
                "priority": "MEDIUM",
                "description": "Move documentation to docs/ subdirectories",
                "actions": [],
                "estimated_files": 0
            },
            "phase_3_script_organization": {
                "priority": "MEDIUM",
                "description": "Organize scripts into subdirectories",
                "actions": [],
                "estimated_files": 0
            },
            "phase_4_log_archive": {
                "priority": "LOW",
                "description": "Archive development logs and clean temporary files",
                "actions": [],
                "estimated_files": 0
            }
        }

        # Phase 1: Configuration consolidation
        if "configuration" in categories:
            config_files = categories["configuration"]
            cleanup_plan["phase_1_config_consolidation"]["actions"] = [
                "Create config/agent_config.json from agent_mode_config.json, cursor_agent_coords.json",
                "Create config/coordination_config.json from coordination_cache.json",
                "Keep only .env.example in root, archive others",
                "Consolidate pre-commit configs to single platform-specific version"
            ]
            cleanup_plan["phase_1_config_consolidation"]["estimated_files"] = len(config_files) - 3

        # Phase 2: Documentation relocation
        if "documentation" in categories:
            doc_files = categories["documentation"]
            cleanup_plan["phase_2_documentation_relocation"]["actions"] = [
                "Move CONTRIBUTING.md and guides to docs/contributing/",
                "Move project documentation to docs/guides/",
                "Keep only README.md and CHANGELOG.md in root"
            ]
            cleanup_plan["phase_2_documentation_relocation"]["estimated_files"] = len(doc_files) - 2

        # Phase 3: Script organization
        if "scripts_utilities" in categories:
            script_files = categories["scripts_utilities"]
            cleanup_plan["phase_3_script_organization"]["actions"] = [
                "Create scripts/tests/ for test utilities",
                "Create scripts/discord/ for Discord-related scripts",
                "Create scripts/utilities/ for general utilities",
                "Move main.py and core scripts appropriately"
            ]
            cleanup_plan["phase_3_script_organization"]["estimated_files"] = len(script_files) - 3

        # Phase 4: Log archive
        if "development_logs" in categories:
            log_files = categories["development_logs"]
            cleanup_plan["phase_4_log_archive"]["actions"] = [
                "Create docs/devlogs/ directory",
                "Move all devlog files to docs/devlogs/",
                "Create reports/archive/ for historical reports",
                "Remove temporary log files"
            ]
            cleanup_plan["phase_4_log_archive"]["estimated_files"] = len(log_files)

        self.analysis_results["cleanup_plan"] = cleanup_plan


def main():
    """Run root directory analysis."""
    print("🔍 Root Directory Analysis")
    print("=" * 50)

    analyzer = RootDirectoryAnalyzer()
    results = analyzer.analyze_directory()

    # Print summary
    print("\n📊 ANALYSIS SUMMARY:")
    print(f"Total files in root: {results['total_files']}")
    print(f"Total directories: {results['total_dirs']}")

    print("\n📁 FILE CATEGORIES:")
    for category, files in results["categories"].items():
        print(f"  {category}: {len(files)} files")

    if results["issues"]:
        print("\n🚨 ISSUES IDENTIFIED:")
        for i, issue in enumerate(results["issues"], 1):
            severity_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(issue["severity"], "⚪")
            print(f"{i}. {severity_emoji} {issue['type']}: {issue['description']}")

    print("\n📋 CLEANUP PLAN:")
    total_reduction = 0
    for phase, details in results["cleanup_plan"].items():
        if details["estimated_files"] > 0:
            print(f"  {phase.upper()}: {details['estimated_files']} files ({details['priority']})")
            total_reduction += details["estimated_files"]

    print(f"\n🎯 ESTIMATED REDUCTION: {total_reduction} files ({total_reduction/results['total_files']*100:.1f}%)")

    # Save detailed results
    output_file = "root_directory_analysis_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n📄 Detailed results saved to: {output_file}")

    if results["recommendations"]:
        print("\n💡 KEY RECOMMENDATIONS:")
        for rec in results["recommendations"]:
            print(f"• {rec}")

    print("\n✅ Root directory analysis completed!")


if __name__ == "__main__":
    main()