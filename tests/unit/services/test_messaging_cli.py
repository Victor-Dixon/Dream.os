#!/usr/bin/env python3
"""
Tests for Messaging CLI
=======================

Comprehensive tests for messaging CLI functionality.

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-01-27
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(project_root))


class TestMessagingCLI:
    """Test suite for MessagingCLI."""

    @pytest.fixture
    def mock_messaging_available(self):
        """Mock messaging system availability."""
        with patch('src.services.messaging_cli.MESSAGING_AVAILABLE', True):
            with patch('src.services.messaging_cli.send_message') as mock_send:
                with patch('src.services.messaging_cli.UnifiedMessageType') as mock_type:
                    with patch('src.services.messaging_cli.UnifiedMessagePriority') as mock_priority:
                        with patch('src.services.messaging_cli.UnifiedMessageTag') as mock_tag:
                            yield {
                                'send_message': mock_send,
                                'UnifiedMessageType': mock_type,
                                'UnifiedMessagePriority': mock_priority,
                                'UnifiedMessageTag': mock_tag
                            }

    @pytest.fixture
    def mock_parser(self):
        """Mock argument parser."""
        parser = MagicMock()
        parser.parse_args.return_value = MagicMock()
        return parser

    @pytest.fixture
    def mock_task_handler_available(self):
        """Mock task handler availability."""
        with patch('src.services.messaging_cli.TASK_HANDLER_AVAILABLE', True):
            with patch('src.services.messaging_cli.TaskHandler') as mock_handler_class:
                mock_handler = MagicMock()
                mock_handler.can_handle.return_value = False
                mock_handler.handle.return_value = None
                mock_handler.exit_code = 0
                mock_handler_class.return_value = mock_handler
                yield mock_handler

    def test_init(self, mock_messaging_available):
        """Test CLI initialization."""
        from src.services.messaging_cli import MessagingCLI
        
        with patch('src.services.messaging_cli.create_messaging_parser') as mock_create:
            mock_create.return_value = MagicMock()
            with patch('src.services.messaging_cli.TASK_HANDLER_AVAILABLE', False):
                cli = MessagingCLI()
                
                assert cli.parser is not None
                assert cli.task_handler is None

    def test_init_with_task_handler(self, mock_messaging_available):
        """Test CLI initialization with task handler."""
        from src.services.messaging_cli import MessagingCLI
        
        with patch('src.services.messaging_cli.create_messaging_parser') as mock_create:
            mock_create.return_value = MagicMock()
            with patch('src.services.messaging_cli.TASK_HANDLER_AVAILABLE', True):
                with patch('src.services.messaging_cli.TaskHandler') as mock_handler_class:
                    mock_handler = MagicMock()
                    mock_handler_class.return_value = mock_handler
                    
                    cli = MessagingCLI()
                    
                    assert cli.parser is not None
                    assert cli.task_handler is not None

    def test_execute_messaging_unavailable(self):
        """Test execute when messaging system unavailable."""
        from src.services.messaging_cli import MessagingCLI
        
        with patch('src.services.messaging_cli.MESSAGING_AVAILABLE', False):
            with patch('src.services.messaging_cli.create_messaging_parser') as mock_create:
                mock_create.return_value = MagicMock()
                cli = MessagingCLI()
                
                result = cli.execute()
                
                assert result == 1

    def test_execute_message_command(self, mock_messaging_available):
        """Test execute with message command."""
        from src.services.messaging_cli import MessagingCLI
        
        with patch('src.services.messaging_cli.create_messaging_parser') as mock_create:
            parser = MagicMock()
            parsed_args = MagicMock()
            parsed_args.message = "Test message"
            parsed_args.broadcast = None
            parsed_args.survey_coordination = None
            parsed_args.consolidation_coordination = None
            parsed_args.coordinates = None
            parsed_args.start = None
            parsed_args.save = None
            parsed_args.leaderboard = None
            parser.parse_args.return_value = parsed_args
            mock_create.return_value = parser
            
            with patch('src.services.messaging_cli.handle_message') as mock_handle:
                mock_handle.return_value = 0
                with patch('src.services.messaging_cli.TASK_HANDLER_AVAILABLE', False):
                    cli = MessagingCLI()
                    
                    result = cli.execute()
                    
                    assert result == 0
                    mock_handle.assert_called_once_with(parsed_args, parser)

    def test_execute_broadcast_command(self, mock_messaging_available):
        """Test execute with broadcast command."""
        from src.services.messaging_cli import MessagingCLI
        
        with patch('src.services.messaging_cli.create_messaging_parser') as mock_create:
            parser = MagicMock()
            parsed_args = MagicMock()
            parsed_args.message = None
            parsed_args.broadcast = True
            parsed_args.survey_coordination = None
            parsed_args.consolidation_coordination = None
            parsed_args.coordinates = None
            parsed_args.start = None
            parsed_args.save = None
            parsed_args.leaderboard = None
            parser.parse_args.return_value = parsed_args
            
            with patch('src.services.messaging_cli.handle_message') as mock_handle:
                mock_handle.return_value = 0
                with patch('src.services.messaging_cli.TASK_HANDLER_AVAILABLE', False):
                    mock_create.return_value = parser
                    cli = MessagingCLI()
                    
                    result = cli.execute()
                    
                    assert result == 0
                    mock_handle.assert_called_once_with(parsed_args, parser)

    def test_execute_survey_command(self, mock_messaging_available):
        """Test execute with survey command."""
        from src.services.messaging_cli import MessagingCLI
        
        with patch('src.services.messaging_cli.create_messaging_parser') as mock_create:
            parser = MagicMock()
            parsed_args = MagicMock()
            parsed_args.message = None
            parsed_args.broadcast = None
            parsed_args.survey_coordination = True
            parsed_args.consolidation_coordination = None
            parsed_args.coordinates = None
            parsed_args.start = None
            parsed_args.save = None
            parsed_args.leaderboard = None
            parser.parse_args.return_value = parsed_args
            
            with patch('src.services.messaging_cli.handle_survey') as mock_handle:
                mock_handle.return_value = 0
                with patch('src.services.messaging_cli.TASK_HANDLER_AVAILABLE', False):
                    mock_create.return_value = parser
                    cli = MessagingCLI()
                    
                    result = cli.execute()
                    
                    assert result == 0
                    mock_handle.assert_called_once()

    def test_execute_consolidation_command(self, mock_messaging_available):
        """Test execute with consolidation command."""
        from src.services.messaging_cli import MessagingCLI
        
        with patch('src.services.messaging_cli.create_messaging_parser') as mock_create:
            parser = MagicMock()
            parsed_args = MagicMock()
            parsed_args.message = None
            parsed_args.broadcast = None
            parsed_args.survey_coordination = None
            parsed_args.consolidation_coordination = True
            parsed_args.coordinates = None
            parsed_args.start = None
            parsed_args.save = None
            parsed_args.leaderboard = None
            parser.parse_args.return_value = parsed_args
            
            with patch('src.services.messaging_cli.handle_consolidation') as mock_handle:
                mock_handle.return_value = 0
                with patch('src.services.messaging_cli.TASK_HANDLER_AVAILABLE', False):
                    mock_create.return_value = parser
                    cli = MessagingCLI()
                    
                    result = cli.execute()
                    
                    assert result == 0
                    mock_handle.assert_called_once_with(parsed_args)

    def test_execute_coordinates_command(self, mock_messaging_available):
        """Test execute with coordinates command."""
        from src.services.messaging_cli import MessagingCLI
        
        with patch('src.services.messaging_cli.create_messaging_parser') as mock_create:
            parser = MagicMock()
            parsed_args = MagicMock()
            parsed_args.message = None
            parsed_args.broadcast = None
            parsed_args.survey_coordination = None
            parsed_args.consolidation_coordination = None
            parsed_args.coordinates = True
            parsed_args.start = None
            parsed_args.save = None
            parsed_args.leaderboard = None
            parser.parse_args.return_value = parsed_args
            
            with patch('src.services.messaging_cli.handle_coordinates') as mock_handle:
                mock_handle.return_value = 0
                with patch('src.services.messaging_cli.TASK_HANDLER_AVAILABLE', False):
                    mock_create.return_value = parser
                    cli = MessagingCLI()
                    
                    result = cli.execute()
                    
                    assert result == 0
                    mock_handle.assert_called_once()

    def test_execute_start_command(self, mock_messaging_available):
        """Test execute with start command."""
        from src.services.messaging_cli import MessagingCLI
        
        with patch('src.services.messaging_cli.create_messaging_parser') as mock_create:
            parser = MagicMock()
            parsed_args = MagicMock()
            parsed_args.message = None
            parsed_args.broadcast = None
            parsed_args.survey_coordination = None
            parsed_args.consolidation_coordination = None
            parsed_args.coordinates = None
            parsed_args.start = True
            parsed_args.save = None
            parsed_args.leaderboard = None
            parser.parse_args.return_value = parsed_args
            
            with patch('src.services.messaging_cli.handle_start_agents') as mock_handle:
                mock_handle.return_value = 0
                with patch('src.services.messaging_cli.TASK_HANDLER_AVAILABLE', False):
                    mock_create.return_value = parser
                    cli = MessagingCLI()
                    
                    result = cli.execute()
                    
                    assert result == 0
                    mock_handle.assert_called_once_with(parsed_args)

    def test_execute_save_command(self, mock_messaging_available):
        """Test execute with save command."""
        from src.services.messaging_cli import MessagingCLI
        
        with patch('src.services.messaging_cli.create_messaging_parser') as mock_create:
            parser = MagicMock()
            parsed_args = MagicMock()
            parsed_args.message = None
            parsed_args.broadcast = None
            parsed_args.survey_coordination = None
            parsed_args.consolidation_coordination = None
            parsed_args.coordinates = None
            parsed_args.start = None
            parsed_args.save = True
            parsed_args.leaderboard = None
            parser.parse_args.return_value = parsed_args
            
            with patch('src.services.messaging_cli.handle_save') as mock_handle:
                mock_handle.return_value = 0
                with patch('src.services.messaging_cli.TASK_HANDLER_AVAILABLE', False):
                    mock_create.return_value = parser
                    cli = MessagingCLI()
                    
                    result = cli.execute()
                    
                    assert result == 0
                    mock_handle.assert_called_once_with(parsed_args, parser)

    def test_execute_leaderboard_command(self, mock_messaging_available):
        """Test execute with leaderboard command."""
        from src.services.messaging_cli import MessagingCLI
        
        with patch('src.services.messaging_cli.create_messaging_parser') as mock_create:
            parser = MagicMock()
            parsed_args = MagicMock()
            parsed_args.message = None
            parsed_args.broadcast = None
            parsed_args.survey_coordination = None
            parsed_args.consolidation_coordination = None
            parsed_args.coordinates = None
            parsed_args.start = None
            parsed_args.save = None
            parsed_args.leaderboard = True
            parser.parse_args.return_value = parsed_args
            
            with patch('src.services.messaging_cli.handle_leaderboard') as mock_handle:
                mock_handle.return_value = 0
                with patch('src.services.messaging_cli.TASK_HANDLER_AVAILABLE', False):
                    mock_create.return_value = parser
                    cli = MessagingCLI()
                    
                    result = cli.execute()
                    
                    assert result == 0
                    mock_handle.assert_called_once()

    def test_execute_no_command(self, mock_messaging_available):
        """Test execute with no command (shows help)."""
        from src.services.messaging_cli import MessagingCLI
        
        with patch('src.services.messaging_cli.create_messaging_parser') as mock_create:
            parser = MagicMock()
            parsed_args = MagicMock()
            parsed_args.message = None
            parsed_args.broadcast = None
            parsed_args.survey_coordination = None
            parsed_args.consolidation_coordination = None
            parsed_args.coordinates = None
            parsed_args.start = None
            parsed_args.save = None
            parsed_args.leaderboard = None
            parser.parse_args.return_value = parsed_args
            
            with patch('src.services.messaging_cli.TASK_HANDLER_AVAILABLE', False):
                mock_create.return_value = parser
                cli = MessagingCLI()
                
                result = cli.execute()
                
                assert result == 0
                parser.print_help.assert_called_once()

    def test_execute_task_handler_handles(self, mock_messaging_available):
        """Test execute when task handler can handle request."""
        from src.services.messaging_cli import MessagingCLI
        
        with patch('src.services.messaging_cli.create_messaging_parser') as mock_create:
            parser = MagicMock()
            parsed_args = MagicMock()
            parser.parse_args.return_value = parsed_args
            
            with patch('src.services.messaging_cli.TASK_HANDLER_AVAILABLE', True):
                with patch('src.services.messaging_cli.TaskHandler') as mock_handler_class:
                    mock_handler = MagicMock()
                    mock_handler.can_handle.return_value = True
                    mock_handler.exit_code = 0
                    mock_handler_class.return_value = mock_handler
                    mock_create.return_value = parser
                    
                    cli = MessagingCLI()
                    
                    result = cli.execute()
                    
                    assert result == 0
                    mock_handler.can_handle.assert_called_once_with(parsed_args)
                    mock_handler.handle.assert_called_once_with(parsed_args)

    def test_execute_exception_handling(self, mock_messaging_available):
        """Test execute exception handling."""
        from src.services.messaging_cli import MessagingCLI
        
        with patch('src.services.messaging_cli.create_messaging_parser') as mock_create:
            parser = MagicMock()
            parsed_args = MagicMock()
            parsed_args.message = "Test message"  # Trigger handle_message path
            parsed_args.broadcast = None
            parsed_args.survey_coordination = None
            parsed_args.consolidation_coordination = None
            parsed_args.coordinates = None
            parsed_args.start = None
            parsed_args.save = None
            parsed_args.leaderboard = None
            parser.parse_args.return_value = parsed_args
            
            with patch('src.services.messaging_cli.handle_message') as mock_handle:
                mock_handle.side_effect = Exception("Test error")
                with patch('src.services.messaging_cli.TASK_HANDLER_AVAILABLE', False):
                    mock_create.return_value = parser
                    cli = MessagingCLI()
                    
                    result = cli.execute()
                    
                    assert result == 1

    def test_main_function(self, mock_messaging_available):
        """Test main function entry point."""
        from src.services.messaging_cli import main
        
        with patch('src.services.messaging_cli.MessagingCLI') as mock_cli_class:
            mock_cli = MagicMock()
            mock_cli.execute.return_value = 0
            mock_cli_class.return_value = mock_cli
            
            result = main()
            
            assert result == 0
            mock_cli.execute.assert_called_once()

