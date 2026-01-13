#!/usr/bin/env python3
"""
Test Suite for Swarm Memory System
====================================

Comprehensive test suite for src/swarm_brain/swarm_memory.py.

Tests:
- SwarmMemory initialization
- Note taking functionality
- Learning sharing
- Decision recording
- Session logging
- Knowledge search
- Status updates

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-12-07
Priority: MEDIUM
"""

import json
import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.swarm_brain.swarm_memory import SwarmMemory
from src.swarm_brain.agent_notes import NoteType


class TestSwarmMemoryInitialization:
    """Test SwarmMemory initialization."""

    def test_swarm_memory_init(self):
        """Test SwarmMemory initialization."""
        with tempfile.TemporaryDirectory() as tmpdir:
            memory = SwarmMemory(
                agent_id="Agent-8",
                workspace_root=tmpdir,
                brain_root=tmpdir,
            )
            assert memory.agent_id == "Agent-8"
            assert memory.agent_notes is not None
            assert memory.knowledge_base is not None

    def test_swarm_memory_default_paths(self):
        """Test SwarmMemory with default paths."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("src.swarm_brain.swarm_memory.Path") as mock_path:
                mock_path.return_value = Path(tmpdir)
                memory = SwarmMemory(agent_id="Agent-8")
                assert memory.agent_id == "Agent-8"


class TestSwarmMemoryNotes:
    """Test note-taking functionality."""

    def test_take_note(self):
        """Test taking a personal note."""
        with tempfile.TemporaryDirectory() as tmpdir:
            memory = SwarmMemory(
                agent_id="Agent-8",
                workspace_root=tmpdir,
                brain_root=tmpdir,
            )
            with patch.object(memory.agent_notes, "add_note") as mock_add:
                mock_add.return_value = "note-1"
                memory.take_note("Test note", NoteType.IMPORTANT)
                mock_add.assert_called_once_with("Test note", NoteType.IMPORTANT)

    def test_take_note_default_type(self):
        """Test taking note with default type."""
        with tempfile.TemporaryDirectory() as tmpdir:
            memory = SwarmMemory(
                agent_id="Agent-8",
                workspace_root=tmpdir,
                brain_root=tmpdir,
            )
            with patch.object(memory.agent_notes, "add_note") as mock_add:
                memory.take_note("Test note")
                mock_add.assert_called_once_with("Test note", NoteType.IMPORTANT)


class TestSwarmMemoryLearning:
    """Test learning sharing functionality."""

    def test_share_learning(self):
        """Test sharing learning with swarm."""
        with tempfile.TemporaryDirectory() as tmpdir:
            memory = SwarmMemory(
                agent_id="Agent-8",
                workspace_root=tmpdir,
                brain_root=tmpdir,
            )
            entry_id = memory.share_learning(
                title="Test Learning",
                content="Test content",
                tags=["test", "qa"],
            )
            assert entry_id is not None
            assert entry_id.startswith("kb-")

    def test_share_learning_no_tags(self):
        """Test sharing learning without tags."""
        with tempfile.TemporaryDirectory() as tmpdir:
            memory = SwarmMemory(
                agent_id="Agent-8",
                workspace_root=tmpdir,
                brain_root=tmpdir,
            )
            entry_id = memory.share_learning(
                title="Test Learning",
                content="Test content",
            )
            assert entry_id is not None


class TestSwarmMemoryDecisions:
    """Test decision recording."""

    def test_record_decision(self):
        """Test recording a decision."""
        with tempfile.TemporaryDirectory() as tmpdir:
            memory = SwarmMemory(
                agent_id="Agent-8",
                workspace_root=tmpdir,
                brain_root=tmpdir,
            )
            memory.record_decision(
                title="Test Decision",
                decision="Use Python",
                rationale="Better for testing",
            )
            # Verify entry was added to knowledge base
            results = memory.knowledge_base.get_by_category("decision")
            assert len(results) == 1
            assert "Test Decision" in results[0].title


class TestSwarmMemorySession:
    """Test session logging."""

    def test_log_session(self):
        """Test logging a work session."""
        with tempfile.TemporaryDirectory() as tmpdir:
            memory = SwarmMemory(
                agent_id="Agent-8",
                workspace_root=tmpdir,
                brain_root=tmpdir,
            )
            with patch.object(memory.agent_notes, "log_work") as mock_log:
                memory.log_session("Session summary")
                mock_log.assert_called_once_with("Session summary")


class TestSwarmMemorySearch:
    """Test knowledge search functionality."""

    def test_search_swarm_knowledge(self):
        """Test searching swarm knowledge."""
        with tempfile.TemporaryDirectory() as tmpdir:
            memory = SwarmMemory(
                agent_id="Agent-8",
                workspace_root=tmpdir,
                brain_root=tmpdir,
            )
            memory.share_learning(
                title="Python Testing",
                content="Test content",
                tags=["python"],
            )
            results = memory.search_swarm_knowledge("Python")
            assert len(results) == 1
            assert results[0].title == "Python Testing"

    def test_search_swarm_knowledge_no_results(self):
        """Test search with no results."""
        with tempfile.TemporaryDirectory() as tmpdir:
            memory = SwarmMemory(
                agent_id="Agent-8",
                workspace_root=tmpdir,
                brain_root=tmpdir,
            )
            results = memory.search_swarm_knowledge("nonexistent")
            assert len(results) == 0


class TestSwarmMemoryNotesRetrieval:
    """Test note retrieval functionality."""

    def test_get_my_notes(self):
        """Test getting personal notes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            memory = SwarmMemory(
                agent_id="Agent-8",
                workspace_root=tmpdir,
                brain_root=tmpdir,
            )
            with patch.object(memory.agent_notes, "get_notes") as mock_get:
                mock_get.return_value = [{"id": "note-1", "content": "Test"}]
                notes = memory.get_my_notes()
                assert len(notes) == 1
                mock_get.assert_called_once_with(None)

    def test_get_my_notes_filtered(self):
        """Test getting notes filtered by type."""
        with tempfile.TemporaryDirectory() as tmpdir:
            memory = SwarmMemory(
                agent_id="Agent-8",
                workspace_root=tmpdir,
                brain_root=tmpdir,
            )
            with patch.object(memory.agent_notes, "get_notes") as mock_get:
                memory.get_my_notes(NoteType.LEARNING)
                mock_get.assert_called_once_with(NoteType.LEARNING)

    def test_get_my_learnings(self):
        """Test getting learning notes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            memory = SwarmMemory(
                agent_id="Agent-8",
                workspace_root=tmpdir,
                brain_root=tmpdir,
            )
            with patch.object(memory.agent_notes, "get_notes") as mock_get:
                memory.get_my_learnings()
                mock_get.assert_called_once_with(NoteType.LEARNING)


class TestSwarmMemoryStatusUpdate:
    """Test status update functionality."""

    def test_update_status_with_notes(self):
        """Test updating status.json with notes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            status_file = Path(tmpdir) / "status.json"
            status_data = {
                "agent_id": "Agent-8",
                "status": "ACTIVE",
            }
            status_file.write_text(json.dumps(status_data), encoding="utf-8")
            memory = SwarmMemory(
                agent_id="Agent-8",
                workspace_root=tmpdir,
                brain_root=tmpdir,
            )
            memory.update_status_with_notes(str(status_file))
            updated_status = json.loads(status_file.read_text(encoding="utf-8"))
            assert "agent_notes" in updated_status

    def test_update_status_with_notes_missing_file(self):
        """Test updating status when file doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            memory = SwarmMemory(
                agent_id="Agent-8",
                workspace_root=tmpdir,
                brain_root=tmpdir,
            )
            # Should not raise error
            memory.update_status_with_notes(str(Path(tmpdir) / "nonexistent.json"))



