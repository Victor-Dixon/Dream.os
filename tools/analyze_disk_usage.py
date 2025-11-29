#!/usr/bin/env python3
"""
Disk Usage Analysis Tool - Agent-1
===================================

Analyzes disk usage and identifies cleanup opportunities.

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-01-27
"""

import os
import shutil
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).parent.parent


def get_disk_usage(path: Path) -> dict:
    """Get disk usage for a path."""
    try:
        usage = shutil.disk_usage(path)
        return {
            "total": usage.total,
            "used": usage.used,
            "free": usage.free,
            "percent_used": (usage.used / usage.total) * 100
        }
    except Exception:
        return None


def analyze_directory_size(directory: Path, max_depth: int = 3) -> list:
    """Analyze directory sizes."""
    sizes = []
    
    def get_size(path: Path) -> int:
        """Get size of path."""
        try:
            if path.is_file():
                return path.stat().st_size
            elif path.is_dir():
                total = 0
                try:
                    for item in path.iterdir():
                        total += get_size(item)
                except (PermissionError, OSError):
                    pass
                return total
        except (PermissionError, OSError):
            pass
        return 0
    
    def scan_dir(path: Path, depth: int = 0):
        """Scan directory recursively."""
        if depth > max_depth:
            return
        
        try:
            size = get_size(path)
            if size > 0:
                sizes.append({
                    "path": str(path.relative_to(PROJECT_ROOT)),
                    "size": size,
                    "size_mb": size / (1024 ** 2),
                    "size_gb": size / (1024 ** 3),
                    "depth": depth
                })
            
            if path.is_dir() and depth < max_depth:
                try:
                    for item in path.iterdir():
                        scan_dir(item, depth + 1)
                except (PermissionError, OSError):
                    pass
        except (PermissionError, OSError):
            pass
    
    scan_dir(directory)
    return sorted(sizes, key=lambda x: x["size"], reverse=True)


def analyze_project_directories() -> dict:
    """Analyze key project directories."""
    key_dirs = [
        "consolidation_backups",
        "consolidation_logs",
        "temp_repos",
        "agent_workspaces",
        "node_modules",
        ".git",
        "__pycache__",
        "venv",
        ".venv"
    ]
    
    results = {}
    for dir_name in key_dirs:
        dir_path = PROJECT_ROOT / dir_name
        if dir_path.exists():
            size = 0
            count = 0
            try:
                for item in dir_path.rglob("*"):
                    if item.is_file():
                        try:
                            size += item.stat().st_size
                            count += 1
                        except (PermissionError, OSError):
                            pass
            except (PermissionError, OSError):
                pass
            
            results[dir_name] = {
                "size": size,
                "size_mb": size / (1024 ** 2),
                "size_gb": size / (1024 ** 3),
                "file_count": count
            }
    
    return results


def main():
    """Main analysis function."""
    print("=" * 60)
    print("💾 DISK USAGE ANALYSIS")
    print("=" * 60)
    print()
    
    # Check disk usage for C: and D: drives
    print("📊 Drive Space Analysis:")
    print("-" * 60)
    for drive in ["C:\\", "D:\\"]:
        usage = get_disk_usage(drive)
        if usage:
            print(f"{drive}")
            print(f"  Total: {usage['total'] / (1024**3):.2f} GB")
            print(f"  Used:  {usage['used'] / (1024**3):.2f} GB ({usage['percent_used']:.1f}%)")
            print(f"  Free:  {usage['free'] / (1024**3):.2f} GB")
            if usage['percent_used'] > 90:
                print(f"  ⚠️  WARNING: Drive is {usage['percent_used']:.1f}% full!")
            print()
    
    # Analyze project directories
    print("📁 Project Directory Analysis:")
    print("-" * 60)
    project_dirs = analyze_project_directories()
    
    total_size = 0
    for dir_name, data in sorted(project_dirs.items(), 
                                  key=lambda x: x[1]["size"], 
                                  reverse=True):
        if data["size"] > 0:
            print(f"{dir_name}:")
            print(f"  Size: {data['size_gb']:.2f} GB ({data['size_mb']:.2f} MB)")
            print(f"  Files: {data['file_count']:,}")
            total_size += data["size"]
            print()
    
    print(f"Total analyzed: {total_size / (1024**3):.2f} GB")
    print()
    
    # Top 20 largest directories
    print("🔍 Top 20 Largest Directories:")
    print("-" * 60)
    top_dirs = analyze_directory_size(PROJECT_ROOT, max_depth=3)
    for i, item in enumerate(top_dirs[:20], 1):
        indent = "  " * item["depth"]
        print(f"{i:2d}. {indent}{item['path']}")
        print(f"    {item['size_gb']:.2f} GB ({item['size_mb']:.2f} MB)")
    
    print()
    print("=" * 60)
    print("✅ Analysis Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()

