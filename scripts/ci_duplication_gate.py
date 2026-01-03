#!/usr/bin/env python3
"""
CI Duplication Detection Gate
=============================

Prevents new file duplications from being committed to the repository.
Runs as a pre-commit hook and CI check.

Features:
- Detects exact file duplicates by hash
- Prevents committing duplicate files
- Reports duplication hotspots
- Integrates with SSOT enforcement

Author: Agent-4 (Captain) - Technical Debt Prevention Specialist
"""

import sys
import hashlib
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass

# Files and directories to skip during duplication check
SKIP_PATHS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    "node_modules",
    "dist",
    "build",
    "logs",
    ".mypy_cache",
    ".vscode",
    ".cursor",
    "reports",  # Generated reports can be duplicated
    "temp_repos",  # Temp repos expected to have duplicates
}

# File extensions to check for duplication
CHECK_EXTENSIONS = {
    ".py", ".md", ".txt", ".json", ".yaml", ".yml",
    ".js", ".ts", ".css", ".html", ".xml"
}

@dataclass
class DuplicateGroup:
    """Represents a group of duplicate files."""
    hash_value: str
    files: List[Path]
    size: int
    extension: str

    @property
    def count(self) -> int:
        return len(self.files)

    def is_allowed_duplicate(self) -> bool:
        """Check if this duplicate group is allowed."""
        # Allow duplicates in certain contexts
        allowed_patterns = [
            "__init__.py",  # Standard Python package files
            "test_*.py",    # Test files can have similar boilerplate
            "README.md",    # Documentation files
        ]

        first_file = str(self.files[0])
        if any(pattern in first_file for pattern in allowed_patterns):
            return True

        # Allow small files (< 100 bytes) - likely boilerplate
        if self.size < 100:
            return True

        return False

class DuplicationDetector:
    """Detects file duplications in the repository."""

    def __init__(self, root_path: Path):
        self.root_path = root_path
        self.hashes: Dict[str, List[Path]] = {}
        self.duplicates: List[DuplicateGroup] = []

    def should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped."""
        # Skip by path components
        if any(part in SKIP_PATHS for part in file_path.parts):
            return True

        # Only check specific extensions
        if file_path.suffix not in CHECK_EXTENSIONS:
            return True

        # Skip files smaller than 10 bytes (likely empty or trivial)
        try:
            if file_path.stat().st_size < 10:
                return True
        except OSError:
            return True

        return False

    def calculate_file_hash(self, file_path: Path) -> str:
        """Calculate hash of file content."""
        try:
            with open(file_path, "rb") as f:
                # Read first 10KB for quick comparison
                data = f.read(10240)
                return hashlib.md5(data).hexdigest()
        except (OSError, IOError):
            return ""

    def scan_files(self) -> None:
        """Scan all files and build hash dictionary."""
        print("🔍 Scanning repository for duplications...")

        file_count = 0
        for file_path in self.root_path.rglob("*"):
            if not file_path.is_file():
                continue

            if self.should_skip_file(file_path):
                continue

            file_count += 1
            if file_count % 500 == 0:
                print(f"  Processed {file_count} files...")

            file_hash = self.calculate_file_hash(file_path)
            if file_hash:
                self.hashes.setdefault(file_hash, []).append(file_path)

        print(f"✅ Scanned {file_count} files")

    def find_duplicates(self) -> None:
        """Identify duplicate file groups."""
        print("🔍 Identifying duplicate groups...")

        for file_hash, files in self.hashes.items():
            if len(files) > 1:
                # Get file info from first file
                first_file = files[0]
                try:
                    size = first_file.stat().st_size
                    extension = first_file.suffix
                except OSError:
                    size = 0
                    extension = ""

                duplicate_group = DuplicateGroup(
                    hash_value=file_hash,
                    files=files,
                    size=size,
                    extension=extension
                )

                self.duplicates.append(duplicate_group)

        # Sort by file count (most problematic first)
        self.duplicates.sort(key=lambda x: x.count, reverse=True)
        print(f"✅ Found {len(self.duplicates)} duplicate groups")

    def get_blocking_duplicates(self) -> List[DuplicateGroup]:
        """Get duplicate groups that should block commits."""
        return [dup for dup in self.duplicates if not dup.is_allowed_duplicate()]

    def generate_report(self) -> str:
        """Generate a detailed duplication report."""
        report_lines = []
        report_lines.append("# Repository Duplication Report")
        report_lines.append("")

        total_duplicates = sum(dup.count for dup in self.duplicates)
        total_blocking = sum(dup.count for dup in self.get_blocking_duplicates())

        report_lines.append(f"**Total duplicate files:** {total_duplicates}")
        report_lines.append(f"**Blocking duplicates:** {total_blocking}")
        report_lines.append(f"**Duplicate groups:** {len(self.duplicates)}")
        report_lines.append("")

        if self.duplicates:
            report_lines.append("## Top Duplicate Groups")
            report_lines.append("")

            for i, dup in enumerate(self.duplicates[:10]):
                status = "⚠️ BLOCKING" if not dup.is_allowed_duplicate() else "✅ ALLOWED"
                report_lines.append(f"### #{i+1}: {dup.count} files ({dup.size:,} bytes) - {status}")
                report_lines.append("")

                for file_path in dup.files[:5]:  # Show first 5 files
                    report_lines.append(f"- `{file_path}`")

                if len(dup.files) > 5:
                    report_lines.append(f"- ... and {len(dup.files) - 5} more")

                report_lines.append("")

        return "\n".join(report_lines)

def main() -> int:
    """Main CI check function."""
    print("🚫 CI Duplication Gate Check")
    print("=" * 40)

    repo_root = Path(".")
    detector = DuplicationDetector(repo_root)

    detector.scan_files()
    detector.find_duplicates()

    blocking_duplicates = detector.get_blocking_duplicates()

    if blocking_duplicates:
        print(f"❌ BLOCKED: Found {len(blocking_duplicates)} blocking duplicate groups!")
        print()

        for dup in blocking_duplicates[:5]:  # Show first 5 blocking groups
            print(f"🚫 {dup.count} duplicate files ({dup.size:,} bytes):")
            for file_path in dup.files[:3]:
                print(f"   - {file_path}")
            if len(dup.files) > 3:
                print(f"   - ... and {len(dup.files) - 3} more")
            print()

        print("💡 To resolve:")
        print("   1. Remove duplicate files")
        print("   2. Consolidate functionality into SSOT locations")
        print("   3. Update imports to use canonical paths")
        print("   4. See docs/SSOT_MAP.md for consolidation guidance")
        print()

        # Save detailed report
        report_path = Path("reports/ci_duplication_report.md")
        report_path.parent.mkdir(exist_ok=True)
        report_path.write_text(detector.generate_report())

        print(f"📄 Detailed report saved to: {report_path}")
        return 1
    else:
        print("✅ PASSED: No blocking file duplications found!")

        if detector.duplicates:
            allowed_count = len(detector.duplicates) - len(blocking_duplicates)
            print(f"   (Found {allowed_count} allowed duplicate groups)")

        return 0

if __name__ == "__main__":
    sys.exit(main())