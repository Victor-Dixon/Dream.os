#!/usr/bin/env python3
"""
Database Initialization Script
===============================

Initialize trading robot database: create tables, test connection.

Usage:
    python scripts/init_database.py

Author: Agent-3 (Infrastructure & DevOps Specialist)
Created: 2025-12-20
V2 Compliant: Yes (<400 lines, type hints, documented)
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from loguru import logger
from config.settings import config
from database.connection import init_database, test_database_connection


def main():
    """Main function."""
    logger.info("🚀 Initializing Trading Robot Database...")
    logger.info(f"📍 Database URL: {config.database_url}")
    
    try:
        # Initialize database (create tables)
        init_database(create_tables=True)
        
        # Test connection
        if test_database_connection():
            logger.info("✅ Database initialization complete")
            return 0
        else:
            logger.error("❌ Database connection test failed")
            return 1
            
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
