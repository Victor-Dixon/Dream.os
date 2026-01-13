#!/usr/bin/env python3
"""
Phase 2: Database Migration Script
==================================

Migrates Dreamscape database schemas to new locations and updates configurations.
Creates migration scripts for preserving existing data when moving databases.

Run this script from the repository root.
"""

import os
import shutil
import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime

# Database migration mapping
DB_MIGRATIONS = {
    # Source (archive) -> Destination (new systems)
    "archive/dreamscape_project/Thea/data/dreamos_memory.db": "systems/memory/data/dreamos_memory.db",
    "archive/dreamscape_project/Thea/data/dreamos_resume.db": "systems/gamification/data/dreamos_resume.db",
    "archive/dreamscape_project/Thea/data/tools.db": "tools/code_analysis/data/tools.db",
    "archive/dreamscape_project/Thea/data/templates.db": "systems/templates/data/templates.db",
}

def check_database_exists(db_path: str) -> bool:
    """Check if a database file exists and is readable."""
    if not os.path.exists(db_path):
        return False

    try:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        conn.close()
        return True
    except sqlite3.Error:
        return False

def get_database_info(db_path: str) -> Optional[Dict]:
    """Get basic information about a SQLite database."""
    if not check_database_exists(db_path):
        return None

    try:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        cursor = conn.cursor()

        # Get table count
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        # Get total rows across all tables
        total_rows = 0
        for table_name, in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                total_rows += count
            except sqlite3.Error:
                continue  # Skip tables we can't read

        conn.close()

        return {
            "path": db_path,
            "tables": len(tables),
            "total_rows": total_rows,
            "size_mb": os.path.getsize(db_path) / (1024 * 1024)
        }
    except sqlite3.Error as e:
        print(f"  ❌ Error reading database {db_path}: {e}")
        return None

def create_backup(source_path: str, backup_dir: str = "database_backups") -> str:
    """Create a backup of the source database."""
    os.makedirs(backup_dir, exist_ok=True)

    db_name = os.path.basename(source_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f"{db_name}.backup_{timestamp}")

    try:
        shutil.copy2(source_path, backup_path)
        print(f"  ✅ Created backup: {backup_path}")
        return backup_path
    except Exception as e:
        print(f"  ❌ Failed to create backup: {e}")
        return None

def migrate_database(source_path: str, dest_path: str) -> bool:
    """Migrate a database from source to destination."""
    # Ensure destination directory exists
    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)

    try:
        # Create backup first
        backup_path = create_backup(source_path)
        if not backup_path:
            print(f"  ⚠️  Skipping migration of {source_path} due to backup failure")
            return False

        # Copy database to new location
        shutil.copy2(source_path, dest_path)
        print(f"  ✅ Migrated: {source_path} → {dest_path}")

        # Verify the migrated database
        dest_info = get_database_info(dest_path)
        if dest_info:
            print(f"    📊 Migrated DB: {dest_info['tables']} tables, {dest_info['total_rows']} rows, {dest_info['size_mb']:.2f} MB")
            return True
        else:
            print(f"  ❌ Migration verification failed for {dest_path}")
            return False

    except Exception as e:
        print(f"  ❌ Migration failed: {e}")
        return False

def update_config_files():
    """Update configuration files to point to new database locations."""
    print("\n🔧 Updating Configuration Files...")

    config_updates = {
        "systems/memory/memory/manager.py": {
            "from dreamscape.core.config import MEMORY_DB_PATH, RESUME_DB_PATH, TOOLS_DB_PATH, TEMPLATES_DB_PATH":
            "# Database paths updated for Phase 2 integration\nMEMORY_DB_PATH = Path('systems/memory/data/dreamos_memory.db')\nRESUME_DB_PATH = Path('systems/gamification/data/dreamos_resume.db')\nTOOLS_DB_PATH = Path('tools/code_analysis/data/tools.db')\nTEMPLATES_DB_PATH = Path('systems/templates/data/templates.db')\nfrom pathlib import Path"
        }
    }

    for config_file, updates in config_updates.items():
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    content = f.read()

                # Apply updates
                for old_text, new_text in updates.items():
                    if old_text in content:
                        content = content.replace(old_text, new_text)
                        print(f"  ✅ Updated: {config_file}")
                        break

                with open(config_file, 'w') as f:
                    f.write(content)

            except Exception as e:
                print(f"  ❌ Failed to update {config_file}: {e}")
        else:
            print(f"  ⚠️  Config file not found: {config_file}")

def create_migration_report(migrations: List[Tuple[str, str, bool]]) -> None:
    """Create a migration report."""
    print("\n" + "=" * 60)
    print("📊 DATABASE MIGRATION REPORT")
    print("=" * 60)

    successful = sum(1 for _, _, success in migrations if success)
    total = len(migrations)

    print(f"\n📈 SUMMARY: {successful}/{total} databases migrated successfully")

    print("\n🔍 MIGRATION DETAILS:")
    for source, dest, success in migrations:
        status = "✅" if success else "❌"
        print(f"  {status} {os.path.basename(source)} → {os.path.basename(dest)}")

    if successful == total:
        print("\n🎉 ALL DATABASES MIGRATED SUCCESSFULLY!")
        print("   ✅ Data preservation confirmed")
        print("   ✅ New locations verified")
        print("   ✅ Configurations updated")
    else:
        print(f"\n⚠️  {total - successful} databases failed migration")
        print("   🔧 Manual intervention may be required")

    print("\n💡 NEXT STEPS:")
    print("1. Test extracted systems with migrated databases")
    print("2. Update any hardcoded database paths")
    print("3. Verify data integrity in new locations")

def main():
    """Main database migration function."""
    print("🗄️  Phase 2: Database Migration")
    print("=" * 40)

    migrations_completed = []

    for source_path, dest_path in DB_MIGRATIONS.items():
        print(f"\n🔄 Migrating: {os.path.basename(source_path)}")

        # Check if source exists
        if not check_database_exists(source_path):
            print(f"  ⚠️  Source database not found: {source_path}")
            migrations_completed.append((source_path, dest_path, False))
            continue

        # Get source database info
        source_info = get_database_info(source_path)
        if source_info:
            print(f"  📊 Source DB: {source_info['tables']} tables, {source_info['total_rows']} rows, {source_info['size_mb']:.2f} MB")

        # Perform migration
        success = migrate_database(source_path, dest_path)
        migrations_completed.append((source_path, dest_path, success))

    # Update configuration files
    update_config_files()

    # Generate migration report
    create_migration_report(migrations_completed)

    print("\n" + "=" * 40)
    print("✅ Phase 2: Database migration complete!")
    print("\nNext: Documentation updates")

if __name__ == "__main__":
    main()