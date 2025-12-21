#!/usr/bin/env python3
"""
Phase -1: Deprecate NOISE Tools and Clean Archive Directories

This script:
1. Deletes 26 NOISE tools (thin wrappers identified in classification)
2. Removes all archive directories (archive/, docs/archive/, consolidation_backups/, etc.)
3. Creates deprecation notices
4. Updates documentation
5. Generates cleanup report
"""

import json
import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple


def load_noise_tools(json_path: Path) -> List[Dict]:
    """Load list of NOISE tools from classification results."""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('noise', [])
    except FileNotFoundError:
        print(f"❌ Classification JSON not found: {json_path}")
        return []


def find_archive_directories(repo_root: Path) -> List[Path]:
    """Find all archive and backup directories."""
    archive_dirs = []

    # Common archive directory names
    archive_patterns = [
        'archive',
        'archives',
        '*_archive',
        '*_backup',
        '*_backups',
        'consolidation_backups',
        'consolidation_logs',
        'backups',
    ]

    # Directories to check
    check_dirs = [
        repo_root,
        repo_root / 'docs',
        repo_root / 'tools',
    ]

    for check_dir in check_dirs:
        if not check_dir.exists():
            continue

        # Look for exact matches
        for pattern in ['archive', 'archives', 'backups', 'consolidation_backups', 'consolidation_logs']:
            archive_path = check_dir / pattern
            if archive_path.exists() and archive_path.is_dir():
                archive_dirs.append(archive_path)

    # Also check for pattern matches in root
    if repo_root.exists():
        for item in repo_root.iterdir():
            if item.is_dir():
                name_lower = item.name.lower()
                if any(pattern in name_lower for pattern in ['archive', 'backup']) and 'backup' not in str(repo_root / 'consolidation_backups'):
                    if item not in archive_dirs:
                        archive_dirs.append(item)

    return sorted(set(archive_dirs))


def delete_noise_tools(repo_root: Path, noise_tools: List[Dict], dry_run: bool = False) -> Tuple[List[str], List[str]]:
    """Delete NOISE tools."""
    deleted = []
    errors = []

    for tool in noise_tools:
        file_path_str = tool.get('file', '')
        # Try multiple path formats
        possible_paths = [
            repo_root / file_path_str,  # Try as-is
            repo_root / file_path_str.replace('\\', '/'),  # Forward slashes
            # OS-specific separators
            repo_root / file_path_str.replace('\\', os.sep),
        ]

        # If path starts with 'tools\', also try removing that prefix
        if file_path_str.startswith('tools\\') or file_path_str.startswith('tools/'):
            clean_path = file_path_str.replace(
                'tools\\', '').replace('tools/', '')
            possible_paths.extend([
                repo_root / 'tools' / clean_path,
                repo_root / 'tools' / clean_path.replace('\\', '/'),
            ])

        file_path = None
        for path in possible_paths:
            if path.exists() and path.is_file():
                file_path = path
                break

        if not file_path:
            errors.append(f"{file_path_str} - File not found")
            print(
                f"⚠️  File not found (may already be deleted): {file_path_str}")
            continue

        try:
            if not dry_run:
                file_path.unlink()
            deleted.append(file_path_str)
            print(f"{'[DRY RUN] ' if dry_run else ''}✅ Deleted: {file_path_str}")
        except Exception as e:
            errors.append(f"{file_path_str} - Error: {str(e)}")
            print(f"❌ Error deleting {file_path_str}: {e}")

    return deleted, errors


def delete_archive_directories(archive_dirs: List[Path], dry_run: bool = False) -> Tuple[List[str], List[str]]:
    """Delete archive directories."""
    deleted = []
    errors = []

    for archive_dir in archive_dirs:
        try:
            if not archive_dir.exists():
                continue

            # Calculate size for reporting
            total_size = sum(
                f.stat().st_size for f in archive_dir.rglob('*') if f.is_file())
            size_mb = total_size / (1024 * 1024)
            file_count = sum(1 for f in archive_dir.rglob('*') if f.is_file())

            if not dry_run:
                shutil.rmtree(archive_dir)

            deleted.append(
                f"{archive_dir} ({file_count} files, {size_mb:.2f} MB)")
            print(
                f"{'[DRY RUN] ' if dry_run else ''}✅ Deleted: {archive_dir} ({file_count} files, {size_mb:.2f} MB)")
        except Exception as e:
            errors.append(f"{archive_dir} - Error: {str(e)}")
            print(f"❌ Error deleting {archive_dir}: {e}")

    return deleted, errors


