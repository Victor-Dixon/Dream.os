"""
Tests for messaging_cli_parser.py

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-11-27
"""

import pytest
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))

from src.services.messaging_cli_parser import create_messaging_parser, CLI_HELP_EPILOG


class TestCreateMessagingParser:
    """Test create_messaging_parser function."""

    def test_create_parser_returns_argparse_parser(self):
        """Test that create_messaging_parser returns an ArgumentParser."""
        parser = create_messaging_parser()
        assert parser is not None
        assert hasattr(parser, 'parse_args')
        assert hasattr(parser, 'add_argument')

    def test_parser_has_message_argument(self):
        """Test that parser has --message argument."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--message", "Test message"])
        assert args.message == "Test message"

    def test_parser_has_agent_argument(self):
        """Test that parser has --agent argument."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--agent", "Agent-1"])
        assert args.agent == "Agent-1"

    def test_parser_has_broadcast_flag(self):
        """Test that parser has --broadcast flag."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--broadcast"])
        assert args.broadcast is True

    def test_parser_has_priority_argument(self):
        """Test that parser has --priority argument with choices."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--priority", "urgent"])
        assert args.priority == "urgent"

    def test_parser_priority_default(self):
        """Test that priority defaults to regular."""
        parser = create_messaging_parser()
        args = parser.parse_args([])
        assert args.priority == "regular"

    def test_parser_priority_choices(self):
        """Test that priority accepts normal, regular, and urgent."""
        parser = create_messaging_parser()
        
        args_normal = parser.parse_args(["--priority", "normal"])
        assert args_normal.priority == "normal"
        
        args_regular = parser.parse_args(["--priority", "regular"])
        assert args_regular.priority == "regular"
        
        args_urgent = parser.parse_args(["--priority", "urgent"])
        assert args_urgent.priority == "urgent"

    def test_parser_has_stalled_flag(self):
        """Test that parser has --stalled flag."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--stalled"])
        assert args.stalled is True

    def test_parser_has_tags_argument(self):
        """Test that parser has --tags argument."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--tags", "tag1", "tag2"])
        assert args.tags == ["tag1", "tag2"]

    def test_parser_has_pyautogui_flag(self):
        """Test that parser has --pyautogui flag."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--pyautogui"])
        assert args.pyautogui is True

    def test_parser_has_coordinates_flag(self):
        """Test that parser has --coordinates flag."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--coordinates"])
        assert args.coordinates is True

    def test_parser_has_start_argument(self):
        """Test that parser has --start argument."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--start", "1", "2", "3"])
        assert args.start == [1, 2, 3]

    def test_parser_has_save_flag(self):
        """Test that parser has --save flag."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--save"])
        assert args.save is True

    def test_parser_has_leaderboard_flag(self):
        """Test that parser has --leaderboard flag."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--leaderboard"])
        assert args.leaderboard is True

    def test_parser_has_get_next_task_flag(self):
        """Test that parser has --get-next-task flag."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--get-next-task"])
        assert args.get_next_task is True

    def test_parser_has_list_tasks_flag(self):
        """Test that parser has --list-tasks flag."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--list-tasks"])
        assert args.list_tasks is True

    def test_parser_has_task_status_argument(self):
        """Test that parser has --task-status argument."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--task-status", "task-123"])
        assert args.task_status == "task-123"

    def test_parser_has_complete_task_argument(self):
        """Test that parser has --complete-task argument."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--complete-task", "task-456"])
        assert args.complete_task == "task-456"

    def test_parser_has_survey_coordination_flag(self):
        """Test that parser has --survey-coordination flag."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--survey-coordination"])
        assert args.survey_coordination is True

    def test_parser_has_consolidation_coordination_flag(self):
        """Test that parser has --consolidation-coordination flag."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--consolidation-coordination"])
        assert args.consolidation_coordination is True

    def test_parser_has_consolidation_batch_argument(self):
        """Test that parser has --consolidation-batch argument."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--consolidation-batch", "batch-1"])
        assert args.consolidation_batch == "batch-1"

    def test_parser_has_consolidation_status_argument(self):
        """Test that parser has --consolidation-status argument."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--consolidation-status", "in-progress"])
        assert args.consolidation_status == "in-progress"

    def test_parser_epilog_contains_help_text(self):
        """Test that parser epilog contains CLI_HELP_EPILOG."""
        parser = create_messaging_parser()
        assert parser.epilog == CLI_HELP_EPILOG

    def test_parser_description(self):
        """Test that parser has correct description."""
        parser = create_messaging_parser()
        assert "SWARM Messaging CLI" in parser.description

    def test_parser_short_flags(self):
        """Test that short flags work."""
        parser = create_messaging_parser()
        args = parser.parse_args(["-m", "Test", "-a", "Agent-1", "-p", "urgent"])
        assert args.message == "Test"
        assert args.agent == "Agent-1"
        assert args.priority == "urgent"

    def test_parser_combined_flags(self):
        """Test that multiple flags can be combined."""
        parser = create_messaging_parser()
        args = parser.parse_args([
            "--message", "Test",
            "--agent", "Agent-2",
            "--priority", "urgent",
            "--stalled",
            "--tags", "bug", "critical"
        ])
        assert args.message == "Test"
        assert args.agent == "Agent-2"
        assert args.priority == "urgent"
        assert args.stalled is True
        assert args.tags == ["bug", "critical"]


class TestCLIHelpEpilog:
    """Test CLI_HELP_EPILOG constant."""

    def test_epilog_is_string(self):
        """Test that CLI_HELP_EPILOG is a string."""
        assert isinstance(CLI_HELP_EPILOG, str)
        assert len(CLI_HELP_EPILOG) > 0

    def test_epilog_contains_examples(self):
        """Test that epilog contains example usage."""
        assert "EXAMPLES" in CLI_HELP_EPILOG
        assert "Send message" in CLI_HELP_EPILOG or "message" in CLI_HELP_EPILOG.lower()

    def test_epilog_contains_swarm_reference(self):
        """Test that epilog contains swarm reference."""
        assert "SWARM" in CLI_HELP_EPILOG


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

