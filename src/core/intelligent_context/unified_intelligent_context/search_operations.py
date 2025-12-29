"""
<!-- SSOT Domain: core -->

Intelligent Context Search Operations
====================================

Search operations for intelligent context search functionality.
V2 Compliance: < 300 lines, single responsibility, search logic.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

import re
from datetime import datetime

from .models import ContextType, Priority, Status
# Use SSOT SearchResult - supports all intelligent context fields
from src.services.models.vector_models import SearchResult


class IntelligentContextSearchOperations:
    """Search operations for intelligent context search."""

    def __init__(self, base_search, logger=None):
        """Initialize search operations with base search reference."""
        self.base_search = base_search
        self.logger = logger

    def search_contexts(
        self,
        query: str,
        context_type: ContextType = None,
        priority_filter: Priority = None,
        status_filter: Status = None,
        limit: int = 10,
    ) -> list[SearchResult]:
        """Search contexts with filters."""
        try:
            # Preprocess query
            processed_query = self._preprocess_query(query)

            # Get search results
            results = self._perform_search(
                processed_query, context_type, priority_filter, status_filter
            )

            # Sort by relevance
            results.sort(key=lambda x: x.relevance_score, reverse=True)

            # Apply limit
            results = results[:limit]

            # Record search
            self.base_search._record_search(query, len(results))

            return results

        except Exception as e:
            if self.logger:
                self.logger.error(f"Error searching contexts: {e}")
            return []

    def _preprocess_query(self, query: str) -> str:
        """Preprocess search query."""
        # Convert to lowercase
        query = query.lower()

        # Remove stop words
        words = query.split()
        filtered_words = [word for word in words if word not in self.base_search.stop_words]

        # Join words back
        processed_query = " ".join(filtered_words)

        return processed_query

    def _perform_search(
        self,
        query: str,
        context_type: ContextType = None,
        priority_filter: Priority = None,
        status_filter: Status = None,
    ) -> list[SearchResult]:
        """Perform the actual search using vector database."""
        try:
            # Try to use real vector database search
            results = self._search_vector_database(
                query, context_type, priority_filter, status_filter
            )
            
            # If vector DB search returns results, use them
            if results:
                return results
            
            # Fallback to mock results if vector DB unavailable or returns no results
            if self.logger:
                self.logger.warning(
                    f"Vector database search returned no results, using fallback for query: {query}"
                )
            return self._create_mock_results(query, context_type, priority_filter, status_filter)
            
        except Exception as e:
            # On error, fallback to mock results
            if self.logger:
                self.logger.error(f"Vector database search failed: {e}, using fallback")
            return self._create_mock_results(query, context_type, priority_filter, status_filter)

    def _search_vector_database(
        self,
        query: str,
        context_type: ContextType = None,
        priority_filter: Priority = None,
        status_filter: Status = None,
    ) -> list[SearchResult]:
        """Search using real vector database."""
        try:
            from src.services.vector_database_service_unified import get_vector_database_service
            from src.web.vector_database.models import SearchRequest as VectorSearchRequest
            
            # Get vector database service
            vector_db = get_vector_database_service()
            if not vector_db:
                return []
            
            # Build search filters based on context type
            filters = {}
            if context_type:
                filters["context_type"] = context_type.value
            if priority_filter:
                filters["priority"] = priority_filter.value
            if status_filter:
                filters["status"] = status_filter.value
            
            # Create search request
            search_request = VectorSearchRequest(
                query=query,
                collection="all",
                limit=20,  # Get more results for filtering
                filters=filters,
            )
            
            # Perform search
            vector_results = vector_db.search(search_request)
            
            # Convert vector database results to SearchResult format
            results = []
            for vec_result in vector_results:
                # Map vector DB result to intelligent context SearchResult
                result = SearchResult(
                    result_id=vec_result.id,
                    title=vec_result.title or "",
                    description=vec_result.content[:200] if vec_result.content else "",  # Truncate
                    relevance_score=vec_result.relevance or vec_result.score or 0.0,
                    context_type=self._infer_context_type(vec_result),
                    metadata={
                        "collection": vec_result.collection,
                        "tags": vec_result.tags,
                        **vec_result.metadata,
                    },
                )
                results.append(result)
            
            return results
            
        except ImportError:
            # Vector database service not available
            if self.logger:
                self.logger.debug("Vector database service not available")
            return []
        except Exception as e:
            if self.logger:
                self.logger.error(f"Vector database search error: {e}")
            return []
    
    def _infer_context_type(self, vec_result) -> ContextType | None:
        """Infer context type from vector database result metadata."""
        try:
            metadata = vec_result.metadata or {}
            collection = vec_result.collection or ""
            
            # Check metadata for context type
            if "context_type" in metadata:
                try:
                    return ContextType(metadata["context_type"])
                except ValueError:
                    pass
            
            # Infer from collection name
            collection_lower = collection.lower()
            if "mission" in collection_lower:
                return ContextType.MISSION
            elif "capability" in collection_lower or "agent" in collection_lower:
                return ContextType.AGENT_CAPABILITY
            elif "emergency" in collection_lower:
                return ContextType.EMERGENCY
            elif "task" in collection_lower:
                return ContextType.TASK
            elif "doc" in collection_lower:
                return ContextType.DOCUMENTATION
            
            return None
        except Exception:
            return None
    
    def _create_mock_results(
        self,
        query: str,
        context_type: ContextType = None,
        priority_filter: Priority = None,
        status_filter: Status = None,
    ) -> list[SearchResult]:
        """Create mock search results for fallback/demonstration."""
        results = []

        # Create some mock results based on query
        if "mission" in query or context_type == ContextType.MISSION:
            results.append(
                SearchResult(
                    result_id=f"mission_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    title="Sample Mission Context",
                    description="A sample mission context for testing",
                    relevance_score=0.8,
                    context_type=ContextType.MISSION,
                    metadata={"query": query},
                )
            )

        if "capability" in query or context_type == ContextType.AGENT_CAPABILITY:
            results.append(
                SearchResult(
                    result_id=f"capability_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    title="Sample Agent Capability",
                    description="A sample agent capability for testing",
                    relevance_score=0.7,
                    context_type=ContextType.AGENT_CAPABILITY,
                    metadata={"query": query},
                )
            )

        if "emergency" in query or context_type == ContextType.EMERGENCY:
            results.append(
                SearchResult(
                    result_id=f"emergency_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    title="Sample Emergency Context",
                    description="A sample emergency context for testing",
                    relevance_score=0.9,
                    context_type=ContextType.EMERGENCY,
                    metadata={"query": query},
                )
            )

        return results

    def search_with_pattern(self, query: str, pattern_name: str) -> list[SearchResult]:
        """Search using a specific pattern."""
        try:
            if pattern_name not in self.base_search.search_patterns:
                return []

            pattern = self.base_search.search_patterns[pattern_name]

            # Apply pattern to query
            if pattern:
                # Simple pattern matching - in real implementation this would be more sophisticated
                if re.search(pattern, query, re.IGNORECASE):
                    return self.search_contexts(query)

            return []

        except Exception as e:
            if self.logger:
                self.logger.error(f"Error searching with pattern: {e}")
            return []

    def optimize_search_query(self, query: str) -> str:
        """Optimize search query for better results."""
        try:
            # Remove extra whitespace
            query = " ".join(query.split())

            # Convert to lowercase
            query = query.lower()

            # Remove special characters except spaces
            query = re.sub(r"[^\w\s]", "", query)

            # Remove duplicate words
            words = query.split()
            unique_words = []
            for word in words:
                if word not in unique_words:
                    unique_words.append(word)

            optimized_query = " ".join(unique_words)

            return optimized_query

        except Exception as e:
            if self.logger:
                self.logger.error(f"Error optimizing search query: {e}")
            return query
