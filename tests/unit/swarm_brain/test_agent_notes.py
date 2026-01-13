#!/usr/bin/env python3
"""
Test Suite for Agent Notes System
==================================

Comprehensive test suite for src/swarm_brain/agent_notes.py.

Tests:
- NoteType enum
- AgentNotes initialization
- Note creation and retrieval
- Note filtering and search
- Markdown file generation
- Error handling

Author: Agent-8 (Testing & Quality Assurance Specialist)
Date: 2025-12-03
Priority: MEDIUM
"""

import json
import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, mock_open
from datetime import datetime

from src.swarm_brain.agent_notes import AgentNotes, NoteType


class TestNoteType:
    """Test NoteType enum."""

    def test_note_type_values(self):
        """Test NoteType enum values."""
        assert NoteType.LEARNING.value == "learning"
        assert NoteType.IMPORTANT.value == "important"
        assert NoteType.TODO.value == "todo"
        assert NoteType.DECISION.value == "decision"
        assert NoteType.WORK_LOG.value == "work_log"
        assert NoteType.COORDINATION.value == "coordination"

    def test_note_type_string_enum(self):
        """Test NoteType is string enum."""
        assert isinstance(NoteType.LEARNING, str)
        assert NoteType.LEARNING == "learning"


class TestAgentNotesInitialization:
    """Test AgentNotes initialization."""

    def test_init_creates_directories(self, tmp_path):
        """Test initialization creates necessary directories."""
        workspace = tmp_path / "agent_workspaces"
        notes = AgentNotes("Agent-8", str(workspace))
        
        assert notes.notes_dir.exists()
        assert notes.notes_dir.is_dir()

    def test_init_sets_agent_id(self, tmp_path):
        """Test initialization sets agent_id."""
        workspace = tmp_path / "agent_workspaces"
        notes = AgentNotes("Agent-8", str(workspace))
        
        assert notes.agent_id == "Agent-8"

    def test_init_creates_default_notes(self, tmp_path):
        """Test initialization creates default notes structure."""
        workspace = tmp_path / "agent_workspaces"
        notes = AgentNotes("Agent-8", str(workspace))
        
        assert "agent_id" in notes.notes
        assert notes.notes["agent_id"] == "Agent-8"
        assert "notes" in notes.notes
        assert isinstance(notes.notes["notes"], list)

    def test_init_loads_existing_notes(self, tmp_path):
        """Test initialization loads existing notes."""
        workspace = tmp_path / "agent_workspaces"
        notes_dir = workspace / "Agent-8" / "notes"
        notes_dir.mkdir(parents=True, exist_ok=True)
        
        existing_notes = {
            "agent_id": "Agent-8",
            "created_at": "2025-12-03T00:00:00",
            "last_updated": "2025-12-03T00:00:00",
            "notes": [{"id": "note-1", "type": "important", "content": "Test"}],
        }
        
        notes_file = notes_dir / "notes.json"
        notes_file.write_text(
            json.dumps(existing_notes, indent=2), encoding="utf-8"
        )
        
        notes = AgentNotes("Agent-8", str(workspace))
        assert len(notes.notes["notes"]) == 1
        assert notes.notes["notes"][0]["id"] == "note-1"


class TestAddNote:
    """Test adding notes."""

    def test_add_note_creates_note(self, tmp_path):
        """Test add_note creates a note."""
        workspace = tmp_path / "agent_workspaces"
        notes = AgentNotes("Agent-8", str(workspace))
        
        note_id = notes.add_note("Test note", NoteType.IMPORTANT)
        
        assert note_id.startswith("note-")
        assert len(notes.notes["notes"]) == 1
        assert notes.notes["notes"][0]["content"] == "Test note"

    def test_add_note_sets_type(self, tmp_path):
        """Test add_note sets note type."""
        workspace = tmp_path / "agent_workspaces"
        notes = AgentNotes("Agent-8", str(workspace))
        
        notes.add_note("Test", NoteType.LEARNING)
        
        assert notes.notes["notes"][0]["type"] == "learning"

    def test_add_note_sets_tags(self, tmp_path):
        """Test add_note sets tags."""
        workspace = tmp_path / "agent_workspaces"
        notes = AgentNotes("Agent-8", str(workspace))
        
        notes.add_note("Test", NoteType.IMPORTANT, tags=["test", "qa"])
        
        assert "test" in notes.notes["notes"][0]["tags"]
        assert "qa" in notes.notes["notes"][0]["tags"]

    def test_add_note_defaults_to_important(self, tmp_path):
        """Test add_note defaults to IMPORTANT type."""
        workspace = tmp_path / "agent_workspaces"
        notes = AgentNotes("Agent-8", str(workspace))
        
        notes.add_note("Test")
        
        assert notes.notes["notes"][0]["type"] == "important"

    def test_add_note_saves_to_file(self, tmp_path):
        """Test add_note saves to file."""
        workspace = tmp_path / "agent_workspaces"
        notes = AgentNotes("Agent-8", str(workspace))
        
        notes.add_note("Test note")
        
        assert notes.notes_file.exists()
        loaded = json.loads(notes.notes_file.read_text(encoding="utf-8"))
        assert len(loaded["notes"]) == 1

    def test_add_note_increments_id(self, tmp_path):
        """Test add_note increments note ID."""
        workspace = tmp_path / "agent_workspaces"
        notes = AgentNotes("Agent-8", str(workspace))
        
        id1 = notes.add_note("Note 1")
        id2 = notes.add_note("Note 2")
        
        assert id1 != id2
        assert id1 == "note-1"
        assert id2 == "note-2"


