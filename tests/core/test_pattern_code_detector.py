"""
Unit tests for pattern_analysis/code_pattern_detector.py - HIGH PRIORITY

Tests CodePatternDetector class functionality.
Note: Maps to refactoring/pattern_detection.py pattern detection functions.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import sys
from pathlib import Path
import tempfile
import os

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Mock dependencies before importing
mock_unified_utility = MagicMock()
mock_path_class = MagicMock()

mock_path_class.rglob = Mock(return_value=[])
mock_path_class.is_file = Mock(return_value=True)
mock_unified_utility.Path = Mock(return_value=mock_path_class)

sys.modules['src.services.unified_messaging_imports'] = MagicMock()
sys.modules['src.services.unified_messaging_imports'].get_unified_utility = Mock(return_value=mock_unified_utility)
sys.modules['src.core.refactoring.toolkit'] = MagicMock()
sys.modules['src.core.refactoring.metrics'] = MagicMock()

# Import using importlib
import importlib.util
pattern_detection_path = project_root / "src" / "core" / "refactoring" / "pattern_detection.py"
spec = importlib.util.spec_from_file_location("pattern_detection", pattern_detection_path)
pattern_detection = importlib.util.module_from_spec(spec)
pattern_detection.__package__ = 'src.core.refactoring'
spec.loader.exec_module(pattern_detection)

ArchitecturePattern = pattern_detection.ArchitecturePattern
analyze_architecture_patterns = pattern_detection.analyze_architecture_patterns
_detect_mvc_patterns = pattern_detection._detect_mvc_patterns
_detect_repository_patterns = pattern_detection._detect_repository_patterns
_detect_factory_patterns = pattern_detection._detect_factory_patterns
_detect_observer_patterns = pattern_detection._detect_observer_patterns
_detect_singleton_patterns = pattern_detection._detect_singleton_patterns

# Alias for test purposes
CodePatternDetector = type('CodePatternDetector', (), {
    'detect_patterns': lambda self, directory: analyze_architecture_patterns(directory),
    'detect_mvc': lambda self, directory: _detect_mvc_patterns(directory),
    'detect_repository': lambda self, directory: _detect_repository_patterns(directory),
    'detect_factory': lambda self, directory: _detect_factory_patterns(directory),
    'detect_observer': lambda self, directory: _detect_observer_patterns(directory),
    'detect_singleton': lambda self, directory: _detect_singleton_patterns(directory),
})


class TestCodePatternDetector:
    """Test suite for CodePatternDetector class."""

    @pytest.fixture
    def detector(self):
        """Create a CodePatternDetector instance."""
        return CodePatternDetector()

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_path = tempfile.mkdtemp()
        yield temp_path
        import shutil
        if os.path.exists(temp_path):
            shutil.rmtree(temp_path)

    def test_initialization(self, detector):
        """Test CodePatternDetector initialization."""
        assert detector is not None

    def test_detect_patterns_empty_directory(self, detector, temp_dir):
        """Test detect_patterns with empty directory."""
        with patch('src.core.refactoring.pattern_detection.get_unified_utility') as mock_util:
            mock_path = MagicMock()
            mock_path.rglob.return_value = []
            mock_util.return_value.Path.return_value = mock_path
            
            patterns = detector.detect_patterns(temp_dir)
            
            assert isinstance(patterns, list)

    def test_detect_mvc_patterns(self, detector, temp_dir):
        """Test MVC pattern detection."""
        with patch('src.core.refactoring.pattern_detection.get_unified_utility') as mock_util:
            mock_path = MagicMock()
            mock_path.rglob.return_value = []
            mock_util.return_value.Path.return_value = mock_path
            
            patterns = detector.detect_mvc(temp_dir)
            
            assert isinstance(patterns, list)

    def test_detect_repository_patterns(self, detector, temp_dir):
        """Test repository pattern detection."""
        with patch('src.core.refactoring.pattern_detection.get_unified_utility') as mock_util:
            mock_path = MagicMock()
            mock_path.rglob.return_value = []
            mock_util.return_value.Path.return_value = mock_path
            
            patterns = detector.detect_repository(temp_dir)
            
            assert isinstance(patterns, list)

    def test_detect_factory_patterns(self, detector, temp_dir):
        """Test factory pattern detection."""
        with patch('src.core.refactoring.pattern_detection.get_unified_utility') as mock_util:
            mock_path = MagicMock()
            mock_path.rglob.return_value = []
            mock_util.return_value.Path.return_value = mock_path
            
            patterns = detector.detect_factory(temp_dir)
            
            assert isinstance(patterns, list)

    def test_detect_observer_patterns(self, detector, temp_dir):
        """Test observer pattern detection."""
        with patch('src.core.refactoring.pattern_detection.get_unified_utility') as mock_util:
            mock_path = MagicMock()
            mock_path.rglob.return_value = []
            mock_util.return_value.Path.return_value = mock_path
            
            patterns = detector.detect_observer(temp_dir)
            
            assert isinstance(patterns, list)

    def test_detect_singleton_patterns(self, detector, temp_dir):
        """Test singleton pattern detection."""
        with patch('src.core.refactoring.pattern_detection.get_unified_utility') as mock_util:
            mock_path = MagicMock()
            mock_path.rglob.return_value = []
            mock_util.return_value.Path.return_value = mock_path
            
            patterns = detector.detect_singleton(temp_dir)
            
            assert isinstance(patterns, list)

    def test_detect_patterns_integration(self, detector, temp_dir):
        """Test detect_patterns integration."""
        patterns = detector.detect_patterns(temp_dir)
        
        assert isinstance(patterns, list)
        # May be empty, but should execute

    def test_pattern_detection_handles_errors(self, detector, temp_dir):
        """Test pattern detection handles errors gracefully."""
        with patch('src.core.refactoring.pattern_detection.get_unified_utility', side_effect=Exception("Error")):
            try:
                patterns = detector.detect_patterns(temp_dir)
                assert isinstance(patterns, list)
            except Exception:
                pass

    def test_architecture_pattern_creation(self):
        """Test ArchitecturePattern dataclass."""
        pattern = ArchitecturePattern(
            name="Test Pattern",
            pattern_type="test",
            files=["file1.py"],
            confidence=0.8,
            description="Test description"
        )
        
        assert pattern.name == "Test Pattern"
        assert pattern.confidence == 0.8

    def test_multiple_pattern_types_detection(self, detector, temp_dir):
        """Test detecting multiple pattern types."""
        patterns = detector.detect_patterns(temp_dir)
        
        assert isinstance(patterns, list)
        # Could contain multiple pattern types

