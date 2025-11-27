#!/usr/bin/env python3
"""
Conversation Storage for Memory Storage
Handles conversation CRUD operations.
"""

import sqlite3
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)


class ConversationStatsCache:
    """Cache for conversation statistics to avoid expensive recalculations."""

    def __init__(self, cache_file: str = "conversation_stats_cache.json"):
        self.cache_file = cache_file
        self.cache_data = {}
        self.load_cache()

    def load_cache(self):
        """Load cached stats from file."""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, "r") as f:
                    self.cache_data = json.load(f)
                logger.info("Loaded conversation stats cache")
            else:
                self.cache_data = {}
        except Exception as e:
            logger.warning(f"Failed to load stats cache: {e}")
            self.cache_data = {}

    def save_cache(self):
        """Save current stats to cache file."""
        try:
            with open(self.cache_file, "w") as f:
                json.dump(self.cache_data, f, indent=2)
            logger.info("Saved conversation stats cache")
        except Exception as e:
            logger.warning(f"Failed to save stats cache: {e}")

    def get_cache_key(self, table_name: str) -> str:
        """Generate cache key for a table."""
        return f"{table_name}_stats"

    def is_cache_valid(self, table_name: str, last_modified: float) -> bool:
        """Check if cached stats are still valid."""
        cache_key = self.get_cache_key(table_name)
        if cache_key not in self.cache_data:
            return False

        cached_time = self.cache_data[cache_key].get("last_modified", 0)
        return cached_time >= last_modified

    def get_cached_stats(self, table_name: str) -> Optional[Dict[str, Any]]:
        """Get cached stats for a table."""
        cache_key = self.get_cache_key(table_name)
        return self.cache_data.get(cache_key, {}).get("stats")

    def update_cache(
        self, table_name: str, stats: Dict[str, Any], last_modified: float
    ):
        """Update cache with new stats."""
        cache_key = self.get_cache_key(table_name)
        self.cache_data[cache_key] = {
            "stats": stats,
            "last_modified": last_modified,
            "cached_at": datetime.now().isoformat(),
        }
        self.save_cache()


def ensure_indexes(conn):
    index_sql = [
        "CREATE INDEX IF NOT EXISTS idx_conversations_timestamp ON conversations(timestamp);",
        "CREATE INDEX IF NOT EXISTS idx_conversations_model ON conversations(model);",
    ]
    for sql in index_sql:
        conn.execute(sql)


