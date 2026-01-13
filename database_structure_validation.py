#!/usr/bin/env python3
"""
Database Structure Validation Script
====================================

Validates database structures across the system including:
- SQLite databases (persistence, trader replay)
- Vector databases (ChromaDB/LocalVectorStore)
- Message deduplication data
- Schema integrity and data freshness

Part of Agent-6 coordination: Database validation and QA automation
Author: Agent-1 (Integration & Core Systems Specialist)
Created: 2026-01-13
"""

import json
import os
import sqlite3
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseValidator:
    """Validates database structures and data integrity."""

    def __init__(self, base_path: str = "D:\\Agent_Cellphone_V2_Repository"):
        self.base_path = Path(base_path)
        self.validation_results = {
            "timestamp": datetime.now().isoformat(),
            "databases": {},
            "issues": [],
            "recommendations": []
        }

    def validate_all_databases(self) -> Dict[str, Any]:
        """Run complete database validation."""
        logger.info("🔍 Starting comprehensive database validation...")

        # Validate SQLite databases
        self._validate_sqlite_databases()

        # Validate vector databases
        self._validate_vector_databases()

        # Validate message deduplication
        self._validate_message_deduplication()

        # Validate data freshness
        self._validate_data_freshness()

        # Generate summary
        self._generate_validation_summary()

        return self.validation_results

    def _validate_sqlite_databases(self):
        """Validate SQLite database structures."""
        logger.info("📊 Validating SQLite databases...")

        # Check main persistence database
        persistence_db = self.base_path / "data" / "unified.db"
        if persistence_db.exists():
            self._validate_persistence_database(persistence_db)
        else:
            self.validation_results["issues"].append({
                "type": "missing_database",
                "database": "persistence",
                "path": str(persistence_db),
                "severity": "medium"
            })

        # Check trader replay database
        trader_db = self.base_path / "src" / "services" / "trader_replay" / "trader_replay.db"
        if trader_db.exists():
            self._validate_trader_replay_database(trader_db)
        else:
            # Trader database might be optional
            logger.info("ℹ️ Trader replay database not found (may be optional)")

    def _validate_persistence_database(self, db_path: Path):
        """Validate main persistence database."""
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()

            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            db_info = {
                "path": str(db_path),
                "tables": [table[0] for table in tables],
                "table_details": {},
                "integrity_check": "pending"
            }

            # Check each table
            for table_name, in tables:
                self._validate_table_structure(cursor, table_name, db_info)

            # Run integrity check
            cursor.execute("PRAGMA integrity_check;")
            integrity_result = cursor.fetchone()
            db_info["integrity_check"] = integrity_result[0] if integrity_result else "unknown"

            if integrity_result and integrity_result[0] != "ok":
                self.validation_results["issues"].append({
                    "type": "integrity_failure",
                    "database": "persistence",
                    "table": "database",
                    "details": integrity_result[0],
                    "severity": "high"
                })

            conn.close()
            self.validation_results["databases"]["persistence"] = db_info

        except Exception as e:
            logger.error(f"❌ Failed to validate persistence database: {e}")
            self.validation_results["issues"].append({
                "type": "validation_error",
                "database": "persistence",
                "error": str(e),
                "severity": "high"
            })

    def _validate_table_structure(self, cursor, table_name: str, db_info: Dict):
        """Validate individual table structure."""
        try:
            # Get table info
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()

            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            row_count = cursor.fetchone()[0]

            table_info = {
                "columns": len(columns),
                "column_details": [
                    {
                        "name": col[1],
                        "type": col[2],
                        "nullable": not col[3],
                        "default": col[4],
                        "primary_key": bool(col[5])
                    } for col in columns
                ],
                "row_count": row_count
            }

            db_info["table_details"][table_name] = table_info

        except Exception as e:
            logger.warning(f"⚠️ Failed to validate table {table_name}: {e}")

    def _validate_trader_replay_database(self, db_path: Path):
        """Validate trader replay database against expected schema."""
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()

            expected_tables = ["symbols", "sessions", "candles", "paper_trades", "journal_entries", "scores", "session_summaries"]

            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            actual_tables = [table[0] for table in cursor.fetchall()]

            db_info = {
                "path": str(db_path),
                "expected_tables": expected_tables,
                "actual_tables": actual_tables,
                "missing_tables": [t for t in expected_tables if t not in actual_tables],
                "extra_tables": [t for t in actual_tables if t not in expected_tables],
                "table_validation": {}
            }

            # Validate each expected table
            for table in expected_tables:
                if table in actual_tables:
                    self._validate_trader_table(cursor, table, db_info)

            # Check data freshness
            self._check_trader_data_freshness(cursor, db_info)

            conn.close()
            self.validation_results["databases"]["trader_replay"] = db_info

        except Exception as e:
            logger.error(f"❌ Failed to validate trader replay database: {e}")
            self.validation_results["issues"].append({
                "type": "validation_error",
                "database": "trader_replay",
                "error": str(e),
                "severity": "high"
            })

    def _validate_trader_table(self, cursor, table_name: str, db_info: Dict):
        """Validate trader table structure and data."""
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            row_count = cursor.fetchone()[0]

            db_info["table_validation"][table_name] = {
                "exists": True,
                "row_count": row_count,
                "status": "valid"
            }

        except Exception as e:
            db_info["table_validation"][table_name] = {
                "exists": True,
                "error": str(e),
                "status": "error"
            }

    def _check_trader_data_freshness(self, cursor, db_info: Dict):
        """Check data freshness in trader database."""
        try:
            # Check latest session date
            cursor.execute("SELECT MAX(created_at) FROM sessions;")
            latest_session = cursor.fetchone()[0]

            if latest_session:
                # Parse timestamp and check if within last 30 days
                # SQLite timestamps are usually in ISO format
                latest_dt = datetime.fromisoformat(latest_session.replace('Z', '+00:00'))
                days_old = (datetime.now() - latest_dt).days

                db_info["data_freshness"] = {
                    "latest_session": latest_session,
                    "days_since_update": days_old,
                    "status": "fresh" if days_old < 30 else "stale"
                }

                if days_old >= 30:
                    self.validation_results["issues"].append({
                        "type": "stale_data",
                        "database": "trader_replay",
                        "details": f"Latest session is {days_old} days old",
                        "severity": "medium"
                    })
            else:
                db_info["data_freshness"] = {
                    "status": "no_data"
                }

        except Exception as e:
            logger.warning(f"⚠️ Failed to check trader data freshness: {e}")

    def _validate_vector_databases(self):
        """Validate vector database configurations."""
        logger.info("🔍 Validating vector databases...")

        # Check for ChromaDB data
        chroma_path = self.base_path / "data" / "chroma"
        if chroma_path.exists():
            self._validate_chromadb(chroma_path)

        # Check for LocalVectorStore data
        vector_store_path = self.base_path / "data" / "vector_store"
        if vector_store_path.exists():
            self._validate_local_vector_store(vector_store_path)

        # Check if vector database service is importable
        try:
            from src.services.vector_database_service_unified import VECTOR_DATABASE_AVAILABLE
            self.validation_results["databases"]["vector_service"] = {
                "available": VECTOR_DATABASE_AVAILABLE,
                "status": "operational" if VECTOR_DATABASE_AVAILABLE else "fallback_mode"
            }
        except ImportError as e:
            self.validation_results["issues"].append({
                "type": "import_error",
                "component": "vector_database_service",
                "error": str(e),
                "severity": "medium"
            })

    def _validate_chromadb(self, chroma_path: Path):
        """Validate ChromaDB instance."""
        try:
            collections = []
            if chroma_path.is_dir():
                for item in chroma_path.iterdir():
                    if item.is_dir():
                        collections.append(item.name)

            self.validation_results["databases"]["chromadb"] = {
                "path": str(chroma_path),
                "collections": collections,
                "collection_count": len(collections),
                "status": "configured"
            }

        except Exception as e:
            logger.warning(f"⚠️ Failed to validate ChromaDB: {e}")

    def _validate_local_vector_store(self, vector_store_path: Path):
        """Validate LocalVectorStore data."""
        try:
            files = list(vector_store_path.glob("*.json"))
            self.validation_results["databases"]["local_vector_store"] = {
                "path": str(vector_store_path),
                "files": len(files),
                "status": "available"
            }

        except Exception as e:
            logger.warning(f"⚠️ Failed to validate LocalVectorStore: {e}")

    def _validate_message_deduplication(self):
        """Validate message deduplication data."""
        logger.info("📋 Validating message deduplication...")

        dedup_file = self.base_path / "data" / "message_deduplication.json"
        if dedup_file.exists():
            try:
                with open(dedup_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                message_count = len(data)
                if message_count > 0:
                    # Check timestamps for freshness
                    timestamps = [float(ts) for ts in data.values()]
                    oldest = min(timestamps)
                    newest = max(timestamps)

                    days_span = (newest - oldest) / (24 * 3600)
                    avg_per_day = message_count / max(days_span, 1)

                    self.validation_results["databases"]["message_deduplication"] = {
                        "file": str(dedup_file),
                        "message_count": message_count,
                        "oldest_timestamp": oldest,
                        "newest_timestamp": newest,
                        "days_span": round(days_span, 2),
                        "avg_messages_per_day": round(avg_per_day, 2),
                        "status": "active"
                    }

                    # Check if data is too old
                    days_since_update = (time.time() - newest) / (24 * 3600)
                    if days_since_update > 7:
                        self.validation_results["issues"].append({
                            "type": "stale_deduplication_data",
                            "details": f"Last deduplication entry is {days_since_update:.1f} days old",
                            "severity": "low"
                        })

                else:
                    self.validation_results["databases"]["message_deduplication"] = {
                        "status": "empty"
                    }

            except Exception as e:
                logger.error(f"❌ Failed to validate message deduplication: {e}")
                self.validation_results["issues"].append({
                    "type": "validation_error",
                    "component": "message_deduplication",
                    "error": str(e),
                    "severity": "medium"
                })
        else:
            logger.info("ℹ️ Message deduplication file not found")

    def _validate_data_freshness(self):
        """Validate overall data freshness across systems."""
        logger.info("⏰ Validating data freshness...")

        # Check coordination cache freshness
        coord_cache = self.base_path / "coordination_cache.json"
        if coord_cache.exists():
            try:
                with open(coord_cache, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                all_timestamps = []
                for agent_pair, timestamps in data.items():
                    all_timestamps.extend(timestamps)

                if all_timestamps:
                    latest_timestamp = max(all_timestamps)
                    hours_old = (time.time() - latest_timestamp) / 3600

                    self.validation_results["data_freshness"] = {
                        "latest_coordination": latest_timestamp,
                        "hours_since_last_activity": round(hours_old, 2),
                        "status": "active" if hours_old < 24 else "stale"
                    }

                    if hours_old > 48:
                        self.validation_results["issues"].append({
                            "type": "inactive_coordination",
                            "details": f"No coordination activity for {hours_old:.1f} hours",
                            "severity": "medium"
                        })

            except Exception as e:
                logger.warning(f"⚠️ Failed to check coordination freshness: {e}")

    def _generate_validation_summary(self):
        """Generate validation summary and recommendations."""
        total_issues = len(self.validation_results["issues"])
        high_priority = sum(1 for issue in self.validation_results["issues"] if issue["severity"] == "high")
        medium_priority = sum(1 for issue in self.validation_results["issues"] if issue["severity"] == "medium")

        self.validation_results["summary"] = {
            "total_databases_checked": len(self.validation_results["databases"]),
            "total_issues": total_issues,
            "high_priority_issues": high_priority,
            "medium_priority_issues": medium_priority,
            "low_priority_issues": total_issues - high_priority - medium_priority,
            "overall_status": "healthy" if high_priority == 0 else "needs_attention" if medium_priority <= 2 else "critical"
        }

        # Generate recommendations based on issues
        if high_priority > 0:
            self.validation_results["recommendations"].append("🚨 Address high-priority issues immediately")
        if medium_priority > 0:
            self.validation_results["recommendations"].append("⚠️ Review and resolve medium-priority issues")
        if total_issues == 0:
            self.validation_results["recommendations"].append("✅ All databases validated successfully")

        # Add specific recommendations
        for issue in self.validation_results["issues"]:
            if issue["type"] == "missing_database":
                self.validation_results["recommendations"].append(f"Create missing database: {issue['database']}")
            elif issue["type"] == "integrity_failure":
                self.validation_results["recommendations"].append(f"Repair database integrity: {issue['database']}")
            elif issue["type"] == "stale_data":
                self.validation_results["recommendations"].append(f"Update stale data in: {issue['database']}")


def main():
    """Run database validation."""
    print("🔍 Database Structure Validation")
    print("=" * 50)

    validator = DatabaseValidator()
    results = validator.validate_all_databases()

    # Print summary
    summary = results["summary"]
    print("\n📊 VALIDATION SUMMARY:")
    print(f"Databases checked: {summary['total_databases_checked']}")
    print(f"Total issues: {summary['total_issues']}")
    print(f"High priority: {summary['high_priority_issues']}")
    print(f"Medium priority: {summary['medium_priority_issues']}")
    print(f"Low priority: {summary['low_priority_issues']}")
    print(f"Overall status: {summary['overall_status'].upper()}")

    if results["issues"]:
        print("\n🚨 ISSUES FOUND:")
        for i, issue in enumerate(results["issues"], 1):
            severity_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(issue["severity"], "⚪")
            print(f"{i}. {severity_emoji} {issue['type']}: {issue.get('details', issue.get('database', 'Unknown'))}")

    if results["recommendations"]:
        print("\n💡 RECOMMENDATIONS:")
        for rec in results["recommendations"]:
            print(f"• {rec}")

    # Save detailed results
    output_file = "database_validation_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n📄 Detailed results saved to: {output_file}")
    print("\n✅ Database validation completed!")


if __name__ == "__main__":
    main()