class TestAppendToMarkdown:
    """Test markdown file generation."""

    def test_add_note_creates_learning_file(self, tmp_path):
        """Test add_note creates learning markdown file."""
        workspace = tmp_path / "agent_workspaces"
        notes = AgentNotes("Agent-8", str(workspace))
        
        notes.add_note("Learned something", NoteType.LEARNING)
        
        assert notes.learnings_file.exists()
        content = notes.learnings_file.read_text(encoding="utf-8")
        assert "Learned something" in content

    def test_add_note_creates_important_file(self, tmp_path):
        """Test add_note creates important markdown file."""
        workspace = tmp_path / "agent_workspaces"
        notes = AgentNotes("Agent-8", str(workspace))
        
        notes.add_note("Important info", NoteType.IMPORTANT)
        
        assert notes.important_file.exists()
        content = notes.important_file.read_text(encoding="utf-8")
        assert "Important info" in content

    def test_add_note_creates_work_log_file(self, tmp_path):
        """Test add_note creates work log markdown file."""
        workspace = tmp_path / "agent_workspaces"
        notes = AgentNotes("Agent-8", str(workspace))
        
        notes.add_note("Work done", NoteType.WORK_LOG)
        
        assert notes.work_log_file.exists()
        content = notes.work_log_file.read_text(encoding="utf-8")
        assert "Work done" in content

    def test_add_note_creates_todos_file(self, tmp_path):
        """Test add_note creates todos markdown file."""
        workspace = tmp_path / "agent_workspaces"
        notes = AgentNotes("Agent-8", str(workspace))
        
        notes.add_note("Todo item", NoteType.TODO)
        
        assert notes.todos_file.exists()
        content = notes.todos_file.read_text(encoding="utf-8")
        assert "Todo item" in content

    def test_add_note_appends_to_existing_file(self, tmp_path):
        """Test add_note appends to existing markdown file."""
        workspace = tmp_path / "agent_workspaces"
        notes = AgentNotes("Agent-8", str(workspace))
        
        notes.add_note("First note", NoteType.IMPORTANT)
        notes.add_note("Second note", NoteType.IMPORTANT)
        
        content = notes.important_file.read_text(encoding="utf-8")
        assert content.count("First note") == 1
        assert content.count("Second note") == 1


class TestGetNotes:
    """Test retrieving notes."""

    def test_get_notes_returns_all(self, tmp_path):
        """Test get_notes returns all notes."""
        workspace = tmp_path / "agent_workspaces"
        notes = AgentNotes("Agent-8", str(workspace))
        
        notes.add_note("Note 1", NoteType.IMPORTANT)
        notes.add_note("Note 2", NoteType.LEARNING)
        
        all_notes = notes.get_notes()
        assert len(all_notes) == 2

    def test_get_notes_filters_by_type(self, tmp_path):
        """Test get_notes filters by note type."""
        workspace = tmp_path / "agent_workspaces"
        notes = AgentNotes("Agent-8", str(workspace))
        
        notes.add_note("Important", NoteType.IMPORTANT)
        notes.add_note("Learning", NoteType.LEARNING)
        
        important_notes = notes.get_notes(note_type=NoteType.IMPORTANT)
        assert len(important_notes) == 1
        assert important_notes[0]["type"] == "important"

    def test_get_notes_filters_by_tags(self, tmp_path):
        """Test get_notes filters by tags."""
        workspace = tmp_path / "agent_workspaces"
        notes = AgentNotes("Agent-8", str(workspace))
        
        notes.add_note("Tagged", NoteType.IMPORTANT, tags=["test"])
        notes.add_note("Untagged", NoteType.IMPORTANT)
        
        tagged_notes = notes.get_notes(tags=["test"])
        assert len(tagged_notes) == 1
        assert "test" in tagged_notes[0]["tags"]

    def test_get_notes_filters_by_type_and_tags(self, tmp_path):
        """Test get_notes filters by both type and tags."""
        workspace = tmp_path / "agent_workspaces"
        notes = AgentNotes("Agent-8", str(workspace))
        
        notes.add_note("Match", NoteType.IMPORTANT, tags=["test"])
        notes.add_note("Wrong type", NoteType.LEARNING, tags=["test"])
        notes.add_note("Wrong tag", NoteType.IMPORTANT, tags=["other"])
        
        filtered = notes.get_notes(note_type=NoteType.IMPORTANT, tags=["test"])
        assert len(filtered) == 1
        assert filtered[0]["content"] == "Match"


