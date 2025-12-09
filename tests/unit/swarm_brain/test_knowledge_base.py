#!/usr/bin/env python3
"""
Test Suite for Knowledge Base System
=====================================

Comprehensive test suite for src/swarm_brain/knowledge_base.py.

Tests:
- KnowledgeEntry dataclass
- KnowledgeBase initialization
- Entry creation and retrieval
- Search functionality
- Category filtering
- Agent filtering
- File persistence

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-12-07
Priority: MEDIUM
"""

import json
import pytest
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

from src.swarm_brain.knowledge_base import KnowledgeBase, KnowledgeEntry


class TestKnowledgeEntry:
    """Test KnowledgeEntry dataclass."""

    def test_knowledge_entry_creation(self):
        """Test creating KnowledgeEntry."""
        entry = KnowledgeEntry(
            id="test-1",
            title="Test Entry",
            content="Test content",
            author="Agent-8",
            category="learning",
            tags=["test", "qa"],
        )
        assert entry.id == "test-1"
        assert entry.title == "Test Entry"
        assert entry.content == "Test content"
        assert entry.author == "Agent-8"
        assert entry.category == "learning"
        assert entry.tags == ["test", "qa"]

    def test_knowledge_entry_defaults(self):
        """Test KnowledgeEntry with default values."""
        entry = KnowledgeEntry(
            id="test-2",
            title="Test",
            content="Content",
            author="Agent-8",
            category="learning",
        )
        assert entry.tags == []
        assert entry.metadata == {}
        assert entry.timestamp is not None


class TestKnowledgeBaseInitialization:
    """Test KnowledgeBase initialization."""

    def test_knowledge_base_init_creates_directories(self):
        """Test KnowledgeBase creates required directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            kb = KnowledgeBase(brain_root=tmpdir)
            assert kb.brain_root.exists()
            assert kb.shared_learnings_dir.exists()
            assert kb.decisions_dir.exists()
            assert kb.protocols_dir.exists()

    def test_knowledge_base_init_creates_kb_file(self):
        """Test KnowledgeBase creates knowledge_base.json if missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            kb = KnowledgeBase(brain_root=tmpdir)
            assert kb.kb_file.exists()
            kb_data = json.loads(kb.kb_file.read_text(encoding="utf-8"))
            assert "created_at" in kb_data
            assert "entries" in kb_data
            assert "stats" in kb_data

    def test_knowledge_base_loads_existing_kb(self):
        """Test KnowledgeBase loads existing knowledge base."""
        with tempfile.TemporaryDirectory() as tmpdir:
            kb_file = Path(tmpdir) / "knowledge_base.json"
            existing_data = {
                "created_at": "2025-12-07T00:00:00",
                "last_updated": "2025-12-07T00:00:00",
                "entries": {"test-1": {"id": "test-1", "title": "Test"}},
                "stats": {"total_entries": 1, "contributors": {}},
            }
            kb_file.write_text(json.dumps(existing_data), encoding="utf-8")
            kb = KnowledgeBase(brain_root=tmpdir)
            assert "test-1" in kb.kb["entries"]


