#!/usr/bin/env python3
"""
Phase 3: Database Setup Script
==============================

Creates and initializes databases for extracted systems that require them.
Sets up schema and initial data for systems like memory management and gamification.

Run this script from the repository root.
"""

import os
import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Database configurations for each system
DATABASE_CONFIGS = {
    "memory": {
        "path": "systems/memory/data/dreamos_memory.db",
        "schema": {
            "conversations": """
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT UNIQUE NOT NULL,
                    title TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT
                )
            """,
            "messages": """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT,
                    FOREIGN KEY (conversation_id) REFERENCES conversations (conversation_id)
                )
            """,
            "memory_chunks": """
                CREATE TABLE IF NOT EXISTS memory_chunks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT,
                    content TEXT NOT NULL,
                    embedding BLOB,
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversation_id) REFERENCES conversations (conversation_id)
                )
            """
        },
        "initial_data": {}
    },
    "gamification": {
        "path": "systems/gamification/data/dreamos_resume.db",
        "schema": {
            "players": """
                CREATE TABLE IF NOT EXISTS players (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_id TEXT UNIQUE NOT NULL,
                    name TEXT,
                    level INTEGER DEFAULT 1,
                    xp INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            "skills": """
                CREATE TABLE IF NOT EXISTS skills (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_id TEXT NOT NULL,
                    skill_name TEXT NOT NULL,
                    skill_level INTEGER DEFAULT 1,
                    xp INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (player_id) REFERENCES players (player_id)
                )
            """,
            "quests": """
                CREATE TABLE IF NOT EXISTS quests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    quest_id TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    xp_reward INTEGER DEFAULT 0,
                    status TEXT DEFAULT 'available',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
        },
        "initial_data": {
            "players": [
                {
                    "player_id": "default_player",
                    "name": "Default Player",
                    "level": 1,
                    "xp": 0
                }
            ],
            "skills": [
                {
                    "player_id": "default_player",
                    "skill_name": "python_development",
                    "skill_level": 1,
                    "xp": 0
                },
                {
                    "player_id": "default_player",
                    "skill_name": "debugging",
                    "skill_level": 1,
                    "xp": 0
                }
            ]
        }
    },
    "templates": {
        "path": "systems/templates/data/templates.db",
        "schema": {
            "templates": """
                CREATE TABLE IF NOT EXISTS templates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    template_id TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    content TEXT NOT NULL,
                    template_type TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            "template_versions": """
                CREATE TABLE IF NOT EXISTS template_versions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    template_id TEXT NOT NULL,
                    version INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (template_id) REFERENCES templates (template_id)
                )
            """
        },
        "initial_data": {}
    },
    "analytics": {
        "path": "tools/code_analysis/data/tools.db",
        "schema": {
            "tools": """
                CREATE TABLE IF NOT EXISTS tools (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tool_name TEXT UNIQUE NOT NULL,
                    description TEXT,
                    category TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            "tool_usage": """
                CREATE TABLE IF NOT EXISTS tool_usage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tool_name TEXT NOT NULL,
                    usage_count INTEGER DEFAULT 0,
                    last_used TIMESTAMP,
                    metadata TEXT,
                    FOREIGN KEY (tool_name) REFERENCES tools (tool_name)
                )
            """
        },
        "initial_data": {
            "tools": [
                {
                    "tool_name": "code_analyzer",
                    "description": "Analyzes code for patterns and issues",
                    "category": "analysis"
                },
                {
                    "tool_name": "refactor_agent",
                    "description": "Automated code refactoring agent",
                    "category": "refactoring"
                }
            ]
        }
    }
}

def create_database(system_name: str, config: Dict[str, Any]) -> bool:
    """Create a database for a specific system."""
    db_path = config["path"]

    # Ensure directory exists
    db_dir = os.path.dirname(db_path)
    os.makedirs(db_dir, exist_ok=True)

    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        print(f"  📊 Creating database: {db_path}")

        # Create tables
        for table_name, schema_sql in config["schema"].items():
            cursor.execute(schema_sql)
            print(f"    ✅ Created table: {table_name}")

        # Insert initial data
        for table_name, data_list in config["initial_data"].items():
            if data_list:
                print(f"    📝 Inserting initial data for {table_name}")
                for data in data_list:
                    columns = ", ".join(data.keys())
                    placeholders = ", ".join(["?" for _ in data])
                    values = list(data.values())

                    insert_sql = f"INSERT OR IGNORE INTO {table_name} ({columns}) VALUES ({placeholders})"
                    cursor.execute(insert_sql, values)

        # Commit and close
        conn.commit()
        conn.close()

        # Verify database
        if verify_database(db_path, config):
            print(f"  ✅ Database created successfully: {system_name}")
            return True
        else:
            print(f"  ❌ Database verification failed: {system_name}")
            return False

    except Exception as e:
        print(f"  ❌ Failed to create database for {system_name}: {e}")
        return False

