#!/usr/bin/env python3
"""
Comprehensive Cleanup Scanner
============================

Scans repository for unnecessary files that can be safely removed.
Identifies cache files, old logs, duplicates, and other cleanup opportunities.

Usage:
    python tools/cleanup_scanner.py --scan-all --output cleanup_report.json
    python tools/cleanup_scanner.py --dry-run --remove-cache --remove-old-logs

Author: Agent-5 (Business Intelligence Specialist)
Date: 2026-01-08
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple
from datetime import datetime, timedelta
import argparse
import hashlib


class CleanupScanner:
    """
    Comprehensive scanner for identifying unnecessary files for cleanup.
    """

    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path)
        self.findings = {
            "cache_files": [],
            "old_logs": [],
            "empty_files": [],
            "duplicate_files": [],
            "temp_files": [],
            "old_backups": [],
            "unused_imports": [],
            "large_files": [],
            "summary": {}
        }

        # File patterns to identify
        self.cache_patterns = [
            r'__pycache__',
            r'\.pyc$',
            r'\.pyo$',
            r'\.cache$',
            r'\.pytest_cache',
            r'\.ruff_cache',
            r'\.mypy_cache',
            r'\.vscode.*cache',
            r'node_modules',
            r'\.DS_Store$',
            r'Thumbs\.db$'
        ]

        self.temp_patterns = [
            r'\.tmp$',
            r'\.temp$',
            r'\.swp$',
            r'\.swo$',
            r'~\$.*',
            r'\.bak$',
            r'\.backup$',
            r'\.old$'
        ]

        self.log_patterns = [
            r'\.log$',
            r'logs/',
            r'agent_cellphone\.log'
        ]

    def scan_all(self) -> Dict[str, Any]:
        """Run all cleanup scans."""
        print("🔍 Starting comprehensive cleanup scan...")

        self.scan_cache_files()
        self.scan_temp_files()
        self.scan_old_logs()
        self.scan_empty_files()
        self.scan_large_files()
        self.scan_duplicate_files()
        self.scan_unused_imports()

        self.calculate_summary()
        return self.findings

    def scan_cache_files(self) -> None:
        """Scan for cache files and directories."""
        print("  📦 Scanning for cache files...")

        # Direct patterns that work with glob
        cache_globs = [
            '**/__pycache__',
            '**/*.pyc',
            '**/*.pyo',
            '**/*.cache',
            '**/.pytest_cache',
            '**/.ruff_cache',
            '**/.mypy_cache',
            '**/.DS_Store',
            '**/Thumbs.db'
        ]

        for pattern in cache_globs:
            try:
                for path in self.root_path.glob(pattern):
                    if path.is_file() or path.is_dir():
                        file_info = self._get_file_info(path)
                        self.findings["cache_files"].append(file_info)
            except ValueError:
                continue

    def scan_temp_files(self) -> None:
        """Scan for temporary files."""
        print("  🗂️  Scanning for temporary files...")

        temp_globs = [
            '**/*.tmp',
            '**/*.temp',
            '**/*.swp',
            '**/*.swo',
            '**/*.bak',
            '**/*.backup',
            '**/*.old'
        ]

        for pattern in temp_globs:
            try:
                for path in self.root_path.glob(pattern):
                    if path.is_file():
                        file_info = self._get_file_info(path)
                        self.findings["temp_files"].append(file_info)
            except ValueError:
                continue

    def scan_old_logs(self, days_old: int = 30) -> None:
        """Scan for old log files."""
        print(f"  📝 Scanning for logs older than {days_old} days...")

        cutoff_date = datetime.now() - timedelta(days=days_old)

        log_globs = [
            '**/*.log',
            'logs/**/*',
            '**/agent_cellphone.log'
        ]

        for pattern in log_globs:
            try:
                for path in self.root_path.glob(pattern):
                    if path.is_file():
                        try:
                            mtime = datetime.fromtimestamp(path.stat().st_mtime)
                            if mtime < cutoff_date:
                                file_info = self._get_file_info(path)
                                file_info["days_old"] = (datetime.now() - mtime).days
                                self.findings["old_logs"].append(file_info)
                        except OSError:
                            continue
            except ValueError:
                continue

    def scan_empty_files(self) -> None:
        """Scan for empty files."""
        print("  📄 Scanning for empty files...")

        for path in self.root_path.rglob("*"):
            if path.is_file() and path.stat().st_size == 0:
                # Skip certain file types
                if not any(skip in str(path) for skip in ['.git', '__pycache__', '.DS_Store']):
                    file_info = self._get_file_info(path)
                    self.findings["empty_files"].append(file_info)

    def scan_large_files(self, min_size_mb: int = 100) -> None:
        """Scan for unusually large files."""
        print(f"  📊 Scanning for files larger than {min_size_mb}MB...")

        min_size_bytes = min_size_mb * 1024 * 1024

        for path in self.root_path.rglob("*"):
            if path.is_file():
                try:
                    size = path.stat().st_size
                    if size > min_size_bytes:
                        file_info = self._get_file_info(path)
                        file_info["size_mb"] = size / (1024 * 1024)
                        self.findings["large_files"].append(file_info)
                except OSError:
                    continue

    def scan_duplicate_files(self) -> None:
        """Scan for duplicate files based on content hash."""
        print("  🔄 Scanning for duplicate files...")

        file_hashes = {}
        duplicates = []

        # First pass: calculate hashes
        for path in self.root_path.rglob("*"):
            if path.is_file() and self._should_check_file(path):
                try:
                    file_hash = self._calculate_file_hash(path)
                    if file_hash in file_hashes:
                        duplicates.append({
                            "file": str(path),
                            "duplicate_of": file_hashes[file_hash],
                            "size": path.stat().st_size
                        })
                    else:
                        file_hashes[file_hash] = str(path)
                except (OSError, IOError):
                    continue

        self.findings["duplicate_files"] = duplicates

    def scan_unused_imports(self) -> None:
        """Scan for potential unused imports in Python files."""
        print("  🐍 Scanning for unused imports...")

        unused_imports = []

        for path in self.root_path.rglob("*.py"):
            if self._should_skip_file(path):
                continue

            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # Simple heuristic: check for common unused import patterns
                lines = content.split('\n')
                imports = []
                usage = set()

                for line in lines:
                    line = line.strip()
                    if line.startswith('import ') or line.startswith('from '):
                        # Extract module names
                        if 'import ' in line:
                            parts = line.split('import ')
                            if len(parts) > 1:
                                modules = [m.strip().split(' as ')[0] for m in parts[1].split(',')]
                                imports.extend(modules)
                        elif 'from ' in line:
                            parts = line.split('from ')
                            if len(parts) > 1:
                                module = parts[1].split(' import ')[0].strip()
                                imports.append(module)

                    # Check for usage (simple heuristic)
                    for imp in imports:
                        if imp in line and not line.startswith('import ') and not line.startswith('from '):
                            usage.add(imp)

                # Find potentially unused imports
                potentially_unused = [imp for imp in imports if imp not in usage]
                if potentially_unused:
                    unused_imports.append({
                        "file": str(path),
                        "potentially_unused": potentially_unused,
                        "total_imports": len(imports)
                    })

            except Exception as e:
                continue

        self.findings["unused_imports"] = unused_imports

    def calculate_summary(self) -> None:
        """Calculate summary statistics."""
        total_cache_size = sum(f.get("size", 0) for f in self.findings["cache_files"])
        total_temp_size = sum(f.get("size", 0) for f in self.findings["temp_files"])
        total_log_size = sum(f.get("size", 0) for f in self.findings["old_logs"])
        total_duplicate_size = sum(f.get("size", 0) for f in self.findings["duplicate_files"])

        self.findings["summary"] = {
            "scan_timestamp": datetime.now().isoformat(),
            "cache_files": {
                "count": len(self.findings["cache_files"]),
                "total_size_mb": total_cache_size / (1024 * 1024)
            },
            "temp_files": {
                "count": len(self.findings["temp_files"]),
                "total_size_mb": total_temp_size / (1024 * 1024)
            },
            "old_logs": {
                "count": len(self.findings["old_logs"]),
                "total_size_mb": total_log_size / (1024 * 1024)
            },
            "empty_files": {
                "count": len(self.findings["empty_files"])
            },
            "duplicate_files": {
                "count": len(self.findings["duplicate_files"]),
                "total_size_mb": total_duplicate_size / (1024 * 1024)
            },
            "large_files": {
                "count": len(self.findings["large_files"])
            },
            "unused_imports": {
                "count": len(self.findings["unused_imports"])
            },
            "total_potential_savings_mb": (total_cache_size + total_temp_size +
                                         total_log_size + total_duplicate_size) / (1024 * 1024)
        }

    def _get_file_info(self, path: Path) -> Dict[str, Any]:
        """Get file information."""
        try:
            stat = path.stat()
            return {
                "path": str(path),
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "is_dir": path.is_dir()
            }
        except OSError:
            return {
                "path": str(path),
                "size": 0,
                "modified": None,
                "is_dir": path.is_dir(),
                "error": "Could not access file"
            }

    def _should_skip_file(self, path: Path) -> bool:
        """Check if file should be skipped in analysis."""
        skip_patterns = [
            '__pycache__',
            '.git',
            'node_modules',
            '.vscode',
            '.idea',
            'build',
            'dist',
            '.pytest_cache',
            '.ruff_cache'
        ]

        path_str = str(path)
        return any(pattern in path_str for pattern in skip_patterns)

    def _should_check_file(self, path: Path) -> bool:
        """Check if file should be included in duplicate checking."""
        if self._should_skip_file(path):
            return False

        # Skip very large files (>100MB)
        try:
            if path.stat().st_size > 100 * 1024 * 1024:
                return False
        except OSError:
            return False

        # Only check text-based files and common binary formats
        extensions_to_check = {
            '.py', '.js', '.ts', '.json', '.txt', '.md', '.html', '.css',
            '.xml', '.yaml', '.yml', '.ini', '.cfg', '.conf'
        }

        return path.suffix.lower() in extensions_to_check

    def _calculate_file_hash(self, path: Path, chunk_size: int = 8192) -> str:
        """Calculate file hash for duplicate detection."""
        hash_obj = hashlib.md5()
        try:
            with open(path, 'rb') as f:
                while chunk := f.read(chunk_size):
                    hash_obj.update(chunk)
            return hash_obj.hexdigest()
        except (OSError, IOError):
            return ""

    def save_report(self, output_path: str) -> None:
        """Save findings to JSON file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.findings, f, indent=2, ensure_ascii=False)

    def print_summary(self) -> None:
        """Print human-readable summary."""
        summary = self.findings["summary"]

        print("\n" + "="*60)
        print("🧹 CLEANUP SCAN RESULTS")
        print("="*60)

        print("\n📦 Cache Files:")
        print(f"   Count: {summary['cache_files']['count']:,}")
        print(f"   Size: {summary['cache_files']['total_size_mb']:.1f} MB")

        print("\n🗂️  Temp Files:")
        print(f"   Count: {summary['temp_files']['count']:,}")
        print(f"   Size: {summary['temp_files']['total_size_mb']:.1f} MB")

        print("\n📝 Old Logs:")
        print(f"   Count: {summary['old_logs']['count']:,}")
        print(f"   Size: {summary['old_logs']['total_size_mb']:.1f} MB")

        print("\n📄 Empty Files:")
        print(f"   Count: {summary['empty_files']['count']:,}")

        print("\n🔄 Duplicate Files:")
        print(f"   Count: {summary['duplicate_files']['count']:,}")
        print(f"   Size: {summary['duplicate_files']['total_size_mb']:.1f} MB")

        print("\n📊 Large Files:")
        print(f"   Count: {summary['large_files']['count']:,}")

        print("\n🐍 Files with Unused Imports:")
        print(f"   Count: {summary['unused_imports']['count']:,}")

        print("\n💾 TOTAL POTENTIAL SAVINGS:")
        print(f"   {summary['total_potential_savings_mb']:.1f} MB")

        print("\n" + "="*60)


def main():
    parser = argparse.ArgumentParser(description="Comprehensive cleanup scanner")
    parser.add_argument("--scan-all", action="store_true", help="Run all cleanup scans")
    parser.add_argument("--cache-only", action="store_true", help="Scan only cache files")
    parser.add_argument("--logs-only", action="store_true", help="Scan only old logs")
    parser.add_argument("--duplicates-only", action="store_true", help="Scan only duplicates")
    parser.add_argument("--output", "-o", help="Output JSON file path")
    parser.add_argument("--root", default=".", help="Root directory to scan")
    parser.add_argument("--days-old", type=int, default=30, help="Consider logs older than N days as old")

    args = parser.parse_args()

    scanner = CleanupScanner(args.root)

    if args.scan_all:
        scanner.scan_all()
    elif args.cache_only:
        scanner.scan_cache_files()
    elif args.logs_only:
        scanner.scan_old_logs(args.days_old)
    elif args.duplicates_only:
        scanner.scan_duplicate_files()
    else:
        print("Use --scan-all or specific scan options")
        return

    scanner.print_summary()

    if args.output:
        scanner.save_report(args.output)
        print(f"\n📄 Detailed report saved to: {args.output}")


if __name__ == "__main__":
    main()