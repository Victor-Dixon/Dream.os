#!/usr/bin/env python3
"""
Repository Consolidation Analyzer
==================================

Analyzes GitHub repository analysis files to identify similar repos
that can be consolidated.

Author: Agent-3 (Infrastructure & DevOps) - JET FUEL AUTONOMOUS MODE
Created: 2025-01-27
Priority: CRITICAL
"""

import json
import logging
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RepoConsolidationAnalyzer:
    """Analyze repos for consolidation opportunities."""

    def __init__(self, analysis_dir: str = "swarm_brain/devlogs/repository_analysis"):
        """Initialize analyzer."""
        self.analysis_dir = Path(analysis_dir)
        self.repos = {}
        self.similarity_groups = defaultdict(list)

    def load_all_repos(self) -> dict[str, dict[str, Any]]:
        """Load all repository analysis files."""
        repos = {}
        
        if not self.analysis_dir.exists():
            logger.warning(f"Analysis directory not found: {self.analysis_dir}")
            return repos
        
        for file_path in self.analysis_dir.glob("*.md"):
            try:
                content = file_path.read_text(encoding="utf-8")
                repo_data = self._parse_repo_analysis(content, file_path.name)
                if repo_data:
                    repos[file_path.name] = repo_data
            except Exception as e:
                logger.debug(f"Failed to parse {file_path.name}: {e}")
        
        logger.info(f"✅ Loaded {len(repos)} repository analyses")
        return repos

    def _parse_repo_analysis(self, content: str, filename: str) -> dict[str, Any] | None:
        """Parse repository analysis file."""
        repo_data = {
            "filename": filename,
            "name": self._extract_repo_name(content, filename),
            "agent": self._extract_agent(content),
            "purpose": self._extract_purpose(content),
            "tech_stack": self._extract_tech_stack(content),
            "category": self._extract_category(content),
        }
        
        # Only return if we have at least a name
        if repo_data["name"]:
            return repo_data
        return None

    def _extract_repo_name(self, content: str, filename: str) -> str:
        """Extract repository name."""
        # Try title patterns
        title_match = re.search(r"^#+\s+(.+?)(?:\s+Analysis|\s+Repo)?$", content, re.MULTILINE)
        if title_match:
            return title_match.group(1).strip()
        
        # Try filename patterns
        patterns = [
            r"Repo_(\d+)_(.+?)_Analysis",
            r"github_repo_analysis_\d+_(.+?)$",
            r"agent\d+_repo\d+_(.+?)$",
        ]
        for pattern in patterns:
            match = re.search(pattern, filename, re.IGNORECASE)
            if match:
                return match.group(-1).replace("_", " ").title()
        
        return filename.replace(".md", "").replace("_", " ").title()

    def _extract_agent(self, content: str) -> str:
        """Extract agent identifier."""
        agent_match = re.search(r"Agent-(\d+)", content, re.IGNORECASE)
        if agent_match:
            return f"Agent-{agent_match.group(1)}"
        return "Unknown"

    def _extract_purpose(self, content: str) -> str:
        """Extract repository purpose."""
        purpose_patterns = [
            r"Purpose[:\s]+(.+?)(?:\n|$)",
            r"Description[:\s]+(.+?)(?:\n|$)",
            r"##\s+Purpose\s+(.+?)(?=##|$)",
        ]
        for pattern in purpose_patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                purpose = match.group(1).strip()[:200]
                return purpose
        
        return "Unknown"

    def _extract_tech_stack(self, content: str) -> list[str]:
        """Extract technology stack."""
        tech_keywords = [
            "Python", "JavaScript", "TypeScript", "React", "FastAPI", "Django",
            "Flask", "Node.js", "Discord", "Discord.py", "PyAutoGUI",
            "MongoDB", "PostgreSQL", "SQLite", "Redis", "Docker", "Kubernetes",
        ]
        
        found_tech = []
        content_lower = content.lower()
        for tech in tech_keywords:
            if tech.lower() in content_lower:
                found_tech.append(tech)
        
        return found_tech

    def _extract_category(self, content: str) -> str:
        """Extract repository category."""
        categories = {
            "trading": ["trading", "stock", "options", "finance", "ticker"],
            "discord": ["discord", "bot", "commander"],
            "web": ["web", "website", "frontend", "react", "html"],
            "api": ["api", "fastapi", "flask", "django", "rest"],
            "automation": ["automation", "automate", "script", "tool"],
            "ml": ["machine learning", "ml", "ai", "neural", "model"],
        }
        
        content_lower = content.lower()
        for category, keywords in categories.items():
            if any(keyword in content_lower for keyword in keywords):
                return category
        
        return "other"

    def find_similar_repos(self) -> dict[str, list[dict[str, Any]]]:
        """Find similar repositories that could be consolidated."""
        repos = self.load_all_repos()
        similarity_groups = defaultdict(list)
        
        # Group by category
        for filename, repo_data in repos.items():
            category = repo_data.get("category", "other")
            similarity_groups[f"category_{category}"].append(repo_data)
        
        # Group by tech stack similarity
        tech_groups = defaultdict(list)
        for filename, repo_data in repos.items():
            tech_stack = tuple(sorted(repo_data.get("tech_stack", [])))
            if tech_stack:
                tech_groups[tech_stack].append(repo_data)
        
        # Find groups with 2+ repos (consolidation candidates)
        consolidation_candidates = {}
        
        for group_name, group_repos in similarity_groups.items():
            if len(group_repos) >= 2:
                consolidation_candidates[group_name] = group_repos
        
        for tech_stack, group_repos in tech_groups.items():
            if len(group_repos) >= 2:
                key = f"tech_{'_'.join(tech_stack[:3])}"
                consolidation_candidates[key] = group_repos
        
        return consolidation_candidates

    def generate_consolidation_report(self) -> dict[str, Any]:
        """Generate consolidation analysis report."""
        repos = self.load_all_repos()
        candidates = self.find_similar_repos()
        
        report = {
            "total_repos": len(repos),
            "consolidation_groups": len(candidates),
            "candidates": {},
            "summary": {},
        }
        
        for group_name, group_repos in candidates.items():
            report["candidates"][group_name] = {
                "count": len(group_repos),
                "repos": [
                    {
                        "name": r.get("name", "Unknown"),
                        "filename": r.get("filename", ""),
                        "agent": r.get("agent", "Unknown"),
                        "category": r.get("category", "other"),
                        "tech_stack": r.get("tech_stack", []),
                    }
                    for r in group_repos
                ],
            }
        
        # Summary statistics
        categories = defaultdict(int)
        for repo_data in repos.values():
            categories[repo_data.get("category", "other")] += 1
        
        report["summary"] = {
            "by_category": dict(categories),
            "consolidation_opportunities": sum(1 for g in candidates.values() if len(g) >= 2),
        }
        
        return report

    def print_consolidation_report(self) -> None:
        """Print human-readable consolidation report."""
        report = self.generate_consolidation_report()
        
        print("\n" + "="*70)
        print("📚 REPOSITORY CONSOLIDATION ANALYSIS")
        print("="*70)
        print(f"Total Repos Analyzed: {report['total_repos']}")
        print(f"Consolidation Groups: {report['consolidation_groups']}")
        print()
        
        print("📊 SUMMARY BY CATEGORY:")
        for category, count in report["summary"]["by_category"].items():
            print(f"  {category}: {count} repos")
        print()
        
        print("🔗 CONSOLIDATION OPPORTUNITIES:")
        for group_name, group_data in report["candidates"].items():
            if group_data["count"] >= 2:
                print(f"\n  {group_name} ({group_data['count']} repos):")
                for repo in group_data["repos"]:
                    print(f"    • {repo['name']} ({repo['agent']}) - {repo['category']}")
                    if repo['tech_stack']:
                        print(f"      Tech: {', '.join(repo['tech_stack'][:5])}")
        print()
        
        print("="*70 + "\n")


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Repository Consolidation Analyzer")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--analysis-dir", default="swarm_brain/devlogs/repository_analysis", help="Analysis directory")
    
    args = parser.parse_args()
    
    analyzer = RepoConsolidationAnalyzer(analysis_dir=args.analysis_dir)
    
    if args.json:
        report = analyzer.generate_consolidation_report()
        print(json.dumps(report, indent=2))
    else:
        analyzer.print_consolidation_report()


if __name__ == "__main__":
    main()




