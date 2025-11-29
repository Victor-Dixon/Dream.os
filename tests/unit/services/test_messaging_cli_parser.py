"""
Unit tests for messaging_cli_parser.py
Target: ≥85% coverage
"""

import pytest
import argparse
from src.services.messaging_cli_parser import create_messaging_parser, CLI_HELP_EPILOG


class TestMessagingCLIParser:
    """Tests for messaging CLI parser."""

    def test_create_messaging_parser_returns_parser(self):
        """Test create_messaging_parser returns ArgumentParser."""
        parser = create_messaging_parser()
        assert isinstance(parser, argparse.ArgumentParser)

    def test_parser_has_message_argument(self):
        """Test parser has --message argument."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--message", "Test message"])
        assert args.message == "Test message"

    def test_parser_has_message_short_flag(self):
        """Test parser has -m short flag for message."""
        parser = create_messaging_parser()
        args = parser.parse_args(["-m", "Test message"])
        assert args.message == "Test message"

    def test_parser_has_agent_argument(self):
        """Test parser has --agent argument."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--agent", "Agent-1"])
        assert args.agent == "Agent-1"

    def test_parser_has_agent_short_flag(self):
        """Test parser has -a short flag for agent."""
        parser = create_messaging_parser()
        args = parser.parse_args(["-a", "Agent-2"])
        assert args.agent == "Agent-2"

    def test_parser_has_broadcast_flag(self):
        """Test parser has --broadcast flag."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--broadcast"])
        assert args.broadcast is True

    def test_parser_has_broadcast_short_flag(self):
        """Test parser has -b short flag for broadcast."""
        parser = create_messaging_parser()
        args = parser.parse_args(["-b"])
        assert args.broadcast is True

    def test_parser_has_priority_argument(self):
        """Test parser has --priority argument."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--priority", "urgent"])
        assert args.priority == "urgent"

    def test_parser_has_priority_short_flag(self):
        """Test parser has -p short flag for priority."""
        parser = create_messaging_parser()
        args = parser.parse_args(["-p", "normal"])
        assert args.priority == "normal"

    def test_parser_priority_default(self):
        """Test parser priority defaults to regular."""
        parser = create_messaging_parser()
        args = parser.parse_args([])
        assert args.priority == "regular"

    def test_parser_priority_choices(self):
        """Test parser priority accepts valid choices."""
        parser = create_messaging_parser()
        for choice in ["normal", "regular", "urgent"]:
            args = parser.parse_args(["--priority", choice])
            assert args.priority == choice

    def test_parser_priority_invalid_choice(self):
        """Test parser rejects invalid priority choice."""
        parser = create_messaging_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["--priority", "invalid"])

    def test_parser_has_stalled_flag(self):
        """Test parser has --stalled flag."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--stalled"])
        assert args.stalled is True

    def test_parser_has_tags_argument(self):
        """Test parser has --tags argument."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--tags", "tag1", "tag2"])
        assert args.tags == ["tag1", "tag2"]

    def test_parser_has_tags_short_flag(self):
        """Test parser has -t short flag for tags."""
        parser = create_messaging_parser()
        args = parser.parse_args(["-t", "tag1", "tag2", "tag3"])
        assert args.tags == ["tag1", "tag2", "tag3"]

    def test_parser_has_pyautogui_flag(self):
        """Test parser has --pyautogui flag."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--pyautogui"])
        assert args.pyautogui is True

    def test_parser_has_gui_flag(self):
        """Test parser has --gui flag (alias for pyautogui)."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--gui"])
        assert args.pyautogui is True

    def test_parser_has_survey_coordination_flag(self):
        """Test parser has --survey-coordination flag."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--survey-coordination"])
        assert args.survey_coordination is True

    def test_parser_has_consolidation_coordination_flag(self):
        """Test parser has --consolidation-coordination flag."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--consolidation-coordination"])
        assert args.consolidation_coordination is True

    def test_parser_has_consolidation_batch_argument(self):
        """Test parser has --consolidation-batch argument."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--consolidation-batch", "batch-1"])
        assert args.consolidation_batch == "batch-1"

    def test_parser_has_consolidation_status_argument(self):
        """Test parser has --consolidation-status argument."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--consolidation-status", "complete"])
        assert args.consolidation_status == "complete"

    def test_parser_has_coordinates_flag(self):
        """Test parser has --coordinates flag."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--coordinates"])
        assert args.coordinates is True

    def test_parser_has_start_argument(self):
        """Test parser has --start argument."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--start", "1", "2", "3"])
        assert args.start == [1, 2, 3]

    def test_parser_has_save_flag(self):
        """Test parser has --save flag."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--save"])
        assert args.save is True

    def test_parser_has_leaderboard_flag(self):
        """Test parser has --leaderboard flag."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--leaderboard"])
        assert args.leaderboard is True

    def test_parser_has_get_next_task_flag(self):
        """Test parser has --get-next-task flag."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--get-next-task"])
        assert args.get_next_task is True

    def test_parser_has_list_tasks_flag(self):
        """Test parser has --list-tasks flag."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--list-tasks"])
        assert args.list_tasks is True

    def test_parser_has_task_status_argument(self):
        """Test parser has --task-status argument."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--task-status", "task-123"])
        assert args.task_status == "task-123"

    def test_parser_has_complete_task_argument(self):
        """Test parser has --complete-task argument."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--complete-task", "task-456"])
        assert args.complete_task == "task-456"

    def test_parser_epilog_set(self):
        """Test parser has epilog set."""
        parser = create_messaging_parser()
        assert parser.epilog == CLI_HELP_EPILOG

    def test_parser_description_set(self):
        """Test parser has description set."""
        parser = create_messaging_parser()
        assert parser.description is not None
        assert "SWARM" in parser.description or "swarm" in parser.description

    def test_parser_combined_arguments(self):
        """Test parser handles combined arguments."""
        parser = create_messaging_parser()
        args = parser.parse_args([
            "--message", "Test",
            "--agent", "Agent-1",
            "--priority", "urgent",
            "--tags", "tag1", "tag2",
            "--pyautogui"
        ])
        assert args.message == "Test"
        assert args.agent == "Agent-1"
        assert args.priority == "urgent"
        assert args.tags == ["tag1", "tag2"]
        assert args.pyautogui is True

    def test_parser_default_values(self):
        """Test parser sets correct default values."""
        parser = create_messaging_parser()
        args = parser.parse_args([])
        assert args.message is None
        assert args.agent is None
        assert args.broadcast is False
        assert args.priority == "regular"
        assert args.stalled is False
        assert args.tags is None
        assert args.pyautogui is False
        assert args.survey_coordination is False
        assert args.consolidation_coordination is False
        assert args.coordinates is False
        assert args.save is False
        assert args.leaderboard is False
        assert args.get_next_task is False
        assert args.list_tasks is False
        assert args.task_status is None
        assert args.complete_task is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
