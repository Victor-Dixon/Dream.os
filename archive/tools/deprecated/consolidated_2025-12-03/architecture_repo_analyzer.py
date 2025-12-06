#!/usr/bin/env python3
"""
Architecture-Focused Repository Analyzer
=========================================

Enhances repo analysis with architectural insights for better GitHub merge decisions:
- Architecture pattern detection (MVC, microservices, monolith, etc.)
- Dependency compatibility analysis
- Merge risk assessment
- Code structure analysis
- Architecture compatibility scoring

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-01-28
Purpose: Improve repo analysis for GitHub merge focus
"""

import json
import re
import ast
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple
from dataclasses import dataclass, asdict


@dataclass
class ArchitecturePattern:
    """Architecture pattern detected in repo."""
    pattern_type: str  # MVC, microservices, monolith, layered, etc.
    confidence: float  # 0-1
    evidence: List[str]  # Files/patterns that indicate this


@dataclass
class DependencyAnalysis:
    """Dependency compatibility analysis."""
    shared_dependencies: List[str]
    conflicting_dependencies: List[str]
    compatibility_score: float  # 0-1
    merge_risk: str  # LOW, MEDIUM, HIGH


@dataclass
class CodeStructure:
    """Code structure analysis."""
    organization_pattern: str  # flat, nested, modular, etc.
    main_language: str
    file_count: int
    avg_file_size: int
    has_tests: bool
    has_docs: bool


@dataclass
class RepoArchitecture:
    """Complete architecture analysis for a repo."""
    repo_num: int
    repo_name: str
    architecture_patterns: List[ArchitecturePattern]
    dependencies: List[str]
    code_structure: CodeStructure
    merge_complexity: str  # LOW, MEDIUM, HIGH
    architecture_score: float  # 0-100


