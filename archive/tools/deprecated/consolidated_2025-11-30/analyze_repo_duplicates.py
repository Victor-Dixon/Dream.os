#!/usr/bin/env python3
"""
General Repository Duplicate File Analyzer - Agent-3
====================================================

A general-purpose tool for analyzing duplicate files in any repository.
Based on Agent-2's DreamVault analysis tool, enhanced for general use.

Usage:
    python tools/analyze_repo_duplicates.py --repo <owner>/<repo>
    python tools/analyze_repo_duplicates.py --repo <owner>/<repo> --check-venv
"""

import os
import sys
import argparse
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
import hashlib

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

try:
    from dotenv import load_dotenv
    env_path = Path('.env')
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass


def get_github_token() -> Optional[str]:
    """Get GitHub token from environment or .env file."""
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if token:
        return token
    
    env_file = Path(".env")
    if env_file.exists():
        try:
            with open(env_file, "r") as f:
                for line in f:
                    if line.startswith("GITHUB_TOKEN="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
        except Exception:
            pass
    return None


def clone_repo(repo_path: str, temp_dir: Path) -> Optional[Path]:
    """Clone repository to temporary directory."""
    token = get_github_token()
    if not token:
        print("⚠️  WARNING: No GitHub token found. Using public clone.")
        url = f"https://github.com/{repo_path}.git"
    else:
        url = f"https://{token}@github.com/{repo_path}.git"
    
    repo_dir = temp_dir / repo_path.split("/")[-1]
    
    try:
        print(f"📥 Cloning {repo_path}...")
        subprocess.run(
            ["git", "clone", "--depth", "1", url, str(repo_dir)],
            check=True,
            capture_output=True
        )
        return repo_dir
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to clone repository: {e}")
        return None


def calculate_file_hash(file_path: Path) -> Optional[str]:
    """Calculate SHA256 hash of file."""
    try:
        with open(file_path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception:
        return None


def find_duplicate_files(repo_dir: Path, exclude_patterns: List[str] = None) -> Dict[str, List[Path]]:
    """Find duplicate files by name and content hash."""
    if exclude_patterns is None:
        exclude_patterns = [
            ".git",
            "__pycache__",
            ".pyc",
            ".pyo",
            ".pyd",
            ".egg-info",
            "node_modules",
            ".venv",
            "venv",
            "site-packages",
        ]
    
    duplicates_by_name = defaultdict(list)
    duplicates_by_hash = defaultdict(list)
    
    print(f"🔍 Scanning {repo_dir} for duplicate files...")
    
    for root, dirs, files in os.walk(repo_dir):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if not any(pattern in d for pattern in exclude_patterns)]
        
        for file in files:
            file_path = Path(root) / file
            
            # Skip excluded files
            if any(pattern in str(file_path) for pattern in exclude_patterns):
                continue
            
            # Track by name
            duplicates_by_name[file].append(file_path)
            
            # Track by hash
            file_hash = calculate_file_hash(file_path)
            if file_hash:
                duplicates_by_hash[file_hash].append(file_path)
    
    # Find actual duplicates (files with same name in different locations)
    name_duplicates = {
        name: paths for name, paths in duplicates_by_name.items()
        if len(paths) > 1
    }
    
    # Find content duplicates (files with same hash but different names)
    hash_duplicates = {
        file_hash: paths for file_hash, paths in duplicates_by_hash.items()
        if len(paths) > 1
    }
    
    return {
        "by_name": name_duplicates,
        "by_hash": hash_duplicates,
    }


def check_venv_files(repo_dir: Path) -> List[Path]:
    """Check for virtual environment files that shouldn't be in repo."""
    venv_patterns = [
        "venv/",
        ".venv/",
        "site-packages/",
        "__pycache__/",
        ".pyc",
        ".pyo",
        ".pyd",
        "*.egg-info/",
    ]
    
    venv_files = []
    
    for root, dirs, files in os.walk(repo_dir):
        for pattern in venv_patterns:
            if pattern in str(Path(root)):
                venv_files.append(Path(root))
                break
    
    return venv_files


def generate_report(duplicates: Dict, venv_files: List[Path], output_file: Path, repo_dir: Path):
    """Generate analysis report."""
    with open(output_file, "w") as f:
        f.write("# Repository Duplicate File Analysis Report\n\n")
        f.write(f"Generated: {Path(__file__).name}\n\n")
        
        # Name duplicates
        name_dups = duplicates["by_name"]
        f.write(f"## Duplicate Files by Name: {len(name_dups)}\n\n")
        for name, paths in sorted(name_dups.items(), key=lambda x: len(x[1]), reverse=True):
            f.write(f"### {name} ({len(paths)} locations)\n")
            for path in paths:
                f.write(f"- {path.relative_to(repo_dir)}\n")
            f.write("\n")
        
        # Content duplicates
        hash_dups = duplicates["by_hash"]
        f.write(f"## Duplicate Files by Content Hash: {len(hash_dups)}\n\n")
        for file_hash, paths in sorted(hash_dups.items(), key=lambda x: len(x[1]), reverse=True):
            if len(paths) > 1:
                f.write(f"### Hash: {file_hash[:16]}... ({len(paths)} files)\n")
                for path in paths:
                    f.write(f"- {path.relative_to(repo_dir)}\n")
                f.write("\n")
        
        # Venv files
        if venv_files:
            f.write(f"## Virtual Environment Files Found: {len(venv_files)}\n\n")
            f.write("⚠️  WARNING: These files should NOT be in the repository!\n\n")
            for venv_path in venv_files:
                f.write(f"- {venv_path.relative_to(repo_dir)}\n")
            f.write("\n")
        
        # Summary
        f.write("## Summary\n\n")
        f.write(f"- Duplicate file names: {len(name_dups)}\n")
        f.write(f"- Duplicate content hashes: {len(hash_dups)}\n")
        f.write(f"- Virtual environment files: {len(venv_files)}\n")


def main():
    parser = argparse.ArgumentParser(description="Analyze duplicate files in a repository")
    parser.add_argument("--repo", required=True, help="Repository path (owner/repo)")
    parser.add_argument("--check-venv", action="store_true", help="Check for virtual environment files")
    parser.add_argument("--output", help="Output file for report")
    args = parser.parse_args()
    
    temp_dir = Path(tempfile.mkdtemp())
    repo_dir = None
    
    try:
        # Clone repository
        repo_dir = clone_repo(args.repo, temp_dir)
        if not repo_dir:
            return 1
        
        # Find duplicates
        duplicates = find_duplicate_files(repo_dir)
        
        # Check for venv files
        venv_files = []
        if args.check_venv:
            venv_files = check_venv_files(repo_dir)
        
        # Generate report
        output_file = Path(args.output) if args.output else Path(f"duplicate_analysis_{args.repo.replace('/', '_')}.md")
        generate_report(duplicates, venv_files, output_file, repo_dir)
        
        # Print summary
        print(f"\n✅ Analysis complete!")
        print(f"📊 Duplicate file names: {len(duplicates['by_name'])}")
        print(f"📊 Duplicate content hashes: {len(duplicates['by_hash'])}")
        if venv_files:
            print(f"⚠️  Virtual environment files: {len(venv_files)}")
        print(f"📄 Report saved to: {output_file}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    finally:
        # Cleanup
        if repo_dir and repo_dir.exists():
            shutil.rmtree(repo_dir, ignore_errors=True)
        if temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

