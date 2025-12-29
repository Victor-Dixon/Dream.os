"""
Tests for discord_commander/discord_service.py - DiscordService class.

Target: ≥85% coverage, 12+ test methods.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, MagicMock, mock_open
import sys

# Mock pyautogui to prevent display connection errors in headless environment
mock_pyautogui = MagicMock()
sys.modules["pyautogui"] = mock_pyautogui

from datetime import datetime
from pathlib import Path
import json
import os
import sys
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

from src.discord_commander.discord_service import DiscordService, get_discord_service


class TestDiscordService:
    """Test DiscordService class."""

    def test_init_with_webhook_url(self):
        """Test DiscordService initialization with webhook URL."""
        webhook_url = "https://discord.com/api/webhooks/test"
        service = DiscordService(webhook_url=webhook_url)
        assert service.webhook_url == webhook_url
        assert service.agent_engine is not None
        assert service.devlogs_path == Path("devlogs")
        assert service.is_running is False
        assert service.session is not None

    def test_init_without_webhook_url(self):
        """Test DiscordService initialization without webhook URL."""
        with patch.dict(os.environ, {}, clear=True):
            with patch.object(Path, 'exists', return_value=False):
                service = DiscordService()
                assert service.webhook_url is None
                assert service.agent_engine is not None

    @patch.dict(os.environ, {"DISCORD_WEBHOOK_URL": "https://test.webhook.url"})
    def test_load_webhook_url_from_env(self):
        """Test loading webhook URL from environment variable."""
        service = DiscordService()
        assert service.webhook_url == "https://test.webhook.url"

    @patch.dict(os.environ, {}, clear=True)
    @patch('builtins.open', new_callable=mock_open, read_data='{"webhook_url": "https://config.webhook.url"}')
    @patch.object(Path, 'exists', return_value=True)
    def test_load_webhook_url_from_config(self, mock_exists, mock_file):
        """Test loading webhook URL from config file."""
        service = DiscordService()
        assert service.webhook_url == "https://config.webhook.url"

    @patch.dict(os.environ, {}, clear=True)
    @patch.object(Path, 'exists', return_value=False)
    def test_load_webhook_url_not_found(self, mock_exists):
        """Test loading webhook URL when not found."""
        service = DiscordService()
        assert service.webhook_url is None

    @pytest.mark.asyncio
    @patch.object(Path, 'exists', return_value=False)
    async def test_start_devlog_monitoring_no_directory(self, mock_exists):
        """Test starting devlog monitoring when directory doesn't exist."""
        service = DiscordService()
        await service.start_devlog_monitoring(check_interval=0.1)
        assert service.is_running is False

    @pytest.mark.asyncio
    @patch.object(Path, 'exists', return_value=True)
    @patch.object(DiscordService, 'test_webhook_connection', return_value=True)
    @patch.object(DiscordService, '_check_for_new_devlogs')
    async def test_start_devlog_monitoring_success(self, mock_check, mock_test, mock_exists):
        """Test successful devlog monitoring start."""
        service = DiscordService()
        service.is_running = True
        
        # Create a task that will stop after a short delay
        async def stop_soon():
            await asyncio.sleep(0.1)
            service.stop_monitoring()
        
        # Run both tasks
        await asyncio.gather(
            service.start_devlog_monitoring(check_interval=0.05),
            stop_soon()
        )
        
        assert service.is_running is False

    def test_find_new_devlogs_no_directory(self):
        """Test finding new devlogs when directory doesn't exist."""
        service = DiscordService()
        with patch.object(Path, 'exists', return_value=False):
            result = service._find_new_devlogs()
            assert result == []

    @patch.object(Path, 'exists', return_value=True)
    @patch.object(Path, 'rglob')
    @patch.object(Path, 'stat')
    def test_find_new_devlogs_with_files(self, mock_stat, mock_rglob, mock_exists):
        """Test finding new devlog files."""
        service = DiscordService()
        service.last_check_time = datetime(2020, 1, 1)
        
        # Create mock file paths
        mock_file1 = Mock(spec=Path)
        mock_file1.stat.return_value.st_mtime = 1609459200.0  # 2021-01-01
        
        mock_file2 = Mock(spec=Path)
        mock_file2.stat.return_value.st_mtime = 1640995200.0  # 2022-01-01
        
        mock_rglob.return_value = [mock_file1, mock_file2]
        
        result = service._find_new_devlogs()
        assert len(result) == 2

    @pytest.mark.asyncio
    @patch('builtins.open', new_callable=mock_open, read_data='# Test DevLog\n\nThis is a test devlog content.')
    @patch.object(DiscordService, 'send_devlog_notification', return_value=True)
    @patch.object(DiscordService, '_notify_agents_of_devlog')
    async def test_process_devlog_success(self, mock_notify, mock_send, mock_file):
        """Test successful devlog processing."""
        service = DiscordService()
        devlog_path = Path("test_devlog.md")
        
        await service._process_devlog(devlog_path)
        
        mock_send.assert_called_once()
        mock_notify.assert_called_once()

    @pytest.mark.asyncio
    @patch('builtins.open', new_callable=mock_open, read_data='# Test DevLog\n\nThis is a test devlog content.')
    @patch.object(DiscordService, 'send_devlog_notification', return_value=False)
    @patch.object(DiscordService, '_notify_agents_of_devlog')
    async def test_process_devlog_notification_failed(self, mock_notify, mock_send, mock_file):
        """Test devlog processing when notification fails."""
        service = DiscordService()
        devlog_path = Path("test_devlog.md")
        
        await service._process_devlog(devlog_path)
        
        mock_send.assert_called_once()
        mock_notify.assert_not_called()

    def test_parse_devlog_filename_full_format(self):
        """Test parsing devlog filename with full format."""
        service = DiscordService()
        filename = "2025_12_03_agent7_test_devlog.md"
        result = service._parse_devlog_filename(filename)
        
        assert result["timestamp"] == "2025_12"
        assert result["category"] == "03"
        assert result["agent"] == "agent7"
        assert result["title"] == "test_devlog"

    def test_parse_devlog_filename_short_format(self):
        """Test parsing devlog filename with short format."""
        service = DiscordService()
        filename = "test_devlog.md"
        result = service._parse_devlog_filename(filename)
        
        assert result["timestamp"] == "unknown"
        assert result["category"] == "general"
        assert result["agent"] == "Unknown"
        assert result["title"] == "test_devlog"

    def test_extract_devlog_summary_with_content(self):
        """Test extracting summary from devlog content."""
        service = DiscordService()
        content = "# Title\n\nThis is a long description that should be extracted as summary content for the devlog notification."
        result = service._extract_devlog_summary(content)
        
        assert len(result) > 0
        assert "description" in result.lower() or "summary" in result.lower()

    def test_extract_devlog_summary_empty_content(self):
        """Test extracting summary from empty devlog content."""
        service = DiscordService()
        content = ""
        result = service._extract_devlog_summary(content)
        
        assert "V2_SWARM monitoring system" in result

    @patch('requests.Session.post')
    def test_send_devlog_notification_success(self, mock_post):
        """Test successful devlog notification sending."""
        service = DiscordService(webhook_url="https://test.webhook.url")
        mock_response = Mock()
        mock_response.status_code = 204
        mock_post.return_value = mock_response
        
        devlog_data = {
            "title": "Test DevLog",
            "description": "Test description",
            "category": "test",
            "agent": "Agent-7",
            "filepath": "test.md",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        result = service.send_devlog_notification(devlog_data)
        assert result is True
        mock_post.assert_called_once()

    @patch.object(DiscordService, '_load_webhook_url', return_value=None)
    def test_send_devlog_notification_no_webhook(self, mock_load_webhook):
        """Test devlog notification when webhook URL is not set."""
        service = DiscordService(webhook_url=None)
        devlog_data = {"title": "Test"}
        
        result = service.send_devlog_notification(devlog_data)
        assert result is False

    @patch('requests.Session.post')
    def test_send_devlog_notification_failure(self, mock_post):
        """Test devlog notification when request fails."""
        service = DiscordService(webhook_url="https://test.webhook.url")
        mock_post.side_effect = Exception("Network error")
        
        devlog_data = {"title": "Test"}
        result = service.send_devlog_notification(devlog_data)
        assert result is False

    @patch('requests.Session.post')
    def test_send_agent_status_notification_success(self, mock_post):
        """Test successful agent status notification."""
        service = DiscordService(webhook_url="https://test.webhook.url")
        mock_response = Mock()
        mock_response.status_code = 204
        mock_post.return_value = mock_response
        
        agent_status = {"agent_id": "Agent-7", "status": "active"}
        result = service.send_agent_status_notification(agent_status)
        assert result is True

    @patch.object(DiscordService, '_load_webhook_url', return_value=None)
    def test_send_agent_status_notification_no_webhook(self, mock_load_webhook):
        """Test agent status notification when webhook URL is not set."""
        service = DiscordService(webhook_url=None)
        agent_status = {"agent_id": "Agent-7"}
        
        result = service.send_agent_status_notification(agent_status)
        assert result is False

    @patch('requests.Session.post')
    def test_send_swarm_coordination_notification_success(self, mock_post):
        """Test successful swarm coordination notification."""
        service = DiscordService(webhook_url="https://test.webhook.url")
        mock_response = Mock()
        mock_response.status_code = 204
        mock_post.return_value = mock_response
        
        coordination_data = {"message": "Test coordination"}
        result = service.send_swarm_coordination_notification(coordination_data)
        assert result is True

    @patch('requests.Session.post')
    def test_test_webhook_connection_success(self, mock_post):
        """Test successful webhook connection test."""
        service = DiscordService(webhook_url="https://test.webhook.url")
        mock_response = Mock()
        mock_response.status_code = 204
        mock_post.return_value = mock_response
        
        result = service.test_webhook_connection()
        assert result is True

    @patch.object(DiscordService, '_load_webhook_url', return_value=None)
    def test_test_webhook_connection_no_webhook(self, mock_load_webhook):
        """Test webhook connection when webhook URL is not set."""
        service = DiscordService(webhook_url=None)
        result = service.test_webhook_connection()
        assert result is False

    @patch('requests.Session.post')
    def test_test_webhook_connection_failure(self, mock_post):
        """Test webhook connection when request fails."""
        service = DiscordService(webhook_url="https://test.webhook.url")
        mock_response = Mock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response
        
        result = service.test_webhook_connection()
        assert result is False

    @patch('requests.Session.post')
    def test_test_webhook_connection_exception(self, mock_post):
        """Test webhook connection when exception occurs."""
        service = DiscordService(webhook_url="https://test.webhook.url")
        mock_post.side_effect = Exception("Connection error")
        
        result = service.test_webhook_connection()
        assert result is False

    def test_stop_monitoring(self):
        """Test stopping devlog monitoring."""
        service = DiscordService()
        service.is_running = True
        service.stop_monitoring()
        assert service.is_running is False

    @pytest.mark.asyncio
    @patch.object(DiscordService, 'test_webhook_connection', return_value=True)
    @patch.object(DiscordService, 'send_devlog_notification', return_value=True)
    async def test_test_integration_success(self, mock_send, mock_test):
        """Test successful integration test."""
        service = DiscordService(webhook_url="https://test.webhook.url")
        mock_result = Mock()
        mock_result.success = True
        service.agent_engine.broadcast_to_all_agents = AsyncMock(return_value=mock_result)
        
        result = await service.test_integration()
        assert result is True

    @pytest.mark.asyncio
    @patch.object(DiscordService, 'test_webhook_connection', return_value=False)
    async def test_test_integration_webhook_fail(self, mock_test):
        """Test integration test when webhook fails."""
        service = DiscordService()
        result = await service.test_integration()
        assert result is False


class TestDiscordServiceSingleton:
    """Test DiscordService singleton pattern."""

    def test_get_discord_service_singleton(self):
        """Test get_discord_service returns singleton instance."""
        # Clear any existing instance
        import src.discord_commander.discord_service as ds_module
        ds_module._discord_service_instance = None
        
        service1 = get_discord_service()
        service2 = get_discord_service()
        
        assert service1 is service2

    def test_get_discord_service_with_webhook(self):
        """Test get_discord_service with webhook URL."""
        import src.discord_commander.discord_service as ds_module
        ds_module._discord_service_instance = None
        
        service = get_discord_service(webhook_url="https://test.webhook.url")
        assert service.webhook_url == "https://test.webhook.url"


# Helper for async mocking
class AsyncMock(Mock):
    """Async mock helper."""
    async def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)

