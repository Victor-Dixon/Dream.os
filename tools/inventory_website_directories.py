#!/usr/bin/env python3
"""
Website Directory Inventory Tool
=================================

Creates detailed inventory of website directories to support safe consolidation.
Identifies what's in root vs. websites/websites/ and what's safe to move.

V2 Compliance: < 300 lines, single responsibility
Author: Agent-7 (Web Development Specialist)
"""

import json
import os
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set

websites_root = Path("D:/websites")


def get_file_inventory(directory: Path, exclude_patterns: List[str] = None) -> Dict:
    """Get inventory of files in a directory."""
    if exclude_patterns is None:
        exclude_patterns = ["__pycache__", ".pyc", ".git", ".pytest_cache"]
    
    inventory = {
        "exists": directory.exists(),
        "files": [],
        "directories": [],
        "total_files": 0,
        "total_size": 0
    }
    
    if not directory.exists():
        return inventory
    
    try:
        for item in directory.iterdir():
            if any(pattern in str(item) for pattern in exclude_patterns):
                continue
            
            if item.is_file():
                size = item.stat().st_size
                inventory["files"].append({
                    "name": item.name,
                    "size": size,
                    "path": str(item.relative_to(websites_root))
                })
                inventory["total_files"] += 1
                inventory["total_size"] += size
            elif item.is_dir():
                inventory["directories"].append(item.name)
    except PermissionError:
        inventory["error"] = "Permission denied"
    
    return inventory


def compare_directories(root_dir: Path, websites_dir: Path) -> Dict:
    """Compare root-level and websites/websites/ directories."""
    root_inv = get_file_inventory(root_dir)
    websites_inv = get_file_inventory(websites_dir)
    
    root_files = {f["name"]: f for f in root_inv["files"]}
    websites_files = {f["name"]: f for f in websites_inv["files"]}
    
    comparison = {
        "root": root_inv,
        "websites": websites_inv,
        "unique_to_root": list(set(root_files.keys()) - set(websites_files.keys())),
        "unique_to_websites": list(set(websites_files.keys()) - set(root_files.keys())),
        "common_files": list(set(root_files.keys()) & set(websites_files.keys())),
        "safe_to_move": []
    }
    
    # Identify safe-to-move files (documentation, static content)
    safe_patterns = [".md", ".yaml", ".yml", ".txt", ".html", ".css"]
    for filename in comparison["unique_to_root"]:
        if any(filename.endswith(ext) for ext in safe_patterns):
            comparison["safe_to_move"].append({
                "file": filename,
                "from": str(root_dir.relative_to(websites_root)),
                "to": f"websites/{root_dir.name}/docs/" if filename.endswith(".md") else f"websites/{root_dir.name}/"
            })
    
    return comparison


def main():
    """Generate inventory for all website directories."""
    sites = [
        "ariajet.site",
        "crosbyultimateevents.com",
        "dadudekc.com",
        "houstonsipqueen.com",
        "prismblossom.online",
        "southwestsecret.com",
        "digitaldreamscape.site",
        "freerideinvestor.com",
        "tradingrobotplug.com",
        "weareswarm.online",
        "weareswarm.site"
    ]
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "websites_root": str(websites_root),
        "sites": {}
    }
    
    print("=" * 60)
    print("Website Directory Inventory")
    print("=" * 60)
    
    for site in sites:
        root_dir = websites_root / site
        websites_dir = websites_root / "websites" / site
        
        if not root_dir.exists() and not websites_dir.exists():
            continue
        
        print(f"\n📁 {site}")
        comparison = compare_directories(root_dir, websites_dir)
        results["sites"][site] = comparison
        
        if comparison["root"]["exists"]:
            print(f"  Root: {comparison['root']['total_files']} files, "
                  f"{len(comparison['root']['directories'])} dirs")
        
        if comparison["websites"]["exists"]:
            print(f"  Websites: {comparison['websites']['total_files']} files, "
                  f"{len(comparison['websites']['directories'])} dirs")
        
        if comparison["unique_to_root"]:
            print(f"  Unique to root: {len(comparison['unique_to_root'])} files")
        
        if comparison["unique_to_websites"]:
            print(f"  Unique to websites: {len(comparison['unique_to_websites'])} files")
        
        if comparison["common_files"]:
            print(f"  ⚠️  Common files (potential duplicates): {len(comparison['common_files'])}")
        
        if comparison["safe_to_move"]:
            print(f"  ✅ Safe to move: {len(comparison['safe_to_move'])} files")
    
    # Save results
    output_file = websites_root / "docs" / "consolidation" / "website_inventory.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Inventory saved to: {output_file}")
    
    # Generate summary
    total_safe = sum(len(s["safe_to_move"]) for s in results["sites"].values())
    print(f"\n📊 Summary: {total_safe} files identified as safe to move")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())