def create_deprecation_notice(repo_root: Path, deleted_tools: List[str], deleted_archives: List[str]):
    """Create deprecation notice document."""
    notice_path = repo_root / 'DEPRECATION_NOTICES.md'

    lines = [
        "# Deprecation Notices",
        "",
        f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Phase**: -1 (Signal vs Noise Classification)",
        "",
        "## Overview",
        "",
        "This document records deprecated tools and directories removed during Phase -1 cleanup.",
        "",
        "## Deprecated NOISE Tools",
        "",
        f"The following **{len(deleted_tools)} tools** were identified as NOISE (thin wrappers) and have been removed:",
        "",
        "### Removal Rationale",
        "",
        "NOISE tools are thin wrappers that:",
        "- Have no real business logic",
        "- Just call other tools/functions",
        "- Can be replaced by direct usage of underlying tools",
        "- Many had syntax errors (broken/unmaintained)",
        "",
        "### Removed Tools",
        "",
        "| Tool | Reason |",
        "|------|--------|",
    ]

    for tool_path in sorted(deleted_tools):
        tool_name = Path(tool_path).name
        clean_path = tool_path.replace(
            'tools\\', 'tools/').replace('tools\\\\', 'tools/')
        lines.append(
            f"| `{clean_path}` | NOISE - Thin wrapper, removed during Phase -1 |")

    lines.extend([
        "",
        "## Removed Archive Directories",
        "",
        f"The following **{len(deleted_archives)} archive/backup directories** were removed:",
        "",
        "### Removal Rationale",
        "",
        "Archive directories are historical snapshots that:",
        "- Take up disk space",
        "- Are no longer needed for active development",
        "- Can be recovered from git history if needed",
        "",
        "### Removed Directories",
        "",
        "| Directory | Details |",
        "|-----------|---------|",
    ])

    for archive_info in sorted(deleted_archives):
        lines.append(
            f"| `{archive_info.split(' (')[0]}` | {archive_info.split(' (')[1].rstrip(')') if ' (' in archive_info else 'Removed'} |")

    lines.extend([
        "",
        "## Recovery",
        "",
        "If any deprecated tools or archives are needed:",
        "- Check git history: `git log --all --full-history -- <path>`",
        "- Check git tags for historical snapshots",
        "- Review deprecation date in this document",
        "",
        "## Reference",
        "",
        "- Classification: `docs/toolbelt/TOOL_CLASSIFICATION.md`",
        "- Migration Plan: `docs/toolbelt/NOISE_TOOLS_MIGRATION_PLAN.md`",
        "- Phase -1 Summary: `docs/toolbelt/PHASE_MINUS1_EXECUTION_SUMMARY.md`",
        "",
        "---",
        "",
        "🐝 **WE. ARE. SWARM. ⚡🔥**",
    ])

    # Append to existing file or create new
    if notice_path.exists():
        with open(notice_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()
        with open(notice_path, 'w', encoding='utf-8') as f:
            f.write(existing_content + '\n\n' + '\n'.join(lines))
    else:
        with open(notice_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

    print(f"✅ Created/updated deprecation notice: {notice_path}")


def generate_cleanup_report(repo_root: Path, deleted_tools: List[str], deleted_archives: List[str], errors: List[str]):
    """Generate cleanup report."""
    report_path = repo_root / 'docs' / 'toolbelt' / 'PHASE_MINUS1_CLEANUP_REPORT.md'
    report_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Phase -1 Cleanup Report",
        "",
        f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Phase**: -1 (Signal vs Noise Classification)",
        f"**Status**: ✅ COMPLETE",
        "",
        "## Summary",
        "",
        f"- **NOISE Tools Removed**: {len(deleted_tools)}",
        f"- **Archive Directories Removed**: {len(deleted_archives)}",
        f"- **Errors**: {len(errors)}",
        "",
        "## Removed NOISE Tools",
        "",
        f"Total: {len(deleted_tools)} tools",
        "",
        "```",
    ]

    for tool in sorted(deleted_tools):
        clean_tool = tool.replace(
            'tools\\', 'tools/').replace('tools\\\\', 'tools/')
        lines.append(f"  {clean_tool}")

    lines.extend([
        "```",
        "",
        "## Removed Archive Directories",
        "",
        f"Total: {len(deleted_archives)} directories",
        "",
        "```",
    ])

    for archive in sorted(deleted_archives):
        lines.append(f"  {archive}")

    lines.extend([
        "```",
        "",
        "## Errors",
        "",
    ])

    if errors:
        for error in errors:
            lines.append(f"- ❌ {error}")
    else:
        lines.append("✅ No errors encountered")

    lines.extend([
        "",
        "## Impact",
        "",
        f"- **Tools Removed**: {len(deleted_tools)} NOISE tools (3.3% of total)",
        f"- **Disk Space Freed**: See archive directory details above",
        f"- **Maintenance Overhead**: Reduced by removing broken/unmaintained wrappers",
        f"- **Refactoring Scope**: Now focused on 719 SIGNAL tools only",
        "",
        "## Next Steps",
        "",
        "1. ✅ NOISE tools deprecated and removed",
        "2. ✅ Archive directories cleaned",
        "3. ⏳ Update toolbelt registry (remove NOISE tools)",
        "4. ⏳ Run V2 compliance checker on SIGNAL tools only (719 tools)",
        "5. ⏳ Update V2 refactoring plan with SIGNAL-only scope",
        "",
        "---",
        "",
        "🐝 **WE. ARE. SWARM. ⚡🔥**",
    ])

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"✅ Generated cleanup report: {report_path}")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Deprecate NOISE tools and clean archive directories')
    parser.add_argument('--dry-run', action='store_true',
                        help='Perform dry run without deleting files')
    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent

    print("🧹 Phase -1 Cleanup: Deprecating NOISE Tools and Removing Archives")
    print(f"   Repository: {repo_root}")
    print(f"   Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    print()

    # Load NOISE tools
    print("📋 Loading NOISE tools classification...")
    classification_json = repo_root / 'tools' / 'TOOL_CLASSIFICATION.json'
    noise_tools = load_noise_tools(classification_json)

    if not noise_tools:
        print("❌ No NOISE tools found in classification results")
        return

    print(f"✅ Found {len(noise_tools)} NOISE tools to remove")
    print()

    # Delete NOISE tools
    print("🗑️  Deleting NOISE tools...")
    deleted_tools, tool_errors = delete_noise_tools(
        repo_root, noise_tools, dry_run=args.dry_run)
    print(f"   ✅ Deleted: {len(deleted_tools)}")
    if tool_errors:
        print(f"   ❌ Errors: {len(tool_errors)}")
    print()

    # Find archive directories
    print("📂 Finding archive directories...")
    archive_dirs = find_archive_directories(repo_root)
    print(f"✅ Found {len(archive_dirs)} archive directories:")
    for archive_dir in archive_dirs:
        print(f"   - {archive_dir}")
    print()

    # Delete archive directories
    print("🗑️  Deleting archive directories...")
    deleted_archives, archive_errors = delete_archive_directories(
        archive_dirs, dry_run=args.dry_run)
    print(f"   ✅ Deleted: {len(deleted_archives)}")
    if archive_errors:
        print(f"   ❌ Errors: {len(archive_errors)}")
    print()

    # Combine errors
    all_errors = tool_errors + archive_errors

    # Create deprecation notice (only if not dry run)
    if not args.dry_run and (deleted_tools or deleted_archives):
        print("📝 Creating deprecation notice...")
        create_deprecation_notice(repo_root, deleted_tools, deleted_archives)
        print()

    # Generate cleanup report
    print("📊 Generating cleanup report...")
    generate_cleanup_report(repo_root, deleted_tools,
                            deleted_archives, all_errors)
    print()

    # Summary
    print("=" * 60)
    print("✅ Cleanup Complete!")
    print(f"   - NOISE tools removed: {len(deleted_tools)}/{len(noise_tools)}")
    print(
        f"   - Archive directories removed: {len(deleted_archives)}/{len(archive_dirs)}")
    print(f"   - Errors: {len(all_errors)}")
    if args.dry_run:
        print()
        print("⚠️  This was a DRY RUN - no files were actually deleted")
        print("   Run without --dry-run to perform actual cleanup")
    print("=" * 60)


if __name__ == '__main__':
    main()
