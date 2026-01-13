"""
Unit Tests for Cycle Snapshot System - Phase 1
==============================================

Tests for Phase 1 modules (data collection, aggregation, reporting).

Author: Agent-3 (Infrastructure & DevOps Specialist)
Created: 2025-12-31
V2 Compliant: Yes

<!-- SSOT Domain: tests -->
"""

import json
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

import pytest

from tools.cycle_snapshots.data_collectors.agent_status_collector import (
    collect_agent_status,
    collect_all_agent_status,
    validate_status_json,
)
from tools.cycle_snapshots.data_collectors.task_log_collector import (
    parse_task_log,
    extract_task_metrics,
    compare_with_previous_snapshot,
)
from tools.cycle_snapshots.data_collectors.git_collector import (
    analyze_git_activity,
    get_commits_since,
    calculate_git_metrics,
)
from tools.cycle_snapshots.aggregators.snapshot_aggregator import (
    aggregate_snapshot,
    generate_snapshot_metadata,
    generate_project_state,
)
from tools.cycle_snapshots.processors.report_generator import (
    generate_markdown_report,
    format_agent_section,
    format_metrics_section,
)
from tools.cycle_snapshots.core.snapshot_models import (
    SnapshotMetadata,
    AgentAccomplishments,
    ProjectMetrics,
    CycleSnapshot,
)


class TestAgentStatusCollector:
    """Tests for agent status collector."""
    
    def test_validate_status_json_valid(self):
        """Test validation of valid status.json."""
        status = {
            "agent_id": "Agent-1",
            "agent_name": "Test Agent",
            "status": "ACTIVE",
            "completed_tasks": ["Task 1"],
        }
        assert validate_status_json(status) is True
    
    def test_validate_status_json_missing_field(self):
        """Test validation fails for missing required field."""
        status = {
            "agent_name": "Test Agent",
            "status": "ACTIVE",
        }
        assert validate_status_json(status) is False
    
    def test_validate_status_json_not_serializable(self):
        """Test validation fails for non-serializable data."""
        status = {
            "agent_id": "Agent-1",
            "agent_name": "Test Agent",
            "status": "ACTIVE",
            "bad_data": object(),  # Not JSON serializable
        }
        assert validate_status_json(status) is False
    
    def test_collect_agent_status_exists(self, tmp_path):
        """Test collecting status from existing file."""
        agent_dir = tmp_path / "agent_workspaces" / "Agent-1"
        agent_dir.mkdir(parents=True)
        
        status_file = agent_dir / "status.json"
        status_data = {
            "agent_id": "Agent-1",
            "agent_name": "Test Agent",
            "status": "ACTIVE",
        }
        status_file.write_text(json.dumps(status_data))
        
        result = collect_agent_status("Agent-1", tmp_path)
        assert result is not None
        assert result["agent_id"] == "Agent-1"
    
    def test_collect_agent_status_not_found(self, tmp_path):
        """Test collecting status from non-existent file."""
        result = collect_agent_status("Agent-99", tmp_path)
        assert result is None
    
    def test_collect_all_agent_status(self, tmp_path):
        """Test collecting status from all agents."""
        # Create test agent directories
        for i in range(1, 4):
            agent_dir = tmp_path / "agent_workspaces" / f"Agent-{i}"
            agent_dir.mkdir(parents=True)
            status_file = agent_dir / "status.json"
            status_data = {
                "agent_id": f"Agent-{i}",
                "agent_name": f"Test Agent {i}",
                "status": "ACTIVE",
            }
            status_file.write_text(json.dumps(status_data))
        
        result = collect_all_agent_status(tmp_path, agent_ids=["Agent-1", "Agent-2", "Agent-3"])
        assert len(result) == 3
        assert "Agent-1" in result
        assert "Agent-2" in result
        assert "Agent-3" in result