def verify_database(db_path: str, config: Dict[str, Any]) -> bool:
    """Verify that a database was created correctly."""
    if not os.path.exists(db_path):
        return False

    try:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        cursor = conn.cursor()

        # Check that all expected tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = {row[0] for row in cursor.fetchall()}

        expected_tables = set(config["schema"].keys())

        if expected_tables.issubset(existing_tables):
            # Check that initial data was inserted
            for table_name in config["initial_data"]:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                if count == 0 and config["initial_data"][table_name]:
                    print(f"    ⚠️  Warning: No data found in {table_name} table")
                elif count > 0:
                    print(f"    ✅ Found {count} records in {table_name}")

            conn.close()
            return True
        else:
            missing_tables = expected_tables - existing_tables
            print(f"    ❌ Missing tables: {missing_tables}")
            conn.close()
            return False

    except Exception as e:
        print(f"  ❌ Database verification error: {e}")
        return False

def create_config_files():
    """Create or update configuration files for database paths."""
    print("\n🔧 Updating Configuration Files...")

    # Memory system config
    memory_config_path = "systems/memory/memory/config.py"
    if not os.path.exists(memory_config_path):
        with open(memory_config_path, 'w') as f:
            f.write("""# Memory system configuration
from pathlib import Path

# Database paths
MEMORY_DB_PATH = Path(__file__).parent.parent / "data" / "dreamos_memory.db"
RESUME_DB_PATH = Path(__file__).parent.parent.parent / "gamification" / "data" / "dreamos_resume.db"
TOOLS_DB_PATH = Path(__file__).parent.parent.parent.parent / "tools" / "code_analysis" / "data" / "tools.db"
TEMPLATES_DB_PATH = Path(__file__).parent.parent.parent / "templates" / "data" / "templates.db"
""")
        print("  ✅ Created memory system config")

    # Gamification config
    gamification_config_path = "systems/gamification/config.py"
    if not os.path.exists(gamification_config_path):
        with open(gamification_config_path, 'w') as f:
            f.write("""# Gamification system configuration
from pathlib import Path

# Database paths
RESUME_DB_PATH = Path(__file__).parent / "data" / "dreamos_resume.db"
MEMORY_DB_PATH = Path(__file__).parent.parent / "memory" / "data" / "dreamos_memory.db"
""")
        print("  ✅ Created gamification system config")

def generate_database_report(results: Dict[str, bool]) -> None:
    """Generate a database setup report."""
    print("\n" + "=" * 60)
    print("🗄️  DATABASE SETUP REPORT")
    print("=" * 60)

    successful = sum(results.values())
    total = len(results)

    print(f"\n📈 SUMMARY: {successful}/{total} databases created successfully")

    print("\n🔍 DATABASE CREATION RESULTS:")
    for system_name, success in results.items():
        status = "✅" if success else "❌"
        config = DATABASE_CONFIGS[system_name]
        db_path = config["path"]
        table_count = len(config["schema"])
        print(f"  {status} {system_name}: {db_path} ({table_count} tables)")

    if successful == total:
        print("\n🎉 ALL DATABASES CREATED SUCCESSFULLY!")
        print("   ✅ Schema initialized")
        print("   ✅ Initial data populated")
        print("   ✅ Configuration files updated")
    else:
        print(f"\n⚠️  {total - successful} databases failed creation")
        print("   🔧 Manual intervention may be required")

    print("\n💡 NEXT STEPS:")
    print("1. Test extracted systems with new databases")
    print("2. Run integration tests to verify connectivity")
    print("3. Populate with real data as systems are used")
    print("4. Set up automated backups for production")

def main():
    """Main database setup function."""
    print("🗄️  Phase 3: Database Setup")
    print("=" * 40)

    results = {}

    for system_name, config in DATABASE_CONFIGS.items():
        print(f"\n🔄 Setting up database for: {system_name}")
        success = create_database(system_name, config)
        results[system_name] = success

    # Update configuration files
    create_config_files()

    # Generate report
    generate_database_report(results)

    print("\n" + "=" * 40)
    print("✅ Phase 3: Database setup complete!")
    print("\nNext: Performance optimization")

if __name__ == "__main__":
    main()