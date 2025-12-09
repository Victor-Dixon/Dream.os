"""
Integration Tests - Phase 2 Endpoints
=====================================

Tests for Phase 2 Integration endpoints (25 files wired to web layer).

Target: ≥85% coverage, comprehensive endpoint testing.
"""

import pytest
import sys
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import importlib.util

# Add project root to path
_project_root = Path(__file__).parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

# Setup Discord mocks (SSOT)
_discord_utils_path = _project_root / "tests" / "utils" / "discord_test_utils.py"
spec = importlib.util.spec_from_file_location("discord_test_utils", _discord_utils_path)
discord_test_utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(discord_test_utils)
setup_discord_mocks = discord_test_utils.setup_discord_mocks
setup_discord_mocks()

from src.web import create_app


@pytest.fixture
def client():
    """Create Flask test client."""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestTaskEndpoints:
    """Test task management endpoints."""

    def test_task_health_endpoint(self, client):
        """Test task health check endpoint."""
        response = client.get('/api/tasks/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
        assert data['service'] == 'task-management'

    def test_assign_task_endpoint_missing_task_id(self, client):
        """Test assign task endpoint with missing task_id."""
        response = client.post('/api/tasks/assign', json={})
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    @patch('src.web.task_handlers.TaskHandlers.handle_assign_task')
    def test_assign_task_endpoint_success(self, mock_handler, client):
        """Test assign task endpoint success."""
        mock_handler.return_value = ({'success': True, 'task_id': 'test-123', 'agent_id': 'Agent-1'}, 200)
        response = client.post('/api/tasks/assign', json={'task_id': 'test-123'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True

    def test_complete_task_endpoint_missing_params(self, client):
        """Test complete task endpoint with missing parameters."""
        response = client.post('/api/tasks/complete', json={})
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    @patch('src.web.task_handlers.TaskHandlers.handle_complete_task')
    def test_complete_task_endpoint_success(self, mock_handler, client):
        """Test complete task endpoint success."""
        mock_handler.return_value = ({'success': True, 'task_id': 'test-123', 'agent_id': 'Agent-1'}, 200)
        response = client.post('/api/tasks/complete', json={'task_id': 'test-123', 'agent_id': 'Agent-1'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True


class TestContractEndpoints:
    """Test contract system endpoints."""

    @patch('src.web.contract_handlers.ContractHandlers.handle_get_system_status')
    def test_contract_status_endpoint(self, mock_handler, client):
        """Test contract status endpoint."""
        mock_handler.return_value = ({'success': True, 'status': 'active'}, 200)
        response = client.get('/api/contracts/status')
        assert response.status_code == 200

    @patch('src.web.contract_handlers.ContractHandlers.handle_get_agent_status')
    def test_agent_contract_status_endpoint(self, mock_handler, client):
        """Test agent contract status endpoint."""
        mock_handler.return_value = ({'success': True, 'contracts': []}, 200)
        response = client.get('/api/contracts/agent/Agent-1')
        assert response.status_code == 200

    @patch('src.web.contract_handlers.ContractHandlers.handle_get_next_task')
    def test_next_task_endpoint(self, mock_handler, client):
        """Test get next task endpoint."""
        mock_handler.return_value = ({'success': True, 'task': None}, 200)
        response = client.post('/api/contracts/next-task', json={'agent_id': 'Agent-1'})
        assert response.status_code == 200


class TestCoreEndpoints:
    """Test core system endpoints."""

    @patch('src.web.core_handlers.CoreHandlers.handle_get_agent_lifecycle_status')
    def test_agent_lifecycle_status_endpoint(self, mock_handler, client):
        """Test agent lifecycle status endpoint."""
        mock_handler.return_value = ({'success': True, 'status': 'active'}, 200)
        response = client.get('/api/core/agent-lifecycle/Agent-1/status')
        assert response.status_code == 200

    @patch('src.web.core_handlers.CoreHandlers.handle_start_cycle')
    def test_start_agent_cycle_endpoint(self, mock_handler, client):
        """Test start agent cycle endpoint."""
        mock_handler.return_value = ({'success': True}, 200)
        response = client.post('/api/core/agent-lifecycle/Agent-1/start-cycle')
        assert response.status_code == 200

    @patch('src.web.core_handlers.CoreHandlers.handle_get_message_queue_status')
    def test_message_queue_status_endpoint(self, mock_handler, client):
        """Test message queue status endpoint."""
        mock_handler.return_value = ({'success': True, 'queue_size': 0}, 200)
        response = client.get('/api/core/message-queue/status')
        assert response.status_code == 200


class TestWorkflowEndpoints:
    """Test workflow engine endpoints."""

    @patch('src.web.workflow_handlers.WorkflowHandlers.handle_execute_workflow')
    def test_execute_workflow_endpoint(self, mock_handler, client):
        """Test execute workflow endpoint."""
        mock_handler.return_value = ({'success': True, 'workflow_id': 'test-123'}, 200)
        response = client.post('/api/workflows/execute', json={'workflow_config': {}})
        assert response.status_code == 200

    @patch('src.web.workflow_handlers.WorkflowHandlers.handle_get_workflow_status')
    def test_workflow_status_endpoint(self, mock_handler, client):
        """Test workflow status endpoint."""
        mock_handler.return_value = ({'success': True, 'status': 'running'}, 200)
        response = client.get('/api/workflows/status/test-123')
        assert response.status_code == 200


class TestServicesEndpoints:
    """Test service layer endpoints."""

    @patch('src.web.services_handlers.ServicesHandlers.handle_get_chat_presence_status')
    def test_chat_presence_status_endpoint(self, mock_handler, client):
        """Test chat presence status endpoint."""
        mock_handler.return_value = ({'success': True, 'status': 'active'}, 200)
        response = client.get('/api/services/chat-presence/status')
        assert response.status_code == 200

    @patch('src.web.services_handlers.ServicesHandlers.handle_start_chat_presence')
    def test_start_chat_presence_endpoint(self, mock_handler, client):
        """Test start chat presence endpoint."""
        mock_handler.return_value = ({'success': True}, 200)
        response = client.post('/api/services/chat-presence/start')
        assert response.status_code == 200

    @patch('src.web.services_handlers.ServicesHandlers.handle_stop_chat_presence')
    def test_stop_chat_presence_endpoint(self, mock_handler, client):
        """Test stop chat presence endpoint."""
        mock_handler.return_value = ({'success': True}, 200)
        response = client.post('/api/services/chat-presence/stop')
        assert response.status_code == 200


class TestCoordinationEndpoints:
    """Test coordination engine endpoints."""

    @patch('src.web.coordination_handlers.CoordinationHandlers.handle_get_task_coordination_status')
    def test_task_coordination_status_endpoint(self, mock_handler, client):
        """Test task coordination status endpoint."""
        mock_handler.return_value = ({'success': True, 'status': 'idle'}, 200)
        response = client.get('/api/coordination/task-coordination/status')
        assert response.status_code == 200

    @patch('src.web.coordination_handlers.CoordinationHandlers.handle_execute_task_coordination')
    def test_execute_task_coordination_endpoint(self, mock_handler, client):
        """Test execute task coordination endpoint."""
        mock_handler.return_value = ({'success': True}, 200)
        response = client.post('/api/coordination/task-coordination/execute', json={})
        assert response.status_code == 200


class TestIntegrationsEndpoints:
    """Test integration service endpoints."""

    @patch('src.web.integrations_handlers.IntegrationsHandlers.handle_jarvis_conversation')
    def test_jarvis_conversation_endpoint(self, mock_handler, client):
        """Test Jarvis conversation endpoint."""
        mock_handler.return_value = ({'success': True, 'data': 'response'}, 200)
        response = client.post('/api/integrations/jarvis/conversation', json={'message': 'test'})
        assert response.status_code == 200

    @patch('src.web.integrations_handlers.IntegrationsHandlers.handle_jarvis_vision')
    def test_jarvis_vision_endpoint(self, mock_handler, client):
        """Test Jarvis vision endpoint."""
        mock_handler.return_value = ({'success': True, 'data': 'analysis'}, 200)
        response = client.post('/api/integrations/jarvis/vision', json={'image': 'base64'})
        assert response.status_code == 200


class TestMonitoringEndpoints:
    """Test monitoring lifecycle endpoints."""

    @patch('src.web.monitoring_handlers.MonitoringHandlers.handle_get_monitoring_status')
    def test_monitoring_lifecycle_status_endpoint(self, mock_handler, client):
        """Test monitoring lifecycle status endpoint."""
        mock_handler.return_value = ({'success': True, 'status': 'active'}, 200)
        response = client.get('/api/monitoring/lifecycle/status')
        assert response.status_code == 200

    @patch('src.web.monitoring_handlers.MonitoringHandlers.handle_initialize_monitoring')
    def test_initialize_monitoring_lifecycle_endpoint(self, mock_handler, client):
        """Test initialize monitoring lifecycle endpoint."""
        mock_handler.return_value = ({'success': True}, 200)
        response = client.post('/api/monitoring/lifecycle/initialize')
        assert response.status_code == 200


class TestSchedulerEndpoints:
    """Test scheduler endpoints."""

    @patch('src.web.scheduler_handlers.SchedulerHandlers.handle_get_scheduler_status')
    def test_scheduler_status_endpoint(self, mock_handler, client):
        """Test scheduler status endpoint."""
        mock_handler.return_value = ({'success': True, 'status': 'active'}, 200)
        response = client.get('/api/scheduler/status')
        assert response.status_code == 200

    @patch('src.web.scheduler_handlers.SchedulerHandlers.handle_schedule_task')
    def test_schedule_task_endpoint(self, mock_handler, client):
        """Test schedule task endpoint."""
        mock_handler.return_value = ({'success': True, 'schedule_id': 'test-123'}, 200)
        response = client.post('/api/scheduler/schedule', json={'task': 'test'})
        assert response.status_code == 200


class TestVisionEndpoints:
    """Test vision/analysis endpoints."""

    @patch('src.web.vision_handlers.VisionHandlers.handle_analyze_color')
    def test_analyze_color_endpoint(self, mock_handler, client):
        """Test analyze color endpoint."""
        mock_handler.return_value = ({'success': True, 'colors': []}, 200)
        response = client.post('/api/vision/analyze-color', json={'image': 'base64'})
        assert response.status_code == 200

