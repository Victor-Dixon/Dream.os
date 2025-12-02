"""
Unit tests for Output Flywheel integration hooks.
"""

import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from systems.output_flywheel.integration.agent_session_hooks import (
    AgentSessionHook,
    end_of_session_hook,
)
from systems.output_flywheel.integration.status_json_integration import (
    StatusJsonIntegration,
    auto_trigger_on_status_update,
)


@pytest.fixture
def temp_workspace():
    """Create temporary workspace for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = Path(tmpdir)
        agent_workspace = workspace / "agent_workspaces" / "Agent-1"
        agent_workspace.mkdir(parents=True)
        
        # Create status.json
        status_file = agent_workspace / "status.json"
        status_file.write_text(json.dumps({
            "agent_id": "Agent-1",
            "agent_name": "Test Agent",
            "current_mission": "Test Mission",
            "completed_tasks": [],
            "achievements": [],
            "last_updated": "2025-12-02 12:00:00",
        }))
        
        yield workspace


@pytest.fixture
def session_hook(temp_workspace):
    """Create AgentSessionHook instance for testing."""
    return AgentSessionHook("Agent-1", temp_workspace)


class TestAgentSessionHook:
    """Test AgentSessionHook class."""
    
    def test_assemble_work_session_basic(self, session_hook):
        """Test basic work session assembly."""
        session = session_hook.assemble_work_session("build")
        
        assert "session_id" in session
        assert session["session_type"] == "build"
        assert session["agent_id"] == "Agent-1"
        assert "timestamp" in session
        assert "metadata" in session
        assert "source_data" in session
        assert "pipeline_status" in session
    
    def test_assemble_work_session_with_metadata(self, session_hook):
        """Test work session assembly with custom metadata."""
        metadata = {"duration_minutes": 60, "files_changed": 10}
        session = session_hook.assemble_work_session("build", metadata=metadata)
        
        assert session["metadata"]["duration_minutes"] == 60
        assert session["metadata"]["files_changed"] == 10
    
    def test_save_session(self, session_hook):
        """Test session file saving."""
        session = session_hook.assemble_work_session("build")
        session_file = session_hook.save_session(session)
        
        assert session_file.exists()
        assert session_file.suffix == ".json"
        
        # Verify content
        loaded = json.loads(session_file.read_text())
        assert loaded["session_id"] == session["session_id"]
    
    @patch("systems.output_flywheel.integration.agent_session_hooks.subprocess.run")
    def test_trigger_pipeline_success(self, mock_subprocess, session_hook):
        """Test successful pipeline triggering."""
        # Mock git commands (called during assemble_work_session)
        git_result = Mock()
        git_result.returncode = 0
        git_result.stdout = ""
        git_result.stderr = ""
        
        # Mock pipeline command
        pipeline_result = Mock()
        pipeline_result.returncode = 0
        pipeline_result.stderr = ""
        
        # Configure mock to return different results for different calls
        def mock_run_side_effect(*args, **kwargs):
            cmd = args[0] if args else []
            if isinstance(cmd, list) and len(cmd) > 0:
                if cmd[0] == "git":
                    return git_result
                elif cmd[0] == "python" and "run_output_flywheel" in str(cmd):
                    return pipeline_result
            return Mock(returncode=0, stderr="")
        
        mock_subprocess.side_effect = mock_run_side_effect
        
        session = session_hook.assemble_work_session("build")
        session_file = session_hook.save_session(session)
        
        success = session_hook.trigger_pipeline(session_file)
        
        assert success is True
        # Verify pipeline was called (not git commands)
        pipeline_calls = [call for call in mock_subprocess.call_args_list 
                         if isinstance(call[0][0], list) and len(call[0][0]) > 0 
                         and call[0][0][0] == "python" and "run_output_flywheel" in str(call[0][0])]
        assert len(pipeline_calls) == 1
    
    @patch("systems.output_flywheel.integration.agent_session_hooks.subprocess.run")
    def test_trigger_pipeline_failure(self, mock_subprocess, session_hook):
        """Test pipeline triggering failure."""
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stderr = "Pipeline failed"
        mock_subprocess.return_value = mock_result
        
        session = session_hook.assemble_work_session("build")
        session_file = session_hook.save_session(session)
        
        success = session_hook.trigger_pipeline(session_file)
        
        assert success is False
    
    @patch("systems.output_flywheel.integration.agent_session_hooks.AgentSessionHook.trigger_pipeline")
    def test_end_of_session_auto_trigger(self, mock_trigger, session_hook):
        """Test end-of-session with auto-trigger."""
        mock_trigger.return_value = True
        
        result = session_hook.end_of_session("build", auto_trigger=True)
        
        assert result is not None
        mock_trigger.assert_called_once()
    
    def test_end_of_session_no_trigger(self, session_hook):
        """Test end-of-session without auto-trigger."""
        result = session_hook.end_of_session("build", auto_trigger=False)
        
        assert result is not None
        assert "session_id" in result


class TestEndOfSessionHook:
    """Test end_of_session_hook convenience function."""
    
    @patch("systems.output_flywheel.integration.agent_session_hooks.AgentSessionHook.end_of_session")
    def test_end_of_session_hook(self, mock_end_of_session, temp_workspace):
        """Test convenience function."""
        mock_end_of_session.return_value = {"session_id": "test-123", "artifacts": {}}
        
        result = end_of_session_hook("Agent-1", "build", auto_trigger=True)
        
        assert result is not None
        mock_end_of_session.assert_called_once()


class TestStatusJsonIntegration:
    """Test StatusJsonIntegration class."""
    
    def test_infer_session_type_build(self, temp_workspace):
        """Test session type inference for build sessions."""
        integration = StatusJsonIntegration("Agent-1", temp_workspace)
        status_data = {"current_mission": "Implement feature"}
        
        session_type = integration._infer_session_type(status_data)
        
        assert session_type == "build"
    
    def test_infer_session_type_trade(self, temp_workspace):
        """Test session type inference for trade sessions."""
        integration = StatusJsonIntegration("Agent-1", temp_workspace)
        status_data = {"current_mission": "Trading session"}
        
        session_type = integration._infer_session_type(status_data)
        
        assert session_type == "trade"
    
    def test_infer_session_type_life_aria(self, temp_workspace):
        """Test session type inference for life_aria sessions."""
        integration = StatusJsonIntegration("Agent-1", temp_workspace)
        status_data = {"current_mission": "Build game with Aria"}
        
        session_type = integration._infer_session_type(status_data)
        
        assert session_type == "life_aria"
    
    def test_should_trigger_with_completed_tasks(self, temp_workspace):
        """Test trigger decision with completed tasks."""
        integration = StatusJsonIntegration("Agent-1", temp_workspace)
        status_data = {"completed_tasks": ["Task 1", "Task 2"]}
        
        should_trigger = integration._should_trigger(status_data, "build")
        
        assert should_trigger is True
    
    def test_should_trigger_with_achievements(self, temp_workspace):
        """Test trigger decision with achievements."""
        integration = StatusJsonIntegration("Agent-1", temp_workspace)
        status_data = {"achievements": ["Achievement 1"]}
        
        should_trigger = integration._should_trigger(status_data, "build")
        
        assert should_trigger is True
    
    def test_update_status_with_artifacts(self, temp_workspace):
        """Test updating status.json with artifacts."""
        integration = StatusJsonIntegration("Agent-1", temp_workspace)
        artifacts = {"readme": "path/to/readme.md", "build_log": "path/to/log.md"}
        
        success = integration.update_status_with_artifacts(artifacts, "test-session-123")
        
        assert success is True
        
        # Verify status.json updated
        status_file = temp_workspace / "agent_workspaces" / "Agent-1" / "status.json"
        status_data = json.loads(status_file.read_text())
        assert "artifacts" in status_data
        assert "test-session-123" in status_data["artifacts"]


class TestAutoTriggerOnStatusUpdate:
    """Test auto_trigger_on_status_update convenience function."""
    
    @patch("systems.output_flywheel.integration.status_json_integration.StatusJsonIntegration.check_and_trigger")
    def test_auto_trigger_on_status_update(self, mock_check, temp_workspace):
        """Test convenience function."""
        mock_check.return_value = {"session_id": "test-123", "artifacts": {}}
        
        result = auto_trigger_on_status_update("Agent-1")
        
        assert result is not None
        mock_check.assert_called_once()