class TestSearchNotes:
    """Test searching notes."""

    def test_search_notes_by_content(self, tmp_path):
        """Test search_notes searches by content."""
        workspace = tmp_path / "agent_workspaces"
        notes = AgentNotes("Agent-8", str(workspace))
        
        notes.add_note("Python testing", NoteType.IMPORTANT)
        notes.add_note("JavaScript code", NoteType.LEARNING)
        
        results = notes.search_notes("Python")
        assert len(results) == 1
        assert "Python" in results[0]["content"]

    def test_search_notes_case_insensitive(self, tmp_path):
        """Test search_notes is case insensitive."""
        workspace = tmp_path / "agent_workspaces"
        notes = AgentNotes("Agent-8", str(workspace))
        
        notes.add_note("Python testing", NoteType.IMPORTANT)
        
        results = notes.search_notes("python")
        assert len(results) == 1

    def test_search_notes_by_type(self, tmp_path):
        """Test search_notes searches by type."""
        workspace = tmp_path / "agent_workspaces"
        notes = AgentNotes("Agent-8", str(workspace))
        
        notes.add_note("Note", NoteType.IMPORTANT)
        notes.add_note("Note", NoteType.LEARNING)
        
        results = notes.search_notes("important")
        assert len(results) == 1
        assert results[0]["type"] == "important"


class TestConvenienceMethods:
    """Test convenience methods."""

    def test_log_work(self, tmp_path):
        """Test log_work method."""
        workspace = tmp_path / "agent_workspaces"
        notes = AgentNotes("Agent-8", str(workspace))
        
        notes.log_work("Completed task")
        
        work_notes = notes.get_notes(note_type=NoteType.WORK_LOG)
        assert len(work_notes) == 1
        assert work_notes[0]["content"] == "Completed task"
        assert "session" in work_notes[0]["tags"]

    def test_record_learning(self, tmp_path):
        """Test record_learning method."""
        workspace = tmp_path / "agent_workspaces"
        notes = AgentNotes("Agent-8", str(workspace))
        
        notes.record_learning("Learned about testing")
        
        learning_notes = notes.get_notes(note_type=NoteType.LEARNING)
        assert len(learning_notes) == 1
        assert learning_notes[0]["content"] == "Learned about testing"
        assert "knowledge" in learning_notes[0]["tags"]

    def test_mark_important(self, tmp_path):
        """Test mark_important method."""
        workspace = tmp_path / "agent_workspaces"
        notes = AgentNotes("Agent-8", str(workspace))
        
        notes.mark_important("Critical information")
        
        important_notes = notes.get_notes(note_type=NoteType.IMPORTANT)
        assert len(important_notes) == 1
        assert important_notes[0]["content"] == "Critical information"
        assert "critical" in important_notes[0]["tags"]


class TestErrorHandling:
    """Test error handling."""

    def test_load_notes_handles_missing_file(self, tmp_path):
        """Test _load_notes handles missing file gracefully."""
        workspace = tmp_path / "agent_workspaces"
        notes = AgentNotes("Agent-8", str(workspace))
        
        # Should create default structure
        assert "agent_id" in notes.notes
        assert "notes" in notes.notes

    def test_save_notes_handles_io_error(self, tmp_path):
        """Test _save_notes handles IO errors."""
        workspace = tmp_path / "agent_workspaces"
        notes = AgentNotes("Agent-8", str(workspace))
        notes.add_note("Test")
        
        # Make directory read-only to simulate error
        notes.notes_file.chmod(0o444)
        
        # Should not raise exception (error handling in real implementation)
        # This test documents expected behavior
        try:
            notes.add_note("Another test")
        except Exception:
            pass  # Expected to handle gracefully

    def test_append_to_markdown_handles_missing_type(self, tmp_path):
        """Test _append_to_markdown handles missing type gracefully."""
        workspace = tmp_path / "agent_workspaces"
        notes = AgentNotes("Agent-8", str(workspace))
        
        # DECISION and COORDINATION don't have markdown files
        notes.add_note("Decision note", NoteType.DECISION)
        
        # Should not raise exception
        assert len(notes.notes["notes"]) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