class ArchitectureRepoAnalyzer:
    """Analyzes repositories from architectural perspective."""
    
    def __init__(self):
        self.master_list_path = Path("data/github_75_repos_master_list.json")
        self.devlogs_path = Path("swarm_brain/devlogs/repository_analysis")
        self.repos: Dict[int, RepoArchitecture] = {}
        
    def load_master_list(self) -> Dict[int, Dict[str, Any]]:
        """Load master repo list."""
        if not self.master_list_path.exists():
            return {}
        
        try:
            data = json.loads(self.master_list_path.read_text())
            repos = {}
            if "repos" in data:
                for repo in data["repos"]:
                    num = repo.get("num")
                    if num:
                        repos[num] = repo
            return repos
        except Exception as e:
            print(f"⚠️ Error loading master list: {e}")
            return {}
    
    def detect_architecture_pattern(self, content: str, files: List[str]) -> List[ArchitecturePattern]:
        """Detect architecture patterns from code structure."""
        patterns = []
        
        # MVC Pattern Detection
        mvc_indicators = [
            r'class.*Controller',
            r'class.*Model',
            r'class.*View',
            r'views?/',
            r'models?/',
            r'controllers?/',
        ]
        mvc_evidence = []
        for indicator in mvc_indicators:
            if re.search(indicator, content, re.IGNORECASE):
                mvc_evidence.append(f"MVC indicator: {indicator}")
        if len(mvc_evidence) >= 2:
            patterns.append(ArchitecturePattern(
                pattern_type="MVC",
                confidence=min(0.9, len(mvc_evidence) * 0.3),
                evidence=mvc_evidence[:3]
            ))
        
        # Microservices Pattern Detection
        microservices_indicators = [
            r'service',
            r'api',
            r'gateway',
            r'docker',
            r'kubernetes',
            r'microservice',
        ]
        microservices_evidence = []
        for indicator in microservices_indicators:
            if re.search(indicator, content, re.IGNORECASE):
                microservices_evidence.append(f"Microservices indicator: {indicator}")
        if len(microservices_evidence) >= 3:
            patterns.append(ArchitecturePattern(
                pattern_type="Microservices",
                confidence=min(0.8, len(microservices_evidence) * 0.25),
                evidence=microservices_evidence[:3]
            ))
        
        # Layered Architecture Detection
        layered_indicators = [
            r'layer',
            r'presentation',
            r'business',
            r'data',
            r'repository',
            r'service',
        ]
        layered_evidence = []
        for indicator in layered_indicators:
            if re.search(indicator, content, re.IGNORECASE):
                layered_evidence.append(f"Layered indicator: {indicator}")
        if len(layered_evidence) >= 3:
            patterns.append(ArchitecturePattern(
                pattern_type="Layered",
                confidence=min(0.75, len(layered_evidence) * 0.25),
                evidence=layered_evidence[:3]
            ))
        
        # Monolith Detection (default if no other pattern)
        if not patterns:
            patterns.append(ArchitecturePattern(
                pattern_type="Monolith",
                confidence=0.6,
                evidence=["No clear architectural pattern detected"]
            ))
        
        return patterns
    
    def analyze_dependencies(self, content: str) -> List[str]:
        """Extract dependencies from code."""
        dependencies = []
        
        # Python dependencies
        python_patterns = [
            r'import\s+(\w+)',
            r'from\s+(\w+)\s+import',
            r'requirements\.txt.*?(\w+)[=><]',
        ]
        for pattern in python_patterns:
            matches = re.findall(pattern, content)
            dependencies.extend(matches)
        
        # JavaScript/Node dependencies
        js_patterns = [
            r'require\([\'"](\w+)[\'"]\)',
            r'import.*?from\s+[\'"](\w+)[\'"]',
            r'"dependencies".*?"(\w+)"',
        ]
        for pattern in js_patterns:
            matches = re.findall(pattern, content)
            dependencies.extend(matches)
        
        return list(set(dependencies))
    
    def analyze_code_structure(self, files: List[str], content: str) -> CodeStructure:
        """Analyze code structure and organization."""
        # Determine organization pattern
        has_nested = any('/' in f or '\\' in f for f in files)
        has_modules = any('__init__.py' in f or 'package.json' in f for f in files)
        
        if has_modules and has_nested:
            org_pattern = "modular"
        elif has_nested:
            org_pattern = "nested"
        else:
            org_pattern = "flat"
        
        # Detect main language
        languages = defaultdict(int)
        for file in files:
            ext = Path(file).suffix.lower()
            if ext == '.py':
                languages['Python'] += 1
            elif ext in ['.js', '.ts', '.jsx', '.tsx']:
                languages['JavaScript/TypeScript'] += 1
            elif ext in ['.java']:
                languages['Java'] += 1
            elif ext in ['.cpp', '.c', '.h']:
                languages['C/C++'] += 1
        
        main_language = max(languages.items(), key=lambda x: x[1])[0] if languages else "Unknown"
        
        # Check for tests and docs
        has_tests = any('test' in f.lower() or 'spec' in f.lower() for f in files)
        has_docs = any('readme' in f.lower() or 'doc' in f.lower() for f in files)
        
        # Estimate file count and size
        file_count = len(files)
        avg_size = len(content) // max(file_count, 1)
        
        return CodeStructure(
            organization_pattern=org_pattern,
            main_language=main_language,
            file_count=file_count,
            avg_file_size=avg_size,
            has_tests=has_tests,
            has_docs=has_docs
        )
    
    def calculate_merge_compatibility(self, repo1: RepoArchitecture, repo2: RepoArchitecture) -> Dict[str, Any]:
        """Calculate merge compatibility between two repos."""
        # Architecture pattern compatibility
        patterns1 = {p.pattern_type for p in repo1.architecture_patterns}
        patterns2 = {p.pattern_type for p in repo2.architecture_patterns}
        pattern_match = len(patterns1 & patterns2) > 0
        
        # Dependency compatibility
        deps1 = set(repo1.dependencies)
        deps2 = set(repo2.dependencies)
        shared_deps = deps1 & deps2
        conflicting_deps = []
        
        # Check for version conflicts (simplified)
        for dep in shared_deps:
            # In real implementation, check versions
            pass
        
        compatibility_score = (
            (len(shared_deps) / max(len(deps1 | deps2), 1)) * 0.4 +
            (1.0 if pattern_match else 0.0) * 0.4 +
            (1.0 if repo1.code_structure.main_language == repo2.code_structure.main_language else 0.0) * 0.2
        )
        
        # Determine merge risk
        if compatibility_score >= 0.7:
            merge_risk = "LOW"
        elif compatibility_score >= 0.4:
            merge_risk = "MEDIUM"
        else:
            merge_risk = "HIGH"
        
        return {
            "compatibility_score": compatibility_score,
            "merge_risk": merge_risk,
            "shared_dependencies": list(shared_deps),
            "conflicting_dependencies": conflicting_deps,
            "architecture_match": pattern_match,
            "language_match": repo1.code_structure.main_language == repo2.code_structure.main_language
        }
    
    def analyze_repo(self, repo_num: int, repo_data: Dict[str, Any]) -> RepoArchitecture:
        """Analyze single repository architecture."""
        # Load devlog if available
        devlog_files = list(self.devlogs_path.glob(f"*{repo_num}*.md"))
        content = ""
        files = []
        
        if devlog_files:
            try:
                content = devlog_files[0].read_text(encoding='utf-8')
                # Extract file list from devlog
                file_matches = re.findall(r'[-*]\s+([^\s]+\.(py|js|ts|java|cpp|h))', content)
                files = [f[0] for f in file_matches]
            except Exception:
                pass
        
        # Detect architecture patterns
        patterns = self.detect_architecture_pattern(content, files)
        
        # Analyze dependencies
        dependencies = self.analyze_dependencies(content)
        
        # Analyze code structure
        code_structure = self.analyze_code_structure(files, content)
        
        # Calculate architecture score
        architecture_score = (
            (1.0 if code_structure.has_tests else 0.0) * 30 +
            (1.0 if code_structure.has_docs else 0.0) * 20 +
            (min(code_structure.file_count / 50, 1.0)) * 20 +
            (1.0 if code_structure.organization_pattern == "modular" else 0.5) * 30
        )
        
        # Determine merge complexity
        if architecture_score >= 70:
            merge_complexity = "LOW"
        elif architecture_score >= 40:
            merge_complexity = "MEDIUM"
        else:
            merge_complexity = "HIGH"
        
        return RepoArchitecture(
            repo_num=repo_num,
            repo_name=repo_data.get("name", f"Repo-{repo_num}"),
            architecture_patterns=patterns,
            dependencies=dependencies,
            code_structure=code_structure,
            merge_complexity=merge_complexity,
            architecture_score=architecture_score
        )
    
    def analyze_all_repos(self) -> Dict[int, RepoArchitecture]:
        """Analyze all repositories."""
        master_list = self.load_master_list()
        
        print(f"📊 Analyzing {len(master_list)} repositories for architecture patterns...")
        
        for repo_num, repo_data in master_list.items():
            try:
                architecture = self.analyze_repo(repo_num, repo_data)
                self.repos[repo_num] = architecture
            except Exception as e:
                print(f"⚠️ Error analyzing repo {repo_num}: {e}")
        
        return self.repos
    
    def generate_merge_recommendations(self) -> List[Dict[str, Any]]:
        """Generate merge recommendations based on architecture compatibility."""
        recommendations = []
        
        # Compare all pairs
        repo_nums = sorted(self.repos.keys())
        for i, num1 in enumerate(repo_nums):
            for num2 in repo_nums[i+1:]:
                repo1 = self.repos[num1]
                repo2 = self.repos[num2]
                
                compatibility = self.calculate_merge_compatibility(repo1, repo2)
                
                if compatibility["compatibility_score"] >= 0.5:
                    recommendations.append({
                        "repo1": {
                            "num": num1,
                            "name": repo1.repo_name,
                            "architecture": repo1.architecture_patterns[0].pattern_type if repo1.architecture_patterns else "Unknown",
                            "complexity": repo1.merge_complexity
                        },
                        "repo2": {
                            "num": num2,
                            "name": repo2.repo_name,
                            "architecture": repo2.architecture_patterns[0].pattern_type if repo2.architecture_patterns else "Unknown",
                            "complexity": repo2.merge_complexity
                        },
                        "compatibility": compatibility,
                        "recommendation": "MERGE" if compatibility["merge_risk"] == "LOW" else "REVIEW"
                    })
        
        # Sort by compatibility score
        recommendations.sort(key=lambda x: x["compatibility"]["compatibility_score"], reverse=True)
        
        return recommendations
    
    def save_analysis(self, output_path: Path):
        """Save analysis results to JSON."""
        output = {
            "repos": {
                str(num): {
                    "repo_num": arch.repo_num,
                    "repo_name": arch.repo_name,
                    "architecture_patterns": [
                        {
                            "pattern_type": p.pattern_type,
                            "confidence": p.confidence,
                            "evidence": p.evidence
                        }
                        for p in arch.architecture_patterns
                    ],
                    "dependencies": arch.dependencies,
                    "code_structure": asdict(arch.code_structure),
                    "merge_complexity": arch.merge_complexity,
                    "architecture_score": arch.architecture_score
                }
                for num, arch in self.repos.items()
            },
            "merge_recommendations": self.generate_merge_recommendations()
        }
        
        output_path.write_text(json.dumps(output, indent=2))
        print(f"✅ Analysis saved to {output_path}")


