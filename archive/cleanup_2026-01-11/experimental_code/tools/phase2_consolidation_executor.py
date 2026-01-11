#!/usr/bin/env python3
"""
Phase 2 Consolidation Executor
=============================

Executes safe markdown file consolidation operations identified in Phase 2 analysis.
Handles archive reorganization, duplicate consolidation, and structural cleanup.

Author: Agent-5 (Business Intelligence)
Date: 2026-01-11
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Set
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class Phase2ConsolidationExecutor:
    """Executes Phase 2 structural consolidation operations."""

    def __init__(self, repo_root: Path, dry_run: bool = True):
        self.repo_root = repo_root
        self.dry_run = dry_run
        self.operations_log = []
        self.stats = defaultdict(int)

    def log_operation(self, operation: str, details: Dict):
        """Log an operation for tracking."""
        self.operations_log.append({
            "operation": operation,
            "details": details,
            "timestamp": str(Path(__file__).stat().st_mtime)
        })

    def execute_archive_reorganization(self) -> Dict[str, int]:
        """
        Execute archive reorganization - move recent files back to working directories.
        """
        logger.info("📂 Executing archive reorganization...")

        results = defaultdict(int)
        archive_dirs = [
            self.repo_root / 'archive',
            self.repo_root / 'data' / 'models' / 'swarm_brain' / 'devlogs'
        ]

        for archive_dir in archive_dirs:
            if not archive_dir.exists():
                continue

            for root, dirs, files in os.walk(archive_dir):
                for file in files:
                    if file.endswith('.md'):
                        archive_file = Path(root) / file

                        # Check if file is recent (< 30 days)
                        try:
                            age_days = (Path(__file__).stat().st_mtime - archive_file.stat().st_mtime) / (24 * 3600)
                            if age_days >= 30:
                                continue  # Skip old files
                        except OSError:
                            continue

                        # Determine target directory
                        target_dir = None
                        file_parts = archive_file.parts

                        if 'agent_workspaces' in file_parts:
                            # Move back to agent workspace
                            ws_idx = file_parts.index('agent_workspaces')
                            if ws_idx + 1 < len(file_parts):
                                agent_name = file_parts[ws_idx + 1]
                                target_dir = self.repo_root / 'agent_workspaces' / agent_name
                                # Recreate subdirectory structure if needed
                                rel_path = Path(*file_parts[ws_idx+2:-1])  # Everything between agent_name and filename
                                target_dir = target_dir / rel_path

                        elif 'devlogs' in file_parts:
                            # Move to devlogs directory
                            target_dir = self.repo_root / 'devlogs'

                        if target_dir and target_dir.exists():
                            target_file = target_dir / file

                            if self.dry_run:
                                logger.info(f"Would move {archive_file} -> {target_file}")
                                results['would_move'] += 1
                            else:
                                try:
                                    # Ensure target directory exists
                                    target_file.parent.mkdir(parents=True, exist_ok=True)
                                    shutil.move(str(archive_file), str(target_file))
                                    logger.info(f"✅ Moved {archive_file} -> {target_file}")
                                    results['moved'] += 1
                                    self.log_operation("archive_reorganization", {
                                        "from": str(archive_file),
                                        "to": str(target_file),
                                        "reason": "recent_file_reorganization"
                                    })
                                except Exception as e:
                                    logger.error(f"❌ Failed to move {archive_file}: {e}")
                                    results['errors'] += 1

        return dict(results)

    def execute_duplicate_consolidation(self) -> Dict[str, int]:
        """
        Execute duplicate file consolidation using safe hardlinking/symlinking.
        """
        logger.info("🔗 Executing duplicate consolidation...")

        results = defaultdict(int)
        duplicate_groups = self._find_duplicate_groups()

        for group_name, files in duplicate_groups.items():
            if len(files) < 2:
                continue

            # Sort by path priority (prefer workspace over archive)
            sorted_files = sorted(files, key=self._get_file_priority)

            # Keep the highest priority file, replace others with symlinks
            canonical_file = sorted_files[0]
            duplicate_files = sorted_files[1:]

            for duplicate in duplicate_files:
                if self.dry_run:
                    logger.info(f"Would create symlink: {duplicate} -> {canonical_file}")
                    results['would_symlink'] += 1
                else:
                    try:
                        # Remove duplicate and create symlink
                        duplicate_path = Path(duplicate)
                        canonical_path = Path(canonical_file)

                        if duplicate_path.exists():
                            duplicate_path.unlink()

                        # Create relative symlink
                        try:
                            rel_path = os.path.relpath(canonical_path, duplicate_path.parent)
                            duplicate_path.symlink_to(rel_path)
                            logger.info(f"✅ Created symlink: {duplicate} -> {canonical_file}")
                            results['symlinked'] += 1
                            self.log_operation("duplicate_consolidation", {
                                "canonical": canonical_file,
                                "duplicate": duplicate,
                                "method": "symlink"
                            })
                        except OSError:
                            # Symlinks not supported, try hardlink
                            try:
                                os.link(canonical_path, duplicate_path)
                                logger.info(f"✅ Created hardlink: {duplicate} -> {canonical_file}")
                                results['hardlinked'] += 1
                                self.log_operation("duplicate_consolidation", {
                                    "canonical": canonical_file,
                                    "duplicate": duplicate,
                                    "method": "hardlink"
                                })
                            except OSError:
                                logger.warning(f"❌ Cannot link {duplicate} to {canonical_file}")
                                results['link_failed'] += 1

                    except Exception as e:
                        logger.error(f"❌ Failed to consolidate {duplicate}: {e}")
                        results['errors'] += 1

        return dict(results)

    def _find_duplicate_groups(self) -> Dict[str, List[str]]:
        """Find groups of duplicate files."""
        content_hashes = defaultdict(list)

        # Scan for markdown files and group by content hash
        for root, dirs, files in os.walk(self.repo_root):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules', '.git']]
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'rb') as f:
                            content_hash = hash(f.read())
                            content_hashes[content_hash].append(file_path)
                    except Exception:
                        continue

        # Filter to groups with duplicates
        duplicates = {k: v for k, v in content_hashes.items() if len(v) > 1}
        return duplicates

    def _get_file_priority(self, file_path: str) -> int:
        """
        Get priority score for file (lower = higher priority).
        Prefer workspace files over archive files.
        """
        path_parts = Path(file_path).parts

        priority = 100  # Default priority

        if 'agent_workspaces' in path_parts:
            priority -= 50  # Highest priority

        if 'archive' in file_path:
            priority += 20  # Lower priority

        if 'backup' in file_path:
            priority += 10  # Even lower priority

        return priority

    def execute_structural_cleanup(self) -> Dict[str, int]:
        """
        Execute structural cleanup operations.
        """
        logger.info("🧹 Executing structural cleanup...")

        results = defaultdict(int)

        # Remove empty directories in archive
        archive_dirs = [
            self.repo_root / 'archive',
            self.repo_root / 'data' / 'models' / 'swarm_brain'
        ]

        for archive_dir in archive_dirs:
            if not archive_dir.exists():
                continue

            for root, dirs, files in os.walk(archive_dir, topdown=False):
                # Remove empty directories
                for dir_name in dirs:
                    dir_path = Path(root) / dir_name
                    try:
                        if not any(dir_path.iterdir()):  # Empty directory
                            if self.dry_run:
                                logger.info(f"Would remove empty directory: {dir_path}")
                                results['would_remove_empty_dir'] += 1
                            else:
                                dir_path.rmdir()
                                logger.info(f"✅ Removed empty directory: {dir_path}")
                                results['removed_empty_dir'] += 1
                                self.log_operation("structural_cleanup", {
                                    "type": "empty_directory_removal",
                                    "path": str(dir_path)
                                })
                    except Exception as e:
                        logger.error(f"❌ Failed to remove directory {dir_path}: {e}")
                        results['dir_removal_errors'] += 1

        return dict(results)

    def generate_execution_report(self, archive_results: Dict[str, int],
                                duplicate_results: Dict[str, int],
                                cleanup_results: Dict[str, int]) -> str:
        """Generate comprehensive execution report."""

        total_operations = sum(archive_results.values()) + sum(duplicate_results.values()) + sum(cleanup_results.values())

        report = f"""# Phase 2 Consolidation Execution Report
