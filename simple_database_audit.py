#!/usr/bin/env python3
"""
Simple Database Audit Script
============================

Quick audit of database files and structures without complex imports.
Checks file existence, sizes, and basic structure validation.

Part of Agent-6 coordination: Database validation and QA automation
Author: Agent-1 (Integration & Core Systems Specialist)
Created: 2026-01-13
"""

import json
import os
import sqlite3
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def audit_databases():
    """Simple database audit without complex imports."""
    base_path = Path("D:\\Agent_Cellphone_V2_Repository")
    results = {
        "timestamp": datetime.now().isoformat(),
        "audit_type": "simple_filesystem_audit",
        "databases": {},
        "issues": [],
        "recommendations": []
    }

    logger.info("🔍 Starting simple database audit...")

    # Check SQLite databases
    sqlite_paths = [
        base_path / "data" / "unified.db",
        base_path / "src" / "services" / "trader_replay" / "trader_replay.db",
    ]

    for db_path in sqlite_paths:
        audit_sqlite_database(db_path, results)

    # Check vector database directories
    vector_paths = [
        base_path / "data" / "chroma",
        base_path / "data" / "vector_store",
    ]

    for vector_path in vector_paths:
        audit_vector_directory(vector_path, results)

    # Check message deduplication
    dedup_file = base_path / "data" / "message_deduplication.json"
    audit_deduplication_file(dedup_file, results)

    # Check coordination cache
    coord_file = base_path / "coordination_cache.json"
    audit_coordination_cache(coord_file, results)

    # Generate summary
    generate_audit_summary(results)

    return results


def audit_sqlite_database(db_path: Path, results: Dict[str, Any]):
    """Audit SQLite database file."""
    db_name = db_path.stem

    if not db_path.exists():
        results["issues"].append({
            "type": "missing_database",
            "database": db_name,
            "path": str(db_path),
            "severity": "medium"
        })
        return

    try:
        # Get file info
        stat = db_path.stat()
        file_size = stat.st_size
        modified_time = datetime.fromtimestamp(stat.st_mtime)

        db_info = {
            "path": str(db_path),
            "exists": True,
            "size_bytes": file_size,
            "size_mb": round(file_size / (1024 * 1024), 2),
            "modified": modified_time.isoformat(),
            "days_since_modified": (datetime.now() - modified_time).days
        }

        # Try to connect and get basic info
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # Get tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        db_info["tables"] = [table[0] for table in tables]
        db_info["table_count"] = len(tables)

        # Get total rows across all tables
        total_rows = 0
        for table_name, in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                count = cursor.fetchone()[0]
                total_rows += count
            except:
                pass  # Skip tables with issues

        db_info["estimated_total_rows"] = total_rows

        # Run integrity check
        cursor.execute("PRAGMA integrity_check;")
        integrity_result = cursor.fetchone()
        db_info["integrity_check"] = integrity_result[0] if integrity_result else "unknown"

        if integrity_result and integrity_result[0] != "ok":
            results["issues"].append({
                "type": "integrity_failure",
                "database": db_name,
                "details": integrity_result[0],
                "severity": "high"
            })

        conn.close()

        results["databases"][db_name] = db_info
        logger.info(f"✅ Audited {db_name}: {len(tables)} tables, {total_rows} rows, {db_info['size_mb']}MB")

    except Exception as e:
        logger.error(f"❌ Failed to audit {db_name}: {e}")
        results["issues"].append({
            "type": "audit_error",
            "database": db_name,
            "error": str(e),
            "severity": "high"
        })


def audit_vector_directory(vector_path: Path, results: Dict[str, Any]):
    """Audit vector database directory."""
    dir_name = vector_path.name

    if not vector_path.exists():
        logger.info(f"ℹ️ Vector directory {dir_name} not found")
        return

    try:
        stat = vector_path.stat()
        dir_info = {
            "path": str(vector_path),
            "type": "directory",
            "size_bytes": get_directory_size(vector_path),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
        }

        if dir_name == "chroma":
            # Count ChromaDB collections
            collections = []
            if vector_path.is_dir():
                for item in vector_path.iterdir():
                    if item.is_dir():
                        collections.append(item.name)
            dir_info["collections"] = collections
            dir_info["collection_count"] = len(collections)
        elif dir_name == "vector_store":
            # Count vector store files
            json_files = list(vector_path.glob("*.json"))
            dir_info["json_files"] = len(json_files)

        results["databases"][dir_name] = dir_info
        logger.info(f"✅ Audited {dir_name}: {dir_info.get('collection_count', dir_info.get('json_files', 0))} items")

    except Exception as e:
        logger.error(f"❌ Failed to audit {dir_name}: {e}")