class TestTaskLogCollector:
    """Tests for task log collector."""
    
    def test_extract_task_metrics(self):
        """Test extracting task metrics from task log content."""
        content = """
## 📥 INBOX
- [ ] **HIGH**: Task 1
- [ ] **MEDIUM**: Task 2

## 📋 THIS WEEK
- [x] **HIGH**: Completed Task
- [ ] **LOW**: Task 3
"""
        metrics = extract_task_metrics(content)
        
        assert metrics["inbox_count"] == 2
        assert metrics["this_week_count"] == 2
        assert metrics["completed_count"] == 1
        assert metrics["by_priority"]["HIGH"] == 2
        assert metrics["by_priority"]["MEDIUM"] == 1
        assert metrics["by_priority"]["LOW"] == 1
    
    def test_parse_task_log_exists(self, tmp_path):
        """Test parsing existing task log file."""
        task_log_file = tmp_path / "MASTER_TASK_LOG.md"
        task_log_file.write_text("## 📥 INBOX\n- [ ] **HIGH**: Task 1\n")
        
        result = parse_task_log(tmp_path)
        assert "error" not in result
        assert "metrics" in result
        assert result["metrics"]["inbox_count"] == 1
    
    def test_parse_task_log_not_found(self, tmp_path):
        """Test parsing non-existent task log."""
        result = parse_task_log(tmp_path)
        assert "error" in result
        assert "MASTER_TASK_LOG.md not found" in result["error"]
    
    def test_compare_with_previous_snapshot(self):
        """Test comparing current and previous task metrics."""
        current = {
            "inbox_count": 5,
            "completed_count": 10,
            "by_priority": {"HIGH": 3, "MEDIUM": 2},
        }
        previous = {
            "inbox_count": 3,
            "completed_count": 8,
            "by_priority": {"HIGH": 2, "MEDIUM": 1},
        }
        
        comparison = compare_with_previous_snapshot(current, previous)
        assert comparison["new_tasks"] == 2
        assert comparison["completed_since_last"] == 2
        assert comparison["priority_changes"]["HIGH"] == 1


