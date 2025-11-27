#!/usr/bin/env python3
"""
Tests for Agent Lifecycle
==========================

Tests for automatic status.json management system.

Author: Agent-7
Date: 2025-11-27
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone

from src.core.agent_lifecycle import AgentLifecycle


class TestAgentLifecycle:
    """Test suite for AgentLifecycle."""

    @pytest.fixture
    def temp_workspace(self):
        """Create temporary workspace for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir) / "agent_workspaces" / "Agent-7"
            workspace.mkdir(parents=True, exist_ok=True)
            yield workspace

    @pytest.fixture
    def lifecycle(self, temp_workspace, monkeypatch):
        """Create AgentLifecycle instance with temp workspace."""
        with patch('src.core.agent_lifecycle.Path') as mock_path:
            mock_path.return_value = temp_workspace
            lifecycle = AgentLifecycle('Agent-7')
            lifecycle.workspace = temp_workspace
            lifecycle.status_file = temp_workspace / "status.json"
            yield lifecycle

    def test_initialization(self, lifecycle):
        """Test AgentLifecycle initialization."""
        assert lifecycle.agent_id == "Agent-7"
        assert lifecycle.workspace is not None
        assert lifecycle.status_file is not None

    def test_create_default_status(self, lifecycle):
        """Test default status creation."""
        status = lifecycle._create_default_status()
        assert status["agent_id"] == "Agent-7"
        assert status["status"] == "IDLE"
        assert status["current_phase"] == "Initialized"
        assert "last_updated" in status
        assert status["current_tasks"] == []
        assert status["completed_tasks"] == []

    def test_load_status_existing(self, lifecycle):
        """Test loading existing status."""
        # Create existing status file
        status_data = {
            "agent_id": "Agent-7",
            "status": "ACTIVE",
            "current_phase": "Testing"
        }
        lifecycle.status_file.write_text(json.dumps(status_data))
        
        lifecycle._load_status()
        assert lifecycle.status["status"] == "ACTIVE"
        assert lifecycle.status["current_phase"] == "Testing"

    def test_load_status_new(self, lifecycle):
        """Test loading new status (creates default)."""
        if lifecycle.status_file.exists():
            lifecycle.status_file.unlink()
        
        lifecycle._load_status()
        assert lifecycle.status["agent_id"] == "Agent-7"
        assert lifecycle.status["status"] == "IDLE"

    def test_save_status(self, lifecycle):
        """Test saving status."""
        lifecycle.status["test_field"] = "test_value"
        lifecycle._save_status()
        
        assert lifecycle.status_file.exists()
        loaded = json.loads(lifecycle.status_file.read_text())
        assert loaded["test_field"] == "test_value"
        assert "last_updated" in loaded

    def test_start_cycle(self, lifecycle):
        """Test starting a cycle."""
        lifecycle.start_cycle()
        
        assert lifecycle.status["status"] == "ACTIVE_AGENT_MODE"
        assert lifecycle.status["current_phase"] == "TASK_EXECUTION"
        assert lifecycle.status["cycle_count"] > 0

    def test_start_mission(self, lifecycle):
        """Test starting a mission."""
        lifecycle.start_mission("Test Mission", "HIGH")
        
        assert lifecycle.status["current_mission"] == "Test Mission"
        assert lifecycle.status["mission_priority"] == "HIGH"

    def test_complete_task(self, lifecycle):
        """Test completing a task."""
        lifecycle.complete_task("Test Task", points=100)
        
        assert "Test Task" in lifecycle.status["completed_tasks"]
        assert lifecycle.status["points_earned"] == 100

    @patch('subprocess.run')
    def test_commit_to_git(self, mock_run, lifecycle):
        """Test git commit functionality."""
        mock_run.return_value = MagicMock(returncode=0)
        
        result = lifecycle._commit_to_git("Test commit")
        
        assert mock_run.called
        assert result is True

    def test_add_task(self, lifecycle):
        """Test adding a task."""
        lifecycle.add_task("New Task")
        
        assert "New Task" in lifecycle.status["current_tasks"]

    def test_add_achievement(self, lifecycle):
        """Test adding an achievement."""
        lifecycle.add_achievement("Test Achievement")
        
        assert "Test Achievement" in lifecycle.status["achievements"]

    def test_end_cycle(self, lifecycle):
        """Test ending a cycle."""
        lifecycle.start_cycle()
        initial_count = lifecycle.status["cycle_count"]
        
        lifecycle.end_cycle(commit=False)
        
        assert lifecycle.status["status"] == "IDLE"
        assert lifecycle.status["cycle_count"] == initial_count

