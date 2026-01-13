#!/usr/bin/env python3
"""
Mass Duplicate Cleanup - Phase 3A
=================================

Systematically eliminate blocking duplicates in safe batches.

SAFETY FIRST:
- Only delete exact duplicates
- Never delete last copy of any file
- Preserve canonical versions
- Test after each batch
"""

import sys
import os
import hashlib
from pathlib import Path
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass

@dataclass
class DuplicateGroup:
    """Represents a group of duplicate files."""
    hash_value: str
    files: List[Path]
    size_bytes: int

    @property
    def count(self) -> int:
        return len(self.files)

    def get_canonical_file(self) -> Path:
        """Get the canonical file to keep (usually the one in main codebase)."""
        # Prefer files in main src/ directories
        src_files = [f for f in self.files if "src/" in str(f)]
        if src_files:
            return min(src_files, key=lambda x: str(x))  # Alphabetical, deterministic

        # Then prefer files not in temp/ or agent_workspaces/
        main_files = [f for f in self.files if not any(part in ["temp", "temp_repos", "agent_workspaces"] for part in f.parts)]
        if main_files:
            return min(main_files, key=lambda x: str(x))

        # Otherwise, keep the lexicographically first one
        return min(self.files, key=lambda x: str(x))

    def get_files_to_delete(self) -> List[Path]:
        """Get files that can be safely deleted."""
        canonical = self.get_canonical_file()
        return [f for f in self.files if f != canonical]

class MassDuplicateCleaner:
    """Safe mass duplicate file cleaner."""

    def __init__(self):
        self.duplicates: List[DuplicateGroup] = []
        self.deleted_files: List[Tuple[Path, str]] = []  # (path, hash)
        self.errors: List[str] = []

    def scan_duplicates(self) -> None:
        """Scan for all duplicates in the repository."""
        print("🔍 Scanning for duplicates...")
        hashes: Dict[str, List[Path]] = {}

        # Directories to scan (avoid temp repos for safety)
        scan_dirs = [
            Path("src"),
            Path("mcp_servers"),
            Path("scripts"),
            Path("tools"),
            Path("systems"),
            Path("agent_workspaces"),  # Include but be careful
            Path("repo_consolidation_groups"),  # Include but be careful
            Path("swarm_brain/shared_learnings"),  # Include stable content
        ]

        total_files = 0
        for scan_dir in scan_dirs:
            if not scan_dir.exists():
                continue

            for file_path in scan_dir.rglob("*"):
                if not file_path.is_file():
                    continue

                # Skip certain files
                if file_path.suffix in [".pyc", ".log"] or file_path.name.startswith("."):
                    continue

                # Skip directories we want to avoid
                skip_parts = [".git", ".venv", "__pycache__", ".pytest_cache", "node_modules",
                             "temp_repos", "logs"]  # Skip temp_repos entirely for safety
                if any(part in skip_parts for part in file_path.parts):
                    continue

                try:
                    with open(file_path, "rb") as f:
                        file_hash = hashlib.sha256(f.read()).hexdigest()

                    if file_hash not in hashes:
                        hashes[file_hash] = []
                    hashes[file_hash].append(file_path)

                    total_files += 1
                    if total_files % 1000 == 0:
                        print(f"  Scanned {total_files} files...")

                except Exception as e:
                    print(f"  Warning: Could not hash {file_path}: {e}")
                    continue

        # Convert to DuplicateGroup objects
        for file_hash, files in hashes.items():
            if len(files) > 1:
                # Get size from first file
                try:
                    size = files[0].stat().st_size
                except OSError:
                    size = 0

                self.duplicates.append(DuplicateGroup(
                    hash_value=file_hash,
                    files=files,
                    size_bytes=size
                ))

        # Sort by file count (most problematic first)
        self.duplicates.sort(key=lambda x: x.count, reverse=True)

        print(f"✅ Found {len(self.duplicates)} duplicate groups")

    def categorize_duplicates(self) -> Dict[str, List[DuplicateGroup]]:
        """Categorize duplicates for safe batch processing."""
        categories = {
            "safe_agent_workspace": [],  # Agent workspace archives (safe to clean)
            "safe_repo_consolidation": [],  # Repo consolidation reports (safe to clean)
            "safe_devlogs": [],  # Development logs (safe to clean)
            "caution_system_duplicates": [],  # System code duplicates (need review)
            "danger_core_duplicates": [],  # Core functionality (do not touch)
        }

        for dup in self.duplicates:
            files_str = [str(f) for f in dup.files]

            # Agent workspace archives - very safe to clean
            if all("agent_workspaces" in fs and ("archive" in fs or "inbox" in fs) for fs in files_str):
                categories["safe_agent_workspace"].append(dup)
                continue

            # Repo consolidation reports - safe to clean
            if all("repo_consolidation_groups" in fs for fs in files_str):
                categories["safe_repo_consolidation"].append(dup)
                continue

            # Devlogs - safe to clean
            if all("devlogs" in fs or "swarm_brain/devlogs" in fs for fs in files_str):
                categories["safe_devlogs"].append(dup)
                continue

            # System duplicates - need caution
            if any("systems/" in fs for fs in files_str):
                categories["caution_system_duplicates"].append(dup)
                continue

            # Core src/ duplicates - danger zone
            if any("src/" in fs for fs in files_str):
                categories["danger_core_duplicates"].append(dup)
                continue

            # Default to caution
            categories["caution_system_duplicates"].append(dup)

        return categories

    def execute_batch_cleanup(self, batch_name: str, duplicates: List[DuplicateGroup],
                            dry_run: bool = True) -> Tuple[int, int]:
        """Execute cleanup for a batch of duplicates."""
        print(f"\n{'🔍 DRY RUN' if dry_run else '🗑️ CLEANUP'}: {batch_name}")
        print(f"Target: {len(duplicates)} duplicate groups")

        total_files_to_delete = 0
        total_space_saved = 0

        for i, dup in enumerate(duplicates[:10], 1):  # Limit to first 10 for safety
            canonical = dup.get_canonical_file()
            to_delete = dup.get_files_to_delete()

            print(f"  Group {i}: {dup.count} files ({dup.size_bytes} bytes each)")
            print(f"    KEEP: {canonical}")
            for file in to_delete:
                print(f"    DELETE: {file}")
                total_files_to_delete += 1
                total_space_saved += dup.size_bytes

                if not dry_run:
                    try:
                        file.unlink()
                        self.deleted_files.append((file, dup.hash_value))
                        print(f"    ✅ Deleted: {file}")
                    except Exception as e:
                        error_msg = f"Failed to delete {file}: {e}"
                        self.errors.append(error_msg)
                        print(f"    ❌ {error_msg}")

        if dry_run:
            print(f"\n📊 DRY RUN SUMMARY:")
            print(f"  Would delete: {total_files_to_delete} files")
            print(f"  Space savings: {total_space_saved:,} bytes ({total_space_saved//1024:,} KB)")
            print(f"  Remaining groups: {len(duplicates) - 10} (showing first 10 only)")
        else:
            print(f"\n📊 CLEANUP SUMMARY:")
            print(f"  Deleted: {len(self.deleted_files)} files")
            print(f"  Errors: {len(self.errors)}")
            if self.errors:
                print("  Error details:")
                for error in self.errors[:5]:
                    print(f"    - {error}")

        return total_files_to_delete, total_space_saved

    def run_safety_checks(self) -> bool:
        """Run safety checks before cleanup."""
        print("🛡️ Running safety checks...")

        issues = []

        # Check that we have git repository
        if not Path(".git").exists():
            issues.append("Not a git repository - cannot safely delete files")

        # Check that we're not in a detached HEAD state
        try:
            import subprocess
            result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                                  capture_output=True, text=True)
            if result.returncode != 0 or result.stdout.strip() == "HEAD":
                issues.append("Git repository is in detached HEAD state")
        except Exception:
            issues.append("Cannot verify git repository state")

        # Check for uncommitted changes
        try:
            result = subprocess.run(["git", "status", "--porcelain"],
                                  capture_output=True, text=True)
            if result.stdout.strip():
                issues.append("Repository has uncommitted changes")
        except Exception:
            issues.append("Cannot check git status")

        if issues:
            print("❌ SAFETY CHECKS FAILED:")
            for issue in issues:
                print(f"  - {issue}")
            return False

        print("✅ All safety checks passed")
        return True

