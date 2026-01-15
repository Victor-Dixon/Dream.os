"""
<!-- SSOT Domain: integration -->

Work Indexer
============

Agent work indexing operations for vector database.
V2 Compliance: < 100 lines, single responsibility.
Migrated to BaseService for consolidated initialization and error handling.

Navigation References:
├── Related Files:
│   ├── Vector Database → src/services/vector_database_service_unified.py
│   ├── Vector Models → src/services/models/vector_models.py
│   ├── Document Types → src/services/vector_database/vector_database_models.py
│   └── Agent Workspaces → agent_workspaces/
├── Documentation:
│   ├── Vector Integration → docs/VECTOR_DATABASE_INTEGRATION.md
│   ├── Search Architecture → docs/architecture/SEARCH_SYSTEM_ARCHITECTURE.md
│   └── Agent Workflows → docs/AGENTS.md
├── API Endpoints:
│   └── Vector Search API → src/services/vector/vector_database_service.py
└── Usage:
    └── Index Work → python -m src.services.work_indexer --help

Author: Agent-7 - Web Development Specialist
"""

import logging
from pathlib import Path
from datetime import datetime

from ..core.base.base_service import BaseService


# Optional vector database imports - import directly to avoid services __init__ chain
try:
    from .vector.vector_database_service import VectorDatabaseService
    from .vector.vector_database_models import VectorDocument
    VECTOR_DB_AVAILABLE = True

    def get_vector_database_service():
        return VectorDatabaseService()

    def add_document_to_vector_db(doc):

        service = get_vector_database_service()
        if service:
            return service.add_document(doc)
        return False


except (ImportError, ValueError, AttributeError) as e:
    print(f"⚠️  Vector database not available for work indexer: {e}")

    VECTOR_DB_AVAILABLE = False
    def get_vector_database_service():
        return None
    def add_document_to_vector_db(doc):
        return False

    # Fallback VectorDocument class

    from dataclasses import dataclass
    @dataclass
    class VectorDocument:
        id: str
        content: str
        embedding: list
        metadata: dict


class WorkIndexer(BaseService):
    """Handles agent work indexing operations."""

    def __init__(self, agent_id: str, config_path: str | None = None):
        """Initialize work indexer."""
        super().__init__("WorkIndexer")
        self.agent_id = agent_id
        self.workspace_path = Path(f"agent_workspaces/{agent_id}")

        # Initialize vector integration
        try:
            self.vector_db = get_vector_database_service()
            self.vector_integration = {"status": "connected", "service": self.vector_db}
        except Exception as e:
            self.logger.warning(f"Vector DB not available: {e}")
            self.vector_integration = {"status": "disconnected", "error": str(e)}

    def index_agent_work(self, file_path: str, work_type: str = "code") -> bool:
        """
        Index agent's completed work to vector database.



        Args:
            file_path: Path to the file to index
            work_type: Type of work (code, documentation, test, etc.)

        Returns:
            True if successfully indexed
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                self.logger.warning(f"File not found: {file_path}")
                return False

            if self.vector_integration["status"] != "connected":
                self.logger.warning("Vector DB not connected, skipping indexing")
                return False

            # Read file content
            content = file_path.read_text(encoding='utf-8')
            if not content.strip():
                self.logger.warning(f"File is empty: {file_path}")
                return False

            # Create vector document
            document = VectorDocument(
                id=f"{self.agent_id}_{file_path.name}_{datetime.now().timestamp()}",
                content=content,
                document_type=DocumentType(work_type),
                source_file=str(file_path),
                tags=[f"agent:{self.agent_id}", f"type:{work_type}"],
                metadata={
                    "agent_id": self.agent_id,
                    "work_type": work_type,
                    "file_size": len(content),
                    "indexed_at": datetime.now().isoformat()
                }
            )

            # Add to vector database
            result = add_document_to_vector_db(document, "agent_work")
            if result.success:
                self.logger.info(f"Successfully indexed {file_path}")
                return True
            else:
                self.logger.error(f"Failed to index {file_path}: {result.message}")
                return False

        except Exception as e:
            self.logger.error(f"Error indexing {file_path}: {e}")
            return False

    def index_inbox_messages(self) -> int:
        """
        Index agent's inbox messages for intelligent search.

        Returns:
            Number of messages indexed
        """
        try:
            inbox_path = self.workspace_path / "inbox"
            if not inbox_path.exists():
                self.logger.info(f"No inbox directory found for {self.agent_id}")
                return 0

            if self.vector_integration["status"] != "connected":
                self.logger.warning("Vector DB not connected, skipping inbox indexing")
                return 0

            indexed_count = 0
            message_files = list(inbox_path.glob("*.md"))

            for message_file in message_files:
                try:
                    content = message_file.read_text(encoding='utf-8')
                    if not content.strip():
                        continue

                    # Create vector document for message
                    document = VectorDocument(
                        id=f"{self.agent_id}_inbox_{message_file.name}_{datetime.now().timestamp()}",
                        content=content,
                        document_type=DocumentType("message"),
                        source_file=str(message_file),
                        tags=[f"agent:{self.agent_id}", "type:inbox_message"],
                        metadata={
                            "agent_id": self.agent_id,
                            "message_file": message_file.name,
                            "indexed_at": datetime.now().isoformat()
                        }
                    )

                    # Add to vector database
                    result = add_document_to_vector_db(document, "agent_messages")
                    if result.success:
                        indexed_count += 1
                        self.logger.debug(f"Indexed inbox message: {message_file.name}")
                    else:
                        self.logger.warning(f"Failed to index message {message_file.name}: {result.message}")

                except Exception as e:
                    self.logger.error(f"Error indexing message {message_file.name}: {e}")
                    continue

            self.logger.info(f"Indexed {indexed_count} inbox messages for {self.agent_id}")
            return indexed_count

        except Exception as e:
            self.logger.error(f"Error indexing inbox messages: {e}")
            return 0
