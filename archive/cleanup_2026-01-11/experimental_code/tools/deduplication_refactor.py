#!/usr/bin/env python3
"""
Code Deduplication Refactor Tool
================================

Automatically refactors repetitive code patterns using the base classes and utilities.

V2 Compliance: Automated refactoring tool for code quality
Author: Agent-3 - Infrastructure & DevOps Specialist
"""

import re
import ast
from pathlib import Path
from typing import Dict, List, Set
from dataclasses import dataclass

@dataclass
class RefactorPattern:
    """Represents a refactoring pattern."""
    name: str
    pattern: str
    replacement: str
    imports_needed: List[str]
    description: str

class CodeDeduplicationRefactor:
    """Automated code deduplication refactorer."""

    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.refactor_patterns = self._define_patterns()

    def _define_patterns(self) -> List[RefactorPattern]:
        """Define refactoring patterns."""
        return [
            RefactorPattern(
                name="logger_initialization",
                pattern=r'self\.logger\s*=\s*logging\.getLogger\(__name__\)',
                replacement="",  # Remove - handled by base class
                imports_needed=[],
                description="Remove logger initialization - handled by BaseDiscordCog"
            ),
            RefactorPattern(
                name="command_logging",
                pattern=r'self\.logger\.info\(f"Command \'([^\']+)\' triggered by \{ctx\.author\}"\)',
                replacement="",  # Remove - handled by command_template decorator
                imports_needed=[],
                description="Remove command logging - handled by @command_template decorator"
            ),
            RefactorPattern(
                name="error_handling_block",
                pattern=r'(\s+)try:\s*\n(?:\s*\n)*((?:\s+.*\n)+?)(\s+)except Exception as e:\s*\n(\s+)self\.logger\.error\(f"Error in ([^\s]+) command: \{e\}", exc_info=True\)\s*\n(\s+)await ctx\.send\(f"❌ Error: \{e\}"\)',
                replacement=r'\3@command_template()\n\1async def \5(self, ctx: commands.Context',
                imports_needed=["from .command_base import command_template"],
                description="Replace manual error handling with @command_template decorator"
            ),
            RefactorPattern(
                name="embed_creation_simple",
                pattern=r'embed = discord\.Embed\(\s*title="([^"]+)",\s*description="([^"]*)",\s*color=discord\.Color\.(\w+),\s*\)',
                replacement=r'embed = self.create_\3_embed("\1", "\2")',
                imports_needed=[],
                description="Replace manual embed creation with helper methods"
            ),
            RefactorPattern(
                name="role_decorator_consolidation",
                pattern=r'@commands\.has_any_role\("Admin", "Captain", "Swarm Commander"\)',
                replacement=r'@RoleDecorators.admin_or_captain()',
                imports_needed=["from .command_base import RoleDecorators"],
                description="Use centralized role decorators"
            )
        ]

    def refactor_file(self, file_path: Path) -> bool:
        """Refactor a single file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
        except Exception as e:
            print(f"❌ Could not read {file_path}: {e}")
            return False

        content = original_content
        changes_made = 0
        imports_added = set()

        # Apply each pattern
        for pattern in self.refactor_patterns:
            matches = re.findall(pattern.pattern, content, re.MULTILINE | re.DOTALL)
            if matches:
                print(f"🔧 Applying {pattern.name}: {len(matches)} matches in {file_path.name}")

                # Replace content
                content = re.sub(pattern.pattern, pattern.replacement, content,
                               flags=re.MULTILINE | re.DOTALL)

                # Track imports needed
                imports_added.update(pattern.imports_needed)
                changes_made += len(matches)

        # Add necessary imports
        if imports_added:
            content = self._add_imports(content, list(imports_added))

        # Update class inheritance if needed
        if "commands.Cog" in content and "BaseDiscordCog" not in content:
            content = self._update_class_inheritance(content)

        # Write back if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Refactored {file_path.name}: {changes_made} changes made")
            return True

        return False

    def _add_imports(self, content: str, imports: List[str]) -> str:
        """Add necessary imports to the file."""
        # Find existing import section
        lines = content.split('\n')
        import_end = 0

        for i, line in enumerate(lines):
            if line.startswith('import ') or line.startswith('from '):
                import_end = i + 1
            elif import_end > 0 and not line.strip().startswith('#') and line.strip():
                break

        # Add new imports
        for import_stmt in imports:
            if import_stmt not in content:
                lines.insert(import_end, import_stmt)
                import_end += 1
                lines.insert(import_end, "")  # Add blank line

        return '\n'.join(lines)

    def _update_class_inheritance(self, content: str) -> str:
        """Update class inheritance to use BaseDiscordCog."""
        # Simple pattern: replace "commands.Cog" with "BaseDiscordCog"
        content = re.sub(
            r'class\s+(\w+)\([^)]*commands\.Cog[^)]*\):',
            r'class \1(BaseDiscordCog):',
            content
        )

        # Add BaseDiscordCog import if needed
        if 'from .command_base import BaseDiscordCog' not in content:
            content = self._add_imports(content, ['from .command_base import BaseDiscordCog'])

        return content

    def refactor_directory(self, directory: str) -> Dict:
        """Refactor all files in a directory."""
        dir_path = self.base_path / directory
        results = {
            "directory": directory,
            "files_processed": 0,
            "files_changed": 0,
            "total_changes": 0,
            "errors": []
        }

        if not dir_path.exists():
            results["errors"].append(f"Directory {directory} not found")
            return results

        for py_file in dir_path.rglob("*.py"):
            if self._should_refactor_file(py_file):
                results["files_processed"] += 1
                try:
                    if self.refactor_file(py_file):
                        results["files_changed"] += 1
                        results["total_changes"] += 1  # Simplified count
                except Exception as e:
                    results["errors"].append(f"Error refactoring {py_file}: {e}")

        return results

    def _should_refactor_file(self, file_path: Path) -> bool:
        """Determine if a file should be refactored."""
        # Skip certain files
        skip_names = ["__init__.py", "command_base.py", "test_"]
        if any(skip in file_path.name for skip in skip_names):
            return False

        # Only refactor Discord command files initially
        path_str = str(file_path).replace('\\', '/')
        is_command_file = "discord_commander/commands" in path_str
        print(f"Checking {file_path}: {'YES' if is_command_file else 'NO'} (path: {path_str})")
        return is_command_file

    def generate_report(self, directories: List[str]) -> Dict:
        """Generate refactoring report."""
        report = {
            "timestamp": str(Path(__file__).stat().st_mtime),
            "directories_refactored": directories,
            "results": {},
            "summary": {},
            "recommendations": []
        }

        total_processed = 0
        total_changed = 0
        total_changes = 0

        for directory in directories:
            result = self.refactor_directory(directory)
            report["results"][directory] = result
            total_processed += result["files_processed"]
            total_changed += result["files_changed"]
            total_changes += result["total_changes"]

        report["summary"] = {
            "total_directories": len(directories),
            "total_files_processed": total_processed,
            "total_files_changed": total_changed,
            "total_changes_made": total_changes
        }

        return report


def main():
    """Main refactoring function."""
    refactorer = CodeDeduplicationRefactor(Path("."))

    # Start with Discord commands - highest impact area
    directories_to_refactor = [
        "src/discord_commander/commands"
    ]

    print("🔧 Starting automated code deduplication refactoring...")
    print("🎯 Target: Discord command files (highest duplication impact)")

    report = refactorer.generate_report(directories_to_refactor)

    print("\n✅ REFACTORING COMPLETE!")
    print(f"📊 Processed {report['summary']['total_files_processed']} files")
    print(f"🔄 Changed {report['summary']['total_files_changed']} files")
    print(f"⚡ Made {report['summary']['total_changes_made']} deduplication improvements")

    # Show next steps
    print("\n🚀 NEXT STEPS:")
    print("1. Run tests to ensure refactoring didn't break functionality")
    print("2. Review changed files for any manual adjustments needed")
    print("3. Expand refactoring to other high-duplication areas (services, core)")
    print("4. Consider creating shared utilities for common patterns")

    if report["summary"]["total_files_changed"] > 0:
        print(f"\n📝 Files changed: {report['summary']['total_files_changed']}")
        print("💡 Check git diff to review all changes before committing")


if __name__ == "__main__":
    main()