def main():
    """Main cleanup function."""
    import argparse

    parser = argparse.ArgumentParser(description="Mass Duplicate Cleanup - Phase 3A")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be deleted")
    parser.add_argument("--batch", choices=["agent_workspace", "repo_consolidation", "devlogs", "system"],
                       help="Specific batch to clean")
    parser.add_argument("--force", action="store_true", help="Skip safety checks (dangerous)")

    args = parser.parse_args()

    cleaner = MassDuplicateCleaner()

    # Safety checks
    if not args.force and not cleaner.run_safety_checks():
        print("\n💡 To bypass safety checks, use --force (not recommended)")
        return 1

    # Scan for duplicates
    cleaner.scan_duplicates()

    # Categorize
    categories = cleaner.categorize_duplicates()

    print("\n📊 Duplicate Categories:")
    for cat_name, cat_dups in categories.items():
        if cat_dups:
            print(f"  {cat_name}: {len(cat_dups)} groups")

    # Execute cleanup based on batch or dry run
    if args.batch:
        batch_map = {
            "agent_workspace": "safe_agent_workspace",
            "repo_consolidation": "safe_repo_consolidation",
            "devlogs": "safe_devlogs",
            "system": "caution_system_duplicates"
        }

        if args.batch in batch_map:
            batch_name = batch_map[args.batch]
            duplicates = categories.get(batch_name, [])

            if duplicates:
                cleaner.execute_batch_cleanup(
                    f"{args.batch.title()} Batch",
                    duplicates,
                    dry_run=args.dry_run
                )
            else:
                print(f"❌ No duplicates found in {args.batch} category")
        else:
            print(f"❌ Unknown batch: {args.batch}")
            return 1

    elif args.dry_run:
        # Show all categories
        for cat_name, cat_dups in categories.items():
            if cat_dups and "danger" not in cat_name:  # Skip danger zone
                print(f"\n🔍 {cat_name.replace('_', ' ').title()}:")
                cleaner.execute_batch_cleanup(
                    cat_name.replace('_', ' ').title(),
                    cat_dups,
                    dry_run=True
                )

    else:
        print("\n💡 Use --dry-run to see what would be cleaned")
        print("   Use --batch <type> to clean specific category")
        print("   Available batches: agent_workspace, repo_consolidation, devlogs, system")

    return 0

if __name__ == "__main__":
    sys.exit(main())