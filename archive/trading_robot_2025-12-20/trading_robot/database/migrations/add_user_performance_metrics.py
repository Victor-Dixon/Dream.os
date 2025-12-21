#!/usr/bin/env python3
"""
Migration: Add user_performance_metrics table
==============================================

Adds the user_performance_metrics table to the database.

Usage:
    python database/migrations/add_user_performance_metrics.py

Author: Agent-3 (Infrastructure & DevOps Specialist)
Created: 2025-12-20
V2 Compliant: Yes (<400 lines, type hints, documented)
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from loguru import logger
from database.connection import get_db_engine
from database.models import Base, UserPerformanceMetric
from sqlalchemy import inspect


def table_exists(engine, table_name: str) -> bool:
    """Check if a table exists in the database."""
    inspector = inspect(engine)
    return table_name in inspector.get_table_names()


def migrate():
    """Add user_performance_metrics table if it doesn't exist."""
    logger.info("🔄 Starting migration: Add user_performance_metrics table")
    
    try:
        engine = get_db_engine()
        
        # Check if table already exists
        if table_exists(engine, "user_performance_metrics"):
            logger.info("ℹ️  Table 'user_performance_metrics' already exists, skipping migration")
            return True
        
        # Create the table
        logger.info("📊 Creating user_performance_metrics table...")
        UserPerformanceMetric.__table__.create(engine, checkfirst=True)
        
        logger.info("✅ Migration complete: user_performance_metrics table created")
        return True
        
    except Exception as e:
        logger.error(f"❌ Migration failed: {e}")
        return False


def rollback():
    """Rollback migration by dropping the table."""
    logger.warning("⚠️  Rolling back migration: Dropping user_performance_metrics table")
    
    try:
        engine = get_db_engine()
        
        if table_exists(engine, "user_performance_metrics"):
            UserPerformanceMetric.__table__.drop(engine, checkfirst=True)
            logger.info("✅ Rollback complete: user_performance_metrics table dropped")
            return True
        else:
            logger.info("ℹ️  Table 'user_performance_metrics' does not exist, nothing to rollback")
            return True
            
    except Exception as e:
        logger.error(f"❌ Rollback failed: {e}")
        return False


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Migration: Add user_performance_metrics table")
    parser.add_argument(
        "--rollback",
        action="store_true",
        help="Rollback migration (drop table)"
    )
    
    args = parser.parse_args()
    
    if args.rollback:
        success = rollback()
    else:
        success = migrate()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
