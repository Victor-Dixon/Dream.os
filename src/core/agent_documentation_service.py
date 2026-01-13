#!/usr/bin/env python3
"""
Agent Documentation Service - KISS Compliant

<!-- SSOT Domain: infrastructure -->

===========================================

Unified documentation service for AI agents.
Consolidates agent_docs_integration.py and agent_documentation_service.py.

Author: Agent-5 - Business Intelligence Specialist
Consolidation: Agent-7 - Web Development Specialist (2025-01-27)
License: MIT
"""

import logging
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


class AgentDocumentationService:
    """Unified documentation service for AI agents."""

    def __init__(self, agent_id: str = None, vector_db=None, db_path: str = "vector_db"):
        """Initialize documentation service.
        
        Args:
            agent_id: Optional agent ID for agent-specific operations
            vector_db: Optional vector database instance
            db_path: Path to vector database (default: "vector_db")
        """
        self.agent_id = agent_id
        self.vector_db = vector_db
        self.db_path = db_path
        self.contexts = {}
        self._initialize()

    def _initialize(self):
        """Initialize documentation service."""
        try:
            if self.agent_id:
                logger.info(f"Initialized documentation access for agent {self.agent_id}")
            else:
                logger.info("Initialized documentation service")
        except Exception as e:
            logger.error(f"Error initializing documentation service: {e}")

    def set_agent_context(self, agent_id: str, context: dict[str, Any]) -> None:
        """Set agent context."""
        self.contexts[agent_id] = context
        logger.info(f"Set context for agent {agent_id}")

    def search_documentation(
        self, agent_id: str = None, query: str = None, n_results: int = 5
    ) -> list[dict[str, Any]]:
        """Search documentation using vector database service.
        
        Args:
            agent_id: Optional agent ID (uses self.agent_id if not provided)
            query: Search query
            n_results: Number of results to return
            
        Returns:
            List of documentation results with title, content, relevance, source
        """
        target_agent_id = agent_id or self.agent_id
        
        if not query:
            return []
        
        try:
            logger.info(f"Searching documentation for agent {target_agent_id}: {query}")
            
            # Use vector database service if available
            try:
                from src.services.vector_database_service_unified import get_vector_database_service
                from src.web.vector_database.models import SearchRequest
                
                vector_db = get_vector_database_service()
                if vector_db:
                    # Build search request with agent filter if provided
                    filters = {}
                    if target_agent_id:
                        filters["agent_id"] = target_agent_id
                    
                    search_request = SearchRequest(
                        query=query,
                        collection="agent_cellphone_v2",  # Default collection
                        limit=n_results,
                        filters=filters if filters else None,
                    )
                    
                    # Perform search
                    results = vector_db.search(search_request)
                    
                    # Convert to expected format
                    return [
                        {
                            "title": result.title or f"Document {result.id}",
                            "content": result.content,
                            "relevance": result.relevance or result.score or 0.0,
                            "source": result.metadata.get("source", result.collection or "unknown") if result.metadata else result.collection or "unknown",
                            "id": result.id,
                            "collection": result.collection,
                            "tags": result.tags or [],
                            "created_at": result.created_at.isoformat() if hasattr(result.created_at, 'isoformat') else str(result.created_at),
                        }
                        for result in results
                    ]
            except ImportError:
                logger.warning("Vector database service not available, using fallback")
            except Exception as e:
                logger.warning(f"Vector database search failed: {e}, using fallback")
            
            # Fallback: Use vector_db if provided directly
            if self.vector_db:
                try:
                    # Try to use vector_db.search if it has that method
                    if hasattr(self.vector_db, 'search'):
                        from src.web.vector_database.models import SearchRequest
                        search_request = SearchRequest(
                            query=query,
                            collection="agent_cellphone_v2",
                            limit=n_results,
                        )
                        results = self.vector_db.search(search_request)
                        return [
                            {
                                "title": result.title or f"Document {result.id}",
                                "content": result.content,
                                "relevance": result.relevance or result.score or 0.0,
                                "source": result.collection or "unknown",
                                "id": result.id,
                            }
                            for result in results
                        ]
                except Exception as e:
                    logger.warning(f"Direct vector_db search failed: {e}")
            
            # Final fallback: Return empty results with warning
            logger.warning(f"No vector database available for documentation search")
            return []
            
        except Exception as e:
            logger.error(f"Error searching documentation: {e}", exc_info=True)
            return []

    def search_docs(self, query: str, n_results: int = 5) -> list[dict[str, Any]]:
        """Search documentation (alias for backward compatibility).
        
        Args:
            query: Search query
            n_results: Number of results to return
            
        Returns:
            List of documentation results
        """
        return self.search_documentation(agent_id=self.agent_id, query=query, n_results=n_results)

    def get_doc(self, doc_id: str) -> dict[str, Any] | None:
        """Get specific document by ID using vector database service.
        
        Args:
            doc_id: Document ID
            
        Returns:
            Document data with id, title, content, metadata, or None if not found
        """
        if not doc_id:
            return None
        
        try:
            logger.info(f"Getting document {doc_id} for agent {self.agent_id}")
            
            # Use vector database service if available
            try:
                from src.services.vector_database_service_unified import get_vector_database_service
                from src.web.vector_database.models import PaginationRequest
                
                vector_db = get_vector_database_service()
                if vector_db:
                    # Search for document by ID using pagination request
                    # Note: Vector DB services typically don't have direct get-by-id,
                    # so we search with a filter or use pagination
                    pagination_request = PaginationRequest(
                        collection="agent_cellphone_v2",
                        page=1,
                        page_size=100,  # Get enough to find the doc
                    )
                    
                    documents = vector_db.get_documents(pagination_request)
                    
                    # Find document by ID in results
                    if isinstance(documents, dict) and "documents" in documents:
                        for doc in documents.get("documents", []):
                            if doc.id == doc_id or str(doc.id) == str(doc_id):
                                return {
                                    "id": doc.id,
                                    "title": doc.title or f"Document {doc.id}",
                                    "content": doc.content,
                                    "collection": doc.collection,
                                    "tags": doc.tags or [],
                                    "metadata": doc.metadata or {},
                                    "created_at": doc.created_at.isoformat() if hasattr(doc.created_at, 'isoformat') else str(doc.created_at),
                                    "updated_at": doc.updated_at.isoformat() if hasattr(doc.updated_at, 'isoformat') else str(doc.updated_at),
                                    "last_updated": doc.updated_at.isoformat() if hasattr(doc.updated_at, 'isoformat') else str(doc.updated_at),
                                }
            except ImportError:
                logger.warning("Vector database service not available, using fallback")
            except Exception as e:
                logger.warning(f"Vector database document retrieval failed: {e}, using fallback")
            
            # Fallback: Use vector_db if provided directly
            if self.vector_db:
                try:
                    if hasattr(self.vector_db, 'get_documents'):
                        from src.web.vector_database.models import PaginationRequest
                        pagination_request = PaginationRequest(
                            collection="agent_cellphone_v2",
                            page=1,
                            page_size=100,
                        )
                        documents = self.vector_db.get_documents(pagination_request)
                        if isinstance(documents, dict) and "documents" in documents:
                            for doc in documents.get("documents", []):
                                if doc.id == doc_id or str(doc.id) == str(doc_id):
                                    return {
                                        "id": doc.id,
                                        "title": doc.title or f"Document {doc.id}",
                                        "content": doc.content,
                                        "last_updated": datetime.now().isoformat(),
                                    }
                except Exception as e:
                    logger.warning(f"Direct vector_db document retrieval failed: {e}")
            
            # Final fallback: Return None (document not found)
            logger.warning(f"Document {doc_id} not found - vector database not available or document doesn't exist")
            return None
            
        except Exception as e:
            logger.error(f"Error getting document: {e}", exc_info=True)
            return None

    def get_agent_relevant_docs(
        self, agent_id: str, doc_types: list[str] = None
    ) -> list[dict[str, Any]]:
        """Get relevant documents for agent."""
        logger.info(f"Getting relevant docs for agent {agent_id}")
        return []

    def get_documentation_summary(self, agent_id: str = None) -> dict[str, Any]:
        """Get documentation summary.
        
        Args:
            agent_id: Optional agent ID (uses self.agent_id if not provided)
            
        Returns:
            Documentation summary dictionary
        """
        target_agent_id = agent_id or self.agent_id
        return {"agent_id": target_agent_id, "docs_count": 0}

    def get_agent_context(self) -> dict[str, Any]:
        """Get agent context.
        
        Returns:
            Agent context dictionary
        """
        return {
            "agent_id": self.agent_id,
            "db_path": self.db_path,
            "timestamp": datetime.now().isoformat(),
        }

    def get_status(self) -> dict[str, Any]:
        """Get service status.
        
        Returns:
            Service status dictionary
        """
        return {
            "active": True,
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat(),
        }

    def get_search_suggestions(self, agent_id: str, partial_query: str) -> list[str]:
        """Get search suggestions."""
        return []


def create_agent_documentation_service(vector_db=None, agent_id: str = None, db_path: str = "vector_db"):
    """Create documentation service."""
    return AgentDocumentationService(agent_id=agent_id, vector_db=vector_db, db_path=db_path)


def create_agent_docs(agent_id: str, db_path: str = "vector_db") -> AgentDocumentationService:
    """Create agent documentation service (alias for backward compatibility)."""
    return AgentDocumentationService(agent_id=agent_id, db_path=db_path)


__all__ = [
    "AgentDocumentationService",
    "create_agent_documentation_service",
    "create_agent_docs",  # Backward compatibility alias
]
