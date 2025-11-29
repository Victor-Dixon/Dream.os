"""
Unit tests for daily_cycle_tracker.py - Infrastructure Test Coverage

Tests DailyCycleTracker class and daily cycle tracking operations.
Target: ≥85% coverage, comprehensive test suite.
"""

import pytest
from unittest.mock import Mock, patch, mock_open
from pathlib import Path
import json
import os
import sys
from datetime import datetime, timezone, date

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.daily_cycle_tracker import DailyCycleTracker


class TestDailyCycleTracker:
    """Test suite for DailyCycleTracker class."""

    def test_initialization(self, tmp_path):
        """Test tracker initialization creates workspace."""
        workspace_dir = tmp_path / "agent_workspaces" / "TestAgent"
        with patch('src.core.daily_cycle_tracker.Path') as mock_path:
            mock_path.side_effect = lambda x: Path(str(x).replace("agent_workspaces/TestAgent", str(workspace_dir)))
            tracker = DailyCycleTracker("TestAgent")
            tracker.workspace = workspace_dir
            
            assert tracker.agent_id == "TestAgent"
            assert hasattr(tracker, 'workspace')

    def test_load_cycles_from_file(self, tmp_path):
        """Test loading cycles from existing file."""
        workspace_dir = tmp_path / "agent_workspaces" / "Agent-3"
        workspace_dir.mkdir(parents=True)
        cycle_file = workspace_dir / "daily_cycles.json"
        
        existing_data = {
            "agent_id": "Agent-3",
            "current_day": "2025-01-27",
            "current_cycle_date": "2025-01-27",
            "daily_cycles": {"2025-01-27": {"date": "2025-01-27"}},
            "total_days": 1,
            "last_updated": datetime.now(timezone.utc).isoformat()
        }
        cycle_file.write_text(json.dumps(existing_data))
        
        tracker = DailyCycleTracker("Agent-3")
        tracker.workspace = workspace_dir
        tracker.cycle_file = cycle_file
        tracker._load_cycles()
        
        assert tracker.cycles["agent_id"] == "Agent-3"
        assert tracker.cycles["current_day"] == "2025-01-27"

    def test_start_new_day(self, tmp_path):
        """Test starting new day creates day entry."""
        workspace_dir = tmp_path / "agent_workspaces" / "Agent-3"
        workspace_dir.mkdir(parents=True)
        
        tracker = DailyCycleTracker("Agent-3")
        tracker.workspace = workspace_dir
        tracker.cycle_file = workspace_dir / "daily_cycles.json"
        tracker._load_cycles()
        
        today = date.today().isoformat()
        result = tracker.start_new_day()
        
        assert today in tracker.cycles["daily_cycles"]
        assert tracker.cycles["current_cycle_date"] == today

    def test_record_interaction(self, tmp_path):
        """Test recording interaction increments count."""
        workspace_dir = tmp_path / "agent_workspaces" / "Agent-3"
        workspace_dir.mkdir(parents=True)
        
        tracker = DailyCycleTracker("Agent-3")
        tracker.workspace = workspace_dir
        tracker.cycle_file = workspace_dir / "daily_cycles.json"
        tracker._load_cycles()
        
        tracker.start_new_day()
        tracker.record_interaction()
        
        today = date.today().isoformat()
        assert tracker.cycles["daily_cycles"][today]["interaction_count"] == 1

    def test_record_task_completed(self, tmp_path):
        """Test recording completed task adds task and points."""
        workspace_dir = tmp_path / "agent_workspaces" / "Agent-3"
        workspace_dir.mkdir(parents=True)
        
        tracker = DailyCycleTracker("Agent-3")
        tracker.workspace = workspace_dir
        tracker.cycle_file = workspace_dir / "daily_cycles.json"
        tracker._load_cycles()
        
        tracker.start_new_day()
        tracker.record_task_completed("Test Task", points=10)
        
        today = date.today().isoformat()
        day_data = tracker.cycles["daily_cycles"][today]
        
        assert len(day_data["tasks_completed"]) == 1
        assert day_data["points_earned"] == 10

    def test_record_commit(self, tmp_path):
        """Test recording commit increments commit count."""
        workspace_dir = tmp_path / "agent_workspaces" / "Agent-3"
        workspace_dir.mkdir(parents=True)
        
        tracker = DailyCycleTracker("Agent-3")
        tracker.workspace = workspace_dir
        tracker.cycle_file = workspace_dir / "daily_cycles.json"
        tracker._load_cycles()
        
        tracker.start_new_day()
        tracker.record_commit()
        
        today = date.today().isoformat()
        assert tracker.cycles["daily_cycles"][today]["commits_made"] == 1

    def test_get_today_summary(self, tmp_path):
        """Test getting today's summary returns correct data."""
        workspace_dir = tmp_path / "agent_workspaces" / "Agent-3"
        workspace_dir.mkdir(parents=True)
        
        tracker = DailyCycleTracker("Agent-3")
        tracker.workspace = workspace_dir
        tracker.cycle_file = workspace_dir / "daily_cycles.json"
        tracker._load_cycles()
        
        tracker.start_new_day()
        tracker.record_interaction()
        tracker.record_task_completed("Task 1", points=10)
        
        summary = tracker.get_today_summary()
        
        assert summary["tasks_completed"] == 1
        assert summary["points_earned"] == 10
        assert summary["interactions"] == 1

    def test_add_blocker(self, tmp_path):
        """Test adding blocker adds to blockers list."""
        workspace_dir = tmp_path / "agent_workspaces" / "Agent-3"
        workspace_dir.mkdir(parents=True)
        
        tracker = DailyCycleTracker("Agent-3")
        tracker.workspace = workspace_dir
        tracker.cycle_file = workspace_dir / "daily_cycles.json"
        tracker._load_cycles()
        
        tracker.start_new_day()
        tracker.add_blocker("Test blocker")
        
        today = date.today().isoformat()
        blockers = tracker.cycles["daily_cycles"][today]["blockers"]
        
        assert len(blockers) == 1
        assert blockers[0]["blocker"] == "Test blocker"

    def test_mark_ready_for_push(self, tmp_path):
        """Test marking ready for push sets flag."""
        workspace_dir = tmp_path / "agent_workspaces" / "Agent-3"
        workspace_dir.mkdir(parents=True)
        
        tracker = DailyCycleTracker("Agent-3")
        tracker.workspace = workspace_dir
        tracker.cycle_file = workspace_dir / "daily_cycles.json"
        tracker._load_cycles()
        
        tracker.start_new_day()
        tracker.mark_ready_for_push()
        
        today = date.today().isoformat()
        assert tracker.cycles["daily_cycles"][today]["ready_for_push"] is True

    def test_mark_pushed(self, tmp_path):
        """Test marking pushed sets flag."""
        workspace_dir = tmp_path / "agent_workspaces" / "Agent-3"
        workspace_dir.mkdir(parents=True)
        
        tracker = DailyCycleTracker("Agent-3")
        tracker.workspace = workspace_dir
        tracker.cycle_file = workspace_dir / "daily_cycles.json"
        tracker._load_cycles()
        
        tracker.start_new_day()
        tracker.mark_pushed()
        
        today = date.today().isoformat()
        assert tracker.cycles["daily_cycles"][today]["pushed"] is True

    def test_end_day(self, tmp_path):
        """Test ending day sets end time and ready flag."""
        workspace_dir = tmp_path / "agent_workspaces" / "Agent-3"
        workspace_dir.mkdir(parents=True)
        
        tracker = DailyCycleTracker("Agent-3")
        tracker.workspace = workspace_dir
        tracker.cycle_file = workspace_dir / "daily_cycles.json"
        tracker._load_cycles()
        
        tracker.start_new_day()
        tracker._end_day()
        
        today = date.today().isoformat()
        day_data = tracker.cycles["daily_cycles"][today]
        
        assert day_data["end_time"] is not None
        assert day_data["ready_for_push"] is True

    def test_save_cycles(self, tmp_path):
        """Test saving cycles writes to file."""
        workspace_dir = tmp_path / "agent_workspaces" / "Agent-3"
        workspace_dir.mkdir(parents=True)
        
        tracker = DailyCycleTracker("Agent-3")
        tracker.workspace = workspace_dir
        tracker.cycle_file = workspace_dir / "daily_cycles.json"
        tracker._load_cycles()
        
        tracker.start_new_day()
        tracker._save_cycles()
        
        assert tracker.cycle_file.exists()
        
        # Verify file contents
        data = json.loads(tracker.cycle_file.read_text())
        assert data["agent_id"] == "Agent-3"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
