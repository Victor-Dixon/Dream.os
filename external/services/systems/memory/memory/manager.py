#!/usr/bin/env python3
"""
Memory Manager
=============

Orchestrates the memory system components following Single Responsibility Principle.
This class coordinates between storage, search, processing, and API layers.
"""

import logging
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime
import functools
import threading

from ..utils.context_mixin import ContextManagerMixin
from .storage import MemoryStorage
from .search import SearchStorage
from .processing import MemoryContentProcessor, MemoryPromptProcessor
from .api import MemoryConversationAPI, MemoryPromptAPI, MemoryAgentAPI
from .storage.thread_safe_db import get_thread_safe_db, close_thread_connections
# Database paths updated for Phase 2 integration
MEMORY_DB_PATH = Path('systems/memory/data/dreamos_memory.db')
RESUME_DB_PATH = Path('systems/gamification/data/dreamos_resume.db')
TOOLS_DB_PATH = Path('tools/code_analysis/data/tools.db')
TEMPLATES_DB_PATH = Path('systems/templates/data/templates.db')
from pathlib import Path

logger = logging.getLogger(__name__)


class MemoryManager(ContextManagerMixin):
    """
    Core memory management system for Dream.OS.

    This class orchestrates the memory system components:
    - Storage: Database operations
    - Search: Search and indexing
    - Processing: Content and prompt analysis
    - API: High-level interfaces

    Responsibilities:
    - Coordinate between components
    - Provide unified interface
    - Manage conversation ingestion
    - Handle context retrieval
    """

    def __init__(self, db_path: str = str(MEMORY_DB_PATH)):
        """
        Initialize the Memory Manager.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        
        # Get thread-safe database manager
        self.db_manager = get_thread_safe_db(db_path)
        
        # Initialize storage layer with thread-safe connection
        self.storage = MemoryStorage(db_path, self.db_manager)

        # Initialize search layer
        self.search_storage = SearchStorage(self.db_manager.get_connection())

        # Initialize processing layer
        self.content_processor = MemoryContentProcessor(self.storage)
        self.prompt_processor = MemoryPromptProcessor(self.storage)

        # Initialize API layer
        self.conversation_api = MemoryConversationAPI(self)
        self.prompt_api = MemoryPromptAPI(self)
        self.agent_api = MemoryAgentAPI(self)

        # Legacy compatibility
        self.conn = self.db_manager.get_connection()
        self.db_path = db_path

        # LRU cache for recent conversations
        self._get_recent_conversations_cached = functools.lru_cache(maxsize=32)(self._get_recent_conversations_uncached)

        logger.info("Memory Manager initialized with modular architecture")

    def _normalize_conversation_json(self, raw: Any, file_path: str) -> Dict[str, Any]:
        """Convert multiple raw JSON shapes into a uniform conversation dict."""
        file_stem = Path(file_path).stem
        fallback_id = hashlib.md5(file_stem.encode()).hexdigest()[:12]

        # Case 1: list of messages or strings
        if isinstance(raw, list):
            messages = []
            for item in raw:
                if isinstance(item, dict):
                    role = item.get("role") or item.get("author_role") or "user"
                    content = (
                        item.get("content")
                        or item.get("text")
                        or item.get("message")
                        or ""
                    )
                else:  # string or unknown
                    role = "system"
                    content = str(item)
                messages.append({"role": role, "content": content})

            return {
                "id": fallback_id,
                "title": file_stem,
                "timestamp": datetime.now().isoformat(),
                "messages": messages,
            }

        # Case 2: already in desired format
        if isinstance(raw, dict) and isinstance(raw.get("messages"), list):
            return raw

        # Case 3: ChatGPT export format with mapping
        if isinstance(raw, dict) and "mapping" in raw:
            messages = []
            for node_id, node in raw["mapping"].items():
                if "message" in node and node["message"]:
                    msg = node["message"]
                    role = msg.get("author", {}).get("role", "user")
                    content = msg.get("content", [])
                    if isinstance(content, list):
                        # Handle content parts
                        text_parts = []
                        for part in content:
                            if part.get("type") == "text":
                                text_parts.append(part.get("text", ""))
                        content = " ".join(text_parts)
                    messages.append({"role": role, "content": content})

            return {
                "id": fallback_id,
                "title": file_stem,
                "timestamp": datetime.now().isoformat(),
                "messages": messages,
            }

        # Case 4: anything else - wrap as system message
        return {
            "id": fallback_id,
            "title": file_stem,
            "timestamp": datetime.now().isoformat(),
            "messages": [{"role": "system", "content": str(raw)}],
        }

    def ingest_conversations(
        self, conversations_dir: str = "data/conversations"
    ) -> int:
        """Ingest conversations from directory."""
        try:
            conversations_path = Path(conversations_dir)
            if not conversations_path.exists():
                logger.warning(
                    f"Conversations directory does not exist: {conversations_dir}"
                )
                return 0

            json_files = list(conversations_path.glob("*.json"))
            logger.info(f"Found {len(json_files)} JSON files to process")

            processed_count = 0
            for json_file in json_files:
                try:
                    with open(json_file, "r", encoding="utf-8") as f:
                        raw_data = json.load(f)

                    # Normalize conversation data
                    conversation_data = self._normalize_conversation_json(
                        raw_data, str(json_file)
                    )

                    # Process conversation using content processor
                    processed_data = self.content_processor.process_conversation(
                        conversation_data
                    )

                    # Store in database using storage layer
                    if self.storage.store_conversation(processed_data):
                        processed_count += 1
                        logger.info(f"✅ Processed: {json_file.name}")
                    else:
                        logger.error(f"❌ Failed to store: {json_file.name}")

                except Exception as e:
                    logger.error(f"❌ Failed to process {json_file.name}: {e}")
                    continue

            logger.info(f"🎉 Ingested {processed_count} conversations")
            return processed_count

        except Exception as e:
            logger.error(f"Failed to ingest conversations: {e}")
            return 0

    def _get_recent_conversations_uncached(self, limit: int = 10) -> List[Dict[str, Any]]:
        return self.storage.get_recent_conversations(limit)

    def get_recent_conversations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent conversations (cached)."""
        try:
            return self._get_recent_conversations_cached(limit)
        except Exception as e:
            logger.error(f"Failed to get recent conversations (cached): {e}")
            return self.storage.get_recent_conversations(limit)

    def get_conversation_by_id(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """Get conversation by ID."""
        return self.storage.get_conversation_by_id(conversation_id)

    def get_conversations_chronological(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get conversations in chronological order."""
        return self.storage.get_conversations_chronological(limit)

    def search_conversations(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search conversations by content."""
        return self.search_storage.search_conversations(query, limit)

    def advanced_search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Run advanced boolean search across conversations."""
        return self.search_storage.advanced_search(query, limit)

    def get_conversation_stats(self) -> Dict[str, Any]:
        """Get conversation statistics."""
        return self.storage.get_conversation_stats()

    def get_conversations_count(self) -> int:
        """Get total number of conversations."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) as count FROM conversations")
            return cursor.fetchone()["count"]
        except Exception as e:
            logger.error(f"Failed to get conversations count: {e}")
            return 0

    def get_templates(self) -> List[Dict[str, Any]]:
        """
        Return all prompt templates as a list of dicts for GUI analytics and template panels.
        Uses PromptTemplateEngine as the backend.
        """
        from systems.templates.templates.engine.template_engine import PromptTemplateEngine

        # Use the correct database path for templates
        template_db_path = Path(TEMPLATES_DB_PATH)
        engine = PromptTemplateEngine(template_db_path)
        templates = engine.find_templates(active_only=True)
        # Convert PromptTemplate dataclass objects to dicts for GUI compatibility
        return [
            {
                "id": t.id,
                "name": t.name,
                "content": t.content,
                "description": t.description,
                "category": t.type or "general",
                "created_at": t.created_at.isoformat() if t.created_at else None,
                "updated_at": t.updated_at.isoformat() if t.updated_at else None,
                "version": t.version,
                "is_active": t.is_active,
                "success_rate": t.success_rate,
                "usage_count": t.usage_count,
                "variables": t.variables,
                "metadata": t.metadata,
            }
            for t in templates
        ]

    def close(self):
        """Close the memory system."""
        if self.storage:
            self.storage.close()
