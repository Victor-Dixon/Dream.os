#!/usr/bin/env python3
"""
Agent Cellphone V2 - Project Cleanup Script
==========================================

This script cleans up the project structure to make it professional and portable.

Usage:
    python scripts/cleanup_project.py --dry-run    # Preview changes
    python scripts/cleanup_project.py --execute    # Execute cleanup
    python scripts/cleanup_project.py --archive    # Move to archive instead of delete
"""

import os
import shutil
import argparse
from pathlib import Path
from typing import List, Dict, Set
import json


class ProjectCleanup:
    """Professional project cleanup orchestrator."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.archive_dir = project_root / "archive" / "cleanup_2026-01-11"
        self.keep_dirs: Set[str] = {
            "src", "tests", "docs", "scripts", ".github", ".git",
            ".pytest_cache", "__pycache__", ".benchmarks"
        }
        self.keep_files: Set[str] = {
            "README.md", "setup.py", "pyproject.toml", "requirements.txt",
            "MANIFEST.in", "pytest.ini", ".pre-commit-config.yaml",
            "Dockerfile", "docker-compose.yml", "main.py", "env.example",
            ".env.example", ".gitignore", ".gitattributes", "LICENSE",
            "CHANGELOG.md", "CONTRIBUTING.md"
        }

    def analyze_directory(self) -> Dict[str, List[str]]:
        """Analyze current directory structure."""
        analysis = {
            "keep": [],
            "archive": [],
            "delete": [],
            "move_to_src": [],
            "unknown": []
        }

        # Analyze directories
        for item in self.project_root.iterdir():
            if item.is_file():
                continue

            name = item.name

            # Directories to keep
            if name in self.keep_dirs:
                analysis["keep"].append(f"dir: {name}")
                continue

            # Development artifacts to delete
            if name in {
                "cache", "__pycache__", ".pytest_cache", "htmlcov",
                ".mypy_cache", ".benchmarks", "temp", "tmp", ".tmp",
                "node_modules", ".next", "dist", "build"
            }:
                analysis["delete"].append(f"dir: {name}")
                continue

            # Archives and backups
            if name in {
                "archive", "archives", "backup", "backups", "phase3b_backup",
                ".deploy_credentials", "consolidated_repositories", "artifacts"
            } or "backup" in name or "archive" in name:
                analysis["delete"].append(f"dir: {name}")
                continue

            # Experimental/development directories
            if name in {
                "dream", "thea_responses", "session_closures", "fsm_data",
                "stress_test_analysis_results", "validation_results",
                "project_scans", "autonomous_config_reports", "devlogs",
                "migration_package", "temp_repo_analysis", "quarantine",
                "repo_consolidation_groups", "swarm_proposals"
            }:
                analysis["archive"].append(f"dir: {name}")
                continue

            # Agent-related (should be moved to examples or archived)
            if "agent" in name or name in {"agent_workspaces", "agent_messages"}:
                analysis["archive"].append(f"dir: {name}")
                continue

            # Database and data directories
            if name in {
                "database", "chroma_db", "test_chroma", "data", "logs",
                "monitoring", "pids", "schemas", "site_posts", "ssl"
            }:
                analysis["delete"].append(f"dir: {name}")
                continue

            # Service-specific directories
            if name in {
                "mcp_servers", "message_archive", "message_queue", "messaging_v3",
                "money_ops", "nginx", "ops", "packages", "sites", "swarm_brain",
                "systems", "tasks", "tools", "website_data", "websites",
                "infrastructure", "deployment", "extensions", "external"
            }:
                analysis["archive"].append(f"dir: {name}")
                continue

            # Configuration and templates
            if name in {"config", "contracts", "core", "examples", "templates", "test"}:
                analysis["archive"].append(f"dir: {name}")
                continue

            # Unknown directories
            analysis["unknown"].append(f"dir: {name}")

        # Analyze files
        for item in self.project_root.glob("*"):
            if item.is_dir():
                continue

            name = item.name

            # Files to keep
            if name in self.keep_files:
                analysis["keep"].append(f"file: {name}")
                continue

            # Hidden files (mostly keep)
            if name.startswith("."):
                if name in {".env", ".env.backup", ".env.local"}:
                    analysis["delete"].append(f"file: {name}")
                else:
                    analysis["keep"].append(f"file: {name}")
                continue

            # Development artifacts
            if name.endswith((".pyc", ".pyo", ".log", ".tmp", ".bak", ".orig")):
                analysis["delete"].append(f"file: {name}")
                continue

            # JSON and data files
            if name.endswith((".json", ".db", ".sqlite", ".sqlite3")):
                analysis["delete"].append(f"file: {name}")
                continue

            # Unknown files
            analysis["unknown"].append(f"file: {name}")

        return analysis

    def create_archive_structure(self):
        """Create archive directory structure."""
        self.archive_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories
        (self.archive_dir / "experimental_code").mkdir(exist_ok=True)
        (self.archive_dir / "development_artifacts").mkdir(exist_ok=True)
        (self.archive_dir / "agent_workspaces").mkdir(exist_ok=True)
        (self.archive_dir / "service_implementations").mkdir(exist_ok=True)
        (self.archive_dir / "configurations").mkdir(exist_ok=True)

    def move_to_archive(self, path: str, category: str):
        """Move item to appropriate archive category."""
        source = self.project_root / path.split(": ")[1]
        if not source.exists():
            return

        dest_dir = self.archive_dir / category
        dest_dir.mkdir(exist_ok=True)

        try:
            if source.is_file():
                shutil.move(str(source), str(dest_dir / source.name))
            else:
                shutil.move(str(source), str(dest_dir / source.name))
            print(f"📦 Archived {path} to {category}")
        except Exception as e:
            print(f"❌ Failed to archive {path}: {e}")

    def delete_item(self, path: str):
        """Delete an item."""
        item_path = self.project_root / path.split(": ")[1]
        if not item_path.exists():
            return

        try:
            if item_path.is_file():
                item_path.unlink()
            else:
                shutil.rmtree(item_path)
            print(f"🗑️  Deleted {path}")
        except Exception as e:
            print(f"❌ Failed to delete {path}: {e}")

    def execute_cleanup(self, archive: bool = True):
        """Execute the cleanup process."""
        print("🧹 Starting Agent Cellphone V2 Project Cleanup")
        print("=" * 60)

        analysis = self.analyze_directory()

        # Create archive structure
        if archive:
            self.create_archive_structure()

        # Process deletions
        print(f"\n🗑️  Deleting {len(analysis['delete'])} items...")
        for item in analysis["delete"]:
            self.delete_item(item)

        # Process archiving
        if archive:
            print(f"\n📦 Archiving {len(analysis['archive'])} items...")
            for item in analysis["archive"]:
                if "agent" in item:
                    self.move_to_archive(item, "agent_workspaces")
                elif "service" in item or "server" in item:
                    self.move_to_archive(item, "service_implementations")
                elif "config" in item or "template" in item:
                    self.move_to_archive(item, "configurations")
                else:
                    self.move_to_archive(item, "experimental_code")

        # Report unknowns
        if analysis["unknown"]:
            print(f"\n❓ Found {len(analysis['unknown'])} unknown items:")
            for item in analysis["unknown"]:
                print(f"   {item}")

        print("\n✅ Cleanup complete!")
        print(f"📁 Kept {len(analysis['keep'])} essential items")
        print(f"📦 Archived {len(analysis['archive'])} items" if archive else "🚫 Skipped archiving")
        print(f"🗑️  Deleted {len(analysis['delete'])} items")
        print(f"❓ Found {len(analysis['unknown'])} unknown items")

        if archive:
            print(f"\n📂 Archive created at: {self.archive_dir}")

    def preview_cleanup(self):
        """Preview the cleanup without executing it."""
        print("🔍 Agent Cellphone V2 Project Cleanup Preview")
        print("=" * 60)

        analysis = self.analyze_directory()

        print(f"\n✅ Will KEEP ({len(analysis['keep'])} items):")
        for item in analysis["keep"][:10]:  # Show first 10
            print(f"   {item}")
        if len(analysis["keep"]) > 10:
            print(f"   ... and {len(analysis['keep']) - 10} more")

        print(f"\n📦 Will ARCHIVE ({len(analysis['archive'])} items):")
        for item in analysis["archive"][:10]:
            print(f"   {item}")
        if len(analysis["archive"]) > 10:
            print(f"   ... and {len(analysis['archive']) - 10} more")

        print(f"\n🗑️  Will DELETE ({len(analysis['delete'])} items):")
        for item in analysis["delete"][:10]:
            print(f"   {item}")
        if len(analysis["delete"]) > 10:
            print(f"   ... and {len(analysis['delete']) - 10} more")

        if analysis["unknown"]:
            print(f"\n❓ UNKNOWN items ({len(analysis['unknown'])}):")
            for item in analysis["unknown"]:
                print(f"   {item}")

        print("\n💡 Run with --execute to perform cleanup")
        print("💡 Run with --archive to move items to archive instead of deleting")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Agent Cellphone V2 Project Cleanup")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without executing")
    parser.add_argument("--execute", action="store_true", help="Execute the cleanup")
    parser.add_argument("--archive", action="store_true", help="Move items to archive instead of deleting")

    args = parser.parse_args()

    if not any([args.dry_run, args.execute]):
        args.dry_run = True  # Default to dry run

    project_root = Path(__file__).parent.parent
    cleanup = ProjectCleanup(project_root)

    if args.dry_run:
        cleanup.preview_cleanup()
    elif args.execute:
        cleanup.execute_cleanup(archive=args.archive)


if __name__ == "__main__":
    main()