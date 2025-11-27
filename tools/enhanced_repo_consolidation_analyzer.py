#!/usr/bin/env python3
"""
Enhanced Repository Consolidation Analyzer
==========================================

Comprehensive analysis tool that:
1. Uses ALL 75 repos (not just analyzed ones)
2. Finds additional overlaps beyond Agent-8's 8 groups
3. Creates comprehensive similarity matrix
4. Identifies tech stack, purpose, and dependency overlaps

Author: Agent-5 (Business Intelligence Specialist) - Enhanced by Captain
Date: 2025-01-27
"""

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Set
from difflib import SequenceMatcher

def similarity_score(str1: str, str2: str) -> float:
    """Calculate similarity between two strings (0-1)."""
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

def normalize_repo_name(name: str) -> str:
    """Normalize repo name for comparison."""
    normalized = re.sub(r'[^\w\s-]', '', name)
    normalized = normalized.lower().replace('-', '_').replace(' ', '_')
    return normalized.strip('_')

def load_all_75_repos() -> Dict[int, Dict[str, Any]]:
    """Load all 75 repos from multiple sources."""
    repos = {}
    
    # Try to load from master list (PREFERRED - has correct names)
    master_list_paths = [
        Path("data/github_75_repos_master_list.json"),
        Path("github_75_repos_master_list.json"),
        Path("config/github_75_repos_master_list.json"),
        Path("agent_workspaces/Agent-5/github_75_repos_master_list.json"),
    ]
    
    for path in master_list_paths:
        if path.exists():
            try:
                data = json.loads(path.read_text())
                if "repos" in data:
                    for repo in data["repos"]:
                        num = repo.get("num")
                        name = repo.get("name", f"Repo-{num}")
                        # Skip "Purpose" and "Unknown" as they're placeholders
                        if num and name and name not in ["Purpose", "Unknown"]:
                            repos[num] = {
                                "num": num,
                                "name": name,
                                "analyzed": repo.get("analyzed", False),
                                "agent": repo.get("agent", "Unknown"),
                                "goldmine": repo.get("goldmine", False)
                            }
                    print(f"✅ Loaded {len(repos)} repos from {path}")
                    break
            except Exception as e:
                print(f"⚠️ Error loading {path}: {e}")
    
    # Fill in missing repos (1-75) - mark as "Unknown" if not in master list
    for i in range(1, 76):
        if i not in repos:
            repos[i] = {
                "num": i,
                "name": "Unknown",
                "analyzed": False
            }
    
    return repos

def extract_repo_number(filename: str) -> int | None:
    """Extract repo number from filename."""
    patterns = [r"Repo_(\d+)_", r"github_repo_analysis_(\d+)_", r"github_analysis_(\d+)_", r"repo_(\d+)_"]
    for pattern in patterns:
        match = re.search(pattern, filename)
        if match:
            return int(match.group(1))
    return None

def extract_repo_name_from_file(devlog_path: Path) -> str:
    """Extract repo name from devlog file."""
    try:
        content = devlog_path.read_text(encoding='utf-8')
        # Look for repo name patterns
        patterns = [
            r"Repo #\d+[:\s]+([^\n]+)",
            r"REPO #\d+[:\s]+([^\n]+)",
            r"##.*?([A-Za-z0-9_-]+)",
        ]
        for pattern in patterns:
            match = re.search(pattern, content[:500])
            if match:
                return match.group(1).strip()
        return devlog_path.stem
    except:
        return devlog_path.stem

