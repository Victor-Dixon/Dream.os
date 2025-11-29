#!/usr/bin/env python3
"""
Tests for Contract Notifications
=================================

Comprehensive test suite for Discord contract notification functionality.

Author: Agent-7
Date: 2025-11-28
"""

import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime


class TestContractNotifier:
    """Test suite for ContractNotifier."""

    @pytest.fixture
    def notifier(self):
        """Create notifier instance with webhook."""
        with patch.dict('os.environ', {'DISCORD_WEBHOOK_URL': 'https://test.webhook.url'}):
            from src.discord_commander.contract_notifications import ContractNotifier
            return ContractNotifier()

    @pytest.fixture
    def notifier_no_webhook(self):
        """Create notifier instance without webhook."""
        with patch.dict('os.environ', {}, clear=True):
            from src.discord_commander.contract_notifications import ContractNotifier
            return ContractNotifier()

    def test_notifier_initialization_with_webhook(self, notifier):
        """Test notifier initialization with webhook."""
        assert notifier is not None
        assert notifier.webhook_url == 'https://test.webhook.url'

    def test_notifier_initialization_without_webhook(self, notifier_no_webhook):
        """Test notifier initialization without webhook."""
        assert notifier_no_webhook is not None
        assert notifier_no_webhook.webhook_url is None

    def test_notify_contract_assigned_success(self, notifier):
        """Test successful contract assignment notification."""
        mock_response = MagicMock()
        mock_response.status_code = 204
        
        with patch('requests.post', return_value=mock_response):
            result = notifier.notify_contract_assigned(
                contract_id="C-TEST-001",
                agent_id="Agent-7",
                contract_name="Test Contract",
                priority="HIGH",
                estimated_hours=25
            )
            assert result is True

    def test_notify_contract_assigned_no_webhook(self, notifier_no_webhook):
        """Test assignment notification without webhook."""
        result = notifier_no_webhook.notify_contract_assigned(
            contract_id="C-TEST-001",
            agent_id="Agent-7",
            contract_name="Test Contract",
            priority="HIGH",
            estimated_hours=25
        )
        assert result is False

    def test_notify_contract_assigned_failure(self, notifier):
        """Test failed assignment notification."""
        mock_response = MagicMock()
        mock_response.status_code = 400
        
        with patch('requests.post', return_value=mock_response):
            result = notifier.notify_contract_assigned(
                contract_id="C-TEST-001",
                agent_id="Agent-7",
                contract_name="Test Contract",
                priority="HIGH",
                estimated_hours=25
            )
            assert result is False

    def test_notify_contract_assigned_exception(self, notifier):
        """Test exception handling in assignment notification."""
        with patch('requests.post', side_effect=Exception("Test error")):
            result = notifier.notify_contract_assigned(
                contract_id="C-TEST-001",
                agent_id="Agent-7",
                contract_name="Test Contract",
                priority="HIGH",
                estimated_hours=25
            )
            assert result is False

    def test_notify_contract_assigned_payload(self, notifier):
        """Test assignment notification payload structure."""
        mock_response = MagicMock()
        mock_response.status_code = 204
        
        with patch('requests.post', return_value=mock_response) as mock_post:
            notifier.notify_contract_assigned(
                contract_id="C-TEST-001",
                agent_id="Agent-7",
                contract_name="Test Contract",
                priority="HIGH",
                estimated_hours=25
            )
            
            call_args = mock_post.call_args
            assert call_args is not None
            payload = call_args[1]['json']
            assert 'embeds' in payload
            assert payload['embeds'][0]['title'] == "📋 Contract Assigned: C-TEST-001"
            assert payload['embeds'][0]['color'] == 0x3498DB

    def test_notify_contract_started_success(self, notifier):
        """Test successful contract started notification."""
        mock_response = MagicMock()
        mock_response.status_code = 204
        
        with patch('requests.post', return_value=mock_response):
            result = notifier.notify_contract_started(
                contract_id="C-TEST-001",
                agent_id="Agent-7",
                contract_name="Test Contract"
            )
            assert result is True

    def test_notify_contract_started_no_webhook(self, notifier_no_webhook):
        """Test started notification without webhook."""
        result = notifier_no_webhook.notify_contract_started(
            contract_id="C-TEST-001",
            agent_id="Agent-7",
            contract_name="Test Contract"
        )
        assert result is False

    def test_notify_contract_started_failure(self, notifier):
        """Test failed started notification."""
        mock_response = MagicMock()
        mock_response.status_code = 400
        
        with patch('requests.post', return_value=mock_response):
            result = notifier.notify_contract_started(
                contract_id="C-TEST-001",
                agent_id="Agent-7",
                contract_name="Test Contract"
            )
            assert result is False

    def test_notify_contract_started_exception(self, notifier):
        """Test exception handling in started notification."""
        with patch('requests.post', side_effect=Exception("Test error")):
            result = notifier.notify_contract_started(
                contract_id="C-TEST-001",
                agent_id="Agent-7",
                contract_name="Test Contract"
            )
            assert result is False

    def test_notify_contract_started_payload(self, notifier):
        """Test started notification payload structure."""
        mock_response = MagicMock()
        mock_response.status_code = 204
        
        with patch('requests.post', return_value=mock_response) as mock_post:
            notifier.notify_contract_started(
                contract_id="C-TEST-001",
                agent_id="Agent-7",
                contract_name="Test Contract"
            )
            
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            assert payload['embeds'][0]['title'] == "🚀 Contract Started: C-TEST-001"
            assert payload['embeds'][0]['color'] == 0xF39C12

    def test_notify_contract_completed_success(self, notifier):
        """Test successful contract completion notification."""
        mock_response = MagicMock()
        mock_response.status_code = 204
        
        with patch('requests.post', return_value=mock_response):
            result = notifier.notify_contract_completed(
                contract_id="C-TEST-001",
                agent_id="Agent-7",
                contract_name="Test Contract",
                points_earned=500,
                actual_hours=22.5
            )
            assert result is True

    def test_notify_contract_completed_no_webhook(self, notifier_no_webhook):
        """Test completion notification without webhook."""
        result = notifier_no_webhook.notify_contract_completed(
            contract_id="C-TEST-001",
            agent_id="Agent-7",
            contract_name="Test Contract",
            points_earned=500,
            actual_hours=22.5
        )
        assert result is False

    def test_notify_contract_completed_failure(self, notifier):
        """Test failed completion notification."""
        mock_response = MagicMock()
        mock_response.status_code = 400
        
        with patch('requests.post', return_value=mock_response):
            result = notifier.notify_contract_completed(
                contract_id="C-TEST-001",
                agent_id="Agent-7",
                contract_name="Test Contract",
                points_earned=500,
                actual_hours=22.5
            )
            assert result is False

    def test_notify_contract_completed_exception(self, notifier):
        """Test exception handling in completion notification."""
        with patch('requests.post', side_effect=Exception("Test error")):
            result = notifier.notify_contract_completed(
                contract_id="C-TEST-001",
                agent_id="Agent-7",
                contract_name="Test Contract",
                points_earned=500,
                actual_hours=22.5
            )
            assert result is False

    def test_notify_contract_completed_payload(self, notifier):
        """Test completion notification payload structure."""
        mock_response = MagicMock()
        mock_response.status_code = 204
        
        with patch('requests.post', return_value=mock_response) as mock_post:
            notifier.notify_contract_completed(
                contract_id="C-TEST-001",
                agent_id="Agent-7",
                contract_name="Test Contract",
                points_earned=500,
                actual_hours=22.5
            )
            
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            assert payload['embeds'][0]['title'] == "✅ Contract Complete: C-TEST-001"
            assert payload['embeds'][0]['color'] == 0x2ECC71
            assert "+500 pts" in str(payload['embeds'][0]['fields'])

    def test_notify_contract_blocked_success(self, notifier):
        """Test successful contract blocked notification."""
        mock_response = MagicMock()
        mock_response.status_code = 204
        
        with patch('requests.post', return_value=mock_response):
            result = notifier.notify_contract_blocked(
                contract_id="C-TEST-001",
                agent_id="Agent-7",
                contract_name="Test Contract",
                blocker="Test blocker"
            )
            assert result is True

    def test_notify_contract_blocked_no_webhook(self, notifier_no_webhook):
        """Test blocked notification without webhook."""
        result = notifier_no_webhook.notify_contract_blocked(
            contract_id="C-TEST-001",
            agent_id="Agent-7",
            contract_name="Test Contract",
            blocker="Test blocker"
        )
        assert result is False

    def test_notify_contract_blocked_failure(self, notifier):
        """Test failed blocked notification."""
        mock_response = MagicMock()
        mock_response.status_code = 400
        
        with patch('requests.post', return_value=mock_response):
            result = notifier.notify_contract_blocked(
                contract_id="C-TEST-001",
                agent_id="Agent-7",
                contract_name="Test Contract",
                blocker="Test blocker"
            )
            assert result is False

    def test_notify_contract_blocked_exception(self, notifier):
        """Test exception handling in blocked notification."""
        with patch('requests.post', side_effect=Exception("Test error")):
            result = notifier.notify_contract_blocked(
                contract_id="C-TEST-001",
                agent_id="Agent-7",
                contract_name="Test Contract",
                blocker="Test blocker"
            )
            assert result is False

    def test_notify_contract_blocked_payload(self, notifier):
        """Test blocked notification payload structure."""
        mock_response = MagicMock()
        mock_response.status_code = 204
        
        with patch('requests.post', return_value=mock_response) as mock_post:
            notifier.notify_contract_blocked(
                contract_id="C-TEST-001",
                agent_id="Agent-7",
                contract_name="Test Contract",
                blocker="Test blocker"
            )
            
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            assert payload['embeds'][0]['title'] == "⚠️ Contract Blocked: C-TEST-001"
            assert payload['embeds'][0]['color'] == 0xE74C3C
            assert "Test blocker" in str(payload['embeds'][0]['fields'])

    def test_all_notification_types(self, notifier):
        """Test all notification types in sequence."""
        mock_response = MagicMock()
        mock_response.status_code = 204
        
        with patch('requests.post', return_value=mock_response):
            # Assignment
            result1 = notifier.notify_contract_assigned(
                "C-TEST-001", "Agent-7", "Test", "HIGH", 25
            )
            # Started
            result2 = notifier.notify_contract_started(
                "C-TEST-001", "Agent-7", "Test"
            )
            # Completed
            result3 = notifier.notify_contract_completed(
                "C-TEST-001", "Agent-7", "Test", 500, 22.5
            )
            # Blocked
            result4 = notifier.notify_contract_blocked(
                "C-TEST-001", "Agent-7", "Test", "Blocker"
            )
            
            assert all([result1, result2, result3, result4])


