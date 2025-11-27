#!/usr/bin/env python3
"""
Stage 1 Duplicate Analyzer - Agent-5
=====================================

Analyzes duplicate files for Stage 1 integration work.
Categorizes duplicates by priority and generates resolution recommendations.

Usage:
    python tools/stage1_duplicate_analyzer.py [path]
"""

import os
import sys
import hashlib
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple
import json

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


def calculate_file_hash(filepath: Path, block_size=65536) -> str:
    """Calculate SHA256 hash of file."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                hasher.update(block)
        return hasher.hexdigest()
    except Exception:
        return None


def categorize_duplicate(filepath: str) -> str:
    """Categorize duplicate by location and importance."""
    path_lower = filepath.lower()
    
    # Critical - Core modules
    if any(x in path_lower for x in ['src/core/', 'src/services/', 'src/managers/']):
        return "CRITICAL"
    
    # High - Merged repos
    if 'temp_repos' in path_lower or 'merged' in path_lower:
        return "HIGH"
    
    # Medium - Tests and docs
    if any(x in path_lower for x in ['test', 'docs/', '__init__.py']):
        return "MEDIUM"
    
    # Low - Everything else
    return "LOW"


def analyze_duplicates(root_path: str) -> Dict:
    """Analyze duplicates and categorize by priority."""
    root = Path(root_path)
    hash_to_files = defaultdict(list)
    name_to_files = defaultdict(list)
    
    print("Analyzing duplicates...")
    
    for dirpath, _, filenames in os.walk(root):
        # Skip .git and other ignored directories
        if '.git' in dirpath or '__pycache__' in dirpath:
            continue
            
        for filename in filenames:
            filepath = Path(dirpath) / filename
            if filepath.is_file():
                try:
                    file_hash = calculate_file_hash(filepath)
                    if file_hash:
                        rel_path = str(filepath.relative_to(root))
                        hash_to_files[file_hash].append(rel_path)
                        name_to_files[filename].append(rel_path)
                except Exception:
                    pass
    
    # Categorize duplicates
    content_duplicates = {
        h: files for h, files in hash_to_files.items() if len(files) > 1
    }
    name_duplicates = {
        name: files for name, files in name_to_files.items() if len(files) > 1
    }
    
    # Priority analysis
    critical = []
    high = []
    medium = []
    low = []
    
    for files in content_duplicates.values():
        categories = [categorize_duplicate(f) for f in files]
        if "CRITICAL" in categories:
            critical.extend(files)
        elif "HIGH" in categories:
            high.extend(files)
        elif "MEDIUM" in categories:
            medium.extend(files)
        else:
            low.extend(files)
    
    return {
        "content_duplicates": content_duplicates,
        "name_duplicates": name_duplicates,
        "priority_breakdown": {
            "critical": len([f for files in content_duplicates.values() 
                           for f in files if categorize_duplicate(f) == "CRITICAL"]),
            "high": len([f for files in content_duplicates.values() 
                        for f in files if categorize_duplicate(f) == "HIGH"]),
            "medium": len([f for files in content_duplicates.values() 
                          for f in files if categorize_duplicate(f) == "MEDIUM"]),
            "low": len([f for files in content_duplicates.values() 
                       for f in files if categorize_duplicate(f) == "LOW"])
        },
        "statistics": {
            "total_content_groups": len(content_duplicates),
            "total_content_files": sum(len(files) for files in content_duplicates.values()),
            "total_name_groups": len(name_duplicates),
            "total_name_files": sum(len(files) for files in name_duplicates.values())
        }
    }


def generate_report(results: Dict, output_file: str = None):
    """Generate analysis report."""
    print("\n" + "="*70)
    print("STAGE 1 DUPLICATE ANALYSIS REPORT")
    print("="*70)
    
    stats = results["statistics"]
    priority = results["priority_breakdown"]
    
    print(f"\n📊 STATISTICS:")
    print(f"   Content duplicate groups: {stats['total_content_groups']}")
    print(f"   Content duplicate files: {stats['total_content_files']}")
    print(f"   Name duplicate groups: {stats['total_name_groups']}")
    print(f"   Name duplicate files: {stats['total_name_files']}")
    
    print(f"\n🎯 PRIORITY BREAKDOWN:")
    print(f"   CRITICAL: {priority['critical']} files (core modules)")
    print(f"   HIGH: {priority['high']} files (merged repos)")
    print(f"   MEDIUM: {priority['medium']} files (tests/docs)")
    print(f"   LOW: {priority['low']} files (other)")
    
    print(f"\n📋 RECOMMENDATIONS:")
    print(f"   1. Resolve CRITICAL duplicates first (blocking integration)")
    print(f"   2. Use Agent-3's merge_duplicate_file_functionality.py for analysis")
    print(f"   3. Use Agent-2's resolution tools for systematic cleanup")
    print(f"   4. Goal: 0 issues (Agent-3 standard)")
    
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n✅ Report saved to: {output_file}")


def main():
    """Main function."""
    import argparse
    parser = argparse.ArgumentParser(description="Analyze duplicates for Stage 1 integration")
    parser.add_argument("path", nargs='?', default=".", help="Path to analyze")
    parser.add_argument("--output", "-o", help="Output JSON file")
    args = parser.parse_args()
    
    results = analyze_duplicates(args.path)
    generate_report(results, args.output)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