def main():
    """Main execution."""
    analyzer = ArchitectureRepoAnalyzer()
    
    print("=" * 70)
    print("🏗️ ARCHITECTURE-FOCUSED REPOSITORY ANALYZER")
    print("=" * 70)
    print()
    
    # Analyze all repos
    repos = analyzer.analyze_all_repos()
    
    print(f"✅ Analyzed {len(repos)} repositories")
    print()
    
    # Generate recommendations
    recommendations = analyzer.generate_merge_recommendations()
    
    print(f"📋 Generated {len(recommendations)} merge recommendations")
    print()
    
    # Show top recommendations
    print("Top 10 Architecture-Compatible Merge Recommendations:")
    print("-" * 70)
    for i, rec in enumerate(recommendations[:10], 1):
        print(f"{i}. {rec['repo1']['name']} (#{rec['repo1']['num']}) + {rec['repo2']['name']} (#{rec['repo2']['num']})")
        print(f"   Compatibility: {rec['compatibility']['compatibility_score']:.2%}")
        print(f"   Risk: {rec['compatibility']['merge_risk']}")
        print(f"   Architecture: {rec['repo1']['architecture']} + {rec['repo2']['architecture']}")
        print()
    
    # Save results
    output_path = Path("data/architecture_repo_analysis.json")
    analyzer.save_analysis(output_path)
    
    print("=" * 70)
    print("✅ ANALYSIS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()

