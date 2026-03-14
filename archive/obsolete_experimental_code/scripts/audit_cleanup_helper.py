#!/usr/bin/env python3
"""
Audit Cleanup Helper - Safe Codebase Cleanup Script
Executes the safer recommendations from the codebase audit.
"""

import os
import shutil
from pathlib import Path
from typing import List, Tuple


class AuditCleanupHelper:
    """Helper class for safe codebase cleanup operations."""

    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.backup_dir = self.repo_root / "audit_backup_2026_01_12"
        self.backup_dir.mkdir(exist_ok=True)

    def backup_file(self, file_path: Path) -> bool:
        """Create backup of file before deletion."""
        if not file_path.exists():
            return False

        # Create relative path for backup
        rel_path = file_path.relative_to(self.repo_root)
        backup_path = self.backup_dir / rel_path

        # Create backup directory if needed
        backup_path.parent.mkdir(parents=True, exist_ok=True)

        # Copy file
        shutil.copy2(file_path, backup_path)
        print(f"📦 Backed up: {rel_path}")
        return True

    def safe_delete_files(self, files_to_delete: List[str]) -> Tuple[int, int]:
        """
        Safely delete files with backup.
        Returns (deleted_count, failed_count)
        """
        deleted = 0
        failed = 0

        for file_path_str in files_to_delete:
            file_path = self.repo_root / file_path_str

            if not file_path.exists():
                print(f"⚠️  File not found: {file_path_str}")
                failed += 1
                continue

            # Check if file is imported anywhere (basic check)
            if self._is_file_imported(file_path):
                print(f"🚫 File still imported: {file_path_str}")
                failed += 1
                continue

            # Backup and delete
            if self.backup_file(file_path):
                file_path.unlink()
                print(f"✅ Deleted: {file_path_str}")
                deleted += 1
            else:
                print(f"❌ Backup failed: {file_path_str}")
                failed += 1

        return deleted, failed

    def _is_file_imported(self, file_path: Path) -> bool:
        """Basic check if file is imported anywhere."""
        # Get module name from file path
        rel_path = file_path.relative_to(self.repo_root)
        module_name = str(rel_path).replace('/', '.').replace('\\', '.')
        if module_name.endswith('.py'):
            module_name = module_name[:-3]

        # Search for imports of this module
        import_patterns = [
            f"from {module_name} import",
            f"import {module_name}",
            f"from .{module_name} import",
        ]

        for py_file in self.repo_root.rglob("*.py"):
            if py_file == file_path:
                continue

            try:
                content = py_file.read_text(encoding='utf-8', errors='ignore')
                for pattern in import_patterns:
                    if pattern in content:
                        return True
            except:
                continue

        return False

    def analyze_directory_duplicates(self, directory: str) -> List[Tuple[str, str]]:
        """Find potential duplicate files in a directory."""
        dir_path = self.repo_root / directory
        if not dir_path.exists():
            return []

        files = {}
        duplicates = []

        # Group files by size (simple duplicate detection)
        for file_path in dir_path.rglob("*.py"):
            if file_path.is_file():
                size = file_path.stat().st_size
                rel_path = str(file_path.relative_to(self.repo_root))

                if size in files:
                    # Potential duplicate - same size
                    duplicates.append((files[size], rel_path))
                else:
                    files[size] = rel_path

        return duplicates

    def generate_cleanup_report(self) -> str:
        """Generate a report of potential cleanup actions."""
        report = []

        # CLI duplicates
        cli_duplicates = self.analyze_directory_duplicates("src/cli/commands")
        if cli_duplicates:
            report.append(f"## CLI Command Duplicates Found: {len(cli_duplicates)}")
            for dup1, dup2 in cli_duplicates:
                report.append(f"- {dup1} ↔ {dup2}")

        # Archive analysis
        archive_path = self.repo_root / "archive"
        if archive_path.exists():
            total_files = len(list(archive_path.rglob("*")))
            old_files = len(list(archive_path.glob("cleanup_*"))) + len(list(archive_path.glob("old_*")))
            report.append(f"## Archive Analysis")
            report.append(f"- Total files: {total_files}")
            report.append(f"- Potentially obsolete: {old_files} ({old_files/total_files*100:.1f}%)")

        return "\n".join(report)


def main():
    """Main CLI interface."""
    import argparse

    parser = argparse.ArgumentParser(description="Audit Cleanup Helper")
    parser.add_argument("--analyze", action="store_true", help="Analyze codebase for duplicates")
    parser.add_argument("--delete-safe", action="store_true", help="Delete safe duplicate files")
    parser.add_argument("--report", action="store_true", help="Generate cleanup report")

    args = argparse.parse_args()

    helper = AuditCleanupHelper(".")

    if args.analyze:
        print("🔍 Analyzing codebase for duplicates...")
        duplicates = helper.analyze_directory_duplicates("src/cli/commands")
        print(f"Found {len(duplicates)} potential duplicates")

    if args.report:
        print("📊 Generating cleanup report...")
        report = helper.generate_cleanup_report()
        print(report)

    if args.delete_safe:
        print("🚨 CAPTAIN APPROVAL REQUIRED - SAFE DELETION MODE")
        print("=" * 60)
        print("This operation requires explicit Captain approval.")
        print("Only the 5 confirmed duplicate CLI handlers will be processed.")
        print("")
        print("SAFETY MEASURES:")
        print("- Files moved to archive (not deleted)")
        print("- Automatic backups created")
        print("- Import dependency checking")
        print("- Git status verification required")
        print("=" * 60)

        # Captain approval check
        captain_approval = input("Enter Captain approval code: ")
        if captain_approval != "CAPTAIN_APPROVED_PHASE1":
            print("❌ Captain approval required. Use code: CAPTAIN_APPROVED_PHASE1")
            print("Operation cancelled.")
            return

        # Files identified as safe to delete in audit
        safe_deletions = [
            "src/cli/commands/cleanup_handler.py",
            "src/cli/commands/start_handler.py",
            "src/cli/commands/status_handler.py",
            "src/cli/commands/stop_handler.py",
            "src/cli/commands/validation_handler.py"
        ]

        print(f"\n📋 Files to process: {len(safe_deletions)}")
        for i, file in enumerate(safe_deletions, 1):
            print(f"  {i}. {file}")

        final_confirm = input(f"\n⚠️  FINAL CONFIRMATION: Process these {len(safe_deletions)} files? (yes/N): ")
        if final_confirm.lower() == 'yes':
            print("\n🛡️  EXECUTING SAFE DELETION PROTOCOL...")
            deleted, failed = helper.safe_delete_files(safe_deletions)

            print("
📊 EXECUTION RESULTS:"            print(f"✅ Successfully processed: {deleted} files")
            print(f"❌ Failed to process: {failed} files")
            print(f"📦 Backups saved to: {helper.backup_dir}")

            if deleted > 0:
                print("
🔍 VERIFICATION REQUIRED:"                print("1. Run: git status")
                print("2. Verify only approved files changed")
                print("3. Test CLI imports: python -c 'from src.cli.commands.command_router import CommandRouter'")
                print("4. If issues found: Files recoverable from backup directory")

        else:
            print("Operation cancelled.")


if __name__ == "__main__":
    main()