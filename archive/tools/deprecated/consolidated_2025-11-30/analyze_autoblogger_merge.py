#!/usr/bin/env python3
"""
Auto_Blogger Merge Analysis Tool
================================

Automated analysis of merged content from content and FreeWork repos.
Extracts patterns and identifies integration opportunities.

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-11-26
"""

import subprocess
import json
from pathlib import Path
from typing import Dict, List, Set, Any
import sys

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

AUTO_BLOGGER_PATH = project_root / "temp_repos" / "Auto_Blogger"


def run_git_command(cmd: List[str], cwd: Path) -> str:
    """Run git command and return output."""
    try:
        result = subprocess.run(
            ["git"] + cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Git command failed: {' '.join(cmd)}")
        print(f"Error: {e.stderr}")
        return ""


def get_merged_files(branch: str) -> List[str]:
    """Get list of files merged from a branch."""
    output = run_git_command(
        ["diff", "--name-only", "main", branch],
        AUTO_BLOGGER_PATH
    )
    return [f for f in output.split("\n") if f.strip()]


def analyze_file_patterns(files: List[str]) -> Dict[str, Any]:
    """Analyze file patterns to identify extractable logic."""
    patterns = {
        "content_processing": [],
        "api_integration": [],
        "testing": [],
        "error_handling": [],
        "utilities": [],
        "documentation": [],
        "config": []
    }
    
    for file in files:
        file_lower = file.lower()
        if any(x in file_lower for x in ["content", "blog", "template", "format"]):
            patterns["content_processing"].append(file)
        elif any(x in file_lower for x in ["api", "client", "request", "http"]):
            patterns["api_integration"].append(file)
        elif any(x in file_lower for x in ["test", "spec"]):
            patterns["testing"].append(file)
        elif any(x in file_lower for x in ["error", "exception", "handler"]):
            patterns["error_handling"].append(file)
        elif any(x in file_lower for x in ["util", "helper", "common"]):
            patterns["utilities"].append(file)
        elif any(x in file_lower for x in ["readme", "doc", ".md"]):
            patterns["documentation"].append(file)
        elif any(x in file_lower for x in ["config", "settings", ".ini", ".yaml", ".json"]):
            patterns["config"].append(file)
    
    return patterns


def check_for_duplicates(content_files: List[str], freework_files: List[str]) -> Dict[str, Any]:
    """Check for duplicate files between merges."""
    content_set = set(content_files)
    freework_set = set(freework_files)
    
    duplicates = {
        "exact_duplicates": list(content_set & freework_set),
        "content_only": list(content_set - freework_set),
        "freework_only": list(freework_set - content_set),
        "total_content": len(content_files),
        "total_freework": len(freework_files),
        "duplicate_count": len(content_set & freework_set)
    }
    
    return duplicates


def check_venv_files() -> List[str]:
    """Check for virtual environment files."""
    venv_patterns = [
        "**/venv/**",
        "**/env/**",
        "**/.venv/**",
        "**/virtualenv/**",
        "**/lib/python*/site-packages/**"
    ]
    
    venv_files = []
    for pattern in venv_patterns:
        for path in AUTO_BLOGGER_PATH.rglob(pattern.replace("**/", "")):
            if path.is_file():
                venv_files.append(str(path.relative_to(AUTO_BLOGGER_PATH)))
    
    return venv_files


def main():
    """Main analysis function."""
    print("=" * 70)
    print("Auto_Blogger Merge Analysis - Automated")
    print("=" * 70)
    
    if not AUTO_BLOGGER_PATH.exists():
        print(f"❌ Auto_Blogger not found at {AUTO_BLOGGER_PATH}")
        return 1
    
    print(f"\n📁 Analyzing: {AUTO_BLOGGER_PATH}")
    
    # Get merged files
    print("\n📊 Analyzing merged files...")
    content_files = get_merged_files("origin/merge-content-20251125")
    freework_files = get_merged_files("origin/merge-FreeWork-20251125")
    
    print(f"✅ Content merge: {len(content_files)} files")
    print(f"✅ FreeWork merge: {len(freework_files)} files")
    
    # Check for duplicates
    print("\n🔍 Checking for duplicates...")
    duplicates = check_for_duplicates(content_files, freework_files)
    print(f"   Duplicate files: {duplicates['duplicate_count']}")
    if duplicates['exact_duplicates']:
        print(f"   ⚠️ Found duplicates: {', '.join(duplicates['exact_duplicates'][:5])}")
    
    # Check for venv files
    print("\n🔍 Checking for venv files...")
    venv_files = check_venv_files()
    if venv_files:
        print(f"   ⚠️ Found {len(venv_files)} venv files (should be removed)")
    else:
        print("   ✅ No venv files found")
    
    # Analyze patterns
    print("\n📋 Analyzing file patterns...")
    content_patterns = analyze_file_patterns(content_files)
    freework_patterns = analyze_file_patterns(freework_files)
    
    print("\n📦 Content Repo Patterns:")
    for category, files in content_patterns.items():
        if files:
            print(f"   {category}: {len(files)} files")
            for f in files[:3]:
                print(f"      - {f}")
    
    print("\n📦 FreeWork Repo Patterns:")
    for category, files in freework_patterns.items():
        if files:
            print(f"   {category}: {len(files)} files")
            for f in files[:3]:
                print(f"      - {f}")
    
    # Save analysis report
    report = {
        "content_files": content_files,
        "freework_files": freework_files,
        "duplicates": duplicates,
        "venv_files": venv_files,
        "content_patterns": {k: v for k, v in content_patterns.items() if v},
        "freework_patterns": {k: v for k, v in freework_patterns.items() if v}
    }
    
    report_path = project_root / "agent_workspaces" / "Agent-1" / "AUTO_BLOGGER_MERGE_ANALYSIS.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n✅ Analysis saved to: {report_path}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