class TestTestFunction:
    """Test test_notifications function."""

    def test_test_notifications(self):
        """Test the test_notifications function."""
        from src.discord_commander.contract_notifications import test_notifications
        
        with patch.dict('os.environ', {'DISCORD_WEBHOOK_URL': 'https://test.webhook.url'}):
            with patch('requests.post') as mock_post:
                mock_response = MagicMock()
                mock_response.status_code = 204
                mock_post.return_value = mock_response
                
                # Should not raise exception
                try:
                    test_notifications()
                except Exception as e:
                    pytest.fail(f"test_notifications raised {e}")

    def test_notify_contract_assigned_timeout(self, notifier):
        """Test assignment notification with timeout."""
        import requests
        with patch('requests.post', side_effect=requests.Timeout("Timeout")):
            result = notifier.notify_contract_assigned(
                contract_id="C-TEST-001",
                agent_id="Agent-7",
                contract_name="Test Contract",
                priority="HIGH",
                estimated_hours=25
            )
            assert result is False

    def test_notify_contract_assigned_connection_error(self, notifier):
        """Test assignment notification with connection error."""
        import requests
        with patch('requests.post', side_effect=requests.ConnectionError("Connection error")):
            result = notifier.notify_contract_assigned(
                contract_id="C-TEST-001",
                agent_id="Agent-7",
                contract_name="Test Contract",
                priority="HIGH",
                estimated_hours=25
            )
            assert result is False

    def test_notify_contract_started_timeout(self, notifier):
        """Test started notification with timeout."""
        import requests
        with patch('requests.post', side_effect=requests.Timeout("Timeout")):
            result = notifier.notify_contract_started(
                contract_id="C-TEST-001",
                agent_id="Agent-7",
                contract_name="Test Contract"
            )
            assert result is False

    def test_notify_contract_completed_timeout(self, notifier):
        """Test completion notification with timeout."""
        import requests
        with patch('requests.post', side_effect=requests.Timeout("Timeout")):
            result = notifier.notify_contract_completed(
                contract_id="C-TEST-001",
                agent_id="Agent-7",
                contract_name="Test Contract",
                points_earned=500,
                actual_hours=22.5
            )
            assert result is False

    def test_notify_contract_blocked_timeout(self, notifier):
        """Test blocked notification with timeout."""
        import requests
        with patch('requests.post', side_effect=requests.Timeout("Timeout")):
            result = notifier.notify_contract_blocked(
                contract_id="C-TEST-001",
                agent_id="Agent-7",
                contract_name="Test Contract",
                blocker="Test blocker"
            )
            assert result is False

    def test_notify_contract_assigned_non_204_status(self, notifier):
        """Test assignment notification with non-204 status codes."""
        for status_code in [200, 201, 400, 401, 403, 404, 500]:
            mock_response = MagicMock()
            mock_response.status_code = status_code
            
            with patch('requests.post', return_value=mock_response):
                result = notifier.notify_contract_assigned(
                    contract_id="C-TEST-001",
                    agent_id="Agent-7",
                    contract_name="Test Contract",
                    priority="HIGH",
                    estimated_hours=25
                )
                assert result is False

    def test_notify_contract_assigned_payload_fields(self, notifier):
        """Test assignment notification payload has all required fields."""
        mock_response = MagicMock()
        mock_response.status_code = 204
        
        with patch('requests.post', return_value=mock_response) as mock_post:
            notifier.notify_contract_assigned(
                contract_id="C-TEST-001",
                agent_id="Agent-7",
                contract_name="Test Contract",
                priority="HIGH",
                estimated_hours=25
            )
            
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            embed = payload['embeds'][0]
            
            assert 'embeds' in payload
            assert embed['title'] == "📋 Contract Assigned: C-TEST-001"
            assert len(embed['fields']) == 4  # Agent, Priority, Est. Hours, Assigned
            assert embed['color'] == 0x3498DB

    def test_notify_contract_completed_zero_points(self, notifier):
        """Test completion notification with zero points."""
        mock_response = MagicMock()
        mock_response.status_code = 204
        
        with patch('requests.post', return_value=mock_response):
            result = notifier.notify_contract_completed(
                contract_id="C-TEST-001",
                agent_id="Agent-7",
                contract_name="Test Contract",
                points_earned=0,
                actual_hours=0.0
            )
            assert result is True

    def test_notify_contract_completed_high_values(self, notifier):
        """Test completion notification with high values."""
        mock_response = MagicMock()
        mock_response.status_code = 204
        
        with patch('requests.post', return_value=mock_response) as mock_post:
            notifier.notify_contract_completed(
                contract_id="C-TEST-001",
                agent_id="Agent-7",
                contract_name="Test Contract",
                points_earned=999999,
                actual_hours=999.99
            )
            
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            embed = payload['embeds'][0]
            
            assert "+999999 pts" in str(embed['fields'])
            assert "999.99h" in str(embed['fields'])