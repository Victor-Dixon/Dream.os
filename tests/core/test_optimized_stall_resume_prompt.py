#!/usr/bin/env python3
"""
Unit Tests for Optimized Stall Resume Prompt
============================================
"""

import pytest
import json
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
from src.core.optimized_stall_resume_prompt import (
    OptimizedStallResumePrompt,
    generate_optimized_resume_prompt,
)


class TestOptimizedStallResumePrompt:
    """Tests for OptimizedStallResumePrompt."""

    def test_initialization_default(self):
        """Test initialization with default workspace."""
        generator = OptimizedStallResumePrompt()
        assert generator.workspace_root == Path("agent_workspaces")

    def test_initialization_custom_workspace(self, tmp_path):
        """Test initialization with custom workspace."""
        generator = OptimizedStallResumePrompt(workspace_root=tmp_path)
        assert generator.workspace_root == tmp_path

    @patch('src.core.optimized_stall_resume_prompt.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_agent_state_exists(self, mock_file, mock_exists):
        """Test loading agent state when file exists."""
        mock_exists.return_value = True
        mock_file.return_value.read.return_value = '{"fsm_state": "active", "current_mission": "Test"}'
        
        generator = OptimizedStallResumePrompt()
        state = generator._load_agent_state("Agent-1")
        assert state.get("fsm_state") == "active"

    @patch('src.core.optimized_stall_resume_prompt.Path.exists')
    def test_load_agent_state_not_exists(self, mock_exists):
        """Test loading agent state when file doesn't exist."""
        mock_exists.return_value = False
        
        generator = OptimizedStallResumePrompt()
        state = generator._load_agent_state("Agent-1")
        assert state == {}

    def test_get_fsm_context(self):
        """Test getting FSM context."""
        generator = OptimizedStallResumePrompt()
        context = generator._get_fsm_context("active")
        assert "Active execution" in context

    def test_get_fsm_context_unknown(self):
        """Test getting FSM context for unknown state."""
        generator = OptimizedStallResumePrompt()
        context = generator._get_fsm_context("unknown")
        assert "Unknown state" in context

    @patch.object(OptimizedStallResumePrompt, '_load_agent_state')
    @patch.object(OptimizedStallResumePrompt, '_get_next_cycle_planner_task')
    def test_generate_resume_prompt(self, mock_get_task, mock_load_state):
        """Test generating resume prompt."""
        mock_load_state.return_value = {}
        mock_get_task.return_value = None
        
        generator = OptimizedStallResumePrompt()
        prompt = generator.generate_resume_prompt(
            agent_id="Agent-1",
            fsm_state="active",
            last_mission="Test Mission",
            stall_duration_minutes=5.0,
        )
        assert "STALL RECOVERY" in prompt
        assert "Agent-1" in prompt
        assert "ACTIVE" in prompt.upper() or "active" in prompt.lower()

    def test_generate_resume_prompt_critical(self):
        """Test generating prompt with critical urgency."""
        generator = OptimizedStallResumePrompt()
        with patch.object(generator, '_load_agent_state', return_value={}):
            with patch.object(generator, '_get_next_cycle_planner_task', return_value=None):
                prompt = generator.generate_resume_prompt(
                    agent_id="Agent-1",
                    stall_duration_minutes=12.0,
                )
                assert "CRITICAL" in prompt

    def test_generate_resume_prompt_with_task(self):
        """Test generating prompt with next task."""
        generator = OptimizedStallResumePrompt()
        next_task = {
            "contract_id": "task-123",
            "title": "Test Task",
            "priority": "HIGH",
            "points": 100,
            "status": "PENDING",
        }
        with patch.object(generator, '_load_agent_state', return_value={}):
            with patch.object(generator, '_get_next_cycle_planner_task', return_value=next_task):
                prompt = generator.generate_resume_prompt("Agent-1")
                assert "Test Task" in prompt
                assert "task-123" in prompt

    @patch('src.core.optimized_stall_resume_prompt.date')
    @patch('src.core.optimized_stall_resume_prompt.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_get_next_cycle_planner_task(self, mock_file, mock_exists, mock_date):
        """Test getting next cycle planner task."""
        mock_date.today.return_value.isoformat.return_value = "2025-01-01"
        mock_exists.return_value = True
        mock_file.return_value.read.return_value = json.dumps({
            "contracts": [
                {"status": "PENDING", "contract_id": "task-1"},
            ]
        })
        
        generator = OptimizedStallResumePrompt()
        task = generator._get_next_cycle_planner_task("Agent-1")
        assert task is not None
        assert task["contract_id"] == "task-1"

    @patch('src.core.optimized_stall_resume_prompt.date')
    @patch('src.core.optimized_stall_resume_prompt.Path.exists')
    @patch('src.core.optimized_stall_resume_prompt.Path.glob')
    def test_get_next_cycle_planner_task_recent_file(self, mock_glob, mock_exists, mock_date):
        """Test getting task from most recent file."""
        mock_date.today.return_value.isoformat.return_value = "2025-01-01"
        mock_exists.return_value = False
        mock_file = MagicMock()
        mock_file.exists.return_value = True
        mock_file.open.return_value.__enter__.return_value.read.return_value = json.dumps({
            "contracts": [{"status": "READY", "contract_id": "task-2"}]
        })
        mock_glob.return_value = [mock_file]
        
        generator = OptimizedStallResumePrompt()
        task = generator._get_next_cycle_planner_task("Agent-1")
        # Should handle file reading if glob returns valid file

    def test_build_prompt_all_sections(self):
        """Test building prompt with all sections."""
        generator = OptimizedStallResumePrompt()
        next_task = {
            "contract_id": "task-1",
            "title": "Test",
            "priority": "HIGH",
            "points": 100,
            "status": "PENDING",
        }
        prompt = generator._build_prompt(
            agent_id="Agent-1",
            fsm_state="active",
            last_mission="Test Mission",
            next_task=next_task,
            recovery_actions=["Action 1", "Action 2"],
            stall_duration_minutes=6.0,
        )
        assert "Agent-1" in prompt
        assert "Test Mission" in prompt
        assert "Action 1" in prompt

    def test_build_prompt_no_task(self):
        """Test building prompt without next task."""
        generator = OptimizedStallResumePrompt()
        prompt = generator._build_prompt(
            agent_id="Agent-1",
            fsm_state="active",
            last_mission="Test",
            next_task=None,
            recovery_actions=["Action 1"],
            stall_duration_minutes=3.0,
        )
        assert "No pending tasks" in prompt or "CYCLE PLANNER" in prompt


class TestGenerateOptimizedResumePrompt:
    """Tests for convenience function."""

    @patch.object(OptimizedStallResumePrompt, 'generate_resume_prompt')
    def test_convenience_function(self, mock_generate):
        """Test convenience function."""
        mock_generate.return_value = "Test prompt"
        result = generate_optimized_resume_prompt(
            agent_id="Agent-1",
            fsm_state="active",
            stall_duration_minutes=5.0,
        )
        assert result == "Test prompt"
        mock_generate.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

