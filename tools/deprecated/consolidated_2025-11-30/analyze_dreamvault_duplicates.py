#!/usr/bin/env python3
"""
Analyze DreamVault Duplicate Files - Agent-2
===========================================

Analyzes duplicate files in DreamVault repository to identify integration issues.
"""

import os
import sys
import subprocess
import tempfile
import shutil
import time
import stat
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


def get_github_username() -> Optional[str]:
    """Get GitHub username from environment or .env file."""
    username = os.getenv("GITHUB_USERNAME")
    if username:
        return username
    
    env_file = Path(".env")
    if env_file.exists():
        try:
            with open(env_file, "r") as f:
                for line in f:
                    if line.startswith("GITHUB_USERNAME="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
        except Exception:
            pass
    return None


def ensure_dir_removed(dir_path: Path, name: str):
    """Ensure directory is completely removed."""
    if dir_path.exists():
        print(f"🧹 Removing existing {name} directory: {dir_path}")
        try:
            shutil.rmtree(dir_path, ignore_errors=True)
            time.sleep(0.5)
            if dir_path.exists():
                def remove_readonly(func, path, exc):
                    os.chmod(path, stat.S_IWRITE)
                    func(path)
                shutil.rmtree(dir_path, onerror=remove_readonly)
                time.sleep(0.5)
        except Exception as e:
            print(f"⚠️ Cleanup warning for {name}: {e}")


def clone_dreamvault(temp_base: Path, token: str, username: str) -> Optional[Path]:
    """Clone DreamVault repository."""
    owner = "Dadudekc"
    repo = "DreamVault"
    repo_dir = temp_base / repo
    
    try:
        repo_url = f"https://{username}:{token}@github.com/{owner}/{repo}.git"
        print(f"📥 Cloning {repo}...")
        subprocess.run(
            ["git", "clone", repo_url, str(repo_dir)],
            check=True, timeout=300, capture_output=True, text=True
        )
        print(f"✅ Cloned {repo} successfully")
        return repo_dir
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to clone {repo}: {e.stderr}")
        return None
    except Exception as e:
        print(f"❌ Error cloning {repo}: {e}")
        return None


def calculate_file_hash(file_path: Path) -> Optional[str]:
    """Calculate SHA256 hash of a file."""
    try:
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except Exception:
        return None


def find_duplicate_files(repo_dir: Path) -> Dict[str, List[Path]]:
    """Find duplicate files by name and content."""
    duplicates_by_name = defaultdict(list)
    duplicates_by_content = defaultdict(list)
    
    # Find duplicates by name
    print("🔍 Finding duplicate file names...")
    for file_path in repo_dir.rglob("*"):
        if file_path.is_file() and file_path.name not in [".gitignore", ".gitkeep"]:
            # Skip .git directory
            if ".git" in file_path.parts:
                continue
            duplicates_by_name[file_path.name].append(file_path)
    
    # Filter to only actual duplicates (2+ files with same name)
    name_duplicates = {name: paths for name, paths in duplicates_by_name.items() if len(paths) > 1}
    
    # Find duplicates by content (for files with same name)
    print("🔍 Analyzing duplicate file content...")
    for name, paths in name_duplicates.items():
        for file_path in paths:
            file_hash = calculate_file_hash(file_path)
            if file_hash:
                duplicates_by_content[file_hash].append(file_path)
    
    return {
        "by_name": name_duplicates,
        "by_content": duplicates_by_content
    }


def categorize_duplicates(duplicates: Dict) -> Dict:
    """Categorize duplicates by type and source."""
    categories = {
        "python_files": [],
        "config_files": [],
        "documentation": [],
        "data_files": [],
        "other": []
    }
    
    for name, paths in duplicates["by_name"].items():
        file_info = {
            "name": name,
            "paths": [str(p.relative_to(duplicates["repo_dir"])) for p in paths],
            "count": len(paths)
        }
        
        ext = Path(name).suffix.lower()
        if ext == ".py":
            categories["python_files"].append(file_info)
        elif ext in [".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf"]:
            categories["config_files"].append(file_info)
        elif ext in [".md", ".txt", ".rst"]:
            categories["documentation"].append(file_info)
        elif ext in [".csv", ".json", ".xml", ".sql"]:
            categories["data_files"].append(file_info)
        else:
            categories["other"].append(file_info)
    
    return categories


def identify_source_repo(file_path: Path) -> str:
    """Identify which merged repo a file likely came from."""
    path_str = str(file_path).lower()
    
    if "dreambank" in path_str or "portfolio" in path_str or "bank" in path_str:
        return "DreamBank"
    elif "digitaldreamscape" in path_str or "dreamscape" in path_str:
        return "DigitalDreamscape"
    elif "thea" in path_str:
        return "Thea"
    else:
        return "DreamVault (original)"


def print_duplicate_analysis(duplicates: Dict, categories: Dict, repo_dir: Path):
    """Print comprehensive duplicate analysis."""
    print("\n" + "="*60)
    print("📊 DREAMVAULT DUPLICATE FILE ANALYSIS")
    print("="*60)
    
    total_duplicates = sum(len(paths) for paths in duplicates["by_name"].values())
    unique_duplicate_names = len(duplicates["by_name"])
    
    print(f"\n📁 Duplicate Summary:")
    print(f"   Total Duplicate Files: {total_duplicates}")
    print(f"   Unique Duplicate Names: {unique_duplicate_names}")
    
    print(f"\n📋 Duplicates by Category:")
    print(f"   Python Files: {len(categories['python_files'])}")
    print(f"   Config Files: {len(categories['config_files'])}")
    print(f"   Documentation: {len(categories['documentation'])}")
    print(f"   Data Files: {len(categories['data_files'])}")
    print(f"   Other: {len(categories['other'])}")
    
    # Show top duplicates
    print(f"\n🔍 Top 10 Duplicate Files:")
    sorted_dups = sorted(
        categories["python_files"] + categories["config_files"] + categories["documentation"],
        key=lambda x: x["count"],
        reverse=True
    )[:10]
    
    for dup in sorted_dups:
        print(f"   {dup['name']}: {dup['count']} locations")
        for path in dup['paths'][:3]:  # Show first 3 paths
            source = identify_source_repo(repo_dir / path)
            print(f"      - {path} ({source})")
        if len(dup['paths']) > 3:
            print(f"      ... and {len(dup['paths']) - 3} more")
    
    print("\n" + "="*60)


def main():
    """Main entry point."""
    token = get_github_token()
    username = get_github_username()
    
    if not token or not username:
        print("❌ GITHUB_TOKEN or GITHUB_USERNAME not found.")
        return 1
    
    # Create temp directory
    timestamp = int(time.time() * 1000000)
    temp_base = Path(tempfile.mkdtemp(prefix=f"dreamvault_duplicates_{timestamp}_"))
    
    try:
        # Clone repository
        repo_dir = clone_dreamvault(temp_base, token, username)
        if not repo_dir:
            return 1
        
        # Find duplicates
        print("\n🔍 Analyzing duplicate files...")
        duplicates = find_duplicate_files(repo_dir)
        duplicates["repo_dir"] = repo_dir
        
        # Categorize duplicates
        print("🔍 Categorizing duplicates...")
        categories = categorize_duplicates(duplicates)
        
        # Print analysis
        print_duplicate_analysis(duplicates, categories, repo_dir)
        
        # Summary
        print("\n📋 Summary:")
        total_dups = sum(len(paths) for paths in duplicates["by_name"].values())
        print(f"   Total Duplicate Files: {total_dups}")
        print(f"   Unique Duplicate Names: {len(duplicates['by_name'])}")
        print(f"\n   ⚠️ These duplicates need resolution:")
        print(f"      - Determine SSOT versions")
        print(f"      - Merge functionality where appropriate")
        print(f"      - Remove redundant files")
        print(f"      - Update imports/references")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        ensure_dir_removed(temp_base, "temp_repo_clone")


if __name__ == "__main__":
    sys.exit(main())

