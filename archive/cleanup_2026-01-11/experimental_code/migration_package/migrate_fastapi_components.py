#!/usr/bin/env python3
"""
FastAPI Components Migration Script
===================================

Automates the extraction of FastAPI components from dream.os
to TradingRobotPlug repository.

Usage:
    python migrate_fastapi_components.py --dry-run    # Preview migration
    python migrate_fastapi_components.py --execute    # Execute migration
    python migrate_fastapi_components.py --rollback   # Rollback migration

Author: Agent-2 (Architecture & Design Specialist)
Phase 4 Block 6: Repository Consolidation
"""

import os
import sys
import shutil
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Any

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FastAPIMigrationManager:
    """Manages FastAPI component migration from dream.os to TradingRobotPlug."""

    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.project_root = Path(__file__).parent.parent
        self.migration_package = Path(__file__).parent

        # Files to migrate
        self.files_to_migrate = {
            # Core FastAPI files
            'src/web/trading_results_api.py': 'fastapi_core/trading_results_api.py',
            'src/web/fastapi_app.py': 'fastapi_core/fastapi_app.py',
            'src/web/fastapi_server.py': 'fastapi_core/fastapi_server.py',

            # Trading web services
            'src/web/portfolio_handlers.py': 'web_services/portfolio_handlers.py',
            'src/web/service_integration_routes.py': 'web_services/service_integration_routes.py',
        }

        # Directories to migrate
        self.directories_to_migrate = {
            'src/web/static/js/trading-robot': 'web_services/trading-robot'
        }

        # Import updates needed after migration
        self.import_updates = {
            # Files that import from the migrated components
            'src/services/messaging_cli.py': [
                ('from src.web.trading_results_api import ', 'from trading_robot.api.trading_results import ')
            ],
            'main.py': [
                ('from src.web.fastapi_app import ', 'from trading_robot.web.fastapi_app import ')
            ]
        }

        # Backup location
        self.backup_dir = self.project_root / 'migration_backup'

    def validate_migration_readiness(self) -> Dict[str, Any]:
        """Validate that migration can proceed safely."""
        issues = []
        warnings = []

        # Check if migration package exists
        if not self.migration_package.exists():
            issues.append("Migration package directory not found")

        # Check if target files exist
        for source_file in self.files_to_migrate.keys():
            if not (self.project_root / source_file).exists():
                issues.append(f"Source file missing: {source_file}")

        # Check for TradingRobotPlug repository (placeholder check)
        trading_robot_repo = self.project_root.parent / 'TradingRobotPlug'
        if not trading_robot_repo.exists():
            warnings.append("TradingRobotPlug repository not found - manual migration required")

        # Check for any uncommitted changes
        # This would require git integration

        return {
            'ready': len(issues) == 0,
            'issues': issues,
            'warnings': warnings
        }

    def create_backup(self) -> bool:
        """Create backup of files to be migrated."""
        if self.dry_run:
            logger.info("DRY RUN: Would create backup in migration_backup/")
            return True

        try:
            self.backup_dir.mkdir(exist_ok=True)

            # Backup individual files
            for source_file in self.files_to_migrate.keys():
                source_path = self.project_root / source_file
                if source_path.exists():
                    backup_path = self.backup_dir / source_file
                    backup_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source_path, backup_path)
                    logger.info(f"Backed up: {source_file}")

            # Backup directories
            for source_dir, target_dir in self.directories_to_migrate.items():
                source_path = self.project_root / source_dir
                if source_path.exists():
                    backup_path = self.backup_dir / source_dir
                    if backup_path.exists():
                        shutil.rmtree(backup_path)
                    shutil.copytree(source_path, backup_path)
                    logger.info(f"Backed up directory: {source_dir}")

            logger.info(f"✅ Backup created in {self.backup_dir}")
            return True

        except Exception as e:
            logger.error(f"❌ Backup failed: {e}")
            return False

    def execute_migration(self) -> bool:
        """Execute the migration by removing files from dream.os."""
        if self.dry_run:
            logger.info("DRY RUN: Would remove migrated files from dream.os")
            for source_file in self.files_to_migrate.keys():
                logger.info(f"Would remove: {source_file}")
            for source_dir in self.directories_to_migrate.keys():
                logger.info(f"Would remove directory: {source_dir}")
            return True

        try:
            # Remove individual files
            for source_file in self.files_to_migrate.keys():
                source_path = self.project_root / source_file
                if source_path.exists():
                    source_path.unlink()
                    logger.info(f"Removed: {source_file}")

            # Remove directories
            for source_dir in self.directories_to_migrate.keys():
                source_path = self.project_root / source_dir
                if source_path.exists():
                    shutil.rmtree(source_path)
                    logger.info(f"Removed directory: {source_dir}")

            logger.info("✅ Migration execution completed")
            return True

        except Exception as e:
            logger.error(f"❌ Migration execution failed: {e}")
            return False

    def update_imports(self) -> bool:
        """Update import statements in remaining files."""
        if self.dry_run:
            logger.info("DRY RUN: Would update import statements")
            for file_path, updates in self.import_updates.items():
                logger.info(f"Would update imports in: {file_path}")
                for old_import, new_import in updates:
                    logger.info(f"  {old_import} -> {new_import}")
            return True

        try:
            for file_path, updates in self.import_updates.items():
                full_path = self.project_root / file_path
                if not full_path.exists():
                    logger.warning(f"File not found for import updates: {file_path}")
                    continue

                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                original_content = content

                for old_import, new_import in updates:
                    if old_import in content:
                        content = content.replace(old_import, new_import)
                        logger.info(f"Updated import in {file_path}: {old_import} -> {new_import}")

                if content != original_content:
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    logger.info(f"Saved updated imports in: {file_path}")

            logger.info("✅ Import updates completed")
            return True

        except Exception as e:
            logger.error(f"❌ Import updates failed: {e}")
            return False

    def rollback_migration(self) -> bool:
        """Rollback migration by restoring from backup."""
        if self.dry_run:
            logger.info("DRY RUN: Would restore files from backup")
            return True

        try:
            if not self.backup_dir.exists():
                logger.error("No backup directory found for rollback")
                return False

            # Restore files
            for source_file in self.files_to_migrate.keys():
                backup_path = self.backup_dir / source_file
                target_path = self.project_root / source_file

                if backup_path.exists():
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(backup_path, target_path)
                    logger.info(f"Restored: {source_file}")

            # Restore directories
            for source_dir in self.directories_to_migrate.keys():
                backup_path = self.backup_dir / source_dir
                target_path = self.project_root / source_dir

                if backup_path.exists():
                    if target_path.exists():
                        shutil.rmtree(target_path)
                    shutil.copytree(backup_path, target_path)
                    logger.info(f"Restored directory: {source_dir}")

            logger.info("✅ Rollback completed")
            return True

        except Exception as e:
            logger.error(f"❌ Rollback failed: {e}")
            return False

    def generate_migration_report(self) -> str:
        """Generate a comprehensive migration report."""
        report = []
        report.append("# FastAPI Components Migration Report")
        report.append("=" * 50)
        report.append("")

        # Migration summary
        report.append("## Migration Summary")
        report.append(f"- **Mode:** {'DRY RUN' if self.dry_run else 'EXECUTION'}")
        report.append(f"- **Files to Migrate:** {len(self.files_to_migrate)}")
        report.append(f"- **Directories to Migrate:** {len(self.directories_to_migrate)}")
        report.append(f"- **Import Updates:** {sum(len(updates) for updates in self.import_updates.values())}")
        report.append("")

        # Files being migrated
        report.append("## Files Migrated")
        for source, target in self.files_to_migrate.items():
            report.append(f"- `{source}` → `{target}`")
        report.append("")

        # Directories being migrated
        report.append("## Directories Migrated")
        for source, target in self.directories_to_migrate.items():
            report.append(f"- `{source}` → `{target}`")
        report.append("")

        # Import updates
        report.append("## Import Updates Required")
        for file_path, updates in self.import_updates.items():
            report.append(f"### {file_path}")
            for old_import, new_import in updates:
                report.append(f"- `{old_import.strip()}` → `{new_import.strip()}`")
        report.append("")

        # Validation results
        validation = self.validate_migration_readiness()
        report.append("## Pre-Migration Validation")
        report.append(f"- **Ready to Proceed:** {'✅ Yes' if validation['ready'] else '❌ No'}")
        if validation['issues']:
            report.append("- **Issues:**")
            for issue in validation['issues']:
                report.append(f"  - ❌ {issue}")
        if validation['warnings']:
            report.append("- **Warnings:**")
            for warning in validation['warnings']:
                report.append(f"  - ⚠️ {warning}")
        report.append("")

        # Post-migration steps
        report.append("## Post-Migration Steps")
        report.append("1. **Move Migration Package:** Copy `migration_package/` to TradingRobotPlug repository")
        report.append("2. **Install Dependencies:** Run `pip install -r requirements-fastapi.txt`")
        report.append("3. **Update Configurations:** Update API endpoints and import paths")
        report.append("4. **Integration Testing:** Test all API endpoints and WordPress integrations")
        report.append("5. **Cleanup:** Remove migration package from dream.os")
        report.append("")

        return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description='FastAPI Components Migration Tool')
    parser.add_argument('--dry-run', action='store_true', help='Preview migration without making changes')
    parser.add_argument('--execute', action='store_true', help='Execute the migration')
    parser.add_argument('--rollback', action='store_true', help='Rollback previous migration')
    parser.add_argument('--report', action='store_true', help='Generate migration report')

    args = parser.parse_args()

    if not any([args.dry_run, args.execute, args.rollback, args.report]):
        parser.print_help()
        return

    # Determine mode
    if args.rollback:
        dry_run = False  # Rollback always executes
    else:
        dry_run = args.dry_run

    migration_manager = FastAPIMigrationManager(dry_run=dry_run)

    # Generate report if requested
    if args.report:
        report = migration_manager.generate_migration_report()
        print(report)
        return

    # Validate readiness
    validation = migration_manager.validate_migration_readiness()
    if not validation['ready']:
        logger.error("Migration validation failed:")
        for issue in validation['issues']:
            logger.error(f"  - {issue}")
        sys.exit(1)

    if validation['warnings']:
        logger.warning("Migration warnings:")
        for warning in validation['warnings']:
            logger.warning(f"  - {warning}")

    # Execute operation
    if args.rollback:
        logger.info("🔄 Starting migration rollback...")
        success = migration_manager.rollback_migration()
    else:
        logger.info(f"{'🔍 DRY RUN:' if dry_run else '🚀 EXECUTING:'} FastAPI Components Migration")
        logger.info("Step 1: Creating backup...")
        if not migration_manager.create_backup():
            sys.exit(1)

        logger.info("Step 2: Executing migration...")
        if not migration_manager.execute_migration():
            sys.exit(1)

        logger.info("Step 3: Updating imports...")
        if not migration_manager.update_imports():
            sys.exit(1)

        success = True

    if success:
        logger.info("✅ Migration completed successfully!")
        if dry_run:
            logger.info("Run with --execute to perform actual migration")
    else:
        logger.error("❌ Migration failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()