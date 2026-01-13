#!/usr/bin/env python3
"""
Check for Duplicate Accomplishments Across Reports
===================================================

Analyzes Agent-2 status.json to find duplicate accomplishments across:
1. achievements section
2. completed_tasks section  
3. current_tasks section

Author: Agent-2
Date: 2025-12-13
"""

import json
import sys
from pathlib import Path
from collections import defaultdict
from difflib import SequenceMatcher


def similarity(a: str, b: str) -> float:
    """Calculate similarity ratio between two strings."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def normalize_text(text: str) -> str:
    """Normalize text for comparison."""
    # Remove common prefixes/suffixes
    text = text.replace("✅", "").replace("⏳", "").replace("🚨", "").strip()
    # Remove artifact references
    if "(artifact:" in text:
        text = text.split("(artifact:")[0].strip()
    return text


def extract_key_phrases(text: str) -> list:
    """Extract key phrases from accomplishment text."""
    text = normalize_text(text)
    # Split by common separators
    phrases = []
    for part in text.split(" - "):
        for subpart in part.split(": "):
            phrases.append(subpart.strip())
    return [p for p in phrases if len(p) > 10]  # Only meaningful phrases


def find_duplicates(agent_status_path: Path):
    """Find duplicate accomplishments across different sections."""
    with open(agent_status_path, 'r', encoding='utf-8') as f:
        status = json.load(f)

    achievements = status.get("achievements", [])
    completed_tasks = status.get("completed_tasks", [])
    current_tasks = status.get("current_tasks", [])

    print("=" * 80)
    print("🔍 DUPLICATE ACCOMPLISHMENTS ANALYSIS")
    print("=" * 80)
    print(f"\n📊 Section Counts:")
    print(f"   Achievements: {len(achievements)}")
    print(f"   Completed Tasks: {len(completed_tasks)}")
    print(f"   Current Tasks: {len(current_tasks)}")
    print()

    # Check for duplicates between achievements and completed_tasks
    print("=" * 80)
    print("1️⃣ ACHIEVEMENTS vs COMPLETED_TASKS")
    print("=" * 80)
    duplicates_ach_comp = []
    for ach in achievements:
        for comp in completed_tasks:
            sim = similarity(normalize_text(ach), normalize_text(comp))
            if sim > 0.7:  # 70% similarity threshold
                duplicates_ach_comp.append({
                    "achievement": ach,
                    "completed_task": comp,
                    "similarity": sim
                })

    if duplicates_ach_comp:
        print(f"⚠️  Found {len(duplicates_ach_comp)} potential duplicates:\n")
        for dup in sorted(duplicates_ach_comp, key=lambda x: x["similarity"], reverse=True):
            print(f"   Similarity: {dup['similarity']:.1%}")
            print(f"   Achievement: {dup['achievement'][:80]}...")
            print(f"   Completed:  {dup['completed_task'][:80]}...")
            print()
    else:
        print("✅ No duplicates found between achievements and completed_tasks\n")

    # Check for duplicates between achievements and current_tasks
    print("=" * 80)
    print("2️⃣ ACHIEVEMENTS vs CURRENT_TASKS")
    print("=" * 80)
    duplicates_ach_curr = []
    for ach in achievements:
        for curr in current_tasks:
            sim = similarity(normalize_text(ach), normalize_text(curr))
            if sim > 0.7:
                duplicates_ach_curr.append({
                    "achievement": ach,
                    "current_task": curr,
                    "similarity": sim
                })

    if duplicates_ach_curr:
        print(f"⚠️  Found {len(duplicates_ach_curr)} potential duplicates:\n")
        for dup in sorted(duplicates_ach_curr, key=lambda x: x["similarity"], reverse=True):
            print(f"   Similarity: {dup['similarity']:.1%}")
            print(f"   Achievement: {dup['achievement'][:80]}...")
            print(f"   Current:     {dup['current_task'][:80]}...")
            print()
    else:
        print("✅ No duplicates found between achievements and current_tasks\n")

    # Check for duplicates between completed_tasks and current_tasks
    print("=" * 80)
    print("3️⃣ COMPLETED_TASKS vs CURRENT_TASKS")
    print("=" * 80)
    duplicates_comp_curr = []
    for comp in completed_tasks:
        for curr in current_tasks:
            sim = similarity(normalize_text(comp), normalize_text(curr))
            if sim > 0.7:
                duplicates_comp_curr.append({
                    "completed_task": comp,
                    "current_task": curr,
                    "similarity": sim
                })

    if duplicates_comp_curr:
        print(f"⚠️  Found {len(duplicates_comp_curr)} potential duplicates:\n")
        for dup in sorted(duplicates_comp_curr, key=lambda x: x["similarity"], reverse=True):
            print(f"   Similarity: {dup['similarity']:.1%}")
            print(f"   Completed:  {dup['completed_task'][:80]}...")
            print(f"   Current:    {dup['current_task'][:80]}...")
            print()
    else:
        print("✅ No duplicates found between completed_tasks and current_tasks\n")

    # Check for duplicates within achievements
    print("=" * 80)
    print("4️⃣ DUPLICATES WITHIN ACHIEVEMENTS")
    print("=" * 80)
    duplicates_within_ach = []
    for i, ach1 in enumerate(achievements):
        for j, ach2 in enumerate(achievements[i+1:], i+1):
            sim = similarity(normalize_text(ach1), normalize_text(ach2))
            if sim > 0.7:
                duplicates_within_ach.append({
                    "achievement1": ach1,
                    "achievement2": ach2,
                    "similarity": sim
                })

    if duplicates_within_ach:
        print(
            f"⚠️  Found {len(duplicates_within_ach)} potential duplicates:\n")
        for dup in sorted(duplicates_within_ach, key=lambda x: x["similarity"], reverse=True):
            print(f"   Similarity: {dup['similarity']:.1%}")
            print(f"   Achievement 1: {dup['achievement1'][:80]}...")
            print(f"   Achievement 2: {dup['achievement2'][:80]}...")
            print()
    else:
        print("✅ No duplicates found within achievements\n")

    # Summary
    print("=" * 80)
    print("📋 SUMMARY")
    print("=" * 80)
    total_duplicates = len(duplicates_ach_comp) + len(duplicates_ach_curr) + \
        len(duplicates_comp_curr) + len(duplicates_within_ach)
    print(f"Total potential duplicates found: {total_duplicates}")
    print(f"  - Achievements ↔ Completed Tasks: {len(duplicates_ach_comp)}")
    print(f"  - Achievements ↔ Current Tasks: {len(duplicates_ach_curr)}")
    print(f"  - Completed Tasks ↔ Current Tasks: {len(duplicates_comp_curr)}")
    print(f"  - Within Achievements: {len(duplicates_within_ach)}")
    print()

    if total_duplicates > 0:
        print("💡 RECOMMENDATION: Review duplicates and consolidate to avoid redundancy.")
    else:
        print("✅ No duplicates detected - all accomplishments are unique!")


if __name__ == "__main__":
    agent_status_path = Path("agent_workspaces/Agent-2/status.json")
    if not agent_status_path.exists():
        print(f"❌ Status file not found: {agent_status_path}")
        sys.exit(1)

    find_duplicates(agent_status_path)