class ConversationStorage:
    """Handles conversation storage operations."""

    def __init__(self, connection):
        """
        Initialize the conversation storage.

        Args:
            connection: SQLite connection object
        """
        self.conn = connection
        ensure_indexes(self.conn)
        self.stats_cache = ConversationStatsCache()

        # Create the conversations table if it doesn't exist
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                timestamp TEXT,
                captured_at TEXT,
                model TEXT DEFAULT 'gpt-4o',
                tags TEXT DEFAULT '',
                summary TEXT,
                content TEXT,
                url TEXT,
                message_count INTEGER DEFAULT 0,
                word_count INTEGER DEFAULT 0,
                source TEXT DEFAULT 'chatgpt',
                status TEXT DEFAULT 'active',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        self.conn.commit()

    def get_table_last_modified(self) -> float:
        """Get the last modification time of the conversations table."""
        try:
            cursor = self.conn.execute(
                """
                SELECT MAX(updated_at) as last_modified 
                FROM conversations 
                WHERE updated_at IS NOT NULL
            """
            )
            result = cursor.fetchone()
            if result and result[0]:
                # Convert ISO format to timestamp
                dt = datetime.fromisoformat(result[0].replace("Z", "+00:00"))
                return dt.timestamp()
            return 0
        except Exception as e:
            logger.warning(f"Failed to get table last modified: {e}")
            return 0

    def get_conversation_stats(self) -> Dict[str, Any]:
        """Get conversation statistics with caching."""
        try:
            # Check if we can use cached stats
            last_modified = self.get_table_last_modified()
            if self.stats_cache.is_cache_valid("conversations", last_modified):
                cached_stats = self.stats_cache.get_cached_stats("conversations")
                if cached_stats:
                    logger.info("Using cached conversation stats")
                    return cached_stats

            # Calculate fresh stats
            logger.info("Calculating fresh conversation stats...")
            stats = self._calculate_conversation_stats()

            # Update cache
            self.stats_cache.update_cache("conversations", stats, last_modified)

            return stats

        except Exception as e:
            logger.error(f"Failed to get conversation stats: {e}")
            return {}

    def _calculate_conversation_stats(self) -> Dict[str, Any]:
        """Calculate conversation statistics (expensive operation)."""
        try:
            cursor = self.conn.cursor()

            # Total conversations
            cursor.execute("SELECT COUNT(*) as total FROM conversations")
            total_conversations = cursor.fetchone()[0]

            # Model distribution
            cursor.execute(
                "SELECT model, COUNT(*) as count FROM conversations GROUP BY model"
            )
            model_distribution = dict(cursor.fetchall())

            # Message and word counts
            cursor.execute(
                "SELECT SUM(message_count) as total_messages, SUM(word_count) as total_words FROM conversations"
            )
            result = cursor.fetchone()
            total_messages = result[0] or 0
            total_words = result[1] or 0

            # Recent conversations (last 7 days)
            cursor.execute(
                "SELECT COUNT(*) as recent_count FROM conversations WHERE timestamp >= datetime('now', '-7 days')"
            )
            recent_conversations = cursor.fetchone()[0]

            # Date range
            cursor.execute("SELECT MIN(timestamp), MAX(timestamp) FROM conversations")
            result = cursor.fetchone()
            date_range = {"earliest": result[0], "latest": result[1]}

            # Time-based counts
            cursor.execute(
                "SELECT COUNT(*) FROM conversations WHERE timestamp >= datetime('now', '-1 day')"
            )
            last_24h = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COUNT(*) FROM conversations WHERE timestamp >= datetime('now', '-7 days')"
            )
            last_7d = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COUNT(*) FROM conversations WHERE timestamp >= datetime('now', '-30 days')"
            )
            last_30d = cursor.fetchone()[0]

            return {
                "total_conversations": total_conversations,
                "model_distribution": model_distribution,
                "total_messages": total_messages,
                "total_words": total_words,
                "recent_conversations": recent_conversations,
                "date_range": date_range,
                "time_based_counts": {
                    "last_24h": last_24h,
                    "last_7d": last_7d,
                    "last_30d": last_30d,
                },
            }

        except Exception as e:
            logger.error(f"Failed to calculate conversation stats: {e}")
            return {}

    def invalidate_stats_cache(self):
        """Invalidate the stats cache (call when data changes)."""
        self.stats_cache.cache_data = {}
        if os.path.exists(self.stats_cache.cache_file):
            os.remove(self.stats_cache.cache_file)
        logger.info("Invalidated conversation stats cache")

    def store_conversation(self, conversation_data: Dict[str, Any]) -> bool:
        """
        Store a conversation in the database.

        Args:
            conversation_data: Dictionary containing conversation data

        Returns:
            True if stored successfully, False otherwise
        """
        try:
            cursor = self.conn.cursor()

            cursor.execute(
                """
                INSERT OR REPLACE INTO conversations
                (id, title, timestamp, captured_at, model, tags, summary, content, url, message_count, word_count, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    conversation_data.get("id"),
                    conversation_data.get("title", "Untitled"),
                    conversation_data.get("timestamp", datetime.now().isoformat()),
                    conversation_data.get("captured_at", datetime.now().isoformat()),
                    conversation_data.get("model", "gpt-4o"),
                    conversation_data.get("tags", ""),
                    conversation_data.get("summary"),
                    conversation_data.get("content"),
                    conversation_data.get("url", ""),
                    conversation_data.get("message_count", 0),
                    conversation_data.get("word_count", 0),
                    datetime.now().isoformat(),
                ),
            )

            self.conn.commit()
            logger.info(
                f"[OK] Stored conversation: {conversation_data.get('title', 'Untitled')}"
            )
            # After successful storage, invalidate cache
            self.invalidate_stats_cache()
            return True

        except Exception as e:
            logger.error(f"❌ Failed to store conversation: {e}")
            return False

    def get_conversation_by_id(self, conversation_id: str) -> Dict[str, Any]:
        """
        Retrieve a conversation by ID.

        Args:
            conversation_id: ID of the conversation to retrieve

        Returns:
            Conversation data dictionary or None if not found
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                SELECT * FROM conversations WHERE id = ?
            """,
                (conversation_id,),
            )

            row = cursor.fetchone()
            if row:
                return dict(row)
            return None

        except Exception as e:
            logger.error(f"❌ Failed to retrieve conversation {conversation_id}: {e}")
            return None

    def _initialize_sample_data(self):
        """Insert a sample conversation if the table is empty."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM conversations")
            count = cursor.fetchone()[0]
            if count == 0:
                sample = {
                    "id": "sample-1",
                    "title": "Sample Conversation",
                    "timestamp": datetime.now().isoformat(),
                    "captured_at": datetime.now().isoformat(),
                    "model": "gpt-4o",
                    "tags": "",
                    "summary": "This is a sample conversation for demonstration.",
                    "content": "Welcome to Dreamscape! This is a sample conversation. Start chatting to see more.",
                    "url": "",
                    "message_count": 1,
                    "word_count": 10,
                    "source": "sample",
                    "status": "active",
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat(),
                }
                self.conn.execute(
                    """
                    INSERT INTO conversations (id, title, timestamp, captured_at, model, tags, summary, content, url, message_count, word_count, source, status, created_at, updated_at)
                    VALUES (:id, :title, :timestamp, :captured_at, :model, :tags, :summary, :content, :url, :message_count, :word_count, :source, :status, :created_at, :updated_at)
                    """,
                    sample,
                )
                self.conn.commit()
                logger.info("[OK] Inserted sample conversation data.")
        except Exception as e:
            logger.warning(f"Failed to insert sample conversation: {e}")

    def get_recent_conversations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent conversations. If none exist, initialize with sample data.
        """
        try:
            self._initialize_sample_data()
            cursor = self.conn.cursor()
            cursor.execute(
                """
                SELECT * FROM conversations 
                ORDER BY timestamp DESC 
                LIMIT ?
            """,
                (limit,),
            )
            conversations = [dict(row) for row in cursor.fetchall()]
            if not conversations:
                logger.info("No conversations found. Returning empty list.")
            return conversations
        except Exception as e:
            logger.error(f"❌ Failed to retrieve recent conversations: {e}")
            return []

    def get_conversations_chronological(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get conversations in chronological order (oldest first). If none exist, initialize with sample data.
        """
        try:
            self._initialize_sample_data()
            cursor = self.conn.cursor()
            if limit is not None:
                query = """
                    SELECT * FROM conversations 
                    ORDER BY timestamp ASC 
                    LIMIT ?
                """
                cursor.execute(query, (limit,))
            else:
                query = """
                    SELECT * FROM conversations 
                    ORDER BY timestamp ASC
                """
                cursor.execute(query)
            conversations = [dict(row) for row in cursor.fetchall()]
            if not conversations:
                logger.info("No conversations found. Returning empty list.")
            return conversations
        except Exception as e:
            logger.error(f"Failed to retrieve chronological conversations: {e}")
            return []

    def get_conversations_count(self) -> int:
        """
        Get the total number of conversations in the database.

        Returns:
            Total number of conversations
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM conversations")
            return cursor.fetchone()[0]
        except Exception as e:
            logger.error(f"❌ Failed to get conversations count: {e}")
            return 0

    def get_conversations(self, limit: int = 1000) -> List[Dict[str, Any]]:
        """
        Get conversations from the database.

        Args:
            limit: Maximum number of conversations to return (None for all)

        Returns:
            List of conversation dictionaries
        """
        try:
            cursor = self.conn.cursor()

            # Build query based on whether limit is specified
            if limit is not None:
                query = """
                    SELECT * FROM conversations 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                """
                cursor.execute(query, (limit,))
            else:
                query = """
                    SELECT * FROM conversations 
                    ORDER BY timestamp DESC
                """
                cursor.execute(query)

            conversations = []
            for row in cursor.fetchall():
                conversations.append(dict(row))

            return conversations

        except Exception as e:
            logger.error(f"❌ Failed to retrieve conversations: {e}")
            return []

    def store_conversations_bulk(self, rows: List[tuple]) -> int:
        """Insert many conversations in one executemany call.

        Parameters
        ----------
        rows : list[tuple]
            Each tuple must match the column order used in
            :py:meth:`store_conversation`.

        Returns
        -------
        int
            Number of rows inserted.
        """
        if not rows:
            return 0
        try:
            cursor = self.conn.cursor()
            cursor.executemany(
                """
                INSERT OR REPLACE INTO conversations
                (id, title, timestamp, captured_at, model, tags, summary, content, url,
                 message_count, word_count, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                rows,
            )
            self.conn.commit()
            return cursor.rowcount or len(rows)
        except Exception as exc:
            logger.error("❌ Bulk insert failed: %s", exc)
            return 0

    def update_conversation_content(
        self, conversation_id: str, content: str, message_count: int, word_count: int
    ) -> bool:
        """
        Update conversation content, message count, and word count.

        Args:
            conversation_id: ID of the conversation to update
            content: New conversation content
            message_count: Number of messages
            word_count: Number of words

        Returns:
            True if updated successfully, False otherwise
        """
        try:
            cursor = self.conn.cursor()

            cursor.execute(
                """
                UPDATE conversations 
                SET content = ?, message_count = ?, word_count = ?, updated_at = ?
                WHERE id = ?
            """,
                (
                    content,
                    message_count,
                    word_count,
                    datetime.now().isoformat(),
                    conversation_id,
                ),
            )

            if cursor.rowcount > 0:
                self.conn.commit()
                logger.info(f"✅ Updated conversation content: {conversation_id}")
                # Invalidate cache after update
                self.invalidate_stats_cache()
                return True
            else:
                logger.warning(f"⚠️ No conversation found with ID: {conversation_id}")
                return False

        except Exception as e:
            logger.error(f"❌ Failed to update conversation content: {e}")
            return False
