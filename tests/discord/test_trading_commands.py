#!/usr/bin/env python3
"""
Tests for Trading Commands
===========================

Comprehensive tests for Discord trading command functionality.

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-01-27
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch, Mock
from datetime import datetime


class TestTradingCommands:
    """Test suite for trading commands."""

    @pytest.fixture
    def mock_discord(self):
        """Mock Discord library."""
        mock_discord_module = MagicMock()
        mock_commands_module = MagicMock()
        mock_commands_module.Context = MagicMock
        
        with patch.dict('sys.modules', {
            'discord': mock_discord_module,
            'discord.ext': MagicMock(),
            'discord.ext.commands': mock_commands_module,
            'discord.utils': MagicMock()
        }):
            # Mock discord.Embed
            mock_embed = MagicMock()
            mock_discord_module.Embed = MagicMock(return_value=mock_embed)
            mock_discord_module.utils.utcnow = MagicMock(
                return_value=datetime(2025, 1, 27, 12, 0, 0)
            )
            yield mock_discord_module

    @pytest.fixture
    def mock_bot(self):
        """Mock Discord bot."""
        bot = MagicMock()
        bot.add_cog = AsyncMock()
        return bot

    @pytest.fixture
    def mock_data_service(self):
        """Mock trading data service."""
        service = MagicMock()
        service.analyze_symbol = MagicMock(return_value={
            "symbol": "TSLA",
            "signal": "CALL",
            "confidence": 0.75,
            "reason": "Bullish trend",
            "price": 250.50,
            "indicators": {
                "sma_20": 245.0,
                "sma_50": 240.0,
                "current": 250.50
            }
        })
        service.get_market_conditions = MagicMock(return_value={
            "market_status": "OPEN",
            "vix": "15.5",
            "spy_trend": "BULLISH",
            "sector_rotation": "Technology",
            "risk_level": "LOW"
        })
        return service

    def test_initialization_without_data_service(self, mock_discord):
        """Test command initialization without data service."""
        with patch('src.discord_commander.trading_commands.TRADING_DATA_AVAILABLE', False):
            with patch('src.discord_commander.trading_commands.TradingDataService', None):
                from src.discord_commander.trading_commands import TradingCommands
                
                bot = MagicMock()
                commands = TradingCommands(bot)
                
                assert commands is not None
                assert commands.bot == bot
                assert commands.data_service is None

    def test_initialization_with_data_service(self, mock_discord, mock_data_service):
        """Test command initialization with data service."""
        with patch('src.discord_commander.trading_commands.TRADING_DATA_AVAILABLE', True):
            with patch('src.discord_commander.trading_commands.TradingDataService') as mock_service_class:
                mock_service_class.return_value = mock_data_service
                
                from src.discord_commander.trading_commands import TradingCommands
                
                bot = MagicMock()
                commands = TradingCommands(bot)
                
                assert commands is not None
                assert commands.bot == bot
                assert commands.data_service == mock_data_service

    def test_initialization_data_service_failure(self, mock_discord):
        """Test initialization when data service fails."""
        with patch('src.discord_commander.trading_commands.TRADING_DATA_AVAILABLE', True):
            with patch('src.discord_commander.trading_commands.TradingDataService') as mock_service_class:
                mock_service_class.side_effect = Exception("Service init failed")
                
                from src.discord_commander.trading_commands import TradingCommands
                
                bot = MagicMock()
                commands = TradingCommands(bot)
                
                assert commands is not None
                assert commands.data_service is None

    def test_generate_trading_report(self, mock_discord):
        """Test trading report generation."""
        from src.discord_commander.trading_commands import TradingCommands
        
        bot = MagicMock()
        commands = TradingCommands(bot)
        
        report = commands._generate_trading_report()
        
        assert report is not None
        assert 'date' in report
        assert 'day_name' in report
        assert 'timestamp' in report
        assert 'tsla' in report
        assert 'other_setups' in report
        assert 'market_conditions' in report
        assert isinstance(report['other_setups'], list)

    def test_analyze_tsla_with_data_service(self, mock_discord, mock_data_service):
        """Test TSLA analysis with data service."""
        with patch('src.discord_commander.trading_commands.TRADING_DATA_AVAILABLE', True):
            with patch('src.discord_commander.trading_commands.TradingDataService') as mock_service_class:
                mock_service_class.return_value = mock_data_service
                
                from src.discord_commander.trading_commands import TradingCommands
                
                bot = MagicMock()
                commands = TradingCommands(bot)
                
                analysis = commands._analyze_tsla()
                
                assert analysis is not None
                assert analysis['symbol'] == "TSLA"
                assert analysis['signal'] in ["CALL", "PUT", "UNKNOWN"]
                assert 'confidence' in analysis
                assert 'reason' in analysis
                assert 'timestamp' in analysis
                assert 'date' in analysis
                assert 'day_name' in analysis

    def test_analyze_tsla_with_fallback_analyzer(self, mock_discord):
        """Test TSLA analysis with fallback analyzer."""
        with patch('src.discord_commander.trading_commands.TRADING_DATA_AVAILABLE', False):
            with patch('tools.tsla_call_put_analyzer.analyze_tsla_simple') as mock_analyzer:
                mock_analyzer.return_value = {
                    "symbol": "TSLA",
                    "signal": "CALL",
                    "confidence": 0.70,
                    "reason": "Fallback analysis"
                }
                
                from src.discord_commander.trading_commands import TradingCommands
                
                bot = MagicMock()
                commands = TradingCommands(bot)
                
                analysis = commands._analyze_tsla()
                
                assert analysis is not None
                assert analysis['symbol'] == "TSLA"
                assert analysis['signal'] == "CALL"

    def test_analyze_tsla_final_fallback(self, mock_discord):
        """Test TSLA analysis with final fallback."""
        with patch('src.discord_commander.trading_commands.TRADING_DATA_AVAILABLE', False):
            with patch('tools.tsla_call_put_analyzer.analyze_tsla_simple', side_effect=ImportError):
                from src.discord_commander.trading_commands import TradingCommands
                
                bot = MagicMock()
                commands = TradingCommands(bot)
                
                analysis = commands._analyze_tsla()
                
                assert analysis is not None
                assert analysis['symbol'] == "TSLA"
                assert analysis['signal'] in ["CALL", "PUT"]
                assert 'confidence' in analysis
                assert 'reason' in analysis
                assert 'timestamp' in analysis

    def test_analyze_tsla_weekday_signal(self, mock_discord):
        """Test TSLA analysis for weekday (should be CALL)."""
        with patch('src.discord_commander.trading_commands.TRADING_DATA_AVAILABLE', False):
            with patch('tools.tsla_call_put_analyzer.analyze_tsla_simple', side_effect=ImportError):
                with patch('datetime.datetime') as mock_datetime:
                    mock_now = MagicMock()
                    mock_now.weekday.return_value = 2  # Wednesday
                    mock_now.strftime = MagicMock(side_effect=lambda fmt: "2025-01-27")
                    mock_datetime.now.return_value = mock_now
                    
                    from src.discord_commander.trading_commands import TradingCommands
                    
                    bot = MagicMock()
                    commands = TradingCommands(bot)
                    
                    analysis = commands._analyze_tsla()
                    
                    assert analysis['signal'] == "CALL"
                    assert analysis['confidence'] == 0.65

    def test_analyze_tsla_weekend_signal(self, mock_discord):
        """Test TSLA analysis for weekend (should be PUT)."""
        with patch('src.discord_commander.trading_commands.TRADING_DATA_AVAILABLE', False):
            with patch('tools.tsla_call_put_analyzer.analyze_tsla_simple', side_effect=ImportError):
                with patch('datetime.datetime') as mock_datetime:
                    mock_now = MagicMock()
                    mock_now.weekday.return_value = 5  # Saturday
                    mock_now.strftime = MagicMock(side_effect=lambda fmt: "2025-01-27")
                    mock_datetime.now.return_value = mock_now
                    
                    from src.discord_commander.trading_commands import TradingCommands
                    
                    bot = MagicMock()
                    commands = TradingCommands(bot)
                    
                    analysis = commands._analyze_tsla()
                    
                    assert analysis['signal'] == "PUT"
                    assert analysis['confidence'] == 0.55

    def test_get_other_setups_with_data_service(self, mock_discord, mock_data_service):
        """Test getting other setups with data service."""
        with patch('src.discord_commander.trading_commands.TRADING_DATA_AVAILABLE', True):
            with patch('src.discord_commander.trading_commands.TradingDataService') as mock_service_class:
                mock_service_class.return_value = mock_data_service
                
                # Mock analyze_symbol for different symbols
                def mock_analyze(symbol):
                    if symbol == "AAPL":
                        return {
                            "symbol": "AAPL",
                            "signal": "LONG",
                            "confidence": 0.70,
                            "reason": "Bullish",
                            "price": 150.0,
                            "indicators": {"sma_20": 148.0, "current": 150.0}
                        }
                    return {
                        "symbol": symbol,
                        "signal": "UNKNOWN",
                        "confidence": 0.0,
                        "reason": "No signal"
                    }
                
                mock_data_service.analyze_symbol = MagicMock(side_effect=mock_analyze)
                
                from src.discord_commander.trading_commands import TradingCommands
                
                bot = MagicMock()
                commands = TradingCommands(bot)
                
                setups = commands._get_other_setups()
                
                assert isinstance(setups, list)
                assert len(setups) > 0
                assert any(s['symbol'] == "AAPL" for s in setups)

    def test_get_other_setups_fallback(self, mock_discord):
        """Test getting other setups with fallback data."""
        with patch('src.discord_commander.trading_commands.TRADING_DATA_AVAILABLE', False):
            from src.discord_commander.trading_commands import TradingCommands
            
            bot = MagicMock()
            commands = TradingCommands(bot)
            
            setups = commands._get_other_setups()
            
            assert isinstance(setups, list)
            assert len(setups) >= 3  # Should have mock data
            assert any(s['symbol'] == "AAPL" for s in setups)
            assert any(s['symbol'] == "MSFT" for s in setups)
            assert any(s['symbol'] == "NVDA" for s in setups)

    def test_get_market_conditions_with_data_service(self, mock_discord, mock_data_service):
        """Test getting market conditions with data service."""
        with patch('src.discord_commander.trading_commands.TRADING_DATA_AVAILABLE', True):
            with patch('src.discord_commander.trading_commands.TradingDataService') as mock_service_class:
                mock_service_class.return_value = mock_data_service
                
                from src.discord_commander.trading_commands import TradingCommands
                
                bot = MagicMock()
                commands = TradingCommands(bot)
                
                conditions = commands._get_market_conditions()
                
                assert conditions is not None
                assert 'market_status' in conditions
                assert 'vix' in conditions
                assert 'spy_trend' in conditions
                assert 'sector_rotation' in conditions
                assert 'risk_level' in conditions

    def test_get_market_conditions_fallback(self, mock_discord):
        """Test getting market conditions with fallback."""
        with patch('src.discord_commander.trading_commands.TRADING_DATA_AVAILABLE', False):
            from src.discord_commander.trading_commands import TradingCommands
            
            bot = MagicMock()
            commands = TradingCommands(bot)
            
            conditions = commands._get_market_conditions()
            
            assert conditions is not None
            assert 'market_status' in conditions
            assert conditions['market_status'] in ["OPEN", "CLOSED"]
            assert 'risk_level' in conditions

    def test_create_trading_report_embed(self, mock_discord):
        """Test creating trading report embed."""
        from src.discord_commander.trading_commands import TradingCommands
        
        bot = MagicMock()
        commands = TradingCommands(bot)
        
        report = {
            "date": "2025-01-27",
            "day_name": "Monday",
            "timestamp": "2025-01-27 12:00:00",
            "tsla": {
                "symbol": "TSLA",
                "signal": "CALL",
                "confidence": 0.75,
                "reason": "Bullish trend",
                "price": 250.50,
                "timestamp": "2025-01-27 12:00:00",
                "date": "2025-01-27",
                "day_name": "Monday"
            },
            "other_setups": [
                {
                    "symbol": "AAPL",
                    "setup_type": "Breakout",
                    "direction": "LONG",
                    "confidence": 0.70,
                    "entry": "Above $150.00",
                    "target": "$154.50",
                    "stop": "$147.00",
                    "notes": "Watch for volume",
                    "price": 150.0
                }
            ],
            "market_conditions": {
                "market_status": "OPEN",
                "vix": "15.5",
                "spy_trend": "BULLISH",
                "sector_rotation": "Technology",
                "risk_level": "LOW"
            }
        }
        
        embed = commands._create_trading_report_embed(report)
        
        assert embed is not None
        mock_discord.Embed.assert_called_once()

    def test_create_trading_report_embed_put_signal(self, mock_discord):
        """Test embed creation with PUT signal."""
        from src.discord_commander.trading_commands import TradingCommands
        
        bot = MagicMock()
        commands = TradingCommands(bot)
        
        report = {
            "date": "2025-01-27",
            "day_name": "Saturday",
            "timestamp": "2025-01-27 12:00:00",
            "tsla": {
                "symbol": "TSLA",
                "signal": "PUT",
                "confidence": 0.55,
                "reason": "Weekend signal",
                "price": None,
                "timestamp": "2025-01-27 12:00:00",
                "date": "2025-01-27",
                "day_name": "Saturday"
            },
            "other_setups": [],
            "market_conditions": {
                "market_status": "CLOSED",
                "vix": None,
                "spy_trend": "UNKNOWN",
                "sector_rotation": "Technology",
                "risk_level": "MODERATE"
            }
        }
        
        embed = commands._create_trading_report_embed(report)
        
        assert embed is not None

    @pytest.mark.asyncio
    async def test_trading_report_command_success(self, mock_discord, mock_bot):
        """Test trading report command execution."""
        with patch('src.discord_commander.trading_commands.TRADING_DATA_AVAILABLE', False):
            from src.discord_commander.trading_commands import TradingCommands
            
            commands = TradingCommands(mock_bot)
            
            # Mock context
            ctx = AsyncMock()
            ctx.trigger_typing = AsyncMock()
            ctx.send = AsyncMock()
            
            # Mock embed creation
            mock_embed = MagicMock()
            with patch.object(commands, '_create_trading_report_embed', return_value=mock_embed):
                await commands.trading_report(ctx)
                
                ctx.trigger_typing.assert_called_once()
                ctx.send.assert_called_once_with(embed=mock_embed)

    @pytest.mark.asyncio
    async def test_trading_report_command_error(self, mock_discord, mock_bot):
        """Test trading report command error handling."""
        with patch('src.discord_commander.trading_commands.TRADING_DATA_AVAILABLE', False):
            from src.discord_commander.trading_commands import TradingCommands
            
            commands = TradingCommands(mock_bot)
            
            # Mock context
            ctx = AsyncMock()
            ctx.trigger_typing = AsyncMock()
            ctx.send = AsyncMock()
            
            # Force error in report generation
            with patch.object(commands, '_generate_trading_report', side_effect=Exception("Test error")):
                await commands.trading_report(ctx)
                
                ctx.send.assert_called_once()
                assert "Error generating trading report" in str(ctx.send.call_args)

    @pytest.mark.asyncio
    async def test_setup_function(self, mock_discord, mock_bot):
        """Test setup function for cog loading."""
        with patch('src.discord_commander.trading_commands.DISCORD_AVAILABLE', True):
            from src.discord_commander.trading_commands import setup
            
            await setup(mock_bot)
            
            mock_bot.add_cog.assert_called_once()

    def test_setup_function_no_discord(self, mock_discord):
        """Test setup function when Discord not available."""
        with patch('src.discord_commander.trading_commands.DISCORD_AVAILABLE', False):
            from src.discord_commander.trading_commands import setup
            
            # Should not raise error
            import asyncio
            asyncio.run(setup(MagicMock()))

    def test_other_setups_with_price_calculations(self, mock_discord, mock_data_service):
        """Test other setups with price-based calculations."""
        with patch('src.discord_commander.trading_commands.TRADING_DATA_AVAILABLE', True):
            with patch('src.discord_commander.trading_commands.TradingDataService') as mock_service_class:
                mock_service_class.return_value = mock_data_service
                
                def mock_analyze(symbol):
                    return {
                        "symbol": symbol,
                        "signal": "LONG" if symbol != "SPY" else "SHORT",
                        "confidence": 0.70,
                        "reason": "Test signal",
                        "price": 100.0,
                        "indicators": {
                            "sma_20": 98.0,
                            "sma_50": 95.0,
                            "current": 100.0
                        }
                    }
                
                mock_data_service.analyze_symbol = MagicMock(side_effect=mock_analyze)
                
                from src.discord_commander.trading_commands import TradingCommands
                
                bot = MagicMock()
                commands = TradingCommands(bot)
                
                setups = commands._get_other_setups()
                
                assert isinstance(setups, list)
                # Should have setups with calculated entry/target/stop
                for setup in setups:
                    if setup.get('price'):
                        assert 'entry' in setup
                        assert 'target' in setup
                        assert 'stop' in setup

    def test_other_setups_unknown_signals_filtered(self, mock_discord, mock_data_service):
        """Test that UNKNOWN signals are filtered out."""
        with patch('src.discord_commander.trading_commands.TRADING_DATA_AVAILABLE', True):
            with patch('src.discord_commander.trading_commands.TradingDataService') as mock_service_class:
                mock_service_class.return_value = mock_data_service
                
                def mock_analyze(symbol):
                    return {
                        "symbol": symbol,
                        "signal": "UNKNOWN",
                        "confidence": 0.0,
                        "reason": "No signal",
                        "price": None,
                        "indicators": {}
                    }
                
                mock_data_service.analyze_symbol = MagicMock(side_effect=mock_analyze)
                
                from src.discord_commander.trading_commands import TradingCommands
                
                bot = MagicMock()
                commands = TradingCommands(bot)
                
                setups = commands._get_other_setups()
                
                # Should fall back to mock data since all signals are UNKNOWN
                assert isinstance(setups, list)
                assert len(setups) > 0