def audit_deduplication_file(dedup_file: Path, results: Dict[str, Any]):
    """Audit message deduplication file."""
    if not dedup_file.exists():
        logger.info("ℹ️ Message deduplication file not found")
        return

    try:
        stat = dedup_file.stat()
        file_info = {
            "path": str(dedup_file),
            "type": "json_file",
            "size_bytes": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
        }

        # Try to read and analyze
        with open(dedup_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        message_count = len(data)
        file_info["message_count"] = message_count

        if message_count > 0:
            # Check timestamps
            timestamps = [float(ts) for ts in data.values()]
            oldest = min(timestamps)
            newest = max(timestamps)

            days_span = (newest - oldest) / (24 * 3600) if newest > oldest else 0
            days_since_update = (time.time() - newest) / (24 * 3600)

            file_info.update({
                "oldest_timestamp": oldest,
                "newest_timestamp": newest,
                "days_span": round(days_span, 2),
                "days_since_update": round(days_since_update, 2),
                "status": "active" if days_since_update < 7 else "stale"
            })

            if days_since_update > 30:
                results["issues"].append({
                    "type": "stale_deduplication_data",
                    "details": f"Deduplication data is {days_since_update:.1f} days old",
                    "severity": "low"
                })

        results["databases"]["message_deduplication"] = file_info
        logger.info(f"✅ Audited message deduplication: {message_count} messages")

    except Exception as e:
        logger.error(f"❌ Failed to audit deduplication file: {e}")


def audit_coordination_cache(coord_file: Path, results: Dict[str, Any]):
    """Audit coordination cache file."""
    if not coord_file.exists():
        results["issues"].append({
            "type": "missing_coordination_cache",
            "details": "Coordination cache file not found",
            "severity": "medium"
        })
        return

    try:
        stat = coord_file.stat()
        file_info = {
            "path": str(coord_file),
            "type": "json_file",
            "size_bytes": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
        }

        # Analyze coordination data
        with open(coord_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        total_interactions = 0
        agent_pairs = len(data)
        latest_timestamp = 0

        for agent_pair, timestamps in data.items():
            total_interactions += len(timestamps)
            if timestamps:
                latest_timestamp = max(latest_timestamp, max(timestamps))

        hours_since_activity = (time.time() - latest_timestamp) / 3600 if latest_timestamp > 0 else float('inf')

        file_info.update({
            "agent_pairs": agent_pairs,
            "total_interactions": total_interactions,
            "latest_timestamp": latest_timestamp,
            "hours_since_activity": round(hours_since_activity, 2),
            "status": "active" if hours_since_activity < 24 else "inactive"
        })

        if hours_since_activity > 48:
            results["issues"].append({
                "type": "inactive_coordination",
                "details": f"No coordination activity for {hours_since_activity:.1f} hours",
                "severity": "medium"
            })

        results["databases"]["coordination_cache"] = file_info
        logger.info(f"✅ Audited coordination cache: {agent_pairs} pairs, {total_interactions} interactions")

    except Exception as e:
        logger.error(f"❌ Failed to audit coordination cache: {e}")


def get_directory_size(path: Path) -> int:
    """Get total size of directory recursively."""
    total_size = 0
    try:
        for item in path.rglob('*'):
            if item.is_file():
                total_size += item.stat().st_size
    except:
        pass
    return total_size


def generate_audit_summary(results: Dict[str, Any]):
    """Generate audit summary and recommendations."""
    total_databases = len(results["databases"])
    total_issues = len(results["issues"])

    high_priority = sum(1 for issue in results["issues"] if issue["severity"] == "high")
    medium_priority = sum(1 for issue in results["issues"] if issue["severity"] == "medium")
    low_priority = sum(1 for issue in results["issues"] if issue["severity"] == "low")

    results["summary"] = {
        "total_databases_checked": total_databases,
        "total_issues": total_issues,
        "high_priority_issues": high_priority,
        "medium_priority_issues": medium_priority,
        "low_priority_issues": low_priority,
        "overall_status": "healthy" if high_priority == 0 else "needs_attention" if medium_priority <= 2 else "critical"
    }

    # Generate recommendations
    if high_priority > 0:
        results["recommendations"].append("🚨 Address high-priority database issues immediately")
    if medium_priority > 0:
        results["recommendations"].append("⚠️ Review and resolve medium-priority database issues")
    if total_issues == 0:
        results["recommendations"].append("✅ All database files validated successfully")

    # Add specific recommendations
    for issue in results["issues"]:
        if issue["type"] == "missing_database":
            results["recommendations"].append(f"Create missing database: {issue['database']}")
        elif issue["type"] == "integrity_failure":
            results["recommendations"].append(f"Repair database integrity: {issue['database']}")
        elif issue["type"] == "inactive_coordination":
            results["recommendations"].append("Restart coordination activities to maintain swarm intelligence")


def main():
    """Run simple database audit."""
    print("🔍 Simple Database Audit")
    print("=" * 40)

    results = audit_databases()

    # Print summary
    summary = results["summary"]
    print("\n📊 AUDIT SUMMARY:")
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

    # Save results
    output_file = "database_audit_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n📄 Detailed results saved to: {output_file}")
    print("\n✅ Database audit completed!")


if __name__ == "__main__":
    main()