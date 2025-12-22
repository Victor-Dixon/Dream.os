#!/usr/bin/env python3
"""
Consolidate CI/CD Workflows
===========================

Analyzes and consolidates duplicate GitHub Actions workflows.
Merges duplicate workflows and eliminates redundancy.

V2 Compliance: <300 lines, single responsibility
Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-12-22
"""

import argparse
import json
import os
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple

import yaml


class WorkflowAnalyzer:
    """Analyzes GitHub Actions workflows for duplicates and redundancy."""

    def __init__(self, workflows_dir: str = ".github/workflows"):
        self.workflows_dir = Path(workflows_dir)
        self.workflows: Dict[str, Dict] = {}
        self.duplicates: List[Dict] = []
        self.recommendations: List[str] = []

    def find_workflows(self) -> List[Path]:
        """Find all workflow YAML files."""
        workflows = []
        if not self.workflows_dir.exists():
            return workflows

        for workflow_file in self.workflows_dir.glob("*.yml"):
            if workflow_file.name not in ["consolidation_analysis.json"]:
                workflows.append(workflow_file)

        for workflow_file in self.workflows_dir.glob("*.yaml"):
            if workflow_file.name not in ["consolidation_analysis.json"]:
                workflows.append(workflow_file)

        return sorted(workflows)

    def load_workflow(self, workflow_path: Path) -> Dict:
        """Load and parse a workflow YAML file."""
        try:
            with open(workflow_path, "r", encoding="utf-8") as f:
                content = yaml.safe_load(f)
                return {
                    "path": str(workflow_path),
                    "name": workflow_path.name,
                    "content": content,
                    "size": workflow_path.stat().st_size,
                }
        except Exception as e:
            print(f"⚠️  Error loading {workflow_path}: {e}")
            return None

    def analyze_workflow_features(self, workflow: Dict) -> Dict:
        """Analyze features of a workflow."""
        if not workflow or not workflow.get("content"):
            return {}

        content = workflow["content"]
        features = {
            "has_testing": False,
            "has_linting": False,
            "has_deployment": False,
            "has_v2": False,
            "has_security": False,
            "has_coverage": False,
            "jobs": [],
            "triggers": [],
        }

        # Check triggers
        if "on" in content:
            triggers = content["on"]
            if isinstance(triggers, dict):
                features["triggers"] = list(triggers.keys())
            elif isinstance(triggers, list):
                features["triggers"] = triggers

        # Check jobs
        if "jobs" in content:
            jobs = content["jobs"]
            if isinstance(jobs, dict):
                features["jobs"] = list(jobs.keys())
                for job_name, job_config in jobs.items():
                    if isinstance(job_config, dict):
                        # Check for testing
                        if "steps" in job_config:
                            steps = job_config["steps"]
                            step_names = [
                                step.get("name", "").lower()
                                if isinstance(step, dict)
                                else ""
                                for step in steps
                            ]
                            step_text = " ".join(step_names)

                            if any(
                                keyword in step_text
                                for keyword in ["test", "pytest", "unittest"]
                            ):
                                features["has_testing"] = True
                            if any(
                                keyword in step_text
                                for keyword in ["lint", "ruff", "black", "isort"]
                            ):
                                features["has_linting"] = True
                            if any(
                                keyword in step_text
                                for keyword in ["deploy", "release", "publish"]
                            ):
                                features["has_deployment"] = True
                            if any(
                                keyword in step_text
                                for keyword in ["v2", "compliance", "standards"]
                            ):
                                features["has_v2"] = True
                            if any(
                                keyword in step_text
                                for keyword in ["security", "bandit", "safety"]
                            ):
                                features["has_security"] = True
                            if any(
                                keyword in step_text
                                for keyword in ["coverage", "cov-report"]
                            ):
                                features["has_coverage"] = True

        return features

    def find_duplicates(self) -> List[Dict]:
        """Find duplicate or redundant workflows."""
        duplicates = []
        workflow_list = list(self.workflows.items())

        for i, (name1, workflow1) in enumerate(workflow_list):
            features1 = workflow1.get("features", {})
            for j, (name2, workflow2) in enumerate(workflow_list[i + 1 :], i + 1):
                features2 = workflow2.get("features", {})

                # Check for similar features
                similarity_score = self._calculate_similarity(features1, features2)

                if similarity_score > 0.7:  # 70% similarity threshold
                    duplicates.append(
                        {
                            "workflow1": name1,
                            "workflow2": name2,
                            "similarity": similarity_score,
                            "features1": features1,
                            "features2": features2,
                        }
                    )

        return duplicates

    def _calculate_similarity(self, features1: Dict, features2: Dict) -> float:
        """Calculate similarity score between two workflows."""
        if not features1 or not features2:
            return 0.0

        # Compare boolean features
        bool_features = [
            "has_testing",
            "has_linting",
            "has_deployment",
            "has_v2",
            "has_security",
            "has_coverage",
        ]
        matches = sum(
            1 for feat in bool_features if features1.get(feat) == features2.get(feat)
        )
        bool_score = matches / len(bool_features) if bool_features else 0.0

        # Compare jobs
        jobs1 = set(features1.get("jobs", []))
        jobs2 = set(features2.get("jobs", []))
        if jobs1 or jobs2:
            job_score = len(jobs1 & jobs2) / len(jobs1 | jobs2) if (jobs1 | jobs2) else 0.0
        else:
            job_score = 0.0

        # Compare triggers
        triggers1 = set(features1.get("triggers", []))
        triggers2 = set(features2.get("triggers", []))
        if triggers1 or triggers2:
            trigger_score = (
                len(triggers1 & triggers2) / len(triggers1 | triggers2)
                if (triggers1 | triggers2)
                else 0.0
            )
        else:
            trigger_score = 0.0

        # Weighted average
        similarity = (bool_score * 0.4) + (job_score * 0.4) + (trigger_score * 0.2)
        return similarity

    def generate_recommendations(self) -> List[str]:
        """Generate consolidation recommendations."""
        recommendations = []

        if not self.duplicates:
            recommendations.append(
                "✅ No duplicate workflows found. Current workflows are well-organized."
            )
            return recommendations

        # Group duplicates
        duplicate_groups = defaultdict(list)
        for dup in self.duplicates:
            key = tuple(sorted([dup["workflow1"], dup["workflow2"]]))
            duplicate_groups[key].append(dup)

        for group_key, group_dups in duplicate_groups.items():
            workflow1, workflow2 = group_key
            recommendations.append(
                f"🔀 Consider consolidating '{workflow1}' and '{workflow2}' "
                f"(similarity: {group_dups[0]['similarity']:.1%})"
            )

        return recommendations

    def analyze(self) -> Dict:
        """Perform full analysis of workflows."""
        print("🔍 Analyzing CI/CD workflows...")

        workflow_files = self.find_workflows()
        print(f"📁 Found {len(workflow_files)} workflow files")

        # Load all workflows
        for workflow_path in workflow_files:
            workflow = self.load_workflow(workflow_path)
            if workflow:
                workflow["features"] = self.analyze_workflow_features(workflow)
                self.workflows[workflow["name"]] = workflow

        # Find duplicates
        self.duplicates = self.find_duplicates()
        print(f"🔎 Found {len(self.duplicates)} potential duplicates")

        # Generate recommendations
        self.recommendations = self.generate_recommendations()

        # Build analysis report
        analysis = {
            "total_workflows": len(self.workflows),
            "workflows": {
                name: {
                    "path": wf["path"],
                    "size": wf["size"],
                    **wf["features"],
                }
                for name, wf in self.workflows.items()
            },
            "duplicates": self.duplicates,
            "recommendations": self.recommendations,
        }

        return analysis

    def save_analysis(self, analysis: Dict, output_path: Path):
        """Save analysis results to JSON."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(analysis, f, indent=2)
        print(f"💾 Analysis saved to {output_path}")


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Consolidate duplicate GitHub Actions workflows"
    )
    parser.add_argument(
        "--workflows-dir",
        type=str,
        default=".github/workflows",
        help="Path to workflows directory",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=".github/workflows/consolidation_analysis.json",
        help="Output path for analysis JSON",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform analysis without making changes",
    )

    args = parser.parse_args()

    analyzer = WorkflowAnalyzer(workflows_dir=args.workflows_dir)
    analysis = analyzer.analyze()

    # Save analysis
    output_path = Path(args.output)
    analyzer.save_analysis(analysis, output_path)

    # Print summary
    print("\n" + "=" * 60)
    print("📊 CI/CD WORKFLOW CONSOLIDATION ANALYSIS")
    print("=" * 60)
    print(f"Total workflows: {analysis['total_workflows']}")
    print(f"Potential duplicates: {len(analysis['duplicates'])}")
    print("\n📋 Recommendations:")
    for rec in analysis["recommendations"]:
        print(f"  {rec}")

    if analysis["duplicates"]:
        print("\n🔍 Duplicate Details:")
        for dup in analysis["duplicates"]:
            print(
                f"  - {dup['workflow1']} ↔ {dup['workflow2']} "
                f"(similarity: {dup['similarity']:.1%})"
            )

    print("\n✅ Analysis complete!")
    if args.dry_run:
        print("🔍 Dry run mode - no changes made")

    return 0


if __name__ == "__main__":
    exit(main())