class TestGitCollector:
    """Tests for git collector."""
    
    def test_calculate_git_metrics_empty(self):
        """Test calculating metrics from empty commit list."""
        metrics = calculate_git_metrics([])
        assert metrics["commits"] == 0
        assert metrics["files_changed"] == 0
        assert metrics["authors"] == {}
    
    def test_calculate_git_metrics_with_commits(self):
        """Test calculating metrics from commits."""
        commits = [
            {"hash": "abc123", "author_name": "Agent-1", "message": "Test commit 1"},
            {"hash": "def456", "author_name": "Agent-2", "message": "Test commit 2"},
            {"hash": "ghi789", "author_name": "Agent-1", "message": "Test commit 3"},
        ]
        metrics = calculate_git_metrics(commits)
        
        assert metrics["commits"] == 3
        assert metrics["authors"]["Agent-1"] == 2
        assert metrics["authors"]["Agent-2"] == 1
        assert len(metrics["commit_messages"]) == 3
    
    @patch("tools.cycle_snapshots.data_collectors.git_collector.subprocess.run")
    def test_get_commits_since_success(self, mock_subprocess, tmp_path):
        """Test getting commits since timestamp."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "abc123|Agent-1|agent1@test.com|2025-12-31 10:00:00|Test commit\n"
        mock_subprocess.return_value = mock_result
        
        since = datetime.now() - timedelta(hours=24)
        commits = get_commits_since(since, tmp_path)
        
        assert len(commits) == 1
        assert commits[0]["hash"] == "abc123"
        assert commits[0]["author_name"] == "Agent-1"
    
    @patch("tools.cycle_snapshots.data_collectors.git_collector.subprocess.run")
    def test_analyze_git_activity_not_repo(self, mock_subprocess, tmp_path):
        """Test analyzing git activity when not a git repository."""
        result = analyze_git_activity(tmp_path)
        assert "error" in result
        assert "Not a git repository" in result["error"]


class TestSnapshotAggregator:
    """Tests for snapshot aggregator."""
    
    def test_generate_snapshot_metadata(self):
        """Test generating snapshot metadata."""
        metadata = generate_snapshot_metadata(
            cycle_num=10,
            workspace_root=Path("/test"),
            previous_cycle=9,
        )
        
        assert metadata.cycle_number == 10
        assert metadata.previous_cycle == 9
        assert metadata.workspace_root == "/test"
    
    def test_generate_project_state(self):
        """Test generating project state from metrics."""
        metrics = {
            "total_agents": 5,
            "total_completed_tasks": 20,
            "total_achievements": 10,
            "active_tasks_count": 8,
        }
        
        state = generate_project_state(metrics)
        assert state["total_agents"] == 5
        assert state["total_completed_tasks"] == 20
        assert state["productivity_indicators"]["tasks_per_agent"] == 4.0
    
    def test_aggregate_snapshot(self):
        """Test aggregating complete snapshot."""
        all_data = {
            "agent_status": {
                "Agent-1": {
                    "agent_id": "Agent-1",
                    "agent_name": "Test Agent",
                    "completed_tasks": ["Task 1"],
                    "achievements": ["Achievement 1"],
                    "current_tasks": ["Task 2"],
                    "current_mission": "Test Mission",
                    "mission_priority": "HIGH",
                    "cycle_count": 10,
                }
            },
            "task_log": {"metrics": {"inbox_count": 5}},
            "git_activity": {"metrics": {"commits": 3}},
        }
        
        snapshot = aggregate_snapshot(
            all_data=all_data,
            cycle_num=10,
            workspace_root=Path("/test"),
        )
        
        assert snapshot.metadata.cycle_number == 10
        assert len(snapshot.agent_accomplishments) == 1
        assert snapshot.project_metrics.total_agents == 1
        assert snapshot.project_metrics.total_completed_tasks == 1


class TestReportGenerator:
    """Tests for report generator."""
    
    def test_format_agent_section(self):
        """Test formatting agent section."""
        agent_data = {
            "agent_name": "Test Agent",
            "current_mission": "Test Mission",
            "completed_tasks": ["Task 1", "Task 2"],
            "achievements": ["Achievement 1"],
            "current_tasks": ["Task 3"],
        }
        
        section = format_agent_section("Agent-1", agent_data)
        assert "Agent-1" in section
        assert "Test Agent" in section
        assert "Test Mission" in section
        assert "Task 1" in section
    
    def test_format_metrics_section(self):
        """Test formatting metrics section."""
        metrics = {
            "total_agents": 5,
            "total_completed_tasks": 20,
            "total_achievements": 10,
            "active_tasks_count": 8,
            "git_commits": 15,
            "git_files_changed": 42,
        }
        
        section = format_metrics_section(metrics)
        assert "Project Metrics" in section
        assert "5" in section
        assert "20" in section
    
    def test_generate_markdown_report(self):
        """Test generating complete markdown report."""
        snapshot = {
            "snapshot_metadata": {
                "cycle": 10,
                "date": "2025-12-31T10:00:00",
                "previous_cycle": 9,
            },
            "agent_accomplishments": {
                "Agent-1": {
                    "agent_id": "Agent-1",
                    "agent_name": "Test Agent",
                    "completed_tasks": ["Task 1"],
                    "achievements": ["Achievement 1"],
                    "current_tasks": ["Task 2"],
                }
            },
            "project_metrics": {
                "total_agents": 1,
                "total_completed_tasks": 1,
                "total_achievements": 1,
                "active_tasks_count": 1,
            },
        }
        
        report = generate_markdown_report(snapshot)
        assert "# Cycle Snapshot" in report
        assert "Cycle 10" in report
        assert "Agent-1" in report
        assert "Test Agent" in report


class TestErrorHandling:
    """Tests for error handling."""
    
    def test_agent_status_collector_invalid_json(self, tmp_path):
        """Test handling invalid JSON in status file."""
        agent_dir = tmp_path / "agent_workspaces" / "Agent-1"
        agent_dir.mkdir(parents=True)
        status_file = agent_dir / "status.json"
        status_file.write_text("invalid json{")
        
        result = collect_agent_status("Agent-1", tmp_path)
        assert result is None
    
    def test_task_log_collector_parse_error(self, tmp_path):
        """Test handling task log parse errors."""
        task_log_file = tmp_path / "MASTER_TASK_LOG.md"
        # Create file that might cause issues
        task_log_file.write_text("")
        
        result = parse_task_log(tmp_path)
        # Should return empty metrics, not crash
        assert "metrics" in result


class TestEdgeCases:
    """Tests for edge cases."""
    
    def test_empty_agent_status(self):
        """Test handling empty agent status collection."""
        result = collect_all_agent_status(Path("/nonexistent"))
        assert result == {}
    
    def test_snapshot_with_no_agents(self):
        """Test aggregating snapshot with no agents."""
        all_data = {
            "agent_status": {},
            "task_log": {"metrics": {}},
            "git_activity": {"metrics": {}},
        }
        
        snapshot = aggregate_snapshot(all_data, cycle_num=1)
        assert snapshot.project_metrics.total_agents == 0
        assert len(snapshot.agent_accomplishments) == 0
    
    def test_report_with_empty_data(self):
        """Test generating report with empty data."""
        snapshot = {
            "snapshot_metadata": {"cycle": 1, "date": "2025-12-31T10:00:00"},
            "agent_accomplishments": {},
            "project_metrics": {
                "total_agents": 0,
                "total_completed_tasks": 0,
                "total_achievements": 0,
                "active_tasks_count": 0,
            },
        }
        
        report = generate_markdown_report(snapshot)
        assert "Cycle Snapshot" in report
        assert "0" in report  # Should show zero agents

