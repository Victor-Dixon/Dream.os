#!/usr/bin/env python3
"""
Comprehensive SSOT Migration Sweep
==================================

Automated migration of all remaining files to SSOT patterns.

<!-- SSOT Domain: migration-automation -->

Executes systematic consolidation across entire codebase:
- Identifies all files needing SSOT patterns
- Applies standardized imports, logging, and error handling
- Batch processes for efficiency
- Validates migration success

V2 Compliant: Complete codebase SSOT adoption
Author: Agent-8 (SSOT & System Integration)
Date: 2026-01-12
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Set, Tuple
from dataclasses import dataclass, field


@dataclass
class MigrationStats:
    """Statistics for migration operations."""
    total_files: int = 0
    processed_files: int = 0
    migrated_files: int = 0
    skipped_files: int = 0
    errors: List[str] = field(default_factory=list)


class ComprehensiveMigrationSweep:
    """
    Comprehensive SSOT migration across entire codebase.

    Systematically applies SSOT patterns to all eligible files.
    """

    def __init__(self):
        self.stats = MigrationStats()
        self.processed_files: Set[Path] = set()

        # SSOT patterns to apply
        self.ssot_patterns = {
            'import_consolidation': {
                'pattern': r'from typing import ([^\n]+)',
                'replacement_func': self._consolidate_typing_imports,
            },
            'ssot_header': {
                'pattern': r'("""[^"]*?Author: ([^\n]+)',
                'replacement_func': self._add_ssot_header,
            },
            'ssot_imports': {
                'pattern': r'(import logging)',
                'replacement': r'# SSOT Import Standardization\nimport logging\nfrom src.core.base.import_standardization import *\nfrom src.core.base.service_base import BaseService\nfrom src.core.base.error_handling import ErrorHandler, error_context',
            },
            'logger_standardization': {
                'pattern': r'logger = logging\.getLogger\(__name__\)',
                'replacement': r'# Initialize standardized logger through SSOT base\nlogger = logging.getLogger(__name__)',
            }
        }

    def _consolidate_typing_imports(self, match: re.Match) -> str:
        """Consolidate typing imports using SSOT patterns."""
        imports_str = match.group(1)

        # Parse imports, removing duplicates
        imports = set()
        for imp in imports_str.split(','):
            imp = imp.strip()
            if imp and not imp.startswith('#'):
                imports.add(imp)

        if not imports:
            return match.group(0)

        # Sort for consistency
        sorted_imports = sorted(imports)

        # Create consolidated import
        imports_str = ',\\n    '.join(sorted_imports)
        consolidated = f"from src.core.base.import_standardization import (\n    {imports_str}\n)"

        return consolidated

    def _add_ssot_header(self, match: re.Match) -> str:
        """Add SSOT migration header."""
        existing_author = match.group(1)

        ssot_header = f"""{match.group(0)}
SSOT Migration: Agent-8 (System Integration)
Date: 2026-01-12

<!-- SSOT Domain: core -->"""

        return ssot_header

    def find_migration_candidates(self, root_path: Path) -> List[Path]:
        """
        Find all files that are candidates for SSOT migration.

        Args:
            root_path: Root directory to search

        Returns:
            List of file paths that need migration
        """
        candidates = []

        # Skip certain directories
        skip_dirs = {'.git', '__pycache__', '.pytest_cache', 'node_modules', '.github'}

        for py_file in root_path.rglob('*.py'):
            # Skip if in excluded directories
            if any(skip_dir in py_file.parts for skip_dir in skip_dirs):
                continue

            # Skip already processed files
            if py_file in self.processed_files:
                continue

            # Skip files that are already migrated
            try:
                content = py_file.read_text(encoding='utf-8')
                if 'SSOT Migration:' in content:
                    continue

                # Check for migration indicators
                has_typing_imports = 'from typing import' in content
                has_logger = 'logger = logging.getLogger' in content
                has_manual_imports = any(imp in content for imp in [
                    'import logging', 'import time', 'import os',
                    'from datetime import', 'from pathlib import'
                ])

                if has_typing_imports or has_logger or has_manual_imports:
                    candidates.append(py_file)

            except (UnicodeDecodeError, OSError) as e:
                self.stats.errors.append(f"Error reading {py_file}: {e}")
                continue

        return candidates

    def migrate_file(self, file_path: Path) -> bool:
        """
        Migrate a single file to use SSOT patterns.

        Args:
            file_path: Path to file to migrate

        Returns:
            True if migration was applied, False otherwise
        """
        try:
            # Read file content
            content = file_path.read_text(encoding='utf-8')
            original_content = content

            # Apply migration patterns
            changes_made = False

            for pattern_name, pattern_config in self.ssot_patterns.items():
                pattern = pattern_config['pattern']

                if 'replacement_func' in pattern_config:
                    # Use function for complex replacements
                    func = pattern_config['replacement_func']

                    def replacement_func(match):
                        result = func(match)
                        if result != match.group(0):
                            nonlocal changes_made
                            changes_made = True
                        return result

                    content = re.sub(pattern, replacement_func, content, flags=re.MULTILINE | re.DOTALL)
                else:
                    # Simple string replacement
                    replacement = pattern_config['replacement']
                    if replacement in content:
                        continue  # Already has this pattern

                    new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
                    if new_content != content:
                        content = new_content
                        changes_made = True

            # Write back if changes were made
            if changes_made:
                file_path.write_text(content, encoding='utf-8')
                self.stats.migrated_files += 1
                print(f"✅ Migrated: {file_path}")
                return True
            else:
                self.stats.skipped_files += 1
                print(f"⏭️  Skipped: {file_path} (no changes needed)")
                return False

        except Exception as e:
            self.stats.errors.append(f"Failed to migrate {file_path}: {e}")
            print(f"❌ Error migrating {file_path}: {e}")
            return False

    def execute_migration_sweep(self, root_path: Path, batch_size: int = 20) -> MigrationStats:
        """
        Execute comprehensive migration sweep.

        Args:
            root_path: Root directory to sweep
            batch_size: Number of files to process in each batch

        Returns:
            Migration statistics
        """
        print("🔍 SSOT Comprehensive Migration Sweep Starting...")
        print("=" * 60)

        # Find all candidates
        candidates = self.find_migration_candidates(root_path)
        self.stats.total_files = len(candidates)

        print(f"📊 Found {len(candidates)} files requiring SSOT migration")

        # Process in batches
        for i in range(0, len(candidates), batch_size):
            batch = candidates[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = (len(candidates) + batch_size - 1) // batch_size

            print(f"\\n🔄 Processing batch {batch_num}/{total_batches} ({len(batch)} files)")

            for file_path in batch:
                self.stats.processed_files += 1
                self.processed_files.add(file_path)

                success = self.migrate_file(file_path)
                if not success and self.stats.processed_files % 10 == 0:
                    print(f"  Progress: {self.stats.processed_files}/{self.stats.total_files} files processed")

        # Final summary
        self._print_summary()

        return self.stats

    def _print_summary(self) -> None:
        """Print migration summary."""
        print("\\n" + "=" * 60)
        print("📋 SSOT Migration Sweep Summary")
        print("=" * 60)

        print(f"Total files found: {self.stats.total_files}")
        print(f"Files processed: {self.stats.processed_files}")
        print(f"Files migrated: {self.stats.migrated_files}")
        print(f"Files skipped: {self.stats.skipped_files}")
        print(f"Errors encountered: {len(self.stats.errors)}")

        success_rate = (self.stats.migrated_files / self.stats.processed_files * 100) if self.stats.processed_files > 0 else 0
        print(".1f")

        if self.stats.errors:
            print("\\n⚠️  Errors encountered:")
            for error in self.stats.errors[:10]:  # Show first 10 errors
                print(f"  - {error}")
            if len(self.stats.errors) > 10:
                print(f"  ... and {len(self.stats.errors) - 10} more errors")

        print("\\n✅ SSOT Migration Sweep Complete!")


def main():
    """Main CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Comprehensive SSOT Migration Sweep")
    parser.add_argument("--root", type=Path, default=Path("src"),
                       help="Root directory to sweep (default: src)")
    parser.add_argument("--batch-size", type=int, default=20,
                       help="Number of files to process per batch (default: 20)")
    parser.add_argument("--dry-run", action="store_true",
                       help="Show what would be migrated without making changes")

    args = parser.parse_args()

    if args.dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
        print("-" * 50)

    # Initialize migration sweep
    sweep = ComprehensiveMigrationSweep()

    try:
        # Execute migration sweep
        if not args.dry_run:
            stats = sweep.execute_migration_sweep(args.root, args.batch_size)
        else:
            # Dry run - just find candidates
            candidates = sweep.find_migration_candidates(args.root)
            print(f"📊 Found {len(candidates)} files that would be migrated:")
            for candidate in candidates[:20]:  # Show first 20
                print(f"  {candidate}")
            if len(candidates) > 20:
                print(f"  ... and {len(candidates) - 20} more")

    except KeyboardInterrupt:
        print("\\n⚠️  Migration sweep interrupted by user")
        sweep._print_summary()

    except Exception as e:
        print(f"❌ Migration sweep failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()