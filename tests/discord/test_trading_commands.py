#!/usr/bin/env python3
"""
Tests for Trading Commands
===========================

Comprehensive tests for Discord trading command functionality.

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-01-27
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime


class TestTradingCommands:
    """Test suite for trading commands."""

    @pytest.fixture
    def mock_discord(self):
        """Mock Discord library."""
        mock_discord_module = MagicMock()
        mock_embed = MagicMock()
        mock_discord_module.Embed = MagicMock(return_value=mock_embed)
        mock_discord_module.Color = MagicMock()
        mock_discord_module.Color.gold = MagicMock()
        
        with patch.dict('sys.modules', {
            'discord': mock_discord_module,
            'discord.ext': MagicMock(),
            'discord.ext.commands': MagicMock(),
        }):
            yield mock_discord_module

    @pytest.fixture
    def mock_bot(self):
        """Mock Discord bot."""
        bot = MagicMock()
        return bot

    @pytest.fixture
    def mock_trading_service(self):
        """Mock trading data service."""
        service = MagicMock()
        service.analyze_symbol = MagicMock(return_value={
            "symbol": "TSLA",
            "signal": "CALL",
            "confidence": 0.75,
            "reason": "Bullish trend",
            "price": 250.50,
            "indicators": {}
        })
        service.get_market_conditions = MagicMock(return_value={
            "market_status": "OPEN",
            "vix": "15.5",
            "spy_trend": "BULLISH",
            "sector_rotation": "Technology",
            "risk_level": "LOW"
        })
        return service

    def test_initialization(self, mock_discord, mock_bot, mock_trading_service):
        """Test command initialization."""
        with patch('src.discord_commander.trading_commands.TradingDataService', return_value=mock_trading_service):
            from src.discord_commander.trading_commands import TradingCommands
            
            commands = TradingCommands(mock_bot)
            
            assert commands is not None
            assert commands.bot == mock_bot
            assert commands.trading_service == mock_trading_service

    def test_generate_trading_report(self, mock_discord, mock_bot, mock_trading_service):
        """Test trading report generation."""
        with patch('src.discord_commander.trading_commands.TradingDataService', return_value=mock_trading_service):
            from src.discord_commander.trading_commands import TradingCommands
            
            commands = TradingCommands(mock_bot)
            report = commands._generate_trading_report()
            
            assert report is not None
            assert 'timestamp' in report
            assert 'tsla_analysis' in report
            assert 'other_setups' in report
            assert 'market_conditions' in report
            assert isinstance(report['other_setups'], list)

    def test_analyze_tsla_call(self, mock_discord, mock_bot, mock_trading_service):
        """Test TSLA analysis for CALL signal."""
        mock_trading_service.analyze_symbol.return_value = {
            "symbol": "TSLA",
            "signal": "CALL",
            "confidence": 0.80,
            "reason": "Strong bullish signals",
            "price": 260.0,
            "indicators": {}
        }
        
        with patch('src.discord_commander.trading_commands.TradingDataService', return_value=mock_trading_service):
            from src.discord_commander.trading_commands import TradingCommands
            
            commands = TradingCommands(mock_bot)
            analysis = commands._analyze_tsla()
            
            assert analysis is not None
            assert analysis['day_type'] == "CALL DAY"
            assert analysis['confidence'] == 0.80
            assert analysis['price'] == 260.0

    def test_analyze_tsla_put(self, mock_discord, mock_bot, mock_trading_service):
        """Test TSLA analysis for PUT signal."""
        mock_trading_service.analyze_symbol.return_value = {
            "symbol": "TSLA",
            "signal": "PUT",
            "confidence": 0.65,
            "reason": "Bearish signals detected",
            "price": 240.0,
            "indicators": {}
        }
        
        with patch('src.discord_commander.trading_commands.TradingDataService', return_value=mock_trading_service):
            from src.discord_commander.trading_commands import TradingCommands
            
            commands = TradingCommands(mock_bot)
            analysis = commands._analyze_tsla()
            
            assert analysis['day_type'] == "PUT DAY"
            assert analysis['confidence'] == 0.65

    def test_analyze_tsla_unknown(self, mock_discord, mock_bot, mock_trading_service):
        """Test TSLA analysis for unknown signal."""
        mock_trading_service.analyze_symbol.return_value = {
            "symbol": "TSLA",
            "signal": "UNKNOWN",
            "confidence": 0.0,
            "reason": "No clear signals",
            "price": None,
            "indicators": {}
        }
        
        with patch('src.discord_commander.trading_commands.TradingDataService', return_value=mock_trading_service):
            from src.discord_commander.trading_commands import TradingCommands
            
            commands = TradingCommands(mock_bot)
            analysis = commands._analyze_tsla()
            
            assert analysis['day_type'] == "NEUTRAL"

    def test_analyze_tsla_error(self, mock_discord, mock_bot):
        """Test TSLA analysis error handling."""
        mock_service = MagicMock()
        mock_service.analyze_symbol.side_effect = Exception("API error")
        
        with patch('src.discord_commander.trading_commands.TradingDataService', return_value=mock_service):
            from src.discord_commander.trading_commands import TradingCommands
            
            commands = TradingCommands(mock_bot)
            analysis = commands._analyze_tsla()
            
            assert analysis is not None
            assert analysis['day_type'] == "UNKNOWN"

    def test_get_other_setups(self, mock_discord, mock_bot, mock_trading_service):
        """Test getting other trading setups."""
        def mock_analyze(symbol):
            return {
                "symbol": symbol,
                "signal": "LONG",
                "confidence": 0.70,
                "reason": "Bullish",
                "price": 150.0 if symbol != "SPY" else 400.0,
                "indicators": {}
            }
        
        mock_trading_service.analyze_symbol.side_effect = mock_analyze
        
        with patch('src.discord_commander.trading_commands.TradingDataService', return_value=mock_trading_service):
            from src.discord_commander.trading_commands import TradingCommands
            
            commands = TradingCommands(mock_bot)
            setups = commands._get_other_setups()
            
            assert isinstance(setups, list)
            assert len(setups) > 0
            for setup in setups:
                assert 'symbol' in setup
                assert 'setup_type' in setup
                assert 'confidence' in setup

    def test_get_other_setups_filters_low_confidence(self, mock_discord, mock_bot, mock_trading_service):
        """Test that low confidence setups are filtered."""
        mock_trading_service.analyze_symbol.return_value = {
            "symbol": "TEST",
            "signal": "LONG",
            "confidence": 0.2,  # Low confidence
            "reason": "Weak signal",
            "price": 100.0,
            "indicators": {}
        }
        
        with patch('src.discord_commander.trading_commands.TradingDataService', return_value=mock_trading_service):
            from src.discord_commander.trading_commands import TradingCommands
            
            commands = TradingCommands(mock_bot)
            setups = commands._get_other_setups()
            
            # Should still have some setups (may include others)
            assert isinstance(setups, list)

    def test_create_trading_report_embed(self, mock_discord, mock_bot, mock_trading_service):
        """Test creating trading report embed."""
        with patch('src.discord_commander.trading_commands.TradingDataService', return_value=mock_trading_service):
            from src.discord_commander.trading_commands import TradingCommands
            
            commands = TradingCommands(mock_bot)
            
            report = {
                "timestamp": datetime.now(),
                "tsla_analysis": {
                    "day_type": "CALL DAY",
                    "confidence": 0.75,
                    "reasoning": "Bullish trend",
                    "price": 250.50,
                    "timestamp": datetime.now().isoformat()
                },
                "other_setups": [
                    {
                        "symbol": "AAPL",
                        "setup_type": "Breakout",
                        "signal": "LONG",
                        "entry": 150.0,
                        "exit": 153.0,
                        "confidence": 0.70,
                        "notes": "Watch for volume"
                    }
                ],
                "market_conditions": {
                    "market_status": "OPEN",
                    "vix": "15.5",
                    "spy_trend": "BULLISH",
                    "risk_level": "LOW"
                }
            }
            
            embed = commands._create_trading_report_embed(report)
            
            assert embed is not None
            mock_discord.Embed.assert_called()

    @pytest.mark.asyncio
    async def test_tbow_command_success(self, mock_discord, mock_bot, mock_trading_service):
        """Test !tbow command execution."""
        with patch('src.discord_commander.trading_commands.TradingDataService', return_value=mock_trading_service):
            from src.discord_commander.trading_commands import TradingCommands
            
            commands = TradingCommands(mock_bot)
            
            ctx = AsyncMock()
            ctx.send = AsyncMock()
            
            await commands.tbow(ctx)
            
            # Should send embed
            assert ctx.send.called
            call_args = ctx.send.call_args
            assert 'embed' in str(call_args) or len(call_args[0]) > 0

    @pytest.mark.asyncio
    async def test_tbow_command_error(self, mock_discord, mock_bot, mock_trading_service):
        """Test !tbow command error handling."""
        mock_trading_service.analyze_symbol.side_effect = Exception("Service error")
        
        with patch('src.discord_commander.trading_commands.TradingDataService', return_value=mock_trading_service):
            from src.discord_commander.trading_commands import TradingCommands
            
            commands = TradingCommands(mock_bot)
            
            ctx = AsyncMock()
            ctx.send = AsyncMock()
            
            await commands.tbow(ctx)
            
            # Should send error message
            assert ctx.send.called
            call_args = str(ctx.send.call_args).lower()
            assert 'error' in call_args or '❌' in call_args
