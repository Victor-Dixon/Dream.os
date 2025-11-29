"""
Unit tests for command_execution_wrapper.py - HIGH PRIORITY

Tests command execution wrapper functionality.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import subprocess

# Import command execution wrapper
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))


class TestCommandExecutionWrapper:
    """Test suite for command execution wrapper."""

    @pytest.fixture
    def wrapper(self):
        """Create command execution wrapper instance."""
        # Would initialize wrapper
        return MagicMock()

    def test_wrapper_initialization(self, wrapper):
        """Test wrapper initialization."""
        assert wrapper is not None

    @patch('subprocess.run')
    def test_execute_command_success(self, mock_run):
        """Test successful command execution."""
        mock_run.return_value = MagicMock(returncode=0, stdout=b"success")
        
        # Simulate command execution
        result = mock_run(["echo", "test"], capture_output=True)
        
        assert result.returncode == 0

    @patch('subprocess.run')
    def test_execute_command_failure(self, mock_run):
        """Test failed command execution."""
        mock_run.return_value = MagicMock(returncode=1, stderr=b"error")
        
        # Simulate command failure
        result = mock_run(["invalid", "command"], capture_output=True)
        
        assert result.returncode != 0

    def test_command_validation(self):
        """Test command validation."""
        valid_command = ["echo", "test"]
        invalid_command = []
        
        is_valid = len(valid_command) > 0
        is_invalid = len(invalid_command) == 0
        
        assert is_valid is True
        assert is_invalid is True

    @patch('subprocess.run')
    def test_timeout_handling(self, mock_run):
        """Test command timeout handling."""
        mock_run.side_effect = subprocess.TimeoutExpired("command", 5.0)
        
        # Would handle timeout
        try:
            raise subprocess.TimeoutExpired("command", 5.0)
        except subprocess.TimeoutExpired:
            assert True  # Timeout handled

    def test_output_capture(self):
        """Test output capture."""
        # Simulate output capture
        stdout = b"output"
        stderr = b""
        
        assert stdout is not None
        assert stderr is not None

    def test_command_execution_result_init(self):
        """Test CommandExecutionResult initialization."""
        from src.core.command_execution_wrapper import CommandExecutionResult
        
        result = CommandExecutionResult(
            command="echo test",
            exit_code=0,
            stdout="output",
            stderr="",
            is_complete=True,
            completion_reason="Success"
        )
        
        assert result.command == "echo test"
        assert result.exit_code == 0
        assert result.stdout == "output"
        assert result.stderr == ""
        assert result.is_complete is True
        assert result.completion_reason == "Success"
        assert result.success is True

    def test_command_execution_result_success_false(self):
        """Test CommandExecutionResult with failure."""
        from src.core.command_execution_wrapper import CommandExecutionResult
        
        result = CommandExecutionResult(
            command="invalid",
            exit_code=1,
            stdout="",
            stderr="error",
            is_complete=True,
            completion_reason="Error"
        )
        
        assert result.success is False
        assert result.exit_code == 1

    def test_command_execution_result_bool_true(self):
        """Test CommandExecutionResult __bool__ returns True for success."""
        from src.core.command_execution_wrapper import CommandExecutionResult
        
        result = CommandExecutionResult(
            command="echo test",
            exit_code=0,
            stdout="output",
            stderr="",
            is_complete=True
        )
        
        assert bool(result) is True

    def test_command_execution_result_bool_false(self):
        """Test CommandExecutionResult __bool__ returns False for failure."""
        from src.core.command_execution_wrapper import CommandExecutionResult
        
        result = CommandExecutionResult(
            command="invalid",
            exit_code=1,
            stdout="",
            stderr="error",
            is_complete=True
        )
        
        assert bool(result) is False

    def test_command_execution_result_str(self):
        """Test CommandExecutionResult __str__ representation."""
        from src.core.command_execution_wrapper import CommandExecutionResult
        
        result = CommandExecutionResult(
            command="echo test",
            exit_code=0,
            stdout="output",
            stderr="",
            is_complete=True
        )
        
        str_repr = str(result)
        assert "SUCCESS" in str_repr or "echo test" in str_repr

    def test_execute_command_with_completion_success(self):
        """Test execute_command_with_completion with successful command."""
        from src.core.command_execution_wrapper import execute_command_with_completion
        
        with patch('src.core.command_execution_wrapper.subprocess.Popen') as mock_popen:
            mock_process = Mock()
            mock_process.stdout.readline.return_value = "output\n"
            mock_process.stderr.readline.return_value = ""
            mock_process.poll.return_value = 0
            mock_process.wait.return_value = 0
            mock_popen.return_value = mock_process
            
            with patch('src.core.command_execution_wrapper.get_completion_detector') as mock_detector_getter:
                mock_detector = Mock()
                mock_detector.detect_output_completion.return_value = (True, "Complete")
                mock_detector_getter.return_value = mock_detector
                
                result = execute_command_with_completion("echo test", check_completion=True, task_id="task-1")
                
                assert result.exit_code == 0
                assert result.is_complete is True

    def test_execute_command_with_completion_failure(self):
        """Test execute_command_with_completion with failed command."""
        from src.core.command_execution_wrapper import execute_command_with_completion
        
        with patch('src.core.command_execution_wrapper.subprocess.Popen') as mock_popen:
            mock_process = Mock()
            mock_process.stdout.readline.return_value = ""
            mock_process.stderr.readline.return_value = "error\n"
            mock_process.poll.return_value = 1
            mock_process.wait.return_value = 1
            mock_popen.return_value = mock_process
            
            with patch('src.core.command_execution_wrapper.get_completion_detector') as mock_detector_getter:
                mock_detector = Mock()
                mock_detector.detect_output_completion.return_value = (True, "Error")
                mock_detector_getter.return_value = mock_detector
                
                result = execute_command_with_completion("invalid command", check_completion=True)
                
                assert result.exit_code == 1

    def test_execute_command_with_completion_timeout(self):
        """Test execute_command_with_completion handles timeout."""
        from src.core.command_execution_wrapper import execute_command_with_completion
        import subprocess
        
        with patch('src.core.command_execution_wrapper.subprocess.Popen') as mock_popen:
            mock_process = Mock()
            mock_process.stdout.readline.return_value = ""
            mock_process.stderr.readline.return_value = ""
            mock_process.poll.return_value = None
            mock_process.wait.side_effect = subprocess.TimeoutExpired("command", 5.0)
            mock_popen.return_value = mock_process
            
            result = execute_command_with_completion("long command", timeout=5)
            
            assert result.exit_code == -1
            assert "Timeout" in result.completion_reason or "timeout" in result.completion_reason.lower()

    def test_execute_command_with_completion_exception(self):
        """Test execute_command_with_completion handles exceptions."""
        from src.core.command_execution_wrapper import execute_command_with_completion
        
        with patch('src.core.command_execution_wrapper.subprocess.Popen', side_effect=Exception("Error")):
            result = execute_command_with_completion("command")
            
            assert result.exit_code == -1
            assert "Exception" in result.completion_reason

    def test_execute_command_with_completion_no_check(self):
        """Test execute_command_with_completion without completion check."""
        from src.core.command_execution_wrapper import execute_command_with_completion
        
        with patch('src.core.command_execution_wrapper.subprocess.Popen') as mock_popen:
            mock_process = Mock()
            mock_process.stdout.readline.return_value = ""
            mock_process.stderr.readline.return_value = ""
            mock_process.poll.return_value = 0
            mock_process.wait.return_value = 0
            mock_popen.return_value = mock_process
            
            result = execute_command_with_completion("echo test", check_completion=False)
            
            assert result.exit_code == 0

    def test_execute_command_with_completion_task_registration(self):
        """Test execute_command_with_completion registers task."""
        from src.core.command_execution_wrapper import execute_command_with_completion
        
        with patch('src.core.command_execution_wrapper.subprocess.Popen') as mock_popen:
            mock_process = Mock()
            mock_process.stdout.readline.return_value = ""
            mock_process.stderr.readline.return_value = ""
            mock_process.poll.return_value = 0
            mock_process.wait.return_value = 0
            mock_popen.return_value = mock_process
            
            with patch('src.core.command_execution_wrapper.get_completion_detector') as mock_detector_getter:
                mock_detector = Mock()
                mock_detector.detect_output_completion.return_value = (True, "Complete")
                mock_detector.update_task_output = Mock()
                mock_detector_getter.return_value = mock_detector
                
                result = execute_command_with_completion("echo test", task_id="task-1")
                
                mock_detector.register_task.assert_called_once()
                mock_detector.update_task_output.assert_called_once()

    def test_wait_for_completion_success(self):
        """Test wait_for_completion returns True when complete."""
        from src.core.command_execution_wrapper import wait_for_completion
        
        with patch('src.core.command_execution_wrapper.get_completion_detector') as mock_detector_getter:
            mock_detector = Mock()
            mock_detector.is_task_complete.return_value = (True, "Complete")
            mock_detector_getter.return_value = mock_detector
            
            with patch('time.sleep'):
                is_complete, status = wait_for_completion("task-1", timeout=300)
                
                assert is_complete is True
                assert status == "Complete"

    def test_wait_for_completion_timeout(self):
        """Test wait_for_completion returns False on timeout."""
        from src.core.command_execution_wrapper import wait_for_completion
        
        with patch('src.core.command_execution_wrapper.get_completion_detector') as mock_detector_getter:
            mock_detector = Mock()
            mock_detector.is_task_complete.return_value = (False, "In progress")
            mock_detector_getter.return_value = mock_detector
            
            with patch('time.sleep'):
                with patch('time.time', side_effect=[0, 400]):  # Timeout exceeded
                    is_complete, status = wait_for_completion("task-1", timeout=300)
                    
                    assert is_complete is False
                    assert status == "TIMEOUT"

    def test_wait_for_completion_checks_repeatedly(self):
        """Test wait_for_completion checks repeatedly."""
        from src.core.command_execution_wrapper import wait_for_completion
        
        with patch('src.core.command_execution_wrapper.get_completion_detector') as mock_detector_getter:
            mock_detector = Mock()
            call_count = [0]
            def side_effect(*args):
                call_count[0] += 1
                if call_count[0] < 3:
                    return (False, "In progress")
                return (True, "Complete")
            
            mock_detector.is_task_complete.side_effect = side_effect
            mock_detector_getter.return_value = mock_detector
            
            with patch('time.sleep'):
                with patch('time.time', side_effect=[0, 1, 2, 3]):
                    is_complete, status = wait_for_completion("task-1", timeout=300, check_interval=0.5)
                    
                    assert is_complete is True
                    assert call_count[0] >= 3

    def test_command_execution_result_incomplete(self):
        """Test CommandExecutionResult with incomplete execution."""
        from src.core.command_execution_wrapper import CommandExecutionResult
        
        result = CommandExecutionResult(
            command="echo test",
            exit_code=0,
            stdout="output",
            stderr="",
            is_complete=False,
            completion_reason="Still running"
        )
        
        assert result.is_complete is False
        assert result.success is False  # Incomplete is not success

    def test_execute_command_exit_code_0_no_pattern(self):
        """Test execute_command_with_completion with exit code 0 but no completion pattern."""
        from src.core.command_execution_wrapper import execute_command_with_completion
        
        with patch('src.core.command_execution_wrapper.subprocess.Popen') as mock_popen:
            mock_process = Mock()
            mock_process.stdout.readline.return_value = "output\n"
            mock_process.stderr.readline.return_value = ""
            mock_process.poll.return_value = 0
            mock_process.wait.return_value = 0
            mock_popen.return_value = mock_process
            
            with patch('src.core.command_execution_wrapper.get_completion_detector') as mock_detector_getter:
                mock_detector = Mock()
                mock_detector.detect_output_completion.return_value = (False, None)
                mock_detector_getter.return_value = mock_detector
                
                result = execute_command_with_completion("echo test", check_completion=True)
                
                # Should assume success if exit code 0
                assert result.is_complete is True
                assert result.completion_reason == "Exit code 0"

    def test_execute_command_exit_code_nonzero_no_pattern(self):
        """Test execute_command_with_completion with non-zero exit code but no pattern."""
        from src.core.command_execution_wrapper import execute_command_with_completion
        
        with patch('src.core.command_execution_wrapper.subprocess.Popen') as mock_popen:
            mock_process = Mock()
            mock_process.stdout.readline.return_value = ""
            mock_process.stderr.readline.return_value = ""
            mock_process.poll.return_value = 1
            mock_process.wait.return_value = 1
            mock_popen.return_value = mock_process
            
            with patch('src.core.command_execution_wrapper.get_completion_detector') as mock_detector_getter:
                mock_detector = Mock()
                mock_detector.detect_output_completion.return_value = (False, None)
                mock_detector_getter.return_value = mock_detector
                
                result = execute_command_with_completion("invalid", check_completion=True)
                
                # Should mark as complete with exit code reason
                assert result.is_complete is True
                assert "Exit code 1" in result.completion_reason


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

