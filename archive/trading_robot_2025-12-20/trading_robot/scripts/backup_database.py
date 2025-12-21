#!/usr/bin/env python3
"""
Database Backup Script
======================

Create database backup.

Usage:
    python scripts/backup_database.py [backup_dir]

Author: Agent-3 (Infrastructure & DevOps Specialist)
Created: 2025-12-20
V2 Compliant: Yes (<400 lines, type hints, documented)
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from loguru import logger
from database.backup import backup_database


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Backup trading robot database")
    parser.add_argument(
        "backup_dir",
        nargs="?",
        type=Path,
        help="Directory to store backup (default: trading_robot/backups)",
    )
    
    args = parser.parse_args()
    
    try:
        backup_file = backup_database(backup_dir=args.backup_dir)
        logger.info(f"✅ Backup complete: {backup_file}")
        return 0
        
    except Exception as e:
        logger.error(f"❌ Backup failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
