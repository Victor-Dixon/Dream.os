#!/usr/bin/env python3
"""
Test Common Command Base - Phase 2 Base Init Extraction Verification
==================================================================

Tests for the common command base classes extracted in Phase 2.
Verifies standardized initialization patterns across commands/controllers.

PHASE 2 EXECUTION: Base init extraction validation
V2 Compliance: Comprehensive testing for standardized base classes

Author: Agent-1 (Infrastructure & Core Systems)
Date: 2026-01-12
"""

import unittest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from src.core.base.common_command_base import (
    CommonCommandBase,
    CommonHandlerBase,
    CommonControllerBase,
    create_command_cog,
    create_handler,
    create_controller
)


class TestCommonCommandBase(unittest.TestCase):
    """Test cases for CommonCommandBase functionality."""

    def setUp(self):
        """Setup test fixtures."""
        self.mock_bot = MagicMock()
        self.mock_bot.user = MagicMock()
        self.mock_bot.user.name = "TestBot"

    @patch('discord.Embed')
    def test_common_command_initialization(self, mock_embed):
        """Test that CommonCommandBase initializes correctly."""
        # Mock discord availability
        with patch('src.core.base.common_command_base.DISCORD_AVAILABLE', True):
            class TestCommand(CommonCommandBase):
                pass

            cog = TestCommand(self.mock_bot)

            # Verify common attributes
            self.assertEqual(cog.bot, self.mock_bot)
            self.assertIsNotNone(cog.logger)
            self.assertEqual(cog.command_prefix, "!")
            self.assertEqual(cog.embed_color, 0x00ff00)
            self.assertEqual(cog.error_color, 0xff0000)

    @patch('discord.Embed')
    def test_create_embed(self, mock_embed_class):
        """Test embed creation functionality."""
        mock_embed_instance = MagicMock()
        mock_embed_class.return_value = mock_embed_instance

        with patch('src.core.base.common_command_base.DISCORD_AVAILABLE', True):
            class TestCommand(CommonCommandBase):
                pass

            cog = TestCommand(self.mock_bot)
            embed = cog.create_embed("Test Title", "Test Description", 0x0000ff)

            # Verify embed creation was called
            mock_embed_class.assert_called_once_with(
                title="Test Title",
                description="Test Description",
                color=0x0000ff
            )
            self.assertEqual(embed, mock_embed_instance)

    @patch('discord.Embed')
    def test_create_error_embed(self, mock_embed_class):
        """Test error embed creation."""
        mock_embed_instance = MagicMock()
        mock_embed_class.return_value = mock_embed_instance

        with patch('src.core.base.common_command_base.DISCORD_AVAILABLE', True):
            class TestCommand(CommonCommandBase):
                pass

            cog = TestCommand(self.mock_bot)
            embed = cog.create_error_embed("Test error message")

            # Verify error embed creation
            mock_embed_class.assert_called_once_with(
                title="❌ Error",
                description="Test error message",
                color=0xff0000
            )

    def test_discord_not_available(self):
        """Test behavior when Discord is not available."""
        with patch('src.core.base.common_command_base.DISCORD_AVAILABLE', False):
            class TestCommand(CommonCommandBase):
                pass

            cog = TestCommand(self.mock_bot)

            # Should still initialize basic attributes
            self.assertEqual(cog.bot, self.mock_bot)
            self.assertIsNotNone(cog.logger)

            # Embed methods should return None
            self.assertIsNone(cog.create_embed("test"))
            self.assertIsNone(cog.create_error_embed("test"))


class TestCommonHandlerBase(unittest.TestCase):
    """Test cases for CommonHandlerBase functionality."""

    def test_common_handler_initialization(self):
        """Test that CommonHandlerBase initializes correctly."""
        class TestHandler(CommonHandlerBase):
            pass

        handler = TestHandler("TestHandler")

        # Verify common attributes
        self.assertEqual(handler.handler_name, "TestHandler")
        self.assertIsNotNone(handler.logger)
        self.assertEqual(handler.exit_code, 0)
        self.assertEqual(handler.success_count, 0)
        self.assertEqual(handler.error_count, 0)
        self.assertIsNone(handler.last_operation)

    def test_handler_default_methods(self):
        """Test default handler methods."""
        class TestHandler(CommonHandlerBase):
            pass

        handler = TestHandler("TestHandler")

        # Test default can_handle (should return False)
        self.assertFalse(handler.can_handle(None))

        # Test default handle method
        result = handler.handle(None)
        expected = {
            'success': False,
            'error': 'Handler not implemented',
            'handler': 'TestHandler'
        }
        self.assertEqual(result, expected)

    def test_log_operation_start(self):
        """Test operation start logging."""
        class TestHandler(CommonHandlerBase):
            pass

        handler = TestHandler("TestHandler")
        handler.log_operation_start("test_operation", "arg1", "arg2", key="value")

        # Verify operation tracking
        self.assertEqual(handler.last_operation, "test_operation")
        self.assertIsNotNone(handler.logger)  # Logger should be available

    def test_log_operation_complete(self):
        """Test operation completion logging."""
        class TestHandler(CommonHandlerBase):
            pass

        handler = TestHandler("TestHandler")

        # Test successful operation
        handler.log_operation_complete("test_operation", success=True)
        self.assertEqual(handler.success_count, 1)
        self.assertEqual(handler.error_count, 0)

        # Test failed operation
        handler.log_operation_complete("test_operation", success=False, result="error details")
        self.assertEqual(handler.success_count, 1)
        self.assertEqual(handler.error_count, 1)


