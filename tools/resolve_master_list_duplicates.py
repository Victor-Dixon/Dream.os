#!/usr/bin/env python3
"""
Resolve Master List Duplicates
================================

Resolves duplicate repo names in the master list by keeping the first
occurrence (lower num) and removing duplicates.

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-11-27
Priority: HIGH
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Set
from collections import defaultdict

# Project root
PROJECT_ROOT = Path(__file__).parent.parent
MASTER_LIST_PATH = PROJECT_ROOT / "data" / "github_75_repos_master_list.json"


def find_duplicates(repos: List[Dict]) -> List[Tuple[int, int]]:
    """Find duplicate repo names (case-insensitive)"""
    name_to_nums = defaultdict(list)
    
    for repo in repos:
        name = repo.get("name", "").lower()
        num = repo.get("num")
        name_to_nums[name].append(num)
    
    duplicates = []
    for name, nums in name_to_nums.items():
        if len(nums) > 1:
            # Sort by num to keep first occurrence
            nums.sort()
            for i in range(1, len(nums)):
                duplicates.append((nums[0], nums[i]))
    
    return duplicates


def resolve_duplicates(repos: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
    """
    Resolve duplicates by keeping first occurrence (lower num).
    Returns: (kept_repos, removed_repos)
    """
    # Find duplicates
    duplicates = find_duplicates(repos)
    duplicate_nums = set()
    for _, dup_num in duplicates:
        duplicate_nums.add(dup_num)
    
    # Separate kept and removed repos
    kept_repos = []
    removed_repos = []
    
    for repo in repos:
        num = repo.get("num")
        if num in duplicate_nums:
            removed_repos.append(repo)
        else:
            kept_repos.append(repo)
    
    return kept_repos, removed_repos


def update_stats(repos: List[Dict]) -> Dict:
    """Update stats after duplicate removal"""
    analyzed = sum(1 for r in repos if r.get("analyzed", False))
    goldmines = sum(1 for r in repos if r.get("goldmine", False))
    total = len(repos)
    pending = total - analyzed
    
    # Count by agent
    agent_counts = defaultdict(lambda: {"assigned": 0, "completed": 0})
    for repo in repos:
        agent = repo.get("agent", "Unknown")
        agent_counts[agent]["assigned"] += 1
        if repo.get("analyzed", False):
            agent_counts[agent]["completed"] += 1
    
    return {
        "total_repos": total,
        "analyzed": analyzed,
        "pending": pending,
        "goldmines": goldmines,
        "completion_percent": round((analyzed / total * 100) if total > 0 else 0, 1),
        "agents": dict(agent_counts)
    }


def main():
    """Main execution"""
    print("🔍 Resolving master list duplicates...")
    
    # Load master list
    try:
        with open(MASTER_LIST_PATH, 'r', encoding='utf-8') as f:
            master_list = json.load(f)
    except FileNotFoundError:
        print(f"❌ Master list not found: {MASTER_LIST_PATH}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing master list: {e}")
        sys.exit(1)
    
    repos = master_list.get("repos", [])
    original_count = len(repos)
    
    # Find duplicates
    duplicates = find_duplicates(repos)
    print(f"📊 Found {len(duplicates)} duplicate pairs:")
    for first_num, dup_num in duplicates:
        first_repo = next(r for r in repos if r.get("num") == first_num)
        dup_repo = next(r for r in repos if r.get("num") == dup_num)
        print(f"  - ({first_num}, {dup_num}): '{first_repo.get('name')}' vs '{dup_repo.get('name')}'")
    
    # Resolve duplicates
    kept_repos, removed_repos = resolve_duplicates(repos)
    
    print(f"\n✅ Resolution:")
    print(f"  - Keeping: {len(kept_repos)} repos")
    print(f"  - Removing: {len(removed_repos)} duplicate repos")
    
    # Show removed repos
    print(f"\n🗑️  Removed duplicates:")
    for repo in removed_repos:
        print(f"  - #{repo.get('num')}: {repo.get('name')} (agent: {repo.get('agent')})")
    
    # Update stats
    stats = update_stats(kept_repos)
    
    # Create updated master list
    updated_master_list = {
        "repos": kept_repos,
        "stats": stats
    }
    
    # Backup original
    backup_path = MASTER_LIST_PATH.with_suffix('.json.backup')
    print(f"\n💾 Creating backup: {backup_path}")
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(master_list, f, indent=2, ensure_ascii=False)
    
    # Write updated list
    print(f"✏️  Writing updated master list: {MASTER_LIST_PATH}")
    with open(MASTER_LIST_PATH, 'w', encoding='utf-8') as f:
        json.dump(updated_master_list, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Master list updated:")
    print(f"  - Original: {original_count} repos")
    print(f"  - Updated: {len(kept_repos)} repos")
    print(f"  - Removed: {len(removed_repos)} duplicates")
    print(f"  - Stats: {stats['analyzed']}/{stats['total_repos']} analyzed ({stats['completion_percent']}%)")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

