"""
Index Builder for DreamVault AI Training Pipeline
================================================

SSOT Domain: ai_training

V2 Compliant: <100 lines, single responsibility
Search index construction for efficient data retrieval.
"""

import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class IndexEntry:
    """Index entry for search"""
    id: str
    content: str
    metadata: Dict[str, Any]
    embedding: Optional[List[float]] = None


class IndexBuilder:
    """
    V2 Compliant Index Builder

    Builds search indices for efficient data retrieval.
    Single responsibility: index construction and maintenance.
    """

    def __init__(self):
        self.logger = logging.getLogger("IndexBuilder")

        # Index storage
        self._entries: Dict[str, IndexEntry] = {}
        self._content_index: Dict[str, List[str]] = {}  # term -> entry_ids
        self._metadata_index: Dict[str, Dict[str, List[str]]] = {}  # field -> value -> entry_ids

    def add_entry(self, entry: IndexEntry) -> None:
        """
        Add entry to index.

        Args:
            entry: Index entry to add
        """
        self._entries[entry.id] = entry

        # Index content for full-text search
        self._index_content(entry.id, entry.content)

        # Index metadata for field searches
        self._index_metadata(entry.id, entry.metadata)

    def add_entries_batch(self, entries: List[IndexEntry]) -> None:
        """
        Add multiple entries to index.

        Args:
            entries: List of index entries
        """
        for entry in entries:
            self.add_entry(entry)

    def search_content(self, query: str, limit: int = 10) -> List[IndexEntry]:
        """
        Search index by content.

        Args:
            query: Search query
            limit: Maximum results to return

        Returns:
            List of matching entries
        """
        query_terms = self._tokenize_query(query.lower())
        candidate_ids = set()

        # Find entries containing any query term
        for term in query_terms:
            if term in self._content_index:
                candidate_ids.update(self._content_index[term])

        # Simple scoring: count of matching terms
        scored_results = []
        for entry_id in candidate_ids:
            if entry_id in self._entries:
                entry = self._entries[entry_id]
                score = self._calculate_content_score(entry.content.lower(), query_terms)
                scored_results.append((score, entry))

        # Sort by score and return top results
        scored_results.sort(key=lambda x: x[0], reverse=True)
        return [entry for _, entry in scored_results[:limit]]

    def search_metadata(self, field: str, value: str, limit: int = 10) -> List[IndexEntry]:
        """
        Search index by metadata field.

        Args:
            field: Metadata field name
            value: Field value to search for
            limit: Maximum results to return

        Returns:
            List of matching entries
        """
        if field not in self._metadata_index:
            return []

        value_index = self._metadata_index[field]
        if value not in value_index:
            return []

        entry_ids = value_index[value]
        return [self._entries[eid] for eid in entry_ids[:limit] if eid in self._entries]

    def get_entry(self, entry_id: str) -> Optional[IndexEntry]:
        """
        Get entry by ID.

        Args:
            entry_id: Entry identifier

        Returns:
            Index entry or None if not found
        """
        return self._entries.get(entry_id)

    def remove_entry(self, entry_id: str) -> bool:
        """
        Remove entry from index.

        Args:
            entry_id: Entry identifier

        Returns:
            True if entry was removed, False if not found
        """
        if entry_id not in self._entries:
            return False

        entry = self._entries[entry_id]

        # Remove from content index
        self._remove_from_content_index(entry_id, entry.content)

        # Remove from metadata index
        self._remove_from_metadata_index(entry_id, entry.metadata)

        # Remove entry
        del self._entries[entry_id]
        return True

    def get_stats(self) -> Dict[str, Any]:
        """
        Get index statistics.

        Returns:
            Dict with index statistics
        """
        return {
            "total_entries": len(self._entries),
            "content_terms": len(self._content_index),
            "metadata_fields": len(self._metadata_index),
            "avg_terms_per_entry": sum(len(ids) for ids in self._content_index.values()) / max(1, len(self._entries))
        }

    def _index_content(self, entry_id: str, content: str) -> None:
        """Index content for full-text search."""
        terms = set(self._tokenize_query(content.lower()))

        for term in terms:
            if term not in self._content_index:
                self._content_index[term] = []
            if entry_id not in self._content_index[term]:
                self._content_index[term].append(entry_id)

    def _index_metadata(self, entry_id: str, metadata: Dict[str, Any]) -> None:
        """Index metadata for field searches."""
        for field, value in metadata.items():
            if field not in self._metadata_index:
                self._metadata_index[field] = {}

            value_str = str(value).lower()
            if value_str not in self._metadata_index[field]:
                self._metadata_index[field][value_str] = []

            if entry_id not in self._metadata_index[field][value_str]:
                self._metadata_index[field][value_str].append(entry_id)

    def _tokenize_query(self, text: str) -> List[str]:
        """Simple tokenization for search."""
        # Remove punctuation and split
        import re
        return re.findall(r'\b\w+\b', text.lower())

    def _calculate_content_score(self, content: str, query_terms: List[str]) -> int:
        """Calculate content relevance score."""
        return sum(1 for term in query_terms if term in content)

    def _remove_from_content_index(self, entry_id: str, content: str) -> None:
        """Remove entry from content index."""
        terms = set(self._tokenize_query(content.lower()))

        for term in terms:
            if term in self._content_index:
                self._content_index[term] = [
                    eid for eid in self._content_index[term] if eid != entry_id
                ]
                if not self._content_index[term]:
                    del self._content_index[term]

    def _remove_from_metadata_index(self, entry_id: str, metadata: Dict[str, Any]) -> None:
        """Remove entry from metadata index."""
        for field, value in metadata.items():
            if field in self._metadata_index:
                value_str = str(value).lower()
                if value_str in self._metadata_index[field]:
                    self._metadata_index[field][value_str] = [
                        eid for eid in self._metadata_index[field][value_str] if eid != entry_id
                    ]
                    if not self._metadata_index[field][value_str]:
                        del self._metadata_index[field][value_str]