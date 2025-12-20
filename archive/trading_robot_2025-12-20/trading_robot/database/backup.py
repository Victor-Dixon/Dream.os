"""
Database Backup and Restore Utilities
======================================

Provides database backup and restore functionality for both
SQLite and PostgreSQL databases.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Created: 2025-12-20
V2 Compliant: Yes (<400 lines, type hints, documented)
"""

from datetime import datetime
from pathlib import Path
from typing import Optional
import shutil
import subprocess
from loguru import logger

from config.settings import config


def backup_database(backup_dir: Optional[Path] = None) -> Path:
    """
    Create database backup.
    
    Args:
        backup_dir: Directory to store backup (default: trading_robot/backups)
        
    Returns:
        Path to backup file
        
    Raises:
        Exception: If backup fails
    """
    database_url = config.database_url
    
    # Determine backup directory
    if backup_dir is None:
        backup_dir = Path(__file__).parent.parent / "backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate backup filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    try:
        if database_url.startswith("sqlite"):
            # SQLite backup (copy file)
            db_path = database_url.replace("sqlite:///", "")
            db_file = Path(db_path)
            
            if not db_file.exists():
                logger.warning(f"⚠️  Database file not found: {db_file}")
                # Create empty database for backup structure
                from database.connection import init_database
                init_database()
            
            backup_file = backup_dir / f"trading_robot_{timestamp}.db"
            shutil.copy2(db_file, backup_file)
            logger.info(f"✅ SQLite backup created: {backup_file}")
            
        elif database_url.startswith("postgresql"):
            # PostgreSQL backup using pg_dump
            backup_file = backup_dir / f"trading_robot_{timestamp}.sql"
            
            # Extract connection details from URL
            # Format: postgresql://user:pass@host:port/dbname
            url_parts = database_url.replace("postgresql://", "").split("/")
            db_name = url_parts[-1]
            auth_host = url_parts[0].split("@")
            
            if len(auth_host) == 2:
                user_pass = auth_host[0].split(":")
                user = user_pass[0]
                password = user_pass[1] if len(user_pass) > 1 else ""
                host_port = auth_host[1].split(":")
                host = host_port[0]
                port = host_port[1] if len(host_port) > 1 else "5432"
            else:
                raise ValueError("Invalid PostgreSQL connection string")
            
            # Set password via environment variable
            env = {"PGPASSWORD": password}
            
            # Run pg_dump
            cmd = [
                "pg_dump",
                "-h", host,
                "-p", port,
                "-U", user,
                "-d", db_name,
                "-F", "c",  # Custom format
                "-f", str(backup_file),
            ]
            
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise RuntimeError(f"pg_dump failed: {result.stderr}")
            
            logger.info(f"✅ PostgreSQL backup created: {backup_file}")
        
        else:
            raise ValueError(f"Unsupported database type: {database_url}")
        
        logger.info(f"📦 Backup size: {backup_file.stat().st_size / 1024:.2f} KB")
        return backup_file
        
    except Exception as e:
        logger.error(f"❌ Database backup failed: {e}")
        raise


def restore_database(backup_file: Path, confirm: bool = False) -> None:
    """
    Restore database from backup.
    
    Args:
        backup_file: Path to backup file
        confirm: If True, skip confirmation prompt (for automation)
        
    Raises:
        Exception: If restore fails
    """
    if not backup_file.exists():
        raise FileNotFoundError(f"Backup file not found: {backup_file}")
    
    if not confirm:
        logger.warning("⚠️  Restore will overwrite existing database!")
        response = input("Continue? (yes/no): ")
        if response.lower() != "yes":
            logger.info("Restore cancelled")
            return
    
    database_url = config.database_url
    
    try:
        if database_url.startswith("sqlite"):
            # SQLite restore (copy file)
            db_path = database_url.replace("sqlite:///", "")
            db_file = Path(db_path)
            
            # Backup current database if it exists
            if db_file.exists():
                old_backup = db_file.with_suffix(".db.old")
                shutil.copy2(db_file, old_backup)
                logger.info(f"📦 Current database backed up to: {old_backup}")
            
            shutil.copy2(backup_file, db_file)
            logger.info(f"✅ SQLite database restored from: {backup_file}")
            
        elif database_url.startswith("postgresql"):
            # PostgreSQL restore using pg_restore
            url_parts = database_url.replace("postgresql://", "").split("/")
            db_name = url_parts[-1]
            auth_host = url_parts[0].split("@")
            
            if len(auth_host) == 2:
                user_pass = auth_host[0].split(":")
                user = user_pass[0]
                password = user_pass[1] if len(user_pass) > 1 else ""
                host_port = auth_host[1].split(":")
                host = host_port[0]
                port = host_port[1] if len(host_port) > 1 else "5432"
            else:
                raise ValueError("Invalid PostgreSQL connection string")
            
            env = {"PGPASSWORD": password}
            
            cmd = [
                "pg_restore",
                "-h", host,
                "-p", port,
                "-U", user,
                "-d", db_name,
                "-c",  # Clean (drop) existing objects
                str(backup_file),
            ]
            
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise RuntimeError(f"pg_restore failed: {result.stderr}")
            
            logger.info(f"✅ PostgreSQL database restored from: {backup_file}")
        
        else:
            raise ValueError(f"Unsupported database type: {database_url}")
        
    except Exception as e:
        logger.error(f"❌ Database restore failed: {e}")
        raise
