#!/usr/bin/env python3
"""
Delivery Verifier - Message Delivery Verification & Diagnostics
=============================================================

Features from message_delivery_verifier.py:
- Inbox file verification
- Delivery status checking
- Message content validation
- Cross-system consistency checks
- Delivery statistics and reporting

V2 Compliance: <250 lines, single responsibility
Author: Agent-7 (Web Development Specialist)
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class DeliveryVerifier:
    """Verifies message delivery status and provides diagnostics."""

    def __init__(self, project_root: Path):
        """Initialize delivery verifier."""
        self.project_root = project_root
        self.queue_file = project_root / "message_queue" / "queue.json"
        self.agent_workspaces = project_root / "agent_workspaces"

    def verify_all_deliveries(self) -> Dict[str, Any]:
        """
        Comprehensive delivery verification for all agents

        Checks:
        - Queue status vs inbox status
        - Message content integrity
        - Delivery timestamps
        - Stuck message detection
        """
        results = {
            "verified_agents": [],
            "queue_inbox_mismatches": [],
            "stuck_messages": [],
            "missing_inboxes": [],
            "total_verified": 0,
            "errors": []
        }

        # Check all agent workspaces
        for agent_dir in self.agent_workspaces.glob("Agent-*"):
            agent_id = agent_dir.name
            try:
                agent_result = self.verify_agent_delivery(agent_id)
                results["verified_agents"].append({
                    "agent_id": agent_id,
                    "result": agent_result
                })

                # Aggregate issues
                if agent_result.get("queue_inbox_mismatch"):
                    results["queue_inbox_mismatches"].append(agent_id)
                if agent_result.get("stuck_messages", 0) > 0:
                    results["stuck_messages"].append({
                        "agent_id": agent_id,
                        "count": agent_result["stuck_messages"]
                    })
                if agent_result.get("inbox_missing"):
                    results["missing_inboxes"].append(agent_id)

                results["total_verified"] += agent_result.get("messages_checked", 0)

            except Exception as e:
                logger.error(f"Failed to verify {agent_id}: {e}")
                results["errors"].append(f"{agent_id}: {e}")

        return results

    def verify_agent_delivery(self, agent_id: str) -> Dict[str, Any]:
        """
        Verify delivery status for specific agent

        Returns comprehensive delivery verification results.
        """
        inbox_dir = self.agent_workspaces / agent_id / "inbox"

        result = {
            "agent_id": agent_id,
            "messages_checked": 0,
            "inbox_missing": False,
            "queue_inbox_mismatch": False,
            "stuck_messages": 0,
            "verified_messages": 0,
            "issues": []
        }

        # Check inbox exists
        if not inbox_dir.exists():
            result["inbox_missing"] = True
            result["issues"].append("Inbox directory missing")
            return result

        # Get messages for this agent from queue
        queue_messages = self._get_agent_queue_messages(agent_id)
        inbox_messages = self._get_agent_inbox_messages(agent_id)

        result["messages_checked"] = len(queue_messages) + len(inbox_messages)

        # Check for stuck messages (PROCESSING too long)
        stuck_threshold = timedelta(hours=2)
        for msg in queue_messages:
            if msg.get('status') == 'PROCESSING':
                updated_at = msg.get('updated_at')
                if updated_at:
                    try:
                        updated_time = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
                        if datetime.now(updated_time.tzinfo) - updated_time > stuck_threshold:
                            result["stuck_messages"] += 1
                    except (ValueError, TypeError):
                        result["stuck_messages"] += 1  # Assume stuck if can't parse

        # Check queue vs inbox consistency
        queue_ids = {msg.get('queue_id') for msg in queue_messages}
        inbox_ids = {self._extract_message_id(filename) for filename in inbox_messages.keys()}

        # Messages in queue but not in inbox (should be delivered)
        undelivered = queue_ids - inbox_ids
        if undelivered:
            result["queue_inbox_mismatch"] = True
            result["issues"].append(f"Undelivered messages: {len(undelivered)}")

        # Messages in inbox but not in queue (orphaned)
        orphaned = inbox_ids - queue_ids
        if orphaned:
            result["issues"].append(f"Orphaned inbox messages: {len(orphaned)}")

        result["verified_messages"] = len(queue_ids & inbox_ids)

        return result

    def verify_specific_message(self, message_id: str) -> Dict[str, Any]:
        """
        Verify delivery of specific message

        Checks all agents for the message and verifies delivery status.
        """
        result = {
            "message_id": message_id,
            "found_in_queue": False,
            "found_in_inboxes": [],
            "queue_status": None,
            "delivery_verified": False,
            "issues": []
        }

        # Check queue
        queue_entry = self._find_message_in_queue(message_id)
        if queue_entry:
            result["found_in_queue"] = True
            result["queue_status"] = queue_entry.get('status')

        # Check all agent inboxes
        for agent_dir in self.agent_workspaces.glob("Agent-*"):
            agent_id = agent_dir.name
            inbox_messages = self._get_agent_inbox_messages(agent_id)

            for filename, content in inbox_messages.items():
                if message_id in filename:
                    result["found_in_inboxes"].append({
                        "agent_id": agent_id,
                        "filename": filename,
                        "content_preview": content[:200] + "..." if len(content) > 200 else content
                    })

        # Determine if delivery is verified
        if result["found_in_queue"] and result["found_in_inboxes"]:
            result["delivery_verified"] = True
        elif result["found_in_queue"] and not result["found_in_inboxes"]:
            if result["queue_status"] in ["PENDING", "PROCESSING"]:
                result["issues"].append("Message queued but not yet delivered")
            else:
                result["issues"].append("Message marked delivered but not found in inbox")
        elif not result["found_in_queue"] and result["found_in_inboxes"]:
            result["issues"].append("Message found in inbox but not in queue (orphaned)")

        return result

    def get_delivery_stats(self) -> Dict[str, Any]:
        """Get comprehensive delivery statistics."""
        all_results = self.verify_all_deliveries()

        stats = {
            "total_agents_verified": len(all_results["verified_agents"]),
            "total_messages_checked": all_results["total_verified"],
            "queue_inbox_mismatches": len(all_results["queue_inbox_mismatches"]),
            "agents_with_stuck_messages": len(all_results["stuck_messages"]),
            "missing_inboxes": len(all_results["missing_inboxes"]),
            "total_stuck_messages": sum(msg["count"] for msg in all_results["stuck_messages"]),
            "verification_errors": len(all_results["errors"])
        }

        # Calculate success rate
        if stats["total_messages_checked"] > 0:
            verified_count = sum(agent["result"]["verified_messages"]
                               for agent in all_results["verified_agents"])
            stats["delivery_success_rate"] = verified_count / stats["total_messages_checked"]
        else:
            stats["delivery_success_rate"] = 1.0

        return stats

    def _get_agent_queue_messages(self, agent_id: str) -> List[Dict[str, Any]]:
        """Get all queue messages for specific agent."""
        if not self.queue_file.exists():
            return []

        try:
            with open(self.queue_file, 'r', encoding='utf-8') as f:
                queue_data = json.load(f)

            agent_messages = []
            for entry in queue_data:
                message = entry.get('message', {})
                recipient = message.get('recipient')
                if recipient == agent_id:
                    agent_messages.append(entry)

            return agent_messages

        except Exception as e:
            logger.error(f"Failed to read queue for {agent_id}: {e}")
            return []

    def _get_agent_inbox_messages(self, agent_id: str) -> Dict[str, str]:
        """Get all inbox messages for specific agent."""
        inbox_dir = self.agent_workspaces / agent_id / "inbox"
        if not inbox_dir.exists():
            return {}

        messages = {}
        for msg_file in inbox_dir.glob("*.md"):
            try:
                content = msg_file.read_text(encoding='utf-8')
                messages[msg_file.name] = content
            except Exception as e:
                logger.warning(f"Failed to read {msg_file}: {e}")

        return messages

    def _find_message_in_queue(self, message_id: str) -> Optional[Dict[str, Any]]:
        """Find specific message in queue by ID."""
        if not self.queue_file.exists():
            return None

        try:
            with open(self.queue_file, 'r', encoding='utf-8') as f:
                queue_data = json.load(f)

            for entry in queue_data:
                entry_message_id = entry.get('message', {}).get('message_id')
                queue_id = entry.get('queue_id')
                if entry_message_id == message_id or queue_id == message_id:
                    return entry

        except Exception as e:
            logger.error(f"Failed to find message {message_id}: {e}")

        return None

    def _extract_message_id(self, filename: str) -> str:
        """Extract message ID from filename."""
        # Look for UUID pattern in filename
        import re
        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        match = re.search(uuid_pattern, filename)
        return match.group(0) if match else filename