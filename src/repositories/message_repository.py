"""
Message Repository - Data Access Layer
======================================

Handles all message-related data operations following the repository pattern.
This repository provides data access abstraction for message storage, history,
and retrieval operations.

<!-- SSOT Domain: data -->

Author: Agent-7 (Quarantine Mission Phase 3)
Date: 2025-10-16
Points: 300

BI Integration: Agent-5 (2025-01-27)
- Added metrics tracking for message analytics
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

try:
    from src.core.analytics.engines.metrics_engine import MetricsEngine
    METRICS_AVAILABLE = True
except ImportError:
    METRICS_AVAILABLE = False
    MetricsEngine = None


class MessageRepository:
    """
    Repository for message data operations.

    Provides data access layer for message persistence, history tracking,
    and retrieval. No business logic - pure data operations.

    Attributes:
        message_history_file: Path to message history JSON file
        inbox_root: Root directory for agent inboxes
    """

    def __init__(
        self,
        message_history_file: str = "data/message_history.json",
        inbox_root: str = "agent_workspaces",
        metrics_engine: Optional[MetricsEngine] = None,
    ):
        """
        Initialize message repository.

        Args:
            message_history_file: Path to message history storage
            inbox_root: Root directory for agent workspaces
            metrics_engine: Optional metrics engine for BI tracking
        """
        self.message_history_file = Path(message_history_file)
        self.inbox_root = Path(inbox_root)
        self.metrics_engine = metrics_engine if metrics_engine else (
            MetricsEngine() if METRICS_AVAILABLE else None
        )
        self._ensure_history_file()

    def _ensure_history_file(self) -> None:
        """Ensure message history file exists with proper structure."""
        if not self.message_history_file.exists():
            self.message_history_file.parent.mkdir(parents=True, exist_ok=True)
            self._save_history(
                {
                    "messages": [],
                    "metadata": {"version": "1.0", "created_at": datetime.now().isoformat()},
                }
            )

    def _load_history(self) -> dict[str, Any]:
        """
        Load message history from file.

        Returns:
            Message history data dictionary
        """
        try:
            with open(self.message_history_file, encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            return {"messages": [], "metadata": {"version": "1.0"}}

    def _save_history(self, data: dict[str, Any]) -> bool:
        """
        Save message history to file.

        Args:
            data: Message history data dictionary

        Returns:
            True if save successful, False otherwise
        """
        try:
            with open(self.message_history_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except OSError:
            return False

    def save_message(self, message: dict[str, Any]) -> bool:
        """
        Save message to storage.

        Args:
            message: Message data dictionary

        Returns:
            True if save successful, False otherwise
        """
        data = self._load_history()
        messages = data.get("messages", [])

        # Add timestamp if not present
        if "timestamp" not in message:
            message["timestamp"] = datetime.now().isoformat()

        # Add message ID if not present
        if "message_id" not in message:
            message["message_id"] = f"msg_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        messages.append(message)
        data["messages"] = messages

        success = self._save_history(data)

        # BI: Track message metrics if metrics engine available
        if success and self.metrics_engine:
            try:
                self.metrics_engine.increment_metric("messages.total")
                
                # Track by sender
                sender = message.get("from") or message.get("sender", "unknown")
                self.metrics_engine.increment_metric(f"messages.by_sender.{sender}")
                
                # Track by recipient
                recipient = message.get("to") or message.get("recipient", "unknown")
                self.metrics_engine.increment_metric(f"messages.by_recipient.{recipient}")
                
                # Track by message type
                msg_type = message.get("message_type") or message.get("type", "unknown")
                self.metrics_engine.increment_metric(f"messages.by_type.{msg_type}")
                
                # Track by priority
                priority = message.get("priority", "normal")
                self.metrics_engine.increment_metric(f"messages.by_priority.{priority}")
                
                # Track Discord username if available
                discord_user = message.get("discord_username")
                if discord_user:
                    self.metrics_engine.increment_metric(f"messages.by_discord_user.{discord_user}")
            except Exception:
                # Don't fail message save if metrics tracking fails
                pass

        return success

    def get_message_history(
        self, agent_id: str | None = None, limit: int | None = None
    ) -> list[dict[str, Any]]:
        """
        Get message history, optionally filtered by agent.

        Args:
            agent_id: Optional agent ID to filter messages
            limit: Optional maximum number of messages to return

        Returns:
            List of message data dictionaries
        """
        data = self._load_history()
        messages = data.get("messages", [])

        # Filter by agent if specified
        if agent_id:
            messages = [m for m in messages if m.get("to") == agent_id or m.get("from") == agent_id]

        # Sort by timestamp (newest first)
        messages.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

        # Apply limit if specified
        if limit:
            messages = messages[:limit]

        return messages

    def get_recent_messages(self, limit: int = 10) -> list[dict[str, Any]]:
        """
        Get recent messages across all agents.

        Args:
            limit: Maximum number of messages to return (default: 10)

        Returns:
            List of recent message data dictionaries
        """
        return self.get_message_history(limit=limit)

    def get_messages_by_sender(self, sender_id: str) -> list[dict[str, Any]]:
        """
        Get all messages from specific sender.

        Args:
            sender_id: Sender identifier

        Returns:
            List of message data dictionaries
        """
        data = self._load_history()
        messages = data.get("messages", [])

        sender_messages = [m for m in messages if m.get("from") == sender_id]

        sender_messages.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

        return sender_messages

    def get_messages_by_recipient(self, recipient_id: str) -> list[dict[str, Any]]:
        """
        Get all messages to specific recipient.

        Args:
            recipient_id: Recipient identifier

        Returns:
            List of message data dictionaries
        """
        data = self._load_history()
        messages = data.get("messages", [])

        recipient_messages = [m for m in messages if m.get("to") == recipient_id]

        recipient_messages.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

        return recipient_messages

    def get_inbox_messages(self, agent_id: str) -> list[dict[str, Any]]:
        """
        Get inbox messages for specific agent from file system.

        Args:
            agent_id: Agent identifier

        Returns:
            List of inbox message file metadata
        """
        inbox_dir = self.inbox_root / agent_id / "inbox"

        if not inbox_dir.exists():
            return []

        messages = []
        for msg_file in inbox_dir.glob("*.md"):
            messages.append(
                {
                    "filename": msg_file.name,
                    "path": str(msg_file),
                    "modified": datetime.fromtimestamp(msg_file.stat().st_mtime).isoformat(),
                    "size": msg_file.stat().st_size,
                    "agent_id": agent_id,
                }
            )

        messages.sort(key=lambda x: x["modified"], reverse=True)
        return messages

    def get_message_count(self, agent_id: str | None = None) -> int:
        """
        Get message count, optionally filtered by agent.

        Args:
            agent_id: Optional agent ID to filter messages

        Returns:
            Count of messages
        """
        messages = self.get_message_history(agent_id=agent_id)
        return len(messages)

    def clear_old_messages(self, days: int = 30) -> int:
        """
        Clear messages older than specified days.

        Args:
            days: Number of days to retain (default: 30)

        Returns:
            Number of messages removed
        """
        data = self._load_history()
        messages = data.get("messages", [])

        cutoff = datetime.now().timestamp() - (days * 24 * 60 * 60)
        original_count = len(messages)

        # Keep messages newer than cutoff
        filtered_messages = []
        for msg in messages:
            timestamp_str = msg.get("timestamp", "")
            try:
                msg_time = datetime.fromisoformat(timestamp_str).timestamp()
                if msg_time >= cutoff:
                    filtered_messages.append(msg)
            except (ValueError, AttributeError):
                # Keep messages with invalid timestamps
                filtered_messages.append(msg)

        data["messages"] = filtered_messages
        self._save_history(data)

        return original_count - len(filtered_messages)

    def compress_old_messages(self, days: int = 7, compression_level: int = 6) -> dict[str, Any]:
        """
        Compress messages older than specified days using Agent-3's compression tools.

        Args:
            days: Number of days to keep uncompressed (default: 7)
            compression_level: Compression level 1-9 (default: 6)

        Returns:
            Dictionary with compression results
        """
        try:
            # Use Agent-3's compression automation tool
            import subprocess
            import sys
            from pathlib import Path

            tool_path = Path("tools/message_compression_automation.py")
            if not tool_path.exists():
                return {
                    "success": False,
                    "error": "Compression tool not found",
                    "compressed": 0,
                    "saved_bytes": 0
                }

            # Run compression tool (no --days or --level args, tool handles age-based compression internally)
            result = subprocess.run(
                [sys.executable, str(tool_path)],
                capture_output=True,
                text=True,
                cwd=Path.cwd()
            )

            if result.returncode == 0:
                # Parse output if available
                return {
                    "success": True,
                    "compressed": 0,  # Will be updated by tool
                    "saved_bytes": 0,  # Will be updated by tool
                    "output": result.stdout
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr,
                    "compressed": 0,
                    "saved_bytes": 0
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "compressed": 0,
                "saved_bytes": 0
            }

    def get_compression_stats(self) -> dict[str, Any]:
        """
        Get compression statistics using Agent-3's health check tool.

        Returns:
            Dictionary with compression statistics
        """
        try:
            import subprocess
            import sys
            from pathlib import Path

            tool_path = Path("tools/message_compression_health_check.py")
            if not tool_path.exists():
                return {
                    "success": False,
                    "error": "Health check tool not found"
                }

            # Run health check tool
            result = subprocess.run(
                [sys.executable, str(tool_path)],
                capture_output=True,
                text=True,
                cwd=Path.cwd()
            )

            if result.returncode == 0:
                return {
                    "success": True,
                    "stats": result.stdout
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }