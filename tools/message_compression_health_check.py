#!/usr/bin/env python3
"""
Message Compression Health Check Tool
=====================================

Health check tool for message compression system.
Monitors compression status, storage usage, and compression effectiveness.

Author: Agent-3 (Infrastructure & DevOps) - JET FUEL AUTONOMOUS MODE
Created: 2025-01-27
Priority: CRITICAL
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MessageCompressionHealthCheck:
    """Health check for message compression system."""

    def __init__(self, history_file: str = "data/message_history.json"):
        """Initialize health check."""
        self.history_file = Path(history_file)
        self.archive_dir = self.history_file.parent / "message_history_archive"

    def calculate_age_days(self, timestamp_str: str) -> int:
        """Calculate age of message in days."""
        try:
            msg_time = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
            now = datetime.now(msg_time.tzinfo) if msg_time.tzinfo else datetime.now()
            age = (now - msg_time).days
            return max(0, age)
        except (ValueError, AttributeError):
            return 0

    def check_compression_health(self) -> dict[str, Any]:
        """
        Perform comprehensive health check.
        
        Returns:
            Health check results dictionary
        """
        health = {
            "timestamp": datetime.now().isoformat(),
            "status": "unknown",
            "issues": [],
            "warnings": [],
            "metrics": {},
        }
        
        # Check if history file exists
        if not self.history_file.exists():
            health["status"] = "error"
            health["issues"].append(f"History file not found: {self.history_file}")
            return health
        
        # Load history
        try:
            with open(self.history_file, encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            health["status"] = "error"
            health["issues"].append(f"Failed to load history: {e}")
            return health
        
        messages = data.get("messages", [])
        metadata = data.get("metadata", {})
        
        # Analyze message distribution by age
        level1_count = 0  # 0-7 days
        level2_count = 0  # 7-30 days
        level3_count = 0  # 30+ days
        
        total_content_size = 0
        compressed_content_size = 0
        
        for msg in messages:
            timestamp = msg.get("timestamp", "")
            age_days = self.calculate_age_days(timestamp)
            
            content = str(msg.get("content", ""))
            content_size = len(content)
            total_content_size += content_size
            
            if age_days <= 7:
                level1_count += 1
            elif age_days <= 30:
                level2_count += 1
                # Check if compressed
                if "content_preview" in msg:
                    compressed_content_size += len(msg.get("content_preview", ""))
                else:
                    compressed_content_size += content_size
            else:
                level3_count += 1
                # Should be aggregated, but still in main file
                health["warnings"].append(f"Message older than 30 days not aggregated: {timestamp}")
        
        # Check file size
        file_size = self.history_file.stat().st_size
        file_size_mb = file_size / (1024 * 1024)
        
        # Check archive directory
        archive_files = list(self.archive_dir.glob("*.json")) if self.archive_dir.exists() else []
        archive_count = len(archive_files)
        
        # Check last compression
        last_compressed = metadata.get("last_compressed")
        compression_age_days = None
        if last_compressed:
            try:
                last_compressed_time = datetime.fromisoformat(last_compressed.replace("Z", "+00:00"))
                compression_age_days = (datetime.now() - last_compressed_time.replace(tzinfo=None)).days
            except (ValueError, AttributeError):
                pass
        
        # Determine health status
        if level3_count > 0:
            health["status"] = "warning"
            health["warnings"].append(f"{level3_count} messages older than 30 days need aggregation")
        
        if compression_age_days and compression_age_days > 7:
            health["status"] = "warning"
            health["warnings"].append(f"Last compression was {compression_age_days} days ago (should be daily)")
        
        if file_size_mb > 50:
            health["status"] = "warning"
            health["warnings"].append(f"History file is large: {file_size_mb:.2f} MB")
        
        if health["status"] == "unknown":
            health["status"] = "healthy"
        
        # Calculate compression metrics
        compression_ratio = 0
        if total_content_size > 0:
            compression_ratio = (1 - compressed_content_size / total_content_size) * 100
        
        # Build metrics
        health["metrics"] = {
            "total_messages": len(messages),
            "level1_count": level1_count,
            "level2_count": level2_count,
            "level3_count": level3_count,
            "file_size_bytes": file_size,
            "file_size_mb": round(file_size_mb, 2),
            "archive_files": archive_count,
            "last_compressed": last_compressed,
            "compression_age_days": compression_age_days,
            "compression_ratio": f"{compression_ratio:.1f}%",
            "total_content_size": total_content_size,
            "compressed_content_size": compressed_content_size,
        }
        
        # Compression recommendations
        recommendations = []
        if level3_count > 0:
            recommendations.append("Run compression to aggregate messages older than 30 days")
        if compression_age_days and compression_age_days > 1:
            recommendations.append("Run daily compression automation")
        if file_size_mb > 10:
            recommendations.append("Consider more aggressive compression for older messages")
        
        health["recommendations"] = recommendations
        
        return health

    def print_health_report(self) -> None:
        """Print human-readable health report."""
        health = self.check_compression_health()
        
        print("\n" + "="*70)
        print("📊 MESSAGE COMPRESSION HEALTH CHECK")
        print("="*70)
        print(f"Status: {health['status'].upper()}")
        print(f"Timestamp: {health['timestamp']}")
        print()
        
        print("📈 METRICS:")
        metrics = health["metrics"]
        print(f"  Total Messages: {metrics['total_messages']}")
        print(f"  Level 1 (0-7 days): {metrics['level1_count']}")
        print(f"  Level 2 (7-30 days): {metrics['level2_count']}")
        print(f"  Level 3 (30+ days): {metrics['level3_count']}")
        print(f"  File Size: {metrics['file_size_mb']} MB")
        print(f"  Archive Files: {metrics['archive_files']}")
        print(f"  Compression Ratio: {metrics['compression_ratio']}")
        if metrics.get("last_compressed"):
            print(f"  Last Compressed: {metrics['last_compressed']}")
            if metrics.get("compression_age_days"):
                print(f"  Compression Age: {metrics['compression_age_days']} days")
        print()
        
        if health["warnings"]:
            print("⚠️  WARNINGS:")
            for warning in health["warnings"]:
                print(f"  • {warning}")
            print()
        
        if health["issues"]:
            print("❌ ISSUES:")
            for issue in health["issues"]:
                print(f"  • {issue}")
            print()
        
        if health["recommendations"]:
            print("💡 RECOMMENDATIONS:")
            for rec in health["recommendations"]:
                print(f"  • {rec}")
            print()
        
        print("="*70 + "\n")


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Message Compression Health Check")
    parser.add_argument("--history-file", default="data/message_history.json", help="Path to message history file")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    health_check = MessageCompressionHealthCheck(history_file=args.history_file)
    
    if args.json:
        health = health_check.check_compression_health()
        print(json.dumps(health, indent=2))
    else:
        health_check.print_health_report()


if __name__ == "__main__":
    main()




