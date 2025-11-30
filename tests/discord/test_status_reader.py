"""
Tests for Discord Status Reader
================================

Comprehensive tests for src/discord_commander/status_reader.py

Author: Agent-7 (Web Development Specialist)
Date: 2025-11-29
Target: 80%+ coverage
"""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
from datetime import datetime, timedelta


class TestStatusReader:
    """Test StatusReader class."""

    @pytest.fixture
    def temp_workspace(self, tmp_path):
        """Create temporary workspace directory."""
        workspace = tmp_path / "agent_workspaces"
        workspace.mkdir()
        return workspace

    @pytest.fixture
    def status_reader(self, temp_workspace):
        """Create StatusReader instance."""
        from src.discord_commander.status_reader import StatusReader
        return StatusReader(workspace_dir=str(temp_workspace), cache_ttl=30)

    def test_initialization_defaults(self):
        """Test StatusReader initialization with defaults."""
        from src.discord_commander.status_reader import StatusReader

        reader = StatusReader()
        assert reader.workspace_dir == Path("agent_workspaces")
        assert reader.cache_ttl == 30
        assert len(reader.cache) == 0
        assert len(reader.cache_timestamps) == 0
        assert reader.max_cache_size == 20

    def test_initialization_custom_values(self, tmp_path):
        """Test StatusReader initialization with custom values."""
        from src.discord_commander.status_reader import StatusReader

        workspace = tmp_path / "custom_workspace"
        reader = StatusReader(workspace_dir=str(workspace), cache_ttl=60)
        assert reader.workspace_dir == workspace
        assert reader.cache_ttl == 60

    def test_read_agent_status_file_not_found(self, status_reader):
        """Test reading status when file doesn't exist."""
        result = status_reader.read_agent_status("Agent-1")
        assert result is None

    def test_read_agent_status_valid_file(self, status_reader, temp_workspace):
        """Test reading status from valid file."""
        agent_dir = temp_workspace / "Agent-1"
        agent_dir.mkdir()
        status_file = agent_dir / "status.json"

        status_data = {
            "agent_id": "Agent-1",
            "agent_name": "Test Agent",
            "status": "ACTIVE",
            "current_mission": "Test mission"
        }

        status_file.write_text(json.dumps(status_data))

        result = status_reader.read_agent_status("Agent-1")
        assert result is not None
        assert result["agent_id"] == "Agent-1"
        assert result["agent_name"] == "Test Agent"
        assert result["status"] == "ACTIVE"

    def test_read_agent_status_caching(self, status_reader, temp_workspace):
        """Test status caching mechanism."""
        agent_dir = temp_workspace / "Agent-1"
        agent_dir.mkdir()
        status_file = agent_dir / "status.json"
        status_file.write_text(json.dumps({"agent_id": "Agent-1", "status": "ACTIVE"}))

        # First read - should read from file
        result1 = status_reader.read_agent_status("Agent-1")
        assert result1 is not None

        # Second read - should use cache
        with patch('builtins.open', mock_open(read_data=json.dumps({"agent_id": "Agent-1", "status": "CHANGED"}))):
            result2 = status_reader.read_agent_status("Agent-1")
            # Should return cached value, not changed value
            assert result2["status"] == "ACTIVE"

    def test_read_agent_status_cache_expiry(self, status_reader, temp_workspace):
        """Test cache expiry after TTL."""
        agent_dir = temp_workspace / "Agent-1"
        agent_dir.mkdir()
        status_file = agent_dir / "status.json"
        status_file.write_text(json.dumps({"agent_id": "Agent-1", "status": "ACTIVE"}))

        # First read
        status_reader.read_agent_status("Agent-1")

        # Expire cache by setting old timestamp
        old_time = datetime.now() - timedelta(seconds=60)
        status_reader.cache_timestamps["Agent-1"] = old_time

        # Update file
        status_file.write_text(json.dumps({"agent_id": "Agent-1", "status": "UPDATED"}))

        # Second read - should read from file (cache expired)
        result = status_reader.read_agent_status("Agent-1")
        assert result["status"] == "UPDATED"

    def test_read_agent_status_invalid_json(self, status_reader, temp_workspace):
        """Test handling of invalid JSON."""
        agent_dir = temp_workspace / "Agent-1"
        agent_dir.mkdir()
        status_file = agent_dir / "status.json"
        status_file.write_text("invalid json {")

        result = status_reader.read_agent_status("Agent-1")
        assert result is None

    def test_read_agent_status_normalization(self, status_reader, temp_workspace):
        """Test status data normalization."""
        agent_dir = temp_workspace / "Agent-1"
        agent_dir.mkdir()
        status_file = agent_dir / "status.json"

        status_data = {
            "agent_id": "Agent-1",
            "status": "ACTIVE",
            "sprint_info": {"points_earned": 100},
            "points_summary": {"total_points": 200}
        }

        status_file.write_text(json.dumps(status_data))

        result = status_reader.read_agent_status("Agent-1")
        assert result["agent_id"] == "Agent-1"
        assert result["status"] == "ACTIVE"
        assert result["sprint_info"] == {"points_earned": 100}
        assert result["points_summary"] == {"total_points": 200}
        assert "points" in result

    def test_read_agent_status_normalization_defaults(self, status_reader, temp_workspace):
        """Test normalization with missing fields."""
        agent_dir = temp_workspace / "Agent-1"
        agent_dir.mkdir()
        status_file = agent_dir / "status.json"
        status_file.write_text(json.dumps({}))

        result = status_reader.read_agent_status("Agent-1")
        assert result["agent_id"] == "Unknown"
        assert result["agent_name"] == "Unknown Agent"
        assert result["status"] == "UNKNOWN"
        assert result["current_tasks"] == []
        assert result["completed_tasks"] == []

    def test_read_all_statuses(self, status_reader, temp_workspace):
        """Test reading all agent statuses."""
        # Create status files for multiple agents
        for i in range(1, 4):
            agent_dir = temp_workspace / f"Agent-{i}"
            agent_dir.mkdir()
            status_file = agent_dir / "status.json"
            status_file.write_text(json.dumps({"agent_id": f"Agent-{i}", "status": "ACTIVE"}))

        result = status_reader.read_all_statuses()
        assert len(result) == 3
        assert "Agent-1" in result
        assert "Agent-2" in result
        assert "Agent-3" in result

    def test_read_all_statuses_missing_directory(self, tmp_path):
        """Test reading all statuses when workspace doesn't exist."""
        from src.discord_commander.status_reader import StatusReader

        reader = StatusReader(workspace_dir=str(tmp_path / "nonexistent"))
        result = reader.read_all_statuses()
        assert len(result) == 0

    def test_read_all_statuses_skips_role_workspaces(self, status_reader, temp_workspace):
        """Test that only main agents (1-8) are read."""
        # Create main agent
        agent_dir = temp_workspace / "Agent-1"
        agent_dir.mkdir()
        (agent_dir / "status.json").write_text(json.dumps({"agent_id": "Agent-1"}))

        # Create role workspace (should be skipped)
        role_dir = temp_workspace / "Agent-SRC-1"
        role_dir.mkdir()
        (role_dir / "status.json").write_text(json.dumps({"agent_id": "Agent-SRC-1"}))

        result = status_reader.read_all_statuses()
        assert "Agent-1" in result
        assert "Agent-SRC-1" not in result

    def test_cache_eviction(self, status_reader, temp_workspace):
        """Test cache eviction when max size reached."""
        # Fill cache to max size
        for i in range(1, 22):  # 21 agents (exceeds max of 20)
            agent_dir = temp_workspace / f"Agent-{i}"
            agent_dir.mkdir()
            status_file = agent_dir / "status.json"
            status_file.write_text(json.dumps({"agent_id": f"Agent-{i}"}))

        # Read all agents
        for i in range(1, 22):
            status_reader.read_agent_status(f"Agent-{i}")

        # Cache should be at max size
        assert len(status_reader.cache) <= status_reader.max_cache_size

    def test_clear_cache(self, status_reader, temp_workspace):
        """Test cache clearing."""
        agent_dir = temp_workspace / "Agent-1"
        agent_dir.mkdir()
        (agent_dir / "status.json").write_text(json.dumps({"agent_id": "Agent-1"}))

        status_reader.read_agent_status("Agent-1")
        assert len(status_reader.cache) > 0

        status_reader.clear_cache()
        assert len(status_reader.cache) == 0
        assert len(status_reader.cache_timestamps) == 0

    def test_get_cache_stats(self, status_reader, temp_workspace):
        """Test cache statistics."""
        agent_dir = temp_workspace / "Agent-1"
        agent_dir.mkdir()
        (agent_dir / "status.json").write_text(json.dumps({"agent_id": "Agent-1"}))

        status_reader.read_agent_status("Agent-1")

        stats = status_reader.get_cache_stats()
        assert stats["cached_agents"] == 1
        assert stats["cache_ttl"] == 30
        assert stats["oldest_cache"] is not None
        assert stats["newest_cache"] is not None

    def test_get_cache_stats_empty_cache(self, status_reader):
        """Test cache statistics with empty cache."""
        stats = status_reader.get_cache_stats()
        assert stats["cached_agents"] == 0
        assert stats["oldest_cache"] is None
        assert stats["newest_cache"] is None

    def test_normalize_status_with_points_summary(self, status_reader):
        """Test normalization extracts points from points_summary."""
        data = {
            "agent_id": "Agent-1",
            "points_summary": {"legendary_total": 500}
        }
        result = status_reader._normalize_status(data)
        assert result["points"] == 500

    def test_normalize_status_with_sprint_info(self, status_reader):
        """Test normalization extracts points from sprint_info."""
        data = {
            "agent_id": "Agent-1",
            "sprint_info": {"points_earned": 300}
        }
        result = status_reader._normalize_status(data)
        assert result["points"] == 300

    def test_normalize_status_no_points(self, status_reader):
        """Test normalization when no points available."""
        data = {"agent_id": "Agent-1"}
        result = status_reader._normalize_status(data)
        assert "points" not in result
