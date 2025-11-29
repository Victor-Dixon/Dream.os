"""
Tests for messaging_cli_parser.py

Comprehensive tests for CLI argument parsing.
Target: ≥85% coverage
"""

import pytest
from src.services.messaging_cli_parser import (
    create_messaging_parser,
    CLI_HELP_EPILOG,
)


class TestCLIHelpEpilog:
    """Tests for CLI_HELP_EPILOG constant."""

    def test_cli_help_epilog_exists(self):
        """Test that CLI_HELP_EPILOG exists."""
        assert CLI_HELP_EPILOG is not None
        assert isinstance(CLI_HELP_EPILOG, str)
        assert len(CLI_HELP_EPILOG) > 0

    def test_cli_help_epilog_content(self):
        """Test CLI_HELP_EPILOG content."""
        assert "SWARM MESSAGING CLI" in CLI_HELP_EPILOG
        assert "EXAMPLES" in CLI_HELP_EPILOG
        assert "--message" in CLI_HELP_EPILOG
        assert "--agent" in CLI_HELP_EPILOG
        assert "--broadcast" in CLI_HELP_EPILOG


class TestCreateMessagingParser:
    """Tests for create_messaging_parser function."""

    def test_create_parser_returns_parser(self):
        """Test that create_messaging_parser returns ArgumentParser."""
        parser = create_messaging_parser()
        assert parser is not None
        assert hasattr(parser, 'parse_args')

    def test_parser_description(self):
        """Test parser description."""
        parser = create_messaging_parser()
        assert "SWARM Messaging CLI" in parser.description

    def test_parser_epilog(self):
        """Test parser epilog."""
        parser = create_messaging_parser()
        assert parser.epilog == CLI_HELP_EPILOG

    def test_parse_message_argument(self):
        """Test parsing --message argument."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--message", "Test message"])
        
        assert args.message == "Test message"

    def test_parse_message_short_form(self):
        """Test parsing -m short form."""
        parser = create_messaging_parser()
        args = parser.parse_args(["-m", "Test message"])
        
        assert args.message == "Test message"

    def test_parse_agent_argument(self):
        """Test parsing --agent argument."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--agent", "Agent-1"])
        
        assert args.agent == "Agent-1"

    def test_parse_agent_short_form(self):
        """Test parsing -a short form."""
        parser = create_messaging_parser()
        args = parser.parse_args(["-a", "Agent-2"])
        
        assert args.agent == "Agent-2"

    def test_parse_broadcast_flag(self):
        """Test parsing --broadcast flag."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--broadcast"])
        
        assert args.broadcast is True

    def test_parse_broadcast_short_form(self):
        """Test parsing -b short form."""
        parser = create_messaging_parser()
        args = parser.parse_args(["-b"])
        
        assert args.broadcast is True

    def test_parse_priority_normal(self):
        """Test parsing --priority normal."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--priority", "normal"])
        
        assert args.priority == "normal"

    def test_parse_priority_regular(self):
        """Test parsing --priority regular."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--priority", "regular"])
        
        assert args.priority == "regular"

    def test_parse_priority_urgent(self):
        """Test parsing --priority urgent."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--priority", "urgent"])
        
        assert args.priority == "urgent"

    def test_parse_priority_default(self):
        """Test priority default value."""
        parser = create_messaging_parser()
        args = parser.parse_args([])
        
        assert args.priority == "regular"

    def test_parse_priority_short_form(self):
        """Test parsing -p short form."""
        parser = create_messaging_parser()
        args = parser.parse_args(["-p", "urgent"])
        
        assert args.priority == "urgent"

    def test_parse_stalled_flag(self):
        """Test parsing --stalled flag."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--stalled"])
        
        assert args.stalled is True

    def test_parse_tags_single(self):
        """Test parsing --tags with single tag."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--tags", "bug"])
        
        assert args.tags == ["bug"]

    def test_parse_tags_multiple(self):
        """Test parsing --tags with multiple tags."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--tags", "bug", "critical", "urgent"])
        
        assert args.tags == ["bug", "critical", "urgent"]

    def test_parse_tags_short_form(self):
        """Test parsing -t short form."""
        parser = create_messaging_parser()
        args = parser.parse_args(["-t", "test"])
        
        assert args.tags == ["test"]

    def test_parse_pyautogui_flag(self):
        """Test parsing --pyautogui flag."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--pyautogui"])
        
        assert args.pyautogui is True

    def test_parse_pyautogui_gui_alias(self):
        """Test parsing --gui alias."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--gui"])
        
        assert args.pyautogui is True

    def test_parse_survey_coordination_flag(self):
        """Test parsing --survey-coordination flag."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--survey-coordination"])
        
        assert args.survey_coordination is True

    def test_parse_consolidation_coordination_flag(self):
        """Test parsing --consolidation-coordination flag."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--consolidation-coordination"])
        
        assert args.consolidation_coordination is True

    def test_parse_consolidation_batch(self):
        """Test parsing --consolidation-batch."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--consolidation-batch", "Batch-1"])
        
        assert args.consolidation_batch == "Batch-1"

    def test_parse_consolidation_status(self):
        """Test parsing --consolidation-status."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--consolidation-status", "Complete"])
        
        assert args.consolidation_status == "Complete"

    def test_parse_coordinates_flag(self):
        """Test parsing --coordinates flag."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--coordinates"])
        
        assert args.coordinates is True

    def test_parse_start_single(self):
        """Test parsing --start with single agent."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--start", "1"])
        
        assert args.start == [1]

    def test_parse_start_multiple(self):
        """Test parsing --start with multiple agents."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--start", "1", "2", "3"])
        
        assert args.start == [1, 2, 3]

    def test_parse_save_flag(self):
        """Test parsing --save flag."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--save"])
        
        assert args.save is True

    def test_parse_leaderboard_flag(self):
        """Test parsing --leaderboard flag."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--leaderboard"])
        
        assert args.leaderboard is True

    def test_parse_get_next_task_flag(self):
        """Test parsing --get-next-task flag."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--get-next-task"])
        
        assert args.get_next_task is True

    def test_parse_list_tasks_flag(self):
        """Test parsing --list-tasks flag."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--list-tasks"])
        
        assert args.list_tasks is True

    def test_parse_task_status(self):
        """Test parsing --task-status."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--task-status", "task-123"])
        
        assert args.task_status == "task-123"

    def test_parse_complete_task(self):
        """Test parsing --complete-task."""
        parser = create_messaging_parser()
        args = parser.parse_args(["--complete-task", "task-456"])
        
        assert args.complete_task == "task-456"

    def test_parse_multiple_arguments(self):
        """Test parsing multiple arguments together."""
        parser = create_messaging_parser()
        args = parser.parse_args([
            "--message", "Test",
            "--agent", "Agent-1",
            "--priority", "urgent",
            "--tags", "bug", "critical",
            "--pyautogui"
        ])
        
        assert args.message == "Test"
        assert args.agent == "Agent-1"
        assert args.priority == "urgent"
        assert args.tags == ["bug", "critical"]
        assert args.pyautogui is True

    def test_parse_invalid_priority(self):
        """Test parsing invalid priority value."""
        parser = create_messaging_parser()
        
        with pytest.raises(SystemExit):
            parser.parse_args(["--priority", "invalid"])

    def test_parse_no_arguments(self):
        """Test parsing with no arguments."""
        parser = create_messaging_parser()
        args = parser.parse_args([])
        
        assert args.message is None
        assert args.agent is None
        assert args.broadcast is False
        assert args.priority == "regular"

    def test_parse_consolidation_with_batch_and_status(self):
        """Test parsing consolidation with both batch and status."""
        parser = create_messaging_parser()
        args = parser.parse_args([
            "--consolidation-coordination",
            "--consolidation-batch", "Batch-1",
            "--consolidation-status", "Complete"
        ])
        
        assert args.consolidation_coordination is True
        assert args.consolidation_batch == "Batch-1"
        assert args.consolidation_status == "Complete"

    def test_parser_help_output(self):
        """Test that parser generates help output."""
        parser = create_messaging_parser()
        
        # Should not raise
        help_text = parser.format_help()
        assert "--message" in help_text
        assert "--agent" in help_text
        assert "--broadcast" in help_text