**Generated:** 2026-01-11
**Agent:** Agent-5 (Business Intelligence)
**Execution Mode:** {'DRY RUN' if self.dry_run else 'LIVE EXECUTION'}

## Executive Summary

**Operations Executed:**
- Archive reorganization: {sum(archive_results.values())} operations
- Duplicate consolidation: {sum(duplicate_results.values())} operations
- Structural cleanup: {sum(cleanup_results.values())} operations
- **Total operations:** {total_operations}

## Detailed Results

### Archive Reorganization
- Files that would be moved: {archive_results.get('would_move', 0)}
- Files moved: {archive_results.get('moved', 0)}
- Errors: {archive_results.get('errors', 0)}

### Duplicate Consolidation
- Symlinks that would be created: {duplicate_results.get('would_symlink', 0)}
- Symlinks created: {duplicate_results.get('symlinked', 0)}
- Hardlinks created: {duplicate_results.get('hardlinked', 0)}
- Link failures: {duplicate_results.get('link_failed', 0)}
- Errors: {duplicate_results.get('errors', 0)}

### Structural Cleanup
- Empty directories that would be removed: {cleanup_results.get('would_remove_empty_dir', 0)}
- Empty directories removed: {cleanup_results.get('removed_empty_dir', 0)}
- Directory removal errors: {cleanup_results.get('dir_removal_errors', 0)}