class TestKnowledgeBaseEntryManagement:
    """Test entry management operations."""

    def test_add_entry(self):
        """Test adding entry to knowledge base."""
        with tempfile.TemporaryDirectory() as tmpdir:
            kb = KnowledgeBase(brain_root=tmpdir)
            entry = KnowledgeEntry(
                id="test-1",
                title="Test Entry",
                content="Test content",
                author="Agent-8",
                category="learning",
                tags=["test"],
            )
            entry_id = kb.add_entry(entry)
            assert entry_id == "test-1"
            assert "test-1" in kb.kb["entries"]
            assert kb.kb["stats"]["total_entries"] == 1

    def test_add_entry_updates_stats(self):
        """Test adding entry updates contributor stats."""
        with tempfile.TemporaryDirectory() as tmpdir:
            kb = KnowledgeBase(brain_root=tmpdir)
            entry = KnowledgeEntry(
                id="test-1",
                title="Test",
                content="Content",
                author="Agent-8",
                category="learning",
            )
            kb.add_entry(entry)
            assert kb.kb["stats"]["contributors"]["Agent-8"] == 1

    def test_add_entry_saves_to_category_file(self):
        """Test adding entry saves to category markdown file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            kb = KnowledgeBase(brain_root=tmpdir)
            entry = KnowledgeEntry(
                id="test-1",
                title="Test Entry",
                content="Test content",
                author="Agent-8",
                category="learning",
                tags=["test"],
            )
            kb.add_entry(entry)
            category_file = kb.shared_learnings_dir / "learning.md"
            assert category_file.exists()
            content = category_file.read_text(encoding="utf-8")
            assert "Test Entry" in content
            assert "Agent-8" in content


class TestKnowledgeBaseSearch:
    """Test search functionality."""

    def test_search_by_title(self):
        """Test searching by title."""
        with tempfile.TemporaryDirectory() as tmpdir:
            kb = KnowledgeBase(brain_root=tmpdir)
            entry = KnowledgeEntry(
                id="test-1",
                title="Python Testing",
                content="Content",
                author="Agent-8",
                category="learning",
            )
            kb.add_entry(entry)
            results = kb.search("Python")
            assert len(results) == 1
            assert results[0].title == "Python Testing"

    def test_search_by_content(self):
        """Test searching by content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            kb = KnowledgeBase(brain_root=tmpdir)
            entry = KnowledgeEntry(
                id="test-1",
                title="Test",
                content="Python testing guide",
                author="Agent-8",
                category="learning",
            )
            kb.add_entry(entry)
            results = kb.search("testing")
            assert len(results) == 1

    def test_search_by_tags(self):
        """Test searching by tags."""
        with tempfile.TemporaryDirectory() as tmpdir:
            kb = KnowledgeBase(brain_root=tmpdir)
            entry = KnowledgeEntry(
                id="test-1",
                title="Test",
                content="Content",
                author="Agent-8",
                category="learning",
                tags=["python", "testing"],
            )
            kb.add_entry(entry)
            results = kb.search("python")
            assert len(results) == 1

    def test_search_no_results(self):
        """Test search with no matches."""
        with tempfile.TemporaryDirectory() as tmpdir:
            kb = KnowledgeBase(brain_root=tmpdir)
            results = kb.search("nonexistent")
            assert len(results) == 0


class TestKnowledgeBaseFiltering:
    """Test filtering operations."""

    def test_get_by_agent(self):
        """Test getting entries by agent."""
        with tempfile.TemporaryDirectory() as tmpdir:
            kb = KnowledgeBase(brain_root=tmpdir)
            entry1 = KnowledgeEntry(
                id="test-1",
                title="Test 1",
                content="Content",
                author="Agent-8",
                category="learning",
            )
            entry2 = KnowledgeEntry(
                id="test-2",
                title="Test 2",
                content="Content",
                author="Agent-7",
                category="learning",
            )
            kb.add_entry(entry1)
            kb.add_entry(entry2)
            results = kb.get_by_agent("Agent-8")
            assert len(results) == 1
            assert results[0].author == "Agent-8"

    def test_get_by_category(self):
        """Test getting entries by category."""
        with tempfile.TemporaryDirectory() as tmpdir:
            kb = KnowledgeBase(brain_root=tmpdir)
            entry1 = KnowledgeEntry(
                id="test-1",
                title="Test 1",
                content="Content",
                author="Agent-8",
                category="learning",
            )
            entry2 = KnowledgeEntry(
                id="test-2",
                title="Test 2",
                content="Content",
                author="Agent-8",
                category="decision",
            )
            kb.add_entry(entry1)
            kb.add_entry(entry2)
            results = kb.get_by_category("learning")
            assert len(results) == 1
            assert results[0].category == "learning"



