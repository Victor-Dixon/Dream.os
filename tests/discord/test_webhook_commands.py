#!/usr/bin/env python3
"""
Tests for Webhook Commands
===========================

Comprehensive test suite for Discord webhook command functionality.

Author: Agent-7
Date: 2025-11-28
"""

import json
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, Mock, patch, mock_open


class TestWebhookCommands:
    """Test suite for WebhookCommands."""

    @pytest.fixture
    def commands(self):
        """Create WebhookCommands instance."""
        with patch.dict('sys.modules', {
            'discord': MagicMock(),
            'discord.ext': MagicMock(),
            'discord.ext.commands': MagicMock(),
            'discord.ui': MagicMock()
        }):
            from src.discord_commander.webhook_commands import WebhookCommands
            mock_bot = MagicMock()
            return WebhookCommands(mock_bot)

    @pytest.fixture
    def mock_ctx(self):
        """Create mock context."""
        ctx = AsyncMock()
        ctx.author = MagicMock()
        ctx.author.id = 123456789
        ctx.author.mention = "@TestUser"
        ctx.author.send = AsyncMock()
        ctx.send = AsyncMock()
        ctx.guild = MagicMock()
        ctx.guild.name = "Test Guild"
        ctx.guild.webhooks = AsyncMock(return_value=[])
        return ctx

    @pytest.fixture
    def mock_channel(self):
        """Create mock channel."""
        channel = MagicMock()
        channel.id = 987654321
        channel.name = "test-channel"
        channel.mention = "#test-channel"
        channel.create_webhook = AsyncMock()
        channel.webhooks = AsyncMock(return_value=[])
        return channel

    def test_commands_initialization(self, commands):
        """Test commands initialization."""
        assert commands is not None
        assert commands.bot is not None
        assert commands.config_dir == Path("config")

    @pytest.mark.asyncio
    async def test_create_webhook_success(self, commands, mock_ctx, mock_channel):
        """Test successful webhook creation."""
        mock_webhook = MagicMock()
        mock_webhook.id = 111222333
        mock_webhook.name = "Test Webhook"
        mock_webhook.url = "https://discord.com/api/webhooks/111222333/abc123"
        mock_channel.create_webhook.return_value = mock_webhook
        
        with patch('pathlib.Path.exists', return_value=False), \
             patch('builtins.open', mock_open()), \
             patch('json.dump'):
            await commands.create_webhook(mock_ctx, mock_channel, "Test Webhook")
            
            mock_channel.create_webhook.assert_called_once()
            mock_ctx.send.assert_called_once()
            assert mock_ctx.author.send.called  # DM sent

    @pytest.mark.asyncio
    async def test_create_webhook_forbidden(self, commands, mock_ctx, mock_channel):
        """Test webhook creation with forbidden error."""
        import discord
        mock_channel.create_webhook.side_effect = discord.Forbidden(Mock(), "Forbidden")
        
        await commands.create_webhook(mock_ctx, mock_channel, "Test Webhook")
        
        assert "permission" in str(mock_ctx.send.call_args).lower()

    @pytest.mark.asyncio
    async def test_create_webhook_exception(self, commands, mock_ctx, mock_channel):
        """Test webhook creation with exception."""
        mock_channel.create_webhook.side_effect = Exception("Test error")
        
        await commands.create_webhook(mock_ctx, mock_channel, "Test Webhook")
        
        assert "failed" in str(mock_ctx.send.call_args).lower()

    @pytest.mark.asyncio
    async def test_create_webhook_dm_forbidden(self, commands, mock_ctx, mock_channel):
        """Test webhook creation when DM is forbidden."""
        import discord
        mock_webhook = MagicMock()
        mock_webhook.id = 111222333
        mock_webhook.url = "https://test.url"
        mock_channel.create_webhook.return_value = mock_webhook
        mock_ctx.author.send.side_effect = discord.Forbidden(Mock(), "Forbidden")
        
        with patch('pathlib.Path.exists', return_value=False), \
             patch('builtins.open', mock_open()), \
             patch('json.dump'):
            await commands.create_webhook(mock_ctx, mock_channel, "Test Webhook")
            
            # Should still send to channel
            assert mock_ctx.send.called

    @pytest.mark.asyncio
    async def test_list_webhooks_channel(self, commands, mock_ctx, mock_channel):
        """Test listing webhooks for specific channel."""
        mock_webhook = MagicMock()
        mock_webhook.id = 111222333
        mock_webhook.name = "Test Webhook"
        mock_webhook.channel_id = 987654321
        mock_webhook.user = MagicMock()
        mock_webhook.user.mention = "@Creator"
        mock_channel.webhooks.return_value = [mock_webhook]
        
        await commands.list_webhooks(mock_ctx, mock_channel)
        
        mock_ctx.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_list_webhooks_all(self, commands, mock_ctx):
        """Test listing all webhooks."""
        mock_webhook = MagicMock()
        mock_webhook.id = 111222333
        mock_webhook.name = "Test Webhook"
        mock_webhook.channel_id = 987654321
        mock_webhook.user = MagicMock()
        mock_webhook.user.mention = "@Creator"
        mock_ctx.guild.webhooks.return_value = [mock_webhook]
        
        await commands.list_webhooks(mock_ctx, None)
        
        mock_ctx.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_list_webhooks_empty(self, commands, mock_ctx):
        """Test listing webhooks when none exist."""
        mock_ctx.guild.webhooks.return_value = []
        
        await commands.list_webhooks(mock_ctx, None)
        
        assert "No webhooks" in str(mock_ctx.send.call_args)

    @pytest.mark.asyncio
    async def test_list_webhooks_forbidden(self, commands, mock_ctx):
        """Test listing webhooks with forbidden error."""
        import discord
        mock_ctx.guild.webhooks.side_effect = discord.Forbidden(Mock(), "Forbidden")
        
        await commands.list_webhooks(mock_ctx, None)
        
        assert "permission" in str(mock_ctx.send.call_args).lower()

    @pytest.mark.asyncio
    async def test_list_webhooks_exception(self, commands, mock_ctx):
        """Test listing webhooks with exception."""
        mock_ctx.guild.webhooks.side_effect = Exception("Test error")
        
        await commands.list_webhooks(mock_ctx, None)
        
        assert "failed" in str(mock_ctx.send.call_args).lower()

    @pytest.mark.asyncio
    async def test_delete_webhook_success(self, commands, mock_ctx):
        """Test successful webhook deletion."""
        mock_webhook = MagicMock()
        mock_webhook.id = 111222333
        mock_webhook.name = "Test Webhook"
        mock_webhook.channel_id = 987654321
        mock_webhook.delete = AsyncMock()
        commands.bot.fetch_webhook = AsyncMock(return_value=mock_webhook)
        
        # Mock confirmation view
        with patch('src.discord_commander.webhook_commands.WebhookDeleteConfirmView') as mock_view_class:
            mock_view = MagicMock()
            mock_view.confirmed = True
            mock_view.wait = AsyncMock()
            mock_view_class.return_value = mock_view
            
            with patch.object(commands, '_remove_from_config'):
                await commands.delete_webhook(mock_ctx, "111222333")
                
                mock_webhook.delete.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_webhook_not_found(self, commands, mock_ctx):
        """Test webhook deletion when webhook not found."""
        import discord
        commands.bot.fetch_webhook = AsyncMock(side_effect=discord.NotFound(Mock(), "Not found"))
        
        await commands.delete_webhook(mock_ctx, "111222333")
        
        assert "not found" in str(mock_ctx.send.call_args).lower()

    @pytest.mark.asyncio
    async def test_delete_webhook_forbidden(self, commands, mock_ctx):
        """Test webhook deletion with forbidden error."""
        import discord
        commands.bot.fetch_webhook = AsyncMock(side_effect=discord.Forbidden(Mock(), "Forbidden"))
        
        await commands.delete_webhook(mock_ctx, "111222333")
        
        assert "permission" in str(mock_ctx.send.call_args).lower()

    @pytest.mark.asyncio
    async def test_delete_webhook_invalid_id(self, commands, mock_ctx):
        """Test webhook deletion with invalid ID."""
        commands.bot.fetch_webhook = AsyncMock(side_effect=ValueError("Invalid ID"))
        
        await commands.delete_webhook(mock_ctx, "invalid")
        
        assert "invalid" in str(mock_ctx.send.call_args).lower()

    @pytest.mark.asyncio
    async def test_delete_webhook_cancelled(self, commands, mock_ctx):
        """Test webhook deletion when cancelled."""
        mock_webhook = MagicMock()
        mock_webhook.id = 111222333
        mock_webhook.name = "Test Webhook"
        mock_webhook.channel_id = 987654321
        commands.bot.fetch_webhook = AsyncMock(return_value=mock_webhook)
        
        with patch('src.discord_commander.webhook_commands.WebhookDeleteConfirmView') as mock_view_class:
            mock_view = MagicMock()
            mock_view.confirmed = False
            mock_view.wait = AsyncMock()
            mock_view_class.return_value = mock_view
            
            await commands.delete_webhook(mock_ctx, "111222333")
            
            mock_webhook.delete.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_webhook_exception(self, commands, mock_ctx):
        """Test webhook deletion with exception."""
        commands.bot.fetch_webhook = AsyncMock(side_effect=Exception("Test error"))
        
        await commands.delete_webhook(mock_ctx, "111222333")
        
        assert "failed" in str(mock_ctx.send.call_args).lower()

    @pytest.mark.asyncio
    async def test_test_webhook_success(self, commands, mock_ctx):
        """Test successful webhook testing."""
        mock_webhook = MagicMock()
        mock_webhook.id = 111222333
        mock_webhook.name = "Test Webhook"
        mock_webhook.channel_id = 987654321
        mock_webhook.send = AsyncMock()
        commands.bot.fetch_webhook = AsyncMock(return_value=mock_webhook)
        
        await commands.test_webhook(mock_ctx, "111222333")
        
        mock_webhook.send.assert_called_once()
        mock_ctx.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_test_webhook_not_found(self, commands, mock_ctx):
        """Test webhook testing when webhook not found."""
        import discord
        commands.bot.fetch_webhook = AsyncMock(side_effect=discord.NotFound(Mock(), "Not found"))
        
        await commands.test_webhook(mock_ctx, "111222333")
        
        assert "not found" in str(mock_ctx.send.call_args).lower()

    @pytest.mark.asyncio
    async def test_test_webhook_forbidden(self, commands, mock_ctx):
        """Test webhook testing with forbidden error."""
        import discord
        commands.bot.fetch_webhook = AsyncMock(side_effect=discord.Forbidden(Mock(), "Forbidden"))
        
        await commands.test_webhook(mock_ctx, "111222333")
        
        assert "permission" in str(mock_ctx.send.call_args).lower()

    @pytest.mark.asyncio
    async def test_test_webhook_invalid_id(self, commands, mock_ctx):
        """Test webhook testing with invalid ID."""
        commands.bot.fetch_webhook = AsyncMock(side_effect=ValueError("Invalid ID"))
        
        await commands.test_webhook(mock_ctx, "invalid")
        
        assert "invalid" in str(mock_ctx.send.call_args).lower()

    @pytest.mark.asyncio
    async def test_test_webhook_exception(self, commands, mock_ctx):
        """Test webhook testing with exception."""
        commands.bot.fetch_webhook = AsyncMock(side_effect=Exception("Test error"))
        
        await commands.test_webhook(mock_ctx, "111222333")
        
        assert "failed" in str(mock_ctx.send.call_args).lower()

    @pytest.mark.asyncio
    async def test_webhook_info_success(self, commands, mock_ctx):
        """Test successful webhook info retrieval."""
        mock_webhook = MagicMock()
        mock_webhook.id = 111222333
        mock_webhook.name = "Test Webhook"
        mock_webhook.channel_id = 987654321
        mock_webhook.url = "https://test.url"
        mock_webhook.user = MagicMock()
        mock_webhook.user.mention = "@Creator"
        mock_webhook.avatar = MagicMock()
        mock_webhook.avatar.url = "https://avatar.url"
        commands.bot.fetch_webhook = AsyncMock(return_value=mock_webhook)
        
        await commands.webhook_info(mock_ctx, "111222333")
        
        mock_ctx.send.assert_called_once()
        assert mock_ctx.author.send.called  # DM sent

    @pytest.mark.asyncio
    async def test_webhook_info_no_avatar(self, commands, mock_ctx):
        """Test webhook info without avatar."""
        mock_webhook = MagicMock()
        mock_webhook.id = 111222333
        mock_webhook.name = "Test Webhook"
        mock_webhook.channel_id = 987654321
        mock_webhook.url = "https://test.url"
        mock_webhook.user = None
        mock_webhook.avatar = None
        commands.bot.fetch_webhook = AsyncMock(return_value=mock_webhook)
        
        await commands.webhook_info(mock_ctx, "111222333")
        
        mock_ctx.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_webhook_info_dm_forbidden(self, commands, mock_ctx):
        """Test webhook info when DM is forbidden."""
        import discord
        mock_webhook = MagicMock()
        mock_webhook.id = 111222333
        mock_webhook.name = "Test Webhook"
        mock_webhook.channel_id = 987654321
        mock_webhook.url = "https://test.url"
        commands.bot.fetch_webhook = AsyncMock(return_value=mock_webhook)
        mock_ctx.author.send.side_effect = discord.Forbidden(Mock(), "Forbidden")
        
        await commands.webhook_info(mock_ctx, "111222333")
        
        mock_ctx.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_webhook_info_not_found(self, commands, mock_ctx):
        """Test webhook info when webhook not found."""
        import discord
        commands.bot.fetch_webhook = AsyncMock(side_effect=discord.NotFound(Mock(), "Not found"))
        
        await commands.webhook_info(mock_ctx, "111222333")
        
        assert "not found" in str(mock_ctx.send.call_args).lower()

    @pytest.mark.asyncio
    async def test_webhook_info_invalid_id(self, commands, mock_ctx):
        """Test webhook info with invalid ID."""
        commands.bot.fetch_webhook = AsyncMock(side_effect=ValueError("Invalid ID"))
        
        await commands.webhook_info(mock_ctx, "invalid")
        
        assert "invalid" in str(mock_ctx.send.call_args).lower()

    @pytest.mark.asyncio
    async def test_webhook_info_exception(self, commands, mock_ctx):
        """Test webhook info with exception."""
        commands.bot.fetch_webhook = AsyncMock(side_effect=Exception("Test error"))
        
        await commands.webhook_info(mock_ctx, "111222333")
        
        assert "failed" in str(mock_ctx.send.call_args).lower()

    def test_remove_from_config_exists(self, commands):
        """Test removing webhook from config when file exists."""
        config_data = {
            "test_webhook": {"webhook_id": "111222333"},
            "other_webhook": {"webhook_id": "999888777"}
        }
        
        with patch('pathlib.Path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=json.dumps(config_data))), \
             patch('json.dump') as mock_dump:
            commands._remove_from_config("111222333")
            
            # Verify config was updated
            assert mock_dump.called

    def test_remove_from_config_not_exists(self, commands):
        """Test removing webhook from config when file doesn't exist."""
        with patch('pathlib.Path.exists', return_value=False):
            # Should not raise exception
            commands._remove_from_config("111222333")

    def test_remove_from_config_exception(self, commands):
        """Test removing webhook from config with exception."""
        with patch('pathlib.Path.exists', return_value=True), \
             patch('builtins.open', side_effect=Exception("Test error")):
            # Should not raise exception
            commands._remove_from_config("111222333")

    @pytest.mark.asyncio
    async def test_create_webhook_existing_config(self, commands, mock_ctx, mock_channel):
        """Test webhook creation when config file already exists."""
        mock_webhook = MagicMock()
        mock_webhook.id = 111222333
        mock_webhook.name = "Test Webhook"
        mock_webhook.url = "https://discord.com/api/webhooks/111222333/abc123"
        mock_channel.create_webhook.return_value = mock_webhook
        
        existing_config = {
            "existing_webhook": {
                "webhook_id": "999888777",
                "webhook_url": "https://existing.url"
            }
        }
        
        with patch('pathlib.Path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=json.dumps(existing_config))), \
             patch('json.load', return_value=existing_config), \
             patch('json.dump'):
            await commands.create_webhook(mock_ctx, mock_channel, "Test Webhook")
            
            mock_channel.create_webhook.assert_called_once()
            mock_ctx.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_list_webhooks_many_webhooks(self, commands, mock_ctx):
        """Test listing webhooks when there are more than 25."""
        mock_webhooks = [
            MagicMock(id=i, name=f"Webhook {i}", channel_id=987654321, user=MagicMock(mention=f"@User{i}"))
            for i in range(30)
        ]
        mock_ctx.guild.webhooks.return_value = mock_webhooks
        
        await commands.list_webhooks(mock_ctx, None)
        
        mock_ctx.send.assert_called_once()
        # Should show footer indicating more webhooks
        call_args = mock_ctx.send.call_args
        assert "25" in str(call_args) or "30" in str(call_args)

    @pytest.mark.asyncio
    async def test_delete_webhook_timeout(self, commands, mock_ctx):
        """Test webhook deletion with view timeout."""
        mock_webhook = MagicMock()
        mock_webhook.id = 111222333
        mock_webhook.name = "Test Webhook"
        mock_webhook.channel_id = 987654321
        commands.bot.fetch_webhook = AsyncMock(return_value=mock_webhook)
        
        with patch('src.discord_commander.webhook_commands.WebhookDeleteConfirmView') as mock_view_class:
            mock_view = MagicMock()
            mock_view.confirmed = False
            mock_view.wait = AsyncMock()  # Simulate timeout
            mock_view_class.return_value = mock_view
            
            await commands.delete_webhook(mock_ctx, "111222333")
            
            # Should not delete if not confirmed
            mock_webhook.delete.assert_not_called()

    @pytest.mark.asyncio
    async def test_test_webhook_send_exception(self, commands, mock_ctx):
        """Test webhook testing when send fails."""
        mock_webhook = MagicMock()
        mock_webhook.id = 111222333
        mock_webhook.name = "Test Webhook"
        mock_webhook.channel_id = 987654321
        mock_webhook.send = AsyncMock(side_effect=Exception("Send failed"))
        commands.bot.fetch_webhook = AsyncMock(return_value=mock_webhook)
        
        await commands.test_webhook(mock_ctx, "111222333")
        
        # Should handle exception
        assert "failed" in str(mock_ctx.send.call_args).lower()

    def test_remove_from_config_no_matching_webhook(self, commands):
        """Test removing webhook when ID doesn't match any in config."""
        config_data = {
            "test_webhook": {"webhook_id": "999888777"},
            "other_webhook": {"webhook_id": "777666555"}
        }
        
        with patch('pathlib.Path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=json.dumps(config_data))), \
             patch('json.dump') as mock_dump:
            commands._remove_from_config("111222333")  # ID not in config
            
            # Should still try to save (even if nothing removed)
            assert mock_dump.called

    @pytest.mark.asyncio
    async def test_webhook_info_no_user(self, commands, mock_ctx):
        """Test webhook info when webhook has no user."""
        mock_webhook = MagicMock()
        mock_webhook.id = 111222333
        mock_webhook.name = "Test Webhook"
        mock_webhook.channel_id = 987654321
        mock_webhook.url = "https://test.url"
        mock_webhook.user = None
        mock_webhook.avatar = None
        commands.bot.fetch_webhook = AsyncMock(return_value=mock_webhook)
        
        await commands.webhook_info(mock_ctx, "111222333")
        
        mock_ctx.send.assert_called_once()


class TestWebhookDeleteConfirmView:
    """Test suite for WebhookDeleteConfirmView."""

    @pytest.fixture
    def view(self):
        """Create view instance."""
        with patch.dict('sys.modules', {
            'discord': MagicMock(),
            'discord.ui': MagicMock()
        }):
            from src.discord_commander.webhook_commands import WebhookDeleteConfirmView
            mock_webhook = MagicMock()
            mock_user = MagicMock()
            mock_user.id = 123456789
            return WebhookDeleteConfirmView(mock_webhook, mock_user)

    @pytest.mark.asyncio
    async def test_confirm_button_success(self, view):
        """Test confirm button success."""
        mock_interaction = AsyncMock()
        mock_interaction.user.id = 123456789
        mock_interaction.response.is_done.return_value = False
        mock_interaction.response.send_message = AsyncMock()
        
        await view.confirm(mock_interaction, MagicMock())
        
        assert view.confirmed is True
        mock_interaction.response.send_message.assert_called_once()

    @pytest.mark.asyncio
    async def test_confirm_button_wrong_user(self, view):
        """Test confirm button with wrong user."""
        mock_interaction = AsyncMock()
        mock_interaction.user.id = 999999999  # Different user
        mock_interaction.response.is_done.return_value = False
        mock_interaction.response.send_message = AsyncMock()
        
        await view.confirm(mock_interaction, MagicMock())
        
        assert view.confirmed is False
        assert "Only the command issuer" in str(mock_interaction.response.send_message.call_args)

    @pytest.mark.asyncio
    async def test_confirm_button_exception(self, view):
        """Test confirm button with exception."""
        mock_interaction = AsyncMock()
        mock_interaction.user.id = 123456789
        mock_interaction.response.is_done.return_value = False
        mock_interaction.response.send_message = AsyncMock(side_effect=Exception("Test error"))
        
        # Should not raise exception
        try:
            await view.confirm(mock_interaction, MagicMock())
        except Exception:
            pytest.fail("Should handle exception gracefully")

    @pytest.mark.asyncio
    async def test_cancel_button_success(self, view):
        """Test cancel button success."""
        mock_interaction = AsyncMock()
        mock_interaction.user.id = 123456789
        mock_interaction.response.is_done.return_value = False
        mock_interaction.response.send_message = AsyncMock()
        
        await view.cancel(mock_interaction, MagicMock())
        
        assert view.confirmed is False
        mock_interaction.response.send_message.assert_called_once()

    @pytest.mark.asyncio
    async def test_cancel_button_wrong_user(self, view):
        """Test cancel button with wrong user."""
        mock_interaction = AsyncMock()
        mock_interaction.user.id = 999999999  # Different user
        mock_interaction.response.is_done.return_value = False
        mock_interaction.response.send_message = AsyncMock()
        
        await view.cancel(mock_interaction, MagicMock())
        
        assert "Only the command issuer" in str(mock_interaction.response.send_message.call_args)

    @pytest.mark.asyncio
    async def test_cancel_button_exception(self, view):
        """Test cancel button with exception."""
        mock_interaction = AsyncMock()
        mock_interaction.user.id = 123456789
        mock_interaction.response.is_done.return_value = False
        mock_interaction.response.send_message = AsyncMock(side_effect=Exception("Test error"))
        
        # Should not raise exception
        try:
            await view.cancel(mock_interaction, MagicMock())
        except Exception:
            pytest.fail("Should handle exception gracefully")


class TestSetupFunction:
    """Test setup function."""

    @pytest.mark.asyncio
    async def test_setup(self):
        """Test setup function."""
        from src.discord_commander.webhook_commands import setup
        
        mock_bot = AsyncMock()
        
        await setup(mock_bot)
        
        mock_bot.add_cog.assert_called_once()
