#!/usr/bin/env python3
"""
A2A Coordination Status Checker - Utility Tool
====================================

Quick utility to check active A2A coordinations and their status.
Complements the full A2A coordination tracker with simplified status reporting.

V2 Compliance: ≤150 lines
Author: Agent-3 (Infrastructure & DevOps)
Created: 2026-01-08
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

class A2ACoordinationStatusChecker:
    """Simple status checker for A2A coordinations."""

    def __init__(self, tracker_file: str = "a2a_coordination_tracking.json"):
        self.tracker_file = Path(tracker_file)

    def get_active_coordinations(self) -> List[Dict[str, Any]]:
        """Get all active (unresponded) coordinations."""
        if not self.tracker_file.exists():
            return []

        try:
            with open(self.tracker_file, 'r') as f:
                data = json.load(f)
                coordinations = data.get("coordinations", [])
                return [c for c in coordinations if not c.get("responded", False)]
        except Exception:
            return []

    def get_recent_responses(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get recent coordination responses."""
        if not self.tracker_file.exists():
            return []

        try:
            with open(self.tracker_file, 'r') as f:
                data = json.load(f)
                responses = data.get("responses", [])
                return sorted(responses, key=lambda x: x.get("timestamp", ""), reverse=True)[:limit]
        except Exception:
            return []

    def get_coordination_summary(self) -> Dict[str, Any]:
        """Get coordination activity summary."""
        if not self.tracker_file.exists():
            return {"total": 0, "active": 0, "completed": 0}

        try:
            with open(self.tracker_file, 'r') as f:
                data = json.load(f)
                coordinations = data.get("coordinations", [])
                responses = data.get("responses", [])

                total = len(coordinations)
                active = len([c for c in coordinations if not c.get("responded", False)])
                completed = len(responses)

                return {
                    "total": total,
                    "active": active,
                    "completed": completed,
                    "acceptance_rate": completed / total if total > 0 else 0
                }
        except Exception:
            return {"total": 0, "active": 0, "completed": 0}

def main():
    """CLI interface for coordination status checking."""
    import argparse

    parser = argparse.ArgumentParser(description="A2A Coordination Status Checker")
    parser.add_argument("--active", action="store_true", help="Show active coordinations")
    parser.add_argument("--recent", type=int, default=5, help="Show recent responses (default: 5)")
    parser.add_argument("--summary", action="store_true", help="Show coordination summary")

    args = parser.parse_args()

    checker = A2ACoordinationStatusChecker()

    if args.active:
        active = checker.get_active_coordinations()
        print(f"🔄 Active Coordinations ({len(active)}):")
        for coord in active:
            print(f"  {coord['message_id']}: {coord['sender']} → {coord['recipient']} ({coord['priority']})")

    elif args.recent:
        recent = checker.get_recent_responses(args.recent)
        print(f"📅 Recent Responses ({len(recent)}):")
        for resp in recent:
            status = "✅" if resp.get("accepted", False) else "❌"
            print(f"  {status} {resp['original_message_id']} → {resp['response_message_id']}")

    elif args.summary:
        summary = checker.get_coordination_summary()
        print("📊 A2A Coordination Summary:")
        print(f"  Total Coordinations: {summary['total']}")
        print(f"  Active: {summary['active']}")
        print(f"  Completed: {summary['completed']}")
        print(f"  Acceptance Rate: {summary.get('acceptance_rate', 0):.1%}")

    else:
        # Show overview
        summary = checker.get_coordination_summary()
        active = checker.get_active_coordinations()
        recent = checker.get_recent_responses(3)

        print("🎯 A2A Coordination Status Overview")
        print("=" * 40)
        print(f"Summary: {summary['completed']}/{summary['total']} completed ({summary.get('acceptance_rate', 0):.1%} acceptance)")
        print(f"Active: {len(active)} pending responses")

        if active:
            print("\n🔄 Active Coordinations:")
            for coord in active[:3]:  # Show first 3
                print(f"  • {coord['sender']} → {coord['recipient']} ({coord['priority']})")

        if recent:
            print("\n📅 Recent Activity:")
            for resp in recent:
                status = "✅ Accepted" if resp.get("accepted", False) else "❌ Declined"
                print(f"  • {resp['original_message_id']}: {status}")

if __name__ == "__main__":
    main()