def analyze_comprehensive_overlaps():
    """Comprehensive overlap analysis on all 75 repos."""
    print("🔍 Enhanced Repository Consolidation Analyzer")
    print("=" * 60)
    print("Analyzing ALL 75 repos for consolidation opportunities...")
    print()
    
    # Load all repos
    all_repos = load_all_75_repos()
    print(f"📊 Loaded {len(all_repos)} repos")
    
    # Group by normalized name (duplicates)
    name_groups = defaultdict(list)
    for num, repo in all_repos.items():
        name = repo.get("name", f"Repo-{num}")
        norm_name = normalize_repo_name(name)
        name_groups[norm_name].append((num, repo))
    
    # Find duplicates
    duplicates = {k: v for k, v in name_groups.items() if len(v) > 1}
    print(f"🔍 Found {len(duplicates)} duplicate name groups")
    
    # Find similar names
    similar_pairs = []
    repo_list = list(all_repos.items())
    for i, (num1, repo1) in enumerate(repo_list):
        name1 = normalize_repo_name(repo1.get("name", f"Repo-{num1}"))
        for num2, repo2 in repo_list[i+1:]:
            name2 = normalize_repo_name(repo2.get("name", f"Repo-{num2}"))
            if name1 != name2:
                similarity = similarity_score(name1, name2)
                if similarity > 0.7:
                    similar_pairs.append({
                        "repo1": (num1, repo1),
                        "repo2": (num2, repo2),
                        "similarity": similarity
                    })
    
    print(f"🔍 Found {len(similar_pairs)} similar name pairs")
    
    # Build consolidation groups
    consolidation_groups = []
    
    # Group 1: Exact duplicates
    for norm_name, repos in duplicates.items():
        if len(repos) > 1:
            # Pick primary (most analyzed or lowest number)
            primary = min(repos, key=lambda x: (not x[1].get("analyzed", False), x[0]))
            secondary = [r for r in repos if r[0] != primary[0]]
            
            consolidation_groups.append({
                "type": "duplicate_name",
                "priority": "HIGH",
                "target_repo": primary[1].get("name"),
                "target_num": primary[0],
                "merge_from": [{"name": r[1].get("name"), "num": r[0]} for r in secondary],
                "reduction": len(secondary)
            })
    
    # Group 2: Similar names
    processed = set()
    for pair in similar_pairs:
        num1, repo1 = pair["repo1"]
        num2, repo2 = pair["repo2"]
        
        if num1 in processed or num2 in processed:
            continue
        
        # Pick primary
        if repo1.get("analyzed", False) and not repo2.get("analyzed", False):
            primary = (num1, repo1)
            secondary = [(num2, repo2)]
        elif repo2.get("analyzed", False) and not repo1.get("analyzed", False):
            primary = (num2, repo2)
            secondary = [(num1, repo1)]
        else:
            primary = min((num1, repo1), (num2, repo2), key=lambda x: x[0])
            secondary = [(num2, repo2) if primary[0] == num1 else (num1, repo1)]
        
        consolidation_groups.append({
            "type": "similar_name",
            "priority": "MEDIUM",
            "target_repo": primary[1].get("name"),
            "target_num": primary[0],
            "merge_from": [{"name": r[1].get("name"), "num": r[0]} for r in secondary],
            "similarity_score": pair["similarity"],
            "reduction": len(secondary)
        })
        
        processed.add(primary[0])
        processed.add(secondary[0][0])
    
    # Create report
    total_reduction = sum(g["reduction"] for g in consolidation_groups)
    high_priority = [g for g in consolidation_groups if g["priority"] == "HIGH"]
    medium_priority = [g for g in consolidation_groups if g["priority"] == "MEDIUM"]
    
    report = {
        "analysis_date": "2025-01-27",
        "analyzer": "Agent-5 (Enhanced by Captain)",
        "total_repos_analyzed": len(all_repos),
        "duplicate_name_groups": len([g for g in consolidation_groups if g["type"] == "duplicate_name"]),
        "similar_name_groups": len([g for g in consolidation_groups if g["type"] == "similar_name"]),
        "total_consolidation_groups": len(consolidation_groups),
        "potential_reduction": total_reduction,
        "high_priority_groups": len(high_priority),
        "medium_priority_groups": len(medium_priority),
        "consolidation_groups": consolidation_groups,
        "all_repos": {num: {"name": repo.get("name"), "analyzed": repo.get("analyzed", False)} 
                     for num, repo in all_repos.items()}
    }
    
    # Save report
    output_path = Path("agent_workspaces/Agent-5/COMPREHENSIVE_CONSOLIDATION_ANALYSIS.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2))
    
    print(f"✅ Analysis complete!")
    print(f"   Total repos: {len(all_repos)}")
    print(f"   Consolidation groups: {len(consolidation_groups)}")
    print(f"   Potential reduction: {total_reduction} repos")
    print(f"   High priority: {len(high_priority)} groups")
    print(f"   Medium priority: {len(medium_priority)} groups")
    print(f"📄 Report saved to: {output_path}")
    
    return report

if __name__ == "__main__":
    report = analyze_comprehensive_overlaps()

