#!/usr/bin/env python3
"""
Queue Manager - Message Queue Health & Cleanup
==============================================

Features from deprecated scripts:
- clean_message_queue.py: System message filtering
- reset_stuck_messages.py: Stuck message recovery
- Queue statistics and health monitoring

V2 Compliance: <200 lines, single responsibility
Author: Agent-7 (Web Development Specialist)
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class QueueManager:
    """Manages message queue health, cleanup, and stuck message recovery."""

    def __init__(self, project_root: Path):
        """Initialize queue manager."""
        self.project_root = project_root
        self.queue_file = project_root / "message_queue" / "queue.json"
        self.archive_dir = project_root / "message_queue" / "archive"

        # Create archive directory if it doesn't exist
        self.archive_dir.mkdir(parents=True, exist_ok=True)

    def clean_system_messages(self) -> Dict[str, Any]:
        """
        Clean system messages from queue (from clean_message_queue.py)

        Removes messages that should not be delivered:
        - SYSTEM sender messages
        - S2A stall recovery messages
        - "Do not reply" messages
        """
        if not self.queue_file.exists():
            return {"status": "error", "message": "Queue file not found"}

        try:
            with open(self.queue_file, 'r', encoding='utf-8') as f:
                queue_data = json.load(f)

            original_count = len(queue_data)
            cleaned_queue = []
            removed_count = 0

            for entry in queue_data:
                if self._is_system_message(entry):
                    removed_count += 1
                    # Archive removed message
                    self._archive_message(entry, "system_message")
                    logger.info(f"🗑️ Removed system message: {entry.get('queue_id', 'unknown')}")
                else:
                    cleaned_queue.append(entry)

            # Save cleaned queue
            with open(self.queue_file, 'w', encoding='utf-8') as f:
                json.dump(cleaned_queue, f, indent=2, ensure_ascii=False)

            # Reset all remaining messages to PENDING status
            self._reset_all_to_pending(cleaned_queue)

            return {
                "status": "success",
                "original_count": original_count,
                "removed_count": removed_count,
                "remaining_count": len(cleaned_queue),
                "message": f"Cleaned {removed_count} system messages, {len(cleaned_queue)} messages remaining"
            }

        except Exception as e:
            logger.error(f"Failed to clean queue: {e}")
            return {"status": "error", "message": str(e)}

    def reset_stuck_messages(self) -> Dict[str, Any]:
        """
        Reset stuck messages to PENDING status

        Identifies messages that have been in PROCESSING status
        for too long and resets them for retry.
        """
        if not self.queue_file.exists():
            return {"status": "error", "message": "Queue file not found"}

        try:
            with open(self.queue_file, 'r', encoding='utf-8') as f:
                queue_data = json.load(f)

            reset_count = 0
            stuck_threshold = timedelta(hours=1)  # Messages stuck > 1 hour

            for entry in queue_data:
                if entry.get('status') == 'PROCESSING':
                    updated_at = entry.get('updated_at')
                    if updated_at:
                        try:
                            # Parse ISO timestamp
                            updated_time = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
                            if datetime.now(updated_time.tzinfo) - updated_time > stuck_threshold:
                                # Reset to PENDING
                                entry['status'] = 'PENDING'
                                entry['updated_at'] = datetime.now().isoformat()
                                entry['metadata'] = entry.get('metadata', {})
                                entry['metadata']['delivery_attempts'] = 0
                                entry['metadata']['last_reset'] = datetime.now().isoformat()
                                reset_count += 1
                                logger.info(f"🔄 Reset stuck message: {entry.get('queue_id', 'unknown')}")
                        except (ValueError, TypeError) as e:
                            logger.warning(f"Could not parse timestamp for {entry.get('queue_id')}: {e}")

            # Save updated queue
            with open(self.queue_file, 'w', encoding='utf-8') as f:
                json.dump(queue_data, f, indent=2, ensure_ascii=False)

            return {
                "status": "success",
                "reset_count": reset_count,
                "message": f"Reset {reset_count} stuck messages to PENDING status"
            }

        except Exception as e:
            logger.error(f"Failed to reset stuck messages: {e}")
            return {"status": "error", "message": str(e)}

    def get_queue_stats(self) -> Dict[str, Any]:
        """Get comprehensive queue statistics."""
        if not self.queue_file.exists():
            return {"status": "error", "message": "Queue file not found"}

        try:
            with open(self.queue_file, 'r', encoding='utf-8') as f:
                queue_data = json.load(f)

            stats = {
                "total_messages": len(queue_data),
                "status_breakdown": {},
                "priority_breakdown": {},
                "sender_breakdown": {},
                "recipient_breakdown": {},
                "oldest_message": None,
                "newest_message": None
            }

            for entry in queue_data:
                # Status breakdown
                status = entry.get('status', 'unknown')
                stats["status_breakdown"][status] = stats["status_breakdown"].get(status, 0) + 1

                # Priority breakdown
                priority = entry.get('priority', 'normal')
                stats["priority_breakdown"][priority] = stats["priority_breakdown"].get(priority, 0) + 1

                # Sender breakdown
                message = entry.get('message', {})
                sender = message.get('sender', 'unknown')
                stats["sender_breakdown"][sender] = stats["sender_breakdown"].get(sender, 0) + 1

                # Recipient breakdown
                recipient = message.get('recipient', 'unknown')
                stats["recipient_breakdown"][recipient] = stats["recipient_breakdown"].get(recipient, 0) + 1

                # Timestamps
                created_at = entry.get('created_at')
                if created_at:
                    if not stats["oldest_message"] or created_at < stats["oldest_message"]:
                        stats["oldest_message"] = created_at
                    if not stats["newest_message"] or created_at > stats["newest_message"]:
                        stats["newest_message"] = created_at

            return stats

        except Exception as e:
            logger.error(f"Failed to get queue stats: {e}")
            return {"status": "error", "message": str(e)}

    def _is_system_message(self, entry: Dict[str, Any]) -> bool:
        """Check if entry is a system message that should be removed."""
        message = entry.get('message', {})

        if not isinstance(message, dict):
            return False

        sender = message.get('sender', '').upper()
        content = message.get('content', '')

        # Remove messages from SYSTEM sender
        if sender == 'SYSTEM':
            return True

        # Remove S2A stall recovery messages
        if 'S2A STALL RECOVERY' in content.upper() or 'DO NOT REPLY' in content.upper():
            return True

        return False

    def _reset_all_to_pending(self, queue_data: List[Dict[str, Any]]) -> None:
        """Reset all messages in queue to PENDING status."""
        for entry in queue_data:
            if entry.get('status') != 'PENDING':
                entry['status'] = 'PENDING'
                entry['updated_at'] = datetime.now().isoformat()
                if 'metadata' not in entry:
                    entry['metadata'] = {}
                entry['metadata']['delivery_attempts'] = 0
                entry['metadata']['reset_reason'] = 'queue_cleanup'

        logger.info(f"🔄 Reset {len(queue_data)} messages to PENDING status")

    def _archive_message(self, entry: Dict[str, Any], reason: str) -> None:
        """Archive a message for audit purposes."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_file = self.archive_dir / f"archived_{timestamp}_{reason}.json"

        archive_data = {
            "archived_at": datetime.now().isoformat(),
            "reason": reason,
            "original_entry": entry
        }

        try:
            with open(archive_file, 'w', encoding='utf-8') as f:
                json.dump(archive_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.warning(f"Failed to archive message: {e}")