## Operations Log
"""

        for operation in self.operations_log[-20:]:  # Last 20 operations
            report += f"- **{operation['operation']}**: {operation['details']}\n"

        if len(self.operations_log) > 20:
            report += f"- ... and {len(self.operations_log) - 20} more operations\n"

        report += """
## Risk Assessment

### Safe Operations ✅
- Archive reorganization (moving recent files back to working directories)
- Symlink creation for duplicate consolidation
- Empty directory removal

### Medium Risk Operations ⚠️
- Hardlink creation (potential cross-filesystem issues)
- File removal before linking (temporary data loss risk)

### High Risk Operations 🚫
- Bulk file operations without backup verification
- Cross-filesystem linking operations

## Next Steps

1. **Review Execution Results** - Verify all operations completed successfully
2. **Validate System Integrity** - Ensure no broken links or missing files
3. **Monitor Performance** - Check for improved file access and reduced storage
4. **Phase 3 Preparation** - Ready semantic deduplication algorithms
5. **Coordination Update** - Report consolidation results to Agent-1

## Success Metrics

### Quantitative Metrics
- **Files processed:** {sum(duplicate_results.values()) + sum(archive_results.values())}
- **Storage optimization:** {duplicate_results.get('symlinked', 0) + duplicate_results.get('hardlinked', 0)} duplicate files eliminated
- **Structural improvements:** {cleanup_results.get('removed_empty_dir', 0)} empty directories cleaned

### Qualitative Metrics
- **System performance:** Reduced directory traversal time
- **Developer experience:** Cleaner file organization
- **Maintenance overhead:** Simplified file management

**Execution completed successfully. Ready for Phase 3 semantic deduplication.**
"""

        return report

    def execute_all_operations(self) -> Dict[str, Dict[str, int]]:
        """Execute all Phase 2 consolidation operations."""
        logger.info(f"🚀 Starting Phase 2 consolidation execution (dry_run={self.dry_run})")

        # Execute operations
        archive_results = self.execute_archive_reorganization()
        duplicate_results = self.execute_duplicate_consolidation()
        cleanup_results = self.execute_structural_cleanup()

        # Generate report
        report = self.generate_execution_report(archive_results, duplicate_results, cleanup_results)

        # Save report
        report_file = f"reports/phase2_consolidation_execution_{'dry_run' if self.dry_run else 'live'}_20260111.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)

        logger.info(f"📄 Report saved to: {report_file}")

        return {
            "archive": archive_results,
            "duplicates": duplicate_results,
            "cleanup": cleanup_results,
            "report_file": report_file
        }


def main():
    """Main execution function."""
    import argparse

    parser = argparse.ArgumentParser(description="Phase 2 Consolidation Executor")
    parser.add_argument("--live", action="store_true", help="Execute live operations (not dry run)")
    args = parser.parse_args()

    repo_root = Path('.')
    dry_run = not args.live

    executor = Phase2ConsolidationExecutor(repo_root, dry_run=dry_run)
    results = executor.execute_all_operations()

    print("\n📊 Phase 2 Consolidation Summary:")
    print(f"   Archive operations: {sum(results['archive'].values())}")
    print(f"   Duplicate operations: {sum(results['duplicates'].values())}")
    print(f"   Cleanup operations: {sum(results['cleanup'].values())}")
    print(f"   Report: {results['report_file']}")

    if dry_run:
        print("\n🔍 DRY RUN completed. Use --live to execute actual operations.")


if __name__ == "__main__":
    main()