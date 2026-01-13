#!/usr/bin/env python3
"""
A2A Coordination Tracker - Utility Tool
======================================

Tracks A2A coordination requests and responses for swarm transparency.
Helps agents monitor active coordinations and response commitments.

V2 Compliance: ≤150 lines
Author: Agent-3 (Infrastructure & DevOps)
Created: 2026-01-07
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class A2ACoordinationTracker:
    """Tracks A2A coordination requests and responses."""

    def __init__(self, data_file: str = "a2a_coordination_tracking.json"):
        self.data_file = Path(data_file)
        self.data = self._load_data()

    def _load_data(self) -> Dict:
        """Load coordination tracking data."""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return {"coordinations": [], "responses": []}

    def _save_data(self):
        """Save coordination tracking data."""
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2, default=str)

    def track_request(self, message_id: str, sender: str, recipient: str,
                     priority: str, timestamp: str, content: str):
        """Track an incoming A2A coordination request."""
        coordination = {
            "message_id": message_id,
            "sender": sender,
            "recipient": recipient,
            "priority": priority,
            "timestamp": timestamp,
            "content": content,
            "status": "received",
            "responded": False,
            "response_timestamp": None
        }

        self.data["coordinations"].append(coordination)
        self._save_data()

    def track_response(self, original_message_id: str, response_message_id: str,
                      accepted: bool, proposed_approach: str, timeline: str):
        """Track a response to an A2A coordination request."""
        for coord in self.data["coordinations"]:
            if coord["message_id"] == original_message_id:
                coord["status"] = "accepted" if accepted else "declined"
                coord["responded"] = True
                coord["response_timestamp"] = datetime.now().isoformat()
                coord["response_message_id"] = response_message_id
                coord["proposed_approach"] = proposed_approach
                coord["timeline"] = timeline
                break

        response_record = {
            "original_message_id": original_message_id,
            "response_message_id": response_message_id,
            "accepted": accepted,
            "proposed_approach": proposed_approach,
            "timeline": timeline,
            "timestamp": datetime.now().isoformat()
        }

        self.data["responses"].append(response_record)
        self._save_data()

    def get_active_coordinations(self, agent_id: str) -> List[Dict]:
        """Get active coordinations for a specific agent."""
        active = []
        for coord in self.data["coordinations"]:
            if coord["recipient"] == agent_id and coord["status"] in ["received", "accepted"]:
                active.append(coord)
        return active

    def get_pending_responses(self, agent_id: str) -> List[Dict]:
        """Get coordinations requiring response from a specific agent."""
        pending = []
        for coord in self.data["coordinations"]:
            if coord["recipient"] == agent_id and not coord["responded"]:
                pending.append(coord)
        return pending

    def get_coordination_summary(self) -> Dict:
        """Get summary statistics of coordination activity."""
        total = len(self.data["coordinations"])
        accepted = len([c for c in self.data["coordinations"] if c["status"] == "accepted"])
        declined = len([c for c in self.data["coordinations"] if c["status"] == "declined"])
        pending = len([c for c in self.data["coordinations"] if not c["responded"]])

        return {
            "total_coordinations": total,
            "accepted": accepted,
            "declined": declined,
            "pending_responses": pending,
            "acceptance_rate": accepted / total if total > 0 else 0
        }

def main():
    """CLI interface for A2A coordination tracking."""
    import argparse

    parser = argparse.ArgumentParser(description="A2A Coordination Tracker")
    parser.add_argument("--track-request", nargs=5,
                       metavar=("MSG_ID", "SENDER", "RECIPIENT", "PRIORITY", "CONTENT"),
                       help="Track incoming coordination request")
    parser.add_argument("--track-response", nargs=5,
                       metavar=("ORIG_MSG_ID", "RESP_MSG_ID", "ACCEPTED", "APPROACH", "TIMELINE"),
                       help="Track coordination response")
    parser.add_argument("--active", metavar="AGENT_ID",
                       help="Show active coordinations for agent")
    parser.add_argument("--pending", metavar="AGENT_ID",
                       help="Show pending responses for agent")
    parser.add_argument("--summary", action="store_true",
                       help="Show coordination summary statistics")

    args = parser.parse_args()
    tracker = A2ACoordinationTracker()

    if args.track_request:
        msg_id, sender, recipient, priority, content = args.track_request
        tracker.track_request(msg_id, sender, recipient, priority,
                            datetime.now().isoformat(), content)
        print(f"✅ Tracked coordination request {msg_id}")

    elif args.track_response:
        orig_id, resp_id, accepted, approach, timeline = args.track_response
        accepted_bool = accepted.lower() == "true"
        tracker.track_response(orig_id, resp_id, accepted_bool, approach, timeline)
        print(f"✅ Tracked {'accepted' if accepted_bool else 'declined'} response")

    elif args.active:
        active = tracker.get_active_coordinations(args.active)
        print(f"🔄 Active coordinations for {args.active}:")
        for coord in active:
            print(f"  {coord['message_id']}: {coord['sender']} → {coord['status']}")

    elif args.pending:
        pending = tracker.get_pending_responses(args.pending)
        print(f"⏳ Pending responses for {args.pending}:")
        for coord in pending:
            print(f"  {coord['message_id']}: {coord['sender']} (priority: {coord['priority']})")

    elif args.summary:
        summary = tracker.get_coordination_summary()
        print("📊 A2A Coordination Summary:")
        print(f"  Total: {summary['total_coordinations']}")
        print(f"  Accepted: {summary['accepted']} ({summary['acceptance_rate']:.1%})")
        print(f"  Declined: {summary['declined']}")
        print(f"  Pending: {summary['pending_responses']}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()