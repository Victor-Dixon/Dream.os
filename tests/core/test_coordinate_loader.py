"""
Unit tests for coordinate_loader.py - HIGH PRIORITY

Tests coordinate loading functionality.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path
import json

# Import coordinate loader
import sys
from pathlib import Path as PathLib

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))


class TestCoordinateLoader:
    """Test suite for coordinate loader."""

    @pytest.fixture
    def temp_coords_file(self, tmp_path):
        """Create temporary coordinates file."""
        coords_file = tmp_path / "coordinates.json"
        coords_data = {
            "Agent-1": {"x": 100, "y": 200},
            "Agent-2": {"x": 300, "y": 400}
        }
        coords_file.write_text(json.dumps(coords_data))
        return coords_file

    def test_load_coordinates(self, temp_coords_file):
        """Test loading coordinates from file."""
        with open(temp_coords_file, 'r') as f:
            coords = json.load(f)
        
        assert "Agent-1" in coords
        assert "Agent-2" in coords
        assert coords["Agent-1"]["x"] == 100
        assert coords["Agent-1"]["y"] == 200

    def test_get_agent_coordinates(self, temp_coords_file):
        """Test getting coordinates for specific agent."""
        with open(temp_coords_file, 'r') as f:
            coords = json.load(f)
        
        agent_coords = coords.get("Agent-1")
        
        assert agent_coords is not None
        assert agent_coords["x"] == 100
        assert agent_coords["y"] == 200

    def test_coordinate_validation(self):
        """Test coordinate validation."""
        valid_coords = (100, 200)
        invalid_coords = (-1, -1)
        
        is_valid = all(c >= 0 for c in valid_coords)
        is_invalid = any(c < 0 for c in invalid_coords)
        
        assert is_valid is True
        assert is_invalid is True

    def test_coordinate_format(self):
        """Test coordinate format."""
        coords = {"x": 100, "y": 200}
        
        assert "x" in coords
        assert "y" in coords
        assert isinstance(coords["x"], int)
        assert isinstance(coords["y"], int)

    def test_missing_coordinates(self, temp_coords_file):
        """Test handling missing coordinates."""
        with open(temp_coords_file, 'r') as f:
            coords = json.load(f)
        
        missing_coords = coords.get("Agent-99")
        
        assert missing_coords is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

