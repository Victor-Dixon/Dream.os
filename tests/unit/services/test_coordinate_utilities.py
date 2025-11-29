"""
Tests for messaging_cli_coordinate_management/utilities.py

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
import sys

# Add project root to path
project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))

from src.services.messaging_cli_coordinate_management import utilities


class TestLoadCoordsFile:
    """Test load_coords_file function."""

    def test_load_coords_file_file_exists(self):
        """Test load_coords_file with existing file."""
        test_data = {
            "agents": {
                "Agent-1": {
                    "chat_input_coordinates": [100, 200],
                    "description": "Test Agent 1",
                    "active": True
                },
                "Agent-2": {
                    "chat_input_coordinates": [150, 250],
                    "description": "Test Agent 2",
                    "active": False
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_data, f)
            temp_path = Path(f.name)
        
        try:
            with patch('src.services.messaging_cli_coordinate_management.utilities.Path') as mock_path:
                mock_path.return_value = mock_path
                mock_path.exists.return_value = True
                mock_path.read_text.return_value = json.dumps(test_data)
                
                result = utilities.load_coords_file()
                
                assert isinstance(result, dict)
        finally:
            temp_path.unlink()

    def test_load_coords_file_file_not_exists(self):
        """Test load_coords_file when file doesn't exist."""
        with patch('src.services.messaging_cli_coordinate_management.utilities.Path') as mock_path:
            mock_coord_file = Mock()
            mock_coord_file.exists.return_value = False
            mock_path.return_value = mock_coord_file
            
            result = utilities.load_coords_file()
            
            assert isinstance(result, dict)
            assert result == {}

    def test_load_coords_file_coordinate_transformation(self):
        """Test load_coords_file transforms coordinates correctly."""
        test_data = {
            "agents": {
                "Agent-1": {
                    "chat_input_coordinates": [100, 200],
                    "description": "Test Agent",
                    "active": True
                }
            }
        }
        
        with patch('src.services.messaging_cli_coordinate_management.utilities.Path') as mock_path:
            mock_coord_file = Mock()
            mock_coord_file.exists.return_value = True
            mock_coord_file.read_text.return_value = json.dumps(test_data)
            mock_path.return_value = mock_coord_file
            
            result = utilities.load_coords_file()
            
            assert "Agent-1" in result
            assert result["Agent-1"]["x"] == 100
            assert result["Agent-1"]["y"] == 200
            assert result["Agent-1"]["description"] == "Test Agent"
            assert result["Agent-1"]["active"] is True

    def test_load_coords_file_default_values(self):
        """Test load_coords_file uses default values for missing fields."""
        test_data = {
            "agents": {
                "Agent-1": {
                    "chat_input_coordinates": [0, 0]
                    # Missing description and active
                }
            }
        }
        
        with patch('src.services.messaging_cli_coordinate_management.utilities.Path') as mock_path:
            mock_coord_file = Mock()
            mock_coord_file.exists.return_value = True
            mock_coord_file.read_text.return_value = json.dumps(test_data)
            mock_path.return_value = mock_coord_file
            
            result = utilities.load_coords_file()
            
            assert result["Agent-1"]["description"] == ""
            assert result["Agent-1"]["active"] is True

    def test_load_coords_file_multiple_agents(self):
        """Test load_coords_file handles multiple agents."""
        test_data = {
            "agents": {
                "Agent-1": {
                    "chat_input_coordinates": [100, 200],
                    "description": "Agent 1",
                    "active": True
                },
                "Agent-2": {
                    "chat_input_coordinates": [300, 400],
                    "description": "Agent 2",
                    "active": False
                },
                "Agent-3": {
                    "chat_input_coordinates": [500, 600],
                    "description": "Agent 3",
                    "active": True
                }
            }
        }
        
        with patch('src.services.messaging_cli_coordinate_management.utilities.Path') as mock_path:
            mock_coord_file = Mock()
            mock_coord_file.exists.return_value = True
            mock_coord_file.read_text.return_value = json.dumps(test_data)
            mock_path.return_value = mock_coord_file
            
            result = utilities.load_coords_file()
            
            assert len(result) == 3
            assert "Agent-1" in result
            assert "Agent-2" in result
            assert "Agent-3" in result

    def test_load_coords_file_exception_handling(self):
        """Test load_coords_file handles exceptions gracefully."""
        with patch('src.services.messaging_cli_coordinate_management.utilities.Path') as mock_path:
            mock_coord_file = Mock()
            mock_coord_file.exists.side_effect = Exception("File error")
            mock_path.return_value = mock_coord_file
            
            with patch('builtins.print'):  # Suppress error output
                result = utilities.load_coords_file()
                
                assert isinstance(result, dict)
                assert result == {}

    def test_load_coords_file_invalid_json(self):
        """Test load_coords_file handles invalid JSON gracefully."""
        with patch('src.services.messaging_cli_coordinate_management.utilities.Path') as mock_path:
            mock_coord_file = Mock()
            mock_coord_file.exists.return_value = True
            mock_coord_file.read_text.return_value = "invalid json content"
            mock_path.return_value = mock_coord_file
            
            with patch('builtins.print'):  # Suppress error output
                result = utilities.load_coords_file()
                
                assert isinstance(result, dict)
                assert result == {}

    def test_load_coords_file_empty_agents(self):
        """Test load_coords_file handles empty agents dictionary."""
        test_data = {
            "agents": {}
        }
        
        with patch('src.services.messaging_cli_coordinate_management.utilities.Path') as mock_path:
            mock_coord_file = Mock()
            mock_coord_file.exists.return_value = True
            mock_coord_file.read_text.return_value = json.dumps(test_data)
            mock_path.return_value = mock_coord_file
            
            result = utilities.load_coords_file()
            
            assert isinstance(result, dict)
            assert len(result) == 0

    def test_load_coords_file_missing_agents_key(self):
        """Test load_coords_file handles missing agents key."""
        test_data = {}
        
        with patch('src.services.messaging_cli_coordinate_management.utilities.Path') as mock_path:
            mock_coord_file = Mock()
            mock_coord_file.exists.return_value = True
            mock_coord_file.read_text.return_value = json.dumps(test_data)
            mock_path.return_value = mock_coord_file
            
            result = utilities.load_coords_file()
            
            assert isinstance(result, dict)
            assert len(result) == 0

    def test_load_coords_file_missing_chat_input_coordinates(self):
        """Test load_coords_file handles missing chat_input_coordinates."""
        test_data = {
            "agents": {
                "Agent-1": {
                    "description": "Test Agent"
                }
            }
        }
        
        with patch('src.services.messaging_cli_coordinate_management.utilities.Path') as mock_path:
            mock_coord_file = Mock()
            mock_coord_file.exists.return_value = True
            mock_coord_file.read_text.return_value = json.dumps(test_data)
            mock_path.return_value = mock_coord_file
            
            result = utilities.load_coords_file()
            
            assert "Agent-1" in result
            assert result["Agent-1"]["x"] == 0
            assert result["Agent-1"]["y"] == 0

    def test_load_coords_file_read_text_exception(self):
        """Test load_coords_file handles read_text exception."""
        with patch('src.services.messaging_cli_coordinate_management.utilities.Path') as mock_path:
            mock_coord_file = Mock()
            mock_coord_file.exists.return_value = True
            mock_coord_file.read_text.side_effect = IOError("Read error")
            mock_path.return_value = mock_coord_file
            
            with patch('builtins.print'):
                result = utilities.load_coords_file()
                
                assert isinstance(result, dict)
                assert result == {}

    def test_load_coords_file_json_decode_error(self):
        """Test load_coords_file handles JSON decode error."""
        with patch('src.services.messaging_cli_coordinate_management.utilities.Path') as mock_path:
            mock_coord_file = Mock()
            mock_coord_file.exists.return_value = True
            mock_coord_file.read_text.return_value = "{ invalid json"
            mock_path.return_value = mock_coord_file
            
            with patch('builtins.print'):
                result = utilities.load_coords_file()
                
                assert isinstance(result, dict)
                assert result == {}

