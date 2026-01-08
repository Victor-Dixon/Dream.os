#!/usr/bin/env python3
"""
Directory Audit Helper Tool
==========================

A utility to assist with repository directory audits by providing:
- Directory size analysis
- File type breakdown
- Risk assessment suggestions
- Archive recommendations

Usage: python tools/directory_audit_helper.py <directory_path>

Author: Agent-7 (Web Development Specialist)
Created: 2026-01-07
"""

import os
import sys
from pathlib import Path
from collections import defaultdict
import argparse

def get_directory_stats(directory_path):
    """Analyze a directory and return comprehensive statistics."""
    path = Path(directory_path)

    if not path.exists():
        print(f"❌ Directory not found: {directory_path}")
        return None

    stats = {
        'total_files': 0,
        'total_size': 0,
        'file_types': defaultdict(int),
        'subdirectories': [],
        'largest_files': [],
        'old_files': []
    }

    try:
        for item in path.rglob('*'):
            if item.is_file():
                stats['total_files'] += 1
                size = item.stat().st_size
                stats['total_size'] += size

                # File type analysis
                ext = item.suffix.lower() or 'no_extension'
                stats['file_types'][ext] += 1

                # Track largest files
                stats['largest_files'].append((item, size))
                stats['largest_files'].sort(key=lambda x: x[1], reverse=True)
                stats['largest_files'] = stats['largest_files'][:5]

                # Track potentially old files (placeholder - would need modification time analysis)
                # stats['old_files'].append((item, item.stat().st_mtime))

            elif item.is_dir() and item != path:
                stats['subdirectories'].append(item)

    except PermissionError:
        print(f"⚠️ Permission denied accessing: {directory_path}")
        return None

    return stats

def format_size(bytes_size):
    """Format bytes into human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f}{unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f}TB"

def generate_risk_assessment(stats):
    """Generate risk assessment suggestions based on directory analysis."""
    assessment = []

    # Size-based assessment
    if stats['total_size'] > 100 * 1024 * 1024:  # 100MB
        assessment.append("🟡 LARGE DIRECTORY - Consider archiving or cleanup")
    elif stats['total_size'] > 10 * 1024 * 1024:  # 10MB
        assessment.append("🟢 MODERATE SIZE - Monitor growth")
    else:
        assessment.append("🟢 SMALL DIRECTORY - Low maintenance concern")

    # File type analysis
    py_files = stats['file_types'].get('.py', 0)
    if py_files > 50:
        assessment.append(f"🔴 HIGH CODE VOLUME - {py_files} Python files, likely active development")

    # Subdirectory analysis
    if len(stats['subdirectories']) > 20:
        assessment.append(f"🟡 MANY SUBDIRS - {len(stats['subdirectories'])} subdirectories, consider reorganization")

    return assessment

def main():
    parser = argparse.ArgumentParser(description='Directory Audit Helper Tool')
    parser.add_argument('directory', help='Directory path to analyze')
    parser.add_argument('--output', '-o', help='Output file for detailed report')

    args = parser.parse_args()

    print("🔍 Directory Audit Helper")
    print("=" * 40)

    stats = get_directory_stats(args.directory)

    if not stats:
        sys.exit(1)

    # Display results
    print(f"📁 Directory: {args.directory}")
    print(f"📊 Total Files: {stats['total_files']:,}")
    print(f"💾 Total Size: {format_size(stats['total_size'])}")
    print(f"📂 Subdirectories: {len(stats['subdirectories'])}")

    print(f"\n📋 File Types (Top 10):")
    sorted_types = sorted(stats['file_types'].items(), key=lambda x: x[1], reverse=True)
    for ext, count in sorted_types[:10]:
        print(f"  {ext}: {count} files")

    print(f"\n🎯 Risk Assessment:")
    assessment = generate_risk_assessment(stats)
    for item in assessment:
        print(f"  {item}")

    if stats['largest_files']:
        print(f"\n📏 Largest Files:")
        for file_path, size in stats['largest_files']:
            print(f"  {format_size(size)} - {file_path.name}")

    # Save detailed report if requested
    if args.output:
        with open(args.output, 'w') as f:
            f.write(f"# Directory Audit Report: {args.directory}\n\n")
            f.write(f"- Total Files: {stats['total_files']}\n")
            f.write(f"- Total Size: {format_size(stats['total_size'])}\n")
            f.write(f"- Subdirectories: {len(stats['subdirectories'])}\n\n")

            f.write("## File Types\n")
            for ext, count in sorted_types:
                f.write(f"- {ext}: {count} files\n")

            f.write("\n## Risk Assessment\n")
            for item in assessment:
                f.write(f"- {item}\n")

            f.write("\n## Largest Files\n")
            for file_path, size in stats['largest_files']:
                f.write(f"- {format_size(size)} - {file_path}\n")

        print(f"\n💾 Detailed report saved to: {args.output}")

    print("
✅ Analysis complete!"if __name__ == "__main__":
    main()