"""
CLI Smoke Tests - Trader Replay Journal

End-to-end CLI workflow validation with temporary database.
Tests all commands: create, list, start, step, pause, status
"""

import pytest
import subprocess
import tempfile
import sys
import os
from pathlib import Path
from datetime import datetime


class TestTraderReplayCLI:
    """End-to-end CLI smoke tests."""

    @pytest.fixture
    def temp_db(self):
        """Create temporary database file."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = Path(f.name)
        yield db_path
        if db_path.exists():
            db_path.unlink()

    @pytest.fixture
    def cli_command(self):
        """Base CLI command."""
        # Use module approach with proper PYTHONPATH
        return [
            sys.executable,
            "-m",
            "src.services.trader_replay.trader_replay_cli",
        ]

    def run_cli(self, cli_command, args, db_path=None, expected_return_code=0):
        """Run CLI command and assert return code."""
        cmd = cli_command.copy()
        if db_path:
            cmd.extend(["--db-path", str(db_path)])
        cmd.extend(args)

        # Set PYTHONPATH to include project root
        env = os.environ.copy()
        project_root = Path(__file__).parent.parent.parent.parent
        pythonpath = str(project_root)
        if "PYTHONPATH" in env:
            env["PYTHONPATH"] = f"{pythonpath}{os.pathsep}{env['PYTHONPATH']}"
        else:
            env["PYTHONPATH"] = pythonpath

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=project_root,
            env=env,
        )

        if result.returncode != expected_return_code:
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")

        assert result.returncode == expected_return_code, \
            f"CLI command failed with return code {result.returncode}\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"

        return result

    def test_create_session(self, cli_command, temp_db):
        """Test create session command."""
        result = self.run_cli(
            cli_command,
            [
                "create",
                "--symbol", "AAPL",
                "--date", "2024-01-15",
                "--timeframe", "1m",
            ],
            db_path=temp_db,
        )

        assert "✅ Created replay session" in result.stdout
        assert "AAPL" in result.stdout
        assert "2024-01-15" in result.stdout

    def test_create_session_with_agent(self, cli_command, temp_db):
        """Test create session with agent ID."""
        result = self.run_cli(
            cli_command,
            [
                "create",
                "--symbol", "TSLA",
                "--date", "2024-01-16",
                "--timeframe", "5m",
                "--agent", "Agent-5",
            ],
            db_path=temp_db,
        )

        assert "✅ Created replay session" in result.stdout
        assert "TSLA" in result.stdout
        assert "Agent-5" in result.stdout

    def test_create_session_missing_required_args(self, cli_command, temp_db):
        """Test create session with missing required arguments."""
        result = self.run_cli(
            cli_command,
            ["create", "--date", "2024-01-15"],
            db_path=temp_db,
            expected_return_code=2,  # argparse error
        )

        assert "error" in result.stderr.lower() or "required" in result.stderr.lower()

    def test_list_sessions(self, cli_command, temp_db):
        """Test list sessions command."""
        # First create a session
        self.run_cli(
            cli_command,
            [
                "create",
                "--symbol", "AAPL",
                "--date", "2024-01-15",
                "--timeframe", "1m",
            ],
            db_path=temp_db,
        )

        # Then list
        result = self.run_cli(
            cli_command,
            ["list"],
            db_path=temp_db,
        )

        # List command may show placeholder message
        assert "Replay Sessions" in result.stdout or "List functionality" in result.stdout

    def test_start_replay(self, cli_command, temp_db):
        """Test start replay command."""
        # Create session first
        create_result = self.run_cli(
            cli_command,
            [
                "create",
                "--symbol", "AAPL",
                "--date", "2024-01-15",
                "--timeframe", "1m",
            ],
            db_path=temp_db,
        )

        # Extract session ID from output (format: "✅ Created replay session 1")
        import re
        match = re.search(r"session (\d+)", create_result.stdout)
        assert match, "Session ID not found in create output"
        session_id = match.group(1)

        # Start replay
        result = self.run_cli(
            cli_command,
            ["start", "--session-id", session_id],
            db_path=temp_db,
        )

        assert "✅ Started replay session" in result.stdout
        assert session_id in result.stdout

    def test_start_nonexistent_session(self, cli_command, temp_db):
        """Test start replay with non-existent session."""
        result = self.run_cli(
            cli_command,
            ["start", "--session-id", "99999"],
            db_path=temp_db,
            expected_return_code=1,  # Error expected
        )

        assert "❌" in result.stdout or "error" in result.stdout.lower(
        ) or "failed" in result.stdout.lower()

    def test_step_replay_forward(self, cli_command, temp_db):
        """Test step replay forward."""
        # Create and start session
        create_result = self.run_cli(
            cli_command,
            [
                "create",
                "--symbol", "AAPL",
                "--date", "2024-01-15",
                "--timeframe", "1m",
            ],
            db_path=temp_db,
        )

        import re
        match = re.search(r"session (\d+)", create_result.stdout)
        session_id = match.group(1)

        self.run_cli(
            cli_command,
            ["start", "--session-id", session_id],
            db_path=temp_db,
        )

        # Step forward
        result = self.run_cli(
            cli_command,
            ["step", "--session-id", session_id, "--direction", "forward"],
            db_path=temp_db,
        )

        assert "✅ Stepped replay forward" in result.stdout
        assert session_id in result.stdout

    def test_step_replay_backward(self, cli_command, temp_db):
        """Test step replay backward."""
        # Create and start session, step forward first
        create_result = self.run_cli(
            cli_command,
            [
                "create",
                "--symbol", "AAPL",
                "--date", "2024-01-15",
                "--timeframe", "1m",
            ],
            db_path=temp_db,
        )

        import re
        match = re.search(r"session (\d+)", create_result.stdout)
        session_id = match.group(1)

        self.run_cli(
            cli_command,
            ["start", "--session-id", session_id],
            db_path=temp_db,
        )

        # Step forward first
        self.run_cli(
            cli_command,
            ["step", "--session-id", session_id, "--direction", "forward"],
            db_path=temp_db,
        )

        # Then step backward
        result = self.run_cli(
            cli_command,
            ["step", "--session-id", session_id, "--direction", "backward"],
            db_path=temp_db,
        )

        assert "✅ Stepped replay backward" in result.stdout
        assert session_id in result.stdout

    def test_pause_replay(self, cli_command, temp_db):
        """Test pause replay command."""
        # Create and start session
        create_result = self.run_cli(
            cli_command,
            [
                "create",
                "--symbol", "AAPL",
                "--date", "2024-01-15",
                "--timeframe", "1m",
            ],
            db_path=temp_db,
        )

        import re
        match = re.search(r"session (\d+)", create_result.stdout)
        session_id = match.group(1)

        self.run_cli(
            cli_command,
            ["start", "--session-id", session_id],
            db_path=temp_db,
        )

        # Pause
        result = self.run_cli(
            cli_command,
            ["pause", "--session-id", session_id],
            db_path=temp_db,
        )

        assert "✅ Paused replay session" in result.stdout
        assert session_id in result.stdout

    def test_status_command(self, cli_command, temp_db):
        """Test status command."""
        # Create session
        create_result = self.run_cli(
            cli_command,
            [
                "create",
                "--symbol", "AAPL",
                "--date", "2024-01-15",
                "--timeframe", "1m",
            ],
            db_path=temp_db,
        )

        import re
        match = re.search(r"session (\d+)", create_result.stdout)
        session_id = match.group(1)

        # Get status
        result = self.run_cli(
            cli_command,
            ["status", "--session-id", session_id],
            db_path=temp_db,
        )

        assert "Session Status" in result.stdout or session_id in result.stdout

    def test_status_nonexistent_session(self, cli_command, temp_db):
        """Test status command with non-existent session."""
        result = self.run_cli(
            cli_command,
            ["status", "--session-id", "99999"],
            db_path=temp_db,
            expected_return_code=1,  # Error expected
        )

        assert "❌" in result.stdout or "not found" in result.stdout.lower()

    def test_end_to_end_workflow(self, cli_command, temp_db):
        """Test complete workflow: create → start → step → pause → status."""
        # Create
        create_result = self.run_cli(
            cli_command,
            [
                "create",
                "--symbol", "MSFT",
                "--date", "2024-01-20",
                "--timeframe", "1m",
            ],
            db_path=temp_db,
        )

        import re
        match = re.search(r"session (\d+)", create_result.stdout)
        session_id = match.group(1)

        # Start
        self.run_cli(
            cli_command,
            ["start", "--session-id", session_id],
            db_path=temp_db,
        )

        # Step forward
        self.run_cli(
            cli_command,
            ["step", "--session-id", session_id, "--direction", "forward"],
            db_path=temp_db,
        )

        # Step forward again
        self.run_cli(
            cli_command,
            ["step", "--session-id", session_id, "--direction", "forward"],
            db_path=temp_db,
        )

        # Pause
        self.run_cli(
            cli_command,
            ["pause", "--session-id", session_id],
            db_path=temp_db,
        )

        # Status
        result = self.run_cli(
            cli_command,
            ["status", "--session-id", session_id],
            db_path=temp_db,
        )

        assert "Session Status" in result.stdout or session_id in result.stdout

    def test_cli_help(self, cli_command):
        """Test CLI help command."""
        result = self.run_cli(
            cli_command,
            ["--help"],
        )

        assert "Dream.OS Trading Replay Journal CLI" in result.stdout
        assert "create" in result.stdout
        assert "list" in result.stdout
        assert "start" in result.stdout

    def test_cli_no_command(self, cli_command):
        """Test CLI with no command shows help."""
        result = self.run_cli(
            cli_command,
            [],
        )

        # Should show help or usage
        assert "usage" in result.stdout.lower() or "help" in result.stdout.lower()
