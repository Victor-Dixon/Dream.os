"""
Unit tests for coordinate_handler.py
Target: ≥85% coverage
"""

import pytest
import time
from unittest.mock import Mock, patch, MagicMock
from src.services.handlers.coordinate_handler import CoordinateHandler


class TestCoordinateHandler:
    """Tests for CoordinateHandler class."""

    def test_init(self):
        """Test CoordinateHandler initialization."""
        handler = CoordinateHandler()
        assert handler.logger is not None
        assert handler.coordinates_cache == {}
        assert handler.last_coordinate_load is None
        assert handler.cache_ttl_seconds == 300

    def test_can_handle_returns_false(self):
        """Test can_handle always returns False."""
        handler = CoordinateHandler()
        args = Mock()
        assert handler.can_handle(args) is False

    def test_handle_returns_false(self):
        """Test handle always returns False."""
        handler = CoordinateHandler()
        args = Mock()
        assert handler.handle(args) is False

    @pytest.mark.asyncio
    async def test_load_coordinates_async_with_cache(self):
        """Test load_coordinates_async returns cached data when valid."""
        handler = CoordinateHandler()
        handler.coordinates_cache = {"Agent-1": [100, 200]}
        handler.last_coordinate_load = time.time() - 100  # 100 seconds ago
        
        result = await handler.load_coordinates_async()
        
        assert result["success"] is True
        assert result["cached"] is True
        assert result["coordinates"] == {"Agent-1": [100, 200]}
        assert result["agent_count"] == 1

    @pytest.mark.asyncio
    async def test_load_coordinates_async_cache_expired(self):
        """Test load_coordinates_async loads fresh data when cache expired."""
        handler = CoordinateHandler()
        handler.coordinates_cache = {"Agent-1": [100, 200]}
        handler.last_coordinate_load = time.time() - 400  # Expired cache
        
        test_data = {
            "agents": {
                "Agent-2": {"chat_input_coordinates": [300, 400]}
            }
        }
        
        with patch('src.services.handlers.coordinate_handler.read_json') as mock_read:
            mock_read.return_value = test_data
            result = await handler.load_coordinates_async()
            
            assert result["success"] is True
            assert result["cached"] is False
            assert result["coordinates"] == {"Agent-2": [300, 400]}
            assert result["agent_count"] == 1

    @pytest.mark.asyncio
    async def test_load_coordinates_async_no_cache(self):
        """Test load_coordinates_async loads data when no cache exists."""
        handler = CoordinateHandler()
        
        test_data = {
            "agents": {
                "Agent-1": {"chat_input_coordinates": [100, 200]},
                "Agent-2": {"chat_input_coordinates": [300, 400]}
            }
        }
        
        with patch('src.services.handlers.coordinate_handler.read_json') as mock_read:
            mock_read.return_value = test_data
            result = await handler.load_coordinates_async()
            
            assert result["success"] is True
            assert result["cached"] is False
            assert len(result["coordinates"]) == 2
            assert result["agent_count"] == 2

    @pytest.mark.asyncio
    async def test_load_coordinates_async_missing_agents_key(self):
        """Test load_coordinates_async handles missing agents key."""
        handler = CoordinateHandler()
        
        with patch('src.services.handlers.coordinate_handler.read_json') as mock_read:
            mock_read.return_value = {}
            result = await handler.load_coordinates_async()
            
            assert result["success"] is True
            assert result["coordinates"] == {}
            assert result["agent_count"] == 0

    @pytest.mark.asyncio
    async def test_load_coordinates_async_missing_coordinates(self):
        """Test load_coordinates_async uses default coordinates when missing."""
        handler = CoordinateHandler()
        
        test_data = {
            "agents": {
                "Agent-1": {}  # Missing chat_input_coordinates
            }
        }
        
        with patch('src.services.handlers.coordinate_handler.read_json') as mock_read:
            mock_read.return_value = test_data
            result = await handler.load_coordinates_async()
            
            assert result["success"] is True
            assert result["coordinates"]["Agent-1"] == [0, 0]

    @pytest.mark.asyncio
    async def test_load_coordinates_async_exception(self):
        """Test load_coordinates_async handles exceptions."""
        handler = CoordinateHandler()
        
        with patch('src.services.handlers.coordinate_handler.read_json') as mock_read:
            mock_read.side_effect = Exception("Test error")
            result = await handler.load_coordinates_async()
            
            assert result["success"] is False
            assert "error" in result
            assert "Test error" in result["error"]

    def test_print_coordinates_table(self):
        """Test print_coordinates_table formats table correctly."""
        handler = CoordinateHandler()
        coordinates = {
            "Agent-1": [100, 200],
            "Agent-2": [300, 400]
        }
        
        with patch('src.services.handlers.coordinate_handler.logger') as mock_logger:
            handler.print_coordinates_table(coordinates)
            
            assert mock_logger.info.called
            # Verify table structure was logged
            calls = [str(call) for call in mock_logger.info.call_args_list]
            assert any("Agent Coordinates" in str(call) for call in calls)

    def test_print_coordinates_table_short_coords(self):
        """Test print_coordinates_table handles short coordinate lists."""
        handler = CoordinateHandler()
        coordinates = {
            "Agent-1": [100]  # Only one coordinate
        }
        
        with patch('src.services.handlers.coordinate_handler.logger') as mock_logger:
            handler.print_coordinates_table(coordinates)
            assert mock_logger.info.called

    def test_print_coordinates_table_exception(self):
        """Test print_coordinates_table handles exceptions."""
        handler = CoordinateHandler()
        
        with patch('src.services.handlers.coordinate_handler.logger') as mock_logger:
            # Pass invalid data to trigger exception
            handler.print_coordinates_table(None)
            assert mock_logger.error.called

    def test_get_agent_coordinates_found(self):
        """Test get_agent_coordinates returns coordinates when found."""
        handler = CoordinateHandler()
        handler.coordinates_cache = {"Agent-1": [100, 200]}
        
        result = handler.get_agent_coordinates("Agent-1")
        assert result == [100, 200]

    def test_get_agent_coordinates_not_found(self):
        """Test get_agent_coordinates returns None when not found."""
        handler = CoordinateHandler()
        handler.coordinates_cache = {"Agent-1": [100, 200]}
        
        result = handler.get_agent_coordinates("Agent-2")
        assert result is None

    def test_get_agent_coordinates_empty_cache(self):
        """Test get_agent_coordinates returns None when cache is empty."""
        handler = CoordinateHandler()
        
        result = handler.get_agent_coordinates("Agent-1")
        assert result is None

    def test_validate_coordinates_valid(self):
        """Test validate_coordinates returns True for valid coordinates."""
        handler = CoordinateHandler()
        
        assert handler.validate_coordinates([100, 200]) is True
        assert handler.validate_coordinates([100.5, 200.7]) is True
        assert handler.validate_coordinates([100, 200, 300]) is True  # Extra values OK

    def test_validate_coordinates_invalid_type(self):
        """Test validate_coordinates returns False for invalid types."""
        handler = CoordinateHandler()
        
        assert handler.validate_coordinates("not a list") is False
        assert handler.validate_coordinates(None) is False
        assert handler.validate_coordinates(100) is False

    def test_validate_coordinates_too_short(self):
        """Test validate_coordinates returns False for lists with < 2 elements."""
        handler = CoordinateHandler()
        
        assert handler.validate_coordinates([]) is False
        assert handler.validate_coordinates([100]) is False

    def test_validate_coordinates_invalid_element_types(self):
        """Test validate_coordinates returns False for invalid element types."""
        handler = CoordinateHandler()
        
        assert handler.validate_coordinates(["100", "200"]) is False
        assert handler.validate_coordinates([None, 200]) is False

    def test_clear_cache(self):
        """Test clear_cache clears cache and resets timestamp."""
        handler = CoordinateHandler()
        handler.coordinates_cache = {"Agent-1": [100, 200]}
        handler.last_coordinate_load = time.time()
        
        handler.clear_cache()
        
        assert handler.coordinates_cache == {}
        assert handler.last_coordinate_load is None

    def test_clear_cache_logs(self):
        """Test clear_cache logs the action."""
        handler = CoordinateHandler()
        
        with patch.object(handler.logger, 'info') as mock_info:
            handler.clear_cache()
            mock_info.assert_called_with('Coordinate cache cleared')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