class TestCommonControllerBase(unittest.TestCase):
    """Test cases for CommonControllerBase functionality."""

    def test_common_controller_initialization(self):
        """Test that CommonControllerBase initializes correctly."""
        class TestController(CommonControllerBase):
            pass

        controller = TestController("TestController")

        # Verify common attributes
        self.assertEqual(controller.controller_name, "TestController")
        self.assertIsNotNone(controller.logger)
        self.assertFalse(controller.is_initialized)
        self.assertIsNone(controller.start_time)
        self.assertEqual(controller.operation_count, 0)
        self.assertEqual(controller.error_count, 0)

    def test_controller_initialization(self):
        """Test controller initialization process."""
        class TestController(CommonControllerBase):
            pass

        controller = TestController("TestController")

        # Test successful initialization
        result = controller.initialize()
        self.assertTrue(result)
        self.assertTrue(controller.is_initialized)
        self.assertIsNotNone(controller.start_time)

    def test_controller_status(self):
        """Test controller status reporting."""
        class TestController(CommonControllerBase):
            pass

        controller = TestController("TestController")
        controller.initialize()

        # Simulate some operations
        controller.operation_count = 10
        controller.error_count = 2

        status = controller.get_status()

        # Verify status structure
        self.assertEqual(status['controller_name'], "TestController")
        self.assertTrue(status['is_initialized'])
        self.assertIsInstance(status['uptime_seconds'], float)
        self.assertEqual(status['operation_count'], 10)
        self.assertEqual(status['error_count'], 2)
        self.assertEqual(status['error_rate'], 0.2)  # 2/10


class TestConvenienceFunctions(unittest.TestCase):
    """Test cases for convenience functions."""

    def test_create_command_cog(self):
        """Test create_command_cog convenience function."""
        mock_bot = MagicMock()

        class TestCog(CommonCommandBase):
            pass

        cog = create_command_cog(mock_bot, TestCog)

        # Verify cog was created and initialized
        self.assertIsInstance(cog, TestCog)
        self.assertEqual(cog.bot, mock_bot)

    def test_create_handler(self):
        """Test create_handler convenience function."""
        class TestHandler(CommonHandlerBase):
            pass

        handler = create_handler(TestHandler, "TestHandler")

        # Verify handler was created and initialized
        self.assertIsInstance(handler, TestHandler)
        self.assertEqual(handler.handler_name, "TestHandler")

    def test_create_controller(self):
        """Test create_controller convenience function."""
        class TestController(CommonControllerBase):
            pass

        controller = create_controller(TestController, "TestController", "extra_arg")

        # Verify controller was created and initialized
        self.assertIsInstance(controller, TestController)
        self.assertEqual(controller.controller_name, "TestController")
        self.assertTrue(controller.is_initialized)


class IntegrationTestCommand(CommonCommandBase):
    """Integration test class using CommonCommandBase."""

    def __init__(self, bot):
        super().__init__(bot)
        self.command_count = 0

    async def test_command(self, ctx):
        """Test command implementation."""
        self.command_count += 1
        embed = self.create_embed("Test", f"Command #{self.command_count}")
        return embed


class IntegrationTestHandler(CommonHandlerBase):
    """Integration test class using CommonHandlerBase."""

    def __init__(self):
        super().__init__("IntegrationTestHandler")

    def can_handle(self, args):
        return hasattr(args, 'test_command') and args.test_command

    def handle(self, args):
        self.log_operation_start("test_handle")
        result = {'success': True, 'handler': self.handler_name}
        self.log_operation_complete("test_handle", success=True, result=result)
        return result


class IntegrationTestController(CommonControllerBase):
    """Integration test class using CommonControllerBase."""

    def __init__(self, config_value):
        super().__init__("IntegrationTestController")
        self.config_value = config_value


class TestIntegration(unittest.TestCase):
    """Integration tests for all base classes working together."""

    def test_full_integration(self):
        """Test all base classes working in an integrated scenario."""
        # Create mock bot
        mock_bot = MagicMock()

        # Create instances of all base classes
        command = IntegrationTestCommand(mock_bot)
        handler = IntegrationTestHandler()
        controller = IntegrationTestController("test_config")

        # Verify they all initialize correctly
        self.assertIsInstance(command, CommonCommandBase)
        self.assertIsInstance(handler, CommonHandlerBase)
        self.assertIsInstance(controller, CommonControllerBase)

        # Test cross-component interaction
        # Handler processes a mock command
        mock_args = MagicMock()
        mock_args.test_command = True

        self.assertTrue(handler.can_handle(mock_args))
        result = handler.handle(mock_args)

        self.assertTrue(result['success'])
        self.assertEqual(result['handler'], "IntegrationTestHandler")
        self.assertEqual(handler.success_count, 1)

        # Controller provides status
        status = controller.get_status()
        self.assertTrue(status['is_initialized'])
        self.assertEqual(status['controller_name'], "IntegrationTestController")


if __name__ == '__main__':
    # Setup logging for test output
    import logging
    logging.basicConfig(level=logging.INFO)

    # Run tests
    unittest.main(verbosity=2)