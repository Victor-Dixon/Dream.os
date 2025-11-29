"""
Unit tests for refactoring/refactoring_analyzer.py - HIGH PRIORITY

Tests RefactoringAnalyzer class functionality.
Note: Maps to analysis_tools_core.py ArchitectureAnalyzer.
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

# Import the analyzer
from src.core.refactoring.analysis_tools_core import ArchitectureAnalyzer
from src.core.refactoring.analysis_tools_models import (
    FileAnalysis,
    DuplicateFile,
    ArchitecturePattern,
    RefactoringSuggestion
)

# Alias for test purposes
RefactoringAnalyzer = ArchitectureAnalyzer


class TestRefactoringAnalyzer:
    """Test suite for RefactoringAnalyzer class."""

    @pytest.fixture
    def analyzer(self, tmp_path):
        """Create a RefactoringAnalyzer instance."""
        return RefactoringAnalyzer(str(tmp_path))

    @pytest.fixture
    def sample_file(self, tmp_path):
        """Create a sample Python file for testing."""
        file_path = tmp_path / "test_file.py"
        file_path.write_text("""class TestClass:
    def __init__(self):
        pass
    
    def test_method(self):
        return True
""")
        return str(file_path)

    def test_initialization(self, tmp_path):
        """Test RefactoringAnalyzer initialization."""
        analyzer = RefactoringAnalyzer(str(tmp_path))
        
        assert analyzer.project_root == str(tmp_path)
        assert analyzer.analyzed_files == {}

    def test_initialization_default(self):
        """Test initialization with default project root."""
        analyzer = RefactoringAnalyzer()
        
        assert analyzer.project_root == "."

    def test_analyze_file_success(self, analyzer, sample_file):
        """Test analyze_file with valid file."""
        analysis = analyzer.analyze_file(sample_file)
        
        assert isinstance(analysis, FileAnalysis)
        assert analysis.file_path == sample_file
        assert analysis.line_count > 0
        assert len(analysis.classes) > 0
        assert len(analysis.functions) > 0

    def test_analyze_file_nonexistent(self, analyzer):
        """Test analyze_file with non-existent file."""
        analysis = analyzer.analyze_file("nonexistent.py")
        
        assert isinstance(analysis, FileAnalysis)
        assert analysis.line_count == 0

    def test_analyze_file_v2_compliance(self, analyzer, tmp_path):
        """Test analyze_file detects V2 compliance."""
        # Create a small file (compliant)
        small_file = tmp_path / "small.py"
        small_file.write_text("def func(): pass\n")
        
        analysis = analyzer.analyze_file(str(small_file))
        
        assert analysis.v2_compliance is True

    def test_analyze_file_v2_violation(self, analyzer, tmp_path):
        """Test analyze_file detects V2 violation."""
        # Create a large file (violation)
        large_content = "\n".join([f"# Line {i}" for i in range(400)])
        large_file = tmp_path / "large.py"
        large_file.write_text(large_content)
        
        analysis = analyzer.analyze_file(str(large_file))
        
        assert analysis.v2_compliance is False

    def test_find_duplicates_no_duplicates(self, analyzer, tmp_path):
        """Test find_duplicates with no duplicates."""
        file1 = tmp_path / "file1.py"
        file2 = tmp_path / "file2.py"
        file1.write_text("def func1(): pass")
        file2.write_text("def func2(): pass")
        
        duplicates = analyzer.find_duplicates([str(file1), str(file2)])
        
        assert isinstance(duplicates, list)
        assert len(duplicates) == 0

    def test_find_duplicates_with_duplicates(self, analyzer, tmp_path):
        """Test find_duplicates with duplicate files."""
        file1 = tmp_path / "file1.py"
        file2 = tmp_path / "file2.py"
        content = "def func(): pass"
        file1.write_text(content)
        file2.write_text(content)
        
        duplicates = analyzer.find_duplicates([str(file1), str(file2)])
        
        assert isinstance(duplicates, list)
        assert len(duplicates) > 0

    def test_identify_patterns_class_based(self, analyzer, tmp_path):
        """Test identify_patterns detects class-based architecture."""
        file_path = tmp_path / "class_file.py"
        file_path.write_text("class MyClass:\n    def __init__(self): pass")
        
        patterns = analyzer.identify_patterns([str(file_path)])
        
        assert isinstance(patterns, list)
        assert len(patterns) > 0

    def test_identify_patterns_functional(self, analyzer, tmp_path):
        """Test identify_patterns detects functional architecture."""
        file_path = tmp_path / "func_file.py"
        file_path.write_text("def my_func(): pass")
        
        patterns = analyzer.identify_patterns([str(file_path)])
        
        assert isinstance(patterns, list)

    def test_generate_suggestions_v2_violation(self, analyzer, tmp_path):
        """Test generate_suggestions for V2 violation."""
        large_file = tmp_path / "large.py"
        large_content = "\n".join([f"# Line {i}" for i in range(400)])
        large_file.write_text(large_content)
        
        analysis = analyzer.analyze_file(str(large_file))
        suggestions = analyzer.generate_suggestions(analysis)
        
        assert isinstance(suggestions, list)
        assert len(suggestions) > 0

    def test_generate_suggestions_high_complexity(self, analyzer, tmp_path):
        """Test generate_suggestions for high complexity."""
        complex_file = tmp_path / "complex.py"
        complex_content = "\n".join([
            "if True:",
            "    for i in range(10):",
            "        while False:",
            "            try:",
            "                pass",
            "            except:",
            "                pass"
        ])
        complex_file.write_text(complex_content)
        
        analysis = analyzer.analyze_file(str(complex_file))
        suggestions = analyzer.generate_suggestions(analysis)
        
        assert isinstance(suggestions, list)

    def test_extract_classes(self, analyzer):
        """Test _extract_classes method."""
        content = "class Class1:\n    pass\nclass Class2:\n    pass"
        
        classes = analyzer._extract_classes(content)
        
        assert len(classes) == 2
        assert "Class1" in classes
        assert "Class2" in classes

    def test_extract_functions(self, analyzer):
        """Test _extract_functions method."""
        content = "def func1(): pass\ndef func2(): pass"
        
        functions = analyzer._extract_functions(content)
        
        assert len(functions) == 2
        assert "func1" in functions
        assert "func2" in functions

    def test_extract_imports(self, analyzer):
        """Test _extract_imports method."""
        content = "import os\nfrom pathlib import Path"
        
        imports = analyzer._extract_imports(content)
        
        assert len(imports) == 2
        assert any("import os" in imp for imp in imports)
        assert any("from pathlib" in imp for imp in imports)

    def test_calculate_complexity(self, analyzer):
        """Test _calculate_complexity method."""
        simple_content = "def func(): pass"
        
        complexity = analyzer._calculate_complexity(simple_content)
        
        assert 0.0 <= complexity <= 1.0

    def test_calculate_complexity_with_conditionals(self, analyzer):
        """Test _calculate_complexity with conditionals."""
        complex_content = "if True:\n    for i in range(10):\n        while False:\n            pass"
        
        complexity = analyzer._calculate_complexity(complex_content)
        
        assert complexity > 0.0

